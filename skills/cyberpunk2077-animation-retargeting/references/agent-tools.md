# Agent workflow tools

Use these for repeated resource lookup, graph inspection and the established native
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

Portable regression checks from the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_agent_workflow_tools.py' -v
```

Use a private owned native fixture for actual integration. Never publish extracted
game data, purchased models, private configs, logs with local asset content or
generated native outputs alongside these reusable tools.
