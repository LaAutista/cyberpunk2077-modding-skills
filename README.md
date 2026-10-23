# Cyberpunk 2077 modding skills

Reusable instructions and tested helpers for AI coding agents working with
WolvenKit, redscript, CET, weapon rigs, animation adaptation and MCP tooling.
The workflow comes from real modding work; evidence and limitations travel with it.

| Start here | Use it for |
| --- | --- |
| [Cyberpunk modding skill](skills/cyberpunk2077-modding/SKILL.md) | Choose implementation layers, inspect resources, select tools and verify packages. |
| [Weapon animation inspection skill](skills/weapon-animation-inspection/SKILL.md) | Inspect donor/replacement rigs, full motion, collisions, hand contact and native exports. |
| [Lynx case study](skills/weapon-animation-inspection/references/lynx-case-study.md) | The tested diagnosis/correction process and its visual, native and gameplay evidence limits. |
| [Tool selection](skills/cyberpunk2077-modding/references/tool-selection.md) | Keep proven tools; reuse corrected summaries; defer unverified MCP integrations. |
| [Topic references](skills/cyberpunk2077-modding/references/topic-map.md) | Maintained external documentation and implementation sources. |

## Install and invoke

Clone this repository into a directory you control:

```bash
git clone https://github.com/LaAutista/cyberpunk2077-modding-skills.git
cd cyberpunk2077-modding-skills
```

For Codex, copy **both sibling skill folders** into your user skill directory.
This example stops if either destination already exists; inspect/merge an existing
installation rather than overwriting it.

```bash
skills_dest="$HOME/.agents/skills"
mkdir -p "$skills_dest"
(
  set -eu
  for skill in cyberpunk2077-modding weapon-animation-inspection; do
    if [ -e "$skills_dest/$skill" ] || [ -L "$skills_dest/$skill" ]; then
      printf 'Already exists: %s\n' "$skills_dest/$skill" >&2
      exit 1
    fi
  done
  cp -R skills/cyberpunk2077-modding skills/weapon-animation-inspection "$skills_dest/"
)
```

For a repository-scoped installation, set `skills_dest` to that project's
`.agents/skills` instead. Keep the two folders adjacent so their relative links
resolve. See [official skill discovery and invocation documentation](https://learn.chatgpt.com/docs/build-skills).
These instructions install knowledge and helpers, not game tools, MCP servers or mods.

Example prompts in Codex:

```text
$cyberpunk2077-modding Inspect this mod project, choose the appropriate tools,
and distinguish automated checks from runtime verification.

$weapon-animation-inspection Inspect this replacement's donor rig and reloads.
Preserve appearance and timing, inspect actual rendered frames, and verify native readback.
```

Use `/skills` to confirm discovery; restart the client if the new skills do not
appear. Other agents can read the two `SKILL.md` files directly or use their own
skill installation mechanism. Automatic discovery in other hosts is not tested here.

## Prerequisites and checks

- Reading/invocation requires an agent that can access the Markdown files.
- JSON summaries require Bash and jq; contact sheets additionally require
  ImageMagick and its configured font. Git is needed for cloning.
- Real asset work requires your own game resources, compatible WolvenKit, Blender
  and import/export tools. Script/runtime work needs the matching frameworks.
  [Environment setup](skills/cyberpunk2077-modding/references/environment.md)
  documents configurable paths and operation-specific Linux/Wine boundaries.
- Node.js is used only for the repository's link/publication checks, not modding.
  Python remains within Blender or an existing project toolchain.

Run the portable regressions from this checkout:

```bash
bash skills/cyberpunk2077-modding/scripts/test_summarize_weapon_json.sh
bash skills/weapon-animation-inspection/scripts/test_contact_sheets.sh
node tests/check-repository.mjs
```

The JSON helper rejects malformed required fields and preserves complete animation
lists and explicit material references. [Detailed MCP findings](skills/cyberpunk2077-modding/references/mcp-comparison.md)
separate copied-asset/offline tests from unverified Codex/game integration.
The Lynx case records actual prior visual/native checks and a package-specific
user-reported laptop reload. Neither establishes every animation or platform.

Game meshes, textures, rigs, animations, private project adapters, rendered game
images and raw private logs are not included. The Lynx workflow is a reusable
method and documented case, not a complete asset bundle or one-command repair.
See [provenance and verification](PROVENANCE.md).

## License

[MIT](LICENSE) covers this repository's original instructions and helpers, allowing
reuse with the copyright/license notice. Linked dependencies and documentation
retain their own licenses; the license grants no rights to game or mod assets.
This is an independent community project, not an official CD PROJEKT RED tool.
