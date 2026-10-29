---
name: cyberpunk2077-animation-retargeting
description: Retarget external or Cyberpunk weapon/player animation onto a verified Cyberpunk 2077 skeleton. Use for source decoding, skeleton mapping, coordinate conversion, FK/IK and hand contact, additive semantics, .anims authoring and native readback. Excludes ordinary mesh fitting, textures, audio and gameplay scripting.
metadata:
  version: "1.3.0"
---

# Cyberpunk 2077 animation retargeting

Produce the smallest native animation artifact with independently checked source,
target reconstruction and serialized output. This is an execution contract plus
bounded validators; it does not supply a universal retargeter or game assets.

## Enter the project

Read the current project STATUS/handoff and preserve the known-good artifact with
its hash and evidence scope. If no runtime baseline exists, record that explicitly.
Choose exactly one blocking gate, one fixture and one next discriminating test.
Keep raw source, evaluated source, preview, final native and package identities
separate. Preserve unrelated tracks, dirty work, user settings and failed reports.

Use [pipeline and receipts](references/pipeline.md) for the status format and
adapter boundaries. Evidence statuses are IMPLEMENTED, CHECKED,
VISUALLY_REVIEWED, USER_RUNTIME_VERIFIED, FAILED, OPEN and HYPOTHESIS. Each describes
one gate and identified artifact; offline success cannot promote visual/runtime.
Historical receipts retain their original terms and limitations.

## Gates

| Gate | Required evidence before advancing |
| --- | --- |
| A — source | Build/decoder and source hashes; actual mesh/skeleton/clip pairing, hierarchy, key/sample times, local T/Q/S, animation type/base, events/curves and ownership. No filename-inferred semantics. Read [source adapters](references/source-adapters.md). |
| B — target | Exact .rig/.anims hashes, native reference locals and hierarchy, compatible container, required controls/helpers, skin/deformation ownership when relevant. A custom animator rig is optional. |
| C — coordinates/mapping | Declared vector/matrix/quaternion conventions, units and both basis transforms; explicit bone correspondence and justified unmapped targets. Check reference-pose reconstruction before motion. Read [spaces](references/spaces-and-transforms.md). |
| D — one clip | Preserve target anatomical translations/scales/lengths and unrelated tracks; solve rotations, assembly placement, nonstretch reach, phase-specific contact and required controls. Check target deformation and original unclamped contact residuals. Read [contact](references/contact-and-ik.md). |
| E — native | Author into a copy of a compatible container with the matching rig. Independently decode stored bytes; compare keys/times, untouched clips, events/floats, scale and additive semantics. Read [semantics](references/cyberpunk-animation-semantics.md) and [native checks](references/native-readback.md). |
| F — package | Isolate exactly the tested clip; extract and compare shipped resources. Record source/rig/container/archive hashes, game version, prerequisites, conflicting packages and visual status. A diagnostic package is not an accepted beta. |
| G — runtime | User confirms the identified package, effective profile and affected variants at beginning/middle/end, transitions, contact, relevant IK and interruptions. Record failures separately. Read [runtime validation](references/runtime-validation.md). |

Read only references needed for the current gate. For general tools/resource work
use the sibling [modding skill](../cyberpunk2077-modding/SKILL.md); for actual
motion/deformation review use [weapon inspection](../weapon-animation-inspection/SKILL.md).
The existing [technical hub](../cyberpunk2077-modding/references/animation-retargeting/index.md)
retains detailed, source-linked chapters and dated case evidence.

For Ready or Not ports, read the [proven HK416 workflow](references/ready-or-not-workflow.md)
before choosing an adapter. It covers source-reference versus replacement geometry,
partial-weight locomotion contact, native key clocks and camera comfort, with the
identified user-tested baseline and the limits of transferring it to another weapon.
Before selecting a locomotion carrier or adding camera compensation, inspect the
composing rig mask and downstream control constraints. A local additive/contact
pass cannot establish that those tracks survive the actual body composition.

## Bound the work

Once one source clip decodes, mapping is established and the target container is
writable, the next deliverable is the isolated vertical slice. Resolve its named
blocking gate before adding polish or processing more clips. A diagnostic slice
may disclose known visual defects to test runtime consumption; do not call it
accepted or replace a baseline. Before accepted-beta promotion or full-set work,
require all applicable gates, including full-motion Blender review and G, to pass.

After two failed corrections at the same gate, stop implementation and write
FAILURE.md using the [failure ledger](references/failure-ledger.md). Separate at
least two hypotheses with a discriminator and obtain its result before another
correction. Do not stack guessed offsets, stretch bones, reuse another weapon's
calibration without proof, or regenerate equivalent previews. Updated destination
parents must precede child reconstruction; synchronize controls and export fresh
final arrays. Never mix native control rests with per-mesh inverse binds.

## Included checks and handoff

For repeated native conversion/checks, archive ownership lookup and bounded graph
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
