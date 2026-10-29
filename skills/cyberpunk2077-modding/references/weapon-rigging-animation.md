# Weapon rigging and animation adaptation

Use this method for a new replacement or an existing rig defect. The method comes
from the Lynx investigation; its numeric offsets, donor mapping and scripts are
weapon-specific. Preserve the requested appearance, alignment, mechanics, timing
and unrelated motion. This reference does not authorize deployment or game launch.

## References and evidence status

Choose a case supplement only when it applies: [Unreal/RoN source recovery and
porting](ron-port-workflow.md), [HK416 recovery](hk416-recovery-contract.md), or
[HK416 status and unresolved issues](ron-hk416-case-study.md). The generic behavior
and acceptance ledger below still applies to the selected weapon; case-specific
mappings, offsets and private commands do not become universal defaults.

- Use the [topic map](topic-map.md) for relevant sources and the
  [resource pipeline](resource-pipeline.md) for import/readback. Check
  [environment requirements](environment.md) when setup is unclear; version-match
  sources against the assets and tools actually in use.
- The [Lynx case study](../../weapon-animation-inspection/references/lynx-case-study.md)
  records the original investigation's recovery, playback, correction and checks;
  its [command contracts](../../weapon-animation-inspection/references/lynx-command-contracts.md)
  distinguish external CLI use from project adapters absent from this repository.
  The case's assets, screenshots and raw evidence remain in the original project;
  the published prose records historical results, not a fresh-clone reproduction.
- Proven on Lynx: native track recovery, full-sequence rendering, explicit image
  review, local mesh/weight/pivot/motion corrections, independent playback checks,
  native surface tests and package readback. Those results cover the stated assets,
  sample times and views. A successful command is not visual or gameplay evidence.
- The choices below are diagnostic options, not a claim that every option has
  worked on every weapon. New rig mappings, codecs, IK, graph reconstruction,
  custom arms or alternate exports need their own proof. Keep proposed techniques
  labelled untested until exercised and inspected.
- For imported Fallout/CAT or Scenario advice, use the [comparison and tested
  boundaries](fo4-scenario-comparison.md), including fixed-animation parent tests
  and the Cyberpunk exception to generic four-influence export guidance.
  When already available, use `scenario-blender-rigging`, `scenario-blender-animation`
  and `scenario-blender-export` as optional diagnostics after checking their versions;
  keep their source skills separate. Generic centering, rest-pose application,
  Rigify regeneration, four-weight limits and retiming are not native-port defaults.

## Acceptance ledger

Keep one project-local checklist using the existing manifest/notes format, not a
new toolchain. For each stage and behavior row record input revision/hashes, source
availability, evidence paths, inspected times/views, result and remaining action.
Use **PASS** only for the stated checks actually completed, **FAIL** for a demonstrated
defect, and **UNVERIFIED** for missing inputs, unrun checks or unsupported playback.
Track availability separately as available, missing or not applicable with a reason;
a missing clip or an approved approximation is not a source-fidelity pass. A narrower
mechanism check can pass while hand, transition or gameplay acceptance stays unverified.

| Stage | Evidence required to pass that stage |
| --- | --- |
| Source identity/playback | Proven model/rig/clip pairing, inventory and original appearance/motion reference; unexplained source deformation blocks fitting acceptance. |
| Retarget/bind | Explicit mapping, preserved rest/bind and channel semantics, complete affected deformation/contact coverage. |
| Visual | Viewed matched source/retarget/native images, every digit accounted for, stated temporal coverage and no unresolved visible defect within it. |
| Native/package | Independent readback of actual cooked and, when in scope, extracted packaged resources; semantic and identity checks. |
| Runtime | Authorized game evidence for dispatch, blends, interruptions, contacts, attachments/collision and player displacement on the identified package. Offline tests leave this UNVERIFIED. |

Do not promote a candidate past a failed dependency. Continue independent diagnostics;
carry missing inputs and fallbacks into the handoff. Reopen affected gates after any
candidate change. These gates reduce repeated mistakes; they do not guarantee a
perfect first port or a fixed completion time.

