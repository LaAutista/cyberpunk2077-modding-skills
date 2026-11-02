# Contact and nonstretch adaptation

Preserve target anatomical local translation, scale and bone lengths. Solve
rotational motion and calibrated weapon/component placement. Virtual attachment
controls may translate when the native graph explicitly requires it; that is not
permission to translate finger joints or stretch arms to conceal contact errors.

Use nonstretch two-bone reach with source-guided pole and axial orientation.
Report distance to the original desired goal separately from a clamped reachable
goal. Reachability alone says nothing about pad-plane contact, thumb opposition,
receiver clearance, skin deformation or finger proportions.

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

## Palm-relative finger rotation

Start with one reversible problematic clip. Map wrist, palm, thumb and all digit
chains on both rigs, including terminal landmarks. Record names, parentage, rest
orientations, length/scale, handedness and any inferred tip axis. A missing terminal
joint is a disclosed limitation, not permission to invent source skin contact.

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

Change rotations only for this finger repair. Preserve joint translations, lengths,
scales, wrist/arm/body motion, source timing, other digits and unrelated clips.
Do not substitute a generic fist or grip preset. Show complete source/native and
before/after playback, both hands, open/closed poses, thumbs and contact, under the
[source comparison gate](../SKILL.md#mandatory-source-versus-retarget-comparison).
Report remaining surface failures and obtain the one-clip review before expansion.

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
