# Native callback storage and packed-skinning consumption

Use this when a pointer/descriptor handoff is being treated as applied auxiliary
motion or completed skinning. These are independently reviewed static findings
for the pinned CP2077 2.5 executable identified in [native skinning](native-skinning.md).
They extend [shared-pose publication](native-shared-pose.md); they do not identify
a selected asset, live object generation, rendered frame or visual result.

## Stored callbacks and owner identity

The successful known-table output of accessor 140822618 reaches a local E and
recipient 1408D6E40. On its ordinary valid, capacity-sufficient, nonoverlapping
route, 1408D6624 copies E into a local record and 1408D6A94 appends a 1B0-stride
record under D+30. For table 14394AEF8, slot+8 copies the 24-byte tuple. The move
adapter copies the table, clears the local table, then invokes slot+10, which
uses the same tuple copier. Those operations establish storage, not execution
of callback slot 0. The alternate producer's table 14394AED8 is distinct and cannot inherit this proof.

The independently reviewed service-type continuation identifies the query key
at 143BC4540 as nominal AIIWorkspotManager. Separate registration and constructor
evidence binds concrete AIWorkspotManager table 1430B32E0: +218 selects
1401CBA70 and +220 selects 14022C790. This establishes an available concrete
implementation, not the dynamic receiver returned by an arbitrary service lookup.
Keep direct result X, promoted P=[X+8], state S and wrapper owner W=[S] distinct.
The promoted path still requires live control, stable storage and nonnull P.

The concrete +220 searches maps and copies a stored pointer/control pair, or
returns a zero pair. Concrete +218 can likewise reuse a map entry, or take its
successful new-state branch through 1401CBDE0 and 1401CBE8C. That constructor
explicitly zeros S's first pair and installs table 14302E198 at D2=S+270. The
creator builds a pair whose first pointer is S, copies it to a local pair, and
swaps that local with S's first pair through the already proved whole-pair swap.
Immediately after the normal swap, [S]=S. Under successful allocation, valid
nonoverlapping objects, balanced control/lifetime and unchanged pair/table
contents through later transport, W=S and D=W+270 equals D2=S+270. This is
store-derived identity for that provenance. An existing map hit or matching
nominal type does not inherit it without its own history.

The concrete destination's +18 method, 1403B2D8C, contains a real stored-record
loop. After its lock/time gates, it obtains Q=[D+30]+index*1B0 and calls
1405E0D4C(Q, output, delta). Under the evaluator's current provider/state
conditions, a nonzero table at Q+190, zero byte Q+A0 and zero qword Q+D8 permit
the callback path. It supplies callback=Q+150, output and Q to 142017C20.
That wrapper stores Q in its entry stack home at entry-RSP+18. One push and
SUB RSP,20 precede LEA R8,[RSP+40], so R8 addresses the same saved Q cell.
The wrapper loads table=[callback+40] and calls its slot0 with output, callback
and that cell's address. For the preserved known table 14394AEF8, the actual
14124B3BC adapter dereferences the cell: its method's K is therefore Q.

This is a conditional static invocation/K proof, beyond copy/move storage.
Entering D+18, its selected count/time/provider/flag path, object lifetime and
unchanged callback table remain premises. The wrapper also passes the cell to
another nonnull callback table, but that table's method does not inherit the
known adapter's dereference or behavior. The proof does not select an upstream
task calling D+18, a live update epoch or an observed frame.

The previously traced cold method's K+CC/+4/+8 writes now bind to record Q;
the callback result is copied to Q+D8. These initialize descriptor/sampling
state. They do not establish a C-to-O acquisition, an [O+30,O+60) source alias,
final accumulated-motion application, or composition-to-reset ordering.
The alternate callback table and indirect providers remain separate contracts.
The descriptor/sample continuation below identifies a clip-extraction source;
record+30 or another matching offset still does not establish aggregate O30.

Private provenance: `aux-callback-edge/service-type`, its sealed 281-file packet
and independent saved-byte, pair/stack and semantic review. These are static and
host-model checks. No target execution or selected gameplay acceptance occurred.

## Clip descriptor sampling and local outputs

