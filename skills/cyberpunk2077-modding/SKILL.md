---
name: cyberpunk2077-modding
description: Build, modify and package Cyberpunk 2077 mods using version-matched documentation, WolvenKit, redscript, CET and native tools. Use for mod implementation, weapon rigging and animation adaptation, resource inspection and evidence-based MCP tool selection.
---

# Cyberpunk 2077 modding

For setup or missing tools, start with the agent-neutral [preflight and setup](references/setup-preflight.md) using the packaged `scripts/setup/*.mjs` entry points (or repository `setup/*.mjs`). Preflight is read-only; follow the task-specific prerequisites and report unknown/manual gates before building.

Inspect the user's current project and installed toolchain before implementing a
change. Read the [development playbook](references/development-playbook.md), relevant
[topic sources](references/topic-map.md) and [documented corrections](references/documentation-corrections.md).
Use [environment setup](references/environment.md) for configurable paths; no private
reference library or preinstalled bridge is assumed.

## Implementation decisions

- Establish installed game/framework versions and resource identities. Match SDK
  layouts and addresses to the executable; dated snapshots are not compatibility proof.
- Select the layer that implements the feature: TweakXL for data, redscript for
  scripted behavior, CET for Lua tools/overlays, WolvenKit/ArchiveXL for resources,
  RED4ext when supported script APIs cannot provide required native behavior.
- Before calling/hooking an API, find a real declaration and usage in version-matched
  scripts, SDK or framework source. Verify signature, ownership and lifecycle.
- Plan attach/detach, callbacks, session transitions, delayed work and persistence.
  Do not retain game objects in long-lived services without a justified lifetime.
- Preserve the user's project, manager, profiles, settings and working assets.
  Stage reversible changes and keep evidence separate from shipping resources.
  Installation, publication and game launch require applicable user authorization.
- Define success at the changed layer. Test relevant failure cases and regressions;
  distinguish implemented, automatically checked, visually inspected and gameplay-tested.
  A compiler, render job or archive build proves only the operation it exercised.

## Route the task

| Task | Preferred route |
| --- | --- |
| Extract, convert, import, cook or pack | The project's established native/Wine WolvenKit pipeline with donor containers and native readback. |
| Inventory clips/material references | [Read-only jq summaries and regression checks](references/tool-selection.md), on fresh serialized copies. |
| Ordinary CR2W authoring differences | A schema-aware diff if available; ignored render buffers require dedicated geometry/payload checks. |
| Fit rigs, adapt animation, inspect collision/contact | [Reusable weapon workflow](references/weapon-rigging-animation.md) and [inspection skill](../weapon-animation-inspection/SKILL.md). |
| Port an Unreal weapon or first-person reload | [Source-to-native port workflow](references/ron-port-workflow.md), including extraction, graph-aware adaptation, preview and export gates. |
| Recover source audio/state coverage or evaluate Scenario Blender helpers | [Beta source/audio findings](references/ron-beta-source-audio.md), with standalone AudioXL integration and separate installation, diagnostic and gameplay evidence. |
| Compare Fallout/CAT or Scenario rigging/export advice with Cyberpunk | [Versioned comparison and copied-asset tests](references/fo4-scenario-comparison.md). Use transferable diagnostics; retain Cyberpunk hierarchy, weights, timing and native export gates. |
| Runtime state inspection | An existing bounded, version-matched bridge if available; prove engine calls separately from offline protocol tests. |
| Evaluate another MCP server | [Tool selection](references/tool-selection.md) and [pinned implementation comparison](references/mcp-comparison.md). |

Neither compared MCP replaces Blender, native rig recovery, collision probes,
actual rendered-frame inspection or export validation. Reuse demonstrated additions
without assuming a second server improves a working CLI or bridge.

## Weapon and evidence boundaries

Compare donor/replacement dimensions, pivots, bones, weights and animation dependencies
before fitting. Similar weapon types do not establish compatibility. Recover weapon
and player motion; inspect complete affected draw/fire/reload variants from first-person
and close-up views, with dense checks around fast motion. Justify local corrections,
recheck neighbors/contact, then inspect the native export and packaged result.

The [Lynx case](../weapon-animation-inspection/references/lynx-case-study.md) supplies
a verified local example with explicit sample/view limits. Its mappings, offsets
and private adapters are not a universal weapon converter. Label unavailable motion
and approximations. Report unresolved defects with location/frame/time, evidence,
attempted fixes, tradeoffs and the specific missing information or decision.

Keep source-linked discoveries in the project's own notes. Do not describe fetched
documentation as reviewed, an offline fixture as runtime proof, or a user's tested
reload as proof of every animation, package or platform.

The [HK416 case and open issues](references/ron-hk416-case-study.md) distinguish
the rejected donor-derived package, the clean rebuild's offline checks, and the
user's later confirmation that the reload plays. Thumb/contact, optic, texture
and sound issues remain open; preserve them when continuing on another machine.
