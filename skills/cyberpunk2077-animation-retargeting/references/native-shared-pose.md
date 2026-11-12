# SharedMetaPose ownership, coordinates and scheduling

This reference establishes one normal graph-chain path in the saved Cyberpunk 2077 2.5 executable with SHA-256 `d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`. All addresses are preferred-image VAs for that binary. It is static implementation evidence, not an observation of a loaded asset or gameplay. Revalidate addresses and layouts for another executable.

The established result is that SharedMetaPose receives mapped entries from an aggregate shared by graph instances in a linked list. Ordinary transforms are local-domain values while those graphs run. Earlier graph writebacks can be read by later graphs in the same outer call. A precise Root-child branch accumulates ancestors before supplying an entry. The graph's static-command callback runs synchronously inside evaluation; later skinning jobs are a separate handoff.

## Evidence and owner identity

WolvenKit's cached documentation revision `2fb9050fad45187867be9fd2b7a98a6ee98f7039`, including Exporting Rigs & Anims, documents discovery/export but does not specify these native semantics. The implementation conclusions below come from the pinned executable. Public layouts corroborate named fields at RED4ext.SDK commit `8ebb8da485b4ab22081e9be65de70fe1193538da`: [Rig](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/animRig.hpp), [MetaRig](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/animMetaRig.hpp), [AnimatedObject](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/animAnimatedObject.hpp), and [AnimationSystem](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/worldAnimationSystem.hpp). The handwritten AnimatedObject header explicitly marks its name inferred; its unnamed native fields are not promoted to official semantic names here.

| Identity or boundary | Address provenance |
|---|---|
| SharedMetaPose | registration `0x1417f2330` → type table `0x1433b7f10` → constructor `0x1411eb218` → instance vtable `0x1431b1528` |
| Shared evaluator / emitted callback / overlay | `0x1403a5ddc` / `0x1403a5db8` / `0x1403a5e6c` |
| AnimGraph | actual constructor `0x140ce99fc`, vtable `0x1430e9b88`; root+0x40, command descriptor+0x90, command flag+0xa2 |
| Graph instance host | `0x1401b25dc`, reached through wrapper `0x1401b5af4` from graph-chain host `0x1401b3e00` |
| worldAnimationSystem | registration `0x141754760` → type `0x1433421f0` → constructor thunk `0x140a250bc` → constructor `0x140a251a8`, vtable `0x1430a86d8` |
| Animation-system graph task | task `0x1421301c0`, graph-call fragment `0x14213031f`, call to graph-chain host at `0x142130836` |

The research ledger retains disassembly and command receipts in the `shared-pose-deep` evidence bundle, especially `findings.md`, `artifact-audit.json`, `evaluator-{outer,inner}.asm`, `command-dispatcher.asm`, `graph-result-writeback.asm`, `aggregate-rebuild.asm`, and `postgraph-continuation.asm`. Reused `transitions-deep` evidence includes `graph-owner-update.asm`, `clock-host-entry.asm`, and the world/task identity traces. These artifact names are provenance, not links to files shipped with this skill. Fresh binary jobs used the shared writer guard, 512 MiB address-space cap and 120-second deadline. No game or native target execution occurred.

## Context and current/reference ranges

Keep these contexts distinct:

- `H`: second argument to graph-instance host `0x1401b25dc`.
- `G`: graph-evaluation context passed to `0x1403a98d0`.
- `N`: node-evaluation context passed to SharedMetaPose.
- `O`: outer graph-chain owner; `Q=[O+0x08]` is MetaRig, `P=[O+0x18]` is the aggregate pose object, and graph-instance list starts at `O+0x60` with next at instance+0x08.

For graph ordinal `j`, outer host supplies `H+0x28=Q`, `H+0x30=Q.mappings+128*j`, and `H+0x38=P`. The host constructs a temporary range view `R`:

