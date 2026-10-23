# Lynx command contracts and portability boundary

These preserve historically successful command shapes from the original project.
They are **not an end-to-end runnable tutorial from a fresh clone**. This repository
does not include the original weapon assets, `tools/inspect_lynx_animation.py`,
`tools/correct_lynx_lever.py`, build/verification adapters or case-specific probes.
Do not substitute a different weapon name into those adapters. Their source part
maps, rig/codec assumptions, paths and build containers were specific to Lynx.

The [case study](lynx-case-study.md) states the historical evidence; the
[general method](../../cyberpunk2077-modding/references/weapon-rigging-animation.md)
is reusable with another project's explicit adapters. Only the contact-sheet
helper referenced below ships here. Do not run correction/export commands during
an inspection-only task or overwrite existing evidence.

## External WolvenKit recovery

Prerequisites: legally available game/donor assets, WolvenKit CLI compatible with
them, and verified exporter settings. The demonstrated version was Linux CLI 9.0.1.
Set these variables to actual paths; they have no hidden machine-specific defaults:

```bash
: "${CP2077_PROJECT:?Set the original project root containing its tools and mods}"
: "${CP2077_GAME:?Set the installed game root}"
: "${WK_CLI:?Set the executable CLI or established project wrapper}"
: "${LYNX_RECOVERY:?Set a new recovery output directory}"
cd "$CP2077_PROJECT"
mkdir -- "$LYNX_RECOVERY"
lynx_donor="$CP2077_PROJECT/mods/gm6-lynx/work/reference/mw3_weapons_poc/sig50/animations"
mkdir -- "$LYNX_RECOVERY/player-glb" "$LYNX_RECOVERY/player-native"
"$WK_CLI" export "$lynx_donor/pma.anims" "$lynx_donor/pwa.anims" \
  -gp "$CP2077_GAME" -o "$LYNX_RECOVERY/player-glb"
"$WK_CLI" unbundle "$CP2077_GAME/archive/pc/content/basegame_4_appearance.archive" \
  -r 'arms_hq\\a0_00[01]_(pma|pwa)_base_hq__full\.mesh$' \
  -o "$LYNX_RECOVERY/player-native"
```

Use a separately configured mesh exporter with `MeshOnly` and `withMaterials:
false` for the two full-arm meshes. Preserve its configuration separately from
other export jobs. `DOTNET_ROOT` is optional when the executable already locates
its runtime; if required, set it to an installed compatible .NET runtime.

```bash
: "${WK_MESH_CLI:?Set the isolated configured mesh exporter}"
mkdir -- "$LYNX_RECOVERY/arms-glb"
"$WK_MESH_CLI" export \
  "$LYNX_RECOVERY/player-native/base/characters/common/player_base_bodies/player_man_average/arms_hq/a0_001_pma_base_hq__full.mesh" \
  "$LYNX_RECOVERY/player-native/base/characters/common/player_base_bodies/player_female_average/arms_hq/a0_000_pwa_base_hq__full.mesh" \
  -o "$LYNX_RECOVERY/arms-glb"
```

MeshOnly does not recover the skeleton hierarchy. Retain the corresponding native
rigs, entity attachment and camera routes. Component export used a separate
resolver tree with `bin/x64/Cyberpunk2077.exe` linked to the installed executable
and `archive/pc/content/basegame_4_appearance.archive` linked to the donor's
`gm6_lynx.archive`. The executable was only an existence check; it was not launched.
This workaround is proven for those inputs/version. Do not rename live archives.
Inspect an existing isolated resolver with `readlink -f` before using it:

```bash
: "${LYNX_RESOLVER:?Set the already prepared isolated resolver tree}"
readlink -f "$LYNX_RESOLVER/bin/x64/Cyberpunk2077.exe"
readlink -f "$LYNX_RESOLVER/archive/pc/content/basegame_4_appearance.archive"
mkdir -- "$LYNX_RECOVERY/part-glb"
"$WK_CLI" export "$lynx_donor/barrel.anims" "$lynx_donor/magazine.anims" \
  -gp "$LYNX_RESOLVER" -o "$LYNX_RECOVERY/part-glb"
```

Root-motion export was disabled. The custom raw animation decoder asserted
unsupported compressed/constant key counts were zero; it was not a universal
codec. Preserve such assertions rather than accepting an unknown format silently.

## Original project playback contracts — adapters not included

These commands run from `$CP2077_PROJECT`. Check adapter existence first. Supply
new output roots and explicitly select input revisions; an output folder does not
select an input assembly. `--state before` alone selected the older historical
baseline, not the later pre-lever completion baseline.

```bash
: "${BLENDER:?Set the Blender executable path}"
: "${LYNX_PREVIEWS:?Set a new preview root}"
test -f tools/inspect_lynx_animation.py
"$BLENDER" -b -t 4 --python tools/inspect_lynx_animation.py -- \
  --state before \
  --assembly mods/gm6-lynx/work/bolt-inspection/completion/before/source/raw/gm6-lynx.blend \
  --animation mods/gm6-lynx/work/bolt-inspection/completion/before/receiver.anims.json \
  --native-dir mods/gm6-lynx/work/bolt-inspection/completion/before/native \
  --clip empty_reload --frames all --view close --player pma --no-arms \
  --asset native --engine workbench --output "$LYNX_PREVIEWS/before-native"
"$BLENDER" -b -t 4 --python tools/inspect_lynx_animation.py -- \
  --state after --clip empty_reload --frames all --view first-person \
  --player pma --asset native --engine workbench --output "$LYNX_PREVIEWS/after-native"
"$BLENDER" -b -t 4 --python tools/inspect_lynx_animation.py -- \
  --state after --asset native --clip empty_reload --frames 125,128,133,135,142 \
  --view close --focus right-hand --player pma --engine workbench \
  --output "$LYNX_PREVIEWS/after-hand-pma"
```