## 1. Establish both assemblies before fitting

Preserve a baseline of the complete donor and replacement, current blend/GLBs,
native meshes/rigs/animations, assembly/build inputs and release identity. Record
hashes, units and coordinate conversions. Pin exporter/importer/helper versions or
commits, settings and script hashes, including optional Scenario helpers. An
installed mod, working project and
old donor export may represent different revisions; identify which is being fixed.
Keep evidence and diagnostic objects out of shipping assets. Use existing tools;
Python is appropriate inside the established Blender/modding pipeline, not a reason
to introduce a new toolchain.

Inspect both models in Blender and record a part-to-motion map before editing:

| Inspect | Establish |
| --- | --- |
| Dimensions and transforms | Units, axes, object/armature transforms, handedness, receiver length, bore/sight axis, grip/trigger, foregrip, magazine well and moving-part envelopes in one coordinate space. Record any deliberate fitting transform. |
| Mesh organization | Named parts within merged chunks, topology, normals, materials/UVs, LODs and matching shadows. Check hidden/duplicate components as well as the visible silhouette. |
| Rig and pivots | Bone names/indices and mapping, hierarchy, rest/local/world matrices, joint centers/axes, inverse binds, component mounts and attachment slots. Prove the source mesh/skin, rig, clips and additive base belong together by resource references and bind agreement, not filename similarity. A mesh-only export can lack hierarchy; recover it from the correct rig/entity. |
| Bone assignments and weights | Which bone moves each part, rigid versus deforming sections, all weight sets, unassigned vertices, normalization and accidental mixed weights. A fixed bracket and a folding leaf need not share a bone. |
| Dependencies | Entity/appearance → component → mesh/rig/animation links, weapon-to-player mount, player camera route, animation sets/graph references, float visibility tracks, events, additive clips and supported player variants. |

Compare the donor's actual trajectories and hand paths with the replacement's
mechanics and dimensions. Similar weapon type, a matching idle pose or shared bone
names are not animation compatibility. Establish contact landmarks and required
travel before fitting; do not globally stretch the weapon to match one hand pose.

Before any pose correction, compare the untouched source import to its original
appearance at rest and in known poses. Record object/armature counts and ownership:
flag duplicated skins, skeletons, double armature modifiers, overlapping preview
and export rigs, wrong parent/socket, double transforms and unexpected roots. Multiple
native roots may be intentional; explain their owners rather than deleting them to
meet a generic one-root rule. Preview arms/helpers must not become shipping components.

Preserve source bind/rest transforms, bone lengths, rolls, scale and inverse binds;
record the explicit source-to-target coordinate conversion separately. Preserve the
target native bind as its own contract. Pose fingers/limbs by rotation about the
correct local joint axes; do not move joint heads/tails, translate phalanges, stretch
limbs or apply a pose as rest to force contact. Retain authored translation/scale
where the source mechanics actually require it. Any intentional change needs named
bone/channel, space, reason and before/after deformation evidence, not a blanket ban
on translations. Inspect wrist/palm, thumb base/opposition and each finger's full
proximal-to-tip parent chain, knuckle spacing, weights and corrective deformation;
matching rest positions alone cannot establish animated equivalence.

## 2. Recover motion and prove playback

Trace the actual component references to recover receiver, barrel, magazine and
other moving-part clips plus matching player-arm clips, rigs and full arm meshes.
Use the existing WolvenKit export/serialization path. Do not interpret an empty
Blender Actions list as missing native animation. Keep an explicit clip inventory:
name, resource/hash, duration, timebase, affected bones, arm counterpart, additive
base, event/visibility dependencies, availability and confidence.

### Behavior coverage matrix

Before fitting, inventory the installed reference weapon's actual resource/graph
routes and observed behavior. When that reference is the installed COD weapon, use
its winning resources and identified build rather than assumptions about COD or a
stale export. Existing recordings can establish only what they show; an unrun game
check stays unverified. Keep the following rows in the project matrix and expand
variants by supported player/skin, attachment and state. For every row fill:
`reference behavior/resource → source clip + paired rig/base → target dispatch →
fallback/reason → source/retarget/native/runtime result + evidence`.

