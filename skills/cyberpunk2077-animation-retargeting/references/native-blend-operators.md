# Named blend operators in the inspected Cyberpunk 2.5 build

Use this when the selected graph contains Blend2, BlendMultiple, BlendOverride
or BlendByMaskDynamic. Identify the actual node and current state before using
its formula. These operators share some kernels but differ in weight acquisition,
activation, events, missing inputs and output domains.

Evidence is static implementation research against saved EXE SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses below use preferred base0x140000000. Native registration/constructor
joins, retained instructions and independent finite discriminators support the
named paths; none establishes actual selected resources, native numerical parity
or gameplay. Pinned [SDK declarations](https://github.com/wopss/RED4ext.SDK/tree/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim)
corroborate names/layouts, not execution.

Read the common [QS, sparse-track and keyed-record contracts](native-graph-semantics.md)
and [synchronization methods](native-synchronization.md) only as needed.

## Blend2

Constructor140E757C8 binds primary1431291A8; update1408E2D30 and
evaluator1408E2C20 establish the typed route. For finite increasing authored
bounds a,b, remap1408E32C0 returns `(clamp(x,a,b)-a)/abs(b-a)`; equal or reversed
bounds return0. There is no Additive bias/scale/deadband. Missing scalar child
retains the stored weight in activation and update; reset140D60D94 clears it
and conditionally clears the12-byte time-warp phase state. A missing input is
not an every-frame reset.

Evaluation uses stored w without remapping: w<=0 evaluates first directly,
w>=1 second directly, and0<w<1 evaluates both then calls ordinary1408E3548.
Endpoints therefore bypass its keyed-record merge and interpolation. With masked
FP exceptions, a raw NaN through valid remap becomes1; a NaN already stored in
the evaluator takes its first-input branch. Do not conflate those entry paths.

Finite active children are first iff w<1, second iff w>0. Entering-child activation
precedes leaving-child deactivation. Children update first then second through
synchronous14207CC30 callbacks. Event factor is1 for first when w<.5, otherwise
for second; both children still update when their factor is0. The helper scales
only newly appended events, then each event's predicate decides removal. Zero
factor does not prove that every event is removed; exact.5 favors second.

## BlendMultiple

Constructor140DB4AE4 binds primary143108AC0; update1408E0EC0,
selector1408E1DB0 and evaluator140584574 form the typed route. Absent scalar
child supplies authored minWeight every refresh, unlike Blend2's retention.
Activation resets raw/fraction to0 and both selected indices toFFFFFFFF, then
acquires/selects again. Reset also conditionally clears phase state.

For sorted scalar values S and count n, n0 gives no selected indices and n1
selects only index0. The evaluator returns without writes for no selection;
this differs from a valid index whose resolved child pointer is null.

For finite n>=2 and valid storage/interval, let
`L=max(minWeight,S[0])`, `H=min(S[n-1],maxWeight)`.
Nonradial selection uses `v=clamp(x,L,H)`. Radial selection uses:

```text
if H-L == 0: v=L
else:
    r=fmodf(x-L,H-L)
    if r<0: r+=H
    v=r+L
```

The negative-remainder addition is **H**, not H-L. For L2,H6,x1 this produces7,
not conventional interval wrap5. x=H wraps toL for a nonzero positive interval.
The function then selects an ordinary adjacent interval; it does not explicitly
blend last and first poses across a seam.

Equality advances beyond each threshold. Let provisional adjacent indices i,j
have span d=S[j]-S[i]. For d<=0, u=1; otherwise r=(v-S[i])/d and:

```text
r < float32(.001): u=0
r > float32(.999): u=1
otherwise: u=clamp((r-float32(.001))*1.0020040273666382,0,1)
```

Both equalities use the arithmetic branch. Next c=floor((n-1)/2); if
`abs(i-c)>abs(j-c)`, swap i,j and set w=1-u, otherwise w=u. Ties retain order.
For S=[0,1,2],x=.25, the final order is1,0 with w approximately.750501.
Duplicates are retained; S=[0,0,1],x0 selects index1, not an average of duplicates.
Post-swap order affects callback order, event ties and keyed-record merging even
when ordinary pose arithmetic is equivalent under an operand swap.

Leaving old active indices deactivate before entering indices activate, with
cross-role checks to preserve an index that remains selected. This differs from
Blend2's entering-before-leaving order. Contributing children update first then
second; exact.5 gives the second **after** any center swap the full event factor.
Interior pose evaluation calls the same1408E3548 ordinary wrapper as Blend2.

Invoked setup14273996C swaps reversed finite authored bounds, then tails1427398C0
to copy source values48 into derived values58, sort them and resize pose links108. Assignment
replaces the logical count/content; spare capacity does not preserve an old prefix
or clear the inactive tail. For newCount>oldCount with enough existing capacity,
cold14245220A copies oldCount*4 bytes, then (newCount-oldCount)*4 bytes; the
common continuation stores newCount. Thus old2,new4 uses two8-byte copies.
Insertion for<=32 and the larger median-partition/heap paths compare floats and
preserve every32-bit payload and duplicate count. Finite ordered comparisons
give ascending values; larger equal-key order is not guaranteed. NaN behavior
and native MXCSR were not observed; subnormal numeric ordering assumes DAZ off
and completed comparisons. Bitwise assignment itself does not convert values.

The scalar sort does **not** permute retained pose links. Source[2,0,1] and
retained links[A,B,C] become values[0,1,2] with links still[A,B,C]. A surplus
link tail is destroyed and new links start as three zero QWORDs. Successful
allocation, readable arrays and valid counts remain required.

A successful admitted generic property-adapter write to an actual Multiple
source S calls S+38=14273996C, then this setup. This is conditional on the source
handle, selected class/path/type, associated-owner admission and successful
write result; it does not establish a particular editor/gameplay or load caller.
Other setup invocation paths remain separate. L>H or v<S[0] can produce an
invalidFFFFFFFF array index before the selector checks anything else. Actual
safe bounds/index/storage are preconditions.

## Contributor, sync and compiled-command distinctions

Both nodes' ordinary contributor query sends incoming weight P*(1-w) to first,
then P*w to second, with active-index/null guards and no missing-child
renormalization. P.8,w.25 gives.6/.2; a missing first still leaves second.2.
This is distinct from dominant event factors. The shared time-warp duration
sum is not normalized either: durations2/6 and P1,w.25 give3; with missing
first they give1.5, not6.

Deactivation visits eligible first, second, then scalar and resets stored
selection/conditional phase. Blend2 snapshots w before invoking scalar sync;
Multiple invokes scalar sync first, then reads w/i/j. A scalar callback that
changes shared selection can therefore alter which Multiple children sync,
while Blend2 uses its snapshot. Two links to the same child are not deduplicated.

Multiple's contributor method1408E1778 also has two explicit alternative query
pointers in the context reached through request+8. Context+188 takes precedence
over+190; the ordinary weighted-list path requires both null. Each alternative
recomputes indices/fraction from an external scalar sample, calls eligible
children with the original request, temporarily redirects query+8 to local
result storage, combines results, then restores the captured pointer. Use
[contributor and motion queries](native-motion-queries.md) for the actual local
constructors, caller-owned result buffers, success rules, SkAnim branch priority,
extraction, C180 clip-record contracts and the captured instance-context
construction. Actual instance selection and arbitrary child side effects remain
separate boundaries.

The compiler does bind this node into its configured provider+48 and persists
provider pointers in the16-byte array header addressed by graph+68. The initial
data pointer143060288 in that header is not a demonstrated vtable. The identified
MultiBlend provider primary1435A8128+E8 only looks up the first provider whose id
matches its parentId, then forwards to that parent's+E8 with its branch40 as the
fourth argument. Missing parent returns low byte1. This is a different interface
from the node's+100 query: it neither reads owner48 nor constructs188/190.
Owner binding and provider persistence alone are insufficient to identify a
query context. The query chapter now traces its actual construction: a separate
K stores `[G68]` at K0 and is moved into instance38. This connects the header
to the ordinal query wrappers; final accumulated first-auxiliary application
remains separate.

* Query+188 samples array[index+3]. Its result contains QS+10, floats0/40/44
  and byte48: interpolate QS/floats and OR the byte. Missing child results use
  the explicit local defaults. This is not a full ordinary pose wrapper.
  SkAnim also writes turn-tag bits at result49; this Multiple combiner reads
  and writes only byte48. Its local writes leave caller49 unchanged under
  stable pointers and no independent callback alias writes. Clearing child
  temporary49 does not initialize caller49; see the query chapter's footprint.
* Query+190 samples array[index]. With query.byte14 nonzero, interior combination
  interpolates scalar0, builds a two-reference tail, and combines a fixed record
  list. It copies the dominant list (first at w<=.5), interpolates duration d,
  then multiplies each chosen record's first three floats by d/chosenDuration.
  Equal positive counts and matching per-record tag bytes are required for list
  validity. A tag mismatch returns false **after** rescaling that record;
  preceding/current writes remain. Zero durations have no division guard here.
  Endpoint outer branches directly copy the selected result instead.
* With query.byte14 zero, byte15 selects i or j. An unmatched choice writes
  nothing. The selected payload/scalar/duration is copied unchanged, while its
  reference tail can blend with the other child. Even w1 preserves the chosen
  payload but copies the other tail and combines validity. Do not substitute
  generic whole-record interpolation or the duration-rescaling mode.

The tail contains the first reference from each input tail plus w; pointer
validity depends on the endpoint/interior weight, not deep reference validity.
Its two count bytes come from selected FootPhase event records: 8-bit count,
right shift3, then max1. Null reference/inner handle defaults1. These bytes are
not generic booleans or automatically a count of distinct footsteps. Fixed
record capacity32 and valid source/query storage remain preconditions.

Compiled command142745284 resolves top/previous pose-storage views and calls
142741DF8 to blend body then floats, pops one entry and consumes4 payload bytes.
It does **not** call the ordinary wrapper's keyed-record or auxiliary-QS blend.
Outer compiled output initialization is separate; do not claim complete ordinary
versus compiled wrapper parity from this command alone.

## Ordinary output and missing selected children

The ordinary1408E3548 wrapper handles sparse tracks/body with presence OR:
both-present interpolate, sole-present copy unchanged, neither writes no value.
It processes keyed112-byte records using the separate matched/unmatched rules,
then interpolates **both** auxiliary QS records. Its finite flag rule is
`(A.flag && w<1)||(B.flag && w>0)`. This is not full-weight additive composition.

Missing child at a valid index calls reference or identity body/track fill and
explicitly writes identity only to the first auxiliary. It does not itself reset
the second auxiliary, keyed records or flag. The direct output therefore retains
those caller-supplied fields. The interior second-child temporary is different:
constructor1403A95BC explicitly initializes both auxiliary translations/quaternions
to(0,0,0,1), scales to ones, keyed count0 and flagfalse. Its missing-child branch
overwrites first translation with four zeros; the **second translation.w stays1**.
For incoming second T=(8,0,0,9), missing second child and w.25, ordinary interpolation
gives(6,0,0,7), not a result based on second T.w0.

Reference fill1403B1D5C clamps the body copy count to its stated rig/pose minimum,
but its float-copy count is rig-derived without a destination-count clamp in that
body. Identity fill1403B0E9C also resets the described validity ranges. Valid rig,
storage, layout and metadata capacity are required; a temporary constructor does
not initialize its arena body/track payload before these fills or child writes.

## BlendOverride

Primary143111FF8 binds setup1403A86BC, update1403AD2CC and
evaluator1403AC248. Update visits base then scalar, refreshes stored old/new w
using `MINSS(MAXSS(value,0),1)` (absent scalar0), performs crossing callbacks, then
updates override iff w>float32(.01). Exact.01 is inactive. Normal active override
events receive factor1, not pose weight w. Optional postprocess runs afterward
even when inactive. Setup clears weights and conditional phase; deactivation
visits base/scalar/active override and clears weights.

Built-in evaluator order is base/fill, optional postprocess, override temporary/fill,
optional blend method, selected bones, tracks, optional postprocess, cleanup.
Configured methods can change inputs/results at those exact boundaries. For
each configured bone in order, resolve a signed16 index, check both pose counts,
and let u=w*recordMultiplier: u<=0 skips, u==1 copies48bytes, other positive u uses
ordinary QS interpolation **without a per-record clamp**. Repeated descriptors
operate on the already modified output.

`blendAllTracks` takes precedence and uses common dense/sparse track blending.
Otherwise numeric mode1 does `current=(1-u)*current+u*second`; mode2 does
`current+=u*second`; other modes write none. Selected-track loops check the output
count but show neither a second-buffer bound nor a sparse-presence update or
positive-u gate. With current2,second4,w.5,multiplier1, two duplicate records give
mode1=3.5 and mode2=6. Global weight clamping does not prevent multiplier-driven
extrapolation. Do not apply the bone skip/copy policy to these tracks.

Name0 returnsFFFF; a cached non-FFFF index returns directly. CachedFFFF searches
two distinct name ranges, adds the corresponding16-bit segment offsets and
returns the first matching index without updating the cache. A missing name does
not imply a useful cached value. Valid signed-index encoding remains required.

Time-warp contributor collection forwards base only; sync forwarding visits
scalar, base, then active override. Optional blendMethod can register a command;
callback1427446A8 obtains the registered index/weight list and uses140EF204C to
blend selected bones from the top stack pose into the preceding one, then pops
one entry. Its weight is w*recordWeight and its index bound is the minimum body
count. Do not assume both this command and normal evaluator run on the same pose.

The reflected `getDeltaMotionFromOverride` byte+48 has constructed flags18B004001,
with serialization bit3 and indirect-address bit21 clear. Generic property access
is possible, but a semantic consumer is still unidentified. The actual+100 method
forwards base only regardless of that byte. The remaining small concrete entries
also add no byte48 read: two leaves return AL=0/1 (not all of RAX), slot+A8
forwards to the typed table's type getter at+8, and slot+110 clears the state byte
indexed by node+38 and sets the supplied output byte. These exact-body negatives
do not make the property globally unused. Configured blend/postprocess/sync
subclasses and external property visitors remain selected implementation boundaries.
Retained provenance: `override-consumer` and its independent leaf/table review.

## BlendByMaskDynamic

Primary1431A90E0 binds update1408E236C, refresh1408E2490 and
evaluator140B3BB94. Update visits base then scalar, clamps scalar as above
(absent0), gets the integer selector (absent-1), and performs weight crossings.
It does not directly call the selector's update callback on this normal path;
it does call its getter. Activation/deactivation visit base, selector, scalar.

Overlay activation/crossing/sync depends on w>float32(.01), without selector
validity checks. Overlay update/evaluation also requires0<=selector<maskCount.
Thus old0→w.5 with selector-1 can activate/synchronize overlay while suppressing
its update/pose. A later valid selector at unchanged active weight starts pose
use without another crossing. A valid index whose mask name misses still evaluates
both children before returning; an invalid index rejects before overlay evaluation.
Overlay events receive factor1. Reset clears weights and selector=-1; deactivation
clears weights but retains selector. Contributor collection uses base only;
sync visits scalar, base, active overlay, not selector.

For an ordinary local record u=w*maskWeight: u<float32(.0001) preserves the full
record; both threshold equalities through float32(.9999) interpolate; u>.9999
copies the second record. Effective1.5 copies here, while Override interpolates
with1.5. The low branch's cold body is a self-copy, not a zero/reference write.
Missing base or overlay takes the common fill policy, so missing overlay with a
valid mask can blend toward reference/default rather than simply skip.

The special hierarchy-rotation branch uses the
[mutable parent contract](native-graph-semantics.md#dynamic-mask-hierarchy-rotation)
and writes only quaternion; current translation/scale remain. Signed-low16 checks
versus fullDWORD write indices and ordered special-list traversal retain valid
index/storage/order preconditions. The typed
[RigPart compiler](native-rig-mask-compilation.md) establishes first-insertion
precedence, signed-index sorting and independent special-list membership. It does
not guarantee the special-list subset that this cursor requires, or clear the
rig name map on every repeated compilation. Preserve those exact premises.

## Evidence limits

Retained private reports `blend2-findings`, `blendmultiple-findings`,
`ordinary-temporary-defaults`, `g2-override-findings` and
`g2-dynamic-mask-findings`, `g2-blend-routing-findings`,
`blendmultiple-producer-findings`, `motion-query-provider-followup` and
`g1-property-adapter-findings` carry exact captures, guard receipts, equations and
review scopes. These finite algorithms are useful for reproducing a selected
graph call; they are not a universal simulator for arbitrary children, compiled
commands, resource producers or malformed inputs. Identify actual selected
subtypes/data and verify the affected final motion separately.