| R offsets | Contents | Source |
|---|---|---|
| +0 / +8 | current transform begin/end | mapped entries from `[P+0]`, 48 bytes per QS |
| +0x10 / +0x18 | current float begin/end | mapped entries from `[P+0x18]`, four bytes per float |
| +0x20 / +0x28 | reference transform begin/end | mapped entries from `Q+0` transform array |
| +0x30 / +0x38 | reference float begin/end | mapped entries from `Q+0x40` reference-track array |

Transform range entries have 64-byte stride: graph index at the beginning and 48-byte QS payload at +0x10. Float entries have 8-byte stride: graph index then float. Mapping pairs themselves have 8-byte stride `{graphIndex, aggregateIndex}`. The host writes graph indices, so an aggregate index is not a destination pose index.

Current-transform producer `0x1401b31f1..0x1401b3274`, current-float producer `0x1401b3443..0x1401b3478`, and separate reference producers `0x1401b3166..0x1401b31be` / `0x1401b3408..0x1401b343c` establish the sources. The pointer chain is `R → G+0x10` at `0x1401b2ded..0x1401b2df4`, then `G+0x10 → N+0x38` at `0x1403a9980..0x1403a9984`.

This supplies the input contract for the SharedMetaPose overlay and SharedMetaPoseAdditive's separate current/reference inputs. It does not imply that ordinary SharedMetaPose subtracts the reference, or that either node receives a whole parent component's final pose.

## Transform publication and float lifetime

The outer host performs two linked-list passes. First, it pre-fills aggregate transforms from every graph rig using `0x1401b45bc`. Selector `0x1401b462c` chooses local A-pose (`rig+0xb8`) when its count (`rig+0xc4`) equals bone-name count (`rig+0x5c`); otherwise it chooses local reference pose (`rig+0x48`). Overlapping mappings can therefore be overwritten by later baseline prefills before any graph evaluates.

The second pass updates and evaluates each graph. Host writeback `0x1401b3c08`, called at `0x1401b30d8`, publishes into the same P before returning to the next graph. Transform output mapping is at mapping+0x40 with count table+0x50; float mapping is at +0x60 with count table+0x70. Ordinary entries are copied unchanged. Later graphs can see earlier writes during the same outer call. A skipped graph contributes no new writeback; input freshness depends on mappings and taken branches.

Floats have a different baseline lifetime. Predicate `0x140bb10e8` requests rebuilding when any graph instance's dirty byte+0x18 is set. The host branch at `0x1401b44f0` calls `0x140582830`, which replaces P with a fresh aggregate and destroys the old one. At `0x14058298e..0x140582996`, the new float array at P+0x18 is resized to `MetaRig.trackNames.count` at Q+0x5c using `0x14026d16c`. That helper zero-fills newly added four-byte elements at `0x14026d189..0x14026d19c`. Thus fresh current floats are 0.0; the rebuild does **not** copy MetaRig reference floats into them. The dirty bytes are cleared at `0x1405829bd`.

The normal per-call prefill writes transforms only. Unwritten current floats can therefore persist between ordinary calls until a write or rebuild. Do not assume reference-track initialization or a reset each frame. This statement covers the inspected path; alternate engine paths may also write the aggregate.

## Coordinate domain and Root-child exception

Ordinary shared records are local-domain while the graph chain runs. After all graph instances return, `0x1401b4265..0x1401b4278` conditionally calls `0x140582b3c(P,Q)` when outer-context+0x9c is set; the normal task-context constructor initializes that byte to 1. The helper traverses bones in index order, composes each non-root with its parent, normalizes output quaternions, and hashes the resulting array. This is the explicit local-to-model boundary after the chain.

The current-range producer has one identified exception. If the destination rig's `parentIndices[graphIndex]==0` **and** its bone 0 name is `Root` (hash `0xca7cfe2bef51b2a5`, literal at `0x14307fb10`), it calls `0x140adeb30`. This starts at the mapped aggregate bone, follows signed 16-bit parent indices at Q+0x10, and composes ancestors until -1. An out-of-range starting index yields identity. The resulting entry is in the accumulated hierarchy/model domain for this Root child. The reference-range producer still performs its direct copy; do not apply the current-range conversion to it by assumption.

