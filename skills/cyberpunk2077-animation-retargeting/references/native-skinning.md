# Native attachment and mesh skinning preparation

## Scope and evidence

These are static findings for Cyberpunk 2077 2.5 executable SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses are preferred-image VAs. Revalidate the executable, class construction
and virtual slots before applying them to another build. The trace reaches actual
CPU matrix/bounds writes, a packed-payload CPU reader and a conditional nested-job
completion relationship. It does not establish selected producer-before-transfer
ordering, GPU upload, vertex rendering, an instantiated asset's inputs or gameplay
acceptance.

The retained `animation-graphs-research/shared-pose-deep` evidence includes
`recipient-followup.md`, `aux-alias-followup.md`, `skinned-metadata-followup.md`,
`skinned-destination-followup.md`, adjacent disassembly/guard receipts,
`skin-symbolic-replay.py` and `check_skinned_followup.py`. These names identify
research provenance, not dependencies shipped with this skill. Pinned SDK layouts
corroborate [ISkinningAttachment](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/ent/ISkinningAttachment.hpp),
[SkinnedMeshComponent](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/entSkinnedMeshComponent.hpp)
and [CMesh](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/CMesh.hpp).

## Typed recipient and destination

AnimatedComponent virtual+0x1b8 (`0x140aa0830`) calls insertion method
`0x140aa0880`. Its runtime cast `0x140aa09b0` accepts `entISkinningAttachment`
ancestry, then appends a reference-counted handle to component+0x120. Registration
`0x14163d674` binds that exact type to the cast's global `0x143bc2ef0`.
The downstream dispatcher `0x140325580` iterates this array and calls attachment
virtual+0xe0. Immediate recipients are attachments, not destination components.

Concrete SimpleSkinningAttachment factory `0x1402031c0` installs vtable
`0x14360f450`; virtual+0xe0 is `0x1403255c4`. It promotes the weak destination
handle at+0x40/+0x48, skips an expired destination or false destination+0x290
result, and otherwise calls `0x140325648` with the pose descriptor.

SkinnedMeshComponent constructor `0x140208a10` installs vtable `0x143031250`:

| Destination slot | Target and established behavior |
| --- | --- |
| +0x290 | `0x140325774`: accepts `(LODMode & 0xfd)==0`, or uint16 at component+0x12a equal to 0 or 8 |
| +0x2c0 | `0x140325ed4`: validates or rebuilds the mesh-to-MetaRig cache |
| +0x2b8 | `0x1401ff2b0`: immediate return; no extra pose change |

The common consumer requires source wrapper+0x198 and a nonempty mesh view. It
calls metadata+0x2c0, then `0x1402983c8` when the mapping cache and a bone or float
backend exist, then pose+0x2b8. Do not stop at the no-op slot and conclude that no
skinning work happened: the common helper already performs the work below.

## Name mapping, source matrices and cache lifetime

Metadata is a 56-byte view of MetaRig bone names, float-track names, parent indices
and hash. Cache M at component+0x1a8 is reused only when its uint64+0x48 equals
that hash and uint64+0x50 equals sourceWrapper+0x10. Equal keys skip rebuilding;
the check does not compare
name-array contents or matrices individually.

Factory `0x140716254` maps each mesh bone name to the **first exact CName match**
in MetaRig names. It copies the mesh's `boneRigMatrices` verbatim, one 64-byte
matrix per bone. This caller supplies no matrix override, and the factory does
not invert matrices or derive them from the current graph pose. Inspect the
actual native matrix bytes when diagnosing deformation; a Blender rest pose or
matching bone names alone cannot certify this contract.

### Source-wrapper fingerprint and replacement

The typed component's virtual+0x2a0 (`0x140716888`) calls factory `0x1407168c8`
with its mesh and an empty matrix-override range. A nonnull mesh is admitted when
WORD[mesh+0x8c] or DWORD[mesh+0xcc] is nonzero. The first test uses only the low16
bone count, while the subsequent view uses the full DWORD count. The 24-byte
wrapper W retains a weak mesh pair at+0/+8 and a stored fingerprint at+0x10.

