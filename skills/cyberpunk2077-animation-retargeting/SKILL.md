---
name: cyberpunk2077-animation-retargeting
description: Retarget external or Cyberpunk animation onto a verified Cyberpunk 2077 skeleton and diagnose animgraph blending, masks and state transitions. Use for source decoding, skeleton mapping, coordinate conversion, FK/IK and hand contact, additive semantics, .anims authoring and native readback. Excludes ordinary mesh fitting, textures, audio and gameplay scripting.
metadata:
  version: "1.8.28"
---

# Cyberpunk 2077 animation retargeting

Produce the smallest native animation artifact with independently checked source,
target reconstruction and serialized output. This is an execution contract plus
bounded validators; it does not supply a universal retargeter or game assets.

## Enter the project

Read the current project STATUS/handoff and preserve the known-good artifact with
its hash and evidence scope. If no runtime baseline exists, record that explicitly.
For an unknown or failing route, choose one blocking gate, fixture and next
discriminating test. For an established route, batch compatible actions using
the measured contract and hash-verified evidence.
Keep raw source, evaluated source, preview, final native and package identities
separate. Preserve unrelated tracks, dirty work, user settings and failed reports.

Use [pipeline and receipts](references/pipeline.md) for the status format and
adapter boundaries. Evidence statuses are IMPLEMENTED, CHECKED,
VISUALLY_REVIEWED, USER_RUNTIME_VERIFIED, FAILED, OPEN and HYPOTHESIS. Each describes
one gate and identified artifact; offline success cannot promote visual/runtime.
Historical receipts retain their original terms and limitations.

## Mandatory Blender review before installation

Inspect **every animation included in the candidate** in Blender, through its
complete timeline and relevant starts/stops, loops, blends and state transitions.
Review the connected target assembly: skinned arms/body, weapon, magazine, bolt
and other moving parts together. Use the exact candidate's native readback and
verified assembly inputs; an older mechanism bank or a preview-only placement
offset cannot stand in for the shipped data.

