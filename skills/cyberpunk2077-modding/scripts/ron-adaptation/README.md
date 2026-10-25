# RoN pose adaptation helpers

Original MIT-licensed Python helpers for the recovered HK416-to-Cyberpunk workflow. They contain no game assets, extracted code, external-mod implementation, credentials or workspace paths. They accept evaluated matrices supplied by the caller; extraction, clip selection, native serialization and rendering remain separate.

Use Blender's Python environment (`mathutils.Matrix`, `Vector` and `Quaternion`). Add this directory to the invoking script's module search path, then import the needed function. There is no standalone command or automatic asset discovery:

```python
from ron_beta_index_correction import ads_trigger_index_sampler
from ron_beta_thumb_correction import preserve_source_thumb_segments
from ron_beta_source_auto_ik import solve_source_hand_targets, normalize_source_camera
```

| Helper | Inputs and output | Place in the pipeline |
|---|---|---|
| `ads_trigger_index_sampler(source_at, hk416_idle)` | Evaluated source-world sampler and HK416 idle matrices; returns a sampler with the ADS index baseline rebased. | Only the explicitly selected ADS firing/last-shot body sampler, before retargeting. |
| `preserve_source_thumb_segments(desired, tr, rl, source, A, side='Left')` | Target desired world matrices, native bind world matrices, native reference local matrices, source world matrices, source-to-target matrix. Mutates only three left-thumb desired matrices and returns measurements. | After target finger IK, before arm IK and native-local reconstruction. Right side deliberately returns without changes. |
| `solve_source_hand_targets(world, local, parents, anchor, sides=('le','ri'))` | Evaluated source world/local matrices, bone-parent mapping, source idle world pose; returns solved world/local matrices and diagnostics. | Source automatic states whose recovered graph ends in static-weapon hand targets; before retargeting. |
| `normalize_source_camera(world, anchor)` | Solved source world pose and source idle world pose; returns a common camera-space transform of all world matrices. | Only when adapting to an intentionally fixed target camera. Recompute locals after this transformation if a downstream consumer requires them. |

The index helper computes each selected local rotation as `q(t) * inverse(q(0)) * q(idle)`. It preserves the source trigger-pull delta and changes only `index_2_ri`, `index_3_ri`, `index_4_ri` and the propagated `index_5_end_ri`. The MCP world position is preserved exactly because it also defines the palm centroid. It is specific to the shared ADS firing offset observed when composing on HK416 idle; do not apply it to arbitrary animations.

The thumb helper preserves native segment lengths and aligns the first two segment directions to the source. The previously aligned distal orientation, including nail roll, remains unchanged. Native-local reconstruction must preserve reference translations/scales and propagate helpers through their existing parents. This is not a general hand-pose replacement.

The automatic helper uses `IK_current @ inverse(IK_idle) @ hand_idle`, a two-bone arm solve, and the current elbow plane. It retains current finger locals. Required names include `upperarm_le/ri`, `lowerarm_le/ri`, `hand_le/ri`, `ik_hand_weapon_static_le/ri`, and `fp_camera` for camera normalization. Local and world dictionaries must represent the same evaluated hierarchy and units. Degenerate/unreachable arm solves raise errors; do not suppress them or stretch the skeleton to force success. The small original `qmat`, `two_bone` and `orient_segment` implementations are embedded, so the portable module has no project-tool import.

These routines preserve the existing native-rest and all-weight-set skinning workflow; they do not read, limit or rewrite skin influences. The automatic solve is an explicit geometric adaptation, **not** an emulation of the source graph's LegIK, blend alpha, montage selection or procedural camera. No helper evaluates Cyberpunk's muscle graph, runtime IK, physics or event dispatch. Mathematical equivalence and offline renders do not establish gameplay behavior or collision-free skinning.

Extraction validation used actual recovered inputs: start/middle/end samples from all three automatic source clips, native PMA/PWA thumb idle and empty-reload contact samples, and all 61 ADS firing source frames. Portable and canonical modules were compared directly against the project originals. Keep local receipts with the project, including source hashes, changed-bone limits and visual/native/runtime boundaries; no extracted fixtures are distributed here. See the accompanying [MIT license](LICENSE).
