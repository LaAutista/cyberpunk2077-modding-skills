# Native gate: reuse the existing implementation

Use the sibling [native animation authoring commands](../../cyberpunk2077-modding/references/native-animation-authoring.md).
Do not add a second native writer or a receipt-only substitute for byte readback.
Confirm the installed WolvenKit/.NET versions and the helper's supported codecs,
animation types, events and root-motion limitations before running it.

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
