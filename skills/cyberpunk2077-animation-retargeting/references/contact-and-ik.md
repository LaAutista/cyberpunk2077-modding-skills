# Contact and nonstretch adaptation

Before choosing a rotation-only mapping, inventory the evaluated source's local
T/Q/S channels and segment-length variation for the mapped arm, wrist and digits.
Separate authored local translation from graph/IK or translation-retargeting
effects. Constant target anatomy does not prove source translations are constant:
if they contribute to reach or contact, record what the target cannot reproduce
and test a declared adaptation instead of silently dropping that motion. Use the
[source contract](source-adapters.md) and reuse its checked channel inventory.

Preserve target anatomical local translation, scale and bone lengths. Solve
rotational motion and calibrated weapon/component placement. Virtual attachment
controls may translate when the native graph explicitly requires it; that is not
permission to translate finger joints or stretch arms to conceal contact errors.

Use nonstretch two-bone reach with source-guided pole and axial orientation.
Report distance to the original desired goal separately from a clamped reachable
goal. Reachability alone says nothing about pad-plane contact, thumb opposition,
receiver clearance, skin deformation or finger proportions.

Compare anatomical directions as well as hand goals: elbow-to-wrist against
wrist-to-middle-knuckle, signed bends in the measured palm frame, and
shoulder-to-wrist distance divided by upper-arm plus forearm length. Record source
and native values at the reference and critical contact/release poses. A matched
palm orientation or reachable wrist can still add excessive wrist bend when
native arm lengths, shoulder placement or extension differ. Bone-local Euler
angles and source sleeve silhouettes do not establish anatomical agreement.

For reloads define phase ownership before fitting: extraction, held magazine,
reinsertion, release/regrip and settled return may follow different frames. One
fixed grip across manipulation changes the source mechanics. Measure contact
frames at phase boundaries, inspect the transition and interpolated motion, then
fit. A new failed grip hypothesis counts toward the same blocking gate's repair
budget; rename neither the artifact nor the hypothesis to escape the loop breaker.

Inspect each digit/thumb, palm/wrist, elbow, mechanism and relevant hidden surfaces
against source and final target. Stale controller arrays, static arm roll,
nearest-parent terminal-helper approximations and linearized nonlinear helpers can
pass a few endpoints while failing between them. Use extremes, hold/release and
fast-motion samples as discriminators, then full-motion review for acceptance.

Read [proportions and contact phases](../../cyberpunk2077-modding/references/animation-retargeting/proportions-contact.md),
[finger checkpoint](../../cyberpunk2077-modding/references/animation-retargeting/finger-checkpoint.md)
and [helpers/skin](../../cyberpunk2077-modding/references/animation-retargeting/native-deformation.md).
Reuse their measured fixtures; do not transfer HK416 offsets to another assembly.

Before fitting a digit, diff the actual expanded deformation graph for a small
perturbation of each proposed driver. A metacarpal can drive another digit's
muscle helpers even when that digit's anatomical tracks are unchanged. Include
those helpers and their weighted skin in the early regression: other-digit
versus weapon contact, as well as digit-versus-digit contact. If a trial worsens
a neighboring surface, isolate which driver causes it before serializing or
batching. Do not certify preservation from raw skeleton tracks alone.

## Thin trigger and guard contact

Nearest oriented face offsets are local winding-relative witnesses, not closed
volume penetration depths. A point in a thin guard can be nearer the outer face
although the intended free space is on the inner side. Before fitting an escape,
identify the intended side using the actual surface, an opening ray or an
equivalent geometric witness. Reduced nearest-face cost alone is insufficient.
Check actual triangle intersections, both sides of the skin and the complete
curl/release range after the correction; preserve the failed pose and compare
unrelated digits, wrist and arm. Reuse the existing finger checkpoint and
contact trajectory checks, without transferring weapon-specific offsets.

## Palm-relative finger rotation

