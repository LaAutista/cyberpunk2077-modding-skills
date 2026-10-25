# Agent-neutral setup and preflight

Use the packaged Node entry points in `scripts/setup/`; they travel with the skill
when `scripts/install-skills.sh` installs the two sibling skills. Codex and Claude
can run the same commands. From a repository checkout the `setup/*.mjs` files are
thin entry points. Set `SETUP` to the installed skill's `scripts/setup` directory,
or `setup` in a repository checkout.

```bash
SETUP=/path/to/cyberpunk2077-modding/scripts/setup
node "$SETUP/preflight.mjs"
node "$SETUP/provision.mjs" plan --root /new/private/cp-tools --components foundation,ron,wine,blender,audio,docs,skills
node "$SETUP/provision.mjs" install --root /new/private/cp-tools --components foundation,ron,wine,blender,audio,docs,skills --apply
source /new/private/cp-tools/env.sh
node "$SETUP/preflight.mjs" --root /new/private/cp-tools
node "$SETUP/provision.mjs" verify --root /new/private/cp-tools
```

Choose components for the task; a RoN port does not make every future source or
runtime framework a requirement. Installation without `--apply` is a plan. Use an
absolute, new, isolated root beneath an existing real directory. Existing unowned
roots are refused. No game, manager profile, shared skill, credential store or
agent settings are changed. The optional `skills` component installs missing
sibling skills and the missing REA skill under the tool root's `agent-skills`;
existing folders and local modifications are preserved.

## Supported platform and host prerequisites

Provisioning is supported on **Linux x86_64**. Windows, macOS and ARM have read-only
discovery; their asset/provisioning paths remain unsupported. Existing native Linux
and Wine operations have distinct compatibility limits. The tested host is CachyOS,
with Wine11.20 and the host CMake/C++ toolchain recorded in the build receipt.

The host needs Node18+ with fetch, Bash, Git, Python with `tarfile.data_filter`
(Python3.12+, or a maintained 3.11 build), pip/venv for Python dependency components,
and operation-specific OS libraries. RoN compilation needs CMake, Make and C++.
Wine components need Wine/wineboot/wineserver. jq, ImageMagick and a font are required
for the existing inventory/contact-sheet helpers, rather than every provisioning
component. Use the distribution's supported package manager for missing host
packages; this installer does not replace host packages during concurrent work.
On Debian-family systems the corresponding starting packages are `nodejs git python3
python3-venv python3-pip build-essential cmake wine jq imagemagick`; on Arch-family
systems use `nodejs git python python-pip base-devel cmake wine jq imagemagick`.
Package availability/names and GPU/display dependencies are distribution-specific.
Inspect `ldd` on the verified binaries when a loader reports a missing shared library.

Node handles orchestration and hashes. Python is retained for the existing docs and
Blender workflows, plus a small standard-library extractor that validates archive
paths/links before extraction. No Python package is installed globally. Blender uses
its own bundled interpreter and a separate, hash-pinned zstandard directory; the
system Blender/Python/add-ons and stale Blender MCP configuration are not adopted.

## Component contracts

| Component | Installed in isolated root | Evidence and boundaries |
| --- | --- | --- |
| `foundation` | independent SDK10.0.400, runtime10.0.12, WolvenKit ConsoleLinux9.0.1 and native launcher | Official archives/checksums; SDK identity, runtime listing and CLI help smoke. No Bodycam SDK dependency. |
| `ron` | foundation, pinned CUE4Parse with recursive submodules and six corrections, Oodle2.9.16, native RonExtract | Fresh private NuGet caches, checked-in package lock graphs, locked restore, CMake/native build, helper help. Source game/mappings remain supplied. |
| `wine` | foundation, pinned 9.0.1 console/desktop packages, custom 456-file assembly and metadata patches, separate win64 prefix and launcher | File identities and patched metadata verified. Prefix initialization, long-path policy and CLI help. No mscoree suppression, Winetricks, foreign prefix copying or .NET installer guessing. |
| `blender` | portable official Blender5.2.3, pinned UEFormat, zstandard0.25.0 wheel | Factory-startup batch import smoke, isolated config/scripts directories. No MCP required. |
| `audio` | Wine route, llvm-mingw20260922 and original offline FMOD helper | Public Windows C API compilation; FMOD2.03.10 DLLs/banks are owner-supplied runtime inputs. No FMOD SDK implementation or game DLL bundled. |
| `docs` | separate Python venv/parser, authoritative WolvenKit pages and independent pinned RED4ext/SDK repositories | Hash-pinned parser plus all transitive dependencies; acquisition, hash verification, index and search. Source URLs, times, hashes and commits retained. |
| `skills` | missing sibling skills and bundled REA skill from official `rea-agents@6.4.0` package | Missing-only, no upgrades/replacement, no MCP registration or engine setup. Package code is not executed. |

The SDK and runtime remain independent. Native .NET applications targeting10.0.0
use patch roll-forward to the isolated10.0.12 runtime. Wine's self-contained package
retains its recorded Windows10.0.11 runtime metadata. WolvenKit9.1.0 is not adopted
for the 9.0.1 builders merely because it exists on the machine.

Official binary archives have pinned hashes in `scripts/setup/downloads.json`.
Git sources use exact commits; CUE4Parse applies only the bundled patch, and its
recursive submodule identities appear in receipts. NuGet's resolved dependency
graph/content hashes are fixed in `scripts/setup/ron-locks`. New receipts hash the
installed file tree and record recipes, build inputs and host toolchain. Generated
Python bytecode and Git bookkeeping are excluded from immutable file-tree checks.
A successful build can retain upstream compiler/advisory warnings; it is not a
security clearance or a gameplay test.

