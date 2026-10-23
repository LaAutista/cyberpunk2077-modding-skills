# Weapon rigging and animation adaptation

Use this method for a new replacement or an existing rig defect. The method comes
from the Lynx investigation; its numeric offsets, donor mapping and scripts are
weapon-specific. Preserve the requested appearance, alignment, mechanics, timing
and unrelated motion. This reference does not authorize deployment or game launch.

## References and evidence status

- Start with the [topic and upstream documentation map](topic-map.md),
  [environment requirements](environment.md) and [tool-selection guide](tool-selection.md).
  Version-check external documentation against the assets and tools in use.
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

## 1. Establish both assemblies before fitting

Preserve a baseline of the complete donor and replacement, current blend/GLBs,
native meshes/rigs/animations, assembly/build inputs and release identity. Record
hashes, units and coordinate conversions. An installed mod, working project and
old donor export may represent different revisions; identify which is being fixed.
Keep evidence and diagnostic objects out of shipping assets. Use existing tools;
Python is appropriate inside the established Blender/modding pipeline, not a reason
to introduce a new toolchain.

Inspect both models in Blender and record a part-to-motion map before editing:

| Inspect | Establish |
| --- | --- |
| Dimensions and transforms | Units, axes, object/armature transforms, handedness, receiver length, bore/sight axis, grip/trigger, foregrip, magazine well and moving-part envelopes in one coordinate space. Record any deliberate fitting transform. |
| Mesh organization | Named parts within merged chunks, topology, normals, materials/UVs, LODs and matching shadows. Check hidden/duplicate components as well as the visible silhouette. |
| Rig and pivots | Bone names, hierarchy, rest/local/world matrices, joint centers/axes, inverse binds, component mounts and attachment slots. A mesh-only export can lack hierarchy; recover it from the correct rig/entity. |
| Bone assignments and weights | Which bone moves each part, rigid versus deforming sections, all weight sets, unassigned vertices, normalization and accidental mixed weights. A fixed bracket and a folding leaf need not share a bone. |
| Dependencies | Entity/appearance → component → mesh/rig/animation links, weapon-to-player mount, player camera route, animation sets/graph references, float visibility tracks, events, additive clips and supported player variants. |

Compare the donor's actual trajectories and hand paths with the replacement's
mechanics and dimensions. Similar weapon type, a matching idle pose or shared bone
names are not animation compatibility. Establish contact landmarks and required
travel before fitting; do not globally stretch the weapon to match one hand pose.

## 2. Recover motion and prove playback

Trace the actual component references to recover receiver, barrel, magazine and
other moving-part clips plus matching player-arm clips, rigs and full arm meshes.
Use the existing WolvenKit export/serialization path. Do not interpret an empty
Blender Actions list as missing native animation. Keep an explicit clip inventory:
name, resource/hash, duration, timebase, affected bones, arm counterpart, additive
base, event/visibility dependencies, availability and confidence.

Build a review matrix for affected draw/first-equip, firing/recoil and reload clips:
empty and partial, alternate/ADS variants, supported player rigs, return-to-idle
and transition endpoints. Mark unavailable or not-applicable entries with reasons.
Select coverage by changed bones, neighbors and contact dependencies, not names
alone; one clean reload does not validate a shared bone's first-equip motion.

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

When packaging is in scope, extract the completed archive, compare shipped resources
with verified inputs and inspect packaged animation readback. A build or ZIP test
cannot prove rig behavior. Follow the existing installation policy only when that
action is in scope; this method does not authorize publication or a game launch.

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