For the known callback's valid typed query result, the descriptor producer follows
`AnimSetEntry.animation` at entry+30 to `Animation.motionExtraction` at animation+68.
It copies the extraction pointer/control pair, then moves it into descriptor+18
and ultimately record **Q+F0**. Separately, animation name at +90 becomes the first
QWORD at **Q+D8**, and duration at +98 becomes a descriptor scalar. The Q+D8 nonzero
test is a **name-field gate**, not a nonnull extraction-handle test. Either field
can pass its own check while the other fails; do not collapse them into one gate.

This transfer requires accessible typed pointers, valid nonoverlapping storage,
balanced controls and stable contents across event/trim helpers and displaced
handle cleanup. The extraction-pair helper does not check a null animation before
reading its fields. A duration helper's null-animation fallback of 1.0 does not
make the whole producer safe, and early exits do not fully initialize the descriptor.

The record sampler distinguishes Q+A0-clear interpolation from Q+A0-set descriptor
sampling. The latter uses the name gate and recorded timing fields; a nonnull
Q+F0 object supplies two virtual+D8 endpoint samples through the shared extraction
helper. This selected helper call passes zero loops; the separate nonzero-loop
route and descriptor repeat handling retain their own contracts. The clip source is established, but its
concrete extraction subclass/table and selected sample times remain unbound.
Do not automatically substitute the previously investigated uncompressed sampler.

For preserved destination table 14302E198, its +C0 method combines the record-loop
accumulator with D+40; the parent stores the result at D+60/+70. Later selected
branches write D+A0 and scalar fields D+B0/+B4/+B8. This is static source/output
dataflow, not numerical parity or an external movement application. The separate
placement path uses component placement fields or cached placement, with its own
predicate and conversion limits; no aggregate O30 alias follows from that input.

The connected manager-map methods transfer state pairs or update S+4C8. A separate
manager getter copies S+50..5B and S+60..6F after its state predicate, leaving the
output's intervening four-byte gap outside that copy. Even on the qualified
D=S+270 route, these are distinct from D+60/+70 at S+2D0/+2E0. This getter therefore
does not join D's local result to a final motion recipient.

A bounded exact-reference and connected map-consumer search found no outer caller
of D+18. Its empty relative-call and supported RIP-reference searches cover only
those encodings; table entries prove implementations, not invocation. The captured
manager bodies contain no such call, while cleanup/queue helpers remain opaque.
This is not transitive or global absence. The missing discriminator is a typed
caller or update registration tied to the qualified destination, arguments and
epoch. That remains an offline static question, separate from live activation.
Final D-output application, C-to-O/O30 acquisition and composition-to-reset order
also remain open.

The constructor-bound manager's +108 registration is now a bounded resolved lead.
It builds a callback capturing raw manager M, with the native label
`[U]/WorkspotManager/PostBucketsTick` and selector 5. Its known copy/move leaf
copies M without retaining it; registration does not itself invoke callback slot0.
The selected adapter loads captured M and reaches a body that iterates map M+1C8.
Each node's pointer/control pair is swapped with a zero local pair before the
old pair is passed to delegated cleanup. The captured bodies do not directly
invoke D+18. Their cleanup, final registration transfer and framework invocation
remain separate boundaries; this is not transitive absence or a lifetime proof.
The registrar's type-related argument is loaded QWORD[M+30] when nonnull, with
its own fallback. It is neither &M30 nor the captured M pointer. Do not repeat
this PostBuckets route as an unexamined animation-update entry.

Private provenance: independently reviewed sealed `aux-callback-edge/sample-output`,
its `descriptor-producer` child, and `aux-callback-edge/upstream-entry`. Their saved
instruction and finite field/handle checks do not establish selected gameplay.

## Concrete bone backend and separate eye storage

For service table 1436CE318, the component's bone factory 140206E60 reaches
1404F690C→1404F6948 and constructs B with table 14305CA08. Its +28 method
140298860 requests 48*n bytes through 1402988E4; its +20 method is RET-only.
That post-write virtual therefore supplies no completion barrier.

Its eye setter+58/140CA7740 stores 64 bytes at B+50+64*selector and then sets the
selector validity bit at B+110. Getter+60/140C363F8 tests that bit, copies the
same 64 bytes and returns AL=true, or returns false without writing output.
For selectors 0/1 the joined caller consumes the stored left/right eye matrices.
Local stores-before-bit order is proved; the bit does not check a frame or
generation and can remain true from an earlier write. Eye freshness and
cross-thread visibility are not established by these leaves. These matrices
are separate from the main 48-byte-per-bone bank.

