# Cyberpunk 2077 modding skills

Reusable instructions and tested helpers for AI coding agents working with
WolvenKit, redscript, CET, weapon rigs, animation adaptation and MCP tooling.
The workflow comes from real modding work; evidence and limitations travel with it.

| Start here | Use it for |
| --- | --- |
| [Agent operating contract](AGENTS.md) | Preserve baselines, work one gate, stop failed repair loops and report bounded evidence. |
| [Animation retargeting skill](skills/cyberpunk2077-animation-retargeting/SKILL.md) | Take one source clip through mapping, target reconstruction, native readback, diagnostic packaging and runtime acceptance. |
| [Cyberpunk modding skill](skills/cyberpunk2077-modding/SKILL.md) | Choose implementation layers, inspect resources, select tools and verify packages. |
| [Weapon animation inspection skill](skills/weapon-animation-inspection/SKILL.md) | Inspect donor/replacement rigs, full motion, collisions, hand contact and native exports. |
| [Animation retargeting knowledge hub](skills/cyberpunk2077-modding/references/animation-retargeting/index.md) | Load focused chapters for source playback, rest/bind, proportions, finger alignment, contact, native helpers, events and evidence-based debugging. Local case receipts retain explicit acceptance limits. |
| [Lynx case study](skills/weapon-animation-inspection/references/lynx-case-study.md) | The tested diagnosis/correction process and its visual, native and gameplay evidence limits. |
| [RoN-to-Cyberpunk workflow](skills/cyberpunk2077-modding/references/ron-port-workflow.md) | Recover source assets, adapt rigs and graph controls, inspect motion and verify native exports. |
| [Proven HK416 retargeting workflow](skills/cyberpunk2077-animation-retargeting/references/ready-or-not-workflow.md) | RoN animation with CG geometry, user-confirmed locomotion/contact, partial additive weights and the separately checked camera-comfort revision. |
| [Tool selection](skills/cyberpunk2077-modding/references/tool-selection.md) | Keep proven tools; reuse corrected summaries; defer unverified MCP integrations. |
| [Topic references](skills/cyberpunk2077-modding/references/topic-map.md) | Maintained external documentation and implementation sources. |

## Install and invoke

Clone this repository into a directory you control:

```bash
git clone https://github.com/LaAutista/cyberpunk2077-modding-skills.git
cd cyberpunk2077-modding-skills
```

For Codex, install **all three sibling skill folders** into your user skill directory:

```bash
bash scripts/install-skills.sh
```

To update an existing clone and installation on your laptop:

```bash
git pull --ff-only
bash scripts/install-skills.sh --update
```

The installer backs up existing versions outside the skill discovery directory,
compares the installed files, and leaves unrelated skills and Codex settings alone.
It prints the backup location; retain any personal additions there and merge them
deliberately. An unchanged installation is a no-op. Run only one installer at a time.

For a repository-scoped or other existing installation, pass
`--dest "/path/to/project/.agents/skills"` (or your current skills directory).
Keep the three folders adjacent so their relative links
resolve. See [official skill discovery and invocation documentation](https://learn.chatgpt.com/docs/build-skills).
These instructions install knowledge and helpers, not game tools, MCP servers or mods.

The root `AGENTS.md` governs this checkout; it is not installed as a global agent
policy. The retargeting skill carries its own gate/loop/baseline rules when invoked
from a mod project. Keep project STATUS and failure evidence with that project.

Example prompts in Codex:

```text
$cyberpunk2077-modding Inspect this mod project, choose the appropriate tools,
and distinguish automated checks from runtime verification.

$cyberpunk2077-animation-retargeting Take one sprint clip through the next blocking
gate. Preserve the working reload and produce an isolated diagnostic slice.

$weapon-animation-inspection Inspect this replacement's donor rig and reloads.
Preserve appearance and timing, inspect actual rendered frames, and verify native readback.
```

Use `/skills` to confirm discovery; restart the client if the new skills do not
appear. Other agents can read the three `SKILL.md` files directly or use their own
skill installation mechanism. Automatic discovery in other hosts is not tested here.

## Setup/preflight review candidate

See [agent-neutral setup commands and boundaries](setup/README.md). Run `node setup/preflight.mjs` from the checkout for read-only discovery; isolated provisioning supports the evidenced Linux toolchain and keeps supplied inputs/manual gates explicit.

## Prerequisites and checks

- Retarget fixture/mapping/receipt checks require Python 3.11+ only; these structural
  checks do not replace measured transforms, native readback or gameplay evidence.
- Reading/invocation requires an agent that can access the Markdown files.
- JSON summaries require Bash and jq; contact sheets additionally require
  ImageMagick and its configured font. Git is needed for cloning.
- Real asset work requires your own game resources, compatible WolvenKit, Blender
  and import/export tools. Script/runtime work needs the matching frameworks.
  [Environment setup](skills/cyberpunk2077-modding/references/environment.md)
  documents configurable paths and operation-specific Linux/Wine boundaries.
- Unreal extraction and native animation helpers use Node.js, an existing .NET 10
  SDK and the documented external CUE4Parse/WolvenKit dependencies. No automatic
  dependency downloads or game installation are performed by the helpers.
  Python preview helpers run within Blender's scripting environment.

Run the portable regressions from this checkout:

```bash
bash skills/cyberpunk2077-modding/scripts/test_summarize_weapon_json.sh
bash skills/weapon-animation-inspection/scripts/test_contact_sheets.sh
node skills/cyberpunk2077-modding/scripts/native-animation/test-native-animation.mjs
node skills/cyberpunk2077-modding/scripts/native-animation/test-beta-additive.mjs
python3 -B -m unittest discover -s tests -p 'test_retarget_contract.py' -v
bash tests/test-install-skills.sh
node tests/check-repository.mjs
```

The retargeting [workflow evals](skills/cyberpunk2077-animation-retargeting/evals/README.md)
test agent decisions separately from these deterministic helper checks.

The JSON helper rejects malformed required fields and preserves complete animation
lists and explicit material references. [Detailed MCP findings](skills/cyberpunk2077-modding/references/mcp-comparison.md)
separate copied-asset/offline tests from unverified Codex/game integration.
The Lynx case records actual prior visual/native checks and a package-specific
user-reported laptop reload. Neither establishes every animation or platform.

The [source extraction](skills/cyberpunk2077-modding/references/ron-source-extraction.md),
[native animation](skills/cyberpunk2077-modding/references/native-animation-authoring.md)
and [additive preview](skills/weapon-animation-inspection/references/additive-preview.md)
references contain working commands, prerequisites and the limits of the included
helpers. Weapon-specific scene assembly and retarget fitting still need an explicit
adapter; these helpers are not a complete HK416 mod builder.

Game meshes, textures, rigs, animations, mappings, private project adapters, rendered game
images and raw private logs are not included. The Lynx workflow is a reusable
method and documented case, not a complete asset bundle or one-command repair.
See [provenance and verification](PROVENANCE.md).

## License

[MIT](LICENSE) covers this repository's original instructions and helpers, allowing
reuse with the copyright/license notice. Linked dependencies and documentation
retain their own licenses; the CUE4Parse correction patch/context has separate
[Apache-2.0 notices](skills/cyberpunk2077-modding/scripts/ron-source/cue4parse-NOTICE.md).
The license grants no rights to game or mod assets.
This is an independent community project, not an official CD PROJEKT RED tool.