Starting at `0xcbf29ce484222325`, helper `0x14049dcac` consumes, in order:
boneNames bytes, boneRigMatrices bytes, boneVertexEpsilons bytes and lodBoneMask
bytes. For each byte, `h=((h XOR byte)*0x100000001b3) mod 2^64`. Float-track names
are present in the view but **are not hashed**. Resource addresses, current float
values and range delimiters are not hash inputs either. Raw matrix bits matter:
equal numerical values with different representations can hash differently.
The first three byte lengths are the low32 pointer difference rounded down to
multiples of 8, 64 and 4; the last is the low32 byte difference. Valid representable
ranges are required. The factory's separate nonempty matrix override replaces the
hashed matrix range, but the ordinary typed caller above supplies none.

The ordinary resource-completion path is joined through typed virtual+0x170
(`0x1403d0eac`), captured weak self-handle, job callback `0x14071600c`, successful
promotion in `0x14071608c`, wrapper factory and move `0x140716de8(&C[0x198])`.
An expired self-handle skips these writes. Construction zeroes both wrapper and
cache handles; replacement exchanges the wrapper pair and releases its previous
owner. The assignment itself does not clear cache C+0x1a8. Further appearance
callbacks may invalidate it and are not all expanded here.

Consequently, **if the cache survives**, the MetaRig key stays equal and a new
wrapper has the same four hashed byte sequences, this validator accepts the old
mapping even if float-track names differ. It reads the stored fingerprint without
rehashing mesh arrays. This is a conditional cache contract, not proof of a broken
reload or global absence of invalidation. Actual scheduling, resource identities
and cache survival remain separate evidence. Retained provenance is
`shared-pose-deep/skin-wrapper-key-findings.md` and its byte/hash/cache checks.

### Queued appearance and proxy ownership

The immediate and dependency-queued appearance routes converge on component
virtual+2C8. The queued binder714B40 moves a16-byte weak component pair into its
payload; callback7149D0 invokes the virtual only after successful strong promotion
and a nonnull component. Null/expired handles skip the call, including the checked
failed-CAS continuation. The payload has no mesh, W/M or resource-generation key;
this callback alone cannot certify that the queued generation is still current.

For the captured component table143031250, +2C8 selects7150E0, gated by C+8B and
nonnull C+200. For nonnull bone-backend B=[C+1B8], descriptor builder4B2D80
carries that exact B into descriptor X+C0. Its X+A8 is **not** cache C+1A8. The selected +278/+288
delegates add no component writes; this bounded observation does not make all
delegated calls pure or prove transitive cache preservation.

Factory722E64 returns its caller's output-pair address on both result branches.
The component then moves that pair into C+1E0/+1E8 through4B10D4: the new pair is
installed before the displaced pair is released. A distinct source pair is
cleared; self-assignment preserves the pair. Failing7150E0's initial gates returns
before replacement. Passing them but receiving N==0 from service+2B0 makes722E64
fill an empty output pair; moving that pair into C1E0 releases the old proxy.
The factory still returns the output-pair address. These branches are not equivalent.
An already-acquired consumer handle
can retain the old proxy after replacement: strong counts1→2 on acquisition,
2→1 on replacement,1→0 on the final release. This does not prove synchronized
concurrent acquisition or a selected frame's actual interleaving.

The factory forwards the descriptor to service143BBCAE8 virtual+2B0. For the
captured service table, this is3D9740, which branches on descriptor byte X+60.
In7150E0, the post-initialization stack store sets X+60=1. The checked builder
writes and qword aliases preserve it under valid-object/ABI premises, selecting
3DAD50 for this table. That constructor installs N's primary table 143059AB0, returns
N, and retains the reloaded B=[X+C0] in H+10. The checked helper links/selects H
through N+48 using the requested Skinning metadata key. A later keyed accessor
returns &H10 for a matching node under its mask gate; actual callers dereference
that field into B. Stable list/key/object identity remains a premise, including
across repeated lookups; a creation request alone does not prove H's instance table.