Ancestor composition `0x1403262dc → 0x140327164` uses the following QS operation, with componentwise scale product `⊙`:

```
C(A,B).t = tA + R(normalize(qA))(sA ⊙ tB)
C(A,B).q = qA * qB
C(A,B).s = sA ⊙ sB
```

`R` rotates a vector and `*` is the Hamilton quaternion product. Rotation helper `0x1403270f4` normalizes its quaternion through `0x14032af60`; this composition's quaternion product itself remains raw. For unit quaternions it agrees with ordinary C composition used by the additive helper. Parent ordering, valid acyclic hierarchy and finite transforms are required; the ancestor loop does not repair cycles.

Writeback has the same Root-child condition at `0x1401b3d57..0x1401b3dba`. It obtains the aggregate parent's accumulated QS, then calls `0x140322f30(destination,parentModel,graphOutput)`. For parent A and graph result Y, the actual native arithmetic is:

```
t = R(normalize(conjugate(qA)))(-tA)
  + R(normalize(conjugate(qA)))((1/sA) ⊙ tY)
q = conjugate(qA) * qY
s = sY / sA
```

The reciprocal scale multiplies Y's translation, not A's negative translation. This is not interchangeable with a general matrix inverse for nonunit scales. Conjugation mask `0x143c39620` initializes through `0x14245772a` from the three-sign-bit constant at `0x1437bafb0`.

## Graph command ordering

Graph compiler `0x14058a718` invokes the root's vtable+0x130 emission method at `0x14058aa58..0x14058aa5b`. Shared emitter `0x140c071f8` emits its input first through `0x140c060a0`, then appends 16 bytes `[callback,nodePointer]`.

Evaluator `0x1403a9c80` tests graph+0xa2. The ordinary route invokes the root through evaluator trampoline `0x1403aacc0`. The compiled route calls dispatcher `0x140326350` with the same node context, instance state and output. The dispatcher reads an eight-byte callback pointer, invokes it with `(N,state,output,payloadCursor)`, advances by its unsigned returned payload length, and continues synchronously. Shared callback `0x1403a5db8` reads its node pointer, calls the common overlay, and returns 8. Its total command therefore occupies 16 bytes and completes before the next command.

This establishes ordering inside this emitted stream. It does not establish a worker thread, a global frame identifier, or the ordering of every node in every graph.

### Alternative candidate and nested GraphSlot

Use A for the actual AnimGraph resource here; G above remains an evaluation
context. Compiler `0x14058a718` clears A+0xc8's handle, then walks its root with
visitor `0x14058c754`. The callback uses a native GraphSlot ancestry cast and
accepts name hash `0x223e48987ba6e518`. Each matching visited node replaces the
candidate, even on a repeated visit whose zero id then prevents child descent.
This is last matching **visited** node, not a claim about every serialized node.
The compiler also sets A+0xa3 for resource-path hash `0x9c91053c1ceb96c3`;
inequality does not clear a previously true flag. String preimages are unproved.

On valid initialized slot entries, update selects that candidate only when A.a3,
incoming admission byte, nonnull candidate, populated nested graph entry and
global byte143915820 are all true/nonzero. Otherwise it selects A.root40.
Evaluation first honors A.a2's compiled stream, then applies the candidate gates,
otherwise ordinary root. Selected nodes use the same synchronous update/eval
dispatch; this selection adds no asynchronous queue.

Order matters: update and eligibility helper `0x1403a987c` compute the populated
entry predicate whenever a candidate exists, before the A.a3/admission gates.
The predicate's missing-ID tail dereferences a null entry; a missing entry is
not the safe false case of a found entry whose graph pointer is null. Disabled
admission therefore does not make an invalid update entry table safe.

Owner O+0x68 bit5 supplies the outer admission byte. Update and evaluation take
separate snapshots and feedback can change it; no semantic flag name or immutable
value is inferred. Normal nested GraphSlot helpers `0x1403a8fdc` and
`0x1403a8e78` force admission zero for both update and evaluation; nested compiled
evaluation still has precedence. GraphSlot_Test's node+0xc8 instead controls
variable transfer before/after root activation; it is not the resource's A.c8.

