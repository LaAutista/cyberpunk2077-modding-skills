# Provenance and verification

This repository publishes original instructions and reusable helpers from a
Cyberpunk modding workspace, adapted for public use on 2026-10-23. Original prose
and code are [MIT-licensed](LICENSE). External documentation, dependencies and
game/mod resources retain their own licenses. No upstream manuals, MCP server
source, third-party mod content or game-derived asset files are redistributed.
The source-extraction correction patch includes necessary upstream context under
its separate Apache-2.0 license/notices.

## What can be reproduced from this repository

- The jq summary's synthetic regression suite: wrapped names/durations, material
  fields, duplicate clip names, long lists, deep/unknown-suffix references,
  unresolved hashes and nine malformed-input rejections.
- The contact-sheet helper's synthetic suite: frame selection/endpoints, image
  dimensions, hashes, honest review flags and nine rejection cases. Generated test
  images are simple synthetic colors/text, not game captures. A synthetic sheet
  was also opened and its frame/time labels inspected during packaging.
- Repository link/anchor, skill metadata, file-type and common credential/personal
  path checks through `node tests/check-repository.mjs`. These checks supplement
  manual inspection; pattern checks cannot guarantee that arbitrary future files
  contain no secrets or copyrighted material.

For the initial 2026-10-23 publication, both skills passed the established skill-creator frontmatter validator during
packaging. The README's installation example was exercised in an isolated directory:
both skill folders and their relative references worked, and a repeated installation
refused existing destinations. All 80 distinct external reference URLs returned
successful HTTP responses at publication review; 63 local links/anchors resolved.
The repository checker also rejected a deliberately broken installed reference.
The distribution was reviewed file by file for portable links, original
content and stated evidence limits. No local credentials, machine-specific user
paths, raw logs, binary assets or third-party source were selected for publication.

## Historical evidence that is documented, not bundled

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| [Lynx case](skills/weapon-animation-inspection/references/lynx-case-study.md) | A local diagnosis/correction workflow with recorded native geometry/animation checks and actual frame-review coverage. | A fresh public clone cannot reproduce the case without the original assets and custom adapters. No universal retargeting or exhaustive platform/graph coverage. |
| User's clean laptop reload report | Positive user-reported gameplay evidence for the package they tested. | Exact package hash/version/variant was not supplied; do not attach the report to every build or animation. |
| [MCP source/copy study](skills/cyberpunk2077-modding/references/mcp-comparison.md) | Pinned source inspection, real offline transport, copied-asset comparisons and explicitly identified API doubles. | No new MCP was registered in Codex; no current CET/game, Proton/VFS or RedSocket acceptance. |
| Private JSON-copy regression | The published helper also matched 19 animation name/duration pairs and all 24 paths against retained Lynx goldens; 21 material entries remained by count. This comparison was rerun during packaging. | Game-derived fixtures/goldens are not shipped, and their counts are not thresholds for other weapons. |
| [Development corrections](skills/cyberpunk2077-modding/references/documentation-corrections.md) | Source/Lua/documentation findings from recorded October 2026 revisions. | Not a claim that current docs retain the same mistakes or that examples work with every installed framework. |

The detailed [Lynx command contracts](skills/weapon-animation-inspection/references/lynx-command-contracts.md)
name unavailable adapters explicitly. They preserve operational knowledge without
pretending to supply an asset bundle. Generic rigging, collision, rendering and
native-export instructions remain applicable with independently validated adapters.

## Maintaining evidence

Preserve regression tests with helper changes. Add a failing input before adapting
another serializer shape. Use your own preserved assets for native checks and
record exact tool/input versions privately. Review generated manifests before
sharing: the contact-sheet helper intentionally records absolute input paths for
local provenance.

For a new result, separate implementation, automated checks, visual inspection and
user gameplay acceptance. State actual commands, views, sampled frames/times and
unavailable checks. Do not copy success wording from this study onto a different
asset, platform or build. No new game launch or weapon edit was performed for the
initial publication.

## HK416 workflow update, 2026-10-24

