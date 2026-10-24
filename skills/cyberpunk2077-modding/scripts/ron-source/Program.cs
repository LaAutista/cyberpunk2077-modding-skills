// Original RoN helper, adapted for explicit local dependencies and fresh output.
using System.Security.Cryptography;
using CUE4Parse.Compression;
using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider.Usmap;
using CUE4Parse.UE4.Assets.Exports;
using CUE4Parse.UE4.Assets.Exports.Animation;
using CUE4Parse.UE4.Assets.Exports.SkeletalMesh;
using CUE4Parse.UE4.Versions;
using CUE4Parse.UE4.Objects.Core.Math;
using CUE4Parse_Conversion;
using CUE4Parse_Conversion.Animations;
using CUE4Parse_Conversion.Options;
using Newtonsoft.Json;
using OodleDotNet;
using Serilog;

const string usage = "Usage: RON_OODLE=/existing/native/library RonExtract PAK_DIRECTORY MAPPING_OR_NONE NEW_OUTPUT_DIRECTORY inventory|dump|export PATH_OR_REGEX ...";
if (args.Length == 1 && args[0] == "--help") { Console.WriteLine(usage); return; }
if (args.Length < 5 || args[3] is not ("inventory" or "dump" or "export")) throw new ArgumentException(usage);
if (!Directory.Exists(args[0])) throw new DirectoryNotFoundException(args[0]);
if (args[1] == "none" && args[3] != "inventory") throw new ArgumentException("A tested mapping is required for dump/export");
if (args[1] != "none" && !File.Exists(args[1])) throw new FileNotFoundException("Mapping is missing", args[1]);
var oodlePath = Environment.GetEnvironmentVariable("RON_OODLE");
if (string.IsNullOrWhiteSpace(oodlePath) || !File.Exists(oodlePath))
    throw new FileNotFoundException("Set RON_OODLE to an existing native library; this helper never downloads it");
var output = Path.GetFullPath(args[2]);
var pakRoot = Path.TrimEndingDirectorySeparator(Path.GetFullPath(args[0]));
if (output == pakRoot || output.StartsWith(pakRoot + Path.DirectorySeparatorChar, StringComparison.Ordinal))
    throw new ArgumentException("Output must be outside the PAK directory");
if (Directory.Exists(output) && Directory.EnumerateFileSystemEntries(output).Any())
    throw new IOException("Output directory must be new or empty; use a distinct directory for each run");
Directory.CreateDirectory(output);
Log.Logger = new LoggerConfiguration().MinimumLevel.Information().WriteTo.Console().CreateLogger();
OodleHelper.Initialize(new Oodle(Path.GetFullPath(oodlePath)));
string OutputPath(string relative) {
    if (Path.IsPathRooted(relative) || relative.Contains('\\') || relative.Split('/').Any(s => s is ".." or "."))
        throw new InvalidDataException($"Unsafe archive-relative path: {relative}");
    return Path.Combine(output, relative);
}
using var provider = new DefaultFileProvider(args[0], SearchOption.TopDirectoryOnly,
    new VersionContainer(EGame.GAME_UE5_3), StringComparer.OrdinalIgnoreCase);