Start with one reversible problematic clip. Map wrist, palm, thumb and all digit
chains on both rigs, including terminal landmarks. Record names, parentage, rest
orientations, length/scale, handedness and any inferred tip axis. A missing terminal
joint is a disclosed limitation, not permission to invent source skin contact.
An incoming phalanx axis is only a terminal-axis hypothesis. Compare it with the
actual distal skin in that mesh's own inverse-bind space; retain the weight/cap or
other landmark selection and its sensitivity. A PCA axis, cap-centroid ray and
authored tip joint are different measurements, not interchangeable calibrations.

For each rig, construct an orthonormal palm frame from the wrist and suitable
index-side/pinky-side knuckles: a forward wrist-to-knuckle-midpoint direction, an
across-palm direction orthogonalized against it, and their cross-product normal.
Declare axis order and left/right sign conventions, verify a proper rotation
frame, and account explicitly for mirrored input bases. Do not guess signs from
bone names. Degenerate landmarks need another measured frame before proceeding.

For each segment compute `d = normalize(next_joint - joint)` and express it in
that rig's palm frame. Compare source pose versus source rest, then apply the
calibrated correspondence to the target rest direction. Use clamped dot products
for alignment and cross products for rotation direction. Near parallel/opposite
directions need a stable rest-derived axis and temporal continuity, not a random
cross-product fallback. Convert the desired orientation to target parent-local
rotation using the already-updated target parent.

Direction constrains swing but leaves twist ambiguous. Preserve source/rest bone
orientation information to transfer twist around the segment axis, check quaternion
hemisphere continuity and review signed bends. Handle thumb opposition and its
different chain separately; use measured anatomical limits without silently
flattening source articulation. A direction match alone is not a contact pass.
Sequential parent swing can also change a child's axial roll while leaving its
ray correct. When each bone has an independently mapped source-derived world
orientation, freeze that orientation and its ray before correcting the chain.
Apply the shortest swing to that snapshot; use the updated parent only to
reconstruct the local rotation. Reusing the child world orientation after its
parent correction adds transport that this mapping did not request. If parent
transport is intentional, state that different contract instead. Compare full
orientations and signed axial differences around the common final ray, then
actual skin; a direction-only residual cannot detect this failure. Re-run the
existing `finger-parent-transport` workflow case and the owning project's exact
pre-calibration capture/native replay before promoting a correction. Mathematical
transverse axes measure algorithmic roll, not independently known anatomical
roll; do not infer the latter from an ill-conditioned fingertip patch normal.

Change rotations only for this finger repair. Preserve joint translations, lengths,
scales, wrist/arm/body motion, source timing, other digits and unrelated clips.
Do not substitute a generic fist or grip preset. Show complete source/native and
before/after playback, both hands, open/closed poses, thumbs and contact, under the
[source comparison gate](../SKILL.md#mandatory-source-versus-retarget-comparison).
Report remaining surface failures and obtain the one-clip review before expansion.
When contact improves, compare the original and corrected inter-joint curl, twist,
knuckle placement and open/released shapes on the same clock. Removing a skin
intersection by opening a distal chain can introduce a different visible failure.
Keep the original articulation and the measured tradeoff in the same receipt;
check the other digits and wrist/arm before carrying the change to another clip.

## Do not preserve a broken reference grip

A rest-relative solver can transfer source motion changes accurately while keeping
an incorrect target reference bend. Compare the actual source and target reference
finger segments first: treating a curved source joint as zero against a straight
target joint can carry a fixed bend error through the entire clip and reverse the
bend during release. Recalibrate the anatomical reference using the measured palm
frames and native bone axes; do not disguise the error with a fingertip-only hook.
Verify both signed bend direction and magnitude, original source-driven twist,
continuity and skin contact. A base-knuckle offset needed by replacement geometry
must be declared separately from the original inter-joint articulation. Do not
flatten genuine fast source motion merely to satisfy an arbitrary per-frame limit;
compare source and target angular changes on the same clock and inspect playback.
