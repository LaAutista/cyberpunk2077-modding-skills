"""Source-segment thumb correction demonstrated in offline left VTK idle views.

This does not evaluate native muscle constraints or establish runtime acceptance.
Call after the finger IK loop and before arm IK. Only the three left thumb
desired world matrices change; corrected_locals must subsequently reconstruct
the final pose using the unchanged native reference local translations/scales.
"""
import math
from mathutils import Matrix


def _angle(a, b):
    a, b = a.normalized(), b.normalized()
    return math.degrees(math.atan2(a.cross(b).length, a.dot(b)))


def preserve_source_thumb_segments(desired, tr, rl, source, A, side="Left"):
    """Mutate only left thumb desired matrices; return diagnostic measurements.

    tr: native bind world matrices. rl: native reference local matrices.
    source: untransformed evaluated source world matrices. A: source-to-player.
    The already aligned distal world orientation (including nail roll) remains
    unchanged. Native lengths are retained, so the distal position can move.
    Right is deliberately a no-op because the demonstrated defect is left-only.
    """
    if side not in {"Left", "Right"}:
        raise ValueError(f"Unknown hand side: {side}")
    if side == "Right":
        return {"applied": False, "reason": "Only left thumb validated offline"}
    chain = ["LeftInHandThumb", "LeftHandThumb1", "LeftHandThumb2"]
    src = ["thumb_1_le", "thumb_2_le", "thumb_3_le", "thumb_4_end_le"]
    directions = [A.to_3x3() @ (source[src[i + 1]].translation - source[src[i]].translation)
                  for i in range(3)]
    if any(v.length < 1e-8 for v in directions):
        raise ValueError("Degenerate source thumb segment")
    start, mid, end = chain
    original = {n: desired[n].copy() for n in chain}
    q0 = original[start].to_quaternion().normalized()
    q1 = original[mid].to_quaternion().normalized()
    q2 = original[end].to_quaternion().normalized()
    # First swing rotates the inherited child frame just as FK propagation
    # does in the copied-pose experiment. The second swing acts from that frame.
    swing0 = (q0 @ rl[mid].translation).normalized().rotation_difference(directions[0].normalized())
    q0 = (swing0 @ q0).normalized()
    q1 = (swing0 @ q1).normalized()
    swing1 = (q1 @ rl[end].translation).normalized().rotation_difference(directions[1].normalized())
    q1 = (swing1 @ q1).normalized()
    p0 = original[start].translation
    p1 = p0 + q0 @ rl[mid].translation
    p2 = p1 + q1 @ rl[end].translation
    for n, q, p in zip(chain, [q0, q1, q2], [p0, p1, p2]):
        desired[n] = Matrix.LocRotScale(p, q, original[n].to_scale())
    native_axis = tr[end].to_quaternion().inverted() @ (tr[end].translation - tr[mid].translation)
    actual = [p1 - p0, p2 - p1, q2 @ native_axis]
    return {
        "applied": True,
        "changedBones": chain,
        "distalJointShiftM": (p2 - original[end].translation).length,
        "segmentDirectionErrorsDeg": [_angle(actual[i], directions[i]) for i in range(2)],
        "jointBendDegrees": [_angle(actual[i], actual[i + 1]) for i in range(2)],
        "sourceBendDegrees": [_angle(directions[i], directions[i + 1]) for i in range(2)],
        "distalSourceAxisErrorDeg": _angle(actual[2], directions[2]),
        "distalOrientationPreserved": True,
        "runtimeVerified": False,
    }
