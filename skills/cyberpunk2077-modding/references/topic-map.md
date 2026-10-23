# Topic references

Choose the smallest relevant set. These are external primary documentation and
implementation links, not bundled snapshots or a claim that every page was tested.
Verify APIs against the actual game/framework build. Start scripting research with
Scripting Cyberpunk rather than deprecated wiki examples.

| Topic | Primary references |
| --- | --- |
| Mod structure and assets | [Cyberpunk modding wiki](https://wiki.redmodding.org/cyberpunk-2077-modding), [WolvenKit docs](https://wiki.redmodding.org/wolvenkit), [WolvenKit source/releases](https://github.com/WolvenKit/WolvenKit) |
| redscript language and hooks | [Scripting Cyberpunk](https://wiki.redmodding.org/scripting-cyberpunk), [compiler/source](https://github.com/jac3km4/redscript), [NativeDB](https://nativedb.red4ext.com/) |
| CET Lua and runtime APIs | [Scripting documentation](https://wiki.redmodding.org/scripting-cyberpunk/cyber-engine-tweaks), [CET source](https://github.com/maximegmd/CyberEngineTweaks) |
| TweakDB records and typed values | [TweakXL reference](https://github.com/psiberx/cp2077-tweak-xl/wiki), [implementation](https://github.com/psiberx/cp2077-tweak-xl) |
| Resource factories and appearances | [ArchiveXL reference](https://github.com/psiberx/cp2077-archive-xl/wiki), [implementation](https://github.com/psiberx/cp2077-archive-xl) |
| Callbacks, persistence, UI and object lifetime | [Codeware reference](https://github.com/psiberx/cp2077-codeware/wiki), [implementation](https://github.com/psiberx/cp2077-codeware) |
| Meshes, rigs and animations | [Blender add-on](https://github.com/WolvenKit/Cyberpunk-Blender-add-on), [reusable workflow](weapon-rigging-animation.md), [Lynx case](../../weapon-animation-inspection/references/lynx-case-study.md) |
| Native extensions | [RED4ext documentation](https://docs.red4ext.com/), [SDK](https://github.com/WopsS/RED4ext.SDK), [RedLib](https://github.com/psiberx/cp2077-red-lib) |
| MCP selection | [Adoption decisions](tool-selection.md), [source comparison and tested limits](mcp-comparison.md) |

For standalone items, trace the whole record → factory → entity/appearance →
mesh/material/texture chain, plus localization/icons and attachments. For UI,
vehicles, quests, world edits or audio, follow that topic in the modding wiki and
read the actual declarations used by the feature. The [development playbook](development-playbook.md)
preserves implementation-layer, lifecycle and packaging guidance.

For requested reverse engineering, inspect the exact executable/resource revision,
check official SDK and NativeDB coverage first, then use the user's established
disassembler/debugger. Treat pseudocode and guessed layouts as hypotheses until
matched to declarations or observed behavior. Keep proprietary dumps and decompiled
game scripts private. No reverse-engineering tool is installed by these skills.

See [documentation corrections](documentation-corrections.md) before adapting
historical examples. A wiki explains a workflow; source establishes behavior for
its revision; a test on the target installation establishes bounded compatibility.
