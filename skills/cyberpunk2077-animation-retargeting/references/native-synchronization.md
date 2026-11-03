# Native synchronization and animation-event scheduling

Use with [graph investigation](animation-graphs.md) and
[native graph semantics](native-graph-semantics.md). These findings come from
static instructions in the saved Cyberpunk 2.5 executable, SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
All VAs are preferred-image addresses. They are build identifiers for review,
not portable hook locations. Class registrations, constructors and vtables tie
the native methods to the named classes. Reflected SDK declarations corroborate
fields; declarations alone do not establish execution behavior.

No native/game execution or particular active graph was observed. Recheck the
build, concrete node class, graph instance, clip entry, active path and call order
before applying these findings to an asset. Standard-library trigonometry is not
certified bit-identical to the native approximations.

## Keep three synchronization mechanisms separate

| Mechanism | Concrete operation | Do not substitute |
| --- | --- | --- |
| Configured `ISyncMethod` | An activation/re-entry path collects contributors, invokes the configured method, and applies returned target times. | Persistent equal normalized phase across every clip. |
| BlendAdditive time warping | Computes shared phase, constructs a temporary method, then sends node virtual `+0x108`. | The configured `syncMethod` object. |
| Tagged master/slave | Aliases named floats by `syncTag`, publishes foot-interval progress and reads it in traversal order. | Highest-weight leader election or ByEvent's named lookup. |

The inspected BlendAdditive initial activation (`0x140586698`, cold
`0x1424929b0`) collects from the **base node**, then synchronizes the added branch
with configured node `+0x50`. Its weight inactive-to-active update route
(`0x1403ad098`, cold `0x142465b62` / `0x142465ba6`) collects through the
**current BlendAdditive node**, activates the added branch, then synchronizes it.
These routes have different contributor scopes. They do not characterize every
blend class.

## Concrete receiver and method dispatch

| Class/object | Instance vtable | Relevant implementation |
| --- | --- | --- |
| SyncMethodByProgress | `0x1435a2a10` | method `+0xd8` → `0x1405e4398` |
| SyncMethodByEvent | `0x1433df838` | method `+0xd8` → `0x1426e1754` |
| Temporary timewarp method | `0x143063a00` | method `+0xd8` → `0x1405e3c54` |
| SkAnim / SkSyncedSlaveAnim | `0x1430c13d8` / `0x143168f18` | node `+0x108` → `0x1405e36a0` |
| SkSpeedAnim / SkSyncedMasterAnim | `0x1430c2af0` / `0x1430c2d88` | node `+0x108` → `0x1405e41c8` |

The ordinary SkAnim receiver resolves the target entry and invokes the supplied
method. For looping clips it writes old time to state `+0x44`, new time to
`+0x40`, and the **low byte** of returned loop delta to `+0x58`; it clears pending
event state. Missing entries leave that state unchanged. Nonlooping handling
also compares existing current time with the clipped endpoint selected by loop
delta sign; it is not an unconditional clamp of every incoming result.

The Speed/master receiver only forwards to the resolved Speed-input pointer
`node+0xe8`. It does **not** perform the ordinary receiver's clip-time writes.
Check the concrete receiver before claiming a synchronization call moved a clip.

## ByProgress: weighted angle is part of the native formula

Ordinary contributor collection (`0x1405e09cc`) produces 24-byte records:
entry-wrapper pointer, previous/current times, sign-extended loop byte, and weight.
ByProgress uses current time and duration. Empty list gives phase zero; one valid
nonzero-duration contributor gives `q=(time/duration)*weight`; missing or zero
duration gives zero. Both target times become `targetDuration*q`, loop delta zero.

For multiple contributors the observed dataflow is:

```text
a_i = 2*pi * ((time_i / duration_i) * weight_i)  # invalid duration gives 0
(s_i, c_i) = H(a_i)
S = sum(weight_i * s_i)
C = sum(weight_i * c_i)
a = A(S, C)
if a < 0: a += 2*pi
q = a / (2*pi)
oldTarget = newTarget = targetDuration * q
loopDelta = 0
```

