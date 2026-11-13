# Weapon retargeting: execution playbook

Use this when starting a weapon port or repairing its hands, motion or transitions.
It is detailed where mistakes destroyed useful work in the BF6 MP5 case. It is not
a universal converter, a command to reopen accepted work, or a requirement to load
all other references. See the [MP5 case](bf6-mp5-success.md) for measured examples.

## 1. Establish the actual starting point

Read the current project handoff and inspect the actual owning files. Record:

| Identity | Minimum information |
| --- | --- |
| Source | Game/build, rig, geometry, arm/weapon clip pair, original clocks, events and missing layers |
| Target | Body/rig, native rest and inverse binds, weapon/prop components and container |
| Current accepted work | Native/package hashes, accepted clips/poses, review scope and user confirmation |
| Toolchain | Executable/library versions and working commands; known codec/adapter limits |
| Next change | Specific clip/channels/window or native fault; protected data and expected visible result |

Do not choose the newest-looking filename as the baseline. Keep the current cumulative
candidate distinct from a donor or importer baseline. Keep failed artifacts read-only
as regression inputs. Use a fresh output directory and the user's project location.
For a new source route, take one connected action through all applicable gates first.
For a proven route, batch compatible changes without repeating approval per clip.

## 2. Reconstruct a truthful connected preview

Load the real source assembly and native target skin, rig, receiver, magazine and
moving parts. Identify every component parent, slot, local offset, rig root and
inverse-bind owner. Prove source arm/weapon clock pairing and visibility phases.
A name such as `mag_plug` is a clue to investigate, not permission to zero its transform.
Apply mounts once. Include controls and downstream constraints actually supported by
the preview; label absent source/runtime layers and customized-body differences.

Use the [finger checkpoint](../../cyberpunk2077-modding/references/animation-retargeting/finger-checkpoint.md)
before motion transfer. Compare target/source palm frames, digit directions, signed
bends, twist, skin weights and posed surfaces. A straight reference finger transferred
as deltas can remain wrong even if it follows the source's changing bend perfectly.
Do not mix animator-control rests with mesh inverse binds. Preserve native lengths.

For source playback or Neto handoff, use the relevant adapter/calibration reference.
Neto's reference rotations and a successful inverse-LBS reconstruction do not establish
full-motion contact or authorize different native bone lengths.

## 3. Locate the failure before changing data

Capture just before, at and after the reported moment using the actual native readback.
Verify the timestamp against the preview schedule; a deliberately inserted review hold
is not evidence of a game breathing delay. Use the same camera/weapon framing across
before/after views. Never anchor a comparison camera to a finger being edited.

| Symptom | First discriminator |
| --- | --- |
| Hand/arm snaps after an otherwise correct reload | Compare complete outgoing/incoming poses and active bases; both arms, all digits, controls and skin |
| Stable wrist but wrong silhouette | Compare elbow planes, arm axial rotation, palm/finger rotations and deformed mesh |
| Grip improves but walking/breathing breaks | Compose old additives with the new base; test re-encoded offsets and partial weights |
| Fingers clip during magazine manipulation | Separate phase ownership, pad/contact surfaces, penetration and self-clearance; preserve seated prop alignment |
| Prop appears to drift from a hand | Check constant mount/calibration offsets and native parent hierarchy before editing tracks |
| Blender looks right, game fails on equip | Compare native byte layout/order/counts/addresses and actual package; do not keep rotating fingers |
| Hip reload works but ADS reload does not | Trace selected ADS script/state/graph/bank/visibility separately; pose acceptance cannot prove that route |

Do not leap to graph research when the same defect is already visible in decoded clip
playback. Conversely, a plausible single clip cannot certify graph selection or final IK.
After two failed corrections at the same gate, use the [failure ledger](failure-ledger.md)
and an actual discriminator rather than a third nearby offset.

## 4. Define the approved pose and every route that can restore another pose

Build a small reference matrix by body, weapon stance and clip role. It must identify
the exact native clip/time or evaluated pose the user accepts. The containing bank name
alone may not identify the right hip/ADS reference for each static clip.

Inventory static shoulder/ADS bases, idle break, safe/friendly holds, equip/unequip,
locomotion starts/holds/stops, sprint/slide/vault, fire returns, inspect, melee and every
reload alias actually present. Include graph/procedural contributors where relevant.
For each entry record held versus manipulating hands, additive base, intended reference
and preservation requirements. Do not rely on broad substring matching for another weapon.

A complete grip includes both arms, wrists/palms, metacarpals, every finger and thumb,
and the evaluated skin. Do not accept a wrist-only or elbow-only boundary check.
If the user asks to eliminate a pose, prove removal from each identified authored path;
keep external/procedural paths explicitly unresolved until traced. Never claim global
impossibility from a finite authored-bank inventory.

## 5. Correct the smallest anatomical scope

For a held pose, use measured rotations from the approved reference. For moving arms,
retain the hand/weapon trajectory while correcting the elbow plane if that is the
measured defect. With column-vector chain transforms `A`, `F`, `H`, one bounded swivel
can preserve the hand using `H_new = inverse(A_new * F) * (A * F * H)`.
Derive the swivel from the current rig/reference, retain translations/scales/lengths,
and verify the reconstructed hand transform. This formula does not choose a good pole
or prove natural anatomy: inspect clavicle, shoulder, elbow, wrist and skin together.

For fingers, select the smallest justified joints and motion window. Preserve useful
PIP/DIP curl and thumb opposition when a metacarpal/base adjustment suffices. Check
neighboring digits, palm and wrist after each correction. Better collision counts can
still hide implausible articulation or a finger embedded in a hollow prop.

