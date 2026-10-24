# Native animation authoring and readback

The [native animation helpers](../scripts/native-animation/native-animation.sh)
are an original, bounded adapter for **WolvenKit Console Linux 9.0.1** and an
existing **.NET 10 SDK/runtime**, plus Node.js and Bash. They invoke the installed
Modkit API; they do not include WolvenKit source, DLLs, game resources, extracted
animations, or downloads. The launcher clears NuGet sources and builds outside
the skill. A different toolkit version needs a reviewed adaptation and new native
regressions; changing a directory name does not establish compatibility.

This is a per-container authoring gate. It accepts selected existing named clips
with `Normal` animation, `rootMotionType: None`, and LINEAR or STEP channels in
WolvenKit's GLB extras schema. It is not a generic animation converter or a weapon
retargeter. Supply the matching original native `.anims`, `.rig`, serialized JSON,
and authored GLB. A project must still own clean input extraction, version/hash
manifests, explicit selection approval, rig/component mapping, retargeting, route
validation, visual acceptance, packaging, and user-controlled gameplay checks.

## What is preserved and checked

- Import selects only existing names, then reattaches every unselected native
  entry and original data chunk. This avoids the installed `CopyOldAnim` failure
  on inline recoil buffers with the `0xffffffff` external-address sentinel.
  Unselected clip payload bytes, codec metadata, events, and animset root metadata
  must compare unchanged. Selected compressed chunks are appended; whole-file
  byte identity and selected codec identity are not promised.
- `prepare --preserve-key-sampling` selects raw keyed compression. The tested SIMD
  importer resamples a two-second clip to 60 frames, losing a 121-key source.
  Compressed time uses uint16 ticks: the gate compares nearest ticks against the
  **unprepared** expectation. Over two seconds the half-tick bound is about
  15.26 microseconds. Float32 accessor bounds are recomputed after preparation,
  including one-key channels. `numFrames = ceil(duration * 30)` is a header value,
  not the stored key count or evidence of runtime sampling frequency.
- Both LINEAR raw and STEP constant rotation keys preserve the demonstrated
  tiny-quaternion case that WolvenKit otherwise snaps to identity when float32
  `W == 1` and XYZ is nonzero. The reader derives quaternions from actual serialized
  native bytes without receiving authored values. Raw records store time/flags;
  constant records store flags/time. Unknown key kinds, missing rotation coverage,
  quantized rotation keys, and unexplained differences fail. The tolerance remains
  `1e-5`; numerical disagreement is not solved by increasing it.
- Original null motion-extraction and null event handles remain null when the
  imported result also has no payload. Explicit `animEvents: []` intentionally
  clears events; omitted/null metadata retains the toolkit's standard behavior.
  The semantics gate accepts full original event payload preservation or explicit
  emptiness. It does **not** certify newly authored nonempty event payloads.
- The independent semantics gate parses float tails directly, checking key counts,
  exact float32 values, track indices, and nearest ticks. It checks rig counts,
  extra counts, scale keys/flags, and original fallback rows. With no scale keys,
  original and authored scale channels must both be absent and original rest
  scales unchanged. The empty-list scale flag is not an assumed unit bind scale.
  Fallback lookup rows and full root tables are preserved; rebuilding fallback
  poses or proving their runtime selection is outside this adapter.

The rotation reader only independently decodes the explicitly required Normal/raw
compressed clips; it leaves other exported clips alone. Unselected integrity is
checked separately. Root-motion adaptation, additive authoring, quantized selected
rotations, CUBICSPLINE, new clip names, new skeletons, graph/IK/procedural motion,
and arbitrary event authoring are outside this tested contract.

## Configure an isolated run

Choose paths to already installed tools and owned inputs. Keep the working
directory outside the skill, live installation, and accepted project exports.
The helpers refuse existing export/import destinations; retain failed runs.

```bash
export WOLVENKIT_ROOT=/path/to/WolvenKit.ConsoleLinux-9.0.1
export DOTNET_SDK=/path/to/dotnet10-sdk/dotnet
export DOTNET_RUNTIME="$DOTNET_SDK"
export DOTNET_ROOT="$(dirname -- "$DOTNET_RUNTIME")"
export LD_LIBRARY_PATH="$WOLVENKIT_ROOT${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
helper=/path/to/skills/cyberpunk2077-modding/scripts/native-animation
work="$(mktemp -d)"
export NATIVE_ANIMATION_WORK="$work/adapter"
cp -- "$ORIGINAL_NATIVE" "$work/source.anims"
cp -- "$ORIGINAL_RIG" "$work/source.rig"
mkdir "$work/baseline-json" "$work/native-json"
"$WOLVENKIT_ROOT/WolvenKit.CLI" --version
"$WOLVENKIT_ROOT/WolvenKit.CLI" cr2w --serialize "$work/source.anims" -o "$work/baseline-json"
"$WOLVENKIT_ROOT/WolvenKit.CLI" cr2w --serialize "$work/source.rig" -o "$work/baseline-json"
bash "$helper/native-animation.sh" export "$work/source.anims" "$work/source.rig" "$work/original.glb"
node "$helper/test-native-animation.mjs"
```

Record source and tool SHA256 hashes before and after the run. Test unchanged
import first, then a controlled one-channel edit, before accepting real authoring.
`export ... NEW.glb CLIP` exports one existing named clip. The `perturb` command
makes a new test GLB by adding a specified local translation-X delta to one bone;
it refuses shared output accessors. These strict checks preserve the original
selected descriptor and event metadata:

