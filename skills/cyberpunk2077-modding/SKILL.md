---
name: cyberpunk2077-modding
description: Build and inspect Cyberpunk 2077 resources, scripts, tweaks and packages. Use for tool setup, extraction, import/export and deployment integration.
---

# Cyberpunk 2077 modding

For setup or missing tools, start with the agent-neutral [preflight and setup](references/setup-preflight.md) using the packaged `scripts/setup/*.mjs` entry points (or repository `setup/*.mjs`). Preflight is read-only; follow the task-specific prerequisites and report unknown/manual gates before building.

Inspect the current project's instructions, checkpoint, inputs and installed
game/framework/tool versions. Preserve the user's stack and current restrictions,
including CET preferences; a documented capability does not authorize adding a
dependency or changing the architecture. Use the existing manager/profile workflow
and session authorization for deployment or game launch.

## Choose the task

Load the matching reference, then only the sections or source pages it needs.
Combine routes when the task actually crosses layers.

| Task | Start here |
| --- | --- |
| WolvenKit instructions, options, UI/CLI, extraction or import/export documentation | [WolvenKit Docs](../wolvenkit-docs/SKILL.md): read the relevant locally cached official pages and version notes before choosing commands or options. |
| Implement scripts, tweaks, UI or native behavior | [Development playbook](references/development-playbook.md); use the [topic map](references/topic-map.md) to find the actual API/format source. Read [corrections](references/documentation-corrections.md) when adapting examples. |
| Extract, import, cook, pack, inventory clips/materials or compare CR2W | [Resource pipeline](references/resource-pipeline.md). Keep the established native/Wine route, compatible donor containers, fresh outputs and native readback; check ignored fields before trusting a diff. |
| Fit or port a weapon; inspect rigs, mechanisms, collision or hand contact | [Weapon workflow](references/weapon-rigging-animation.md): establish source pairing and the behavior/acceptance ledger before fitting. Use the sibling [inspection skill](../weapon-animation-inspection/SKILL.md) for playback/render/contact inspection. |
| Retarget any animation; diagnose source playback, binds, fingers, proportions or native deformation | [Retargeting skill](../cyberpunk2077-animation-retargeting/SKILL.md) for one-gate execution and bounded repair loops; [technical hub](references/animation-retargeting/index.md), then the chapter for the failing stage. Complete the finger checkpoint before motion transfer where hands/digits are involved. |
| Diagnose animgraph blending, masks, state transitions or composed-pose mismatches | [Graph investigation](../cyberpunk2077-animation-retargeting/references/animation-graphs.md): trace the component, state, clocks, pose/value links and downstream consumers against pinned resources. |
| Inspect runtime state or evaluate a bridge/MCP/tool, including Edgemodders | [Tool selection](references/tool-selection.md). Discover existing bounded capabilities; distinguish source claims, protocol fixtures and live engine results. |
| Resolve paths, prerequisites or Linux/Wine setup | [Environment](references/environment.md). Locate the actual tools and profile; historical paths and downloaded packages do not establish working installations. |

For implementation, verify real declarations and usage before calling or hooking
an API; check types, ownership, lifecycle and session transitions. Use supported
script/data layers where they satisfy the feature. Keep evidence and diagnostic
assets separate from shipping resources.

For complete RoN ports on an established route, use the sibling
[MP5 1.0 workflow](../cyberpunk2077-animation-retargeting/references/mp5-workflow.md)
for the private recipe, reusable tools, attachments, audio and release boundaries.
For BF6 ports, use the [current findings and platform boundary](../cyberpunk2077-animation-retargeting/references/bf6-workflow.md).
Keep historical RoN acceptance separate from BF6 candidates. First installations
need firing, dry-fire, reload and applicable mechanism/equip/holster sounds;
record source provenance and identify donor placeholders. A visible attachment
slot does not prove compatibility or correct optic/muzzle placement.

## Animation acceptance

The [retargeting skill](../cyberpunk2077-animation-retargeting/SKILL.md) owns motion
repair and its visual/native/runtime acceptance rules. Use its
[visual procedure](../cyberpunk2077-animation-retargeting/references/visual-acceptance.md)
for changed animation and its evidence-reuse rule for unchanged accepted motion.
This applies to bodies, creatures, faces, props, cameras and weapon mechanisms;
packing success does not establish visual or gameplay success. Keep named user-accepted
exceptions explicit. For actual skin/contact inspection use the
[weapon inspection skill](../weapon-animation-inspection/SKILL.md) and the relevant
[QA reference](references/animation-retargeting/qa-debugging.md).

A custom animator/control rig is optional. Preserve the native skeleton/rest/bind
and validated deformation/export contract for the chosen route; see
[bind and architecture](references/animation-retargeting/spaces-bind.md#native-skeleton-versus-animator-controls).

## Evidence and handoff

Retain **PASS / FAIL / UNVERIFIED / BLOCKED** in existing and non-retarget ledgers;
use the [gate-specific vocabulary](../cyberpunk2077-animation-retargeting/references/pipeline.md)
for new retarget receipts. Record versions,
input/output identities, inspected times/views, commands and remaining gaps.
Source inspection, retained receipts, newly run checks, visual review and gameplay
prove different things; a pass for one build or sample does not cover every asset.
Use the [evidence register](references/animation-retargeting/evidence-register.md)
for dated case receipts and ownership context, then check the owning project's
current checkpoint. Preserve failed reports and valuable references when updating
knowledge; add source-linked discoveries at the relevant branch, not case history here.

For a significant retargeting mistake or missed inspection, apply the existing
[validation learning rule](../cyberpunk2077-animation-retargeting/SKILL.md#learn-from-validation-failures):
record cause and missed detection, update the relevant shared prevention, and run
a regression. Deformation acceptance requires matched opaque/wire skin plus
joint/weight/orientation checks of the connected fingers, thumb, wrist and arm;
no numeric direction/contact result substitutes for those views and full motion.
