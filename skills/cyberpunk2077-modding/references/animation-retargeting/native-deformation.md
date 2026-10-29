# Native helpers, skin and normals

Use when main bones agree but palms, twists, nails or shading fail. Evidence IDs
resolve in the [register](evidence-register.md). Preserve the raw failed views and
separate transform, geometry, normals and runtime conclusions.

## Preserve distinct domains

**PROVEN, H1/H2:** the current CP diagnostic separates animator FK controls,
Native152 animation/export skeleton, D183 deformation graph and a 167-joint
own-bind skin palette. The prior preview describes 109 private helper joints;
current first-person positively used outputs are 87 PMA / 84 PWA. Those are
different counts, not interchangeable descriptions of one list.
The custom animator-control layer is optional; direct native-skeleton retargeting
still preserves the chosen skin's required native helper evaluation and binds.
An unfinished control UI or V4 authoring feature is not itself a direct-port blocker.

A helper's name or nearest native ancestor does not define its evaluation.
The current CP V4 authoring scaffold remains **FK-only**; optional nonstretch
control-side IK/poles are proposed work, not an implemented V4 solver. Its native
constraint/helper evaluation is distinct from those animator-facing IK controls.
Preserve graph dependency/order, temporary reference locals, sex-specific parameters,
left/right operation order, driver bases and condition context. Thumb-web helpers
can depend on index drivers. A hand-only fixture reads 30 model-space drivers,
80 temporaries and 112 ordered operations to produce 32 hand muscle joints.
Temporary graph reference transforms are not mesh inverse binds or a generic A-pose.

The tested high-quality binding is N152 → D183 → shadow with 66 non-Root shared
anchors and private helper reference locals. The old extra Root copy was inert
for identity-Root clips, not a general root adapter. Current condition proof uses
evaluation LOD0 and skip-performance byte 0. Signed native comparison is
`currentLOD <= conditionLOD`; this does not establish the live actor context.

## Failed approaches and regression guards

| Failed approach | Why it failed | Guard to keep |
| --- | --- | --- |
| Follow nearest ancestor for helpers | Omits muscle/twist operations and cross-digit drivers. | Compare actual graph outputs, skin and extremes against independent source/evaluator evidence. |
| Reversed signed Twist cross product | Wrong orientation/sign despite plausible neutral pose. | Native order `cross(A_forward,A_perpendicular)`; retained independent 600 scalar fixtures. |
| Bake helpers every half frame and interpolate | Nonlinear graph differs between baked samples, recorded up to 8.899 mm / 4.115°. | Evaluate helpers at the actual requested time after source controls; include quarter intervals. |
| Validate only keys and midpoints | Normalized quaternion components can agree there yet differ from SLERP off midpoint. | Immutable exported-GLB sampling compared independently at quarter/off-grid times. |
| Check only rest normals | Large posed hand-normal errors remained in the older preview. | Compare posed source-compute normal field and skin, including packed output contract. |
| Canonicalize root placement to make fixture pass | Extends beyond validated placement assumptions. | Preserve Root/Trajectory/object-space rejection until an explicit adapter is independently verified. |

These are **PROVEN bounded failures**, not evidence that every alternative solver
is impossible. Current V4 guards reject arbitrary root/trajectory/object placement,
nonunit native local scales, retained shear and nonfinite poses before helper/normal
writes. Inspect the exact fixture contract before using it on a new scene.

## Skin and normals are separate checks

**PROVEN static instruction/data result, H2:** installed shader interpretation uses
normalized all-eight-influence affine LBS; normals use the same blended 3×3 matrix,
normalization and UNorm10 packing. Generic inverse-transpose advice is not a
substitute for matching this observed implementation. Preserve both influence
sets, named joints and full bind matrices. Check dropped/renormalized influences,
joint-index remaps, bone-palette selection and quantized positions independently.

The reusable evaluator matched an independent actual-SSA interpreter on 105,675
samples for positions, normal core and packed normals. That is not a native GPU
dispatch, final draw or runtime pose pass. Optional post-LBS geometric correction,
upload/remapping and loaded renderer context remain unverified.

V3/V4 uses a post-armature source-compute normal field without editing geometry,
weights or binds. Keep evaluation order explicit: reference control sample → native
constraints → graph helpers → source normal field. Opt-in preview start/stop must
restore Action/slot, manual poses, float metadata, helpers and normal state even
on exceptions. Do not install a load handler or overwrite the owner's open scene.

## What the V4 pass proves

892 Native152 sampled reference comparisons pass, worst position 0.002209 mm and
rotation 0.000121656°. Separate recorded skin observation covers 864 poses and
sampled corner-normal agreement; 688 actual Workbench panels were reviewed.
This is bounded exported-reference/CPU preview evidence.

The PMA reload frame 158.25 +Y bright crescent is interior palm/thumb-base geometry,
mostly chunk 3. It is not explained as an open rim or opposite arm. Anatomy/native
shape, occluded pads/webs, hidden surfaces, unsampled motion, runtime parity and
Halo source contact remain unaccepted. Do not turn “no gross exposed collapse in
reviewed panels” into a complete hand-deformation pass.

## Next diagnostic when skin still fails

Hold the native driver pose fixed. Compare helper worlds → skin matrices → posed
vertices → posed normals → final renderer, changing one boundary at a time. Check
the interior palm/underside at the known failing pose, neighboring times and a
neutral reference. Record body variant, camera, normal source, chunk/palette and
root context. If drivers already disagree, return to source/reference sampling.
If skin matches a source compute result but the source anatomy is not accepted,
label that shape question separately; a matching implementation cannot certify it.
