# Measured quaternion normalization limits

Use this when a simplified normalization model disagrees with native pose math.
This is one fixed-build leaf, not whole-graph numerical parity or a character fix.
See [composition and interpolation](native-graph-semantics.md) for its caller.

Cyberpunk 2.5 executable SHA256:
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Leaf `0x14032AF60..0x14032AFB8` is exactly 89 bytes/25 instructions, including
return. It reads a quaternion xyzw through RCX and the original ones constant
at `0x1437BBAE0`, returning XMM0. It makes no external calls or target stores.

## Actual execution scope

The exact saved bytes ran in an isolated Linux fixture on an AMD Ryzen 7 7800X3D,
using GCC 16.2.1 and its Microsoft ABI attribute. The wrapper's argument/result
and MXCSR order were checked in compiler output. Only the code page was RX;
input and constant pages were read-only. The original RIP displacement was
preserved. No game loader, CRT, graph, game process or mod was started or changed.
The fixture used the existing bounded-job guard, restored MXCSR and unmapped its
owned regions. Changed code/constant files were rejected before execution.

This ABI bridge follows [GCC's ms_abi attribute](https://gcc.gnu.org/onlinedocs/gcc/x86-Attributes.html)
and [Microsoft's x64 argument, vector-return and MXCSR contract](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170).
Those references explain the wrapper; the numerical result comes from the
identified bytes, not documentation. No executable or game bytes are distributed
with this skill, and this measurement does not authorize another target run.

920 synthetic inputs ran under each of two explicit modes: masked exceptions and
round-to-nearest with gradual underflow (`1F80`), then FTZ+DAZ (`9FC0`). These
settings are fixture inputs; the game's setting was not measured.

- All 1,834 finite-input output pairs matched the float32 instruction-order
  model bit for bit on this host. This is a finite corpus, not universal parity.
- For 880 ordinary inputs in both modes, the largest component error against
  independent double-precision `q/math.hypot(*q)` was `1.1824903245472029e-7`;
  maximum norm error was `1.1824966472673282e-7`. Both passed the predeclared
  `3e-7` limits. The corpus has 624 nonzero signed grid vectors with norms in
  [.5,2] and 256 deterministic nearly parallel mixtures.
- The mixtures straddle the documented .99 input-dot threshold, but only their
  normalization ran. They do not execute the interpolation branch or SLERP.
  Nonfinite inputs were classified separately, without a NaN-payload guarantee.

## Finite does not imply safely normalizable

Each arithmetic step rounds to float32. The grouping is
`s=(x*x+y*y)+(z*z+w*w)`, then `n=sqrt(s)`, `r=1/n`, output `r*q`.
A final mask clears every lane when the computed n equals zero. Division and
multiplication precede the mask, so zero input still sets masked exception flags.
It is not an early zero return or identity fallback.

| Input xyzw | Gradual underflow | FTZ+DAZ |
| --- | --- | --- |
| (0,0,0,0) | all +0; status flags 05 | all +0; status flags 05 |
| (2^-75,0,0,0) | all +0 | all +0 |
| (2^-74,0,0,0) | (1,0,0,0) | all +0 |
| (2^-64,0,0,0) | (1,0,0,0) | all +0 |
| (2^-63,0,0,0) | (1,0,0,0) | (1,0,0,0) |
| (2^64,0,0,0) | all +0 | all +0 |
| (2^63,2^63,2^63,2^63) | all +0 | all +0 |
| (+infinity,0,0,0) | (NaN,0,0,0) | (NaN,0,0,0) |
| (quiet NaN,1,0,0) | all NaN | all NaN |

A stable double normalization returns a unit vector for the tiny/huge finite
examples, so replacing this leaf by that formula loses native behavior there.
Establish the selected caller's input range and floating-point mode before
using those cases to diagnose a real asset. The ordinary finite sample contract
does not establish every reachable input, CPU path or rounding mode.

Private provenance: `blending-deep/normalize-leaf/CONTRACT.md`, `admission.json`,
`build2.json`, `check2.json` and `verification.json`. The first completed run had
one output row split by buffered stdout/stderr; the checker rejected it. Flushing
stdout before the final status fixed the wrapper only, and a complete rerun
passed. Original failure, bytes, inputs and acceptance limits were preserved.

The later [transform measurements](native-transform-numerics.md) execute the
interpolation selector and native trig dependencies, signed nonuniform-scale QS
composition, masked kernels, weight prefixes and inverse-Euler pole branches on
separate finite corpora. None comes from this normalization-only run. Event seams,
remaining constraint/skinning numerical paths and wider domains remain outside
those measurements. Independent review has separate retained records; selected
game inputs and visual/game acceptance remain separate.
