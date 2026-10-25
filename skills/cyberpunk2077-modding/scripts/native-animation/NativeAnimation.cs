// Copied-asset animation adapter for installed WolvenKit9.0.1; no live resolver/config mutation.
using System.Reflection;
using System.Runtime.Loader;
using System.Runtime.CompilerServices;
using System.Text;
using WolvenKit.RED4.Archive.IO;
using WolvenKit.RED4.Archive.CR2W;
using WolvenKit.RED4.Types;
using WolvenKit.Modkit.RED4;
using WolvenKit.Modkit.RED4.RigFile;
using WolvenKit.Common.Model.Arguments;
using WolvenKit.Core.Interfaces;
using SharpGLTF.Schema2;

class Program {
static string Library="";
static int Main(string[] args) {
try {
if(args.Length<5)throw new Exception("Usage: LIBRARY export|import NATIVE RIG GLB [OUTPUT_NATIVE|CLIP]");
Library=Path.GetFullPath(args[0]);
var version=System.Diagnostics.FileVersionInfo.GetVersionInfo(Path.Combine(Library,"WolvenKit.Modkit.dll")).ProductVersion;
if(version is null || !(version=="9.0.1" || version.StartsWith("9.0.1+") || version.StartsWith("9.0.1.")))throw new Exception("This adapter requires WolvenKit.Modkit 9.0.1; found "+version);
AssemblyLoadContext.Default.Resolving += (c,n)=> {var p=Path.Combine(Library,n.Name+".dll");return File.Exists(p)?c.LoadFromAssemblyPath(p):null;};
Run(args);return 0;
}catch(Exception e){Console.Error.WriteLine(e);return 1;}
}
[MethodImpl(MethodImplOptions.NoInlining)]
static void Run(string[] args) {
var logger=(ILoggerService)DispatchProxy.Create(typeof(ILoggerService),typeof(LogProxy));
var tool=(ModTools)RuntimeHelpers.GetUninitializedObject(typeof(ModTools));
typeof(ModTools).GetField("_loggerService",BindingFlags.NonPublic|BindingFlags.Instance)!.SetValue(tool,logger);
CR2WFile Read(string p){using var s=File.OpenRead(p);using var r=new CR2WReader(s){LoggerService=logger};var status=r.ReadFile(out var doc,true);if(status.ToString()!="NoError")throw new Exception("Read failed: "+status);return doc!;}
var native=Read(args[2]);var rigFile=Read(args[3]);
if(native.RootChunk is not animAnimSet anims)throw new Exception("Expected animAnimSet");
if(args[1]=="export") {
if(File.Exists(args[4]))throw new Exception("Refusing to overwrite an existing export");
if(args.Length>5){var selected=anims.Animations.Where(a=>a.Chunk!.Animation.Chunk!.Name.ToString()==args[5]).ToArray();if(selected.Length!=1)throw new Exception("Expected one selected clip");anims.Animations.Clear();foreach(var a in selected)anims.Animations.Add(a);}
var model=ModelRoot.CreateModel();
if(!tool.GetAnimation(native,rigFile,Path.GetFileName(args[2]),ref model,true,true,true))throw new Exception("Export failed");
model.SaveGLB(args[4]);
} else if(args[1]=="import") {
if(args.Length!=6)throw new Exception("Import requires an output native path");
if(Path.GetFullPath(args[2])==Path.GetFullPath(args[5]))throw new Exception("Refusing to overwrite source");
var rig=RIG.ProcessRig(rigFile)??throw new Exception("Bad rig");var model=ModelRoot.Load(args[4]);
var names=anims.Animations.Select(a=>a.Chunk!.Animation.Chunk!.Name.ToString()).ToHashSet();
if(model.LogicalAnimations.Select(a=>a.Name).Distinct().Count()!=model.LogicalAnimations.Count)throw new Exception("Duplicate selected clip names");
var supportedTypes=new HashSet<string>{"Normal","Additive","AdditiveWithoutFirstFrame"};
foreach(var incoming in model.LogicalAnimations) {
 var type=incoming.Extras?["animationType"]?.ToString()??"";
 if(!supportedTypes.Contains(type)||incoming.Extras?["rootMotionType"]?.ToString()!="None")throw new Exception("Selected imports require a supported animation type and rootMotionType None");
 var original=anims.Animations.SingleOrDefault(e=>e.Chunk!.Animation.Chunk!.Name.ToString()==incoming.Name)?.Chunk?.Animation.Chunk;
 if(original is null||original.AnimationType.ToString()!=type)throw new Exception("Selected animation type must match original target: "+incoming.Name);
 if(original.MotionExtraction?.Chunk is not null)throw new Exception("Root-motion adaptation is outside this selected null-root-motion adapter");
 if(type!="Normal"&&model.Extras?["betaAdditiveRepresentation"]?.ToString()!="raw-delta-v1")throw new Exception("Run beta prepare before importing bind-relative additive clips");
}
if(model.LogicalAnimations.Count==0||model.LogicalAnimations.Any(a=>!names.Contains(a.Name)))throw new Exception("Import must select existing named clips; no empty or new clip imports");
// Import selected clips only: installed CopyOldAnim cannot preserve inline
// vanilla recoil buffers (sentinel external address). Reattach originals below.
var originalEntries=anims.Animations.ToArray();
var originalChunks=anims.AnimationDataChunks.ToArray();
var selectedNames=model.LogicalAnimations.Select(a=>a.Name).ToHashSet();
anims.Animations.Clear();
foreach(var entry in originalEntries.Where(e=>selectedNames.Contains(e.Chunk!.Animation.Chunk!.Name.ToString())))anims.Animations.Add(entry);
var importArgs=new GltfImportArgs{ImportFormat=GltfImportAsFormat.Anims,AdditiveStripLocalTransform=false};
var method=typeof(ModTools).GetMethod("PutAnimations",BindingFlags.NonPublic|BindingFlags.Instance)!;
object?[] parameters={anims,rig,model,Path.GetFileName(args[4]),Path.GetFileName(args[3]),importArgs};
if(!(bool)method.Invoke(tool,parameters)!)throw new Exception("Import failed");
anims=(animAnimSet)parameters[0]!;
// WKit9.0.1 RQuaternionNormalize snaps W==1 to identity even when XYZ is
// nonzero. Prepared additive rotations are already raw deltas, so the same repair applies.
// The independent raw-key reader also checks the compressed-export counterpart.
int repaired=0;
foreach(var incoming in model.LogicalAnimations) {
var desc=anims.Animations.Single(a=>a.Chunk!.Animation.Chunk!.Name.ToString()==incoming.Name).Chunk!.Animation.Chunk!;
if(!supportedTypes.Contains(desc.AnimationType.ToString()))throw new Exception("Unexpected selected animation type");
var affected=incoming.Channels.Where(c=>c.TargetNodePath==PropertyPath.rotation)
 .SelectMany(c=>c.GetRotationSampler().GetLinearKeys().Where(k=>k.Value.W==1f&&(k.Value.X!=0f||k.Value.Y!=0f||k.Value.Z!=0f)).Select(k=>(Channel:c,Key:k))).ToArray();
if(affected.Length==0)continue;
if(desc.AnimBuffer.Chunk is not animAnimationBufferCompressed buffer || !buffer.HasRawRotations || buffer.NumAnimKeys!=0 || buffer.DataAddress.FsetInBytes!=0)
 throw new Exception("Tiny rotation repair requires selected raw compressed keys without offsets/quantized keys");
foreach(var a in affected) {
int joint=Array.IndexOf(rig.Names!,a.Channel.TargetNode.Name);
var rotationKeys=a.Channel.GetRotationSampler().InterpolationMode.ToString()=="STEP"?buffer.ConstAnimKeys.OfType<animKeyRotation>():buffer.AnimKeysRaw.OfType<animKeyRotation>();
var key=rotationKeys.Single(k=>k.Idx==joint&&k.Time==a.Key.Key);
if(key.Rotation!=System.Numerics.Quaternion.Identity)throw new Exception("Expected demonstrated identity snap before repair");
var q=System.Numerics.Quaternion.Normalize(a.Key.Value);
key.Rotation=new System.Numerics.Quaternion(q.X,-q.Z,q.Y,q.W);repaired++;
}
var oldSize=buffer.DataAddress.ZeInBytes;buffer.WriteBuffer();
if(buffer.TempBuffer.Buffer.MemSize!=oldSize)throw new Exception("Rotation repair changed native chunk size");
anims.AnimationDataChunks[(int)(uint)buffer.DataAddress.UnkIndex].Buffer=new SerializationDeferredDataBuffer(buffer.TempBuffer.Buffer.GetBytes());
}
Console.Error.WriteLine($"Preserved {repaired} tiny quaternion keys affected by installed identity snapping");
var imported=anims.Animations.ToDictionary(e=>e.Chunk!.Animation.Chunk!.Name.ToString());
var importedChunks=anims.AnimationDataChunks.ToArray();
foreach(var entry in imported.Values){
 var importedDesc=entry.Chunk!.Animation.Chunk!;
 var originalEntry=originalEntries.Single(e=>e.Chunk!.Animation.Chunk!.Name==importedDesc.Name);
 var originalDesc=originalEntry.Chunk!.Animation.Chunk!;
 var authored=model.LogicalAnimations.Single(a=>a.Name==importedDesc.Name.ToString());
 // Installed BuildEventsContainer treats [] as 'copy old'. Explicit [] in this
 // adapter is an intentional removal; null/absent still uses stock behavior.
 if(authored.Extras?["animEvents"] is System.Text.Json.Nodes.JsonArray eventList && eventList.Count==0)
  entry.Chunk.Events=new(new animEventsContainer());
 // PutAnimations creates a non-null handle containing null for RootMotionType.None.
 // Preserve the source's actual null representation where both have no motion data.
 if(originalDesc.MotionExtraction is null && importedDesc.MotionExtraction?.Chunk is null)importedDesc.MotionExtraction=null!;
 if(originalEntry.Chunk!.Events is null && entry.Chunk.Events?.Chunk is null)entry.Chunk.Events=null!;
 if(importedDesc.AnimBuffer.Chunk is not animAnimationBufferCompressed buf)throw new Exception("Expected explicitly prepared compressed selected clip");
 buf.DataAddress.UnkIndex=(uint)buf.DataAddress.UnkIndex+(uint)originalChunks.Length;
}
anims.AnimationDataChunks.Clear();foreach(var c in originalChunks)anims.AnimationDataChunks.Add(c);foreach(var c in importedChunks)anims.AnimationDataChunks.Add(c);
anims.Animations.Clear();foreach(var oldEntry in originalEntries){var n=oldEntry.Chunk!.Animation.Chunk!.Name.ToString();anims.Animations.Add(imported.TryGetValue(n,out var fresh)?fresh:oldEntry);}
Console.Error.WriteLine($"Preserved {originalEntries.Length-imported.Count} untouched native entries and {originalChunks.Length} complete original chunks, including inline buffers");
native.RootChunk=anims;
using var stream=new FileStream(args[5],FileMode.CreateNew);using var writer=new CR2WWriter(stream,Encoding.UTF8,true){LoggerService=logger};writer.WriteFile(native);
} else throw new Exception("Unknown operation");
}
}
public class LogProxy:DispatchProxy {
protected override object? Invoke(MethodInfo? method,object?[]? args){if(method!.Name.StartsWith("get_"))return method.ReturnType.IsValueType?System.Activator.CreateInstance(method.ReturnType):null;if(!method.Name.StartsWith("set_"))Console.Error.WriteLine(method.Name+": "+string.Join(" ",args??[]));return null;}
}
