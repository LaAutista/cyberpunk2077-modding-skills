"""Bounded embedded-GLB skin/bind/LBS comparison; no native or gameplay claim.

Row correspondence must be explicit. Supports float/normalized integer weights,
local TRS/matrices, LINEAR/STEP Normal clips. Rejects sparse/external/compressed data.
"""
import hashlib
import json
from pathlib import Path
import struct
import numpy as np


def rotation(q):
    q=np.asarray(q,dtype=float)
    if not np.isfinite(q).all() or np.linalg.norm(q)==0:raise ValueError('Invalid quaternion')
    x,y,z,w=q/np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def trs(node):
    if 'matrix' in node:
        m=np.asarray(node['matrix'],dtype=float).reshape(4,4).T
    else:
        m=np.eye(4);m[:3,:3]=rotation(node.get('rotation',[0,0,0,1]))@np.diag(node.get('scale',[1,1,1]));m[:3,3]=node.get('translation',[0,0,0])
    if not np.isfinite(m).all():raise ValueError('Non-finite transform')
    return m


class GLB:
    def __init__(self,path):
        self.path=Path(path);data=self.path.read_bytes()
        if len(data)<28 or struct.unpack_from('<4sII',data)!=(b'glTF',2,len(data)):raise ValueError('Invalid GLB')
        chunks=[];offset=12
        while offset<len(data):
            size,kind=struct.unpack_from('<I4s',data,offset)
            if size%4 or offset+8+size>len(data):raise ValueError('Invalid GLB chunk')
            chunks.append((kind,data[offset+8:offset+8+size]));offset+=8+size
        if [c[0] for c in chunks]!=[b'JSON',b'BIN\0']:raise ValueError('Expected embedded JSON/BIN GLB')
        self.doc=json.loads(chunks[0][1]);self.binary=chunks[1][1]
        buffers=self.doc.get('buffers',[])
        if len(buffers)!=1 or 'uri' in buffers[0] or not 0<=len(self.binary)-buffers[0]['byteLength']<=3:raise ValueError('External/ambiguous buffer')
        self.nodes=self.doc['nodes'];self.names={};self.parents={}
        joint_nodes={j for skin in self.doc.get('skins',[]) for j in skin['joints']}
        for i,node in enumerate(self.nodes):
            name=node.get('name')
            if not name:raise ValueError('Named nodes required for mapping')
            if name in self.names:
                old=self.names[name]
                if (i in joint_nodes)==(old in joint_nodes):raise ValueError('Ambiguous joint/node name: '+name)
                if i in joint_nodes:self.names[name]=i
            else:self.names[name]=i
            for child in node.get('children',[]):
                if not 0<=child<len(self.nodes) or child in self.parents:raise ValueError('Invalid/multiple parents')
                self.parents[child]=i
        self.bind=self.world([trs(n) for n in self.nodes])

    def values(self,index):
        a=self.doc['accessors'][index]
        if 'sparse' in a or 'bufferView' not in a:raise ValueError('Sparse/implicit accessor unsupported')
        v=self.doc['bufferViews'][a['bufferView']]
        if v.get('buffer',0)!=0:raise ValueError('External accessor')
        dtype,width,divisor={5121:('<u1',1,255),5123:('<u2',2,65535),5125:('<u4',4,4294967295),5126:('<f4',4,None)}[a['componentType']]
        components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        stride=v.get('byteStride',width*components);start=a.get('byteOffset',0);count=a['count'];base=v.get('byteOffset',0)
        if count<=0 or stride<width*components or start<0 or start+(count-1)*stride+width*components>v['byteLength'] or base<0 or base+v['byteLength']>self.doc['buffers'][0]['byteLength']:raise ValueError('Accessor out of bounds')
        result=np.ndarray((count,components),dtype=dtype,buffer=self.binary,offset=base+start,strides=(stride,width)).astype(float)
        if a.get('normalized'):
            if divisor is None:raise ValueError('Normalized float accessor')
            result/=divisor
        if not np.isfinite(result).all():raise ValueError('Non-finite accessor')
        return result

    def world(self,local):
        result={};visiting=set()
        def visit(i):
            if i in visiting:raise ValueError('Cyclic hierarchy')
            if i not in result:
                visiting.add(i);result[i]=visit(self.parents[i])@local[i] if i in self.parents else local[i];visiting.remove(i)
            return result[i]
        for i in range(len(self.nodes)):visit(i)
        return {name:result[i] for name,i in self.names.items()}

    def primitives(self):
        result={}
        for node in self.nodes:
            if 'mesh' not in node or 'skin' not in node:continue
            skin=self.doc['skins'][node['skin']];indices=skin['joints'];names=[self.nodes[i]['name'] for i in indices]
            if len(names)!=len(set(names)):raise ValueError('Duplicate skin joints')
            if 'inverseBindMatrices' not in skin:raise ValueError('Explicit inverse binds required by this diagnostic')
            ib_access=self.doc['accessors'][skin['inverseBindMatrices']]
            if ib_access['type']!='MAT4' or ib_access['componentType']!=5126:raise ValueError('Inverse binds require float MAT4 accessors')
            inverse=self.values(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
            if len(inverse)!=len(names) or not np.allclose(inverse[:,3,:],[0,0,0,1],atol=1e-6):raise ValueError('Invalid inverse-bind count/affine row')
            if np.any(np.abs(np.linalg.det(inverse))<1e-12):raise ValueError('Singular inverse bind')
            for pi,primitive in enumerate(self.doc['meshes'][node['mesh']]['primitives']):
                if primitive.get('extensions') or primitive.get('targets'):raise ValueError('Compressed/extended/morph primitive unsupported')
                attr=primitive['attributes'];positions=self.values(attr['POSITION']);pairs=[]
                js=sorted(k for k in attr if k.startswith('JOINTS_'));ws={k for k in attr if k.startswith('WEIGHTS_')}
                if not js or ws!={j.replace('JOINTS_','WEIGHTS_') for j in js}:raise ValueError('Unpaired skin attributes')
                for key in js:
                    ja=self.doc['accessors'][attr[key]];wa=self.doc['accessors'][attr[key.replace('JOINTS_','WEIGHTS_')]]
                    if ja['type']!='VEC4' or ja['componentType'] not in (5121,5123) or ja.get('normalized'):raise ValueError('Joint indices require unnormalized unsigned VEC4 accessors')
                    if wa['type']!='VEC4' or wa['componentType'] not in (5121,5123,5126) or (wa['componentType']!=5126 and not wa.get('normalized')):raise ValueError('Unsupported weight accessor')
                    joints=self.values(attr[key]);weights=self.values(attr[key.replace('JOINTS_','WEIGHTS_')])
                    if joints.shape!=weights.shape or joints.shape!=(len(positions),4) or np.any(joints!=np.floor(joints)) or np.any(joints<0) or np.any(joints>=len(names)) or np.any(weights<0):raise ValueError('Invalid joint/weight rows')
                    pairs.append((joints.astype(int),weights))
                if not np.allclose(sum(w.sum(axis=1) for _,w in pairs),1,atol=1e-5,rtol=0):raise ValueError('Unnormalized skin weights')
                key=(node['name'],pi)
                if key in result:raise ValueError('Ambiguous mesh correspondence')
                result[key]={'names':names,'inverse':inverse,'positions':positions,'pairs':pairs}
        if not result:raise ValueError('No skinned primitives')
        return result

    def clip(self,name):
        matches=[a for a in self.doc.get('animations',[]) if a['name']==name]
        if len(matches)!=1:raise ValueError('Missing/duplicate animation clip '+name)
        clip=matches[0]
        if clip.get('extras',{}).get('animationType')!='Normal':raise ValueError('Only explicitly Normal clips supported')
        return clip

    def pose(self,clip,time):
        nodes=[dict(n) for n in self.nodes];seen=set()
        for channel in clip['channels']:
            sampler=clip['samplers'][channel['sampler']];target=channel['target'];index,field=target['node'],target['path'];mode=sampler.get('interpolation','LINEAR')
            if not 0<=index<len(nodes) or mode not in ('LINEAR','STEP') or field not in ('translation','rotation','scale') or (index,field) in seen or 'matrix' in nodes[index]:raise ValueError('Unsupported/duplicate animation channel')
            seen.add((index,field));times=self.values(sampler['input']).ravel();values=self.values(sampler['output'])
            if len(times)!=len(values) or not np.all(np.diff(times)>0) or times[0]<0:raise ValueError('Invalid animation times')
            left=max(0,min(len(times)-1,int(np.searchsorted(times,time,side='right'))-1));right=min(left+1,len(times)-1)
            f=0 if mode=='STEP' or times[left]==times[right] else np.clip((time-times[left])/(times[right]-times[left]),0,1)
            a,b=values[left],values[right]
            if field=='rotation':
                a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);dot=float(a@b)
                if dot<0:b=-b;dot=-dot
                if dot>.9995:value=a+f*(b-a);value/=np.linalg.norm(value)
                else:angle=np.arccos(np.clip(dot,-1,1));value=(np.sin((1-f)*angle)*a+np.sin(f*angle)*b)/np.sin(angle)
            else:value=a*(1-f)+b*f
            nodes[index][field]=value
        return self.world([trs(n) for n in nodes])

    def stress(self,time,joints):
        local=[trs(n) for n in self.nodes]
        for name in joints:
            i=self.names[name];digest=hashlib.sha256(name.encode()).digest();axis=digest[0]%3;amplitude=np.sin(np.pi*time);angle=.10*amplitude*(.5+digest[1]/255)
            q=np.zeros(4);q[axis]=np.sin(angle/2);q[3]=np.cos(angle/2);delta=np.eye(4);delta[:3,:3]=rotation(q);delta[(axis+1)%3,3]=.002*amplitude*np.sin(2*np.pi*time+digest[2]/255)
            local[i]=local[i]@delta
        return self.world(local)


