# Provenance and verification

This repository publishes original instructions and reusable helpers from a
Cyberpunk modding workspace, adapted for public use on 2026-10-23. Original prose
and code are [MIT-licensed](LICENSE). External documentation, dependencies and
game/mod resources retain their own licenses. No upstream manuals, MCP server
source, third-party mod content or game-derived asset files are redistributed.

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

Both skills also passed the established skill-creator frontmatter validator during
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
asset, platform or build. No new game launch, weapon edit or native export was
performed merely to publish these skills.
