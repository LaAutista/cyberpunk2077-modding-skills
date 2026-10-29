# HK416 rest frames, scoped animation sets and contact inspection

Local evidence, 2026-10-25. Supplement the [weapon workflow](weapon-rigging-animation.md),
[RoN workflow](ron-port-workflow.md), [native authoring](native-animation-authoring.md)
and the existing documentation library. This is not a claim of completed gameplay acceptance.

## Control rest frames are not interchangeable with mesh skin binds

The first animator FBX mixed native player control rest transforms with hand mesh
inverse binds. It reproduced the posed mesh, yet introduced roughly 0.54–0.57 m
of compensating local translation in the thumb control chain. Geometry-only
round-trip verification missed that editing-rig defect.

The corrected handoff keeps the complete native control hierarchy/rest transforms.
Separate per-mesh child deformation bones retain each hand/nail mesh's inverse
binds and weight associations. Test control rest-to-pose local translations,
hierarchy, all posed vertices, named weights, morphs and an actual temporary
control edit. The corrected five-frame FBX had main finger offsets below 0.000658 mm;
fresh Blender reimport kept vertices within 0.006 mm and a thumb rotation moved
both flesh and separate nails. An unweighted torso control moved 0.065 mm; record
that bounded exception instead of silently widening every joint tolerance.

This repairs the interchange rig, **not the runtime thumb**. Independent native
readback found static finger translation channels within sub-micrometre reference
precision. The source finger tracks have only tiny position variation in the
selected rifle motion. Generic pistol graph dependencies are not HK416 evidence.
Right-side close-ups still show finger-base creases, and native muscle helpers
are approximated in Blender. Do not attribute all visible deformation to translated
native joints or claim a clean surface from a numeric transform pass.

## Returned MAX scenes

