# Agent workflow tools

Use these for repeated resource lookup, graph/mask inspection and the established native
animation checks. They do not choose calibration, author motion, execute engine IK,
review renders, install a mod or establish gameplay acceptance.

## Run the native gate from one fixture

`scripts/native_pipeline.py` uses the sibling modding skill's existing native
adapter and independent readers. It replaces repeated command construction; it is
not another animation serializer. Requires Python 3.11+, Linux/POSIX, Node, an
existing .NET runtime, WolvenKit 9.0.1 and the built `NativeAnimation.dll` from the
[native authoring setup](../../cyberpunk2077-modding/references/native-animation-authoring.md).

Save a private JSON config. Paths are absolute or relative to the config file;
`node` and `dotnet` may also be executable names on PATH.

```json
{
  "schema": 1,
  "inputs": {
    "native": "baseline/player.anims",
    "rig": "baseline/player.rig",
    "authored": "authored/player.glb"
  },
  "tools": {
    "node": "node",
    "dotnet": "/existing/dotnet/dotnet",
    "wolvenkit": "/existing/WolvenKit-9.0.1",
    "native_adapter": "/private/native-build/bin/NativeAnimation.dll"
  },
  "output": "work/native-candidate-01",
  "timeout_seconds": 55,
  "lock": "/tmp/cp2077-heavy-work.lock"
}
```

From the retargeting skill directory:

```sh
python3 -B scripts/native_pipeline.py plan /private/fixture.json
python3 -B scripts/native_pipeline.py run /private/fixture.json
python3 -B scripts/native_pipeline.py status /private/fixture.json
```

Supply the **unprepared** authored GLB, selecting existing clip names in the
compatible native container. The tool freshly serializes the original container
and rig, exports the original, prepares selected clips once, imports, serializes
and exports the candidate, independently decodes the selected stored clips, and
runs authored and semantic comparisons. Original native inputs stay untouched.

The final stdout is compact JSON; step progress goes to stderr. `CHECKED` covers
these native checks only. `runtimeVerified` and `visuallyReviewed` stay false.
`FAILED` identifies the step, retained log and resume command. `BUSY` exits75 when
another heavy job holds the lock. Do not launch another copy to bypass that lock.
Each tool has a bounded timeout and modest CPU/thread/heap settings; timed-out
process groups are killed. Child tools retain the lock if the runner is interrupted.

Rerun the same `run` command to resume: completed steps are reused only after their
output hashes and all input/tool fingerprints match. Failed attempts remain in
separate directories. A completed rerun executes zero conversion steps. Changed
source, tool, config or completed-output bytes require a fresh output directory;
preserve the previous receipt. This prevents stale or partially written files from
being treated as successful work. Exit0 alone is insufficient: expected outputs,
signatures, JSON and final verifier results are checked, including WolvenKit's
logged conversion errors that can accompany exit0.

## Batch established native fixtures

After the first route is established, put existing fixture configs in a private
manifest. Each fixture may contain several compatible authored clips. Relative
fixture paths resolve against the manifest; each config retains its own path base.

```json
{"schema": 1, "fixtures": ["player-male.json", "player-female.json", "weapon.json"]}
```

```sh
python3 -B scripts/native_pipeline.py batch-plan /private/batch.json
python3 -B scripts/native_pipeline.py batch-run /private/batch.json
python3 -B scripts/native_pipeline.py batch-status /private/batch.json
```

All configs and existing receipts are validated before any conversion. Outputs
must be distinct, nonoverlapping and outside every input/config/tool/lock; all
fixtures share a heavy-work lock. Jobs run serially and stop at the first failure
or busy lock. Rerun the same command to reuse completed fixtures/stages. The JSON
includes per-fixture results, unstarted fixtures, steps run/reused and wall seconds
for this invocation. It does not measure authoring, visual review or gameplay.

Preflight also rejects fractional/negative/out-of-range native event frames in
the authored GLB. The native event clock is separate from the animation key clock;
this check does not resample or retime either. Empty/null event arrays are valid.

## Inventory source action references once

```sh
python3 -B scripts/ron_action_inventory.py /private/AnimData.uasset.json \
  --output /private/source-actions.json
python3 -B scripts/ron_action_inventory.py /private/AnimData.uasset.json \
  --action FireSingle --action Draw --output /private/selected-actions.json
```

