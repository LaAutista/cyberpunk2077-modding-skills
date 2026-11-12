# Native BlendFromPose capture and curves

Companion to [native graph semantics](native-graph-semantics.md). Researched
2026-11-02 on CP2077 2.5 executable SHA-256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses are preferred-image VAs. These are static implementation findings and
analyst transcription checks, not execution of the game or its native bytes.
Use the named valid-data branches; revalidate a different build.

## Captured contribution

After evaluating its current input X, BlendFromPose obtains a captured pose Y.
Its capture wrapper `0x142741d98` invokes `0x140327fc4` for each 48-byte transform
record and stores the resulting contribution D on the equal-count capture path.
For XYZ translation, finite
nonzero scales and unit quaternions:

```text
D.t = rotate(conjugate(X.q), Y.t / X.s - X.t)
D.q = HamiltonProduct(conjugate(X.q), Y.q)
D.s = Y.s / X.s
```

Division is componentwise. The native translation rotates two terms separately;
this algebra does not promise identical float32 reassociation. Conjugation does
not normalize the quaternion. Static-initializer tracing established the sign
masks; reading zero-filled BSS would have missed them.

This is not a general affine inverse. With identity rotations, X.t=(2,0,0),
X.s=(2,1,1), Y.t=(6,0,0), Y.s=(2,1,1), it produces D.t=(1,0,0). Applying D at
full Local weight gives translation(4,0,0), not Y.t. For unit X scale the tested
round trips reconstruct Y. Preserve the actual branch; do not substitute a
preferred inverse or use the unit-scale fixture to certify nonunit scale.

Subsequent evaluation applies this saved contribution through Local additive
helper `0x140328f18` after evaluating the current input, with weight
`1-shapedProgress`. The capture input and present input can differ over time.

## Layout conversion

Count-different capture/application paths invoke `0x1403ab2a0` before the record
operation. It copies matching prefixes of three transform segments by index,
using minimum source/destination segment counts, then fills missing destination
tails from reference/default arrays or additive identity. It performs no name
lookup, parent reconstruction or coordinate conversion.

Scalar tracks also use segment copying/default tails, but the base scalar copy
uses the destination count without a minimum check, and the next segment assumes
the same base offset. Two validity bitsets copy whole words and zero additional
destination words; partial-word high bits are not independently cleared here.
Compatible segment order, base-track layout and capacities are preconditions.
Equal transform counts alone do not prove rig compatibility.

The count-different **capture** caller has a further hazard: at `0x142739ea6`,
it passes a newly allocated temporary as the conversion source, not the saved
capture pointer used in the equal-count branch. The traced temporary constructors
reserve arena storage and initialize metadata, not the pose payload. No saved
capture copy into that source appears on this path. More specifically, the mismatch
tests current X versus saved Y transform totals, while both fresh temporaries A/B
receive the same copied 18-byte node-context descriptor. On successful ordinary
disjoint reservations with stable compatible layout, conversion A→B copies every
logical transform/scalar segment and complete validity word; all missing-tail
lengths are zero in either mode. Reference-context metadata is still accessed.
Default tails therefore do not initialize this source.

The size helper performs only arithmetic; metadata follows reserved transform
storage, and logical third-segment counts can differ from reserved capacities.
Between A construction and conversion, the only call is B construction through
the same non-payload-writing chain. The subsequent difference reads X/B and
writes A's transforms; X still needs accessible compatible records. Prior child
evaluation reaches virtual+128 before A is reserved, so selected earlier writers
and actual A bytes remain history inputs. This conditional theorem does not
identify a live mismatch or an asset defect. Do not assume identity data or
silently correct the source. The later count-different **application** branch
explicitly passes the saved contribution and has a different source contract.
Private provenance: recovery `scratch-continuation` and its independent review;
byte-layout/source discriminators illustrate the static result, not native parity.

### Scratch lifetime on the connected normal host

