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

D is W+270. The connected owner factory promotes a pair at S and transports
**W=[S]**; it does not prove W=S. The separate attachment route supplies S+270,
stores it in a manager's recipient field, invokes virtual80 and later reloads
the field before virtual78. The recipient can change across those calls. A
conditional setup also depends on an input flag; one captured caller supplies
zero. Neither matching offsets nor the same constructor family supplies the
missing pointer identity or invocation.

Reset 14022E294 locks D2+28, calls the existing D2.virtualA0 and releases the
byte; its body installs no concrete table. Transfer 142613788 swaps an exact
16-byte pair; it does not construct an object. A third real factory caller
obtains a lookup result X using key[143BC4540], promotes its embedded control
and uses P=[X+8] as the receiver of virtual220. X, P and the pair holder
are distinct identities unless a self-handle invariant joins them. This path
requires a live control and nonnull P: it dereferences P without another null
test after promotion. The returned first pointer S passes a concrete predicate
that preserves RCX before entering the factory. These direct joins do not
determine virtual220's construction target or prove W=[S]=S.

Final auxiliary-motion application remains OPEN. Bind the stored record's actual
slot 0 call, its supplied third argument/K, the concrete owner/table and an actual
source/alias to aggregate O+30 before naming a movement recipient. The connected
service lookup virtual8 and the virtual218/220 producers remain concrete
identity boundaries. Repeating proved tuple moves or assigning K from its parameter name
does not answer them. Selected lifetime/mutation and accumulation-to-reset timing
remain separate from this static storage result.

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
it can establish producer-before-transfer ordering. The precise remaining
phase edge is the caller's selected [outer+350].virtual40 at 1403D60BD, with a
local descriptor argument, and its producer/group relationship. The range
builder appends nonnull context+FB0/+FB8/+FC0 objects; this is not a pose pointer.
The connected registry helpers' captured direct bodies use S+41A0 and establish
no main-bank producer/group join. Their delegated calls are not a proof of
transitive absence. Do not infer a race, fixed delay, finished frame or engine
defect from that missing join. Selected generation/bank history, destination
mapping/lifetime and actual draw consumption remain OPEN.

Private provenance: recovery packets `aux-callback-edge/storage-invocation`,
`skinning-edge/reader/continuation`, `main-buffer-association`, `queue-consumer`,
`second-queue-publication/stage-invocation` and the G3 `owner-reset` continuation,
with their independent saved-evidence reviews.
They contain exact byte/argument checks and finite address/order discriminators;
those models do not constitute a game concurrency test. Executable bytes and
raw disassembly are not distributed with this guidance.
