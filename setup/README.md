# Cyberpunk setup entry points

The installer runtime is packaged inside the Cyberpunk skill so Codex and Claude
can provision tools even after the two skill folders are installed independently
of the checkout. These repository entry points invoke that same code:

```bash
node setup/preflight.mjs
node setup/provision.mjs plan --root /new/private/cp-tools --components foundation,ron,wine,blender,audio,docs,skills
node setup/provision.mjs install --root /new/private/cp-tools --components foundation,ron,wine,blender,audio,docs,skills --apply
source /new/private/cp-tools/env.sh
node setup/provision.mjs verify --root /new/private/cp-tools
```

Choose task components. Linux x86_64 provisioning is supported; other platforms
have discovery only. Host OS libraries/tools, owned game assets/DLLs/mappings,
game-compatible runtime frameworks and proprietary SDK headers remain explicit
inputs/routes. No live profile, shared skill or agent settings are modified.

Read the [complete setup/component/recovery guide](../skills/cyberpunk2077-modding/references/setup-preflight.md)
and [validation receipt](VALIDATION.md). Review candidate only; nothing is published.
