# HK416 recovery: destination spaces and graph controls

Local evidence, 2026-10-25. Read with the [weapon workflow](weapon-rigging-animation.md),
[native authoring](native-animation-authoring.md) and [ADS investigation](hk416-ads-centering.md).
Ready/Neto is user-reported working. The later ADS beta was rejected after equip
displacement, hand/sight regressions and failure to reload in ADS. The new recovery
has native and bounded visual evidence only; catastrophic runtime causality remains open.

## Preserve identity before attribution

Preserve the exact release ZIP, extracted payload, authoring code, profile and logs.
Compare against the tested package, not a similarly named folder. The rejected ZIP
SHA-256 is `26c1270b8bf2809c78ed8875ab144d835b2c8f5ebc7aac6a0cfa8c8f683d15b1`;
Ready is `3180966c7a5ee9c676e9b7d508dd8c8449beb89f542afe4c21c48f484216792c`.
Only four native animation sets changed in that failed beta. Meshes, rigs, entities,
attachment/collision/physics resources and materials were byte-identical. Sampled
roots showed no large authored jump, with root-motion extraction still null.
Historical HK muzzle telemetry corroborates an abnormal excursion but lacks player
transforms and a per-run archive hash. It does not establish the teleport's cause.

## Two demonstrated space errors

1. Changing an IK offset parent then computing a child against its stale world
   matrix invalidates control goals. Recompute parents first. The installed official
   player-base normal branch copies `arm_right_ik_weapon`/left onto `WeaponRight`/left
   through DirectConnConstraint nodes3695/3696 (Scene.tier<=2). Evaluate this stage
   before declaring a pose centred: it changed the failed PWA result by about
   −0.571° yaw/−0.788° pitch. The corrected neutral/equip endpoints are within
   0.00004° in that explicit calculation. Full graph/IK/physics is not emulated.
2. Source and retained destination parents differed by up to114mm. Copying child
   controls from the source under retained Ready ancestors produced a116mm mismatch
   and visibly detached ADS hands. Reject that merge. Solve aligned source hand
   and weapon world goals against the actual destination roots, limb lengths and
   parents; preserve destination joint offsets/scales and source finger articulation,
   then rebuild controls parent-first. Do not fix it with a global weapon offset.

Import Neto's FBX independently and compare rotations/local offsets in native
readback. Ready fingers reproduce the FBX within0.000566°. The failed beta's idle
finger keys were also within0.0000273° of Ready: wrist/control composition changed;
an older finger-key overwrite was not established. Keep this distinction when
diagnosing a deformation. Do not translate finger joints or map absent muscle
helpers onto arbitrary bones. Customized arms/nails need a bounded proxy plus game checks.

## Trace the effective ADS route

REA's binary tool rejected REDengine archives in this environment. Preserve that
error; use the existing WolvenKit native readers, not an invented REA evidence ID.
Installed Spear1.0.7/Core1.0.2 use a global `player_ranged.animgraph` replacement:
six custom slots, `wwcm_adsr_seconds/aim/slot/active`, additive player clips and
normal weapon clips. An absolute HK clip must not be aliased into an additive slot.
Core also retains the native normal reload branch when its custom gate is inactive.
No second ADS-idle sampler was found in that branch. Lack of custom Core inputs
alone therefore does not explain HK ADS failure or require adopting that Core.

The isolated recovery uses genuine RoN ADS tactical in native normal slot2,
baseline hip/empty in slot0, and exact-item aim permission independent of the
transient OnEnter latch. Preserve native ammo/cancellation/exit handling and speed
scaling. ADS commitment/completion are2.5462995/2.6666667s before scaling. Selection,
held aim, callback order, mixing and cancellation remain unverified in game.
Fast reload/new locomotion changes were deferred during recovery.

## Export and inspection gates actually exercised

Decode **all** inherited clips after sequential native imports. Selected-only raw
readback left earlier clips exposed to the toolkit's tiny-quaternion snapping;
complete decoding fixed the preview data without changing those native bytes.
Keep original render receipts and prove decoded equivalence before reusing views.

Core14-clip controls pass20µm/0.01° for both bodies; all127 descriptors preserve
roots, scales, clocks, metadata, events and float tracks. Source ADS encoded keys
match within1.356µm/0.000088°. At nominal60Hz, time compression reaches0.08751mm /
0.02437°: do not call resampled equality exact. Expanded22-clip checking still fails
the original absolute position gate at nine hand-adjustment samples/body,
frames94–100, peak44.252µm versus Ready38.011µm. Keep that failure visible.

Actually inspect native-readback first-person and grip sequences. Diagnostic
right-index nail/magazine surface intersections at frames90–96 (1.50–1.60s) also
occur in Ready's hip tactical proxy; they are an inherited unresolved contact,
not demonstrated ADS-only regression. Nail morph endpoint1, muscle ancestry and
flat preview materials do not establish the loaded VTK result. Offline cameras
exclude procedural sight offsets: muzzle-direction checks do not prove live sight
alignment. Preserve animation/material-summary regression checks from the linked guide.

## Local commands and prerequisites

These helpers require the private existing project, recovered source/Ready readback,
Neto transfer, Blender5.2.3, Node, existing .NET SDK, WolvenKit9.0.1 adapter and owned
game resources. They are not bundled universal converters. Set `CP2077_DEV` to the
checkout; preserve previous attempts because outputs refuse overwriting.

```sh
cd "$CP2077_DEV"
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/ron_recovery_motion.py
node --max-old-space-size=12288 tools/ron_recovery_author.mjs center
bash tools/ron_recovery_native.sh center
bash tools/ron_recovery_readback.sh center center-readback-all
RON_RECOVERY_STAGE=motion-v2 blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/ron_recovery_motion.py
node --max-old-space-size=12288 tools/ron_recovery_author.mjs ads-v2
bash tools/ron_recovery_native.sh ads-v2
bash tools/ron_recovery_readback.sh ads-v2 final-readback-v2
bash mods/ron-hk416-recovery/work/render-ads-v2.sh pwa
bash mods/ron-hk416-recovery/work/render-ads-v2.sh pma
```

Use the project's
`work/commands.md`, `native-audit/FINDINGS.md`, `ads-reference/FINDINGS.md`, evidence
journals and package receipts for executed stages/hashes. Independent readback,
frame viewing and exact final archive comparison remain required. Script compilation
and a successful pack do not prove equip safety, ADS support or gameplay compatibility.