No compatible 3ds Max scene evaluator was installed. `file`, `7z l` and selected
non-executable compound metadata identify the container, not controller output.
Do not infer a corrected pose from the proprietary Scene stream or screenshots.
[Autodesk's format documentation](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-file-formats-does-3ds-Max-import-and-export.html)
describes MAX as native scene content; a genuine scene export is needed here.

Request binary FBX 2014/2015 (7.4), full skeleton, skinned hands and nails, Animation
and Bake Animation enabled, 60 fps, frames 0–4, step 1, with Skins/Morphs. Retain
names, hierarchy, units and saved bind pose; identify intentional rest/weight/helper
changes. Preserve the exact original handoff so a returned correction can be
compared in world space even when the editing rig subsequently improves. Neto's
`idle tweak.max` remains unevaluated directly; the subsequently supplied
`idle fix.FBX` is an independently evaluable export of the correction.

## Transfer an animator's returned pose, not the exporter's incidental bind edits

The returned binary FBX 7400 imported successfully in Blender 5.2.3: 275 bones,
27 meshes, identical hierarchy/topology. Its frames 0–2 at 30 fps cover the same
duration as the original frames 0–4 at 60 fps. Compare seconds, not frame labels.
Preserve both files and hash them. Diff posed world transforms, rest transforms,
mesh points, named weights, morphs and helper controls separately. Max's round
trip changed several unweighted rest frames; blindly replacing native binds would
be incorrect. The main posed axes matched the native baseline within 0.000012
matrix units, allowing the intended wrist/finger rotation deltas to be transferred.

Reconstruct the hierarchy parent-first with the original native local joint
translations/scales. Synchronize `arm_left_ik_offset` with the resulting left-hand
world transform; editing FK while leaving that controller stale is insufficient.
Do not apply an idle hand shape throughout magazine manipulation. This candidate
uses a fore-end contact test relative to `WeaponRight` and a 120 ms temporal
envelope at grip release/return. A spatial-only fade was rejected because a fast
reload crossed it in one frame. Inspect the dense transition frames; the envelope
is a port-specific adaptation, not a recovered RoN event or general magic value.

Neto also moved `l_thumb_side_mscl_JNT` and `l_pinky_knuckle_B_top_mscl_JNT`.
Those controls are absent from the weapon animation skeleton. Their edits are
recorded but not assigned to unrelated bones or exported into a shared player rig.
The offline renderer approximates muscle deformation. **The right-side finger-base
crease remains visible**, including in the returned FBX; transfer/export success
does not establish a complete skin repair. Next investigate the actual muscle
graph and loaded FPP mesh/rig, or obtain an animator correction on the revised
control rig with helper edits explicitly identified. Neither path is yet proven.

## Private animation ownership and state selection

The candidate uses `ron_hk416_equipped` as its ArchiveXL player-set gate. An
HK416-specific redscript wrapper sets/clears it on right-hand item add/removal,
player attach/detach and Ready entry, using the exact item record. Delayed removal
of the old item must not clear the newly equipped item. Do not write shared
`safe`/combat variables or globally replace player animation paths.

[ArchiveXL's parser](https://github.com/psiberx/cp2077-archive-xl/blob/main/src/App/Extensions/Animation/Config.cpp)
reads `vars`; its [animation extension](https://github.com/psiberx/cp2077-archive-xl/blob/main/src/App/Extensions/Animation/Extension.cpp)
copies them into `animAnimSetupEntry.variableNames`. The inspected installed
ArchiveXL was 1.27.5. The old vars-parser bug is not evidence for this installation.
The new script compiled with the installed redscript compiler and copied Codeware/
AudioXL dependencies. Compiler success does **not** establish that the reported
cross-weapon leakage is cured. Test equip/switch/holster/save-load lifecycle and
unrelated weapons in-game. Leave native combat/safe/quest state selection intact.

## Adapt shared locomotion with explicit contact constraints

The recovered HK416 AnimData selects shared rifle walking/running/ADS loops. The
master graph also references rifle sprint start/loop/stop, separately from pistol,
heavy-armour and tactical-up variants. Use that evidence, not filename similarity.
Keep the recovered clock and distinguish chosen branch from untested runtime selection.

Full-weight shared lowered/sprint motion lost hand contact in the first adaptation.
It cannot be assumed to reproduce source procedural IK/masking. A local candidate
retains the accepted HK416 hand/finger transforms relative to the moving rifle for
non-manipulation locomotion, while preserving weapon travel and source timing and
solving the arms with unchanged joint lengths. Treat that as an explicit adaptation,
not exact RoN runtime playback. Keep reload/trigger articulation separate. Review
both sides of the fingers; first-person thumbnails can hide detached fingers.

## Inspect actual aiming integration

The inspected installed ReArmament scripts matched local sources, and the installed
DLL matched the local built artifact. `RecoilDot.reds` projects the actual `Muzzle`
slot at long distance; eligible native physical projectiles use that slot too.
Eligibility depends on settings/attack type. Inspect `RecoilAim.reds`,
`PhysicalProjectiles.reds` and `native_ammo.cpp`; do not infer shot alignment from
barrel placement. The private HK416 slot matched the fitted source muzzle landmark
and barrel direction. Raw ready was 0.973° from camera forward; ADS was aligned.
Exact centered hip aim, engine ADS response and actual impacts remain gameplay checks.
Do not rotate only the muzzle away from the barrel to conceal a pose mismatch.

## Working local commands and boundaries

These project-specific adapters require the preserved private assets/manifests;
they are not a fresh-clone extraction recipe. Existing tools: Blender 5.2.3,
WolvenKit Modkit/CLI 9.0.1, .NET 10, Wine for the established pack/compiler steps,
jq and ImageMagick. No new dependency was installed.

```bash
export CP2077_DEV=/path/to/CP2077Dev
cd "$CP2077_DEV"
R="$CP2077_DEV/mods/ron-hk416-ready/work/refinement-20261025"
blender -b --factory-startup -t 2 --python-exit-code 1 \
  --python tools/export_ron_hk416_animator.py -- "$R/animator-v2"
blender -b --factory-startup -t 2 --python-exit-code 1 \
  --python tools/check_ron_hk416_animator.py -- "$R/animator-v2"
# Fresh output folders only; archived failed attempts must remain distinguishable.
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/ron_ready_motion.py
node tools/ron_ready_author.mjs
bash tools/ron_ready_native.sh
```

The initial locomotion candidate updated 18 player clips; independent native
readback preserved 109 other player clips, events, float tracks and rig metadata.
It was **not** visually accepted merely for passing import. The local evidence
folder contains the subsequent contact correction and source-state coverage table.

Long clips exposed two tool limits: near-identical source endpoints collapsed to
one float32 timestamp, and repeated linear key lookup made tiny-quaternion repair
impractical. Keep the exact duration but omit a redundant near-end sample; assert
strict timestamp separation. Index native repair keys by joint/time without
removing identity/codec checks. Duration verification must reduce key values,
not spread hundreds of thousands of arguments into `Math.max`. The copied adapter
passed the existing additive/raw-readback regressions; its original test fixture
also needed the now-required identity rig rotation. Preserve all failing logs.

For each accepted candidate: inspect complete numbered first-person and contact
sheets, dense fast transitions and full-resolution defect frames; read back native
assets independently; retain animation/material summary regression tests; extract
the finished archive and compare all inputs. Report native, visual and runtime
results separately. Neto's exact repose, muscle solver output, remaining source
state integration, indoor/outdoor audio and gameplay switching are not established
by these tool checks. The rotational portion of Neto's repose has now survived
native import/readback for 31 clips per player variant; his helper translations
have not. In the local evidence folder, `neto-fbx/compare_skin.py`, `stage_idle.py`,
`adapt_clips_smooth.py`, `author_clips_smooth.mjs` and `import_neto_smooth.sh` record
the actual staged experiment. They depend on private source manifests and are
not published assets or a generic fresh-clone recipe. Native assertions separately
preserve unrelated clips, events, float tracks, skeleton data and source durations.

The final local inspection used 80 sequence/view combinations (20 clips, two
player variants, two cameras): action sheets at 60 Hz and breathing/locomotion
at 10 Hz plus endpoint. Original-size release/regrip samples supplemented the
sheets; not every PNG was opened individually. The source actions remained
continuous in these samples, while the finger-base crease remained. Record
`visuallyInspected: true` separately from `visuallyAccepted: false`.

The final local rerun order, after preserving the existing output folders, was:

```bash
# These private scripts resolve the local evidence tree; relocate their roots
# when moving a full private project. They are not shipped by this skill.
blender -b --factory-startup -t 2 --python-exit-code 1 \
  --python "$R/neto-fbx/stage_idle.py"
blender -b --factory-startup -t 2 --python-exit-code 1 \
  --python "$R/neto-fbx/adapt_clips_smooth.py"
node "$R/neto-fbx/author_clips_smooth.mjs"
bash "$R/import_neto_smooth.sh"
blender -b --factory-startup -t 2 --python-exit-code 1 \
  --python "$R/check_neto_preservation.py"
# Only after binding a real image review receipt to the final inputs:
python tools/package_ron_hk416_ready.py check
python tools/package_ron_hk416_ready.py pack
```

The packaging helper keeps prior attempts, limits native changes to the two
private player animation sets, preserves all other Refined resources, and checks
fresh evidence, archive extraction and ZIP member hashes. Its scope/script change
is compiled independently. Packaging remains a test-candidate operation, not
visual or gameplay acceptance. Keep `REPORT.md`, the small before/after evidence
set and `INSTALL.txt` with the local candidate; do not publish the source assets.

The subsequent [neutral alignment, locomotion and ADS-reload findings](hk416-ads-centering.md)
cover camera-relative source motion, existing native reload selectors and independent
cross-component duration checks. New routing remains a gameplay candidate.
