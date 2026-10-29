# Source adapter boundary

The adapter owns decoding and source interpretation. Emit a canonical skeleton
(names, parents, reference-local T/Q/S), clip (seconds, original key/sample times,
local T/Q/S, interpolation, animation type/base, events/curves), assembly (player
anchor, weapon root, component mounts/sockets and mechanism ownership) and evidence
(source hashes, decoder version, unsupported semantics). Keep original sparse keys
and sample cadence; a sampled fixture is evidence, not permission to resample assets.

| Source | Establish before retargeting |
| --- | --- |
| RoN / Unreal | Actual package/build, complete motion skeleton, arm/weapon clip pairing, component sockets and clocks, source additive base/order, translation-retarget modes, graph/curve/visibility contributions. The recorded 292-bone HK416 source and 152-bone target are case identities, not required counts. |
| FO4 / HKX | Decoder/codec identity, full skeleton and binding, actual per-file clock, blend/additive definition, assembly/annotation ownership and independently evaluated playback. Header inspection or an unexecuted HKX library is not decode proof. |
| Max / M1911 | Scene/take identity, effective frame ticks and export sampling, weighted terminal helpers, per-component clocks and independent native-to-interchange comparisons. A 60 fps header can still contain 30 Hz motion. Unadmitted multi-block clips remain OPEN. |
| New source | A bounded decoder fixture and explicit semantics; no borrowed weapon offset or one-click conversion claim. |

The Cyberpunk target adapter owns native hierarchy/reference locals, player/weapon
anchors, PMA/PWA differences, required control synchronization, target additive
representation, events/floats and container semantics. Source-specific assumptions
must not be hidden in that adapter.

Use [source playback/adapters](../../cyberpunk2077-modding/references/animation-retargeting/source-playback-adapters.md)
and [RoN extraction](../../cyberpunk2077-modding/references/ron-source-extraction.md)
for existing bounded routes. The [evidence register](../../cyberpunk2077-modding/references/animation-retargeting/evidence-register.md)
pins dated receipts; refresh the owning project's status before execution.

General humanoid rest-pose/Rokoko guidance is an alignment reference only. It does
not authorize omitting weapon roots/trajectory, scaling anatomy, dropping controls
or changing a first-person container. External advice is a hypothesis until a
version-matched fixture discriminates it.
