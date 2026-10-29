# Edgemodders comparison and reusable lessons

Reviewed 2026-10-27. Use this note when evaluating REDbridge, REDcode, REDnode,
REDswap, EDGEdeck, EDGEmat or EDGEfab against an existing Cyberpunk pipeline.
Keep the established operation-specific native/Wine WolvenKit and Blender routes
until a candidate demonstrates a concrete improvement on preserved copies.

## Evidence boundaries

- **LOCAL-CODE:** directly inspected local implementation. This establishes what
  the code does, without claiming that its current execution or gameplay passed.
- **LOCAL-RECEIPT:** retained local test report or knowledge entry. Carry its
  date, versions and scope; it was not rerun for this comparison.
- **UPSTREAM-DOCUMENTED:** upstream documentation or release notes, linked below.
  Their tests and compatibility statements have not been independently reproduced.
- **PROPOSED:** an opportunity to investigate or implement; not a delivered tool.

This comparison performed lightweight file/source inspection only. No compared
tools were installed or executed, and no game/profile files or runtime were used.
`CP2077_DEV` below names the originating workspace; resolve its path locally
(the observed convention was `${HOME}/Documents/VibeCoding/CP2077Dev`). These
relative evidence paths are not bundled dependencies or guarantees on another machine.

## Version selection changes the answer