## Main allocation, B+14 and actual payload reads

With M=[service+D8], the ordinary allocation validates B+10's low16 index and
high16 generation, returns bank+uint32(offset), and emits a 12-byte
`{handle,offset,size}` record before the caller writes its matrices. Registration
retains B in row `M+820+48*index`, at row+20. Record/count visibility and the
allocation's local byte protocol cannot certify those later matrix writes.

The connected transfer moves pending records at M+CE034/count M+DA038 to
M+DA03C/count M+E603C. The publication path installs each nonzero handle's
offset/size into its row history using the low16 index, without repeating the
high16 generation validation. The same-M, bank, B and generation/lifetime
premises remain required across the asynchronous global reloads.

On the valid active-row path, history chooses current/previous entries; when
their sizes differ it uses the larger descriptor for both. Successful publication
writes four DWORDs at B+14:

```text
{ currentOffset+48, 48, previousOffset+48, currentOffset!=previousOffset }
```

This is an offset/stride/history descriptor, not a CPU pointer or matrix payload.
The arithmetic is 32-bit under the ordinary valid-range premise. The separate
`{0,0,0,1}` write is a failure/reset path. The established B+14 and context+38
consumers read this descriptor; their presence alone was not a payload read.

Two scheduled workers partition the second queue. Worker 140B01C48 loads the bank
from M+E6040 and a destination pointer D selected by uint32(M+E6108−1), then
copies record.size bytes from `bank+uint32(offset)` to
`D+48+uint32(offset)`. The exact copy body has actual source loads and destination
stores, including both 48-byte SIMD routes. Thus this route reads the normal
packed writer's allocation, subject to the same-object/bank/record premises.
It does not decode those matrices or prove vertex/GPU use. The zero-length copy
returns without payload access; preceding pointer/index loads still need valid
state.

## Actual invocation and bounded completion

The constructed service stores T at S+70. Its same-table virtual4D0 is the exact
getter 1419545D0. In 1403D5F88, the first getter result supplies T.virtual330 at
1403D60E2; the constructor-bound target waits on the group loaded from T+8,
with timeout -1, until the ordinary successful path observes count+18 equal 0.
The caller then builds its range, reloads the service/getter, and calls T.virtual10
at 1403D614A with publication enabled. This is an actual static invocation of
1403D6D84, not merely a pointer stored in a table. Same-T/S/M and valid stable
objects remain premises across the reloads and old-owner callbacks.

Queue advance 14027316C is asynchronous: B descriptor publication can precede
finished copies. The publisher's nested queue joins both copy jobs into its
parent before callback return, and the transfer exports completion into T+8.
An ordinary later wait on that same closed enrollment epoch includes those
callbacks and their stores. The preceding wait at 60E2 covers prior selected
work; it does not complete jobs that the new transfer at 614A has yet to submit.
Reusing a group pointer does not enroll arbitrary future work in a completed
dependency. Other concrete drain/wait paths attach exported T+8 work to their
supplied query; an address or descriptor alone is still not a completion fence.

The transfer takes records before importing its prior dependency internally,
while allocation emitted each record before matrix production. The now-proved
outer wait therefore needs an actual join to the selected pose producer before
it can establish producer-before-transfer ordering. The selected outer+350
phase object is now conditionally constructed through the fixed
`servicesGameServicesWin` registration. Its virtual40 drains a locked collection
of 0x28-byte records and clears its count; that byte lock is not the pending-work
DWORD18 or a pose-completion wait. Initial virtual38 uses a RET callback, subject
to later mutation. Successful initialization selects state2, whose traced delegates
reach an external user-provider request and a Boolean command queue. Selected
command execution/completion updates those command fields, not T8 completion.
Neither this finite coverage nor the remaining delegates prove transitive absence
of animation work. The range
builder appends nonnull context+FB0/+FB8/+FC0 objects; this is not a pose pointer.
The connected registry helpers' captured direct bodies use S+41A0 and establish
no main-bank producer/group join. Their delegated calls are not a proof of
transitive absence. Do not infer a race, fixed delay, finished frame or engine
defect from that missing join. Selected generation/bank history, destination
mapping/lifetime and actual draw consumption remain OPEN.