The [port workflow](skills/cyberpunk2077-modding/references/ron-port-workflow.md)
and [case](skills/cyberpunk2077-modding/references/ron-hk416-case-study.md) preserve
the distinction between the rejected donor-derived attempt, the clean rebuild's
offline checks and the user's later report that the reload plays. Thumb/contact,
optic, texture and sound issues remain open. The report supplied no exact package
hash, player variant or frames; none are inferred. Existing Lynx and MCP guidance
and summary regressions remain intact.

Included helper origins and new portability checks:

- `scripts/ron-source` derives from the original RonExtract project,
  `ron_pak_inventory.mjs`, `ron_source_export_check.mjs` and the retained converter
  patch. Explicit SDK/source/mapping/Oodle/output arguments replace private paths;
  the extractor no longer silently downloads Oodle. Fresh output reproduced all
  34 historical exchange files byte-for-byte: 40 packages, 97 raw companions and
  114,345 sampled channels. All 26 PAK indexes passed. Patch application reproduced
  the four corrected pinned upstream files exactly. Negative tests rejected reused
  output, missing Oodle, invalid mode, changed raw bytes and incomplete timelines.
- `scripts/native-animation` derives from the original selected native adapter,
  preparation/comparison, canonicalization, independent readback and semantics
  checkers. With existing WolvenKit 9.0.1 and .NET 10.0.400, unchanged and controlled
  single-channel copied-resource roundtrips passed. Selected authoring passed for
  58 clips with 91 untouched, maximum discrepancy 3.6508e-7 and 15,938 stored float
  keys checked. Corrupt float/event/unselected-descriptor cases were rejected.
  All 20 original input hashes stayed unchanged. Portability tests also caught and
  fixed null event-handle preservation and malformed key-kind/coverage rejection.
- The preview helpers derive from original GLB sampling and additive-composition
  code, not copied Blender/UEFormat/WolvenKit implementations. The reference defines
  the bind-relative export contract and remaining native-graph limits. Contact
  sheets retain the Lynx manifest format and add hash-checked HK416 frame manifests.
  Fresh parsing sampled 149 clips at 8,568 key times across five native-readback
  GLBs; four explicit additive/base combinations passed 80 sample evaluations.
  These checks establish finite transform sampling, not native graph behavior.
  The portable sampler's final STEP endpoint bug was fixed with a regression.
- Both skill frontmatter validators and the original animation/material-summary
  regressions passed again. Blender synthetic cases cover noncommuting additive
  rotations, scale/hierarchy composition and endpoint interpolation, with 13
  negative cases. Contact-sheet checks cover both manifest schemas and 19 rejected
  inputs. A real four-frame manifest produced a sheet whose layout/labels were
  opened for inspection; this was not a new weapon-animation visual acceptance.
- The portable installer passed fresh install, explicit update, unchanged no-op,
  backup preservation, unrelated-file preservation, simulated promotion-failure
  rollback and source/destination-overlap refusal in temporary directories.

Final publication checks resolved all 112 local links/anchors across 47 text files
and both skill entry points. New source/tool reference URLs were checked, including
successful HTTP header checks for the mapping and Oodle download locators; the
dependency payloads were not downloaded again. This verifies link availability,
not the compatibility of future bytes served by mutable URLs.

The fresh extraction and native tests wrote only private scratch output using
existing external dependencies/assets. Their binaries, fixtures, assets and raw
logs are not published. Clean-machine dependency bootstrap, laptop execution and
new Blender/gameplay acceptance are not implied by these copied-asset tests.
The historical package's visual receipts stay local and are not recreated by
documentation publication. These helpers retain their stated version and input
contracts; they are not universal game converters.

The repository's original instructions/helpers remain MIT. CUE4Parse patch context
retains [Apache-2.0](skills/cyberpunk2077-modding/scripts/ron-source/cue4parse-LICENSE.md)
and [attribution](skills/cyberpunk2077-modding/scripts/ron-source/cue4parse-NOTICE.md).
External mapping files, commercial decompression libraries and game resources are
referenced, not redistributed or licensed by this repository.
