# Native graph semantics: pinned Cyberpunk 2.5 branches

Researched 2026-11-02 by tracing new functions in the saved executable, not merely
reading field declarations. Use with [graph investigation](animation-graphs.md).
Executable SHA256:
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
All addresses below are preferred-image addresses, not portable hooks. Class
registration, constructor stores and instance vtables establish the operator
identities; constants and branch instructions establish the formulas.

These are scoped implementation findings and analyst numerical checks, not native
code execution or game observations. Use finite valid transforms, valid mask
indices and the identified branch. Recheck identities before applying them to a
different build. The focused references cover [capture and custom curves](native-capture-curves.md),
[feature durations](native-feature-duration.md), [clocks and inertia](native-clock-inertia.md),
[synchronization/events](native-synchronization.md) and
[shared-pose publication](native-shared-pose.md), followed by
[attachment and mesh skinning preparation](native-skinning.md). These equations and traces do
not implement a whole REDengine graph.

For actual Blend2/BlendMultiple/Override/DynamicMask caller policies, read
[named blend operators](native-blend-operators.md). Their endpoint, lifecycle,
event, missing-input and compiled-command paths differ even where a kernel is shared.

## Transform composition and interpolation

For translation xyz, quaternion xyzw and componentwise scale, define `C(X,Y)`:

```text
C.t = X.t + rotate(X.q, X.s * Y.t)
C.q = X.q * Y.q                  # Hamilton product, in this order
C.s = X.s * Y.s
```

Helper `0x14032911c` implements this QS composition. It does not introduce a
general shear representation. Quaternion multiplication and translation/scale
were cross-checked against independent SSE-lane transcriptions and numerical
examples, including noncommuting rotations.

Define `L(X,Y,w)` from `0x14032a460`: translation and scale lerp with `w`;
rotation uses helper `0x14032a664`. The quaternion helper flips the second
quaternion's signs when the dot product has its sign bit set, then uses the
absolute dot. For dot greater than float32(0.99), it normalizes the linear blend.
Otherwise it uses sine/angle SLERP weights. The exact stored threshold is
`0.9900000095367432`, not the often-assumed 0.9995. The sign-mask initializer and
acosf/sinf calls were traced. The normalization helper's zero-norm branch returns
zero lanes, not identity; this is not a valid-input substitute for validation.
These equations are not promises of bit-identical Python/native float behavior.

Ordinary transition blend helper `0x1408e3548` reaches this same `L` through
`0x1408e3a54`. Sparse body records interpolate when both inputs are present, copy
the sole present transform unchanged, and perform no value write when neither
is present. Presence bits matter; absent data is not universally an identity pose.

### Ordinary blend's keyed records

Helper `0x1408e35fc` separately merges the collections at pose-wrapper+0x18.
Records have stride0x70, exact64-bit key+0 and collection count+0x700; sixteen
records fit before that count. It builds a temporary collection before assigning
the output. Valid pointers/counts and merged capacity are preconditions; append
does not enforce capacity. This is separate from body, float and auxiliary QS.

It visits every A record in order, pairing it with the first equal-key B record
or copying it unmatched. It then appends each B record whose key is absent from
the temporary. Thus A duplicates remain; B-only duplicates keep their first
occurrence. No sorting or endpoint pruning occurs, even at w=0 or1. Both-empty
input sets output count0. Staging supports output equal to either input within
valid storage bounds; it does not establish arbitrary stack/byte alias safety.

For a matched record, five scalars at+0x50/+0x54/+0x58/+0x5c/+0x60 use ordinary
`(1-w)*A+w*B`; signed32+0x64 takes min and+0x68 takes max. Vec4+0x30 resets to
ones. Vec4+0x10, quaternion+0x20 and vec4+0x40 instead use separate factors from
the **original** coefficient pairs+0x50,+0x54,+0x58. Leaf `0x1403a6f1c` computes,
for finite ordinary inputs:

```text
s = a+b
if s < 2^-23: return w
r = 1/s
F = clamp((1-(1-w)*a)*(r*b) + (w*b)*(r*a), 0, 1)
```

Equality at the threshold uses the computed branch; the small-sum branch returns
w unclamped. This is not the usual normalized weighted-blend fraction. With
a=b=.5,w=.25, F=.375; a=b=1 gives clamped w. Vectors lerp all four lanes and the
quaternion adapter reaches the same `0x14032a664` interpolation kernel above.

An unmatched record preserves its copied fields except that **only +0x50/+0x54**
are multiplied by1-w (A-only) or w (B-only). It does not normalize the quaternion
or scale the other three scalars. Assignment copies key and+0x10..+0x6b, leaves
the two gaps untouched, and updates count without clearing old inactive records.
Matched vec4+0x30 initialization and inactive/gap preservation must not be lost
in an offline model. The record's application purpose and upstream capacity
guarantee remain unproved; do not label it an IK/event/root-motion payload from
its layout. Retained provenance: `blending-deep/ordinary-metadata-findings.md`,
saved direct callees and finite record/ordering checks. No native float parity
or runtime selection follows from these equations.

