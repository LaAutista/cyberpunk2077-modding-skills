# Contributor collection and motion queries

Use this chapter when tracing AnimNode virtual `+0x100`, its request/result
storage, or a discrepancy between ordinary clip weights and extracted motion.
These are static findings for Cyberpunk 2077 2.5, saved EXE SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses use preferred image base `0x140000000`; re-establish identity and
type/table correspondence on another build. Analyst examples do not execute
the native implementation or establish gameplay, numerical parity or reachability.

Sections: [collection](#identify-the-collection-before-interpreting-its-fields),
[query construction and buffers](#query-construction-selection-and-caller-buffers),
[policy dispatch and scheduling](#movement-policy-dispatch-cached-delta-and-stage-order),
[interval extraction](#c188-interval-extraction-and-selected-result-writes),
[full-clip records](#c180-full-clip-records-events-and-cleanup),
and [evidence/open links](#evidence-and-open-links).

## Identify the collection before interpreting its fields

Let R be the collection request and C=`pointer[R+8]`. C is separate contributor
storage, not the graph update context. In time-warp update `0x1405E3FF0`, C is
local stack storage; count at C+168 starts zero, 16 context bytes are copied to
C+170, and pointers C+180/C+188/C+190 start null. Eleven retained activation,
crossing and transition producers use the same initialization. They establish
ordinary collection on those paths, not global absence of optional queries.
Offsets in this chapter are hexadecimal unless otherwise stated.

Ordinary SkAnim `0x1405E09CC` appends 24-byte records: wrapper pointer at 0,
previous/current time at 8/C, sign-extended loop byte as DWORD at 10, request
weight at 14. Count is at C+168. The prefix physically fits 15 records, but
this writer has no local capacity check; do not infer upstream admission.
Time-warp reads these records to sum duration times weight and later supplies
the same C to virtual +108 synchronization.

After successful entry resolution, the concrete SkAnim branch priority is
C+188, then C+190, then C+180, then ordinary append. The optional branches
bypass ordinary record construction. Multiple has its own +188/+190 routing;
use [named operators](native-blend-operators.md) for its selection, redirection
and C190 combination contracts. An identical vtable slot on an untyped object
does not establish this request interface.

## Query construction, selection and caller buffers

Distinguish the local request from its external result buffer. Actual helpers
`0x140820D04` (C188) and `0x1408E167C` (C190) receive `(P,I,X,U,V,b)`.
Each creates stack-local R, C and Q, initializes C.count168 and C170..17F to
zero, sets only its selected optional pointer, and calls
`[P+48].virtual100(node,R,I)`. R contains X, C, weight1 and byte b; Q contains
U, V and DWORD10=0. C190 also sets Q.byte14/15 from P.virtualD8/E0. For the
constructor-validated MultiBlend provider those methods return low bytes1/0;
re-establish the actual provider type before transferring that result.

Neither helper initializes V. Their return rules differ:

| Query | Return after child call |
| --- | --- |
| C188 | byte V48 verbatim, including noncanonical nonzero values |
| C190 | canonical1 iff byte V228 and DWORD V204 are both nonzero; otherwise0 |

V228 alone does not establish C190 success. A no-write child can leave old
caller bytes intact; neither rule certifies that this invocation wrote them.
Track the actual caller's initialization, repeated calls and later stores.
For example, under the explicit premise of a no-write child, C188 V48=7
returns7. After a preceding call stored marker1 and scalar9, the same premise
leaves both values. This is a conditional store-history discriminator, not an
observed game defect or proof that this child/configuration is reachable.

Wrappers `0x140820CCC` and `0x1408E1644` receive `(K,index,U,V)` and select
P from `[[[K]+0] + 8*zero_extend_u32(index)]`; they pass `[K+8]`, `[K+10]`
and byte K18 to the helper. This is an array ordinal, not an ID lookup. The
wrappers do not check index bounds/null pointers or clear V. Selector
`0x1408E0C9C` scans the signed-positive H.countC at H=`[K]`, matches entry38
and entry3C against the requested type/action, then applies the parent's
virtualE8 gate when parent lookup finds one. It returns the first admitted
ordinal, or FFFFFFFF. Provider ID matching belongs to that separate parent
lookup. Array stability, callback effects and valid storage remain premises.

Concrete caller `0x14082071C` reads K from owner A1C0 and issues14 C188 queries.
It initializes a local V once per index group and tests each returned AL before
storing V40 or translation-Y V14 into A. The first three groups reuse V across
multiple samples without clearing V48/V49 between calls. A later threshold
policy clears selected owner scalars; it is not a generic per-query reset.
The owner constructor initializes A+B0..E4 to positive infinity and indices
to FFFFFFFF. A failed query therefore need not mean a zero owner value.

Several C190 callers also consume duration, event and clip fields. `0x1408DF108`
and `0x1408E0A08` test query AL; `0x1408DFFD4`, the selected `0x1403B77CC`
path and both `0x140CE3F3C` query sites continue without testing it. Inspect
the named caller before treating the helper's return as an enforced guard.
The first of those unchecked callers also has no local FFFFFFFF index rejection.
This establishes a validity premise, not an observed crash.

Constructor `0x1406EF184` installs owner table `0x1430756B8`; its slot80 is
`0x1402D34DC`. The actual binding path calls that slot, which obtains K through
`0x1402D3850`, stores K in A1C0 and initializes16 selector ordinals. The
positive context lookup path reaches an entAnimatedComponent, reads its270
pointee I, then I38. Rejected attachments advance through the captured cold
continuation; a successful component cast with null I instead returns null.
The lookup is not a search for the first nonnull K. Valid suffix bounds remain
an upstream premise. These buffers are not automatically O30.

### Instance construction connects the provider header

On the captured setup path `0x14212DED0`, factory `0x14022397C` creates a fresh
instance I and its result replaces component270. The complete constructor
`0x1402239D8` explicitly zeros I20, I28 and I38. Setup `0x140222AD4` resolves
G from the component's graph ref, writes G to I20 and the component to I25A8,
then prepares instance state at I28. Its nonnull-G branch calls `0x140222EB8`
and moves the resulting context into I38 through `0x140223BB0`:

| Context field | Value on this construction path |
| --- | --- |
| K0 | H=`[G+68]`, the provider-array header |
| K8 | state=`[I+28]` |
| K10 | X=`I+2548`, the address of embedded context storage |
| byte K18 | 1 |

G and state are reloaded after graph initialization, immediately before K
construction. Do not substitute an earlier predicate's resource for that later
snapshot. Joining the outer caller's fresh allocation to these stores assumes
stable owner/component/instance identity across delegated calls.

K is a separate32-byte allocation: **K differs from H; `[K]` equals H.** This
joins the earlier compiler-populated G68 list to the ordinal query wrappers.
The pointer move clears its temporary and disposes of a nonnull old K through
the existing allocator route. These shallow stores do not establish ownership
or retention of every pointee. Actual selected graph/provider instances and
callback behavior remain separate evidence.

H and state are captured pointer values. Merely replacing G68 or I28 later
does not rewrite K0/K8; mutations through the same H remain visible. X is an
embedded address, not G: the refresh leaf `0x140D45CF0` reads the164 field of
the object pointed to by `[X]` and can reissue queries using existing indices.
The connected constructor/revision writer and teardown are traced below; the
entire mutation/callback history is not established.
Byte K18 starts1 here; its entire subsequent history is not proved.

The null-G setup branch skips K construction/move. The captured fresh-instance
caller therefore leaves K null, but the branch alone does not clear an old K
on a hypothetical reused instance. Do not turn that conditional history into
an observed defect, universal reset contract or proof of runtime reachability.
Setup replaces D through embedded X before this null-G test, so such hypothetical
reuse can retain old K0/K8 while the same X points to a new D.
Final accumulated O30 application is still a separate implementation question.

### Revision and teardown of the embedded context

Call D=`[X]`. Constructor `0x14022333C` explicitly sets byte D0=0, byte D162=0
and DWORD D164=1. The existing wrapper `0x1401B5AF4` loads D from I2548 after
the ordinary host returns and calls `0x1401B5DB4`. If D162 is nonzero, that leaf
clears mask0x02 in DWORD10 of every pointed-to D138 entry (count D144), then
clears D162. It increments DWORD D164 with32-bit wrap **only if byte D0 is
nonzero**, and clears D0 in either case. D162 alone does not advance the counter;
a second call without a new D0 write does not increment it again. This is one
connected revision writer, not proof of every dirty-flag producer or one update
per rendered frame. The refresh caller still uses its existing provider indices.

Retirement reloads D from the same embedded X cell when K10 still names it;
it does not guarantee the same D object survived the host call. Refresh compares
the revision value alone: replacing D with another D carrying the same revision
does not itself trigger refresh. Keep valid live K/X/D storage as a premise;
the refresh leaf does not separately null-check X and D. A revision is not
object identity or a lifetime guarantee.
Caller82071C caches the revision at82075E before issuing its queries. A failed
query can therefore leave the cache holding the new revision; mismatch admission
does not prove refreshed output or guarantee an automatic retry.

The displaced-instance release reaches `0x140222088`, which calls `0x1402221E4`
before its later member cleanup. Under normal returns without independent or
reentrant writes, this resets I20, moves null into I38 and disposes of old K,
moves null into I2548 and destroys/releases old D, then clears I28 before
destroying/releasing its old state. K is disposed before those supporting
objects. X remains the embedded address; its pointee D is cleared. If this reset
ran before null-G setup, K is already null; the setup branch alone is still not
a universal reset. Nested destructors contain callbacks. These direct stores
do not establish callback purity, every rebind path, post-destruction pointer
safety or actual game scheduling.

### Mutation producers and refresh ordering

Treat D0 as a coalescing invalidation flag, not a count of distinct changes.
The captured pre-update route calls `0x1401B4804(I,&I2548)`. On its nonempty
command-list branch, `0x140D14130` forwards key/scalar records to primary D
and the extra contexts. `0x1402AA044` calls `0x1402AA094` for each16-byte record
and unconditionally writes D0=1 after each returning call. An empty valid
range performs no such store. Repeating an already-active key can therefore
mark D0 without changing an activation bit. Several marks before one retirement
produce one revision increment; D164 itself stays unchanged until retirement.
These rules assume valid ranges, returning callees and no independent writes.

For ordinary finite scalars, `0x1402AA094` selects activation at values>=0.5
and deactivation below0.5, on R=`[D8]`. The helpers change key bits in R28/R50
and mark R70 only when a bit changes. The clear helper can fall through from
an already-clear primary bit to the dynamic-key list. Afterwards2AA094 sets
D161 when R70 and D160 are nonzero; it does not clear existing D161 otherwise.
R70 may reflect preceding work, so that pending flag need not mean this call
changed a bit. Container growth and exceptional floating behavior remain separate.

`0x1408DD7D0(D)` clears D160, and if D161 is nonzero writes D0=1, rebuilds
resource state, calls `0x1404A5E5C(D,1)` and clears D161. That latter helper's
AEFB40 path can set D162 after its global/argument/predicate/entry-mask gates.
The ordinary943E7C preparation instead passes0 and skips that optional branch.
Do not conflate D0, D161, D162 or the per-entry flags/counters. In particular,
AEFCAC changes a descriptor's status byte and D148..154 counters;1EBC84 writes
an entry policy. Neither is a direct context revision increment.

The normal route places command processing before the conditional host wrapper;
inside that wrapper the ordinary host returns before1B5DB4 retires D0/D162.
This is a local ordering result. The owner refresh3B77CC→D45CF0 now has a
connected movement-policy caller and stage registration, as below. The ordinary
nested-job dependency is connected too: stage0 work precedes stage8 within the
same bucket. Across buckets, use actual submission order rather than stage numbers.
A comparison before retirement can still see the old
value; do not infer same-frame refresh, rebuilt ordinals,
all callback/rebind histories or final entity movement from invalidation alone.

### Movement-policy dispatch, cached delta and stage order

On this exact build, registration, constructor and descriptor-returning slot0
identify `moveComponent` primary table `0x143033168`. Let M be a component with
that table. M+A8 holds its active policy; M+B0 contains the embedded fallback.
The earlier binding path stores A at M+A8 and calls A.virtual80 to obtain K.
Do not infer that an observed animation instance selected this policy unless
the component, active pointer and table are joined in the same observation.

Primary slot240 (`0x14020D084`) returns when M90 is null. Its admitted path
loads **float[M22C]**, then `0x14020C830` reloads/selects the active policy and
calls virtual18 with that cached value. For A's verified table `0x1430756B8`,
the target is `0x1403B77CC`. Its call to D45CF0 still needs the nonnull A28
and handle-resolution gates; refresh then needs nonnull K and a changed
revision. A policy update is not proof that queries were refreshed.
The delta is captured before delegated dispatch, while the active policy is
reloaded afterward; a replacement policy can receive the earlier sample.

Driver `0x1401F83D0` stores incoming XMM1 at M22C **after comparing M8B but
before branching on that comparison**. The disabled branch can therefore
update the cache without dispatching. On its enabled route, it invokes policy
virtual10, then calls20D084 only when M1FD is zero. A.virtual10 is the leaf
`0x1401FF2B0` (`ret 0`); it is distinct from the virtual18 update.

Outer caller `0x1408AA04C` conditionally calls20D084 with XMM1=0. That does
not zero the cached input:20D084 loads M22C instead. If that load sees0.025,
the policy receives0.025. The outer body's delegated helper could still write
through an alias; a particular cache value requires its own history. Neither
this finite example nor the no-op pre-update proves a stale-delta game defect.
The subsequent policy+20/+28/+30 result wrappers are also not automatically
aliases of the animation aggregate O30.

The typed `gamePuppetUpdaterSystem` registration binds D930AC under
`PuppetUpdaterSystem/PreTick`, bucket mask7, **stage0**. Its selected weak-handle
workers reach1F90B8→1F7C4C→1F83D0. The selector calls the object's virtual120
and uses float+4 of its returned pair; identify that object's actual override
before applying an Entity/Puppet clock formula. The nested worker label
`UpdateSecondPhase` does not mean scheduler stage2.

The same registrar places `EntityAnimations/Update` at stage8 with bucket mask7.
Both descriptors therefore participate in buckets0,1,2 when enabled. Scheduler
`0x1408ED21C` is bucket-major: it resets the twelve-stage scan at8ED247/8ED24A,
then advances the bucket at8ED2F8. With one queue and handle advances between
nonempty stage lists, the relevant order is PreTick0, Animations0, PreTick1,
Animations1, PreTick2, Animations2, where the suffix is the bucket. Stage8 in
bucket0 precedes stage0 in bucket1; all stage0 work does not precede all stage8 work.
The ordinary [nested-job completion contract](#nested-stage-completion) below joins
earlier submitted groups to later ones.
`0x14027316C` remains an asynchronous handle advance, not a blocking wait. Stage
numbers or the advance call alone would not have established this contract.
Actual selected-instance identity, clock override and callback histories remain
separate from the conditional static ordering proof.

A third decoded driver route can repeatedly submit `FixedUpdate_PreSolve`
work, but its connected outer label is `VehicleSystem_SingleFixedStep`.
Keep that owner and route attached to the evidence: it does not show repeated
ordinary V updates. The first route is now connected to the vehicle update owner
below. Concrete selected V clock, final movement application and numerical parity
for these query/clock paths remain open.

#### Vehicle update owner and direct worker completion

Registration1415DA270 names `gameVehicleSystem`, size20A80 and type table14366D0E0.
Its constructor thunk141934F44 reaches9C4624, whose primary-table store1430A31D8
is supported by the complete base-constructor register flow. Primary slot0
returns the same descriptor143BC83B8; slot33/+108 isDAB65C. That method binds the
object to `VehicleSystem_Update`, group4/stage2/mask1. This establishes the owner
of the constructor/table route, not a sampled live system or V selection.

The `VehicleSystem_PreUpdate&PreMove` submission copies its incoming frame delta
unchanged through the explicit payload fields to the movement driver's M22C.
The copied delta is an input; the label does not identify V's effective clock.
The fixed-step route above remains a separate vehicle path.

The first submission passes Q10/Q18 cells through the complete A0CBEC wrapper
to272B40. Its completion group is C=Q18. Worker context E20 points to C's cell.
The child maker21ACC00 passes E20 as the completion-cell argument through the
complete A0D2D0 wrapper to274208. A separately created group273008(0), initialized
with pending count0, is the predecessor. It is not the child's completion group.

Every submitted parallel worker contributes directly to C18. The original
parent job retains its own count until callback return, preventing transient zero
while children finish during incremental submission. These workers need no extra
nested-queue destructor to join C. With no work, the connected terminal callback
still releases the copied payload before its worker returns.

For example, with parent count1: submit child A ->2, finish A ->1, submit B ->2,
return parent ->1, finish B ->0. Under the ordinary stable-storage/normal-return
premises below, this joins the traced stage2 PreMove workers before later submitted
groups on that queue, including later stages of the same bucket. It is neither a
synchronous wait nor a fixed frame delay.
The callback's other jobs have not all had their behavior reconstructed.

Private provenance: `shared-pose-deep/query-upper-clock-findings.md` and
`query-vehicle-join-findings.md`; 50 new instruction anchors, 19 guarded reads,
395 finite direct-parent schedules and 74 prior source bindings checked. This is
static/model evidence. No actual scheduler execution, V policy/clock observation,
final O30 application or character acceptance follows from the owner join.

#### Nested stage completion

Use this contract only for the identified build and ordinary connected queue path,
with valid handles, nonoverflowing counters, normal returns and stable storage.
Child enrollment must be closed when completion is accepted, or future enrollment
must be protected by an already-counted callback. The count cannot reach zero
while that callback can still add its ordinary children. This completion epoch
does not cover new work submitted through a captured handle after zero, arbitrary
detached queues or external state mutation.

Stage submitter8ED324 passes queue10 as predecessor and queue18 as completion
handle to272B40. Submission increments completion.count18 before queuing or
deferring the job; the zero-to-one transition retains a reference at1C. If the
predecessor is pending, its byte20 gate protects a count recheck and linked-list
insertion at head0. If completion wins that race, the job takes the ready route.
27316C moves a pending queue18 into queue10 and allocates a new empty queue18.
Jobs sharing one stage list can run concurrently; later submitted groups depend
on its handle. The stage number alone does not order different buckets.

Worker2732D0 copies a ready job and its handle, builds context E with E20 pointing
to a local handle cell, and invokes the callback at2735DF. Wrapper4BA494 constructs
nested queue Q through2746D8: Q20=E20 and Q30=0. It invokes the stage callback,
then destroys Q through272DB8. With Q30=0, finalizer272F30 moves any pending Q18
into Q10; otherwise it releases Q18. If Q10 remains pending and Q20 is nonnull,
272E1C adds a no-op dependency from Q10 to the parent handle **before returning**.
That operation increments the parent's pending count; it does not block the caller.

Only after the callback returns does the worker decrement its original group's
count18 at2735F1. On a one-to-zero transition it acquires the same gate and rechecks
the count before detaching waiters. Ordinary waiters are submitted with their
already-counted completion handle. A no-op dependency instead decrements its target
count at273760;271F00 detaches further waiters on a guarded zero recheck. The
worker drains those linked records too, propagating completion through nested groups.
If admission found the child already complete, the no-op can run through the normal
ready/callback/decrement path. Reference count1C is distinct from pending count18.
The byte20 gate protects waiter-list operations; it does not serialize every count
increment. A zero recheck cannot fence arbitrary work newly enrolled after that
observation. Such work needs its own dependency/epoch, not a stronger reading of
the existing fence.

Parallel submitter274208 contributes once per worker, including deferred workers.
Its range wrapper2729F4 invokes the optional terminal callback on the last terminal
ticket after the claimed ranges finish, before that worker returns. The one-worker
2E0400 and zero-work-terminal2E03C8 routes also return before the outer decrement.
With no work or terminal callback, submission uses a no-op dependency. The concrete
Puppet PreTick path passes Q10/Q18 through2DFD10 to274208 and advances Q before its
stage wrapper finalizes it. Thus these child workers participate in the parent fence.

For example, a parent body contributes1. Attaching a pending child's dependency
makes its count2; returning the body leaves1. Finishing the child releases that
dependency and permits the count to reach0. Children finishing before finalization
need no pending join. If the join has reserved its parent contribution and the
child finishes before the guarded recheck, it takes the ready route. Returning
from the callback alone cannot clear the pending-child example.

For enabled descriptors in the same bucket, this connects stage0 completion before
stage8 execution. That stage0 refresh cannot see a revision retired later by that
bucket's stage8. It does not exclude an earlier bucket's stage8 retirement. Puppet
1F8470 filters objects by `(object.byte15A & 15) == bucket`; EntityAnimations
D33BEC forwards the bucket to79D980, whose time-bearing79CFB0/79D574 graph routes
select bucket1. Joining the selected policy object, animation instance, context
revision and bucket is still required. Neither registration mask7 nor this ordering
proves that V uses a particular path, a fixed frame delay or a Saber defect.
The pinned [SDK group declarations](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/JobQueue.hpp)
corroborate group completion; the address joins above come from saved-build code,
not a separately verified mapping of SDK address hashes. Root instruction checks
and finite interleaving models support this result. A later independent instruction
audit corrects the former traversal-wide shorthand to bucket-major ordering and
makes the closed-enrollment premise explicit. It preserves the original checks;
native scheduler execution and final game/visual acceptance remain unverified.

## C188: interval extraction and selected result writes

Set Q=`[C+188]`, U=`[Q]`, V=`[Q+8]`, W=resolved entry wrapper,
Animation=`[[W]+30]`, M=`[Animation+68]`. The selected SkAnim branch at
`0x1405E0BA9` returns without these result writes when M is null. Valid
Animation/U/V storage and stable object identity are premises.

The duration helper reads Animation+98. There are separate reads: L0 is tested,
L1 is used if L0>0, and L2 is read after sampling for the final result.
For stable finite duration L and valid sampling storage:

```text
d = L if L > 0 else 1
a = min(U.float0, d)                  if U.byte8 == 0
    remainder_toward_zero(U.float0,d) otherwise
b = d                                if U.float4 < 0
    min(U.float4,d)                   if U.float4 >= 0 and U.byte8 == 0
    remainder_toward_zero(U.float4,d) otherwise
n = 1 if a > b else 0
```

There is no lower clamp on a. The negative endpoint sentinel is handled before
remainder; signed remainder is not positive modulo. n is one bit, not the
number of cycles originally represented by the inputs. For d=4, mode1 and
inputs (8,1), the selected pair is (0,1), n=0. Inputs (4,-1) produce (0,4), n=0;
inputs (-.5,1) preserve the negative start in either mode. Nonfinite/exceptional
CRT paths and changes to duration during callbacks require their literal code.

Adapter `0x140FDF5D8` forwards W,a,b,n and destination V+10 through
`0x1405DEF6C`/`0x1405DF77C` to `0x1405DF7F4`. Let S(t) be the concrete
M.virtual+D8 sample and Te=M.virtual+E0(), requested only when n is nonzero.
Te is not assumed equal to raw Animation duration or d.

For finite XYZ, unit input quaternions and nonzero scales, the native helpers
have the following argument order and algebra:

```text
C(X,Y) [0x14032911C]:
  t = X.t + rotate(X.q, X.s * Y.t)
  q = X.q * Y.q; s = X.s * Y.s
D(X,Y) [0x140327FC4]:
  t = rotate(conjugate(X.q), Y.t / X.s - X.t)
  q = conjugate(X.q) * Y.q; s = Y.s / X.s
```

Products of quaternions use Hamilton order. D is not a conventional affine
inverse: X.t=3, X.s=2, Y.t=7, Y.s=4 along one identity-rotation axis gives
t=.5 and s=2. Neither helper normalizes q here. This algebra does not certify
float32 reassociation or translation-w equivalence; preserve captured lane values.

For n=0, output is D(S(a),S(b)). For n=1:

```text
Z=S(0); E=S(Te)
P=D(Z,E); A=D(Z,S(a)); B=D(Z,S(b))
J=C(Iw1,P); B=C(J,B); output=D(A,B)
```

Iw1 has translation/quaternion (0,0,0,1) and four scale ones. The actual call
does one iteration. The generic dispatcher's negative-loop branch is not
reachable from this caller's n in {0,1}. With unit-scale, identity-rotation
samples S(t).x=10+t, Te=4 and a=3,b=1, output.x=2. For a=7,b=1 and Te=4,
output.x=-2 even if d=8. These abstract samples distinguish endpoint selection;
they are not an Uncompressed sampler fixture. See [extraction sampling](native-motion-adjuster.md)
for the separately identified subtype and its endpoint/count assumptions.

The selected result stores are:

| V offset | Direct value |
| --- | --- |
| 0 | max(L2-b,0) |
| 10..3F | 48-byte extraction QS |
| 40 | (1/d) times XYZ length of that translation |
| 44 | (1/d) times V40 |
| 48 | byte 1 |
| 49 | 2 times has(TurnLeft), OR 4 times has(TurnRight) |

The reciprocal is computed once and reused; neither magnitude is divided by
b-a. V+4..F has no explicit write. Duplicate tags do not increase the bits.
The caller ignores extraction's return byte. Distinct missing-data helpers
initialize translation-w differently; its prior M check does not prove against
concurrent mutation or arbitrary subtype effects.

Multiple's local C188 combiner clears child temporary bytes 48/49, but combines
only byte 48. Its final local stores cover V0..3, V10..47 and byte V48, leaving
caller V49 unchanged under stable pointers and no independent callback alias
writes. Child turn bits 2 and 4 do not imply caller byte49 becomes 6 or zero.
Use the actual caller initialization above; it is not supplied by this combiner.
This is not an observed gameplay defect or a guarantee about arbitrary child
side effects.

## C180: full-clip records, events and cleanup

With C188/C190 null, B=`[C+180]` selects cold branch `0x14249AD3A`.
It increments unsigned DWORD[B+C280] to k, then zero-fills C28 bytes at
P=B+k*C28-C28. C280=16*C28 is a physical prefix, not a bound check. This body
has no count guard or growth call. Valid writable storage and old count 0..15
are premises. Old count 16 makes P overlap the count; FFFFFFFF wraps k to zero
and selects B-C28. These are static address consequences, not observed faults.

| P offset | Direct result |
| --- | --- |
| 0..7 | zero; no request weight stored |
| 8 | XYZ length of the full-clip extraction delta |
| C | raw Animation duration L |
| 10..C0F | up to 128 records, 24 bytes each |
| C10 | event record count |
| C14..17, C19..1F | zero on this direct path |
| C18 | byte 1, including when M is absent |
| C20..27 | QWORD key from node.virtual+148 |

Extraction requests W,start0,endL,loops0 into a separate temporary QS. It does
not use C188's duration fallback, endpoint sentinel, cap, remainder or cycle
flag. Thus it requests D(S(0),S(L)); M+E0 is not called. Missing M leaves XYZ
length zero but still produces the record and events. The length is not
duration-divided or contribution-weighted; the QS itself is not copied to P.
All four identified SkAnim-family +148 slots use `0x14026A920`, which returns
node+C8 through the supplied output slot and ignores the prior R8 value.

Adapter `0x1426083B0` calls event collection `0x1401B6400` with entry=[W],
start0,endL,loops0, clipping sentinels -1/-1, F={P+10,null} and a distinct
local active-event cache K. F's null second pointer bypasses the predicate.
The append helper guards event count<128, retains a 16-byte event handle,
writes float1 at event+10 and a marker byte at +14. A request weight .2 or zero
does not change these emitted weights on this branch. Event records need not
equal distinct authored events; use [synchronization](native-synchronization.md)
for interval, active-event and marker semantics. The 128-event check does not
protect the outer 16-record prefix.

Cleanup passes K to `0x1405E13F4`, which releases 16-byte entries in reverse
through `0x140198330` and clears K.count30. It does not explicitly pass B or P.
The output event handles have their own increments. Final handle destruction,
callback effects and overall lifetime still require their own evidence.

## Concrete C180 producer and locomotion descriptor reader

There is a positive nonnull C180 producer. Typed LocomotionMachine's +F0
refresh (`0x1427275A8`) calls dispatcher `0x14272710C`, which iterates its
16-byte node handles, admits LocoState through a class check and calls
`0x1427284F8`. LocoState registration `0x1417EB004`, constructor `0x142728700`
and primary table `0x143733910` identify that source. The machine's later
planning/selection logic is separate from this descriptor collection; selected
consumers and caller ordering are traced below.

In the helper, entry stack S gives currentSP=S-C488 and RBP=currentSP+100.
C=currentSP+38=RBP-C8, B=RBP+D0, C180=B and B.countC280=0.
C.count168 and C170..17F are zero; C188/C190 are null. The request holds the
incoming third argument, C, float weight1 and the incoming fourth byte. It
selects the first node through `[[LocoState+48]]` and calls its +100. The
exact contract is two dereferences through +48. A local, revision-unverified
SDK describes the inherited field as an array of node handles; that field-name
interpretation remains conditional because no native reflected field join was
inspected. Valid selected storage is a premise; the helper does not check it here.

Let M be the machine node, I the instance descriptor and base=[I]. The
dispatcher constructs a separate output descriptor:

```text
data = base + unsigned32[M+190]
capacity = unsigned32[M+198]
countPointer = data + capacity * 0x238
```

The native address calculation has DWORD arithmetic before addition to base;
valid count/capacity/offset storage and no overflow are required for the displayed
form. This is instance-relative output, not accumulated O+30.

For each C28 source record P with byte[P+C18] nonzero, the helper computes
newCount=oldCount+1 and admits it only when newCount<capacity. Equality rejects.
It stores the new count, selects slot V=data+(newCount-1)*238 and writes:

| V offset | Source |
| --- | --- |
| 0 / 4 | P8 extraction length / PC raw duration |
| 8 | event conversion through `0x1405E1568`, using float[P+C] and P10 |
| 210 / 218 | LocoState DWORD88 / QWORD90 metadata |
| 220 | P0 leading label |
| 228 | P+C20 SkAnim key |
| 230 | P+C18 validity byte |

Event conversion uses the separately traced FootPhase-list helper. It writes
float[P+C] to V+20C, appends selected 16-byte entries using count at V+208,
and does not clear that count before appending. The producer ignores its AL
result and accepts the valid outer record even if no selected events were
produced. This is not a copy of every source event handle or the QS. Unwritten
bytes and initial event-list/count state retain their lifecycle requirements.

No entry reset does not mean an unchanged final count. After its append loop,
`0x1405E1568` validates/canonicalizes the existing output even when the source
event count was zero. Invalid continuity/start conditions reach `0x14249AF16`,
clear V+208 and return AL0. Normal completion returns whether the resulting
count is nonzero. Therefore no newly selected events alone does not determine
AL or the final count. With raw duration4 and no source events:

| Existing output | Final count / AL | Other direct effects |
| --- | --- | --- |
| count0 | 0 / 0 | V20C becomes4 |
| count1, valid entry (start0,end1,duration1,phase0) | 1 / 1 | V20C becomes4; entry remains |
| count2: (-1,1,2,phase0), (1,2,1,phase1) | 0 / 0 | V20C becomes4; rejected payload remains |

The last case has continuous endpoints but a negative first start; it clears
the logical count before sorting. These finite cases use the direct main/cold
bodies and the sorter's zero/one-entry returns. They do not certify arbitrary
event sequences or all canonicalization branches. In each case the outer
producer still ignores AL; one otherwise accepted valid outer record can
succeed even though its event-list count becomes zero.

The helper returns true after at least one accepted valid record, but returns
false on capacity rejection even if earlier records were written. Zero records
or only invalid records also return false. On false, the dispatcher clears the
logical destination count and stops; it does not erase or roll back payload.
For capacity3 with old count1 and two valid source records, slot1 is written
with count2; the next record rejects at newCount3, then the dispatcher stores
count0. Both earlier and just-written payload bytes remain. A later consumer
must honor the logical count rather than treating stale bytes as valid records.

The destination capacity check occurs after child +100 collection. It does
not protect B's earlier 16-record prefix from a seventeenth append. On exit,
the helper releases source event handles in reverse record order through
`0x1401B538C` and clears each P+C10; that release helper visits 24-byte entries
in reverse and delegates handle destruction. The temporary collection and
instance output have distinct ownership.

The selected Machine reset `0x142727510` preserves RDX=I and resets other
instance slots; it does not visibly initialize this destination count or each
output event count. The compiler/allocator route below establishes fresh initial
zeros under explicit premises, not a whole-cache reset on every activation.

### TagSwitch annotates only the newest appended record

Registration `0x1417EB720`, constructor `0x1427261A0` and primary `0x143733548`
tie TagSwitch +100 to `0x142726250`. When C180 is nonnull it visits every
nonnull configured child in order with the original request. For each child
it snapshots B.count, invokes +100, and, only if the count increased, writes
the corresponding QWORD label to the newest record's P0. If a child emits
multiple records, earlier records from that child are not annotated here.
With 2/0/1 appends and labels X/Y/Z, initially zero leading QWORDs become
[0,X,Z]. This label is distinct from the SkAnim key at P+C20.
The C180 branch does not apply the separate ordinary current/blending-state
selection and weight path. Preserve child mutation and storage premises when
following an actual graph; this is not a global all-node collection policy.

## Fresh allocation is distinct from reactivation

Typed Machine compile `0x1427276B8` copies M184 to capacity M198 and registers
an eight-aligned instance allocation of `u32(capacity*238+4)` through descriptor
M188. The layout finalizer writes its offset to M190. Instance creation
`0x140222F3C` through `0x140222FE8` chooses one of two compiled layouts and
zero-fills the requested payload. If that layout includes this block, allocation
arithmetic did not overflow and no intervening writer ran, both the trailing
descriptor count and each D208 event count start zero. This establishes a fresh
allocation path, not the state at every collection or reactivation.

Activation dispatcher `0x140586E38` increments the node's instance byte and
calls +F0 only when the old byte was zero and the reloaded new byte is greater.
The retained root route can select this Machine and thus its C180 refresh;
actual root selection remains unobserved. Machine +110 resets different state
storage, not this descriptor count. Re-entry, retained state transfer, callbacks
and event finalization still require their own write history. Initial zeros
do not enlarge the earlier source16/event128/destination capacity limits.

## Descriptor selection and planner callers

With P=[I], converted descriptors are D_j=P+u32(M190)+j*238. Four separate state
records S_j=P+u32(M1A8)+j*28 hold IDs at8/C, time10, pending time14, duration18,
time scale1C, motion scale20 and overlap24. Offsets/stride are hexadecimal.
The active index J lives at P+u32(M1C0).

`0x142727300` independently selects the first admitted LocoState with matching
DWORD88 kind and QWORD90 key. Descriptor helpers `0x142727268`/`0x1427272B0`
scan a signed-positive logical count: kind1 requires D210=1/D218=key; kind0
requires D210=0/D218=key/D220=label. They do not test D230 or bound that count
against capacity. Matching node and descriptor indices need not be equal.
Planner failure still writes key and IDs before returning; it is not a no-op.

For valid ordinary finite inputs, `0x142726C90` selects kind1 and computes
`n=floor((r/L if L>0 else0)+0.5)`, `v=n*L`, `s=r/v if v>0 else1`, where r is
remaining distance and L=D0. It writes duration=n*D4 and both scales=s, leaving
distance r-v*s. A negative r instead becomes0 without those state-field writes.
A tie r=1,L=2 selects n=1, not nearest-even0; r=.5,L=2 selects n=0,scale1 and
leaves.5 unconsumed. This equation excludes conversion overflow/nonfinite inputs
and is not native float32 parity.

**Reconcile the caller before predicting playback.** Mode3 `0x142727D98`
requires a nonnull target key and J=3. It resets S0, subtracts one selected
kind0 clip's length/time through `0x142726E2C`, resets S1 and calls the repetition
helper. It ignores both AL returns, then overwrites S1.duration with -1 while
preserving the computed scales. Thus n*D4 is not the retained duration on this
route. Missing IDs can still be skipped by the separate advance method.

Mode1 `0x142727F34` requires a different nonnull target key and J=1. It resets
S2 with scales1 and overlap0, then calls event planner `0x142726EDC`. That helper
can align converted phase events or fall back to requested time; it writes
time scale but not motion scale, so this caller retains S2.motionScale=1.
Positive source delay preserves S1 except for time0/new duration and sets an
output flag; nonpositive delay resets S1. The caller ignores helper AL, resets
S3, selects kind1 through `0x142726DBC` and forces S3.duration=-1. Both mode
callers clear two distance accumulators after the nonnull-key test but before
checking J, so a false result need not mean unchanged instance storage.

Event phase conversion must follow literal code. `0x1405E3A44` classifies a
remainder time, with special handling of a boundary-crossing first interval;
`0x1426F2DFC` finds the next phase0 and can return negative delay in a current
phase0 interval. Reverse lookup `0x1405E3608` uses the crossing first interval's
end as its base; when the calculated time exceeds duration it writes negative
duration. It does not implement an ordinary modulo inverse. The aligned planner
uses T/(T-a) without a local zero-denominator guard. These static branches do not
prove that an actual resource reaches such inputs or that they are gameplay bugs.

## Length consumption and first-auxiliary adjustment

Machine +120 `0x142727AC8` zeroes b at P+M1D0 each update. For one valid finite
state iteration, d>0, t=S10, T=S18 and valid next-state overlap o (otherwise0):
negative T or `h=max(T-o,0)-(t+d)>=0` advances S10 by d and supplies d*S1C.
For T>=0 and h<0, it adds `((T-t)/T if T>0 else0)*D[SC].length` to b and
advances state with remaining delta -h. The fraction is not clamped; h=0 does
not advance. This is an iteration contract, not proof for all callbacks/loops.
The pending-time branch writes its saved S14 into the update context after the
child call; do not assume it always restores the original incoming delta.

Evaluation +128 `0x142727948` captures J and the S base before base evaluation.
After that call it adjusts the first auxiliary QS through E+8 unless the
captured J is FFFFFFFF or3. It reloads payload for b and the later accumulation;
the simple P/S notation assumes stable payload identity across the call.
Its bit test is not a general index bounds check.
With finite translation t, L=length(t), s=S20 and b above,
the selected initialized normalization mask yields:

```text
t' = (t/L)*(L*s+b) if L>0, otherwise zero
translation.w = 0
P[M260] += length(t')
```

The mask initializer `0x14009F040` copies all-one XYZ masks and a zero W mask; this formula
requires that initializer and no later mask writer, plus ordinary masked floating
exceptions. Quaternion and scale receive no local writes here. For t=(3,4,0),
s=2,b=1, output=(6.6,8.8,0); b=-12 reverses direction to(-1.2,-1.6,0).
Zero t stays zero even with positive b: a scalar cannot supply a direction.
The pointer join is explicit: the outer host's H+0 holds its local QS;
1B5AF4 forwards H to1B25DC, which copies H+0 to its evaluation frame+18;
3A98D0 then copies that value to E+8. These are distinct frame layouts.
The host later composes that per-graph QS into O30. This is a concrete motion
modifier and accumulation path, not the final entity-movement application.

### Component accessor joins do not yet prove the aggregate recipient

The two component-side accessors8230A0/822618 obtain their query object through
823290 and8232FC. The latter returns `[P+270]+2548` when both pointers exist;
otherwise it returns a lazily initialized global fallback context. P comes from
the promoted Q+250/+258 handle, not an unconditional alias of the entry component.
These are query-context returns, not aggregate O+30.

One accessor carries a C-bearing callback tuple into the record builder. A
pointer in that tuple, a field at record+30, or membership in a callback table
does not establish execution or an aggregate read. Follow the selected callback
transfer/dispatch and exact pointer origin before calling it the final motion
recipient. Transfer1FFADD0 clears the source table at+40, installs it at destination
+40 and calls its+10 method; selected2FCAE0 copies exactly the24-byte tuple. This
is a transfer, not by itself a proved evaluation. The initial accessor/getter
packets left the cold method and invocation open. Later independently reviewed
cold and concrete workspot-manager continuations bind the conditional slot0 call
and its K argument to stored record Q; cold K+CC/+4/+8 writes therefore address
that record. The known method still reacquires the query context, not aggregate O.
The [callback continuation](native-output-consumption.md#stored-callbacks-and-owner-identity)
explains the successful new-state self-pair and actual stack argument while
preserving dynamic service/map identity and selected outer-entry/epoch boundaries.
The later [descriptor/output continuation](native-output-consumption.md#clip-descriptor-sampling-and-local-outputs)
joins the known callback to `AnimSetEntry.animation.motionExtraction`, moved into
record Q+F0. Q+D8 holds its separate name gate, so a nonzero name does not establish
a nonnull extraction object. Conditional endpoint samples feed D-local results;
the concrete extraction subtype and final recipient remain unbound. Connected
manager methods transfer state fields or read S+50/+60, distinct from D's outputs
even when the qualified self-pair establishes D=S+270. A scoped exact-reference/map
pass did not find the outer D+18 caller; it does not exclude indirect or transitive
routes and leaves caller/epoch selection as an offline static question.
Retained provenance: `aux-recipient-continuation/accessor-followup`,
`getter-callback`, `cold-recipient/captured`, and recovery `aux-callback-edge/service-type`,
`sample-output`, its `descriptor-producer` child and `upstream-entry`.
No aggregate O30 reader is proved by these accessor/callback joins.

## Evidence and open links

Retained private reports are `motion-query-context-findings`,
`query-extraction-findings`, `query-result-flag-comparison` and
`query-c180-findings`, `query-producer-findings`, `query-lifecycle-findings`,
`query-machine-follow-findings`, `query-normal-mask-followup`, `query-planner-findings`
and `query-planner-parent-followup`, plus `query-option-construction-findings`
and `query-context-construction-findings`, `query-lifetime-findings` and
`query-mutation-findings` and `query-owner-schedule-findings`,
with companion checks and
scoped independent instruction reviews. They link constructor/table identity, complete selected
bodies, guarded captures and finite discriminators. The report hashes remain
in the private investigation ledger; no game resources ship with this skill.

The lifecycle continuation includes a separate draft instruction review completed
and rechecked by root after worker availability ended. Machine/planner state
writes, caller overwrites, captured-state timing and the first-QS pointer join now
have a separate retained-instruction review and finite discriminators. A separate
query review covers K/X construction, revision/teardown, mutation markers and
policy dispatch. These reviews do not execute native code or cover arbitrary
callback histories, every option-buffer constructor or selected gameplay.
Earlier planner/parent and query-construction/lifetime receipts omit their own
producer-script hashes; newly bound copies do not retroactively supply that
provenance. Frozen reports and failures retain their original scope.

The local C188/C190 constructors, named result consumers and the captured
K-construction/G68-provider join are established. Final O30 application and
selected rebind/cache/callback histories remain implementation questions.
Actual extraction subtype/data, remaining caller topology, storage lifetime,
capacity admission and exceptional inputs are not supplied by these equations.
Do not equate a provider, contributor, query result, pose auxiliary and final
movement recipient from similar names or offsets. Installing this guidance
does not complete the full animation investigation or accept a character mod.