Wrapper constructor 3D9C64 stores N at P+10 and retains it. Later 7155C0
dispatches [service+70].virtual98 with &P10 and argument0. The later constructor,
storage and getter proof binds this field to stage T for the same constructed,
stable service; virtual98's own consumer behavior is separate from the proved
main-bank copy path. The [output-consumption trace](native-output-consumption.md)
now joins the bone-backend type, eye storage/read pair, B+14 descriptor, actual
packed-bank reader, stage invocation and bounded completion. Its successor
continuation distinguishes imported job dependencies from synchronous setup,
then binds both selected-record dispatch routes and explicit holds that account
for the constructed jobs before terminal dependency imports. It also follows
source-row copying, later metadata/reset writes and the outer hold's queued
release, preserving both pending/completed advance cases. Selected record type,
source/destination nonaliasing and producer/transfer identity remain separate
obligations. The later [AnimationSystem and B0 frame trace](native-output-consumption.md#animation-update-to-frame-transfer)
conditionally joins admitted graph jobs and qualifying synchronous skinning work
to a real wait before transfer across both captured Update branches. It resolves
that represented-work path, while the actual registration, selected gates and
same allocation/record/bank/generation still need evidence. None alone proves
rendered output.

Retained provenance: `appearance-handoff-continuation/captured` and
`appearance-handoff-continuation/proxy-followup`, `backend-retention` and
`backend-retention/attachment-ownership`, followed by the recovery `skinning-edge`
packets. Weak promotion, descriptor aliases and the named handle transport are
statically checked. Selected scheduling,
resource generations, transitive cache lifetime and rendered output remain OPEN.

### WolvenKit round-trip boundary

The cached [mesh documentation](https://github.com/CDPR-Modding-Documentation/WolvenKit-8-Wiki/blob/2fb9050fad45187867be9fd2b7a98a6ee98f7039/wolvenkit-app/usage/import-export/models.md)
distinguishes the flat MeshOnly skeleton from WithRig/MultiMesh exports. In pinned
WolvenKit revision `6ab5da88c009b99e653ce87be5251a9c5bd15330`,
[`GetOrphanRig`](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/MeshTools.cs#L1165)
inverts mesh rig matrices, extracts/remaps translation and rotation, and emits
unit scale with parent -1. The corresponding
[import helper and caller](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/MeshImportTools.cs#L348)
can rebuild matrices from each selected joint's **local** translation/rotation,
reversing the basis and inverting the rebuilt transform. That helper does not
consume joint scale, world matrices or glTF inverse binds. A legacy heuristic
instead preserves existing matrix/position tables when at least one name matches
and all matched rotations are nearly identity; translations do not disable it.

With destination bone names present, `GetBestMatchingSkinJointArray` selects the
skin with the greatest positive matching-name count, keeping the first on ties;
zero matches returns no joints. Only an empty destination name list selects by
total joint count. The legacy test requires at
least one match, not a match for every destination bone. On that branch the caller
also avoids adding missing bones. A matched rotation outside the near-identity
tolerance disables the heuristic, permitting the nonlegacy rebuild/add-missing
route. Record the actual
branch; import success alone does not identify it.

Check the project's actual tool version, export route, joint domain and native
readback before relying on a round trip. A flat child's translation 3 and a
hierarchical child's local translation 1 under parent translation 2 represent
different inputs to this helper, despite the same world position. Do not silently
substitute one or assume nonunit scale survives. These pinned source findings are
separate from the native consumer and are not an instruction to upgrade tools.

### Packed mappings

Each 12-byte entry stores a packed index word, LOD mask byte+4 and epsilon float+8:

```text
aggregateIndex = packed & 0x7ff
matrixIndex    = (packed >> 11) & 0x7ff
outputSlot     = packed >> 22
```

The factory initializes matrix/output indices from mesh bone ordinal. Missing
names pack aggregate index 0x7ff; there is no nearest-parent fallback. Parallel
bone/matrix/mask/epsilon lengths and the fixed index widths are input invariants,
not repaired by this loop. Mesh float-track names likewise map to the first
MetaRig match; missing tracks become uint16 0xffff.

LOD range helper `0x1402987e4` uses low 10 bits of its selected packed word as
start and high 11 bits as a count added to start; an oversized LOD index clamps
to the last word. The factory constructs that high field as last active index+1.
Thus an artificial nonzero-start case differs from a conventional end index:
start 1/high 3 yields entries [1,4). Do not silently reinterpret the arithmetic.
A valid-resource invariant may make starts zero; this trace does not prove it or
show a shipped asset violating it.

## Concrete matrix writes

`0x1402983c8` selects LOD0 unless component.useSkinningLOD is true, then uses the
descriptor's LOD. It obtains a buffer through bone-backend virtual+0x28, or uses
the pre-supplied descriptor at component+0x1c8/+0x1d0 and clears that descriptor
after the call. Both branches select **48-byte output records** through
`0x1402982dc → 0x140298f4c`, followed by backend virtual+0x20. The separately
inspected raw-64-byte helper exists but is not selected by this caller. For the
constructed table 14305CA08, +28 returns the normal bank allocation and +20 is
RET-only; it is not a completion barrier. The [allocation/publication continuation](native-output-consumption.md#main-allocation-b14-and-actual-payload-reads)
joins that bank to its actual CPU reader and distinguishes the B+14 descriptor
from payload and selected-update completion.

The inner loop skips an entry only when its entire mask byte is zero. Selection
of the outer range is separate; the inner loop does not test the selected LOD bit.
An aggregate index outside the input pose count substitutes identity QS. Otherwise
it reads the aggregate model-space QS produced after the graph chain's
[local-to-model boundary](native-shared-pose.md#coordinate-domain-and-root-child-exception).
The input pose is read, not rewritten by this consumer.

Let D be the mesh-supplied matrix and P the converted QS. With quaternion
(x,y,z,w), scale (sx,sy,sz) and translation (tx,ty,tz), P's **stored rows** are:

```text
P0 = (sx*(1-2*y*y-2*z*z), sx*(2*x*y+2*z*w), sx*(2*x*z-2*y*w), 0)
P1 = (sy*(2*x*y-2*z*w), sy*(1-2*x*x-2*z*z), sy*(2*y*z+2*x*w), 0)
P2 = (sz*(2*x*z+2*y*w), sz*(2*y*z-2*x*w), sz*(1-2*x*x-2*y*y), 0)
P3 = (tx,ty,tz,1)
C[i,j] = sum(D[i,k] * P[k,j] for k=0..3)
output[outputSlot] = (C00,C10,C20,C30, C01,C11,C21,C31, C02,C12,C22,C32)
```

The QS converter does not normalize the quaternion. The fourth-column formula
is real arithmetic with finite intermediate results, not a claim about overflow,
NaNs or exact float32 grouping. Preserve the stored-row convention when using a
column-vector library. Scalar and four-entry writers check outputSlot against
output element count and skip an out-of-range store; the stride is fixed 48.

An independent symbolic replay checked 443 saved SSE operations against all
48 four-entry output lanes and 60 converter SSE operations plus a final store
against all 16 matrix lanes. It caught a draft error: legacy memory-source MOVSS
clears upper lanes, so the converter's fourth column is (0,0,0,1) under the stated
arithmetic assumptions. This is instruction-dataflow verification, not game
execution or floating-point/rendering parity.

Discriminator: D translates by (-2,0,0); P rotates +90 degrees around Z and
translates by (10,20,30), with unit scale. D*P translation is (10,18,30), while
reversed multiplication gives (8,20,30). Packed output columns are
(0,-1,0,10), (1,0,0,18), (0,0,1,30), up to floating-point approximation.
With an out-of-range aggregate index, identity P leaves D's first three columns.
The missing-name sentinel 0x7ff takes that branch for the small valid fixture;
do not assume a separate sentinel test for an arbitrarily oversized pose array.
It does not substitute aggregate bone0.

## Bounds, eye matrices and float delivery

Bounds accumulate each selected QS translation minus/plus its mesh epsilon.
They are not obtained by transforming vertices and do not scale epsilon by QS
scale. For (10,20,30) and epsilon .25, XYZ bounds are (9.75,19.75,29.75) through
(10.25,20.25,30.25), independent of D's bind translation. Nonfinite resulting
lanes take the traced finite fallback box; an invalid empty-range box takes the
separate [-1,1] XYZ fallback. The result writes component+0x160/+0x170 without
editing graph bones.

The two special mapped mesh indices are **eyes**, with initializers and name
bytes verified: preferred `l_J_eye_JNT` / `r_J_eye_JNT`, falling back to `LeftEye`
/ `RightEye` only when the preferred lookup has no valid mapped bone. Each valid
index produces a bone-derived matrix delivered to backend virtual+0x58 with
selector 0 / 1. The caller replaces its last stored vector with (1,1,1,1).
These matrices are unrelated to the task's two auxiliary QS records. The special
helper does not repeat the main loop's aggregate-index bounds check; valid input
mapping remains required. The named subtype's+58/+60 pair now proves storage
and an actual validity-gated read of those 64 bytes. Stores precede the validity
bit locally, but the bit does not certify a fresh frame or synchronization; see
[separate eye storage](native-output-consumption.md#concrete-bone-backend-and-separate-eye-storage).
No shader or procedural-eye execution was observed.

### Concrete float-track backend

The component's virtual+0x2b0 factory `0x140206da0` calls service+0x2d0 when
mesh, track count and service exist. The service's identified callable provider
`0x140ae9830` constructs table `0x1436ce318`; its +0x2d0 factory `0x140737044`
constructs a 0x68-byte object with table `0x143077ba0` through `0x140737120`.
Setup `0x140206c48` and replacement `0x14020629c` connect that returned object
to component+0x1c0. These constructor/table joins identify this concrete backend;
do not assign its behavior to arbitrary objects sharing the interface.

The object stores output count C at+0x20, buffer count K=2 at+0x24, storage B
at+0x10, current write pointer at+0x28, and another pointer B+4*C at+0x30.
Constructor/resizer `0x14026d16c` and reserve `0x140270174` establish explicit
zero fill of both buffers on a successful, nonoverflowing 2*C allocation.
This does not mean they are cleared again on every engine frame.

The connected caller tests the low32 of `(sourceEnd-sourceBegin)>>2` for zero.
On a valid range, an empty source skips both virtual+0x30 and +0x20. Otherwise
it passes map count n, the 16-bit map range and source float begin S; it supplies
no per-index source bound. Concrete mapper `0x140a70230` obtains D through
virtual+0x28 (`0x1419413d0`) and clears exactly 4*C bytes before either loop.
Signed32 n<=0 therefore clears without reading map/source data; the caller then
still advances the pointer when its source was nonempty.

For each row i in a positive n, both branches use:

```text
sourceAddress = S + 4 * signed16(map[i])
```

`0xffff` reads S-4; `0x8000` reads S-0x20000. There is no sentinel skip, index
clamp or source bounds check. This is not Python's negative list indexing.
Actual prefix accessibility/value is required before predicting a result or
fault; the address rule alone is not a deformation diagnosis.

An empty secondary table selects the direct branch `0x1425165c8`, which copies
unchanged 32-bit values to D+4*i. The mapper does not enforce n<=C. Exceeding C
from the first buffer can write into the second before leaving the allocation.
A nonempty secondary table instead looks up row ordinal i, **after loading the
source value**, then stores at D+4*j only if that ordinal is found. Missing
ordinals suppress the store, not the source read. Later stores win on duplicate
destinations. The input descriptor's end pointer is not used as a bound.

Initializer `0x1407371d8` matches each mesh name against the first matching name
at+0x30 in 80-byte registry records. It inserts `{name,i,j}` keyed by i only when
unsigned j<C. Null/no-match/only-rejected registries leave the table empty and
select direct mapping; partial matches select the secondary path. These bounds
apply to valid constructor payloads, not fabricated entries. Cold duplicate-key
and allocation-failure behavior is outside this normal-path proof.

Post-write virtual+0x20 (`0x140d67cc4`) adds 4*C to current+0x28 and wraps to B
only when it equals `B+4*uint32(C*K)`, with a 32-bit product. For valid positive
C and K=2, two calls give `B -> B+4*C -> B`. It does not change pointer+0x30,
clear/copy floats, call a renderer, or prove a read/write-pointer swap. Keep
this CPU write-pointer rotation separate from subsequent shader/morph use.

Retained provenance: `float-backend-followup.md`, constructor/mapping captures,
`float-backend-independent-review.md` and explicit-address model checks in the
private `shared-pose-deep` bundle. These are static/code-derived checks, not
native execution. No game executable or disassembly is distributed here.

For an actual asset, record destination type/gates, mesh and MetaRig identities,
cache keys, names, matrices, masks, selected LOD, aggregate pose/float values and
backend/buffer identities for the same update. Compare D/P to the 48-byte output
after `0x140299360` and bounds before/after `0x140298533`. Check backend completion
and final vertices separately. This proposed procedure has not run and does not
establish all component subtypes or global IK/render ordering.