Repeat matching before/after cameras and variants as needed; the three examples
alone do not provide a matching complete review. The established renderer used
30 fps and wrote `render.json` only on completion. Relevant variants included
`pwa`, `reload` and `first_equip`; mechanism cameras included `left`, `close` and
`rear`. `--player none` was receiver-only; `--no-arms` isolated the mechanism.
Neither established hand acceptance. `--player-pose idlepose_shoulder` with receiver
recoil held static arms, explicitly recorded as an approximation.

The renderer's `--native-dir` means the parent containing `meshes/`. The disk gate
below instead expects the directory directly containing `receiver.glb` and
`receiver.mesh.json`. The lever gate takes a `--mesh` file. Keep these distinctions.

Use this repository's [contact-sheet helper](contact-sheets.md), then open its
outputs and full-size critical frames. For a contiguous 30 fps sequence starting
at zero, FFmpeg can create a supplemental video without replacing still inspection:

```bash
: "${LYNX_RENDER:?Set one completed contiguous render directory}"
: "${LYNX_VIDEO:?Set a new MP4 filename}"
ffmpeg -n -framerate 30 -start_number 0 -i "$LYNX_RENDER/%04d.png" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p "$LYNX_VIDEO"
ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=nb_read_frames,r_frame_rate,width,height -of json "$LYNX_VIDEO"
```

Match the actual manifest fps, start/end and decoded count. A sparse focused frame
list is not a faithful `%04d.png` video. Encoding does not mean it was watched.

## Original correction and native gates — adapters not included

The successful lever bake used an unchanged pre-lever input and refused existing
output/report files. Repeating it against corrected output was not safe:

```bash
mkdir mods/gm6-lynx/work/lever-reproduction
"$BLENDER" -b -t 2 --python-exit-code 1 --python tools/correct_lynx_lever.py -- \
  --input mods/gm6-lynx/work/bolt-inspection/completion/before/receiver.anims.json \
  --output mods/gm6-lynx/work/lever-reproduction/receiver.anims.json \
  --report mods/gm6-lynx/work/lever-reproduction/verification.json
```

That reproduction is not automatically a build input. Only an authorized asset
change may adopt it into `mods/gm6-lynx/work/reload-correction/receiver.anims.json`,
after preserving the previous input and inspecting the candidate. The established
builder used native and Wine operations as appropriate; shared Wine-prefix jobs
ran serially. Its animation stage was Lynx-specific, not a generic importer.

```bash
python tools/build_weapon_replacements.py gm6-lynx animation
python tools/build_weapon_replacements.py gm6-lynx meshes --mesh receiver --mesh receiver_shadow
python tools/verify_weapon_replacements.py gm6-lynx geometry
"$BLENDER" -b -t 2 --python mods/gm6-lynx/work/bolt-inspection/completion/disk/verify_final_native.py -- \
  --native-dir mods/gm6-lynx/work/verification/meshes \
  --source mods/gm6-lynx/source/raw/receiver.glb \
  --animation mods/gm6-lynx/work/reload-correction/readback/receiver.anims.json \
  --output mods/gm6-lynx/work/bolt-inspection/completion/disk/recheck-native-disk.json
"$BLENDER" -b -t 2 --python mods/gm6-lynx/work/bolt-inspection/completion/lever/check_native_lever_fast.py -- \
  --mesh mods/gm6-lynx/work/verification/meshes/receiver.glb \
  --animation mods/gm6-lynx/work/reload-correction/readback/receiver.anims.json \
  --output mods/gm6-lynx/work/bolt-inspection/completion/lever/recheck-native-lever.json
```

Use fresh report paths. The geometry verifier checked all eight native meshes.
Animation import serialized the actual resource and required exact `Data` equality.
For the shadow lever, the gate additionally used `--shadow-manifest` with the
assembly manifest to resolve named bone slots. Only actual native readback gates,
matched previews and explicit review established the bounded results in the case.

## Original package checks — adapters and payload not included

When packaging was in scope, the established workflow was:

```bash
python tools/build_weapon_replacements.py gm6-lynx pack
python tools/verify_weapon_replacements.py gm6-lynx package
```

The verifier extracted the archive and compared all resources against verified
inputs, including exact native animation `Data`. A two-entry distribution ZIP
contained `INSTALL.txt` and `archive/pc/mod/GM6Lynx_WWCM.archive`; `bsdtar --format zip`
created it, `unzip -t` checked integrity, and `unzip -p ... | cmp - ...` compared
each payload to its verified source. Preserve an older release and write a fresh
pending output before promotion. These checks did not prove gameplay or authorize
installation. The archive and original install text are not part of this skills
repository.
