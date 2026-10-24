# Environment and prerequisites

The skills are instructions plus small helpers, not a toolchain installer. Record
the game executable, framework versions, active manager/profile, input hashes,
WolvenKit build, Blender/add-on versions and operation-specific commands before work.
Keep machine-specific paths in a private file outside version control.

## Paths

Examples use Bash variables, not a maintainer's filesystem. Set these to paths on
your machine; `SKILL_DIR` is this skill's directory, not the repository root.

```bash
export CP2077_PROJECT="/path/to/your/mod-project"
export CP2077_GAME="/path/to/your/Cyberpunk 2077"
export WK_CLI="/path/to/your/wolvenkit-cli-launcher"
export BLENDER="/path/to/your/blender"
export SKILL_DIR="/path/to/skills/cyberpunk2077-modding"
```

`WK_CLI` is a single executable/launcher path, not a shell command string containing
arguments. It may wrap the CLI's matching .NET runtime. Use your already working
launcher and inspect `"$WK_CLI" --help` plus each subcommand's help. Do not turn a
native serialization test into a claim that every import/cook operation works there.
The Lynx project used different native/Wine routes for particular operations.

## Tool requirements by operation

| Operation | Requirements and boundary |
| --- | --- |
| Read skills | Markdown-capable agent; the sibling skill folders must remain adjacent. |
| JSON summary/regressions | Bash, jq, standard coreutils; tested on WolvenKit 9.0.1 / JSON 0.0.9 copies. Other serializers need schema tests. |
| Contact sheets | Bash, jq, ImageMagick and the selected font; frame manifests and images from your renderer. Sheets must actually be viewed. |
| Mesh/rig/animation work | Your own lawfully obtained resources, compatible [WolvenKit](https://github.com/WolvenKit/WolvenKit), [Blender](https://www.blender.org/download/) and [Cyberpunk Blender tools](https://github.com/WolvenKit/Cyberpunk-Blender-add-on). See the [weapon workflow](weapon-rigging-animation.md). |
| RoN extraction | Existing .NET 10 SDK, pinned CUE4Parse source/dependencies, Linux Oodle and build-compatible mappings; [source instructions](ron-source-extraction.md). |
| Native animation adapter | Existing WolvenKit 9.0.1 assemblies, .NET 10 SDK/runtime, Node.js and Bash; [commands and supported contract](native-animation-authoring.md). |
| Additive preview math | Blender Python, NumPy/mathutils supplied by Blender; [helper and synthetic checks](../../weapon-animation-inspection/references/additive-preview.md). |
| Runtime mod development | Only the frameworks needed for the feature; see the [topic map](topic-map.md). Verify installed API signatures and lifecycle. |
| Portable repository audit | Node.js with built-in modules; no npm install. The small audit is not a comprehensive secret scanner. |

No game assets, private Modwright bridge, Lynx-specific adapter, .NET runtime,
WolvenKit, Blender, framework binaries or MCP dependency tree is bundled. The
original source/native-animation and preview helpers are included; weapon-specific
scene/retarget/build orchestration is not. Python commands in the historical Lynx
case still refer to its established project tools, not newly bundled scripts.

## Linux, Wine and Proton

Native Node stdio tests ran on CachyOS; they establish transport behavior only.
Windows shell assumptions (`cmd.exe`) and WSL `/mnt/` mappings do not describe
native Linux or the originating project's Wine `Z:` route. Do not assemble Windows
paths by unquoted string substitution. Keep the prefix, runtime and path conversion
of a proven operation-specific launcher.

Inspect the selected manager's effective resource resolution, not only the physical
game directory. Host absolute paths and CET mod-relative paths must identify the
same mailbox for a CET file bridge. The originating redscript bridge instead used
the prefix's `LOCALAPPDATA` mailbox outside that VFS. Those are distinct protocols;
no bridge registration or current-game compatibility is claimed by this repository.

Game launch and acceptance remain user-controlled. For a runtime change, state the
exact action, expected value/appearance, lifecycle transitions and logs to inspect.
For a weapon, test affected equip/fire/reload variants with the exact exported
package; preserve save/settings/profile state and report untested variants.
