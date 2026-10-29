# Resource pipeline and compact inventories

Use for extraction, serialization, import/cook, packing and CR2W inspection.
Keep the project's operation-specific native/Wine WolvenKit launcher; read the
[environment guide](environment.md) only when paths, prerequisites or platform
behavior are unclear. Version-match the game, codec and resource type. Compare
new tools through [tool selection](tool-selection.md), not by replacing the
working pipeline during an asset task.

## Native resource checks

- Preserve inputs and donor-container identity. Match raw/native paths and import
  settings; a GLB does not establish materials, binds, skin or native compatibility.
- Require real exit/log checks and fresh outputs. Re-serialize the actual generated
  native resource instead of trusting an old JSON sidecar; inspect packed/extracted
  payload identity when packaging is in scope.
- A general CR2W field diff can omit payloads. The inspected Modwright 0.1.10 diff
  ignores `renderResourceBlob` and `parameters` subtrees, plus HandleId/BufferId;
  inspect affected geometry/parameters independently. See the source-linked
  [comparison](edgemodders-comparison.md#cr2w-diff-blind-spots) for its exact scope.
- For animation packaging/testing, first pass the universal
  [Blender full-motion/360° gate](animation-retargeting/qa-debugging.md#mandatory-blender-visual-acceptance).
  Diagnostic exports remain allowed; native/package and runtime gates stay separate.

## Corrected animation and material inventories

The maintained summaries belong in
[summarize_weapon_json.jq](../scripts/summarize_weapon_json.jq), with
[test_summarize_weapon_json.sh](../scripts/test_summarize_weapon_json.sh) beside it.
They are separate from Blender adapters and MCP servers so inspections do not
silently lose fields when a wrapper changes. The helper reads JSON and does not
convert or modify assets.

Set `SKILL_DIR` to the actual directory of the loaded `SKILL.md` (its `scripts/`
folder must contain the linked helper); do not assume the current project is the
skill source checkout. Configure `WK_CLI` as the executable or established
launcher for **this operation**. Assign `asset_copy` to a preserved native resource,
`fresh_output` to a new empty directory, and `animation_json` or `mesh_json` to the
output actually produced there. Serialize each resource separately, stop on a
nonzero result, and inspect the converter log and output provenance before querying.
Do not continue with a stale sidecar after conversion fails.

```bash
: "${SKILL_DIR:?Set SKILL_DIR to the actual loaded skill directory}"
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