The global's file initializer is1 in writable data. Its alternate producer/live
value remains untraced; limited reference scans do not prove immutability.
Actual reflected resource E8/EC/ED time/pause controls remain unresolved.
Retained provenance: `graph-control-deep/a3-alternative-findings.md`, typed
binding/static-slot/nested-pose reports and independent selector discriminators.

## Auxiliary QS records

The node output wrapper contains pose pointer at +0, first auxiliary QS pointer at +8 and second at +0x10. These are distinct from the bone array.

The outer host resets owner O+0x30/+0x40/+0x50 to identity at `0x1401b3eb8`, `0x1401b3ec5` and `0x1401b3ec9` before the graph-list evaluation loop. That owner QS accumulates within one chain invocation; it is not an unconditionally cumulative world transform across frames. Per-graph history at instance+0x2510 has a separate lifetime.

| Record | Proven owner/lifetime | Proven consumer or limit |
|---|---|---|
| Wrapper+8 | `G+0x18 ← H+0`; per-graph stack QS initialized to identity at `0x1401b400e..0x1401b401d` | composed into owner+0x30 after each graph at `0x1401b4241..0x1401b4250` through `0x14032911c`; retained at instance+0x2510 by `0x1401b301b..0x1401b3038`, then forwarded to next graph update's context+0x60 → node-update-context+0xb0 |
| Wrapper+0x10 | `G+0x20 ← H+8 ← outerContext+0x20`; task stack QS initialized to identity at `0x142130435..0x142130454`, passed by constructor `0x14212ff40` | passed through the graph chain; the normal continuation discards its final value and exports neither it nor its known alias to the two later jobs |

The first record has a confirmed motion-adjustment use. MotionAdjuster registration `0x1417e72e0` → type table `0x1433afa38` → thunk `0x14272f598` → constructor `0x14272ee90` binds vtable `0x1437344b8`. Evaluator `0x14272f62c` evaluates its input first, passes wrapper+8 to method `0x14272f16c`, and on its active branch writes adjusted translation at `0x14272f74d` and normalized rotation at `0x14272f76c`. The method reads target-position, target-direction and duration links matching the pinned [MotionAdjuster declaration](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_MotionAdjuster.hpp).

This establishes a motion-adjustment channel, but does not identify its final gameplay/root-motion recipient. The second record also has a typed motion-derived producer, described below; no camera label is supported. The proven full-weight auxiliary composition in additive blending must not be used to infer either channel's final recipient.

### A concrete second-channel producer

SkAnimAdjuster registration `0x1417e8de4` installs type table `0x1433b0e60`; its constructor thunk `0x14272b900` reaches `0x14272b47c`, which installs instance table `0x1437340e8`. Evaluator slot37 is `0x14272b978`. The [pinned SkAnimAdjuster declaration](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_SkAnimAdjuster.hpp) corroborates target-position/direction link offsets; instructions establish their use.

This evaluator first calls the plain SkAnim pose evaluator, then gates its additional work on a resolved animation entry, inherited applyMotion byte+0x50 and per-instance adjustment state. Extraction helper `0x1405def6c` loads AnimSetEntry.animation at+0x30 and Animation.motionExtraction at+0x68; missing entry/extraction yields identity. Through `0x1405df77c` and `0x1405df7f4`, the extraction object samples start/end via virtual+0xd8. The zero-loop result uses native QS difference `0x140327fc4`; nonzero loops additionally sample zero and the endpoint and compose cycles. Do not replace that difference with a conventional matrix inverse for nonunit scales.

The adjuster combines sampled extraction with target/context values and an interpolated instance correction. At `0x14272bdb8` it loads **wrapper+0x10**, writes translation at `0x14272bdcb`, then writes normalized rotation at `0x14272bdd8`. It leaves that QS's scale unchanged. This is a conditional motion-derived adjustment in the **second** auxiliary, not an established entity/world-movement application. In contrast, the inspected plain SkAnim evaluator `0x1405846dc` only supplies wrapper[0] to its pose sampler and does not directly write either auxiliary pointer.