## Successor dependency after transfer

On the captured normal route, the outer caller invokes its +360 helper after T10.
That helper reloads the service/getter, saves T and its table+18 target across a
verified 19-byte leaf, then actually calls T.virtual18. Its query constructor
initializes two groups and clears Q20/Q30. The import of T8 at query+10 reads the
source group's pending count: zero returns, nonzero attaches a no-op dependency.
This is neither pointer assignment nor a CPU wait. A zero count also needs a
closed enrollment epoch; later contributions are not retroactively covered.

The traced submitters use the query's current predecessor/completion groups.
Asynchronous advances carry the dependency into subsequent queued stages. The
final callback builds a nested query, calls a service dispatcher, and finalizes
its children through the retained ordinary completion contract. Export moves the
resulting completion group back to T8. With stable identities, valid storage and
ordinary queue/callback preservation, queued successors inherit the imported
prior dependency. This is conditional static ordering, not an observed frame.

Direct setup is separate. One helper calls selected record/context virtual20 and
virtual58 methods synchronously before its later submission/advance. Those direct
operations do not wait merely because a dependency was imported. The retained
record's virtual20 returns its embedded descriptor; construction moves selected
handles, so do not call it an immutable byte-for-byte snapshot.

The final service dispatcher also has later dependency plumbing through the
**object field T+18**, distinct from the **virtual method at table+18** and T+8.
The nested-query consumers now reach an actual selected-record dispatch. Both the
parallel worker and the separately constructed dependency-graph jobs load O from
the selected 48-byte row at +10, construct a local context/nested query, and call
140332F90(O,context,query). Its body actually invokes O.virtual08 after selected
policy gates. A call site and shared row layout still do not identify O's concrete
table, its animation role, an immutable cross-callback snapshot or a matrix read.
The index mask 0xDFFFFFFF clears only bit29; valid selected storage is a separate
premise. The context copier preserves selected bits and retains a named handle;
it is not a bytewise snapshot. The optional post-action can run directly or as
another queued job according to a selected virtual gate.

Preserve the direction: prior wait → transfer submission → successor dependency/
submissions → later completion. Successor ordering does not establish a
producer-before-transfer join. Selected group/instance history, lifetime and
actual completed use retain their own evidence requirements.

### Row installation and active selection

The selected record source is now a concrete subrecord P returned by a bounded
lookup. It selects the first entry with either the requested hash or an unused
hash sentinel; it does not prefer a later exact match over an earlier sentinel.
The caller requires a valid nonnull result. Its following hash leaf compares and
stores the requested hash, and unchanged hashes permit reuse of existing P
contents. Hash equality alone certifies neither initialization nor freshness.
Keep loaded F=QWORD[Q+38], embedded descriptor address V=F+10 and L=&K10 distinct.

The installer shallow-copies 16 bytes from source row+8 to destination row+8,
including O at +10. It copies the qword at +18, then replaces only its low DWORD
with the caller's subrecord ordinal. It neither constructs nor retains O in those
captured direct stores. The tail can rewire links and remove selected rows by
swapping index entries and leading ordinal DWORDs. It does not physically swap
whole 48-byte rows or their O cells. A removed row may still contain the copied
pointer bits while no longer belonging to the active prefix. Use the updated
indices to determine which row is selected; retained bits do not prove lifetime
or eventual invocation.

On the construction path, the later destination finalizer clears WORD[row+1C]
and derives two byte labels at +1C/+1D, then sets L+68. These bytes overlap the
upper DWORD of row+18: its preservation was true only at the earlier copy point.
The captured graph operations do not directly rewrite O, active indices or count.
Their byte arithmetic wraps; valid graph/scratch bounds and terminating recursion
remain premises, not an unrestricted topological-order proof. The no-rebuild
branch bypasses these finalizers.