## Discovery, configuration and runtime frameworks

Preflight never executes discovered candidates. It reports platform/distribution,
common Steam installations and static PE file versions where available, file hashes,
and four statuses: `present` for a verified recipe/recorded identity, `missing`,
`incompatible` with the selected recorded recipe, and `unknown` for found bytes
whose compatibility is unverified. A present tool does not establish game parity.
Common-location discovery supplements explicit `CP2077_GAME` or private path config;
it cannot establish a mod manager's effective resource resolution.

```bash
node "$SETUP/preflight.mjs" --project /path/to/existing/CP2077Dev
node "$SETUP/preflight.mjs" --root /new/private/cp-tools --config /private/paths.json --source ron-hk416
```

The private config is a JSON object mapping component names to file paths. For
example, supply `mapping`, `game-executable`, `fmod-dll`, or framework DLL paths.
`--strict` checks only the selected source's execution requirements, or the three
foundation tools when no source is selected. Source build requirements are recorded
separately. Different mapping bytes are incompatible with the bounded recorded
source recipe until decoded and validated; the filename/date proves nothing.

Runtime frameworks remain task/game-version-specific supplied or separately staged
inputs: RED4ext, redscript, Codeware, ArchiveXL, TweakXL, CET, and AudioXL0.8.1 for the
evidenced audio branch. Use the [topic map](topic-map.md) for their authoritative
sources and check current installed APIs/signatures. This installer does not put
frameworks into a live game or manager. Native RED4ext extension compilation may
also need compatible Windows SDK/MSVC headers; the observed xwin0.10.0/MSVC route
requires Microsoft's applicable terms and is separate from the supplied-game
redscript `scc_lib.dll` compiler route. The MinGW FMOD helper does not need that SDK.

Game resources, source DLLs/banks, game/SDK headers and build-compatible mappings
are supplied inputs, never starter-kit downloads. REA MCP/analysis engine activation
is separate: read the installed REA connection guide and prepare its client setup
plan before authorized registration. Installing its skill alone registers nothing.

## Source adapters and documentation

Cyberpunk2077 remains the destination. Read `scripts/setup/sources/README.md` and
`ron-hk416.json`: the verified first source adapter is bounded to the recorded
RoN/HK416 build, formats and assets. Future sources need their own build identities,
tool/dependency pins, adapters, semantic losses and actual evidence. They begin as
experimental; no Halo/Tarkov/other Unreal toolchain is installed speculatively.
Shared destination rigging, contact/animation inspection, audio/event translation,
native export/readback, packaging and gameplay gates remain in the existing guides.

The documentation component initially scopes retrieval to authoritative WolvenKit
pages. To extend it for a scripting task, use the same root's private library and
venv rather than editing shared installed skills:

```bash
DOCS=/new/private/cp-tools/library
PY=/new/private/cp-tools/state/docs-venv/bin/python
"$PY" "$DOCS/tools/sync-docs.py" --sections scripting-cyberpunk
"$PY" "$DOCS/tools/verify-docs.py"
"$PY" "$DOCS/tools/restore-repositories.py" --name codeware --name codeware-wiki --apply
"$PY" "$DOCS/tools/build-doc-index.py"
"$PY" "$DOCS/tools/find-docs.py" 'animation' --json
```

Repository snapshots are restored independently of wiki pages. Existing repositories
are preserved; confirm their commits before trusting them. The inherited sync tool
uses cached manifest entries without rehashing, so run `verify-docs.py` before
indexing/trusting cached content. Hashes and acquisition do not imply reading.
The historical full library had887 indexed pages/62,265,688 logical bytes; it is not
bundled or represented as freshly reacquired by this scoped component.

## Repeat, recovery and validation limits

Repeat the same install command to verify installed recipes and perform no-op
component acquisition. Changed archive/component/config bytes cause refusal and
remain intact. Incomplete downloads/staging cannot become complete components.
Cached documentation scripts/locators are checked against this packaged revision
before execution; changed copies and symlinked library paths are preserved and
refused. Fetch failures are nonzero, and cached page hashes are verified before
refresh/index operations. Indexing retains unacquired repository locators so later
task-specific snapshots remain available. Failed builds retain isolated diagnostic work and subsequent attempts use a new
build directory. A failed/unknown Wine prefix is preserved; inspect it and select a
new root rather than merging it into a known prefix. An incomplete docs venv is
similarly preserved for inspection. Another installer on the same root is refused
by a lock. A stale lock after process termination needs deliberate inspection. Generated
launchers contain local paths; relocating a root requires provisioning a new root,
not adopting stale launchers or prefix markers.

Rollback is removal of the user-owned isolated root after its own processes have
exited; it does not require restoring a live profile. Keep supplied inputs outside
that root. Never delete an unfamiliar root or stop another prefix's Wine server.

The optional comparison probes also have exact helper/runtime preflight; see the
[bounded diagnostic additions](fo4-scenario-comparison.md#additional-isolated-skindependency-gates).
The review receipt is in repository `setup/VALIDATION.md`. Automated extraction,
all-sample checks, batch imports and native export are distinct from actual rendered
frame inspection, native reimport, texture cooking and user-controlled gameplay.
A complete game/mod acceptance pass and a bare-OS reinstall remain untested.