Python standard library only. Reads exported class `Properties`, including nested
arrays, and preserves property/index plus `Body_FP`/`Gun_FP` context. Direct `_FP`
properties are included; TP references are excluded. The complete receipt contains
source hash, references and deduplicated extraction paths with numeric export
object suffixes removed. It fails on unknown selected properties, malformed refs
or no explicit FP references. Output files must be new. Without `--output`, stdout
contains the full JSON; with it, stdout is a compact summary.

This inventories explicit references only. Resolve inheritance, montages, selected
variants, additive bases and source decoder semantics separately. Do not infer
animation type, runtime selection or A2/A3 equivalence from names/counts.

## Measure changed clips separately from changed containers

```sh
node scripts/animation_coverage.mjs /private/baseline.anims.json \
  /private/candidate.anims.json /private/coverage.json
```

Reads WolvenKit native JSON through the sibling canonicalizer. It compares stored
per-clip payload hashes and metadata separately, excluding relocatable addresses
and serializer buffer copies. Reports `unchanged`, `metadata_only`,
`motion_changed`, `added` and `removed`; output must be new. Chunk bounds,
duplicate names and malformed payloads fail. Unchanged donor bytes identify
retained native data; metadata and graph composition still influence evaluated
motion. Changed bytes can be helper edits or codec differences, so they do not
prove source fidelity. The report does not decode motion or certify runtime.

Portable coverage regression: `node tests/test-animation-coverage.mjs` from the
repository root. Never publish real input JSON or generated coverage receipts.

## Find the archive before extracting

```sh
python3 -B scripts/asset_inspect.py locate /game/archive/pc/content \
  'base/gameplay/anim_graphs/player_dualwield.animgraph'
```

This reads RDAR v12 indexes and reports the depot hash and all matching archives.
It avoids guessing an archive from an old cache or interpreting an empty regex
extraction as success. It does not extract assets or determine effective mod load
order. Incomplete scans report errors and exit1; no matches in a complete scan is
an explicit empty result.

## Inspect graphs without expanding huge handle trees

```sh
python3 -B scripts/asset_inspect.py graph /private/player.animgraph.json
python3 -B scripts/asset_inspect.py graph /private/player.animgraph.json --clip idlepose_ironsight
python3 -B scripts/asset_inspect.py graph /private/player.animgraph.json --node 130
python3 -B scripts/asset_inspect.py compare-graphs /private/authored.json /private/readback.json
```

Summaries replace embedded handles with references and bound array/string output;
they never print recursive graph subtrees. Node IDs are local to that exact file,
not stable across game builds. The comparison checks the complete `Data` graph,
including shared-reference identity, every property and array order. It tolerates
only small numeric serialization variation (absolute/relative2e-8) and reports at
most20 differences. Header timestamps/paths are excluded. A matching graph is
serialization evidence, not proof of native scheduling, initialization or gameplay.

## Inspect the composing body mask

```sh
python3 -B scripts/asset_inspect.py rig-mask /private/player.rig.json \
  --mask _base_upperbody --bone Hips --bone Torso_COG_Control_JNT \
  --bone Torso_Chest_Control_Override_GRP --bone Torso_fppCamera_Control_GRP
```

Use the serialized rig matching the current graph. The result binds the input hash
to declared bone weights and explicit model-space rotation flags. Unlisted bones
have weight0; a valid excluded bone is a result, not a command failure. Output
contains counts and at most32 requested bones, never the full rig hierarchy.

The inspector supports declarative `treeBones` with descendant `subtreesToChange`
and `singleBones`. Nested subtree weights replace their parent subtree's weights;
same-weight overlaps are allowed. Conflicting sibling, top-level or single/tree
declarations, malformed hierarchies, unknown bones, invalid weights and nonempty
compiled `mask`/`maskRotMS` arrays fail explicitly. Do not guess native precedence
or claim support for a compiled-only mask from these declarations.

This establishes declared mask weights only. Trace which mask the current state
actually applies and inspect downstream constraints before choosing a carrier.
Sample native-readback motion after that composition at partial weights, including
camera, hand-to-gun and control transforms. Flags do not execute model-space
rotation handling. `activeMaskVerified` and `runtimeVerified` remain false.

Portable regression checks from the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_agent_workflow_tools.py' -v
```

Use a private owned native fixture for actual integration. Never publish extracted
game data, purchased models, private configs, logs with local asset content or
generated native outputs alongside these reusable tools.
