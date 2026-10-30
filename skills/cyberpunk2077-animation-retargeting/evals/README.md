# Retargeting workflow evals

[Cases and trigger prompts](retargeting-cases.json) test agent decisions separately
from deterministic Python/native helper tests. [minimal.json](fixtures/minimal.json)
is synthetic two-bone data with intentionally synthetic identity hashes. It is not
a game skeleton or a certified source decode.
The [rig-mask fixture](fixtures/rig-mask.json) is a synthetic ten-bone hierarchy for
`masked-locomotion-carrier`; it establishes only the supplied composition example.

The `port-batch` fixtures are synthetic AnimData references and native-shaped JSON
for `accepted-release-batched-port`; their payload bytes are not animations.

For each workflow case, start an independent evaluation with the current skill
and only that case's `prompt` plus relevant raw fixtures. Keep `must_observe` and
`must_not_observe` with the reviewer; do not feed the answer rubric to the evaluated
agent. Use a temporary workspace, synthetic files and read-only source assets.
Do not install a mod, start a game or contact anyone to evaluate the skill.

Review actual outputs and mutations against every criterion. Record skill/source
hash, case ID, model/harness, commands, artifacts, observed decisions, pass/fail
and limitations in a local report outside this distributable skill. A proposed
test is not an executed discriminator; a refusal alone does not satisfy a case
that calls for a concrete failure record or derivation. Retain failing transcripts
and change the skill only when a demonstrated decision warrants it.

For trigger cases, expose the three skill descriptions to a fresh evaluator with
the prompt and record selected skills. Do not expose `activate`. Positive prompts
should select this skill; pure static fitting, texture, audio or gameplay requests
should route elsewhere. A description review is not a live host auto-routing test.
Codex `skills/list` proves discovery/enabling only, not selection on real prompts.

From the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_retarget_contract.py' -v
python3 -B skills/cyberpunk2077-animation-retargeting/scripts/retarget_contract.py validate-fixture skills/cyberpunk2077-animation-retargeting/evals/fixtures/minimal.json
python3 -B skills/cyberpunk2077-animation-retargeting/scripts/retarget_contract.py verify-mapping skills/cyberpunk2077-animation-retargeting/evals/fixtures/minimal.json
```

These deterministic checks exercise valid and corrupt contracts, hash preservation,
evidence categories, missing runtime/visual proof and the failed-attempt breaker.
They do not execute the behavioral prompts or prove game-level retarget quality.