Run the required [final-readback clipping audit](../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#final-readback-clipping-audit)
on the assembled, deformed candidate before installation. Check every affected
frame and relevant alias/body variant; bind findings to final resource hashes.
Also verify that [previously approved clips survived the merge](references/native-readback.md#cumulative-candidate-preservation). A draft audit or preservation against a
stale import baseline cannot clear the final build.

Actually inspect continuous playback at normal speed, plus slow playback/scrubbing
of fast contacts. Use first-person and complementary side/close views and the
[full-motion review checklist](../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#mandatory-blender-visual-acceptance).
For skin creases, also verify the renderer's normal source and evaluated corner
normals at a fixed pose; positions/weights passing does not prove that authored
normals survived import. Use the existing [skin/normal boundary check](../cyberpunk2077-modding/references/animation-retargeting/native-deformation.md#next-diagnostic-when-skin-still-fails).
Record clip, variant, candidate hash, complete time range, views, observed defects
and evidence. Unwatched renders, a few poses, contact sheets, numeric checks and
successful native exports do not pass this gate. Missing coverage stays OPEN;
visible hand separation, broken bolt/magazine motion, clipping or deformation
stays FAILED regardless of other passed checks.

**Show the user smooth video previews and obtain their explicit acceptance of the
identified candidate before installing it.** Render actual motion at least 30 fps
(or the higher source cadence where fast motion requires it); do not interpolate
a sparse slideshow and call that a full review. Show complete affected actions
and transitions, with first-person and useful side/close views. Record the user's
answer against the preview and candidate identities. Review a batch together;
do not require a separate conversation per clip. Changed motion requires an updated
preview and acceptance. A diagnostic label does not waive this installation gate.

Fix Blender-visible failures offline before requesting game tests. Runtime testing
addresses remaining integration questions; it must not replace the visual homework.
State preview limitations honestly, but never use absent runtime parity to dismiss
a defect already visible in Blender. Do not expand engine reconstruction to avoid
correcting a demonstrated motion defect.

## Mandatory source-versus-retarget comparison

For every port, show the original source animation and the exact native target
readback side by side, synchronized through every retargeted clip's full timeline.
Use normal-speed playback (at least 30 fps, or source cadence for fast contacts),
slow review, matched anatomical views and the connected target weapon assembly.
A target-only preview cannot clear this gate. Include before/after when repairing
an existing port; record source, target and preview hashes and the user's review.

Inspect both hands digit by digit, including thumb, open/released poses, closed
grips and regrip, plus wrists, arms, mechanisms and weapon contact. Compare actual
anatomical joint directions/bends in measured palm frames, not similarly named
bone Euler angles. Preserve source articulation and timing; explain deliberate
replacement-model grip offsets. A plausible-looking target or a numerical pass
cannot substitute for the comparison. If the source is itself defective, report
that instead of silently correcting or attributing it to the game runtime.

Use verified source skin when available. Label joint-only proxies, inferred tip
axes, missing source runtime layers and target body differences explicitly; they
do not establish source skin/contact equivalence. Missing comparison coverage
stays OPEN and visible mismatches stay FAILED. Show the user the limited evidence
before any approval request; never hide its limitations in a receipt alone.
Start a finger repair with one reversible clip and obtain its review before
propagating the change. Preserve local translations, scales, lengths, wrist/body
motion, other digits and unrelated clips. See [contact](references/contact-and-ik.md)
for the reference-pose trap and the existing visual gate for installation approval.

## Learn from validation failures

When a significant defect or missed inspection is found, record both its technical
cause and why the previous checks let it through. In the owning project's existing
FAILURE/status record, link three outcomes: root cause, the smallest reusable
prevention change in this skill/workflow, and an executed regression or a precise
unrun check. Preserve rejected artifacts and failed subchecks. Update the relevant
reference/helper and existing evals; do not create a second validation system or
turn a case-specific offset/tolerance into a general rule.

Before batching deformation work, complete the existing
[finger/skin checkpoint](../cyberpunk2077-modding/references/animation-retargeting/finger-checkpoint.md)
with matched opaque and wire surfaces, actual joints/bone orientations and skin
influences at rest and representative contact/release/extreme keys. Inspect digits,
thumb, wrist and arm together. Bone-direction agreement does not certify skin
shape/contact; a repair that improves one measurement but damages curl, twist,
wrist pose or reach remains FAILED. Reuse unchanged evidence; refresh affected
views and native readback after a real change, then review complete motion.

Inventory source animated local translations/scales before assuming a rotational
adapter can represent the action. The existing
[source-motion check](references/pipeline.md#source-motion-inventory) exposes these
channels; it cannot authorize copying them onto native anatomical joints. Unhandled
anchor travel needs a measured adaptation or a named OPEN limitation before
expansion. See the [RPG7 validation lesson](references/bf6-workflow.md#rpg7-validation-failure).

For measured reference-pose matching, use [matched-pose calibration](references/matched-pose-calibration.md). It separates saved world-orientation correspondence from optional inverse-LBS replacement-mesh work; preserve native anatomy, per-mesh binds and the existing acceptance gates.

## Gates

| Gate | Required evidence before advancing |
| --- | --- |
| A — source | Build/decoder and source hashes; actual mesh/skeleton/clip pairing, hierarchy, key/sample times, local T/Q/S, animation type/base, events/curves and ownership. No filename-inferred semantics. Read [source adapters](references/source-adapters.md). |
| B — target | Exact .rig/.anims hashes, native reference locals and hierarchy, compatible container, required controls/helpers, skin/deformation ownership when relevant. A custom animator rig is optional. |
| C — coordinates/mapping | Declared vector/matrix/quaternion conventions, units and both basis transforms; explicit bone correspondence and justified unmapped targets. Check reference-pose reconstruction before motion. Read [spaces](references/spaces-and-transforms.md). |
| D — one clip | Preserve target anatomical translations/scales/lengths and unrelated tracks; solve rotations, assembly placement, nonstretch reach, phase-specific contact and required controls. Check target deformation and original unclamped contact residuals. Read [contact](references/contact-and-ik.md). |
| E — native | Author into a copy of a compatible container with the matching rig. Independently decode stored bytes; compare keys/times, untouched clips, events/floats, scale and additive semantics. Read [semantics](references/cyberpunk-animation-semantics.md) and [native checks](references/native-readback.md). |
| E2 — source/target review | Full synchronized source/native side-by-side; repair before/after; complete finger, mechanism and contact review; identified user acceptance and explicit missing-source limitations. Target-only playback does not pass. |
| F — package | Isolate the initial diagnostic clip or explicitly checked action batch; extract and compare shipped resources. Record source/rig/container/archive hashes, game version, prerequisites, conflicting packages and visual status. Offline packaging does not clear the mandatory Blender and user-preview installation gate. |
| G — runtime | User confirms the identified package, effective profile and affected variants at beginning/middle/end, transitions, contact, relevant IK and interruptions. Record failures separately. Read [runtime validation](references/runtime-validation.md). |

Read only references needed for the current gate. For general tools/resource work
use the sibling [modding skill](../cyberpunk2077-modding/SKILL.md); for actual
motion/deformation review use [weapon inspection](../weapon-animation-inspection/SKILL.md).
For graph-only defects or motion that changes during composition, use
[animation graphs, blending and transitions](references/animation-graphs.md).
For the inspected Cyberpunk 2.5 implementation, use the
[native blend/state semantics](references/native-graph-semantics.md): transform
order, quaternion interpolation, sparse tracks, weight history, priority and curves,
with focused chapters for feature-driven duration, clock/inertialization,
synchronization/events, shared-pose publication and concrete mesh skinning preparation. Use
[measured normalization limits](references/native-normalization.md) when judging
float32 parity, zero/overflow behavior or a simplified quaternion model. Use
[measured transform numerics](references/native-transform-numerics.md) for exact
composition order, interpolation/mask/weight boundaries, inverse-Euler pole
snapping and caller-specific
writes; keep its finite host corpus separate from selected game inputs. Use
[named blend operators](references/native-blend-operators.md) for Blend2,
BlendMultiple, Override or DynamicMask selection, missing inputs and command
differences; use [motion adjustment](references/native-motion-adjuster.md) for
the two distinct auxiliary solvers and identified extraction sampling. Use
[contributor and motion queries](references/native-motion-queries.md) to distinguish
ordinary weighted collection from optional interval/full-clip results, their
time rules, write footprints, event ownership and locomotion lifecycle/planner
consumers. Check the caller's later overwrites and cached inputs before treating
a helper result or outer argument as the retained playback state. For query-refresh
timing, distinguish registered stages from completion of their nested jobs. Consult the sibling
[WolvenKit Docs skill](../wolvenkit-docs/SKILL.md) for cached primary documentation;
where it does not specify a runtime contract, follow the exact implementation
and validate a discriminator instead of inventing semantics from field names.
Trace the selected state and its changing inputs through masks and downstream
constraints; clip playback, a declared transition and final evaluated pose are
separate evidence. Reuse the bounded graph/mask inspector before adding tooling.
For BF6 and replacement-model ports, start with the
[BF6 findings and platform boundary](references/bf6-workflow.md): measured interaction
frames, native component bindings, arm controls, finger calibration and release coverage.
The historical [RoN MP5 1.0 workflow](references/mp5-workflow.md) retains useful
batching and recipe guidance; its acceptance does not certify the later BF6 MP5.
The existing [technical hub](../cyberpunk2077-modding/references/animation-retargeting/index.md)
retains detailed, source-linked chapters and dated case evidence.

For Ready or Not ports, read the [proven HK416 workflow](references/ready-or-not-workflow.md)
before choosing an adapter. It covers source-reference versus replacement geometry,
partial-weight locomotion contact, native key clocks and camera comfort, with the
identified user-tested baseline and the limits of transferring it to another weapon.
Before selecting a locomotion carrier or adding camera compensation, inspect the
composing rig mask and downstream control constraints. A local additive/contact
pass cannot establish that those tracks survive the actual body composition.
Attaching motion to the pelvis is a hypothesis until that carrier survives the
selected mask and keeps hands, weapon, camera and player displacement correct.

## Bound the work

Once one source clip decodes, mapping is established and the target container is
writable for a new route, the next deliverable is the isolated vertical slice. Resolve its named
blocking gate before adding polish or processing more clips. A diagnostic slice
may be prepared offline with disclosed defects; installing it still requires the
mandatory preview review. Do not call it accepted or replace a baseline.
Before accepted-beta promotion or full-set work,
require applicable native/package, full-motion review and runtime evidence. Once
the route is established, batch compatible clips and review changed motion and
state boundaries together. Do not impose a stop-and-ask cycle per clip. Explicit
user acceptance defines release scope: record known defects/fallbacks and untested
combinations separately, without inventing evidence or requiring deferred work.

After two failed corrections at the same gate, stop implementation and write
FAILURE.md using the [failure ledger](references/failure-ledger.md). Separate at
least two hypotheses with a discriminator and obtain its result before another
correction. Do not stack guessed offsets, stretch bones, reuse another weapon's
calibration without proof, or regenerate equivalent previews. Updated destination
parents must precede child reconstruction; synchronize controls and export fresh
final arrays. Never mix native control rests with per-mesh inverse binds.

## Included checks and handoff

For source inventory, native batches/resume, clip coverage, archive lookup and bounded graph
and rig-mask inspection, use the [agent workflow tools](references/agent-tools.md). Prefer the
resumable native runner over copying another per-weapon command script; its checked
receipt still leaves visual and runtime gates open.

From this skill directory, using Python 3.11+'s standard library:

```sh
python3 -B scripts/retarget_contract.py validate-fixture /path/to/fixture.json
python3 -B scripts/retarget_contract.py verify-mapping /path/to/fixture.json
python3 -B scripts/retarget_contract.py summarize-receipt /path/to/STATUS.json
```

These check structural contracts, hashes and evidence bookkeeping. They cannot
prove a decoder's interpretation, correct transforms, actual review or gameplay.
Use the existing native helpers rather than another wrapper/serializer. See
[evals](evals/README.md) for workflow and trigger tests.

Report baseline, changed files, commands, passed/failed/unavailable checks,
visual/gameplay status, blockers and one next highest-information test. State
exact manual steps and expected observations when the required environment is
unavailable. Installation/discovery does not prove that native tools execute.
