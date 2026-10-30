# Cyberpunk 2077 modding agent contract

This repository supplies bounded workflows and helpers, not a universal converter.
Case-specific offsets, skeletons, clocks and thresholds need new fixtures before reuse.

## Start and scope

1. Read the relevant skill and the owning project's current STATUS/evidence handoff.
2. Identify and preserve the known-good artifact, its hash and its actual evidence
   level. If none exists, say so; an intermediate export is not a runtime baseline.
3. For an unknown/failing route select one blocking gate and discriminating fixture.
   For an established route batch compatible actions using measured contracts.
4. Record input/tool versions and hashes before editing. Preserve dirty work and
   failed reports. Do not change live profiles or launch the game without authorization.

Routes: [general modding](skills/cyberpunk2077-modding/SKILL.md),
[weapon inspection](skills/weapon-animation-inspection/SKILL.md),
[retargeting state machine](skills/cyberpunk2077-animation-retargeting/SKILL.md).
The retargeting skill carries the operating rules when installed outside this repo;
this root AGENTS.md is not automatically loaded in unrelated mod projects.

## Evidence vocabulary

Use IMPLEMENTED (operation exists), CHECKED (named deterministic/offline/native
check passed), VISUALLY_REVIEWED (identified motion/views actually inspected),
USER_RUNTIME_VERIFIED (user confirmed an identified package in game), FAILED
(failing fixture), OPEN (not established), or HYPOTHESIS (requires a discriminator).
Keep evidence per gate, artifact and scope; none of these promotes another gate.
Retain historical PASS/FAIL/UNVERIFIED/BLOCKED receipts without relabeling them;
[pipeline](skills/cyberpunk2077-animation-retargeting/references/pipeline.md)
defines the interpretation and new status format.

## Work policy

- Preserve timing, hierarchy, anatomical translations/scales/lengths and unrelated
  tracks unless a measured fixture explicitly requires an authorized change.
- Reconstruct destination locals using updated destination parents, parent-first.
- Read back serialized native bytes independently; never export stale preview or
  controller arrays. Review the final converted motion, not an earlier revision.
- No guessed corrective rotations, cross-weapon calibration reuse, speculative
  fix stacking, or equivalent previews after the existing fixture answers the question.
- No scope expansion or replacement of a working baseline by an experimental branch.
- Compiler/import/archive success proves only that operation, not animation or gameplay.

## Vertical slice and failure breaker

For a new source, take ONE clip through decode, mapping, target locals, native
import/readback, isolated diagnostic package and user runtime test. Once decode,
mapping and container writing work, aim the next work at that slice's remaining
blocking checks. Do not polish or batch a full set first.

A diagnostic package may expose known visual defects to test the plumbing, with
those defects disclosed. It is not an accepted beta. Full-motion Blender visual
acceptance, native/package checks and identified runtime acceptance are all
required before promotion or full-set expansion. See the
[runtime contract](skills/cyberpunk2077-animation-retargeting/references/runtime-validation.md).

After a route is accepted, reuse unchanged evidence and batch compatible clips;
do not require another single-clip approval cycle per action. Explicit user release
acceptance may retain named defects or native fallbacks. Record those limits
without inventing a flawless visual pass or expanding release criteria. Use the
[MP5 workflow](skills/cyberpunk2077-animation-retargeting/references/mp5-workflow.md).

After two failed corrections at the same gate, stop correction. Write FAILURE.md
with the fixture, observations, attempted changes, evidence and remaining hypotheses.
Construct a discriminator separating at least two hypotheses; run it before another
correction. A materially equivalent edit is not a discriminator. Reuse existing
evidence when it answers the question. Missing environments leave a named blocker
and exact manual test, not a third speculative fix.

## Repository checks

From the repository root, run the checks affected by the change:

```sh
python3 -B -m unittest discover -s tests -p 'test_retarget_contract.py' -v
python3 -B -m unittest discover -s tests -p 'test_agent_workflow_tools.py' -v
node tests/test-animation-coverage.mjs
bash tests/test-install-skills.sh
node tests/check-repository.mjs
bash skills/cyberpunk2077-modding/scripts/test_summarize_weapon_json.sh
bash skills/weapon-animation-inspection/scripts/test_contact_sheets.sh
node skills/cyberpunk2077-modding/scripts/native-animation/test-native-animation.mjs
node skills/cyberpunk2077-modding/scripts/native-animation/test-beta-additive.mjs
```

For skill behavior changes, run relevant [workflow evals](skills/cyberpunk2077-animation-retargeting/evals/README.md).
Synthetic tests and agent evals do not establish native/game behavior.

## Completion

State baseline, changed files, exact commands and passed/failed/unavailable checks;
give visual/gameplay status, remaining blockers and the next highest-information
test. Completion means the user's requested acceptance gate passed. For a skill
refactor, repository/install/discovery/eval checks are the relevant scope; do not
launch ports or manufacture game evidence to validate documentation.
