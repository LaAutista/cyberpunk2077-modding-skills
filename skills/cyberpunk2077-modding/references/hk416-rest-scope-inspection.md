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
`idle tweak.max` correction remains unevaluated until that export is available.

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
by these tool checks.
