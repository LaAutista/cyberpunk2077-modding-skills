---
name: cyberpunk2077-animation-retargeting
description: Retarget and repair Cyberpunk 2077 animation, hand poses, transitions and native playback. Use for motion mapping, additive bases or animgraph mismatches; not static mesh fitting.
metadata:
  version: "1.9.0"
---

# Cyberpunk animation retargeting

Own motion conversion and repair, native animation semantics and composed-pose
mismatches. For an unfamiliar weapon workflow or a snapping/contact regression,
follow the [weapon retargeting playbook](references/weapon-retargeting-playbook.md).
The [BF6 MP5 success case](references/bf6-mp5-success.md) explains the demonstrated
failures, exact recovery and remaining limits. Its calibration values are not defaults.

## Enter the project

Read the owning project's current STATUS/handoff and verify its current artifact
hash. Keep source, evaluated source, authored target, native readback, preview,
package and user-tested build identities separate. Preserve failed candidates.
For a new or failing route, choose one blocking question and discriminating fixture;
for an established route, reuse unchanged evidence and batch compatible actions.
Use the [pipeline and receipts](references/pipeline.md) without inventing passes.

Use sibling skills only for their actual responsibilities:

| Work | Owner |
| --- | --- |
| Motion mapping, fingers/arms, additive bases, transitions and graph diagnosis | This skill |
| Mesh fitting, native assembly, contact/deformation inspection and playback views | [Weapon inspection](../weapon-animation-inspection/SKILL.md) |
| Resource extraction, tooling, scripts/tweaks, packing and deployment | [Modding](../cyberpunk2077-modding/SKILL.md) |
| WolvenKit command options or documentation | [WolvenKit Docs](../wolvenkit-docs/SKILL.md) |

Generic Blender skills supply APIs and applicable authoring checks. Their defaults
for applying transforms, changing rest poses/FPS/loop keys, moving roots, cleaning
mocap or fixing every mesh must not overwrite the native contract or expand the
user's scope. Preserve native rests, inverse binds, anatomy, original clocks and
unrelated tracks unless a measured, authorized change requires otherwise.
A custom control rig is optional; validate the actual chosen deformation/export path.

## Choose the reference for the current gate

| Question | Read |
| --- | --- |
| New weapon port or step-by-step repair | [Weapon playbook](references/weapon-retargeting-playbook.md) |
| Source playback, pairing or missing layers | [Source adapters](references/source-adapters.md) |
| Coordinates, updated-parent locals, native binds | [Spaces](references/spaces-and-transforms.md) |
| Neto/matched-reference correspondence or inverse-LBS handoff | [Matched-pose calibration](references/matched-pose-calibration.md) |
| Finger shape, palm alignment, phase contact, nonstretch reach | [Contact and IK](references/contact-and-ik.md) and [finger checkpoint](../cyberpunk2077-modding/references/animation-retargeting/finger-checkpoint.md) |
| Normal/additive bases, export or native bytes | [Animation semantics](references/cyberpunk-animation-semantics.md), then [native readback](references/native-readback.md) |
| State selection, blends, masks, interruptions or preview/game disagreement | [Animation graphs](references/animation-graphs.md) |
| Specific native engine implementation question | [Technical hub](../cyberpunk2077-modding/references/animation-retargeting/index.md), then the relevant native chapter |
| BF6 source/assembly contracts | [BF6 workflow](references/bf6-workflow.md) |
| Ready or Not route | [HK416 workflow](references/ready-or-not-workflow.md); [historical RoN MP5](references/mp5-workflow.md) is a different artifact |
| Automated fixture, coverage, native batch/resume | [Agent tools](references/agent-tools.md) |
| Package acceptance or gameplay | [Runtime validation](references/runtime-validation.md) |

Load the selected references, not the whole library. Do not reconstruct the engine
instead of fixing a demonstrated Blender-visible defect.

## Mandatory Blender review before installation

Use the [full visual acceptance procedure](references/visual-acceptance.md) and
[final-native clipping audit](../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#final-readback-clipping-audit).
Inspect complete affected motion and transitions on the connected, deformed native
assembly, with first-person and complementary full/close views. Review both arms,
every digit/thumb, controls and mechanisms; endpoint/wrist checks cannot prove grip
continuity. Generated but unwatched renders and numeric checks are not visual approval.
Show smooth actual-motion previews and record the user's acceptance before installing
changed motion. Keep named accepted defects and missing coverage explicit.

Retain existing review and user acceptance for unchanged covered motion and unchanged
relevant rig, skin, assembly, source and evaluation inputs. Bind that reuse to the new
package through exact native/readback and extracted-resource checks. A record-order-only
repair with byte-identical decoded motion does not require re-authoring or redundant
preview approval. Refresh affected views when any relevant input changes. Gameplay
confirmation remains specific to the package actually tested.

## Mandatory source-versus-retarget comparison

For ports, follow the [source comparison procedure](references/visual-acceptance.md#mandatory-source-versus-retarget-comparison):
synchronized complete source/native motion, matched anatomical views and actual
contacts, plus before/after for repairs. Label missing source skin/runtime layers
and body differences. User acceptance can retain named limitations; it cannot create
unobserved source parity or a flawless clipping result.

## Learn from validation failures

Use the existing [failure ledger](references/failure-ledger.md): demonstrated cause,
why the old check missed it, smallest shared prevention, and a regression that rejects
the original failure while accepting a legitimate control. Retain the failed evidence.
After two failed corrections at the same gate, stop speculative correction and run a
discriminator separating at least two hypotheses before another edit.

For native record surgery, preservation is more than a multiset: validate dynamic
record ordering, exact protected channel sequences, counts/addresses, constants,
floats and metadata. The existing [native reader](references/native-readback.md)
checks supported compressed record order before producing preview data. Do not add
another writer or bypass a failed native gate because Blender looks correct.

## Gates

Source → target/rest/skin → mapping → one connected action → actual native readback
→ source/target visual review → extracted package → identified user gameplay.
[Pipeline](references/pipeline.md) defines the evidence vocabulary and schema.
An established route may batch compatible actions. A new route first needs its
reviewable vertical slice; a missing optional animator rig is not an automatic blocker.

## Bound the work

Start finger repairs with one reversible motion interval and review before propagation.
Preserve original source keys, anatomical Normal translations/scales/lengths and
unrelated motion. Derive destination locals parent-first. Re-encode additive offsets
against changed bases when necessary; preserving anatomy does not mean freezing the
old encoded additive translations. Check between keys and partial blend weights.

Respect the user's accepted release scope and deferred work. A rollback contains a
runtime regression; it does not replace an authorized request to repair the accepted
poses. Repair the demonstrated fault with the smallest change and revalidate the
actual package. Never treat successful import or a diagnostic label as deployment approval.

## Included checks and handoff

Use existing [contract and workflow tools](references/agent-tools.md); their structural
passes do not establish spatial fidelity or gameplay. Run relevant [evals](evals/README.md)
when updating this workflow. Keep exact paths, commands, hashes, observed results,
failed controls and next steps in the owning project's handoff. Keep private assets
and per-weapon calibration out of the distributable skill.