| Behavior | Coverage to resolve explicitly |
| --- | --- |
| Equip/unequip | First equip, repeat draw, holster and return endpoints. |
| Idle/rest/low ready | Each available stance, holds and return-to-idle; do not substitute one pose for all states. |
| Hipfire and fire | Hipfire stance, firing/recoil, recovery and repeated shots; weapon and arms together. |
| Aim/ADS | Source aim/ADS when supported, enter/hold/fire/exit and sight alignment; identify absent source variants. |
| Reload | Empty and tactical/partial separately, magazine/control contact, ammo/events and return state; ADS variants if present. |
| Walk/jog/sprint | Available direction/speed/stance variants, start/stop and hand/weapon contact under shared locomotion. |
| Melee | Available strike/recovery and interrupted return behavior. |
| Transitions/interruptions | Relevant idle/aim/fire/reload/locomotion/equip boundaries, cancel/restart and graph blends, not isolated clips alone. |

Select coverage by changed bones, neighbors, shared clips and contact dependencies,
not names alone. Record a missing source variant explicitly and choose a disclosed
fallback: retained target motion, a justified adaptation, reduced scope, or awaiting
source recovery. Identify its lineage and visual/runtime checks; do not invent a
source clip, claim an untested fallback works, or mark required target behavior not
applicable merely because the source lacks it. One clean reload does not validate
a shared bone's first-equip or sprint motion.

Reconstruct mounts and coordinate conversions before assessing hand alignment.
Use native rest matrices and original inverse binds; retain all skin influences.
Compare decoded poses against an independent export/import at endpoints and
intermediate times where supported. Verify key counts/timestamps, scale semantics,
float tracks and durations. Investigate disagreements without relaxing tolerances
or guessing an interpolation explanation. Lynx's closely spaced keys merged during
Blender import at 30 fps; expanding comparison time units preserved keys. That
workaround needs fresh key-preservation assertions on another asset.

Label each unavailable or approximated ingredient in the preview manifest and
report: static arms, neutral muscle correctives, missing runtime IK, additive/graph
blends, magazine switching, chosen FOV or shader substitutes. If authentic arms
cannot be recovered, complete mechanism inspection and keep hand acceptance open;
do not silently replace the missing motion with a convenient pose.

## 3. Render and actually inspect complete sequences

Render the complete applicable sequences including start/end frames in Blender,
with the assembled weapon and arms, from first-person and useful mechanism/contact
close-ups. Keep before/after inputs, clip, camera, timebase and player variant
matched. Use arms-disabled or cutaway views only as supplemental diagnostics.
Opaque views must establish the final appearance; adjust framing if fingers or
neighbors are cropped. Record completed manifests with input hashes and frame lists.

At each critical matched pose/time, capture **source original → retarget → final
native readback** from **top, left and right** in a declared common frame and at a
comparable scale. Preserve source camera/FOV for first-person comparison too. Add
palm/underside, thumb-web and finger/trigger/magazine close-ups wherever those three
views hide contact or deformation. Source original appearance and motion are primary
evidence; anatomical diagrams or real holding references can explain a joint/contact
but cannot replace it or justify silently redesigning the source pose. If the original
view or final-native playback cannot be recovered, label that comparison unverified.

Account for **both hands' thumb, index, middle, ring and little finger**, their full
joint chains and palm/wrist; mark each visible/inspected view and time or the missing
evidence. Look for collapsed or elongated segments, twisted joints, fused/splayed
digits, thumb opposition, knuckle creases, weight leaks and corrective pops. Inspect
the deformed skin, not just bone sticks or fingertip targets. Check grip/control
contact, floating or penetrating fingers and weapon/body clipping at rest, contacts,
releases, extremes and neighboring poses; a hidden digit cannot receive a visual pass.

