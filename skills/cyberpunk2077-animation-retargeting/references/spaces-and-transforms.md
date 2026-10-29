# Spaces and mapping contract

Declare vector convention, matrix storage/multiplication order, quaternion ordering,
units and source-to-working/working-to-target basis matrices before conversion.
The portable fixture validator accepts column vectors, row-major stored matrices,
xyzw unit quaternions and seconds; a source adapter must explicitly convert to
that representation. It does not guess engine conventions.

For column vectors:

```text
W_child = W_parent * L_child
L_destination = inverse(W_destination_parent_UPDATED) * W_destination_desired
basis conversion: W_new = C * W_old * inverse(C)
assembly placement: W_placed = A * W
```

A basis change and assembly placement are different operations. Rebuild changed
parents first, then children, then dependent controls. Do not reuse source parent
worlds or cached destination worlds. Prove this with a noncommuting parent/child
fixture in which the destination parent changes; an identity parent hides the bug.

Keep native control reference locals, skin inverse binds and animator rest poses
separate. Per-mesh inverse binds cannot serve as global native control rests.
Preserve target anatomical local translations/scales and lengths. Intentional
mechanism translations or virtual attachment-control offsets need explicit ownership.

Mapping records pair actual names from both skeletons. Every target bone is either
mapped once or explicitly left unmapped with a preservation/helper/control reason.
Many-to-one targets are rejected by the structural helper; source reuse also needs
a documented project-specific adapter instead of silent duplication. Matching
names alone proves nothing about anatomical correspondence or rest-pose alignment.

Gate C additionally needs independent reference-pose reconstruction: compare target
worlds, parent-local reconstruction and relevant skin/contact using declared
tolerances justified by units/codec precision. Record numerical maxima and failing
bones. `verify-mapping` checks coverage/names only; it cannot award this gate.

Detailed [rest, bind and direct-skeleton guidance](../../cyberpunk2077-modding/references/animation-retargeting/spaces-bind.md)
and [finger checkpoint](../../cyberpunk2077-modding/references/animation-retargeting/finger-checkpoint.md)
remain authoritative for the selected path. An animator control rig is optional.