The owner finalizer clears each source P's byte+68 and DWORD counts at
+10/+24/+34/+40/+54/+64, leaving backing pointers, stored hash and physical O bits.
It neither releases O nor proves source/destination nonaliasing. Distinct P/L and
row storage are needed to conclude that source reset leaves destination selection
intact; opaque storage delegates and later callbacks retain their own limits.
The source may be cached or conditionally rebuilt by separately supplied direct
preparers. O's construction/table and selected instance history remain concrete
offline questions. Do not choose an O subtype from the row category or hash.

### Constructed job enrollment under explicit holds

A dependency import that occurs before individual job admission can still cover
that constructed set when a real pending-work hold already exists. The traced
1403E90F4 increments group pending DWORD+18 before storing the group in an
unreleased wrapper. Its zero-to-one reference-count handling is separate. It
does not directly replace the supplied group cell. In the outer call this
preserves destination D; importing a dependency from T+18 did not alias D to T18.
Optional observer/container calls retain their explicit no-relevant-mutation
and lifetime premises.

For each constructed graph record, the code makes holds for completion group A
and predecessor group B before linking edges or importing terminal A groups.
The paired move transfers the group pointers and release flags to persistent
64-byte records. Moved-from temporary destruction sees null groups and removes
no contribution. All jobs are then admitted with B as predecessor and A as
completion. The actual control-flow path finalizes the nested query before
walking the persistent records backwards, releasing B then A for each record.
The once-only release flag prevents a second decrement; count zero still uses
the retained gated detach/recheck contract.

For example, a completion group starting at zero has pending=1 after its hold.
An import at that point attaches to represented work. Two admissions raise its
count to 3; dropping the hold leaves 2 until those jobs finish. Completions may
interleave with release without erasing admitted contributions. Without the
hold, an earlier import at zero cannot cover jobs added afterward. This is the
constructed-set distinction, not authorization to add arbitrary contributors
after the hold has been released or to omit the closed-epoch premise.

The result assumes valid initialized groups/arrays, matching wrapper counts,
nonoverflowing counters, nonaliasing stable storage and ordinary successful
admission/completion. It does not prove progress through cycles or external
blocking. The independent finite hold and linked-group models explain the count
invariant; they are not engine execution or a concurrency stress test.

### Outer hold release and the later import

The distinct outer D wrapper now has a concrete release route. Two ownership
moves transfer it through a temporary into a queued payload; cleanup of either
moved-from wrapper sees a null group. The queued callback releases the payload
once, before its own ordinary job completion. A second release call is inert
under the once-only flag. Releasing D and finishing the callback are separate
events; allocation/free and optional observer delegates retain their limits.

The parallel submission, intervening ordinary job and release job each use the
current Q10 predecessor and Q18 completion, then advance Q. An advance seeing
pending work promotes Q18 to Q10 and creates a new completion group. Seeing zero
leaves the cells unchanged. Thus a later counted stage either depends on the
preceding stage's pending completion or follows its already completed work.
This requires stable group identities, successful ordinary admission/completion,
properly attached child work and closed relevant enrollment. The intervening
callback remains opaque; no termination or unjoined-work guarantee follows.

After the release submission advances, the code exports Q2 and imports its
completion into the then-current Q10. If release is pending, that destination
is the release completion group, not its already captured predecessor. If
advance sees zero, the release callback has already returned and Q10 may retain
the old predecessor; the later import cannot retroactively delay that release.
Do not claim that advance always creates a new group. The ordinary Q2 export
uses its constructed, unmodified Q20=0 state; the alternate state is separate.
Finite scheduling models distinguish these cases without proving arbitrary
graph progress or an observed engine deadlock. D remains distinct from the T18
source. Selected O construction/type and producer enrollment before the earlier
T10 transfer remain open.

Private provenance: recovery packets `aux-callback-edge/storage-invocation`,
`skinning-edge/reader/continuation`, `main-buffer-association`, `queue-consumer`,
`second-queue-publication/stage-invocation`, `phase-producer`, `phase38-producer`,
`outer360`, `successor-consumer`, `successor-enrollment`, `row-installation`,
`row-finalization`, `outer-hold-release`,
and the G3 `owner-reset` and `update-entry/capture` continuations, with their independent
saved-evidence reviews.
They contain exact byte/argument checks and finite address/order discriminators;
those models do not constitute a game concurrency test. Executable bytes and
raw disassembly are not distributed with this guidance.