The retained `first-aux-producer-followup.md` contains this class-to-write trace.
The later [motion-adjustment chapter](native-motion-adjuster.md) separately
derives both direct correction solvers, their admitted caller/lifecycle paths and
one uncompressed extraction sampler. Other extraction subclasses, arbitrary
node uses and the final aggregate movement recipient are not generalized from it.

The later-job alias question is resolved by the submitted ranges. Let T be the animation task's RBP: the second QS occupies `[T+0x280,T+0x2b0)`. Skinning's 96-byte source view is `[T+0x220,T+0x280)`, ending immediately before it, and the final 112-byte descriptor is `[T+0x160,T+0x1d0)`. The pointer fields trace through `0x1403242e0` to MetaRig metadata and through `0x140b4eef8` to aggregate transform/float arrays. The latter helper also copies the first auxiliary QS temporarily, but that copy is overwritten before submission. Neither numerical QS belongs to the submitted skinning view. The broadcast job copies only a component pointer. The task then releases its stack without a later direct read of the second QS or its context alias. This excludes those two delivery routes; it does not prove that every possible graph callback is unable to retain a pointer elsewhere.

### Stored query callbacks and clip extraction

The known accessor output reaches a 1B0-stride record through tuple copy/move.
A later concrete workspot-manager new-state construction proves [S]=S for that
successful stable provenance, joining D=W+270 to S+270. Existing map entries and
an arbitrary nominal service lookup do not inherit that identity. The constructed
destination's +18 body contains a real slot0 call; its known adapter binds K to
the stored record Q. Entry into that body and its gates remain premises.
Follow [callback storage and output consumption](native-output-consumption.md#stored-callbacks-and-owner-identity)
for the actual stack-cell argument, known/alternate table distinction and selected
outer-caller/epoch limits. Neither this invocation nor record initialization
establishes final aggregate O+30 application.

The known callback's descriptor now joins to the queried animation's motion-extraction
handle at record Q+F0. Its separate Q+D8 name gate is not the handle's nonnull test.
Conditional endpoint sampling and combination reach destination-local output fields;
the concrete extraction subclass and final application remain open. Connected manager
map/getter methods do not supply the missing outer D+18 caller or a D-output recipient.
Use the [descriptor/output continuation](native-output-consumption.md#clip-descriptor-sampling-and-local-outputs)
for null/lifetime premises and the bounded search's exact limits.

### Retained component handles are not auxiliary-QS consumers by themselves

Three concrete retained-handle routes now have distinct immediate readers:
WetnessComponent reads O+0xe0 status; PhysicalSkinnedMeshComponent reads a named
ShapeBlend value through O+0x18; SkinnedClothComponent reads **ClothBlend** through
that named-record route into state+0x224. These reads do not fetch O+0x30's QS.

The Cloth path is joined from its typed destination+0x2b8 (`0x1404e5e6c`), retained
AnimatedComponent handle at state+0x160, key helper `0x1404e5d94` and getter
`0x1405fd920`. The getter writes default0, then copies the first matching record
and returns success separately. On success the callback emits command0x3b with
four unchanged scalar bytes; its separate pointer command0x2b precedes that test.
Missing ClothBlend and present-zero therefore both leave scalar0, but only
present-zero emits0x3b. Incoming per-bone QS data is consumed separately.

The owner pre-reset helper `0x140325c5c` reads descriptor limits and changes a
limit field; it does not read the accumulated QS. These finite reader closures
and the known overwritten exporter copy exclude specific suspected consumers,
not every downstream use. Final application of accumulated O+0x30 remains open;
the already established instance+0x2510 feedback remains a different lifetime.
Retained provenance: `first-aux-holder-closure.md`, `first-aux-physical-followup.md`,
`first-aux-cloth-followup.md` and `first-aux-exporter-prereset-followup.md` in the
private `shared-pose-deep` research bundle.

## Downstream jobs and limits of ordering

After graph-chain evaluation, animation task continuation `0x142130b1e..0x142130d99` traverses graph instances and obtains each component at instance+0x25a8. Event-range forwarding at `0x142130b86 → 0x1409e97ac` precedes conditional later job submissions:

| Submission | Proven target |
|---|---|
| `0x142130d2e → 0x14212f670 → 0x14212fbd0 → 0x140a0cbec` | `Update Skinning` literal `0x1436177d8`, task `0x1421314b0`, 112-byte copied descriptor |
| `0x142130d67 → 0x14212f800 → 0x140a0cbec` | `Broadcast AnimParams` literal `0x1436177c0`, task `0x142131540`, eight-byte copied component pointer |

The skinning task optionally broadcasts parameters via `0x14053c978`, checks component+0x8b, and calls `0x140325580`. That helper walks 16-byte handles at component+0x120 with count+0x12c and calls each recipient's vtable+0xe0. A traced AnimatedComponent insertion path filters those handles by **entISkinningAttachment** ancestry before appending them; the recipients are attachments. Concrete SimpleSkinningAttachment locks its destination component and forwards the view. The [native skinning reference](native-skinning.md) follows a confirmed SkinnedMeshComponent destination through metadata/name mapping, actual 48-byte matrix writes, bounds, eye matrices and float-track delivery. This goes beyond the unnamed array in the public ISkinableComponent declaration.

Thus node overlay and graph writeback precede aggregate local-to-model conversion, which precedes the later job submissions on this path. The graph's synchronous command callback is separate from those jobs. Concrete attachment/destination identity, packed-buffer CPU reads and a conditional nested-job completion relationship are now traced for the named branch; see [output consumption](native-output-consumption.md). Selected producer-before-transfer ordering, destination lifetime and completion relative to rendering remain separate. An IK node's placement depends on active graph topology, and external procedural components may have other stages; this trace does not order all IK globally.

## Discriminators and runtime follow-up

These are independent consequences of the inspected branches, not engine-executed tests:

- With baseline A, graph 1 writes B to an ordinary mapped bone and graph 2 reads B during the same outer call. If graph 1 is skipped, graph 2 can read prefilled A. This distinguishes sequential publication from an obligatory one-frame-old input.
- With MetaRig reference float 0.75, rebuilding current P yields 0.0. After a graph writes 0.4, a subsequent ordinary call with no write to that slot can still read 0.4. This distinguishes current/reference and rebuild/call lifetimes.
- With identity rotations, parent translation 10, parent scale 2 and graph output translation 14 on one axis, the Root writeback helper gives `-10+14/2=-3`; a conventional inverse would give 2. Unit scale removes that distinction.
- Swapping graph-list order can change which mapped value is visible at a SharedMetaPose node. Changing only the command route does not itself insert a deferred callback: the compiled Shared callback finishes within the dispatch loop.

For an actual asset, capture one call/frame identifier with owner/P pointers, graph ordinal, mapping pairs, input range payload and output at `0x1401b31f1`, `0x1403a5e6c` and `0x1401b3c08`. Record P before/after `0x140582b3c`, both auxiliary pointers, and each recipient pointer/vtable at `0x1403255b8`. Expected ordinary shared entries match preceding writebacks in local space; only the documented Root-child branch accumulates ancestors. Observe a rebuild separately to test float reset. This procedure is proposed verification only; no instrumentation, game launch, runtime pose capture or visual acceptance was performed.

Resolved here: normal-path producer, mapped ownership, ordinary coordinate domain and Root exception, same-call graph publication, float initialization/lifetime, synchronous command dispatcher, named motion-adjustment writers for both auxiliary channels, later job payloads, and a concrete attachment/destination path. Partial: first auxiliary record's final gameplay recipient and other graph-internal uses of the second. Dynamic inputs still required: active graph list/order, mappings, hierarchy, masks, taken skip/LOD branches, actual handle recipients, and cross-component dependencies. Do not turn this static path into a universal parent-pose, skinning, or runtime-correctness claim.