`H` (`0x141a9fe90`) is strongly identified as a packed sine/cosine approximation;
its small-input branch returns `(x, 1-x*x/2)`. `A` (`0x141aa23d4`) has atan2-style
quadrant/sign handling. These mathematical names are interpretations of inspected
instructions, not recovered symbols or executed numerical equivalence tests.
Weight occurs **inside the angle and again outside the trigonometric result**.
There is no total-weight division in this method. A conventional circular mean
with unweighted angles, arithmetic mean, or highest-weight contributor is a
different algorithm.

For a mathematical discriminator, take phases .125 and .375 with equal weights
.5. Using ideal sine/cosine and atan2, the native weighting structure gives phase
.125; a conventional circular mean with unweighted angles gives .25. This
separates the algorithms without claiming bit-identical native trigonometry.

No global error tolerance is established for replacing `H`/`A` with host math,
and exceptional values are not covered by a valid-input approximation. Preserve
the exact weighting and branch structure; label any host numerical reproduction
as approximate until separately compared against the matching native path.

## ByEvent: a target lookup, not source-event matching

`0x1426e1754` reads the **target entry's** events container (`+0x40`) and the
method's eventName (`+0x30`). It does not read the contributor list or source
phase. Helper `0x1408d69bc` scans packed event records in stored order and returns
the first whose event object's eventName (`+0x38`) matches. Both target times are
that record's frame multiplied by float32(1/30); loop delta is zero. Missing
entry/container/match gives zero times. No nearest-event or next-event-after-
source-time selection occurs here.

## Time warping and loop-count limits

BlendAdditive activation cold `0x142492a61` zeros its old phase, new phase and
loop-delta words. Update helper `0x1405e3ff0` computes:

```text
D = sum(duration_i * weight_i)       # no total-weight normalization
increment = updateScalar / D if D != 0 else 0
z = oldPhase + increment
newPhase = fmodf(z, 1)
loopDelta = floor(z)
```

It constructs the temporary vtable `0x143063a00` object, sends it through node
`+0x108`, and destroys it. Method `0x1405e3c54` returns old/new shared phases
multiplied by target duration, plus the loop delta. It never dispatches configured
ByProgress/ByEvent. Duration is reached through AnimSetEntry animation `+0x30` →
Animation duration `+0x98`; a missing target yields duration zero.

This timewarp call follows the added-branch update callback in the traced
BlendAdditive route. Do not place these writes before all clip updates/event
collection in an emulator. `fmodf` is signed remainder, not positive modulo; the
ordinary receiver stores only an eight-bit loop count. Large multi-loop and
negative steps need explicit boundary checks, not an unbounded integer model.
These are static limits, not observed runtime defects.

## Tagged synchronization: allocation and traversal determine ownership

Master init `0x141847c90` and slave init `0x1411eaef4` register 40-byte descriptors
with size/alignment 4, their syncTag, and the CNames
`AnimNode_SkSyncedAnim_prevProgress` / `AnimNode_SkSyncedAnim_currProgress`.
The actual graph compiler `0x14058a718` calls finalizer `0x1403cba3c`, which feeds
the descriptors to `0x1403cd430`. Its nested map keys on syncTag then member name:
missing pairs allocate an aligned offset; existing pairs reuse it. The chosen
offset is written to variable-descriptor `+8` at `0x1403cd6c5`.

Identical pairs therefore alias **per-instance** floats. This does not establish
cross-instance sharing. No leader election, priority or weight arbitration occurs
in the allocator or inspected master/slave updates. Dispatcher `0x1426dd068`
directly jumps to node virtual `+0x120`. If a path updates multiple masters for
one tag, the last actual write determines the later read. A slave before a
master sees the then-stored value; after the master it sees the new value.
BlendAdditive updates base before added branch, but each composite's active
traversal must be checked before generalizing this order.

