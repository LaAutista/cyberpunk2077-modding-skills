"""ADS-only right-index baseline rebase for the shared G36C firing delta.

The recovered ADS clip contains a persistent finger offset when composed on the
HK416 idle. Rebase its three index rotations at frame zero onto HK416 idle while
retaining each time-varying local rotation delta. Do this before retargeting.
No other source bone is changed. This is a port-specific adaptation, not a claim
about the source game's complete procedural graph or runtime acceptance.
"""
from mathutils import Matrix

_CHAIN = ("index_2_ri", "index_3_ri", "index_4_ri", "index_5_end_ri")
_PARENTS = ("index_1_ri", "index_2_ri", "index_3_ri", "index_4_ri")


def rebase_ads_trigger_index(source, ads_baseline, hk416_idle):
    """Return a pose with only the right index chain replaced.

    Inputs are evaluated source world matrices in the same coordinate system.
    The input dictionaries/matrices are never modified. Native retargeting and
    its existing bone-length, skinning and control preservation remain separate.
    Call only for an explicitly selected ADS firing clip, never generic poses.
    """
    required = set(_CHAIN) | set(_PARENTS)
    if any(not required <= pose.keys() for pose in (source, ads_baseline, hk416_idle)):
        raise ValueError("ADS index rebase requires the complete source right-index chain")
    result = dict(source)
    for bone, parent in zip(_CHAIN, _PARENTS):
        current = source[parent].inverted() @ source[bone]
        position, rotation, scale = current.decompose()
        if bone != "index_5_end_ri":
            base = ads_baseline[parent].inverted() @ ads_baseline[bone]
            idle = hk416_idle[parent].inverted() @ hk416_idle[bone]
            rotation = (rotation.normalized() @ base.to_quaternion().normalized().inverted()
                        @ idle.to_quaternion().normalized()).normalized()
        result[bone] = result[parent] @ Matrix.LocRotScale(position, rotation, scale)
        if bone == "index_2_ri":
            # This joint also anchors the retargeter's palm centroid. Preserve
            # its world position exactly, avoiding matrix roundoff moving the
            # palm/arm or the other fingers while changing only its rotation.
            result[bone].translation = source[bone].translation
    return result


def ads_trigger_index_sampler(source_at, hk416_idle):
    """Wrap one ADS firing sampler; capture its own frame-zero baseline once."""
    baseline = {name: matrix.copy() for name, matrix in source_at(0).items()}
    return lambda time: rebase_ads_trigger_index(source_at(time), baseline, hk416_idle)