Open the rendered images yourself. Review the full sequence at a declared cadence,
then every frame around fast motion, direction changes, contact/release and detected
collisions; use full-size frames where sheets obscure detail. Increase temporal
sampling around rapid sweeps, including native key times and subframes when needed
and supported. Existing Lynx rendering is 30 fps; its denser numeric probes do not
claim dense visual inspection. Record any unsampled visual interval. Rendered frames,
generated sheets and encoded videos alone are not reviewed frames or watched video.

Check proactively, even if the reported bug is narrower:

- Receiver/bolt/carrier/charging-handle/cover intersections; pivots, connected joints,
  full moving-part travel and clearance to the barrel, sights and attachments.
- Magazine removal, handoff, insertion angle/depth, hand contact, seating/release,
  duplicated or missing magazines and rounds, feed path and visibility transitions.
- Trigger finger placement during idle/fire/reload; palm/thumb/finger contact on the
  grip, foregrip and controls; penetration, floating hands and grasp/release timing.
- Draw, firing and reload variants, their endpoints, sight alignment, cover closure,
  shadows, unexpected scaling, sudden pops, hidden parts and unrelated motion.

Use targeted geometry probes to complement images: surface intersections, signed
or inside-depth checks with stated assumptions, contact distance and joint continuity.
AABB bounds or a fingertip distance alone cannot prove surface clearance or a good
grasp. Compare donor contact too: wrapped-finger internal overlap can exist in stock
assets. Distinguish it from visible exterior breakthrough. Document intentional
rigid joins narrowly; do not exempt a whole chunk or moving neighbor to obtain a pass.
Probe interpolated motion between keys as well as exact keys; passing poses can
still produce a crossing, stretch or pop in between. State sampling limits. Derive
numeric bounds from the actual source, scale, codec precision and intended contact;
record units and rationale. Do not impose a universal invented distance/angle
tolerance or widen an established gate to hide disagreement.

## 4. Diagnose, choose and apply a local correction

For each defect record the part, clip/frame/time, view and evidence, then identify
whether the cause is geometry, hierarchy/bind/weight, pivot, animation or inaccurate
playback. Reproduce the baseline defect with the same probe/preview used for the fix.

| Established cause | Candidate adjustment and preservation check |
| --- | --- |
| Wrong part follows a bone | Correct the named assignment or local weights; retain intentional deformation and check every clip using that bone. |
| Joint sweeps around the wrong center | Correct the local pivot/mount and compensate motion if needed; verify both joint attachment and hand trajectory throughout the sweep. |
| Small geometric interference | Relieve/refit only the demonstrated surface; preserve mechanics, wall thickness, silhouette, UV/material intent and nearby joints. |
| Motion does not fit replacement mechanics | Adapt the affected bone/channel in its correct space; preserve duration/events, unrelated tracks, idle/transition boundaries and intended travel/contact. |
| Many landmarks fail together | Revisit units, axes, mounts, binds and donor suitability before adding compensating deformations. |

Compare alternatives when tradeoffs matter. Capture candidate identity, changed
parts/channels, collision/contact results and visible cost. Reject fixes that hide
the defective part, cut away unrelated bodywork, distort the whole weapon or merely
move the collision into a hand/neighbor. A combined local correction may be smaller
and more faithful than a large mesh-only change. Preserve unsuccessful attempts as
evidence without treating them as proof that the problem is impossible.

## 5. Reinspect and verify the exported result

Repeat the affected complete sequences, dense intervals and proactive checks after
correction. Compare the whole assembly, including untouched parts, weights, UVs,
materials, rest bones and shadows. Explain every semantic change; hash-check assets
that should remain identical. Any final candidate change invalidates earlier
acceptance for that changed geometry/motion.

Export/cook through the project's established pipeline and compatible containers;
keep diagnostic cameras and arms out. Read back the actual native mesh and animation
where supported. Check topology, quantized positions, normals, UVs, bone identities,
weights/binds, references and animation keys/timing/events/float/scale data. Replay
the native readback with the same cameras/arms and inspect it. Run collision/contact
checks on cooked positions and decoded tracks, not only the source candidate.
Describe unsupported export checks explicitly. Preserve input hashes across tools.

