# Tool selection

Use the simplest established tool that supplies the required evidence. These
decisions come from the [pinned MCP comparison](mcp-comparison.md), completed on
2026-10-23. It records measured benefits, reproduced failures and untested runtime
boundaries. Check the [environment guide](environment.md) and
[documentation topic map](topic-map.md) before adapting commands to another setup.

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
| Compare ordinary CR2W authoring changes | Established schema-aware diff, with its ignored fields inspected | The originating Modwright diff ignores some render buffers; keep dedicated mesh and payload checks. |
| Fit meshes, adapt motion, inspect collisions or hand contact | [Weapon adaptation workflow](weapon-rigging-animation.md), Blender and native readback | Actually inspect complete applicable sequences and dense frames around fast motion; summaries and MCP calls cannot replace this. |
| Inspect current player/weapon/ammo state | Existing bounded bridge, if installed and accepted for the current game version | Fixture tests prove protocol behavior, not current native game callbacks. |
| Diagnose an effective TweakDB value absent from offline data | A scoped future typed-query extension | Deferred; requires protocol fixtures and independent live acceptance. |

## Corrected animation and material inventories

The maintained summaries belong in
[summarize_weapon_json.jq](../scripts/summarize_weapon_json.jq), with
[test_summarize_weapon_json.sh](../scripts/test_summarize_weapon_json.sh) beside it.
They are separate from Blender adapters and MCP servers so inspections do not
silently lose fields when a wrapper changes. The helper reads JSON and does not
convert or modify assets.

From the repository root, configure `WK_CLI` as the executable or established
launcher for **this operation**. Assign `asset_copy` to a preserved native resource,
`fresh_output` to a new empty directory, and `animation_json` or `mesh_json` to the
output actually produced there. Serialize each resource separately, stop on a
nonzero result, and inspect the converter log and output provenance before querying.
Do not continue with a stale sidecar after conversion fails.

```bash
SKILL_DIR="$PWD/skills/cyberpunk2077-modding"
: "${WK_CLI:?Set WK_CLI to the verified serializer executable or launcher}"
: "${asset_copy:?Set asset_copy to a preserved native resource}"
: "${fresh_output:?Set fresh_output to a new empty output directory}"
"$WK_CLI" convert serialize "$asset_copy" -o "$fresh_output"
```

Only after successful conversion and inspecting the fresh outputs, run:

```bash
jq -e -f "$SKILL_DIR/scripts/summarize_weapon_json.jq" "$animation_json"
jq -e -f "$SKILL_DIR/scripts/summarize_weapon_json.jq" "$mesh_json"
```

The CLI syntax and helper were tested locally with WolvenKit 9.0.1 / JSON 0.0.9.
Do not assume all WolvenKit operations run natively on Linux: the established
pipeline used native and Wine routes for different operations. A Wine launcher
must supply its own correctly mapped paths and environment; the example is not a
portable Wine implementation.

For `animAnimSet`, the helper follows `animations[].Data.animation.Data`, preserving
order, duplicate clip names and every duration. For `CMesh`, it preserves material
names, indexes and local-instance flags, and traverses every explicit typed
`DepotPath` without suffix, depth or result limits. It separately reports unique
string paths, total occurrences, empty paths and unresolved non-string storage.
Unsupported roots or missing required fields fail before producing a summary.
Adapt a changed serializer schema explicitly and add a regression; unknown is not
zero, empty or clean.

This material inventory does **not** resolve hashes, dynamic paths, transitive
dependencies, textures or shaders. An animation list does not recover player arms,
animation graphs or runtime IK. Retain original JSON and hashes for those checks.

```bash
bash -n "$SKILL_DIR/scripts/test_summarize_weapon_json.sh"
bash "$SKILL_DIR/scripts/test_summarize_weapon_json.sh"
```

The portable synthetic suite covers wrapped fields, duplicate names, 121 clips,
25-level references, unknown suffixes, `.remt`, explicit unresolved hashes and nine
malformed inputs that must fail without summary output. Keep these regressions
with every helper change.

The original private Lynx-copy run additionally compared every one of 19 clip
name/duration pairs and all 24 explicit paths against retained golden results, and
retained all 21 material entries by count. Those fixtures and game-derived files
are not distributed here. The test script's optional two-directory mode is
specific to that preserved fixture layout, not a generic acceptance threshold.
Public synthetic checks do not independently reproduce that private native-asset
study; test your own preserved copies before claiming another schema is supported.

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
