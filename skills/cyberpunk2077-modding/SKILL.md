---
name: cyberpunk2077-modding
description: Implement and inspect Cyberpunk 2077 mods, resources, weapon ports and animation retargets using version-matched WolvenKit, redscript, ArchiveXL, TweakXL and native APIs. Use for mod development and tool evaluation; distinguish offline checks, visual acceptance and gameplay evidence.
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
| Implement scripts, tweaks, UI or native behavior | [Development playbook](references/development-playbook.md); use the [topic map](references/topic-map.md) to find the actual API/format source. Read [corrections](references/documentation-corrections.md) when adapting examples. |
| Extract, import, cook, pack, inventory clips/materials or compare CR2W | [Resource pipeline](references/resource-pipeline.md). Keep the established native/Wine route, compatible donor containers, fresh outputs and native readback; check ignored fields before trusting a diff. |
| Fit or port a weapon; inspect rigs, mechanisms, collision or hand contact | [Weapon workflow](references/weapon-rigging-animation.md): establish source pairing and the behavior/acceptance ledger before fitting. Use the sibling [inspection skill](../weapon-animation-inspection/SKILL.md) for playback/render/contact inspection. |
| Retarget any animation; diagnose source playback, binds, fingers, proportions or native deformation | [Retargeting skill](../cyberpunk2077-animation-retargeting/SKILL.md) for one-gate execution and bounded repair loops; [technical hub](references/animation-retargeting/index.md), then the chapter for the failing stage. Complete the finger checkpoint before motion transfer where hands/digits are involved. |
| Inspect runtime state or evaluate a bridge/MCP/tool, including Edgemodders | [Tool selection](references/tool-selection.md). Discover existing bounded capabilities; distinguish source claims, protocol fixtures and live engine results. |
| Resolve paths, prerequisites or Linux/Wine setup | [Environment](references/environment.md). Locate the actual tools and profile; historical paths and downloaded packages do not establish working installations. |

For implementation, verify real declarations and usage before calling or hooking
an API; check types, ownership, lifecycle and session transitions. Use supported
script/data layers where they satisfy the feature. Keep evidence and diagnostic
assets separate from shipping resources.

## Animation acceptance

**All animations** require the [Blender visual review and receipt](references/animation-retargeting/qa-debugging.md#mandatory-blender-visual-acceptance)
before accepted-beta promotion: matched source versus converted
target through the full timeline and important transitions, with full 360° coverage,
above/below/obscured areas and relevant close-ups. This covers bodies, faces,
creatures, props, interactions, cameras and mechanisms. Inspect deformation,
jitter/popping, stretch/twist, clipping, sliding/contact loss and unnatural motion;
visible defects fail and require correction and renewed review. Every digit and
thumb, wrist/palm, arm and moving weapon contact must be accounted for when present.
Stills, numeric checks and export success do not replace actual motion review.
Diagnostic exports and isolated single-clip test packages are allowed under the
[vertical-slice contract](../cyberpunk2077-animation-retargeting/references/runtime-validation.md),
with visual failures/gaps disclosed. They are not accepted betas; native/package
and runtime acceptance remain separate.

A custom animator/control rig is **optional**. Direct raw/native-skeleton retargeting
is valid; validate the selected path's rest/binds, limb lengths, skin, required
helpers and exporter. Use justified FK rotations and nonstretch IK/contact
corrections. An unfinished control rig blocks an independent route only when an
identified shared native component actually fails that route. See the
[bind and architecture contract](references/animation-retargeting/spaces-bind.md#native-skeleton-versus-animator-controls).

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
