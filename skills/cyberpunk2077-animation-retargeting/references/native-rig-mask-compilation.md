# RigPart compilation and dynamic-mask prerequisites

Use this with [BlendByMaskDynamic](native-blend-operators.md#blendbymaskdynamic)
when the compiled mask differs from its authored single-bone/tree descriptors.
These are static findings for Cyberpunk2.5 EXE SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`,
preferred base140000000. Re-establish type/table identity on another build.
Private `shared-pose-deep/rig-mask-producer-findings.md` and its check/guard
receipts retain the evidence; none is an installed dependency or runtime proof.

## Typed producer and output

animRig registration141058EC8, constructor140D33484 and primary1430F03F8 join
the actual+28 hook14138A9FC to compiler1404B74D8. Its rig130/count13C loop
calls140A20B78 on each88-byte part. The dynamic-mask evaluator140B3BB94 reads
the same array/stride. Each part holds derived ordinary pairs at8/count14,
source singles18/count24, source trees28/count34, source special names38/count44,
and derived special indices48/count54. Ordinary pairs are8-byte full signed32
index plus float weight; special indices are DWORDs.

Each part build clears both derived counts, then:

1. Visit source singles in order. Resolve each name; skip lookup−1. Append only
   if the full32-bit index is absent, copying the weight bits unchanged.
2. Visit source tree descriptors in order. A missing root skips that entire
   descriptor, including its nested descriptors. Otherwise visit nested trees
   first, add the root if absent, then recursively add its later-index descendants.
3. Sort ordinary pairs by signed32 index, carrying their weight bits.
4. Resolve special names independently, remove duplicates within that special
   list, and sort its signed32 indices. No ordinary-membership filter is applied.

Thus **first insertion wins**: singles outrank trees, earlier top-level trees
outrank later ones, and nested trees outrank enclosing defaults. Existing bone
membership does not prune its descendants. A nested root need not belong to the
outer subtree. There is no weight clamp or normalization in this builder.

Tree scans only visit child indices greater than their parent. Covering the
intended hierarchy requires parent-before-child ordering; parents[-1,2,0] and
root2 omit child1. Source nested descriptors also need finite, noncyclic valid
storage; this recursion has no visited-set guard.

The actual small insertion and larger median-partition/heap sort branches are
traced for both derived lists. Counts and pair payloads are preserved. Uniqueness
comes from membership checks before sorting, not from the sorter. Valid storage,
nonoverflowing counts and successful allocation/copy remain premises.

## Special rotations require more than two sorted lists

The consumer's special cursor starts at0, advances only on an exact match with
the current ordinary index, and saturates at the final special entry. It does
not skip smaller unmatched special indices.

| Compiled ordinary indices | Compiled special indices | Special matches |
| --- | --- | --- |
| [2,4] | [1,4] | none |
| [1,4] | [1,2,4] |1 only |
| [1,4] | [1,4,7] |1 and4 |

The first row can be produced from singles bone2/.4,bone4/.5 and special names
bone4,bone1,bone4. Both arrays are valid, unique and sorted, yet the cursor stalls
at1. This is a builder-admitted counterexample, not a diagnosed game asset.
Special-set inclusion in the ordinary set is sufficient only when every preceding
matching ordinary entry also passes the consumer's validity checks. A rejected
ordinary entry can leave the cursor behind. Preserve compatible pose counts,
parent arrays and the [mutable parent rotation contract](native-graph-semantics.md#dynamic-mask-hierarchy-rotation).

## Name-map encoding and repeated compilation

The rig compiler appends16-byte name records, storing each ordinal's low16 bits,
then sorts by unsigned64 name key. Lookup140286E6C uses lower-bound/exact-key
matching and sign-extends that16-bit ordinal. Zero/missing names return−1.
Duplicate names are not rejected; the first sorted equal-key record wins, with
no guaranteed authored order for larger equal-key sets.

For valid ordinals below32768 this supplies canonical nonnegative indices.
Ordinal32768 becomes−32768;65535 becomes−1 and is skipped;65536 wraps to0.
It cannot emit fullDWORD00010001 from ordinal65537: the returned index is1.
No local count-range check repairs an unsupported rig. Consumer signed16 count
admission and parent-table indexing also need a compatible supported range.

The map reserve helper140434E20 does **not** reset its logical count at rigA4.
Fresh constructor140D33484 clears QWORDA0, including that count, but the inspected
compiler appends to the current map. Repeated compilation therefore needs an
external reset that has not been traced. This differs from the unconditional
per-part14/54 clear. Optional pre-part rig hooks receive the rig and remain
unexpanded; their potential writes are not assumed absent. Other producers and
post-part work are likewise outside this local guarantee.

For a real diagnosis record the authored names/weights/trees, resolved map,
compiled ordinary/special arrays, actual count/index admission and selected
operator. The finite compiler and cursor checks do not establish those inputs,
native floating-point behavior, rendered deformation or Saber acceptance.