**UPSTREAM-DOCUMENTED:** [REDbridge 0.11.0 release](https://github.com/Edgemodders/REDbridge/releases/tag/v0.11.0)
uses WolvenKit 10.0.0-beta.1 for game 2.5. Its
[tagged changelog](https://github.com/Edgemodders/REDbridge/blob/v0.11.0/CHANGELOG.md#0110-2026-10-26)
reports incompatible 2.31 streaming-sector reads and changed sector JSON fields.
The [tagged README](https://github.com/Edgemodders/REDbridge/blob/v0.11.0/README.md)
directs 2.31 sector work to 0.10.0/WolvenKit 9.1.0. The release also reports that
2.31 and 2.5 share CR2W version 195: the header alone does not establish schema
compatibility. Version-match the game, codec and resource type before comparison.

**LOCAL-RECEIPT:** the last target named by the
local bridge README (`$CP2077_DEV/mods/modwright-bridge/README.md`)
is executable 2.31 (3.0.80.51928), not a fresh current-install check. The
WolvenKit 9.1.0 report (`$CP2077_DEV/tools/wolvenkit-update-9.1.0/REPORT.txt`)
records archive-list/extraction parity and one CMesh serialization check on
2026-10-11. The inspected
default launcher (`$CP2077_DEV/tools/bin/wolvenkit-cli`)
still selects 9.0.1. Having 9.1.0 alongside it does not migrate pinned operations;
the downloaded Windows desktop was not runtime-tested in that report.

## Capability comparison

| Lead and evidence | Existing local equivalent | Worth investigating |
| --- | --- | --- |
| **UPSTREAM-DOCUMENTED:** REDbridge exposes document sessions, type inspection and JSON Patch with inverse patches; its [changelog](https://github.com/Edgemodders/REDbridge/blob/v0.11.0/CHANGELOG.md) describes undo support. | **LOCAL-CODE:** Modwright's converters (`$CP2077_DEV/tools/modwright-local/package/dist/core/text/converters/cyberpunk.js`) declare CR2W-to-JSON byte-roundtrip and JSON-to-CR2W reverse field-diff policies. | **PROPOSED:** bounded document inspection and an explicit patch/undo receipt could reduce repeated whole-document handling. Native reconstruction still needs independent readback. |
| **UPSTREAM-DOCUMENTED:** [REDbridge mesh import](https://github.com/Edgemodders/REDbridge/blob/v0.11.0/README.md#mesh-import) copies a template, resizes appearance material assignments and reports submeshes/materials. | **LOCAL-CODE:** weapon builder (`$CP2077_DEV/tools/build_weapon_replacements.py:106`) copies donors, imports with `--keep`, reads native JSON back and reconstructs materials. HK416 clean builder (`$CP2077_DEV/tools/build_ron_hk416_clean.py:110`) checks a material-template hash and restores inverse binds by bone name after import. | **PROPOSED:** make donor identity, input/output hashes, actual submesh order and appearance/material assignment an explicit reusable receipt. Automatic resizing or repeating the final material is a convenience fallback, not acceptance of intended appearance. |
| **UPSTREAM-DOCUMENTED:** [REDcode export/import](https://edgemodders.ai/wiki/redcode/export-import.html) documents a Blender save watcher, retained import settings and folder import restricted to existing native targets. | **LOCAL-CODE:** Blender assembly (`$CP2077_DEV/tools/assemble_weapon_replacements.py`) and the builders already implement GLB/native roundtrips with dedicated verification. | **PROPOSED:** borrow the explicit watch lifecycle and folder-import filter. Exported dependency textures should not silently become new overrides. Automation remains separate from animation/geometry acceptance. |
| **UPSTREAM-DOCUMENTED:** [EDGEdeck](https://github.com/Edgemodders/EDGEdeck#readme) presents inside-archive conflicts, winners and pending deployment changes using REDbridge. | **LOCAL-CODE:** Modwright conflict core (`$CP2077_DEV/tools/modwright-local/package/dist/core/archive-conflicts.js`) already groups resource-hash collisions, names first-loaded winners, optionally resolves paths and compares stored resource segments. | **PROPOSED:** improve presentation and feed it the selected Fluorine profile's effective archive set/order; there is no demonstrated need to replace the manager. |
| **UPSTREAM-DOCUMENTED:** [EDGEmat README](https://github.com/Edgemodders/EDGEmat#readme) reports a 0.3.1 preview with a game-derived surface/microblend library, multilayer setup editing and preview. Its stale scaffold badge conflicts with that explicit status paragraph; do not infer capability from branding alone. | **LOCAL-CODE / scoped search:** inspected builders author/retain material instances, including `metal_base.remt`; no general multilayer editor or validated multilayer authoring workflow was established in the inspected project scripts/skill references. | **PROPOSED:** a multilayer dependency inspector and layer preview are a concrete gap. Existing documentation already covers much of the format knowledge; preview fidelity and game output require separate acceptance. |
| **UPSTREAM-DOCUMENTED:** [EDGEfab README](https://github.com/Edgemodders/EDGEfab#readme) explicitly says it is a scaffold with design/build-plan documents and no implementation code. | Existing local mesh/rig/material/native build steps are implemented independently. | Treat whole-asset fabrication, Unreal ingestion and animation promises as design ideas. EDGEfab supplies no demonstrated converter or retargeter to adopt at this review. |

The mutable README/wiki links were read on 2026-10-27. Release-tag links preserve
the compared release identity; check later changes before reusing this conclusion.

## CR2W diff blind spots

**LOCAL-CODE:** the inspected Modwright 0.1.10
diff implementation (`$CP2077_DEV/tools/modwright-local/package/dist/core/text/diff/cr2w.js:8`)
ignores complete subtrees named `renderResourceBlob` and `parameters`, and keys
named `HandleId` or `BufferId`. It also normalizes CName/ResourcePath spelling and
uses a numeric tolerance. A clean result therefore does not establish buffer,
parameter or byte equality. This is wider than the earlier shorthand warning
about render buffers; it does not mean every material field is ignored.

For geometry or parameter edits, inspect the affected payload independently and
retain its exact before/after identity. A prospective patch workflow should check
the expected old value/type, record the patch/inverse, serialize fresh native
output and compare the fields/buffers that actually matter. These additions are
**PROPOSED**, not implemented or tested by this documentation update. Preserve
existing dedicated mesh, material, bind and visual checks.

## Fluorine and archive conflict limits

**LOCAL-CODE:** the Cyberpunk archive enumerator (`$CP2077_DEV/tools/modwright-local/package/dist/surfaces/cyberpunk2077/archive-conflicts.js:10`)
reads physical `archive/pc/mod` and `mods/<name>/archives` under the detected install,
using its load-order reader. The conflict core compares hashes even when path
names cannot be resolved. It excludes vanilla overlaps and defaults to 25 displayed
conflicts and 25 groups, with explicit truncation flags. `sameContent` compares
stored resource segments; it is not a semantic CR2W comparison.

The local bridge's Fluorine warning (`$CP2077_DEV/mods/modwright-bridge/README.md:103`)
states that stock installation detection does not prove what the running VFS
exposes. A useful conflict report must identify the selected profile, enabled
providers and effective order. A physical-directory scan is only a partial input;
archive priority also does not decide redscript/TweakXL hook or record conflicts.
No effective-profile scan was run for this comparison.

## Hot swapping remains unverified here

**UPSTREAM-DOCUMENTED:** [REDnode 0.41.0](https://github.com/Edgemodders/REDnode/releases/tag/v0.41.0)
introduces REDswap for game 2.5. Its
[tagged REDswap documentation](https://github.com/Edgemodders/REDnode/blob/v0.41.0/docs/redswap.md)
describes version/address/cache checks, archive replacement and resource
invalidation, followed by REDnode entity/preview refresh. It distinguishes the
swap from refreshing existing instances, labels 2.5 audio handling unverified,
and warns that malformed/incomplete resources can still crash. These are external
claims, not local success evidence or a general safe-hot-reload guarantee.

**LOCAL-RECEIPT:** Modwright's retained
asset-build knowledge (`$CP2077_DEV/tools/modwright-local/package/knowledge/cyberpunk2077/process.assetbuild.yaml:62`)
records a mounted weapon mesh becoming corrupted during whole-archive RHT hot
ingest and prescribes cold deployment for that workflow. Its
reload table (`$CP2077_DEV/tools/modwright-local/package/dist/core/deploy/reload.js`)
also records removed tweak records surviving until restart, a `.hot-tweaks`
sentinel not causing reload in the named RHT version, and session-reload needs
for added request handlers or added/retyped struct fields. These retained findings
do not prove how REDswap behaves; REDswap's claims do not invalidate them.

Any later runtime trial needs the installed game/framework versions, exact
profile/package identity and an independently checked result across the relevant
spawn/equip/save-load lifecycle. No such trial is included here.

## Smallest useful follow-up work

All items below are **PROPOSED**:

1. Build a read-only multilayer dependency inventory on preserved copies:
   material instance, `.mlsetup`, per-layer `.mltemplate`, `.mlmask`, microblends
   and global normal. Report missing/unresolved references explicitly. Add preview
   only when a concrete material task needs it, with native/game acceptance separate.
2. Consolidate the existing donor-import receipt instead of replacing the codec.
   Include source/template hashes, version, actual submesh/material mapping,
   restored native binds and fresh output checks. Preserve any dedicated epsilon,
   geometry, normal and skin verification required by that target.
3. Adapt conflict presentation to an explicitly established Fluorine effective
   profile, retaining unresolved hashes, unreadable archives and report truncation.

For multilayer format knowledge already present locally, start with cached
MLMask/MLSetup I/O (`$CP2077_DEV/reference/laptop-20261007/library/docs/upstream/redmodding/wolvenkit/wolvenkit-app/usage/import-export/import-export-mlmask-and-mlsetup.md`)
and multilayer properties (`$CP2077_DEV/reference/laptop-20261007/library/docs/upstream/redmodding/cyberpunk-2077-modding/for-mod-creators-theory/materials/configuring-materials/multilayered-material-properties.md`).
Upstream versions are [WolvenKit MLMask/MLSetup I/O](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/usage/import-export/import-export-mlmask-and-mlsetup)
and [multilayer properties](https://wiki.redmodding.org/cyberpunk-2077-modding/for-mod-creators-theory/materials/configuring-materials/multilayered-material-properties).
The cached pages were inspected; those live wiki pages were not revalidated here.

No evaluated lead demonstrates local animation retargeting, source/target contact
parity or native helper-deformation acceptance. Continue the
[retargeting hub](animation-retargeting/index.md) and its separate source, visual,
native/package and runtime evidence gates.
