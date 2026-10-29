# QA gates and debugging trees

Use to choose the next discriminating check. Where hands/digits are involved,
the [finger checkpoint](finger-checkpoint.md) precedes full motion fitting.
The [evidence register](evidence-register.md) gives
named receipts; historical script names do not mean they were run for a new asset.

## Acceptance ledger

| Gate | A pass requires | Common false pass |
| --- | --- | --- |
| Source pairing | Actual mesh/skin/skeleton/clip/base references and per-mesh bind contract. | Similar names or same weapon type. |
| Evaluated source playback | Independent raw/exchange/assembly checks, with missing graph inputs disclosed. | Successful import or tiny error to an inapplicable IK target. |
| Bind/reference checkpoint, including fingers where applicable | Preserved offsets/lengths/binds and observed relevant surfaces in matched poses; full hand coverage when hands/digits are involved. | Fingertips or a single silhouette only. |
| Retarget | Declared bases/parents/proportions, desired-target residuals and path-specific native channels/solvers; custom authoring controls are optional. | Zero residual after clamping an unreachable goal. |
| Converted animation / Blender visual | [Mandatory full-motion and 360° review](#mandatory-blender-visual-acceptance): source versus converted target, relevant anatomy/objects/contacts, corrections and re-review documented. | Source-only screenshots, static turntable, numeric pose agreement or successful export. |
| Native/package | Independent stored-byte/readback semantics and shipped resource identity. | Export/compile/pack returned success. |
| Runtime | Identified package, effective graph/mod/skin, affected states and transitions tested. | Offline graph fixture, static shader interpretation or another build's reload report. |

Retain PASS / FAIL / UNVERIFIED / BLOCKED in existing receipts. New retarget
status files use the [gate-specific vocabulary](../../../cyberpunk2077-animation-retargeting/references/pipeline.md).
Record exact versions, hashes,
commands, body variant, frames/times/views, tolerance rationale and remaining gaps.
Keep failed original reports beside later certificates; later scope must be explicit.

## Mandatory Blender visual acceptance

**Visual coverage requirement recorded 2026-10-27: this gate applies to ALL animations.**
The 2026-10-28 vertical-slice policy permits disclosed diagnostic test packages;
it retains this visual gate for accepted-beta promotion and full-set expansion.
Before promoting a candidate as an accepted beta, play and actually
review the **converted animation on its target skeleton/rig or target animated
objects/channels in Blender**. Compare source versus converted side by side or
with comparable framing and synchronized times. Review the full timeline and
important transitions, plus full 360° spatial coverage: front, back, left, right,
above and below, and obscured areas/close-ups as applicable. Repeat playback from
complementary views until the relevant motion and surfaces are accounted for.
Neither a still-pose turntable nor a few selected frames validates motion.

This covers characters and full bodies, faces where animated, creatures, props,
interactions, cameras and mechanical objects. Inspect deformation, jitter/popping,
unwanted stretch/twist, clipping, sliding/contact loss and unnatural movement.
Check starts/stops, loops and cross-clip/state transitions where present, fast
motion, extremes, attachment changes and moving contacts. For camera animation,
review the moving camera's output as well as its trajectory/orientation from
external views where useful; an external turntable alone does not validate framing.

Use these subject-specific checks within that universal gate:

- Characters/creatures: full anatomy and joints, spine/pelvis/limbs, ground or
  support contacts and sliding; face/eyes/jaw/expression surfaces where applicable.
- Props/mechanisms: intended pivots, travel, attachment continuity, part alignment,
  collisions and contacts throughout the mechanism cycle.
- Interactions: all participants and relevant environment/props, timing, alignment,
  changing contact ownership and separation/rejoining through the full sequence.
- Weapon/hand specialization: **each thumb, index, middle, ring and little finger
  on both hands**, wrist/palm, elbow/arm anatomy, grip, release/regrip and other
  moving contacts, plus weapon and mechanism alignment. Include front/top/left/
  right, the remaining 360° views, palm/underside/thumb-web and finger/wrist close-ups.

Preserve rest/bind calibration and joint lengths/scales. Use justified FK rotations
and nonstretch IK/contact correction when differing limb proportions require it;
report the original desired-contact residual as well as any clamped solver result.
Do not arbitrarily translate bones to conceal deformation or reach errors. Intentional
source-authored object/mechanism channels remain governed by their explicit contract.

**Visible deformation or the other listed defects is a FAIL.** Identify whether
it originates in the source, conversion/retarget, target deformation or remains
unknown; retain source and converted evidence. An inherited source defect is not
a waiver for a visibly defective converted candidate. Record frame/time, view,
subject/part, correction and renewed review of affected motion/transitions. Review
the updated candidate, not an earlier visually clean revision; a changed converted
artifact needs an updated receipt. Missing playback, comparisons, required views or
hidden-area coverage leaves the gate UNVERIFIED/BLOCKED, not PASS.

Source-only screenshots, export success and numeric pose checks cannot substitute
for this converted-target Blender review. Diagnostic exports and isolated
single-clip packages are allowed during
development under the [vertical-slice contract](../../../cyberpunk2077-animation-retargeting/references/runtime-validation.md),
including native readback used for review. Disclose visual failures or missing
review and keep them diagnostic; do not promote an accepted beta or expand the
full animation set until this gate and the other applicable gates pass.
Blender acceptance still does **not** establish
in-game/runtime acceptance: retain the separate native/package and runtime gates.

### Reusable Blender review checklist and receipt

Start UNVERIFIED and fill one receipt for the identified candidate and affected
clip/subject variants. Do not prefill a pass from historical results.

- [ ] Pin source and converted candidate identities/hashes, target skeleton/rig or
  animated-channel contract, Blender version, Action/clip, effective FPS/range,
  base/additive/reference-pose convention and subject variants.
- [ ] Play source versus converted target, side by side or comparably framed at
  matched times, through the complete timeline and important transitions.
- [ ] Review full 360° coverage including front/back/left/right/above/below and
  relevant obscured regions/close-ups while reviewing motion; record actual
  frame/time ranges per view. A static orbit/turntable is spatial evidence only.
- [ ] Inspect all applicable subject checks and listed defects, including every
  digit/thumb and wrist/elbow/arm/contact/mechanism in the weapon specialization.
- [ ] Preserve rest/bind/lengths; document justified rotation, nonstretch IK and
  contact corrections. Distinguish source defects from converted-target defects.
- [ ] Record defects, correction revisions and actual re-review coverage. Keep
  gate FAIL until visible defects are resolved and re-review passes; missing
  evidence stays UNVERIFIED/BLOCKED. Keep runtime status separate.

```text
Candidate/revision/hash; source identity/hash; target rig/object/channel contract:
Reviewer/date; Blender version; clip/subject/body or other variant:
Effective FPS; start/end/timebase; base/additive/reference convention:
Source-versus-converted comparison layout/framing and time synchronization:
Full-timeline playback ranges; important transition/loop ranges actually reviewed:
View → frame/time range → playback/scrub coverage → evidence path:
  front / back / left / right / above / below / obscured-area and subject close-ups
Subject-specific checks completed; inapplicable checks and reason:
Defect → source/target/unknown origin → frame/time/view/part → evidence:
Correction → new revision/hash → affected motion/transition re-review → outcome:
Blender visual gate: UNVERIFIED | FAIL | BLOCKED | PASS (with evidence/reason)
Promotion eligibility: diagnostic-only until Blender visual gate PASS and other applicable gates pass
Native/package gate: UNVERIFIED | FAIL | BLOCKED | PASS (separate evidence)
Runtime gate: UNVERIFIED | FAIL | BLOCKED | PASS (separate evidence)
```

## If the source grip is wrong

1. Verify mesh/skeleton/clip/base pairing, source hierarchy and mount transforms.
2. Compare raw decoder → exchange locals → accumulated worlds → evaluated skin.
3. If locals agree but skin fails, inspect indices, complete weights and per-mesh
   inverse binds. If skin agrees but fingers are open, identify source graph/IK,
   attachment, translation-retargeting or other pose-changing writers.
4. Request the precise missing evaluated-pose input or continue a bounded source
   investigation. Preserve the failing source gate. Do not “fix” it by fitting CP
   fingers and then call the result original-source fidelity.

## If the target hand or weapon jumps

1. Check units/basis, double-applied object transforms, root ownership and actual
   destination parents. Recompute parent worlds before child locals.
2. Check native graph copies/controls after FK, not only before constraints.
3. Check Normal/additive slot and chosen base. A correct local finger track can
   look wrong under a changed wrist/control composition.
4. If only contact transitions fail, inspect phase ownership and temporal release/
   regrip. If only elbows flip, inspect pole degeneracy/sign and reach limits.

## If geometry or shading fails after exchange

1. Establish fixed vertex/topology correspondence where available; compare named
   weights, all influence sets, full inverse binds and object transforms.
2. If terminal helper weights disappear, inspect raw clusters and importer node
   classification. Preserve the source; do not reweight to conceal missing joints.
3. If bind silhouette matches but animation fails, run fixed-clip wrong-parent and
   independent bind checks. Roundtrip equality alone can preserve an incorrect bind.
4. If bones fit but skin fails, isolate native helper evaluation. If geometry fits
   but shading fails, inspect source custom normals and the actual posed normal path.
5. Compare reference-pose, extreme-pose and interpolated motion. A static idle pass
   does not establish moving reload or source initial bind.

## If timing or events fail

Compare actual native source clock, exchange key times, endpoint seconds and raw
curve spacing. Inspect odd/intermediate source frames and fast peaks. Then inspect
state/montage trimming, component clamping, speed scaling and event time origin.
Keep transform, annotation and gameplay clocks separate. Metadata rate alone cannot
rescue the M1911 30 Hz curve failure. Do not shift frames or raise tolerance to
erase the discrepancy.

## Regression set and visual coverage

Retain one neutral/reference pose, hand opposition/flexion extreme, known failure,
contact/release/regrip, fast mechanism sweep and transition endpoint per affected
behavior row. Include original key times, quarter/off-grid samples and dense
critical intervals. Regular sampling elsewhere needs a declared cadence.

Negative controls should detect the failure they target: wrong parent with the
same rest silhouette; dropped weight set; changed native float/event/unselected
descriptor; unsupported additive/interpolation; wrong sample clock; reversed Twist
sign; off-midpoint quaternion mismatch. Reuse existing controls; label a proposed
new control UNVERIFIED until actually run.

Use full-size source → retarget → final-native images at matched times to support
the mandatory Blender playback review above: full 360° views and relevant
subject close-ups, including first-person/palm/thumb-web/digits when applicable. Identify
what is occluded or unreviewed. Contact sheets aid navigation; they do not prove
review or surface clearance. AABB overlap, fingertip distance or a source shader
match alone cannot certify skin contact/anatomy.

When recording a defect use `candidate/hash → body → clip → frame/time → view/
component → observed defect → attempted fix → measured/visible tradeoff → next
missing evidence`. Preserve prior candidates and owning agents' checkpoints. Do
not rerun their GUI/VM jobs or promote a port as part of maintaining this hub.
