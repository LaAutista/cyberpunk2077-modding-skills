"""Copied synthetic GLBs: skin permutation, inverse-bind and animated deformation controls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skin',ROOT/'skills/cyberpunk2077-modding/scripts/comparison/skin_deformation.py');skin=importlib.util.module_from_spec(spec);spec.loader.exec_module(skin)

def write(path,permuted=False,wrong_bind=False):
    binary=bytearray();views=[];accessors=[]
    def values(rows,kind,typ):
        a=np.asarray(rows,dtype={5126:'<f4',5123:'<u2'}[kind]);binary.extend(b'\0'*(-len(binary)%4));start=len(binary);binary.extend(a.tobytes());views.append({'buffer':0,'byteOffset':start,'byteLength':a.nbytes});accessors.append({'bufferView':len(views)-1,'componentType':kind,'count':len(a),'type':typ});return len(accessors)-1
    position=values([[1,0,0],[2,0,0],[1,1,0]],5126,'VEC3')
    joints=values([[1 if permuted else 0,0 if permuted else 1,0,0]]*3,5123,'VEC4')
    weights=values([[.5,.5,0,0]]*3,5126,'VEC4')
    matrices=[np.eye(4),np.eye(4)];matrices[1][0,3]=-1
    if permuted:matrices.reverse()
    if wrong_bind:matrices[0][1,3]=.05
    ib=values([m.T.ravel() for m in matrices],5126,'MAT4')
    times=values([[0],[1]],5126,'SCALAR');rotations=values([[0,0,0,1],[0,0,np.sin(np.pi/4),np.cos(np.pi/4)]],5126,'VEC4')
    doc={'asset':{'version':'2.0'},'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors,'nodes':[{'name':'mesh','mesh':0,'skin':0},{'name':'root','children':[2]},{'name':'child','translation':[1,0,0]}],'skins':[{'joints':[2,1] if permuted else [1,2],'inverseBindMatrices':ib}],'meshes':[{'name':'fixture','primitives':[{'attributes':{'POSITION':position,'JOINTS_0':joints,'WEIGHTS_0':weights}}]}],'animations':[{'name':'bend','extras':{'animationType':'Normal'},'samplers':[{'input':times,'output':rotations,'interpolation':'LINEAR'}],'channels':[{'sampler':0,'target':{'node':2,'path':'rotation'}}]}]}
    text=json.dumps(doc).encode();text+=b' '*(-len(text)%4);binary.extend(b'\0'*(-len(binary)%4));path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(text)+len(binary))+struct.pack('<I4s',len(text),b'JSON')+text+struct.pack('<I4s',len(binary),b'BIN\0')+binary)

with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);source=root/'source.glb';good=root/'permuted.glb';bad=root/'bad-bind.glb'
    write(source);write(good,True);write(bad,True,True);before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
    result=skin.compare(source,good);assert result['passed'] and not result['primitiveResults'][0]['indicesPreserved']
    animated=skin.compare(source,good,source,['bend']);assert animated['passed'] and animated['maxSourceMotionM']>.1
    negative=skin.compare(source,bad,source,['bend']);assert not negative['passed'] and not negative['bindMappingPassed'] and not negative['sampledDeformationPassed']
    bad_doc=skin.GLB(good);bad_doc.doc['skins'][0]['joints']=[1,1]
    try:bad_doc.primitives();raise AssertionError('duplicate joint mapping accepted')
    except ValueError:pass
    try:skin.compare(source,good,source,['not-a-clip']);raise AssertionError('missing clip accepted')
    except ValueError:pass
    assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
print('PASS: named joint permutation equivalence, inverse-bind fault rejection with unchanged weights, sampled multi-joint/Normal-clip deformation, duplicate mapping/missing clip refusal and unchanged copied inputs.')
