# WolvenKit and CET MCP comparison

This is a public summary of a completed **2026-10-23 local source/copy study**.
Its private asset fixtures, raw logs, custom Modwright implementation and test
harnesses are not distributed. The numerical results below are retained study
findings, not a claim that a public checkout reproduces all experiments. The
[included summary regressions](../scripts/test_summarize_weapon_json.sh) use
synthetic inputs and can run without game assets. See [tool selection](tool-selection.md)
for adoption decisions and current task routing.

## Source identity and evidence levels

| Implementation | Pinned revision | Discovery result |
| --- | --- | --- |
| [Y4rd13/wolvenkit-mcp](https://github.com/Y4rd13/wolvenkit-mcp/tree/39429a7036ad1deb7b6dcc18738a1f3b4bc90178) | `39429a7036ad1deb7b6dcc18738a1f3b4bc90178` | Actual SDK stdio initialization and 45 tools listed. |
| [Y4rd13/cyber-engine-tweak-mcp](https://github.com/Y4rd13/cyber-engine-tweak-mcp/tree/4893237b5d181c7d1e0bd8638035a56b1bf607fc) | `4893237b5d181c7d1e0bd8638035a56b1bf607fc` | Actual SDK stdio initialization and 37 tools listed. |

Both projects were MIT-licensed at these revisions; retain their notices if copying
substantial source. This repository includes original guidance and an independent
jq helper, not the servers or their dependencies. Findings apply to the pinned
implementations and tested versions; do not assume later revisions share defects.

The study distinguished source inspection, actual offline transport, copied-native
asset comparison, and explicit API doubles. No new server was registered in Codex;
no live CET/game query, TCP/RedSocket trial, current game callback acceptance or
visual weapon test occurred in the MCP study. Existing Lynx visual/gameplay evidence
is separate. Tool discovery does not establish that every named tool works.

## WolvenKit capability map

| Implementation | Existing equivalent and practical assessment |
| --- | --- |
| [Archive tools](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/archive.ts#L10-L235): listing, search, extraction, pack, conflict listing | Existing CLI and manager-aware inspection already cover these. Search scans archives sequentially; no cache/index or speed benefit was demonstrated. Physical game-directory scans omit other archive roots and manager overlays. |
| [Conversion and patching](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/convert.ts#L11-L299) | Named convenience around the existing codec. Patch lacks typed validation, backup and roundtrip guarantees supplied by the originating guarded workflow. |
| [Inspection summaries](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/inspect.ts#L9-L390) | Compact inventory is useful, but animation, mesh, texture and dependency assumptions omitted actual fields on copied assets. The independent jq helper retains the corrected animation/material subset. |
| [Export/import/uncook](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/assets.ts#L7-L88) | Thin wrappers omit operation-specific rigs, game paths, donor containers, import settings and native readback. They do not replace the verified weapon pipeline. |
| [Project tools](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/project.ts#L10-L396) | Creation makes four folders, not a WolvenKit project file. Validation mainly checks directories/extensions. Orphan detection lacks external roots; build does not deploy a manager-aware scripts/resources/tweaks chain. The TweakXL template places `$base` outside the new record. |
| [Information/diff helpers](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/info.ts#L10-L360) | Reverse-hash rehashes its input; performance analysis measures disk bytes/extensions; decompile searches filenames. Diff includes export metadata and caps detail. These names do not establish resource resolution, GPU profiling or decompilation. |
| [Mod-management wrappers](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/modmanager.ts#L11-L157) | Backup overwrites one `.bak`; archive comparison uses listing lines rather than payload hashes; merge loops separate pack operations rather than staging a union. Installation targets a physical directory rather than the effective manager profile. |

### Tested copied-asset results

The actual stdio harness made **22 MCP calls and 33 comparison/reproduction
assertions**. Some assertions confirmed defects: a passing reproduction is not a
passing upstream feature. Six source asset/archive hashes remained unchanged.
Direct native WolvenKit 9.0.1 serialization supplied the independent comparison.

| Experiment | Observed result and boundary |
| --- | --- |
| Untouched runner on CachyOS | Discovery succeeded; CLI execution failed because the runner always invokes `cmd.exe /c`. Setting `WOLVENKIT_CLI` alone did not fix it. [Runner](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/cli.ts#L13-L55). |
| Native execution alone | CLI 9.0.1 treated legacy `-p` as an invalid input but still serialized the later valid asset. Exit 160 was hidden because the wrapper treated nonempty stdout as success. Partial output did not mean successful execution. |
| Archive search | Without explicit `--list`, the CLI emitted no file listing; the wrapper returned no meshes from a copied archive containing them. |
| Temporary compatibility runner | Direct execution, positional inputs, explicit archive `--list` and real exit propagation allowed mesh, animation, texture, entity and rig serialization. All five JSON `Data` values matched direct CLI exactly. This temporary adapter was not installed or an upstream fix. |
| Animation summary | Reported 19 entries with missing names/durations. The actual values are under `animations[].Data.animation.Data`. [Summary implementation](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/inspect.ts#L326-L345). |
| Mesh/texture/entity summaries | Missed 21 mesh chunks and 4096×4096 texture dimensions/13 mips; all five typed CName component names were returned correctly without flattening. The mesh uses `renderResourceBlob.Data.header.renderChunkInfos`; mip count is nested under the PC texture resource. [Implementation](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/inspect.ts#L75-L138). |
| Dependency traversal | The suffix heuristic omitted the actual `engine\materials\metal_base.remt` path. Typed `DepotPath` traversal recovered all 24 explicit paths. This is not a transitive graph or resolution of hashed/dynamic references. |
| Patch/hash/diff | A copied bone-name patch preserved all other `Data`; generated hash matched direct CLI. Reverse-hash hashed the number again. Upstream diff treated path/time metadata differences between identical native resources as changes. |
| Pack and readback | Adapted MCP and direct native CLI each packed two copied resources. Independent extraction returned the exact two input payload hashes. This narrow trial does not replace operation-specific production packaging or full weapon verification. |
| Stale output after failure | With a converter deliberately exiting 7, mesh inspection accepted an old JSON sidecar and reported success. [Ignored conversion result](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/tools/inspect.ts#L9-L30). |
| Existing typed diff | The originating Modwright diff ignored export metadata for identical copied rigs and reported exactly one changed bone-name field. Its render-buffer ignore list still makes it unsuitable for mesh equality. This custom implementation is not shipped here. |
| Corrected compact triage | Recovered 19 full clip name/duration pairs in 1,247 bytes from 17,984,184 bytes of animation JSON; 21 chunks, 30,668 vertices, 90,684 indices and 19 bones matched the existing geometry receipt. Also recovered texture details, five component names and explicit paths. This measures selected-field completeness/output volume, not general speed. |

The maintained animation/material helper additionally passed synthetic cases for
duplicate names, 121 clips, deep/unknown-suffix paths and fail-closed schema errors.
The private copy regression compared every animation pair and all 24 paths with
golden results, plus the count of 21 retained material entries. These fixture
counts are not acceptance thresholds for other weapons. Mesh, texture and entity
triage recipes are study findings, not implemented features of the shipped helper.

## CET capability map

| Implementation | Existing overlap or useful increment | Boundary |
| --- | --- | --- |
| [Execution/evaluation/batch](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/tools/execution.ts#L11-L65) | Remote console convenience beyond a bounded snapshot interface | Expression evaluation can write state; the actual offline Lua fixture wrote a marker. `pcall` is not a time limit or rollback. |
| [Player/game state](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L5-L98), [inventory/equipment](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L455-L614) | Originating bridge already exposed player/position, weapon identity, magazine count/capacity and ammo assertions; broader queries could aid targeted diagnosis | No matching boot/save identity or explicit snapshot assertions. Player description promises fields omitted by the handler; equipment enumeration is incomplete. |
| [TweakDB/RTTI](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L100-L247) | A live effective flat read is useful scope absent from the originating bridge | Current engine APIs were not exercised. Some API shapes differ from captured declarations; missing/partial values are unknown, not evidence of absence. |
| [Observation](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L249-L326) | A bounded buffer could help event timing | Offline drop-oldest/drain worked with an explicit callback double. No live hook proof, unsubscribe, subscription cap, drop count or epoch; nil arguments truncate later values. |
| [Player mutations](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L618-L698), [world/quest mutations](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L702-L915) | May arrange separately authorized test conditions | Grants, teleport, stats, effects, time/weather and quest facts are writes. They do not belong in a read-only weapon inspection route. |
| [Log and mod listing](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/tools/dev-tools.ts#L46-L126) | Matched direct copied-file inspection; no demonstrated practical benefit | Physical `init.lua` directories do not establish enabled profile, installed version or runtime load. Log reads load the entire file before slicing. |

### Tested offline results and reproduced defects

The actual Node file transport exchanged commands with the actual upstream Lua
bridge/serializer under LuaJIT 2.1, without `Game`, CET or RedSocket. Pure Lua
returned 42 for `6*7`. Actual SDK stdio discovery/calls, copied log tailing and
two copied mod-directory listings matched expectations. These were protocol and
filesystem checks, not game integration.

- **Concurrency:** two hosts sharing one mailbox overwrote the command slot; only
  the second command reached the worker, and response deletion could leave both
  callers timed out. There is no queue/lock; the shared temporary filename adds
  rename races. [File transport](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/transport/file-bridge.ts#L25-L55).
- **Freshness:** a heartbeat one day in the future was accepted because the test
  checks `age < 3000` without a lower bound. No process boot or save identity is
  checked. [Predicate](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/transport/file-bridge.ts#L63-L66).
- **Timeout:** a command already consumed by a deliberately delayed worker
  executed after the host's five-second timeout. Timeout did not cancel execution;
  retries can duplicate effects. Requests lack expiry/session data.
  [Protocol](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/utils/protocol.ts#L3-L17),
  [dispatch](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/bridge.lua#L121-L169).
- **False success with a declared API double:** `SetFlat(false)` returned success
  because only thrown errors are checked. This establishes wrapper semantics,
  not an attempted live write. [Handler](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L168-L176).
- **Batch and callbacks:** all-failing batch entries retained top-level success;
  callback `head,nil,tail` retained only `head`. A double verified that buffer size
  two keeps the latest two of three events and drains on read; no game observer
  was exercised. [Batch](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L328-L348),
  [callback loop](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/handlers.lua#L280-L289).
- **Serialization:** raw U+0001 appeared inside purported JSON and was rejected by
  strict Node parsing and the bundled Lua decoder. Outer transport escaping did
  not make the inner result valid JSON. [Serializer](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/serializer.lua#L29-L35).

For comparison, four copied originating-bridge host tests passed: strict wire,
malformed/stale data; assertion truth/failure; unrelated response/epoch rejection;
and native file roundtrip/concurrent refusal/helper-death detection. This proves
the tested native fixture path, not current Cyberpunk callbacks. Same-process
concurrent refusal does not establish safety with independent hosts.

## Codex, CachyOS and Proton compatibility

- **Codex:** both implementations use standard SDK stdio. Actual interoperability
  passed on Node 24.16.0. Codex 0.144.1 accepted the command/args/env configuration
  shape in local help, but neither server was registered or tested through an
  installed Codex integration. Claude configuration files are not Codex settings.
- **CachyOS/WolvenKit:** native CLI 9.0.1 was exercised. The upstream runner assumes
  `cmd.exe` and [WSL `/mnt/` mappings](https://github.com/Y4rd13/wolvenkit-mcp/blob/39429a7036ad1deb7b6dcc18738a1f3b4bc90178/src/utils/paths.ts#L25-L51),
  which differ from operation-specific Wine `Z:` mappings. Keep explicit native or
  Wine launchers, version-specific arguments and true failure propagation.
- **CET file mode:** the Node host ran natively. Its configurable absolute path
  must reach the same writable mailbox as Lua's mod-relative IO through the
  selected manager/Proton profile. This live mapping was not tested. The
  originating bridge instead used a prefix `LOCALAPPDATA` mailbox outside the
  game VFS. Physical directories did not represent the active profile; retained
  logs referred to older binaries than the current installation.
- **Defaults and TCP:** [Node defaults to file mode](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/src/index.ts#L5-L16),
  while [Lua defaults to TCP](https://github.com/Y4rd13/cyber-engine-tweak-mcp/blob/4893237b5d181c7d1e0bd8638035a56b1bf607fc/cet-mod/CETBridge/config.lua#L1-L8)
  but also polls files. TCP requires additional RedSocket game-side support;
  fallback behavior differs between host and Lua. RedSocket, TCP, pause/load/quit
  lifecycle and current CET/game APIs were not exercised.
- **Maintenance:** both pinned dependency locks installed 94 packages. Only the
  available Node 24 version was tested. Full adoption adds shell/argument/schema
  maintenance or game API/transport/lifecycle maintenance; no end-to-end speed,
  rendering or gameplay improvement was demonstrated.

## Reuse and verification requirements

Adopt the independent corrected JSON inventories and retain their regressions;
keep the established native/Wine, Blender and bounded-bridge routes. Neither MCP
recovers weapon/player animation dependencies, retargets rigs, checks surface
collisions, inspects rendered frames or verifies exported geometry. Follow the
[weapon workflow](weapon-rigging-animation.md) for those tasks.

The smallest potentially useful runtime addition is one fixed typed TweakDB flat
query through an existing bounded protocol. It remains deferred. The
[tool-selection guide](tool-selection.md#smallest-worthwhile-future-integration)
lists the exact acceptance work: current signatures, missing/type errors, session
freshness, fixture tests and an independently checked user-controlled live query.
Do not call arbitrary evaluation read-only, or promote fixture/build success into
gameplay evidence. Consult [version-matched primary documentation](topic-map.md)
before adapting runtime APIs.