## Additive body transforms and weight history

BlendAdditive evaluator `0x1403a92e4` calculates:

```text
e = (instanceWeight - biasValue) * scaleValue
if abs(e) <= float32(0.01): evaluate base and record its named track; skip added pose
otherwise: w = clamp(e, 0, 1) for the ordinary transform kernels
Local: C(B, L(identity, A, w))
Ref:   L(B, C(A, B), w)
```

`B` and `A` are the evaluated base and added transforms. Full weight directly
composes `C(B,A)` for Local and `C(A,B)` for Ref. Their order differs; Ref does not
read a skeleton rest pose inside this helper and must not simply be called model
space. Clip animation type, sampler conversion, graph additive mode and the
[writer's bind-relative adapter](cyberpunk-animation-semantics.md) remain separate.

The magnitude gate occurs before the clamp: a negative value such as -0.5 enters
the composition route but clamps body weight to zero; 0.005 skips added evaluation.
Optional postprocess callbacks surround composition. Unmasked wrappers additionally
compose two auxiliary QS records at full weight. Their distinct storage and
lifetimes are traced in [shared-pose publication](native-shared-pose.md); do not
assign camera/root-motion names merely from this blend helper. A blanket rule
that every output is multiplied by `w` is unsupported.

For a useful discriminator, use B translation (1,2,3), rotation X90 degrees and
scale (2,3,4); A translation (5,6,7), rotation Y60 degrees and scale (0.5,1.5,2).
At w=0.5, Local translation is (6,-12,12), while Ref is approximately
(5.723076,5.5,6.283494). Their quaternion z components have opposite signs
(approximately +0.183013 versus -0.183013). Use noncommuting rotations to establish
quaternion multiplication order; nonunit scales and translations additionally
expose transform-order differences.

In the inspected masked kernels, `u=w*maskWeight` has no second clamp:
above float32(0.9999) use full composition; below float32(0.0001) skip the write;
otherwise use the same Local/Ref formulas with `u`. Equality takes interpolation.
Unlisted bones remain unwritten. Local checks signed indices against storage
bounds; no corresponding check was observed in the inspected Ref kernel. Valid
compiled-mask data is a precondition. Do not substitute these branches for the
separate BlendByMaskDynamic model-space-rotation path.

The named previous-frame track is concrete state, not just metadata. Evaluation
records the selected track from the base pose before evaluating the added pose.
A subsequent Update reads that stored value as current weight, bypassing
weightNode when the named track is configured. Missing/out-of-range lookup does
not write a new value, so initialization/history matters. Old/current effective
weight magnitudes crossing float32(0.01) trigger added-node activation/deactivation
and optional sync callbacks. The [synchronization reference](native-synchronization.md)
traces concrete receivers and ordinary sampler activation/re-entry. Those paths
must be identified before predicting a reset; the callback alone is insufficient.

Configured named-track history has an explicit default producer. During selected
node setup, BlendAdditive virtual+0x118 (`0x1403a8834 -> 0x14246565c`) copies
authored node+0x98 bits to the instance offset stored at node+0xd8. It does not
apply weight bias/scale/clamp there. A missing later track preserves that value
or the last successful capture. With no intervening callback/transfer writer,
default .75 stays .75 through a missing lookup; a later captured .2 stays .2
through subsequent missing lookups. Re-running setup writes .75; ordinary
activation `0x140586698` invokes weight update and consumes retained history.
Optional child/postprocess callbacks remain possible writers, so this is not
a global reset/no-reset claim. See [fresh/reused state](native-feature-duration.md#fresh-state-versus-reused-state).

## Float-track policies are independent

For ordinary dense tracks, with base `b`, added `a` and global body weight `w`:

| Policy | Dense result | Added-only sparse result in inspected helper |
| --- | --- | --- |
| BasePose | b | Unmasked Local additionally copies a; inspected Ref and masked Local wrappers only copy base |
| Interpolate | (1-w)b + wa | a, unchanged |
| Add | b + wa | wa |

For Interpolate/Add, both-present sparse channels use the dense formulas,
base-only channels retain base, and neither-present channels receive no value
write; presence propagates by OR. BasePose copies base storage regardless of
validity, with the Local exception above. With b=4, a=10, w=.25, dense results are
4, 5.5 and 6.5; added-only
Interpolate gives 10 while Add gives 2.5. Filling absent channels with zero loses
these differences. The Local BasePose exception disproves a universal claim that
BasePose never adopts added-only data.

The inspected masked Local Add route applies global `w` to float tracks, not
each bone's mask weight. Do not apply bone weights to all float tracks. Full
coverage of every masked wrapper and metadata segment is not claimed.

## Dynamic-mask hierarchy rotation

BlendByMaskDynamic evaluator `0x140b3bb94` has a separate special-index rotation
branch. Its wrapper `0x14032a57c` returns identity for index FFFF before reading
pose/context fields. Otherwise context byte+0xd9 selects direct record copy;
when zero it calls hierarchy kernel `0x14032adb0`. For valid finite transforms,
with N denoting quaternion normalization, that kernel computes:

```text
acc = pose[i]
p = parent[i]
while p != FFFF:
    P = pose[p]
    acc.t = P.t + rotate(N(P.q), P.s * acc.t)
    acc.q = P.q * acc.q
    acc.s = P.s * acc.s
    p = parent[p]
acc.q = N(acc.q)
```

Translation uses a normalized parent quaternion; the quaternion product uses its
original lanes. Final normalization also happens for a root with no parent.
Thus root q=(0,0,0,2) becomes (0,0,0,1), while the direct-copy branch retains 2.
The zero-length normalization mask yields zero quaternion, not identity. The
wrapper's FFFF identity has t=(0,0,0,1), q=(0,0,0,1), s=(1,1,1,1).
Hierarchy translation's fourth lane instead follows `P.t.w+P.s.w*acc.t.w`;
scale multiplies all four lanes. This QS walk is not a shear-preserving matrix
composition or an entity/world-placement operation.

The kernel reads neither range end, checks no cycle and has no initial sentinel
guard of its own. Valid nonnegative signed16 indices and terminating parents are
required. MOVSX to EAX followed by 64-bit addressing means non-sentinel 8000
becomes index0xffff8000, not a negative pointer offset. The mask caller's low16
bound check does not validate its full32 write index; malformed00010001 can name
bone1 for hierarchy reads but another output address. Do not hide this with an
analyst model's bounds/cycle guards or treat malformed assets as supported.

Let F be the wrapper above, O the current mutable output, A the second pose and M
the selected/interpolated F(O,i)/F(A,i). The special branch computes F(O,parent[i]),
uses `0x140327fc4` for its difference from M, and writes **only quaternion** to
O[i]. It skips a FFFF parent before these calls. Earlier mask entries can already
have changed O's parents, so later bones must read the current O, not a frozen
base snapshot. Translation and scale of O[i] remain unchanged on this branch.

Retained `shared-pose-deep/g2-hierarchy-findings.md` and its 44-instruction symbolic
replay check the hierarchy/sentinel bodies and noncommuting/nonunit examples.
These are code-derived equations, not native numerical parity. The separate
[named-operator chapter](native-blend-operators.md) closes mask fallback/update
and Blend2/BlendMultiple evaluator joins; this hierarchy branch alone must not
stand in for their distinct policies and producer/input preconditions.

## State selection and interruption

StateMachine candidate pass `0x1403aa5f0` establishes this branch-specific order:

1. When transition-active is zero, scan current-state outgoing transition indices
   first, then globals. During an active transition, skip that local list and
   scan globals.
2. Require enabled. Ordinary candidates require a condition returning true;
   forced candidates bypass that Boolean result requirement.
3. A forced candidate beats an ordinary winner regardless of priority. The first
   forced winner remains. Otherwise strictly higher **signed** priority wins;
   equal priority retains the earlier eligible candidate in runtime traversal.

Thus an eligible local20 beats global20 on a tie in this branch, while global200
beats local20. Forced-100 beats ordinary200. Two forced candidates retain the
first. This does not establish that every initialization path preserves serialized
array order. Conditional activation entries use a separate pass with the same
observed higher-priority/first-tie/forced selection, not an ordinary crossfade.

When a global transition interrupts, the inspected helper deactivates current
and in-flight target contributions, activates the designated frozen state and
uses a state-count sentinel as current. That is not simply restarting the original
source clip. The frozen pose is captured from **state-machine output**, not proven
final whole-graph/post-IK/render output. Its age depends on update/evaluate order.

The capture predicate considers enabled, non-inertial globals with positive
selected duration; otherwise it scans local `supportBlendFromPose` flags. That
local flag scan does not itself check enabled. A possible capture must not be
confused with a currently eligible transition.

## Duration, progress, curves and inertialization

Duration getter `0x1403aaea4` uses authored duration when no feature name is set;
otherwise it reads a registered feature-driven slot, with a separate out-of-action
slot. The [feature-duration trace](native-feature-duration.md) follows ordinary
refresh through first-matching action-database rows and the separate action-node
writer of outgoing duration/inertia slots. Serialized duration is not always the
effective duration. Start helper
`0x1405858e0` resets progress to zero and stores the selected duration.

For finite positive stored duration, update `0x1403aa174` computes:

```text
p = clamp(p + updateContext.scalar_at_0x08 / storedDuration, 0, 1)
```

Nonpositive duration sets p=1. The [clock trace](native-clock-inertia.md) follows
the registered animation update through Entity/Puppet dilation policies into
this scalar. Do not label it unscaled wall-clock delta or multiply it by a
sampler's speed. Candidate/completion handling
runs before this increment, with a 16-iteration bound. Consequently pose evaluation
can select the target at p=1 before a subsequent update commits its state index.
The completion path also honors a separate context force-complete byte and
propagates the target state's activation-frame transition guard.

If the selected inertialization request is true, the start branch stores crossfade
duration zero and requests downstream smoothing with at least the selected
duration. A zero state-machine crossfade does not prove zero visual smoothing;
the [inertialization solver](native-clock-inertia.md) instead uses two saved poses,
directional/rotational/scalar corrections and a quintic decay. Its activation
gates, history and later limits matter separately from state selection.

For the inspected Blend transition interpolator and 0<p<1:

| Mode | Weight |
| --- | --- |
| Linear | p |
| EaseIn | p³ |
| EaseOut | (p-1)³+1 |
| EaseInOut | 4p³ for p<.5; 4(p-1)³+1 otherwise |

At p=.25 these give .25, .015625, .578125 and .0625. Generic smoothstep gives
.15625 and is not the observed EaseInOut. At endpoints the evaluator directly
evaluates source or target; for interior progress it evaluates both then calls
the ordinary pose interpolation helper. Algebraic formulas describe scalar intent,
not reassociated float32 bit identity.

BlendFromPose also has stateful lifetime: activation resets elapsed; AlwaysOnActivation
requests capture, while RequestedByTag needs a matching tag. Deactivation releases
the stored pose. Update accumulates the context scalar and releases on completion.
During capture, it computes a per-record contribution through `0x140327fc4`;
evaluation later applies that saved contribution through the Local additive helper
with `1-shapedProgress` after evaluating the current input. This is not ordinary
lerp between two present-time samplers. The [capture and custom-curve reference](native-capture-curves.md)
gives the recovered equation, including its nonunit-scale counterexample. Do not
replace it with a mathematical inverse transform. The count-different conversion
helper copies corresponding segments and fills tails, without matching bone names
or converting coordinate spaces. The **capture caller** passes a newly allocated
temporary as source on that branch; its payload is not initialized by the traced
constructors. Do not conflate that scratch-data hazard with the later application
caller's correct saved-contribution source or claim it caused a particular asset
failure without observations. The capture reference gives the exact argument flow.

This node's Linear mode returns p; its Smoothstep mode uses
`clamp((3-2*p)*p*p,0,1)` for finite input, and CustomCurve dispatches to a separate
curve evaluator. At p=.25, Smoothstep gives .15625, unlike the ordinary transition
EaseInOut's .0625. The same reference traces Constant, Linear, quadratic/cubic
Bezier and Hermite custom kernels, key grouping, time clamping and stored tangents.
Do not substitute one node's curve for the other.

## Time warping and synchronization

The inspected BlendAdditive time-warp path obtains weighted contributor scalars,
sums them without dividing by total weight, then for finite nonzero sum `D`
computes `z=oldPhase+updateScalar/D`. Zero D gives zero increment. It stores old
phase, `fmod(z,1)` and `floor(z)`, then invokes node virtual `+0x108` with a generated
shared sync object. This
does not independently change state-transition duration or prove sampler-speed
coupling. [Synchronization and events](native-synchronization.md) traces the
generated method separately from configured ByProgress/ByEvent, concrete receiver
classes, tag/member aliasing, traversal-controlled writes/reads, normal re-entry,
loop handling and event delivery. There is no weight-based leader election in
the traced tagged path. These are defined branches, not universal rules for
unidentified nodes or all alternate scheduling paths.

A useful remaining discriminator records exact source/added sampler identities,
phase, weight history and sync callbacks across threshold crossing and re-entry.
Use a matching retained trace or authorized existing observation capability first.
Do not turn this missing integration evidence into a requirement for a new custom
observer on every animation task.

## Evidence and scope

Private research receipts live under `animation-graphs-research/transitions-deep`
and `animation-graphs-research/blending-deep` in the owning investigation workspace:
class/instance identity tables, exact-hash PE scans, bounded disassembly, raw
constant reads, branch notes and `equation-checks.json`. No game binaries or
disassembly are redistributed in this skill. Heavy jobs retained the shared lock,
memory/headroom/thread caps and deadlines; refused jobs were not treated as evidence.

These findings replace declaration-only uncertainty for the named branches.
The shared-pose trace establishes normal graph-chain publication and later skinning
submission; active graph topology determines which IK nodes precede an overlay.
Actual active graphs, alternate operator/cache paths, concrete downstream skinning
recipients, final rendering and visual/gameplay acceptance remain separate evidence.