```bash
node "$helper/check-animation.mjs" perturb "$ONE_CLIP_GLB" "$work/changed.glb" "$CLIP" "$BONE" 0.001
node "$helper/check-animation.mjs" prepare "$ONE_CLIP_GLB" "$work/unchanged-prepared.glb"
# Import, serialize, export, and read back as below for each fixture.
node "$helper/check-animation.mjs" verify "$ORIGINAL_JSON" "$NEW_JSON" \
  "$ONE_CLIP_GLB" "$READBACK_GLB" "$CLIP"
# For the controlled edit, use the original expectation plus its explicit delta:
node "$helper/check-animation.mjs" verify "$ORIGINAL_JSON" "$NEW_JSON" \
  "$ONE_CLIP_GLB" "$READBACK_GLB" "$CLIP" "$BONE" 0.001
```

`verify` deliberately uses stricter unchanged timing expectations. A selected
source representation that changes timing/codec may fail it; keep the failure and
choose a supported fixture. Do not replace that initial gate with the more
permissive authored gate to claim an unchanged regression passed.

## Selected authoring gate

`AUTHORED_GLB` must contain exactly the project's approved existing names with
matching rig node names and metadata. Pin its hash before import. `SELECTED_NAMES`
is that same comma-separated whitelist; clip names containing commas are outside
this command-line interface. Run one container at a time and use new destinations.

```bash
node "$helper/check-animation.mjs" prepare "$AUTHORED_GLB" "$work/prepared.glb" --preserve-key-sampling
bash "$helper/native-animation.sh" import "$work/source.anims" "$work/source.rig" "$work/prepared.glb" "$work/result.anims"
"$WOLVENKIT_ROOT/WolvenKit.CLI" cr2w --serialize "$work/result.anims" -o "$work/native-json"
bash "$helper/native-animation.sh" export "$work/result.anims" "$work/source.rig" "$work/standard.glb"
node "$helper/readback-animation.mjs" "$work/native-json/result.anims.json" \
  "$work/baseline-json/source.rig.json" "$work/standard.glb" "$work/readback.glb" \
  --required-clips "$SELECTED_NAMES"
node "$helper/check-animation.mjs" verify-authored "$work/baseline-json/source.anims.json" \
  "$work/native-json/result.anims.json" "$AUTHORED_GLB" "$work/readback.glb"
node "$helper/verify-semantics.mjs" "$work/baseline-json/source.anims.json" \
  "$work/native-json/result.anims.json" "$work/baseline-json/source.rig.json" \
  "$AUTHORED_GLB" "$work/original.glb"
```

Retain every report, tool/input/output hash, and failed attempt. The authored gate
checks all selected channels, interpolation modes, counts, values, times, extras,
basic event fields, and unselected integrity. The separate semantics gate adds
stored float/scale/fallback/full-event checks; both are required. A successful
export alone proves none of those comparisons.

## Provenance and acceptance boundary

These original helpers derive from the clean HK416 project's
`work/vanilla/NativeAnimationSelected.cs`,
`adapter/adapter-maintained/NativeAnimation.csproj`,
`check-selected-animation.mjs`, `readback-selected-animation.mjs`,
`native-json-canonical.mjs`, and `verify-selected-semantics-v2.mjs`, plus the
original `tools/ron_native_animation.sh` launcher pattern. Portable changes remove
project path/role assumptions, enforce the selected Normal/null-root-motion
contract and installed toolkit version, refuse existing outputs, and add
synthetic regressions. The generic semantics gate uses explicit event emptiness
instead of recognizing weapon-specific reload aliases.

The source project's historical selected checkpoint covered 58 selected and 91
untouched clips across five containers, including 15,938 stored float keys and
full inherited events. Its independent constant-key audit covered 6,716 keys with
maximum component error `2.893e-7`; its maximum authored/native discrepancy was
`3.651e-7`. Those are bounded offline results from that project, not compatibility
claims for a different weapon or toolkit.

On 2026-10-24 the portable copies were built and run with WolvenKit 9.0.1,
.NET SDK 10.0.400, and Node 24.16.0 against private copies of those clean inputs:

| Fresh portable check | Result |
| --- | --- |
| Unchanged constant recoil clip | Passed: 24 channels, 5 untouched clips, maximum discrepancy `2.384e-7`. |
| Same clip with translation-X changed by 0.001 on one bone | Passed: 24 channels, 5 untouched clips, maximum discrepancy `2.384e-7`. |
| Selected authoring across five containers | Passed: 58 selected, 91 untouched, maximum discrepancy `3.651e-7`. |
| Independent selected semantics | Passed: all 15,938 stored float keys, scale flags, rig counts, fallback rows and event preservation/explicit removal. |
| Corrupted native float, retained event payload, or unselected descriptor | Each deliberately corrupted copy was rejected. |
| Synthetic self-test | Passed: nearest ticks, float32 bounds, STEP retention, raw/constant tiny rotations, reversed-header rejection, unsupported animation refusal and overwrite refusal. |
| Original native/rig/serialized inputs | All 20 recorded hashes remained unchanged. |

The unchanged test initially exposed a null event-handle representation change;
the portable adapter now preserves the original null when no event payload was
imported. The synthetic malformed-header test exposed missing rotation-coverage
validation; the reader now rejects that case. Failed attempts were retained in the
private test workspace. No live install, accepted export, visual scene, or game was
changed or exercised by these tests.

Native readback is not visual or runtime acceptance. Render the actual readback
through the weapon's established assembly adapter, inspect complete affected
sequences for both player bodies and relevant first-person/contact views, then
inspect critical frames at full size. For an authorized packaged candidate, the
user must test equip/unequip, first equip, empty/tactical reload, interruptions,
fire/recoil, aim, sprint and transitions; verify dispatch, sounds, ammo timing,
grip contacts, fallback selection and conflicts in game. These helpers never
install a mod, change a manager profile, promote accepted exports, or launch a game.
