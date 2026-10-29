# Target animation semantics

Identify the exact target .rig/.anims, selected clip and native animation type.
Do not infer Normal/Additive/AdditiveWithoutFirstFrame from a filename. Preserve
events, float tracks, fallback rows, extraction metadata and unrelated payloads.
The current writer's version/format limits are in
[native authoring](../../cyberpunk2077-modding/references/native-animation-authoring.md).

For that helper's bind-relative interchange contract, with original native local
bind B, intended normal base L and desired pose P:

```text
D.T = P.T - L.T
D.Q = inverse(L.Q) * P.Q
D.S = P.S / L.S
E.T = B.T + D.T
E.Q = normalize(B.Q * D.Q)
E.S = B.S * D.S
```

This is a named adapter contract, not a universal source additive formula. First
evaluate the source with its own base/order; then derive target deltas. Test
noncommuting rotations and nonunit base scale. Guard zero scales and missing scale
semantics; absent additive scale is not automatically an absolute unit-scale track.
Strip the bind exactly once. Preserve the first sample even for
AdditiveWithoutFirstFrame; do not delete it based on the type name.

Preserve real stored key times, constant/hold keys and terminal endpoints. Header
numFrames is not the stored key count. Raw keyed and SIMD-resampled output need
different evidence; inspect serialized times independently. Tiny rotations with
float32 W == 1 and nonzero XYZ must not silently become identity.

Keep FK and graph-required controls in agreement in updated destination space,
including player/weapon anchors and each supported PMA/PWA variant. Offline
agreement cannot establish graph selection or native runtime constraint behavior.
See [events and native export](../../cyberpunk2077-modding/references/animation-retargeting/events-native-export.md).

Advice to zero numTracks to cure flicker is unverified troubleshooting here. Do
not apply it blindly: it can remove meaningful float tracks. Preserve the original,
isolate one clip and compare actual native metadata plus runtime behavior before
accepting any such source-specific workaround.