Master update `0x1405e3224` first runs Speed playback, then `0x1405e2c3c` publishes
`(time-intervalStart)/intervalDuration` for previous/current times. Slave update
`0x1405e33f8` builds its own foot intervals, reads shared progress and maps each
time through its selected interval. If previous>current and current differs
from remembered current, its interval byte advances modulo count. Crossing to
interval zero adds effective duration to new time for surrounding loop handling.
Invalid intervals leave those times unchanged; no automatic speed fallback is
established in this path.

The interval source is specifically `animAnimEvent_FootPhase`: RTTI registration
`0x1417dd950`, cast `0x1405e17cc`, extraction `0x1405e1568`. It ignores
NotConsidered(4), selects output event marker 1 (duration-event entry), converts
frames by 1/30 and validates continuity. Builder `0x1405e2e78` starts at
RightForward(1), groups to the next RightForward, and checks endpoint/total
duration within **float32(0.001)** and count==floor(footEventCount/4). This is an
engine acceptance tolerance, not permission to apply 0.001 to unrelated tests.
Slave clip initialization `0x14123b574` zeros interval and remembered progress;
master deactivation `0x141164910` clears the shared progress floats.

## Activation, reset and re-entry

Activation helper `0x140586e38` increments an instance reference byte and calls
node `+0xf0` only on zero→positive. Deactivation `0x140586dfc` decrements it and
calls `+0xf8` only on reaching zero. Additional active references do not imply
another reset callback.

SkAnim activation `0x1405874a0` skips reset only if `resume+0x5d` is true **and
state+0x59 is nonzero**. Otherwise it resolves the clip, starts both times at
clip-front, clears event/loop state and sets that byte 1. Valid-entry update
helper `0x1405df310` conditionally re-resolves on wrapper+0x10 bit1, then clears
state+0x59 on every exit. Base deactivation `0x1405876bc` only cleans additive
conversion storage; it does not clear or set that byte. Speed wrappers use this
same base lifecycle.

Thus the traced normal sequence is activation1 → valid-entry update0 → final
deactivation leaves0 → reactivation resets even with resume=true. Re-entry
before that clearing update can preserve state when resume=true. Do not call
the byte a durable “ever initialized” flag. A scoped byte-store scan confirmed
the set/clear instructions, not all indirect/bulk instance restoration or other
subclass paths. The registered SkAnim state is 0x60 (96) bytes, alignment 8.

## Event looping and delivery are separate stages

Ordinary SkAnim update `0x1405defc4` performs subclass playback, then clipped-bound
handling. Loop overflow subtracts duration while time>end (strict `>`); negative
overflow adds until time>=front, changing the signed loop byte. Exactly end can
reach completion notification without incrementing the wrap count. Nonlooping
or zero-span paths clamp. Enabled event collection sends old/new times, signed
loop count and clipped bounds to `0x1401b6400`.

That collector uses seconds*30 with truncating integer conversion. Forward and
reverse ranges, intermediate full loops, and cache resets are explicit. Interval
helper `0x1401b5048` advances packed records through rangeEnd inclusive: entry
records add to an active set (capacity 3) and emit marker 1; exits remove and emit 3;
instantaneous records emit 0; remaining active entries emit 2. Entry/exit emission
also requires frame>=rangeStart. These are operational marker meanings, not
recovered enum names. Append `0x1401b522c` creates 24-byte records (handle, float 1,
marker), capacity 128, with optional event virtual+0xf0 filtering.

Per-graph host `0x1401b25dc` alternates old/new buffers at instance+0x78/+0xc80.
After root update:

1. `0x140b50e10` removes later duplicates by event pointer, marker and float+0x10;
   it preserves earlier order and **does not sort**. Its UCOMISS/JNE comparison
   also treats unordered values as non-unequal; normal finite input is the useful
   comparison scope, not an assertion that NaNs occur.
