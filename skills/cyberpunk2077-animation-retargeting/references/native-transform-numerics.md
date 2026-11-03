# Measured native composition and quaternion interpolation

Use these measurements to check an offline pose model's transform order,
interpolation branch and write footprint. They extend the separate
[normalization measurement](native-normalization.md), not whole-graph parity.
The [graph semantics](native-graph-semantics.md) identify the callers and equations.

Build: Cyberpunk 2.5, executable SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses are preferred-image addresses for this saved build, not portable hooks.
Exact unmodified bytes ran in isolated Linux fixtures on an AMD Ryzen 7 7800X3D
with GCC 16.2.1's Microsoft ABI bridge. Compiler argument/result handling was
reviewed. Code was RX, constants/first inputs read-only, output writes guarded;
owned mappings and MXCSR were restored. Changed payloads were rejected before
mapping/execution. No game loader, game process, mod or character asset ran.

Both fixtures used masked exceptions and round-to-nearest with gradual underflow
(`1F80`) and FTZ+DAZ (`9FC0`). These are fixture settings, not measured game values.
They reused the bounded guard and preserved predeclared tolerances and failures.
No game code or executable is distributed with this skill. The experiments do
not authorize new target execution or attachment.

## Composition order, scale and input domain

The complete 214-byte leaf `0x14032911C..0x1403291F1` ran 1,039 input pairs in both
MXCSR modes: 2,078 calls and 24,936 output lanes. All lane bits matched a separate
float32 instruction-order model. For 2,058 ordinary comparisons, an independent
double rotation-matrix/Hamilton-product reference passed the declared limits:
translation `2e-5 + 2e-6*abs(reference)`, quaternion component `1e-6`, scale
`2e-6*max(1,abs(reference))`. Maximum absolute errors were respectively
`6.881328744157145e-6`, `8.15454148650474e-8` and `4.7390022928084363e-7`.

Ordinary inputs had translations in [-10,10], rounded unit orientations and signed
nonuniform scales with magnitudes .25 to 4, plus identified identity/zero-scale
examples. 512 deterministic pairs ran in both orders. For
X = t(1,2,3), q(X90), s(2,3,4) and
Y = t(5,6,7), q(Y60), s(.5,1.5,2):

| Composition | Measured translation | Measured quaternion xyzw | Scale |
| --- | --- | --- | --- |
| C(X,Y) | (11,-26,20.9999981) | (.6123724,.3535534,.3535534,.6123724) | (1,4.5,8) |
| C(Y,X) | (10.4461517,9,9.5669870) | (.6123724,.3535534,-.3535534,.6123724) | (1,4.5,8) |

The leaf does not normalize input/output quaternions. Doubling X.q changes the
first translation to (11,-164,-9.0000076) and leaves output quaternion norm about
2; that is a diagnostic outside the ordinary contract, not a valid rotation.
The fourth translation/scale lanes also participate: X.tw=3, X.sw=2, Y.tw=4,
Y.sw=-3 yield output tw=11 and sw=-6. Do not silently force these lanes to 0/1
when comparing stored QS bytes. A minimum-subnormal translation survives in
gradual mode and becomes zero with FTZ+DAZ; scale multiplication has the same
mode-sensitive underflow boundary.

This QS operation has no general shear representation. A finite passing corpus
does not make it equivalent to unrestricted affine-matrix multiplication, prove
aliasing, or establish the selected caller's scales or quaternion validity.

## Interpolation branch and second-input mutation

The complete helper `0x14032A664..0x14032A754` ran with its exact normalization,
acos-clamp, native acosf/sinf and three tiny MXCSR dependencies. The latter allow
the ordinary zero-dot acos path without replacing exception handling by a stub.
Eight admitted code ranges total 2,782 bytes. Sparse code/constant pages retained
the original relative displacements. Unadmitted code and out-of-scope CRT
NaN/domain-error/huge-sine helpers were not available for silent fallback.

Neither sine dispatch global `0x14397C57C` nor signmask `0x143BF66D0` has file
backing. The fixture explicitly tested dispatch 0 (baseline SSE) and 1 (AVX/FMA),
and initialized the signmask to the four sign bits copied by initializer
`0x140076790`. These are declared fixture inputs, not recovered live values.
Two failed file reads were retained; a separate backing check identified both
unbacked globals before execution.

1,116 quaternion/weight rows ran in both dispatches and both MXCSR modes:

- All 4,464 calls returned finite outputs and exactly the expected second-input
  hemisphere write, with no writes outside that quaternion's 16 bytes.
- 4,396 ordinary comparisons passed independent double-reference component and
  norm limits of `1e-6`; maxima were `1.3048589142528044e-7` and
  `1.3931558284774326e-7`. Inputs were rounded unit quaternions and seven weights
  in [0,1], including orthogonal/antipodal, near-parallel and 128 random pairs.
- All 560 ordinary normalized-linear results also matched the float32 model
  bit for bit. SLERP was checked against independent double trigonometry;
  do not describe it as an exhaustive bit-exact CRT transcription.
- All 24 threshold discriminators selected SLERP at absolute-dot bits
  `3f7d70a3` and `3f7d70a4`, and normalized linear interpolation at `3f7d70a5`.
  At weight .25, the other formula missed by about `4.4333e-5`; the selected
  formula's error was below `1.43e-8`. Equality belongs to SLERP.
- The two sine dispatches produced identical output bits in this corpus. That
  does not establish every input/CPU path or the game's selected dispatch.

The sign decision uses the dot's **sign bit**, including negative zero. The
second quaternion is overwritten with the sign-adjusted bits before either
branch, including endpoint weights. Preserve that effect when the caller reuses
the buffer; a pure function returning only the blended quaternion misses it.

SLERP does not add a final normalization. For q0=(0,0,0,1), q1=(2,0,0,0), w=.5,
the diagnostic output is approximately (1.41421354,0,0,.70710677), not unit length.
Two zero quaternions return zero, not identity. With an orthogonal unit pair,
minimum-subnormal weight yields x bits `00000002` in gradual mode and zero with
FTZ+DAZ. These diagnostics do not establish that such inputs reach a real graph.

Private provenance: `blending-deep/compose-leaf/` and
`blending-deep/interpolate-leaf/`, each with pre-execution contract, exact-byte
admission, compiler review, native log, independent checker and hash verification.
The wider investigation still needs weight/mask thresholds, event seams, Euler
poles, other native numerical paths, selected inputs/lifetimes, fresh independent
review and final visual/game acceptance. These measurements do not diagnose or
repair a stretched character by themselves.
