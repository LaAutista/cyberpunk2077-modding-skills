# Tool selection

Use the simplest established tool that supplies the required evidence. These
decisions come from the [pinned MCP comparison](mcp-comparison.md), completed on
2026-10-23. It records measured benefits, reproduced failures and untested runtime
boundaries. Check the [environment guide](environment.md) and
[documentation topic map](topic-map.md) before adapting commands to another setup.

For an Edgemodders evaluation, read the [capability comparison](edgemodders-comparison.md):
version/schema caveats, diff blind spots, Fluorine limits and proposed material/import improvements.

## Adoption decisions

| Implementation | Keep | Selectively reuse and benefit | Defer |
| --- | --- | --- | --- |
| Y4rd13 WolvenKit MCP | An established, operation-specific native/Wine WolvenKit pipeline, guarded JSON conversion/diff and dedicated weapon verification. The originating workspace used custom Modwright and weapon adapters; they are not bundled here. | Compact schema-aware inventories, implemented in the independent jq helper below. They retain complete named clips/durations and explicit material references while reducing agent input; typed traversal catches the actual `.remt` omission found upstream. | The complete server. Its wrappers supplied no demonstrated speed or output-quality advantage over the existing CLI. Windows-shell assumptions, CLI arguments, stale outputs and summary omissions would require maintenance. The temporary Linux adapter was an experiment, not upstream Linux support. |
| Y4rd13 CET MCP | An existing bounded status/snapshot bridge, if available, plus direct log and profile inspection. Preserve boot/session/sequence/expiry checks and explicit expected-value assertions. | The idea of one fixed typed live TweakDB read, when a diagnosis needs an effective value after runtime patches. That capability was absent from the originating bridge's status/snapshot protocol. Engine behavior remains unverified. | The complete server, arbitrary evaluation, mutation helpers, observers and TCP/RedSocket. A second general mailbox did not improve the tested workflow; concurrency, timeout, serialization and false-success defects add work before live integration. |

The originating Modwright server, redscript bridge, native verification tools and
Lynx adapters are **not supplied by this repository**. Discover the user's existing
equivalents; do not invent an installation URL or claim their presence. If a needed
operation lacks a verified equivalent, state the gap and validate a scoped adapter
on preserved copies before relying on it.

## Route tasks by evidence needed

| Task | Preferred route | Acceptance boundary |
| --- | --- | --- |
| Extract, serialize, cook, export or pack | Version-checked WolvenKit CLI and existing operation-specific launcher | Require exit/log checks, fresh outputs and the appropriate native roundtrip; a successful command is insufficient. |
| Inventory animation clips and material references | Included read-only jq helper on fresh serialized copies | Complete supported fields, not animation playback or a resolved dependency graph. |
| Compare ordinary CR2W authoring changes | Established schema-aware diff, with its ignored fields inspected | The originating Modwright diff ignores `renderResourceBlob` and `parameters` subtrees; keep dedicated payload and parameter checks. |
| Fit meshes, adapt motion, inspect collisions or hand contact | [Weapon adaptation workflow](weapon-rigging-animation.md), Blender and native readback | Actually inspect complete applicable sequences and dense frames around fast motion; summaries and MCP calls cannot replace this. |
| Inspect current player/weapon/ammo state | Existing bounded bridge, if installed and accepted for the current game version | Fixture tests prove protocol behavior, not current native game callbacks. |
| Diagnose an effective TweakDB value absent from offline data | A scoped future typed-query extension | Deferred; requires protocol fixtures and independent live acceptance. |

## Corrected animation and material inventories

Use the [resource pipeline and maintained inventory recipe](resource-pipeline.md#corrected-animation-and-material-inventories)
for fresh serialization, jq summaries and their regression/evidence boundaries.

## Preserve weapon acceptance

Continue donor/replacement dimension, pivot, bone and weight inspection; recover
complete applicable weapon/player sequences; render and actually inspect
first-person and close-up views; check moving parts and hand contacts; justify
local fixes; reinspect regressions; inspect native exports and packaged payloads.
Neither MCP adds a rigging, rendering or collision engine. Keep automated, visual
and user gameplay evidence separate, including the clean Lynx laptop reload as
user-reported evidence for that tested package only.

## Smallest worthwhile future integration

When a concrete diagnosis needs a live value, extend an existing bounded bridge
with **one fixed typed TweakDB flat query** for an independently verified path. The
upstream [GetFlat handler](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L100-L114)
demonstrates the idea, not a verified drop-in implementation. Check installed API
signatures, version the actual host/companion protocol, and preserve explicit
missing/type errors, expiry and session checks. Do not send upstream JSON to an
unrelated binary mailbox or silently enable a disabled route.

Test success, missing/type errors and stale sessions with protocol fixtures first.
Then compare a user-controlled live query with an independent version-matched
expectation, repeat across save/load, and verify stale responses are rejected.
Record exact executable, dependency, profile and package identity. A TweakDB flat
is not final computed damage or visual proof. This extension remains unimplemented
and unverified; no extra server is required solely to add the query.

The immediate task enabled by this repository is to inventory a replacement's
copied native animations and explicit material references, then enter the existing
Blender fitting and inspection workflow with complete supported inputs.