def deform(primitive,world):
    palette=np.asarray([world[name]@inverse for name,inverse in zip(primitive['names'],primitive['inverse'])]);positions=np.c_[primitive['positions'],np.ones(len(primitive['positions']))];result=np.zeros_like(positions)
    for joints,weights in primitive['pairs']:
        for column in range(4):result+=weights[:,column,None]*np.einsum('nij,nj->ni',palette[joints[:,column]],positions)
    if not np.isfinite(result).all():raise ValueError('Non-finite deformation')
    return result[:,:3]


def compare(source_path,output_path,animation_path=None,clips=None,tolerance=1e-5):
    source,output=GLB(source_path),GLB(output_path);before,after=source.primitives(),output.primitives()
    if before.keys()!=after.keys():raise ValueError('Mesh/primitive correspondence changed')
    joints=set(n for p in before.values() for n in p['names']);rows=[]
    for key,old in before.items():
        new=after[key]
        if old['positions'].shape!=new['positions'].shape or np.max(np.abs(old['positions']-new['positions']))>1e-6:raise ValueError('Vertex correspondence changed')
        if set(old['names'])!=set(new['names']):raise ValueError('Skin joint-name mapping changed')
        mapping=[new['names'].index(n) for n in old['names']]
        rows.append({'mesh':key[0],'primitive':key[1],'vertices':len(old['positions']),'joints':len(old['names']),'jointIndexMapping':mapping,'indicesPreserved':mapping==list(range(len(mapping))),'maxInverseBindComponentError':float(np.max(np.abs(old['inverse']-new['inverse'][mapping]))),'maxBindJointWorldComponentError':max(float(np.max(np.abs(source.bind[n]-output.bind[n]))) for n in old['names']),'maxBindDeformationErrorM':float(np.linalg.norm(deform(old,source.bind)-deform(new,output.bind),axis=1).max())})
    samples=[];animation=GLB(animation_path) if animation_path else None;native_bind_error=None
    if animation:
        if not clips:raise ValueError('Select explicit representative Normal clips')
        if not joints<=animation.names.keys():raise ValueError('Animation lacks required skin joints; no implicit corrective/retarget mapping: '+', '.join(sorted(joints-animation.names.keys())))
        native_bind_error=max(float(np.max(np.abs(source.bind[n]-animation.bind[n]))) for n in joints)
        if native_bind_error>tolerance:raise ValueError('Animation/model bind frames differ; no implicit retargeting: '+str(native_bind_error))
        for name in clips:
            clip=animation.clip(name);end=max(float(animation.values(s['input'])[-1,0]) for s in clip['samplers'])
            for t in np.linspace(0,end,9):
                pose=animation.pose(clip,float(t));samples.append((name,float(t),pose,pose))
    else:
        for t in np.linspace(0,1,9):samples.append(('synthetic-local-stress',float(t),source.stress(float(t),joints),output.stress(float(t),joints)))
    samples_report=[];max_motion=0
    for name,t,a,b in samples:
        error=0
        for key,old in before.items():
            posed=deform(old,a);max_motion=max(max_motion,float(np.linalg.norm(posed-deform(old,source.bind),axis=1).max()));error=max(error,float(np.linalg.norm(posed-deform(after[key],b),axis=1).max()))
        samples_report.append({'clip':name,'timeSeconds':t,'maxVertexErrorM':error})
    bind_pass=all(r['maxInverseBindComponentError']<=tolerance and r['maxBindJointWorldComponentError']<=tolerance and r['maxBindDeformationErrorM']<=tolerance for r in rows)
    motion_pass=all(r['maxVertexErrorM']<=tolerance for r in samples_report)
    return {'schema':1,'scope':'Copied GLB named joint mapping, inverse binds and sampled CPU linear-blend skinning; no native/gameplay acceptance','passed':bind_pass and motion_pass,'bindMappingPassed':bind_pass,'sampledDeformationPassed':motion_pass,'toleranceM':tolerance,'primitiveResults':rows,'sampledPoses':samples_report,'maxSourceMotionM':max_motion,'animationSource':'supplied Normal clip; bind frames verified' if animation else 'deterministic synthetic multi-joint stress clip; not native motion','animationBindFrameError':native_bind_error,'limits':['Identical mesh/primitive/row correspondence is required.','Joint permutation is reported/remapped by unique names; native joint-index preservation is not established when order changes.','No additive layers, animation graph, IK, procedural effects, materials, mesh cooking, rendered review or gameplay.','Only declared sample times are checked; root hierarchy warnings remain separate and cannot be waived.']}


def main():
    import argparse
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from diagnostic_dependencies import preflight,require
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument('--source',type=Path,required=True);args.add_argument('--candidate',type=Path,required=True);args.add_argument('--animation',type=Path);args.add_argument('--clip',action='append');args.add_argument('--output',type=Path,required=True)
    parsed=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    inputs=[p.resolve() for p in (parsed.source,parsed.candidate,parsed.animation) if p is not None]
    if parsed.output.resolve() in inputs:raise ValueError('Report must not overwrite input')
    if parsed.output.exists() or parsed.output.is_symlink():raise ValueError('Report already exists; preserved')
    dependencies=require(preflight('skin',numpy=np.__version__))
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    result=compare(parsed.source,parsed.candidate,parsed.animation,parsed.clip)
    result['dependencyPreflight']=dependencies;result['inputSHA256']=before
    if before!={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}:raise ValueError('Input bytes changed')
    with parsed.output.open('x') as target:target.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'scope':result['scope'],'samples':len(result['sampledPoses'])}))
    if not result['passed']:raise SystemExit(1)


if __name__=='__main__':main()
