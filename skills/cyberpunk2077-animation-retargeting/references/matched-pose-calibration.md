# Matched reference calibration and optional mesh pose-back

Neto's 10 November 2026 handoff describes a useful distinction: animation transfer saves a relationship between posed rigs; a replacement-mesh port can also invert a measured deformation. This guidance adapts those principles. The supplied Starfield/FO4 reports are historical claims; no Cyberpunk port or full-body application has been validated by this document.

## Animation calibration

Keep the working source evaluator and native exporter. Pin the actual source reference, native skeleton, skin, per-mesh inverse binds and required helper evaluation. Pose the destination reference onto the source reference by rotations, preserving native anatomical local translations, lengths and scales. Keep any positive uniform comparison scale/placement outside runtime bone channels. A neutral/setup match and a weapon-specific grip/contact adaptation are separate inputs.

Assess actual evaluated skin from matched views. When fitting numerically, use both directions of corresponding surface distance, sampled by area and restricted by side, digit and anatomical region. Match knuckles, thumb opposition, pads and segment roll as well as tips. Exclude only unsupported overhang, retaining supported surfaces as evidence. A smaller surface inside a larger one or a tip matched to a neighboring finger must not receive a false fit pass. Surface distance alone does not clear clipping, containment or contact.

For proper world rotations in a declared common frame and column-vector convention:

```text
C_i = transpose(S_reference_i) * T_matched_i
T_world_i(t) = S_world_i(t) * C_i
T_local_i(t) = transpose(T_world_parent_UPDATED(t)) * T_world_i(t)
```

Choose the root frame explicitly and convert out of comparison space before native serialization. Rebuild positions with native local offsets. This is one orientation-transfer model, not a solution for source translation, reach, helpers or contact. A local-delta adapter may remain appropriate; do not mix the two multiplication conventions.

Check that the source reference reproduces the matched destination reference. A common rigid rotation of source parent and child should rotate their mapped world orientations while leaving the mapped internal pose unchanged. Use noncommuting rotations and a changed destination parent. For optional bilateral transfer, reflect the **rotation delta** through the character's measured symmetry frame and each side's native rest axes; preserve each side's original offsets and proper rotations. Do not mirror the skeleton by negative scale.

The existing source-motion inventory, finger checkpoint, native readback and full source/native review still apply. Helpers must be mapped by function. Record source, matched-reference, native-bind and comparison-transform identities independently; a matched pose does not become a new native bind.

## Optional replacement-mesh operation

This step belongs only to an expressly requested mesh port. It is not required for animation retargeting or permission to resume a deferred character project.

After a measured native-to-incoming surface match, transfer native weights using anatomically restricted triangle correspondence and barycentric interpolation. With the complete established per-bone skinning transform `D_i` in one common mesh frame, fixed normalized final weights `w_vi`, and incoming posed vertex `y_v`, form:

```text
A_v = sum_i(w_vi * D_i)
x_v = solve(A_v[0:3,0:3], y_v - A_v[0:3,3])
```

For the conventional common-space case, `D_i = P_i * inverseBind_i`. Include the actual object/mesh factors when that simplified form does not apply; control rests are not substitutes for per-mesh inverse binds. Invert the weighted blend, never a weighted sum of per-bone inverses. Check finite inputs, normalization, conditioning and physical-unit residuals. Preserve singular failures rather than masking them with a pseudoinverse or guessed fallback.

Restore the native skeleton/bind and re-pose the result using the same weights and deformer stack. Verify both the algebra and actual reopened/exported evaluation. Weight edits invalidate the original round-trip result. Active correctives, dual-quaternion skinning and nonlinear deformers require a separately established treatment. Temporary authoring length factors are not native animation changes and are excluded from this default calibration.

Keep seam, morph-driver, skin-helper and contact validation separate. Starfield scales, drift thresholds and residuals are not Cyberpunk defaults; full-body, outfit and armour transfer remain new validation work.
