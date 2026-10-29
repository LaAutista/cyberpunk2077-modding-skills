# Spaces, rest and bind contracts

Use this chapter when an apparently correct rest pose breaks during animation,
controls jump under a retained parent, or a hand fits only after joint translation.
Evidence IDs resolve in the [register](evidence-register.md).

## Native skeleton versus animator controls

**A custom human-facing control/animator rig is optional.** Direct source-to-target
retargeting on raw/native skeletons is a valid route; do not require an animator
rig, handles, IK/FK UI or a separate rig project's completion before using it.
An FK mapping or analytic IK/contact solver can write native joint channels directly.

| Component | Direct-skeleton route | Optional animator-rig route |
| --- | --- | --- |
| Native motion/deformation skeleton | Preserve the actual target hierarchy, channel identities and required deformation dependencies. | The same native contract remains the output. |
| Rest/reference and per-mesh inverse binds | Calibrate frames explicitly; retain distinct rest and skin-bind conventions. | Control rests do not replace native rests or mesh binds. |
| Skin and required evaluated helpers | Preserve all influences/binds and evaluate helpers actually required by the chosen target skin/path. | Widgets/authoring handles do not supply missing native deformation behavior. |
| Human-facing controls | Not required; mapping and solvers act on the native skeleton. | Add handles, constraints or space switching only when useful; bake to native channels. |
| Exporter | Validate the chosen native export/readback contract. | Exclude custom widgets, diagnostic objects and solver-only bones from native output. |

Regenerating a control rig is not permission to rename/reparent the native
hierarchy or rebind its skin. Conversely, skipping it does not permit dropping
required native helper bones, weights or evaluated deformation.

**PROVEN as inspected architecture, F2:** Bingle's MMD retargeter maps calibrated
source skeleton rotations directly onto target pose bones, in hierarchy order,
with optional two-bone IK and post-IK descendants (`_mapped_rotation:927–948`,
`_mapped_local_rotation:951–978`, `_apply_fk_mappings:1347–1402`,
`_apply_frame:1902–1935` in the pinned source). This demonstrates that a human-facing
animator rig is not fundamental to the method; it is not an executed CP port or
proof of compatibility with CP bindings/helpers/export.

For either route, validate calibrated rest/axis mapping and FK rotation order,
then add nonstretch IK/pole/contact compensation where proportions or contacts
require it. Recompute destination parents before children; preserve native offsets,
lengths/scales and intentional source channels. Do not blindly copy rotations or
assume a retargeter is a reversible black box. Verify each direction actually used
against declared inputs/outputs; one-way pose agreement does not prove an inverse.

Do not block a direct-skeleton port on an unfinished animator rig. A block tied
to shared rig work needs a **demonstrated defect in a native component actually
used by that path**—for example its skeleton/rest/bind, skin, required helper
evaluation or exporter—with an exact failing fixture/revision and dependency.
Scope that block to affected paths; other native routes can proceed independently.
Source, visual, native/package and runtime gates still apply, including the
[full-motion/360° converted-target review](qa-debugging.md#mandatory-blender-visual-acceptance).

**PROVEN, H1/H2:** a serialized rig, exported GLB and procedural helper graph can
represent different parts of the evaluated character. A skeleton export alone is
not the complete deformation system. **INFERRED transfer:** treat controls,
native transforms and per-mesh deformation bindings as separate layers, with a
declared conversion at each boundary.

## Record spaces before copying channels

For each source/target pair record: units, handedness, basis axes, quaternion
ordering, local/world convention, parent order, root ownership, object transforms,
rest locals, inverse binds, mesh bind space, skin joint indices and all influences.
Record whether a clip is absolute, additive, bind-relative or already base-composed.
A shared bone name is only a mapping candidate.

With column vectors, let `L_i` be bone local and `W_i = W_parent L_i` world.
Let `C` convert a coordinate basis and `A` be a world placement/alignment. A basis
change is `C W C^-1`; a placement is `A W`. They are different operations. Convert
translations with the unit scale exactly once. A reflection can alter winding and
tangent/normal orientation; check those explicitly instead of guessing a quaternion
sign flip. Declare any different matrix convention in the adapter.

For a desired world goal `G_i` under the **actual destination** parent, solve
`L_i = inverse(W_parent_destination) G_i`, updating parent-first. Use the rig's
declared inheritance behavior where it differs from ordinary TRS composition.

**PROVEN, R2:** copying source child controls under retained target ancestors
produced roughly 116 mm error when parent worlds differed by up to 114 mm.
Updating an offset parent while using its stale world matrix also invalidated IK
goals. Solve destination locals after the parent update; a global weapon offset
does not repair an incorrect control-space equation.

## Rest is not inverse bind

The rig's rest/control pose need not equal every mesh's skin bind. For conventional
linear blend skinning, each influence contributes `W_i(t) inverseBind_i v_bind`,
with declared mesh/object-space factors around it. Preserve the complete contract,
not just the visible bind silhouette. If you need control bones and deformation
children, document which layer owns each matrix and how mesh bind compensation is
applied. Do not multiply that compensation twice.

**PROVEN, R3:** a first handoff preserved a posed silhouette while hiding about
0.54–0.57 m compensating thumb translations. A revised full-native-control and
per-mesh-deformation arrangement repaired the interchange contract; that did not
prove native runtime thumb behavior. Holding the rest pose equal while deliberately
changing a parent is a useful negative control: the same clip must expose the
incorrect parent in motion.

When transferring articulation, define source and target reference frames first.
For a declared local-space delta convention, `D = inverse(R_source) P_source`
and `P_target = R_target D` are a starting model. A joint-axis correspondence may
require conjugating `D` by a calibrated basis. **INFERRED:** this is a mapping
model, not a substitute for source graph reconstruction or a validated finger fit.
Test noncommuting rotations; a neutral-pose identity test cannot catch reversed
quaternion multiplication.

## Preserve geometry and intentional channels

Keep native arm/finger local offsets, scales, lengths and hierarchy when solving
pose rotations. Do not apply a pose as rest, stretch fingers or move their joints
to conceal a grip mismatch. Preserve translation/scale channels that are actually
authored mechanisms or graph outputs; record permitted exceptions per bone/channel.
“Never translate anything” would incorrectly erase magazine/bolt motion and source
translation-retarget semantics.

**PROVEN, H3:** all 77 inspected serialized Halo arm BoneTree entries used
`Animation` translation mode. Forcing their bind translations is unsupported by
that source evidence. Distinguish this **source evaluation** question from the
later **target proportions/contact** problem.

Before motion transfer, complete the [finger checkpoint](finger-checkpoint.md).
If the source pose is already wrong, return to the [source adapter](source-playback-adapters.md),
not to target finger corrections.
