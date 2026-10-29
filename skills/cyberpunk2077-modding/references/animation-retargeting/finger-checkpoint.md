# Finger alignment checkpoint — before motion

Do this before transferring complete clips. A wrong reference grip contaminates
every frame and invites compensating joint translations. Source appearance is the
primary reference; anatomical or real-grip images can help diagnosis but do not
supply an absent evaluated source pose.

## Establish a matched static checkpoint

1. Pin the source mesh/skin/skeleton/clip/base pairing and the exact evaluated
   source frame. Establish whether graph IK, translation retargeting, constraints
   or procedural deformation are missing. Keep raw decoded playback and evaluated
   playback distinguishable. Use the [source contract](source-playback-adapters.md).
2. Pin target native skeleton, player variant, skin and required helper evaluation. Keep native
   rest/bind matrices, all influence sets and component placement. Use direct native
   skeleton mapping or optional controls around that contract; do not rebuild the
   deformation skeleton to fit a grip or wait for an unrelated animator-rig project.
3. Align source and target in a declared weapon/common frame. Calibrate wrist/palm
   orientation, thumb base/opposition and digit axes using rotations. Record the
   calibration and both skeletons' unchanged local lengths/scales.
4. Capture source → target retarget → final native readback at the same time and
   framing, from top/left/right plus palm/underside, thumb web and digit close-ups.
   At the early checkpoint, final-native evidence may be UNVERIFIED; it remains a
   later required gate, not an assumed result.
5. Account for both hands' thumb, index, middle, ring and little finger: full joint
   chain, knuckles, webbing, nail, surface shape and intended contact. Record
   occlusions explicitly. Inspect actual opaque skin, not just bones or wireframe.
6. Check the reference pose and a small set of flexion/opposition extremes with
   interpolation. Only proceed to full motion once the relevant source and target
   reference failures are resolved or the next experiment is explicitly bounded.

## Record the checkpoint

| Field | Required evidence |
| --- | --- |
| Identity | Input/tool hashes, source frame/time, body/skin variant, base/additive convention. |
| Mapping | Named joint correspondence, reference frames, rest and inverse-bind ownership. |
| Preservation | Joint offsets, scales, lengths, weights and intentional authored exceptions. |
| Shape | Palm/thumb-base/digit surface comparison in matched views, including hidden regions. |
| Contact | Palm/digit/control/component distances or intersections with assumptions stated. |
| Status | PASS / FAIL / UNVERIFIED for source, bind, alignment, deformation, native and runtime. |

**PROVEN lessons, [R2/R3/H1/H2](evidence-register.md):** unchanged finger keys can
look wrong when wrists or controls compose differently; equal posed skin can hide
bad bind/rest compensation; passing bone transforms does not certify palm skin.
The V4 comparison pass is therefore insufficient to pass this full checkpoint.

## Stop and diagnose

- **Source grip already wrong:** inspect the source runtime/evaluated pose, clip
  pairing, additive base, object mounts, translation mode and source constraints.
  Target retargeting cannot establish the missing source truth.
- **All fingers fail similarly:** revisit common frame, wrist roll, hand scale and
  parent/control composition before adding per-digit offsets.
- **Only thumb fails:** inspect thumb base rest/axis and opposition, not just its
  endpoint. Match the source then inspect native helpers and skin.
- **Bones fit, skin folds:** preserve the failing view/time and inspect weighted
  helpers, inverse binds and normals. Do not reweight before identifying the owner.
- **One view looks good:** add the missing surface view. Mark unobserved interior
  or hidden skin UNVERIFIED; do not infer it from the silhouette.

After corrections, retain the failed checkpoint and rerun its static views before
full [contact/motion](proportions-contact.md) QA. Bingle's palm/finger calibration
is an inspected transferable idea; its FO4/MMD mapping and scale are not CP presets.