Audit final component ownership, mounts and collision/physics shapes for extra
skeletons, diagnostic meshes, wrong attachments and unintended root-motion channels.
Compare root/weapon/camera trajectories and collision extents to the baseline; do
not zero intentional motion without evidence. The native authoring helper supports
only its declared no-root-motion contract; another mode needs a separate proven
route. Actual player pushing, lifting, snapping or camera displacement from an
attachment, collider or root motion requires runtime observation and stays unverified
offline, even when the resource audit passes.

When packaging is in scope, extract the completed archive, compare shipped resources
with verified inputs and inspect packaged animation readback. A build or ZIP test
cannot prove rig behavior. Follow the existing installation policy only when that
action is in scope; this method does not authorize publication or a game launch.

### Reusable regression checkpoints

Reuse the existing tools and retain small project-owned fixtures/checklists in the
project's evidence area; do not bundle game assets into the skills or add a second
Python dependency stack. Select controls that exercise the changed failure mode:

| Checkpoint/control | Existing route and acceptance boundary |
| --- | --- |
| Untouched baseline + one controlled channel change | [Native authoring regressions](native-animation-authoring.md): unchanged and selected-edit roundtrips, separate numeric/semantic gates, unselected integrity; tests certify their bounded serialization contract. |
| Wrong parent with rest pose held equal | [Fixed-animation parent comparison](fo4-scenario-comparison.md#verified-supplement-fixed-animation-parent-comparison): keep clip bytes fixed, demonstrate the negative control fails in motion, then restore the bind/parent. Its included fixture targets a rigid component, not finger-skin acceptance. |
| Lost influence set | [Weight export comparison](fo4-scenario-comparison.md#verified-exception-scenario-gltf-weights): compare named influences against source; retain the default-pruning negative control. Separately verify inverse binds and actual animated deformation; the weight-only fixture does not prove them. |
| Rotation versus joint translation | On isolated copies, compare local translation/scale and bone lengths to the pinned baseline at rest, keys and in-betweens. A deliberately translated finger/limb must trip the undeclared-channel/deformation check; a legitimate rotated pose must retain lengths and pass only after skin/contact review. Record this project-specific control as UNVERIFIED until run. |
| Visual/motion regression | Reuse one known contact/extreme and one transition from each affected matrix row, [preview/contact sheets](../../weapon-animation-inspection/references/contact-sheets.md), full-size digit views and a collision probe positive control. Expand to full affected sequences for acceptance; generated sheets start unreviewed. |
| Final-resource regression | Re-extract the packaged candidate, compare hashes/references to checked cooked inputs, and repeat readback/critical views from those extracted inputs. A prepack GLB or earlier package cannot certify the final one. |

Keep expected source behavior and failures with each fixture. Do not convert the
historical example's numbers into universal thresholds, waive a failed negative
control, or call these runtime tests. If inputs/tools are unavailable, keep the
checkpoint unverified and name the exact missing requirement.

## 6. Report coverage, remaining defects and the next decision

Separate **implemented**, **automatically checked**, **visually inspected** and
**user-reported/gameplay tested**. Give revision/package identity, commands actually
run, input hashes, sample rates, viewed clips/frames/timestamps/cameras/players,
before/after evidence and relevant limitations. Do not imply every generated frame
was viewed or every exported clip was visually accepted.

For each unresolved defect, report: exact part/location and clip/frame/time; linked
image/probe evidence; observed versus expected behavior; attempted fixes and why
they failed; remaining tradeoffs; the specific decision, asset, motion data or
environment needed to continue. Say "unresolved within these attempts" rather than
"impossible". Continue independent checks and bounded corrections within scope.

Give precise remaining user-controlled game checks with expected appearance and
behavior. Attribute a user's test to their tested package, clips and environment;
record missing identity/version details as unknown. The [Lynx laptop report](../../weapon-animation-inspection/references/lynx-case-study.md#user-reported-laptop-reload-test)
is positive reload evidence for that tested package, not proof of every animation,
platform, additive graph, custom arm setup or future build.
