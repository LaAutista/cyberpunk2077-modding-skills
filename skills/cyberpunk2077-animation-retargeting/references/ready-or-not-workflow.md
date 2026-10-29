# Ready or Not workflow proven by the HK416

Use the existing [source extraction, assembly and native route](../../cyberpunk2077-modding/references/ron-port-workflow.md)
for the commands and prerequisites. This reference adds the decisions established
by the CGTrader HK416 and its locomotion correction on 2026-10-28. Reuse the route;
measure a new weapon's skeleton, geometry and contact calibration independently.

## Identify the accepted baseline

The user reported that the installed pelvis-coupled HK416 worked and described the
port as solid, with excessive camera motion remaining. The installed archive was
independently identified as `CG-SMR-Pelvis-Locomotion-v3-20261028`, SHA-256
`3e7a7422d2333fc1b458c47981968df87bb164d2f28ae4152f013ab9b30ce276`.
This is positive user gameplay evidence for the reported locomotion/contact fix.
The body variant was not specified; do not infer a test matrix or every attachment.

The subsequent camera-comfort v4 reduced the shared locomotion carrier to 10%.
Archive SHA-256: `44c05193306dfefa81e092f6035049d2303d559a2321c8e463a3e01e071770d1`.
Its offline checks passed, but the user rejected the gun feel: the camera was reduced
and the gun lost the movement they liked. This is a failed requirement, not an
accepted comfort build. Preserve v3's full weapon motion and its camera complaint;
keep v4's rejection visible even when a later candidate passes technical checks.

Record the effective enabled folder and archive hash again when resuming. Earlier
HK416 handoffs referred to a disabled Recovery folder; the user later installed the
working build in a different folder. A historical path is not current load evidence.

## Source reference and replacement geometry have separate jobs

1. Trace the actual RoN weapon class to its mesh, full skeleton, animation-data
   record, paired body/weapon sequences and montages. Verify decoded local samples,
   source bases, clocks, component mounts, visibility and mechanism behavior.
2. Import the matching RoN model as a reference when needed for accurate animation
   reconstruction. Keep that reference distinct from the final replacement model.
3. Assemble the chosen CGTrader parts, checking real dimensions, axes, pivots and
   grip surfaces against the reference. Fit the replacement and derive its own
   receiver, magazine, stock, support-hand and trigger-hand landmarks. Preserve the
   original assets; do not deform the skeleton or stretch limbs to hide a mismatch.
4. Transfer the source motion to the verified native target rig and container.
   Keep nonstretch reach, finger/surface contact and graph controls explicit. Use
   phase-dependent grip release during reloads; a permanent two-hand lock would
   destroy the source action. Inspect the final replacement's mechanism travel.
5. Take one representative clip through native readback, the shipped archive and
   identified runtime acceptance before expanding the set. The HK416's success
   establishes this route, not MP5 offsets, clip dispatch or package acceptance.

The HK416 used a CG receiver/barrel and Geissele handguard while retaining RoN
animation lineage. Its calibration is not an MP5 template. A model swap needs new
surface and mechanism checks even when source animation decoding already works.
Keep purchased/game assets private; publish reusable instructions and original
helpers, not the source meshes, extracted animations or textures.

## Locomotion contact must survive partial additive weights

The original full-weight preview kept both hands near the gun, yet the user saw
separation while walking and sprinting. Sampling weights 0, 0.25, 0.5, 0.75 and 1
reproduced up to 5.328 mm of support-hand drift in the earlier sprint candidate.
Therefore a full-weight endpoint check cannot certify the locomotion blend.

For this native rig, apply the same locomotion carrier to `Hips` and the separate
`Torso_COG_Control_JNT` branch, retaining grip-relative descendant poses. The
current game graph reconstructs the torso through controls and copies weapon
controls into the driven weapon bones; moving only the visible FK hierarchy is
insufficient. Reconstruct parents first, then synchronize the required hand/weapon
controls. Inspect the current graph instead of hardcoding historical node numbers.

Verify the actual walk/jog/sprint dispatch, source-transform caching and blend
weight route. Check hand-to-gun transforms through the complete loops, intermediate
weights and sampled sprint-start/stop bases. Keep anatomical local translations,
scales and finger shapes unless the measured fixture calls for a separate change.
The HK416 local-additive probe checked 2,430 poses per build across both bodies and
500 transition combinations; these counts are coverage receipts, not universal
thresholds or an execution of the complete engine graph, masks or IK solver.

## Camera comfort is an independent requirement

A carrier can fix contact while introducing camera bob. Full-weight camera
compensation did not cancel intermediate blends: v3 failed its original 0.25 mm
camera-preservation tolerance, reaching about 1.91 mm in the offline model. The
user subsequently reported excessive in-game camera movement.

A request to reduce camera shake does not authorize reducing the shared gun/body
carrier. Preserve the identified full-amplitude weapon baseline. Inspect the actual
camera branch, inherited parent motion and separate headbob layers before editing;
a camera-named channel alone does not establish final camera ownership. After two
failed corrections, use the failure ledger and a discriminating source/graph or
runtime check before another change.

The current-game HK416 investigation found separate male/female `head_bobbing.anims`
sets. The base graph's camera locomotion state consumes `add_walk_0`, `add_jog_0`,
`add_sprint_0` and their transitions/upperbody variants, distinct from the private
`add_*_weapon_0` clips. Native camera Aim/Target translation keys reach about 84 mm
in sprint. Upperbody variants also contain torso motion: scaling the entire clip
would change more than the camera.

The camera-only candidate restores v3 weapon sets byte-for-byte and scopes private
headbob sets with the existing equipped-HK wrapper. It scales only camera-branch
additive translation and rotation deltas to 0.1 in 42 walk/jog/sprint and transition
clips per body. Keep non-camera bytes, key times, events, float tracks and scale
unchanged. Check quantized rotation error explicitly; 10% authored gain does not
prove 90% less total on-screen motion. Do not copy game assets into this repository.

Confirm native serialization/readback and package identities separately from
runtime. Test walking, strafing, sprint entry/exit and ADS with the same save, FOV,
body and hand mods. The gun should retain the v3 movement and both grips; hard
camera bob should diminish. Check a different weapon after unequipping to confirm
scope. Camera-only gameplay and comfort remain OPEN until that identified build is
tested. Do not treat source inspection or the earlier v4 test as that acceptance.

## Keep the native clock and untouched behavior

For selected edits, preserve the original native key times. Combining a regular
60 Hz grid with nearly identical decoded key times produced colliding native
clock bins in an earlier attempt. Reject duplicate quantized ticks; do not silently
discard a peak or alter timing to make import pass. Use dense/exact-key samples for
verification without forcing all verification times into the authored key set.

Use the existing selected-clip writer and independent readback. Compare both player
variants, untouched descriptors/chunks, events, float tracks, scale and additive
semantics. Then extract the packed archive and compare every shipped resource and
loose-file hash. V4 changed three locomotion loops per body and preserved 121 other player clips.
The camera-only correction instead restores both complete v3 weapon sets and adds
scoped camera sets, retaining CG resources, scripts and audio. Prior script compile
evidence may be reused only by exact payload identity; label it as reused.

Preserve the working archive and manager settings before an authorized update.
Use the existing enabled mod when the user's workflow calls for that; record the
new installed hashes and rollback location. A game launch stays user-controlled.