The task supplies a backing pointer from `0x140a49f1c` and capacity 0x40000.
That leaf looks up a GS-derived execution key in a pool and returns a pre-existing
32-byte slot's pointer; it does not fill the buffer. With a stable slot/key
association, repeated calls reuse the same backing storage. The graph host
`0x1401b25dc` constructs a local arena descriptor with cursor0 each call and
passes it through graph context+0x28 to node context+0x18 and the temporary
constructors. The pointer is not a newly zeroed pose allocation.

Reservation `0x140326250` aligns and advances the cursor without writing payload.
Its returned pair contains the aligned offset and old cursor. Release
`0x1403ab654` restores that old cursor when temporary metadata exists; it clears
no bytes. Under valid capacities, alignment and nested lifetimes, a written
temporary can therefore be released and reallocated at the same address with
its old payload intact. The two simultaneously live temporaries in the captured
branch have separate reservations; constructing B does not initialize A.

This closes the normal reset/reuse contract, not the contents of any live pose.
Even zero-filled initial backing memory would not establish zero on later reuse.
Record preceding writers and the pre-read payload when reproducing the branch;
do not silently repair its source argument. Pool construction/external mutations
and other callbacks are not certified absent. Private provenance is
`transitions-deep/scratch-lifecycle-findings.md` and its retained-code/address
checks; no native execution was used to claim these values.

## Custom scalar curves

The separate node mode Smoothstep uses `clamp((3-2p)*p²,0,1)`. CustomCurve instead
dispatches through `0x1427413c0` on the curve's interpolation enum. The data
materializer `0x14093ba1c` supplies times, values and wrap flag0. Finite, nonempty,
sorted curve data and a valid enum are required; no safe empty/invalid-enum
fallback was established.

Time is clamped to the first/last key. Search `0x140498200` chooses the key at or
below it for strictly increasing times. Exact duplicate ties follow the search
path, not a guaranteed last-duplicate rule; all-equal keys select the last index.
Linear uses adjacent keys. Quadratic rounds the selected index down to a multiple
of2 and uses three indices; cubic and Hermite round down to a multiple of3 and
use four. Subsequent indices clamp to the last key on this path.

For each group, `u=(time-firstTime)/(lastTime-firstTime)` for positive span,
otherwise u=1. Interior Bezier times do not cause an inverse time-curve solve.
Let a=1-u:

| Enum / kernel | Scalar output |
| --- | --- |
| Constant / `0x140497d0c` | selected value |
| Linear / `0x14049815c` | a*P0 + u*P1 |
| BezierQuadratic / `0x140498a78` | a²*P0 + 2*u*a*P1 + u²*P2 |
| BezierCubic / `0x140497db4` | a³*P0 + 3*u*a²*P1 + 3*u²*a*P2 + u³*P3 |
| Hermite / `0x140e74f98` | (2u³-3u²+1)*P0 + (u³-2u²+u)*T0 + (u³-u²)*T1 + (3u²-2u³)*P1 |

Hermite stores P0,T0,T1,P1; its kernel uses tangents directly without multiplying
them by interval length. These kernels do not clamp the scalar result to[0,1].
The later Local additive application separately clamps its weight. Do not infer
looping from a separate helper's wrap branch: this data materializer supplies0.

## Discriminating evidence

Private research receipts in the owning workspace's
`animation-graphs-research/transitions-deep` include `capture-curve-findings.md`,
argument/constant/branch traces and two check scripts. Capture lane transcription
matched independent quaternion/rotation algebra in 128 seeded nonuniform-scale
cases and 128 unit-scale round trips. Curve search matched stdlib bisect in 1,632
strict-key cases; 256 Bezier evaluations matched independent de Casteljau checks.
Single-key, time-clamp, grouping and nonunit-interval Hermite checks also passed.
No game binaries or disassembly are distributed in this skill.

For an offline Blender reconstruction, preserve these capture histories, segment
contracts and actual curve types explicitly. A single current action or arbitrary
bone-name remap does not exercise this native behavior. These findings do not
identify the active game graph, final rendered pose or visual/gameplay acceptance.
