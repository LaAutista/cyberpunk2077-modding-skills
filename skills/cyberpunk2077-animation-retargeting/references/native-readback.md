# Native gate: reuse the existing implementation

Use the sibling [native animation authoring commands](../../cyberpunk2077-modding/references/native-animation-authoring.md).
Do not add a second native writer or a receipt-only substitute for byte readback.
Confirm the installed WolvenKit/.NET versions and the helper's supported codecs,
animation types, events and root-motion limitations before running it.

The [agent native runner](agent-tools.md#run-the-native-gate-from-one-fixture)
orchestrates this existing sequence from one private config, with fresh baseline
exports, hash-checked resume, retained failures and bounded execution. Use it when
the fixture fits the existing selected-clip adapter.

Start with copies of the compatible original container and matching rig. Run an
unchanged roundtrip and one controlled channel edit, then the selected single clip.
Keep the expectation from the unprepared authoring input. Reusing the serializer's
intermediate arrays as readback makes the check circular.

The existing sequence provides:

1. `native-animation.sh` export/import against installed native tooling.
2. `check-animation.mjs prepare --preserve-key-sampling` with one-time additive
   preparation guards, followed by actual native import and CR2W serialization.
3. `readback-animation.mjs` independently decoding stored bytes with
   `--required-clips`, taking native/rig JSON and CLI GLB, not authored values.
4. `check-animation.mjs verify` comparing keys/time/values and untouched payloads.
5. `verify-semantics.mjs` comparing metadata, events, floats, scale and fallback
   tables against original/native/rig/authored/original-GLB inputs.

Use the exact argument order and environment in the linked command contract.
These commands need owned native fixtures; the following portable suites need no
game and do not replace that run (from the repository root):

```sh
node skills/cyberpunk2077-modding/scripts/native-animation/test-native-animation.mjs
node skills/cyberpunk2077-modding/scripts/native-animation/test-beta-additive.mjs
```

Fail the native gate on changed untouched clips, unexplained metadata changes,
missing endpoints/holds or out-of-tolerance readback. Do not widen tolerances or
declare a beta ready after import alone. Re-extract the final archive and hash
its resources against these checked native inputs; container pass does not prove
the packager shipped them. Native pass still leaves visual/runtime gates separate.

## Coupled hand and prop sampling

A common world-space correction can preserve hand/prop contact analytically yet
lose it when their local translation and quaternion curves interpolate separately.
Passing stored-key readback does not check that approximation. Compare the exact
native pair against the approved motion at changed keys, between keys and phase
boundaries, including controls, hand/prop relative transforms and surrounding
anatomy. Reuse the project sampler and actual readback; label its interpolation
contract and keep game composition unverified.

When a key passes but a midpoint fails, compare authored and native playback at
both times before changing the pose. If both have the same midpoint error, refine
only the affected channels/time window on the native clock, then repeat the joined
check and visual review. Preserve the approved analytic motion, unrelated keys,
T/S, events and insertion/release timing. Choose sampling from measured residuals;
do not universalize a weapon-specific cadence or loosen the raw-value tolerance.
The `coupled-between-key-contact` workflow case exercises this failure class.

## Cumulative candidate preservation

When merging a new clip into an existing port, identify the intended complete
candidate and the actual native importer baseline separately. Selected-clip import
preserves **its supplied native baseline**, not unselected clips that happen to be
present in an editor/authored GLB. A stale baseline can silently restore an older,
broken reload while every unchanged-clip comparison against that same baseline
passes.

Keep a per-weapon list of previously approved clip/variant identities and their
required motion/metadata. Verify those requirements against the final native
readback after each merge, as well as comparing newly authored channels. Preserve
current unrelated motion, translations/scales, timing, events and floats. A lost
approved correction fails the merge even when the isolated new clip passes. Check
aliases rather than assuming the primary action covers them. Re-extract the final
archive and confirm that it ships the checked banks, then run the required
[final-readback clipping audit](../../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#final-readback-clipping-audit).