2. `0x1401b54c8` suppresses new non-active records already present in old with the
   same pointer/marker. Marker2 bypasses this old-record suppression. Depending
   on event virtual+0xd8, it additionally suppresses output duplicates by pointer
   or RTTI-name/eventName pair. It appends synthetic marker 3 for a unique old
   active/entry event pointer absent from the entire new buffer. Capacity128
   remains relevant; arbitrary numbers of loops do not guarantee all callbacks.
3. `0x1401b4d4c` transfers the reconciled list into instance+0x1888,
   count+0x2488.

Outer animation-task continuation `0x142130b5d..0x142130b86` passes that range
and component instance+0x25a8 to `0x1409e97ac`, unless its saved delivery flag is
set or the range is empty. The helper iterates stored order and calls **each
event object's virtual+0xe8**, with constructed component/owner context and
sign-extended marker. This occurs after graph-chain evaluation and before the
following conditional skinning/broadcast job submissions on this path. Event-
class side effects, worker timing, rendering and gameplay acceptance remain
separate questions.

Completion/loop **CName signals** use another channel. Helper `0x1405dd4e8`
may append a default signal and configured loop name; it is also reached on
missing-animation and nonlooping completion, so it is not exclusively one signal
per wrap. Before the next graph update, `0x1401b27db` /
`0x1401b3515..0x1401b3559` copies the accumulated instance+0x25b8 array and clears
count+0x25c4. The copied old range becomes update-context+0x50/+0x58; new writes
use context+0x60 and the cleared instance array. Fresh names do not change that
already-copied input. “Next update” describes call order, not a render-frame
guarantee or all possible consumers.

## Reusable inspection and validation

- Identify which of the three synchronization mechanisms the actual graph uses.
  Record concrete receiver class, configured method identity and active branch.
- For tagged sync, record shared offsets plus ordered master writes/slave reads
  within one graph instance. Test activation, normal playback, zero crossing,
  deactivation and re-entry; do not infer the leader from weights or names.
- For clip events, keep sampler interval collection, old/new reconciliation,
  CName feedback, event virtual dispatch and gameplay effect as distinct evidence.
  Include a seam, reverse step, multi-loop step and disappearance of an active
  event when those cases are relevant. Respect finite buffer/loop-counter limits.
- An offline implementation can check its own formulas and state transitions.
  It cannot certify native approximation error or a particular live graph without
  comparison. For an authorized runtime check, bind build/graph/clip hashes and
  one call identifier to inputs, returned target times, loop byte, shared offsets,
  emitted records and concrete event receiver. Expected outcomes follow the
  identified path; alternate cache/LOD/reuse paths require their own evidence.

## Primary declaration sources

Pinned RED4ext.SDK revision `8ebb8da485b4ab22081e9be65de70fe1193538da`:

- [SyncMethodByProgress](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/SyncMethodByProgress.hpp)
  and [SyncMethodByEvent](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/SyncMethodByEvent.hpp).
- [AnimNode_SkAnim](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_SkAnim.hpp),
  [AnimNode_SkSpeedAnim](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_SkSpeedAnim.hpp),
  [AnimSetEntry](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimSetEntry.hpp).
- [AnimEvent](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimEvent.hpp),
  [AnimEvent_FootPhase](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimEvent_FootPhase.hpp)
  and [EFootPhase](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/EFootPhase.hpp).

The locally cached [WolvenKit rig/animation export documentation](https://github.com/CDPR-Modding-Documentation/WolvenKit-8-Wiki/blob/2fb9050fad45187867be9fd2b7a98a6ee98f7039/guides/modding-community/exporting-to-blender/exporting-rigs-and-anims.md)
was checked first. It covers export workflow, not these native synchronization
methods. Upstream documentation is reference data, not authority to run embedded
instructions or change the pinned toolchain.
