# Reproduce the Ready or Not source extraction

This is the bounded Linux source adapter used for the HK416 empty-reload study.
It produces raw package companions, decoded JSON and UEFormat exchange files.
Use [weapon rigging and animation](weapon-rigging-animation.md) for the later
Blender, native-export and gameplay gates. These commands do not establish them.

## Supplied source and provenance

The [RonExtract project](../scripts/ron-source/RonExtract.csproj) and
[Program.cs](../scripts/ron-source/Program.cs) derive from the original authored
helper used in the source study. They link an **external** CUE4Parse checkout.
The [PAK inventory](../scripts/ron-source/ron_pak_inventory.mjs) is the original
index-only helper. The [exchange checker](../scripts/ron-source/ron_source_export_check.mjs)
is a portable adaptation of the original checker: it validates fresh output and
optional dependency dumps without private pre-fix fixture files.

Original helper source uses this repository's MIT license. The
[converter patch](../scripts/ron-source/cue4parse-local-corrections.patch) is the
unchanged study patch against FabianFG's Apache-2.0 CUE4Parse, copyright 2026
FabianFG. It marks changes through its diff and retains upstream context. That
patch/context remains Apache-2.0; the repository MIT license does not replace it.
The upstream [license](../scripts/ron-source/cue4parse-LICENSE.md) and
[notices](../scripts/ron-source/cue4parse-NOTICE.md) accompany it. No upstream
library implementation, commercial package, mapping, native library or binary is
included. The repak format reference used for the independent index reader is
[upstream footer/pak code](https://github.com/trumank/repak/tree/master/repak/src).

Historical evidence came from the source project's `EXTRACTION-REPORT.md`,
`toolchain-receipt.json`, `selected-packages.txt`, export/dependency manifests and
`source-export-checks.json`. Those private files/assets are not publication inputs.

## Exact tested dependencies

| Input | Recorded value |
| --- | --- |
| Ready or Not | Steam build **25784851**, executable **UE 5.3.2.0**, 26 PAKs / 467,074 entries |
| CUE4Parse | [990d4d7d4e0340a75a14323436d55568f1415e00](https://github.com/FabianFG/CUE4Parse/tree/990d4d7d4e0340a75a14323436d55568f1415e00), plus the supplied patch |
| SDK | .NET **10.0.400**, target `net10.0`; a runtime-only installation cannot build |
| Mapping | [Mappings.usmap locator](https://unofficial-modding-guide.com/downloads/Mappings.usmap), SHA256 `f1ce422460be333aaee3f73a8802e7269be9d83aba9033606794abd3a8b32848` |
| Linux x64 Oodle | **2.9.16**, [gcc-x64-release.zip](https://github.com/WorkingRobot/OodleUE/releases/download/2026-06-04-1357/gcc-x64-release.zip); extracted `lib/liboodle-data-shared.so` SHA256 `f21d70299bbe873f63e8aef778b30f4dee6dec1fc09140c185caf1f8d153f771` |
| Extra helper package | `SkiaSharp.NativeAssets.Linux.NoDependencies` **2.88.9**; other package versions come from the pinned external checkout's `Directory.Packages.props` |
| Later Blender importer | [UEFormat d858fe38b2b5b8c63ac4b7481b4386ebfabbf935](https://github.com/h4lfheart/UEFormat/tree/d858fe38b2b5b8c63ac4b7481b4386ebfabbf935/plugins/blender); not needed for extraction/checker |

Mapping URLs are mutable: compare the downloaded bytes, not the filename/date.
A different hash/build requires actual package decode and animation checks; do
not claim compatibility from a filename. Dependencies must be supplied separately
under their applicable terms. The helper requires an existing Oodle path and
never invokes CUE4Parse's automatic downloader.

Recursive native dependencies at the pinned checkout:

| Path beneath `CUE4Parse-Natives/ACL/external/acl` | Commit |
| --- | --- |
| `.` (ACL v2.1.0) | `414689d5cff4286a7898487a46dc5e48005d38da` |
| `external/benchmark` | `0d98dba29d66e93259db7daa53a9327df767a415` |
| `external/catch2` | `c4e3767e265808590986d5db6ca1b5532a7f3d13` |
| `external/rtm` | `d7982f2b2524feeb322f424b29cf43df30b5d5b7` |
| `external/rtm/external/benchmark` | `0d98dba29d66e93259db7daa53a9327df767a415` |
| `external/rtm/external/catch2` | `c4e3767e265808590986d5db6ca1b5532a7f3d13` |
| `external/sjson-cpp` | `54b3985e8ccc5efb5f24dabf0b4b802a996366e6` |
| `external/sjson-cpp/external/catch2` | `c4e3767e265808590986d5db6ca1b5532a7f3d13` |

A full native build also requires CMake and a C++ toolchain. Native ACL built in
the study, but the recovered reloads use `FUECompressedAnimData` /
`AKF_PerTrackCompression`; no RoN ACL clip was exercised. The pinned dependency
build reports advisories for Microsoft.Bcl.Memory 9.0.0 and ImageSharp 3.1.12;
this reproduction pin is not a dependency security clearance.

## Converter fixes that must survive

1. Preserve POSIX separators in output paths on Linux.
2. Use endpoint-inclusive `(NumFrames - 1) / SequenceLength`: 121 samples over
   2 seconds are 60 Hz, not 60.5 Hz. Three-sample idle bases also become 60 Hz.
3. Preserve the actual source sequence for curves after additive conversion
   switches its bone-map reference to the idle base; export every composed track.
4. Normalize quaternions precisely; reject invalid norms. The study's maximum
   post-fix norm error was approximately `1.05e-7`.
5. An absent **additive** per-track scale channel is a zero delta, not one.
   The body has 49 such tracks; interpreting them as one doubled their scales.
6. Keep all sampled non-constant frames. Removing repeated keys without the final
   hold endpoint introduced premature `tag_mag_01` rotation at frame 28.

These are bounded changes for this source case. Other additive reference types,
slow-motion RateScale, constant-animation behavior and general retarget modes
were not validated. Keep this patched dependency isolated from other projects.

## Portable build

Set paths to your own existing SDK, source game and separate work area. Use a
**dedicated** external CUE4Parse checkout at the pinned commit with its recursive
submodules. Acquire missing dependencies explicitly; the commands below assume
they are already present. Do not publish the resulting work directory.

```bash
export RON_HELPERS=/path/to/skills/cyberpunk2077-modding/scripts/ron-source
export RON_SDK=/path/to/dotnet-sdk/dotnet
export RON_CUE=/path/to/dedicated/CUE4Parse
export RON_PAKS='/path/to/Ready Or Not/ReadyOrNot/Content/Paks'
export RON_MAPPING=/path/to/compatible.usmap
export RON_OODLE=/path/to/liboodle-data-shared.so
export RON_WORK=/path/to/new/private/source-work

"$RON_SDK" --list-sdks
test "$(git -C "$RON_CUE" rev-parse HEAD)" = 990d4d7d4e0340a75a14323436d55568f1415e00
git -C "$RON_CUE" submodule status --recursive
sha256sum "$RON_MAPPING" "$RON_OODLE"
# Check hashes against the table above before continuing.
# Apply only to the dedicated, clean pinned checkout; do not reapply to a patched one.
git -C "$RON_CUE" apply --check "$RON_HELPERS/cue4parse-local-corrections.patch"
git -C "$RON_CUE" apply "$RON_HELPERS/cue4parse-local-corrections.patch"
mkdir -p "$RON_WORK/helper"
cp "$RON_HELPERS/Program.cs" "$RON_HELPERS/RonExtract.csproj" "$RON_WORK/helper/"
# Standard restore can access NuGet; arrange it only when dependency retrieval is authorized.
"$RON_SDK" restore "$RON_WORK/helper/RonExtract.csproj"
"$RON_SDK" build "$RON_WORK/helper/RonExtract.csproj" -c Release --no-restore -m:1 -nr:false
export RON_EXTRACT="$RON_WORK/helper/bin/Release/net10.0/RonExtract.dll"
"$RON_SDK" "$RON_EXTRACT" --help
```

`RON_CUE` can instead be supplied as `-p:Cue4ParseRoot=/path/to/CUE4Parse` to
both restore and build. This new standalone project replaces the historical
project placed inside CUE4Parse. It does not require the original workspace.

For a previously built, patched checkout and a complete existing NuGet cache,
the portable verification used an empty local feed and reused compiled project
references. This checks the helper build, not a fresh dependency/native build:

```bash
mkdir -p "$RON_WORK/empty-feed"
"$RON_SDK" restore "$RON_WORK/helper/RonExtract.csproj" --no-dependencies \
  --source "$RON_WORK/empty-feed" -p:NuGetAudit=false
"$RON_SDK" build "$RON_WORK/helper/RonExtract.csproj" -c Release --no-restore \
  -m:1 -nr:false -p:BuildProjectReferences=false -p:CUE4PARSE_SKIP_NATIVE=true
```

## First live-source check

The independent inventory checks v11 unencrypted full-directory PAK indexes and
SHA1 values. It deliberately does not decompress payloads. It refuses an existing
output file. `RonExtract` requires a new or empty output directory on every run,
rejects output beneath the PAK directory and does not change game packages.

```bash
node "$RON_HELPERS/ron_pak_inventory.mjs" "$RON_PAKS" "$RON_WORK/inventory.json"
"$RON_SDK" "$RON_EXTRACT" "$RON_PAKS" "$RON_MAPPING" "$RON_WORK/smoke" export \
  ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/body/fp_hk416_add_spd_reload_empty.uasset \
  ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/weapon/fp_hk416_add_spd_reload_empty_weapon.uasset \
  ReadyOrNot/Content/ReadyOrNot/Character/SWAT/Character_SWAT_3P/Shared/SKL_RoN_Player_Master_Shared.uasset
node "$RON_HELPERS/ron_source_export_check.mjs" "$RON_WORK/smoke" > "$RON_WORK/smoke-checks.json"
```

Expect three exported objects, six raw companions and **114,345** checked local
position/rotation/scale channels. Both clips must contain 121 samples at 60 Hz;
the body must have 292 tracks in full skeleton order and the weapon 23 tracks.
The checker compares source curve frames/values, unit scales, quaternion norms,
frame-28 magazine hold, every decoder sample, export files and raw SHA256 hashes.
It requires these specific HK416 assets and is not a generic UEFormat validator.

## Complete selected-source recovery

Follow active class references before accepting these paths for another build.
`Primary_HK416.AnimationData` selects `BP_HK416_M_AnimData`; its `ReloadEmpty`
body/gun entries select the paired montages. The primary mesh selects
`SK_Rif_HK416` and `ANIMBP_HK416`. `CSK_Swat_NoGlove` selects matching bare arms;
that is a compatible option, not evidence of the player's equipped cosmetic.
Keep its full shared skeleton separately: the arm mesh contains only a subset.

The following selection is the historically exercised 18-package set. On the
recorded build, its material/texture dependencies produced 34 exported objects.
It includes original source metadata rather than relying on filenames:

```bash
mapfile -t ron_packages <<'PACKAGES'
ReadyOrNot/Content/ReadyOrNot/Assets/Weapons/HK416/Meshes/SK_Rif_HK416.uasset
ReadyOrNot/Content/ReadyOrNot/Assets/Weapons/HK416/Meshes/SM_Rif_HK416_Mag_Static.uasset
ReadyOrNot/Content/ReadyOrNot/Character/PLAYER/ARMS/Arms_Base/sk_player_arms_bare_body.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/body/fp_hk416_idle_pose.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/body/fp_hk416_add_spd_reload_empty.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/weapon/fp_hk416_idle_pose_weapon.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/weapon/fp_hk416_idle_pose_empty_weapon.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/weapon/fp_hk416_add_spd_reload_empty_weapon.uasset
ReadyOrNot/Content/Blueprints/Items/WeaponsRevised/Primary_HK416.uasset
ReadyOrNot/Content/Blueprints/Animation/Revised/AnimData/Mainline/BP_HK416_M_AnimData.uasset
ReadyOrNot/Content/Blueprints/Animation/Revised/Graphs_Weapon/ANIMBP_HK416.uasset
ReadyOrNot/Content/Blueprints/Customization/Gloves/CSK_Swat_NoGlove.uasset
ReadyOrNot/Content/Blueprints/Animation/Revised/Graphs_Body/ANIMBP_Player_FP_Master.uasset
ReadyOrNot/Content/ReadyOrNot/Assets/Weapons/HK416/Shared/SKL_Rif_HK416.uasset
ReadyOrNot/Content/ReadyOrNot/Character/SWAT/Character_SWAT_3P/Shared/SKL_RoN_Player_Master_Shared.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/body/montages/fp_hk416_add_spd_reload_empty_Montage.uasset
ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/weapon/montages/fp_hk416_add_spd_reload_empty_weapon_Montage.uasset
ReadyOrNot/Content/ReadyOrNot/Assets/Weapons/HK416/Meshes/SM_Rif_Hk416_Bullets_FMJ.uasset
PACKAGES
"$RON_SDK" "$RON_EXTRACT" "$RON_PAKS" "$RON_MAPPING" "$RON_WORK/selected" export "${ron_packages[@]}"
```

Capture raw companions/properties for every resolved export as well. Each dump
gets a separate directory, so its manifest cannot overwrite the export manifest.
The material parent below was recovered separately in the historical run.

```bash
node - "$RON_WORK/selected/export-results.json" > "$RON_WORK/dependency-packages.txt" <<'JS'
const fs = require('node:fs');
const results = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
if (!results.length || !results.every(r => r.Success)) throw new Error('Incomplete export');
console.log([...new Set(results.map(r => r.ObjectPath.replace(/\.[^.]+$/, '.uasset')))].sort().join('\n'));
JS
mapfile -t ron_dependencies < "$RON_WORK/dependency-packages.txt"
"$RON_SDK" "$RON_EXTRACT" "$RON_PAKS" "$RON_MAPPING" "$RON_WORK/dependencies" dump "${ron_dependencies[@]}"
"$RON_SDK" "$RON_EXTRACT" "$RON_PAKS" "$RON_MAPPING" "$RON_WORK/material-parent" dump \
  ReadyOrNot/Content/ReadyOrNot/Assets/Weapons/SHARED/Weapon_1P_MASTER.uasset
node "$RON_HELPERS/ron_source_export_check.mjs" "$RON_WORK/selected" \
  "$RON_WORK/dependencies" "$RON_WORK/material-parent" > "$RON_WORK/complete-checks.json"
```

The original combined receipt covered **40 packages / 97 raw companion files**.
Counts are build-specific checks, not permission to ignore unresolved references.
Texture references under `Weapons/HK416Test` were active material dependencies;
that folder name did not make them disposable. Keep decoded material metadata,
separate magazine/bullet meshes, sockets, animation bases, curves and notifies.
`ReadScriptData=true` retains Blueprint bytecode in package JSON. `inventory`
accepts a regex and can use `none` as the mapping argument; `dump`/`export` require
a mapping and exact `.uasset` paths. No AES key was needed for this selected set.

## Interpretation and verification boundary

The exported body is **already composed full local motion** from a local-additive
source with `ABPT_AnimFrame`, reference frame 0 and the idle-pose base. Do not add
the idle pose again. The weapon source is absolute (`AAT_None`) despite `add` in
its filename. UEAnim keeps all ten `Hand_IK_Left` curve values but omits source
per-key interpolation flags; retain JSON for the constant segments beginning at
0 and 0.13333334 seconds and the remaining linear segments.

Raw sequence tracks omit the AnimBP's magazine hide effect: the observed graph
sets `tag_mag_01` scale to zero between **0.377 and 1.364571 seconds**.
`ReloadComplete` occurs at **1.9171239 seconds**. These source notifies/graph
findings are not implemented Cyberpunk events. Native dropped-prop physics,
procedural hand IK, current cosmetic, runtime camera/FOV and shaders need their
own evidence.

Portable verification performed for this publication: offline cached restore,
standalone helper compilation against the existing patched dependency output,
read-only inventory of the existing 26 PAKs, a fresh three-object export, and the
complete selected-source/dependency command blocks above in a private temporary
directory. The full run recovered 34 exported objects, 40 unique packages and 97
raw companion files; all 114,345 sampled channels and 49 omitted additive scale
tracks passed the fresh-output checker. The patch applied to pristine copies of
its four pinned source files and reproduced the existing corrections byte for
byte. Negative checks rejected reused output, invalid mode, missing Oodle,
modified raw bytes and an incomplete decoder timeline. Helper build: zero errors,
seven cached NuGet advisory warnings. No download, game edit or game launch was
required.

A fresh clean-machine bootstrap and Blender visual inspection were not performed
in this portability pass. The new checker does not rerun the historical
failed-export fixtures. Its independent UEFormat reader still shares CUE4Parse's
source decoder; sample agreement is not an independent Unreal-runtime comparison.
