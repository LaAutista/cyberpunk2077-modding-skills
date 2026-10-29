# One-gate pipeline and receipt format

Keep `STATUS.json` and `FAILURE.md` in the owning mod project, not in the shared
skill. The repository's synthetic examples contain no game assets or real passes.
Do not initialize a project by labeling old packages known-good from their names.
Copy the [OPEN status template](../assets/STATUS.template.json) into the project,
then supply the real fixture identity and blocking question before validation.

## Boundaries

Source adapter → canonical motion → Cyberpunk target adapter → existing native
serializer/readback → isolated package → identified user runtime observation.
The source adapter owns engine-specific base/clock/socket/graph interpretation;
the target adapter owns native reference/control/additive/event semantics.

Canonical motion keeps skeleton names/parents/reference-local T/Q/S; duration,
original sample/key times, local T/Q/S and interpolation; source animation/base
definition, events/curves; player/weapon/component assembly and ownership; decoder
identity, source hashes and unsupported semantics. Preserve sparse original keys
alongside sampled comparisons. Unsupported interpretation blocks the relevant gate.

The [minimal fixture](../evals/fixtures/minimal.json) is a **synthetic sampled
subset** used by the structural helper, not a universal interchange format.
It holds complete source locals at explicit times, target reference locals,
coordinate declarations and a mapping. Hashes identify inputs but are not resolved
by this structural check. Units/base/ownership text must come from source evidence;
a nonempty field does not prove its truth. The helper rejects incomplete skeletons,
cycles, nonfinite/invalid transforms, bad clocks, unsupported interpolation and
unresolved semantics. It does not solve or validate actual spatial conversion.
Sparse/native formats need their own existing decoder and parity checks.

## Evidence categories

| Category | Meaning |
| --- | --- |
| IMPLEMENTED | Operation exists; no passed behavior implied. |
| CHECKED | Named deterministic offline/native check passed for the recorded scope. |
| VISUALLY_REVIEWED | Current candidate motion and required views were actually inspected and passed. |
| USER_RUNTIME_VERIFIED | Identified user confirmed this package's behavior in the named environment/scope. |
| FAILED | A fixture demonstrates failure; keep its evidence. |
| OPEN | Required evidence unavailable or not run. |
| HYPOTHESIS | Explanation awaiting a discriminator. |

Source, target, mapping, retarget, native and package checks can earn CHECKED.
Visual requires VISUALLY_REVIEWED; runtime requires USER_RUNTIME_VERIFIED. A review
that found defects is FAILED, with the review evidence retained. Existing
PASS/FAIL/UNVERIFIED/BLOCKED receipts are historical evidence, not rewritten flags:
FAIL maps to FAILED, missing/blocked evidence to OPEN plus a reason, and a PASS
can support only the corresponding gate with current hash/scope evidence. Do not
automatically translate an old PASS into a new positive category.

## STATUS.json

Use the following fields, with `schema_version: 1`:

- `project`: stable project label.
- `baseline`: `{path, sha256}` of the immutable known-good artifact, or null with
  `baseline_note` explaining its absence. Describe its actual evidence in the handoff.
- `candidate`: `{path, sha256}` of the current native/package artifact, or null
  before one exists. It must be distinct from the baseline. After packaging, bind
  checks to the archive hash using extraction/resource comparison evidence.
- `fixture`: `{path, sha256}` of the named fixture/input manifest. That manifest
  must pin all source, target, tool and acceptance identities that affect meaning.
- `current_gate`: `{id, question}`: one of source, target, mapping, retarget,
  native, visual, package, runtime and one precise blocking question.
- `gates`: all eight IDs with `{status, evidence: []}` initially OPEN. A positive
  gate also requires `scope`, `fixture_sha256` and at least one evidence file
  `{path, sha256}`. Retarget/native/visual/package/runtime additionally require
  `candidate_sha256`. Runtime needs `user_confirmation` (actual quote/reference,
  never invented) and `environment` (game/profile/variant/conditions).
- `attempts`: chronological `{gate, hypothesis, change, result, fixture_sha256, evidence}` records;
  result is FAILED or CHECKED. Preserve actual evidence file identities. This
  history belongs to this fixture; changed inputs require an explicit new status
  revision while keeping the original failure history.
- `discriminator`: null or `{gate, question, hypotheses, after_attempt, status,
  fixture_sha256, evidence, result}`. Both attempt and discriminator fixture hashes
  must match this status's fixture. Hypotheses must be distinct; `after_attempt` is the count of
  attempts completed before it ran. Only CHECKED with evidence/result resets the
  repair budget for that gate; OPEN or a stale boundary does not.
- `next_test`: the single highest-information test, including expected outcomes.

All file references resolve relative to STATUS.json; absolute paths are allowed
for private local receipts. Every referenced file is rehashed. New evidence never
automatically carries over to another fixture/candidate hash. Failure logs remain
available even when a later discriminator permits a fresh correction.

Run from the installed skill directory with Python 3.11+:

```sh
python3 -B scripts/retarget_contract.py validate-fixture /path/to/fixture.json
python3 -B scripts/retarget_contract.py verify-mapping /path/to/fixture.json
python3 -B scripts/retarget_contract.py summarize-receipt /path/to/STATUS.json
```

The CLI reads inputs only and writes JSON to stdout; malformed or changed inputs
exit nonzero. A valid receipt with FAILED/OPEN gates exits zero while its summary
keeps acceptance false. Inspect the fields, not exit status alone. The summary
requires a discriminator after two failed corrections at the active gate; it does
not execute one or judge its scientific adequacy. No wrapper can prove honesty of
a written review or user confirmation. Independently inspect the referenced evidence.

Do not synthesize a CHECKED receipt to satisfy this helper. The fixture/mapping
validators prove structure only; native parity, measured reference poses, visual
review and gameplay remain separate work. The workflow evals exercise these false
success traps with realistic prompts rather than matching instruction wording.