Copy an alias only after proving compatible rests, source action, clock, trajectories
and channel semantics. Do not overwrite all manipulating-hand rotations with the held grip.

## 6. Rebase dependent motion instead of retaining stale offsets

Changing a Normal base changes the meaning of its additive offsets. For each affected
additive, identify the actual base and composition policy, evaluate the old motion,
construct the desired corrected pose, then encode offsets relative to the new base.
Compose the result again and compare it with the desired pose. Reconstruct child locals
from updated destination parents. Check noncommuting rotations, not just Euler numbers.

Preserve anatomical Normal translations/scales. Encoded additive translation offsets
may need to change to preserve the same evaluated wrist/weapon contact; do not prohibit
that legitimate re-encoding. Test full and intermediate blend weights, source/native keys,
between-key samples and state transitions. Label an offline composition hypothesis as
such; it is not every possible engine blend or constraint state.

## 7. Preserve manipulation phases and the original clock

Partition extraction, held manipulation, insertion, release and return using actual
source/native events, visibility and geometry. Keep the seated magazine fixed unless
its placement is itself wrong. Check hand-relative prop motion with all constant offsets.
Do not compensate a wrong mount by moving the whole prop animation.

Blend small corrections in/out only in justified departure/return windows. Preserve
approved middle-phase records, other digits, hand/weapon controls, events and timing.
Check self-contact and weapon contact separately. Triangle-intersection pair totals are
not penetration depth or visual approval; deeply embedded geometry may also evade a
surface-crossing test. Use signed/inside tests or representative surface inspection
where the failure demands it.

Retain original sparse keys, holds and endpoints. Additional samples must survive native
time quantization without collapsing onto existing times. Choose cadence from actual
between-key errors and codec resolution, not a universal 60/120/480 Hz rule. A midpoint
failure in both authored and native playback is an interpolation problem, not necessarily
serialization corruption. Do not stretch native anatomy to absorb source anchor travel.

## 8. Pass the native gate before trusting the preview

Use the existing [native command contract](../../cyberpunk2077-modding/references/native-animation-authoring.md)
and [native readback](native-readback.md), with fresh outputs and the version-matched
container/rig. Preserve the unprepared authoring expectation. Do not introduce a new
writer because JSON editing looks easier.

For supported compressed buffers, the shared audit checks dynamic key order and bounds:

```sh
node "$SKILLS/cyberpunk2077-modding/scripts/native-animation/audit-compressed-keys.mjs" "$NATIVE_JSON"
```

Here `SKILLS` is the verified sibling-skills directory and `NATIVE_JSON` is freshly
serialized actual native output, not a stale authoring sidecar. Inspect report scope
and nonzero failures. Unsupported data stays unverified; do not call it a pass.

For the inspected WolvenKit 9.0.1 compressed writer, quantized/raw records are ordered
by **bone, time, key type** (position, rotation, scale), separately per section.
Grouping all translations before all rotations is not equivalent. An order-independent
decoder and an unordered multiset check can both pass malformed output. Do not silently
sort the input in a validator and then report that the stored order was valid.

Check exact protected per-channel sequences, constants and float tails, declared counts,
addresses, lengths, flags, animation types, motion extraction, events and fallback data.
Independently read actual bytes, including tiny quaternions that another exporter may snap.
Compare all previously approved cumulative clips after merging, not only the current edit.

## 9. Verify motion, skin and state boundaries independently

Use actual final readback on the complete native assembly. Check the full relevant
clock, endpoints, holds, interpolation and transitions for every affected alias/variant.
Measure both complete arm/digit chains and evaluated skin in world and camera space.
Check normals separately when the surface looks wrong despite matching vertices.
Retain the original visibly bad join as a negative control: the new test must catch it.

Then actually inspect continuous source/native playback at normal speed and slow/scrub
fast contacts. Use first-person plus complementary side, palm/underside, hidden-area
and close views. State which variants/views were inspected and which remain open.
Rendered-but-unwatched video or sparse sheets do not become a full-motion pass.
Follow [visual acceptance](visual-acceptance.md) and respect explicitly accepted exceptions.

## 10. Preserve approved motion through repairs and packaging

For a serialization-only repair, prefer a bounded record permutation over reauthoring
poses. Prove every raw key/value/time and per-channel sequence is unchanged, constants,
float tails and all other metadata are exact, and decoded motion matches the reviewed
input. Keep the failed package as a negative control. Renew visual review for changed
motion or relevant assembly/skin/evaluation inputs; reuse demonstrated unchanged evidence.

Pack into a fresh archive, re-extract it, hash every resource and reserialize/check the
shipped animation banks. Verify the intended effective profile/override. Use existing
authorization for the concrete installation. Replace only intended files while the game
is closed if it loads these resources; a mod-manager restart is not automatically needed.
Keep a verified rollback artifact, but do not make an old rejected grip the final solution
when the user requested repair of the approved pose.

## 11. Record the actual acceptance and leave an actionable handoff

Ask for the smallest remaining runtime discriminator: equip/idle first after an equip
regression, then affected transitions/actions. A user gameplay pass belongs to the exact
archive and tested scope. ADS aiming is not ADS reload; one body is not every body.
Keep minor accepted clipping, deferred routes and untested combinations explicit.
Do not edit successful motion to satisfy an expanded assistant checklist.

Leave the next agent: current accepted hash and files; source/tool/rig identities;
reference matrix and protected channels; safe reproduction commands; rejected scripts
and negative controls; passed native/package checks; preview identities and actual
review scope; user confirmation and exceptions; and one bounded next task.
The [MP5 case](bf6-mp5-success.md) shows this distinction in a completed user-tested port.
