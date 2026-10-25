"""Bounded source-space hand-target adaptation, not a RoN graph emulator.

The recovered graph ends in LegIK nodes targeting the static weapon hand bones.
This analytic two-bone solve preserves the current source elbow plane and all
finger locals. Runtime LeftHandIKAlpha and native auto-montage selection remain
unverified. The source idle hand/target calibration is preserved explicitly.
"""
import math


def qmat(q, p):
    m = q.normalized().to_matrix().to_4x4()
    m.translation = p
    return m


def two_bone(start, end, pole, l1, l2):
    v = end - start
    d = v.length
    if d < 1e-8 or d > l1 + l2 + 1e-6 or d < abs(l1 - l2) - 1e-6:
        raise ValueError(('unreachable', d, l1, l2))
    axis = v.normalized()
    bend = pole - start
    perp = bend - axis * bend.dot(axis)
    if perp.length < 1e-7:
        raise ValueError('Degenerate IK pole')
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0, l1 * l1 - x * x))
    return start + axis * x + perp.normalized() * h


def orient_segment(ref, child, p, end):
    old = (child.translation - ref.translation).normalized()
    new = (end - p).normalized()
    return qmat(old.rotation_difference(new) @ ref.to_quaternion().normalized(), p)

def solve_source_hand_targets(world, local, parents, anchor, sides=('le','ri')):
    desired={}; diagnostics={}
    for side in sides:
        upper='upperarm_'+side; lower='lowerarm_'+side; hand='hand_'+side
        ik='ik_hand_weapon_static_'+side
        target=world[ik]@anchor[ik].inverted()@anchor[hand]
        shoulder=world[upper].translation; wrist=target.translation
        elbow=two_bone(shoulder,wrist,world[lower].translation,
                       (world[lower].translation-shoulder).length,
                       (world[hand].translation-world[lower].translation).length)
        desired[upper]=orient_segment(world[upper],world[lower],shoulder,elbow)
        desired[lower]=orient_segment(world[lower],world[hand],elbow,wrist)
        desired[hand]=target
        diagnostics[side]={'wristShiftMeters':(wrist-world[hand].translation).length,
                           'calibration':'IK_current @ IK_idle^-1 @ hand_idle',
                           'fingerLocals':'retained from current source clip'}
    solved={}; solved_local={}
    def visit(n):
        if n in solved:return solved[n]
        p=parents[n]
        if p:visit(p)
        solved[n]=desired[n] if n in desired else (solved[p]@local[n] if p else local[n].copy())
        solved_local[n]=solved[p].inverted()@solved[n] if p else solved[n].copy()
        return solved[n]
    for n in world:visit(n)
    return solved,solved_local,diagnostics

def normalize_source_camera(world, anchor):
    """Map current source camera to its idle camera; preserves relative anatomy.

    Only appropriate when the target camera is fixed. This is an explicit
    camera-space adaptation, not evidence that native RoN performs this step.
    """
    correction=anchor['fp_camera']@world['fp_camera'].inverted()
    return {n:correction@m for n,m in world.items()}