provider.ReadScriptData = true;
if (args[1] != "none") provider.MappingsContainer = new FileUsmapTypeMappingsProvider(args[1]);
provider.Initialize();
var mounted = provider.Mount();
provider.PostMount();
Console.WriteLine($"Mounted {mounted}; files {provider.Files.Count}; mappings {args[1]}");
var settings = new JsonSerializerSettings { Formatting = Formatting.Indented };
void Save(string relative, object obj) {
    var target = OutputPath(relative);
    Directory.CreateDirectory(Path.GetDirectoryName(target)!);
    File.WriteAllText(target, JsonConvert.SerializeObject(obj, settings));
}
if (args[3] == "inventory") {
    var regex = new System.Text.RegularExpressions.Regex(args[4], System.Text.RegularExpressions.RegexOptions.IgnoreCase);
    var files = provider.Files.Values.Where(f => regex.IsMatch(f.Path)).Select(f => new { f.Path, f.Size }).OrderBy(f=>f.Path).ToArray();
    Save("inventory.json", files);
    Console.WriteLine($"Inventory matches {files.Length}");
    return;
}
var manifest = new List<object>();
var runId = Convert.ToHexStringLower(SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(string.Join("\n", args.Skip(3)))))[..12];
var session = new ExportSession { MaxDegreeOfParallelism = 1 };
foreach (var path in args.Skip(4)) {
    Console.WriteLine($"Loading {path}");
    if (!path.EndsWith(".uasset", StringComparison.OrdinalIgnoreCase)) throw new ArgumentException("Select .uasset package paths");
    _ = OutputPath(path);
    var source = provider.Files[path];
    var bytes = source.Read();
    var package = provider.LoadPackage(path);
    if (!package.CanDeserialize) throw new InvalidDataException($"Cannot deserialize {path}");
    var exports = package.GetExports().ToArray();
    var rawFiles = new List<object>();
    foreach (var extension in new[]{".uasset", ".uexp", ".ubulk"}) {
        var rawPath = source.PathWithoutExtension + extension;
        if (!provider.Files.TryGetValue(rawPath, out var rawFile)) continue;
        var raw = rawFile.Read();
        var destination = OutputPath("raw/" + rawPath);
        Directory.CreateDirectory(Path.GetDirectoryName(destination)!);
        File.WriteAllBytes(destination, raw);
        rawFiles.Add(new { Path = rawPath, rawFile.Size, Sha256 = Convert.ToHexStringLower(SHA256.HashData(raw)) });
    }
    Save("properties/" + path + ".json", exports);
    var records = new List<object>();
    foreach (var obj in exports) {
        object? animation = null;
        if (obj is UAnimSequence sequence) {
            var converted = sequence.ConvertAnims();
            if (converted.Sequences.Count != 1) throw new InvalidDataException("Single sequence conversion count mismatch");
            var decoded = converted.Sequences[0];
            var decodedSkeleton = sequence.Skeleton?.Load<USkeleton>()
                ?? throw new InvalidDataException("Animation skeleton could not be loaded");
            var decodedFrames = Enumerable.Range(0, decodedSkeleton.BoneCount).Select(bone => {
                var rest = decodedSkeleton.ReferenceSkeleton.FinalRefBonePose[bone];
                return new { Bone = decodedSkeleton.ReferenceSkeleton.FinalRefBoneInfo[bone].Name.Text,
                    Frames = Enumerable.Range(0, decoded.NumFrames).Select(frame => {
                        var position = rest.Translation; var rotation = rest.Rotation; var scale = rest.Scale3D;
                        decoded.Tracks[bone].GetBoneTransform(frame, decoded.NumFrames, ref rotation, ref position, ref scale);
                        return new { Frame = frame, Position = new[]{position.X,position.Y,position.Z},
                            Quaternion = new[]{rotation.X,rotation.Y,rotation.Z,rotation.W}, Scale = new[]{scale.X,scale.Y,scale.Z} };
                    }).ToArray() };
            }).ToArray();
            Save("decoded/"+path+".json", decodedFrames);
            object? compression = null;
            if (sequence.CompressedDataStructure is FUECompressedAnimData ue) {
                var skeleton = decodedSkeleton;
                compression = new { ue.KeyEncodingFormat, ue.TranslationCompressionFormat,
                    ue.RotationCompressionFormat, ue.ScaleCompressionFormat,
                    CompressedBytes = ue.CompressedByteStream.Length,
                    StreamSha256 = Convert.ToHexStringLower(SHA256.HashData(ue.CompressedByteStream)),
                    ue.CompressedScaleOffsets.StripSize,
                    ScaleOffsets = ue.CompressedScaleOffsets.OffsetData,
                    TrackOffsets = ue.CompressedTrackOffsets,
                    BoneTracks = Enumerable.Range(0, skeleton.BoneCount).Select(i=>new {
                        Bone = skeleton.ReferenceSkeleton.FinalRefBoneInfo[i].Name.Text,
                        TrackIndex = sequence.FindTrackForBoneIndex(i) }) };
            }
            animation = new { sequence.NumFrames, sequence.SequenceLength, sequence.RateScale,
                sequence.AdditiveAnimType, sequence.RefPoseType, sequence.RefFrameIndex,
                Codec = sequence.CompressedDataStructure?.GetType().Name,
                Compression = compression,
                Skeleton = sequence.Skeleton?.ResolvedObject?.GetPathName(),
                TrackCount = converted.Sequences[0].Tracks.Count,
                converted.Sequences[0].FramesPerSecond,
                Curves = sequence.CompressedCurveData?.FloatCurves?.Select(c=> new { c.CurveName, KeyCount = c.FloatCurve.Keys.Length }),
                SourceWasAdditive = converted.Sequences[0].IsAdditive,
                ExportedPoseSpace = "full-local-transforms",
                ComposedBase = sequence.RefPoseSeq?.GetPathName() };
        }
        records.Add(new { obj.Name, obj.ExportType, RuntimeType = obj.GetType().Name, animation });
        if (args[3] == "export" && (obj is UAnimationAsset || obj is USkeletalMesh || obj.ExportType is "StaticMesh" or "Skeleton" or "Texture2D" or "MaterialInstanceConstant")) session.Add(obj);
    }
    manifest.Add(new { Path = path, source.Size, Sha256 = Convert.ToHexStringLower(SHA256.HashData(bytes)),
        package.ArchiveName, package.ImportMapLength, package.ExportMapLength, RawFiles = rawFiles, Exports = records });
    Save("manifest.json", manifest);
    Save($"manifest-{runId}.json", manifest);
}
if (args[3] == "export") {
    var results = await session.RunAsync(Path.Combine(output,"assets"), new ExportOptions(meshFormat: EMeshFormat.UEFormat, socketFormat: ESocketFormat.Socket, exportMaterials: true));
    Save("export-results.json", results.Select(r=>new {r.Success,r.ObjectPath,r.DiskFilePaths,Error=r.Error?.ToString()}));
    Save($"export-results-{runId}.json", results.Select(r=>new {r.Success,r.ObjectPath,r.DiskFilePaths,Error=r.Error?.ToString()}));
    if (results.Any(r=>!r.Success)) throw new InvalidDataException("One or more exports failed; see export-results.json");
    Console.WriteLine($"Exported {results.Count} objects");
}
