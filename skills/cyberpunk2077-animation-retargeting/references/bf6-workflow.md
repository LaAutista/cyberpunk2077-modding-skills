# BF6 weapon ports: findings and platform boundary

Latest case: [BF6 MP5 user-tested success, 2026-11-12](bf6-mp5-success.md).
For an explicit execution sequence use the [weapon playbook](weapon-retargeting-playbook.md).
The earlier dated findings below retain their original evidence scope; the new case
records current accepted gameplay, minor tactical clipping and deferred ADS reload.


Updated 2026-11-02 from the MP5/PW5A3, L115 and rejected RPG7 work. This is a reusable method
with bounded case evidence, not a release declaration for any whole weapon.
The earlier RoN MP5 acceptance is a different source route and artifact. RoN work
was later shelved in favor of BF6; retain its useful lessons without treating its
missing-animation fallbacks as the BF6 baseline. Purchased replacement models,
source-game assets and private project adapters remain outside this repository.

## Deliver a connected action before expanding the platform

Use one source action, measured replacement assembly and exact target native
readback to produce a reviewable sequence. Fix failures visible there before
requesting another game test. A full animation-engine reconstruction, all-game
animation dump or completed humanoid animator rig is not a prerequisite.

Blender is the inspection environment for the geometry and motion actually loaded
into it. It exposed the earlier bolt, arm and finger failures. That does not make
an incomplete assembly, missing runtime layer or wrong skin a 1:1 engine preview.
Record what was evaluated and correct visible defects; investigate graph behavior
only for a remaining demonstrated mismatch. Runtime testing answers integration
questions after the user accepts the offline motion.

## Source, replacement and native target are separate contracts

1. Preserve the original source skeleton, source geometry reference, decoded data,
   evaluated pose samples, events, visibility and clocks. Identify actual arm/weapon
   clip pairing and any missing source layers. Names alone do not identify variants
   or source semantics. Preserve original samples alongside native export times.
2. Measure replacement-model bore/sight line, grip, magazine well, mechanism pivots
   and attachment rails. Keep the source rig/model as a reference even when shipping
   CGTrader geometry. Store one declared source-to-target weapon interaction frame;
   hands and moving parts must use compatible frames throughout manipulation.
3. Preserve native anatomical offsets, lengths, scales, rests and per-mesh inverse
   binds. Apply calibrated rotations and nonstretch reach in the final hierarchy.
   Transport the source elbow bend plane to the target shoulder-to-wrist direction;
   a static pole projected onto a different reach direction can flip the elbow.
4. Keep source camera motion, weapon motion and player displacement separately
   owned. Reducing a common carrier can stiffen the gun without solving camera bob.
   A pelvis anchor is useful only where the selected mask and constraints retain
   it. Check partial blend weights and start/stop transitions, not only weight 1.

Do not reuse a measured MP5/L115 axis, offset, clock or visibility interval as a
new weapon's default. See [spaces](spaces-and-transforms.md),
[source adapters](source-adapters.md) and [contact](contact-and-ik.md).

## Preview the actual native component hierarchy

A correct-looking preview can bypass a binding that the game still applies.
Record each component's parent, slot, local transform, rig root, animated part
and inverse-bind owner. Reconstruct parent-first and apply each mount exactly once.
Re-export the candidate's own rigs and mechanism banks; do not combine new player
motion with an older magazine bank or a convenient preview-only offset.

The MP5 investigation found a specific mismatch:

- The preview mounted the magazine directly under `WeaponRight`.
- The native magazine root was `mag_plug`; the receiver supplied `mag_slot`.
- Read-only static inspection of the tested executable found `_plug` to `_slot`
  name remapping in rig binding. This supports that binding for the inspected
  route/build; it does not prove every component's runtime parent.
- A 139 mm mount baked into the magazine root plus the receiver slot applied the
  placement twice. The doubled-mount diagnostic reproduced the reported direction
  of protrusion; removing another component offset had already failed in game.
- The offline correction restored the slot-relative rig and six animation aliases
  and mounted the preview at the receiver slot. Composed weighted-bone matrices
  matched the previously approved appearance within approximately 3.413e-6 in
  matrix components at reference, native keys and 60 Hz samples. Meshes, inverse
  binds and player motion were unchanged. Gameplay acceptance of this correction
  was still OPEN at this publication.

The general lesson is to prove native assembly ownership, not to zero every root
or delete every `_plug` offset. A magazine can match the hand numerically in one
space while being mounted incorrectly in another. Check seated idle, extraction,
held manipulation, reinsertion, release, visibility changes and final rest together.

## Reconcile authored arms, controls and transitions

Identify whether each clip is Normal or additive, its actual base, active masks
and the downstream arm-control ownership. Authored wrist motion and an old IK
target can disagree after composition. Where a control is contractually the same
target, synchronize it from the final wrist/weapon transform before rebuilding
parent-local keys. Do not overwrite an intentionally different control target.

Apply an established correction to every routed compatible bank, including idle,
equip and additive bases; correcting only reload aliases left older arm frames
elsewhere in the MP5 experiment. Inspect fire-to-idle, bolt-to-idle, sprint-to-stop,
ADS entry/exit and interruptions. A constant-input graph experiment cannot certify
those changing states. Observe camera and player movement as well as arm contact.

For mixed source holds and native transitions, compare the final native pose on
both sides of each graph edge: idle/start, start/sprint hold, hold/stop, stop/idle,
and sprint/slide. Check weapon, shoulder/elbow/wrist and driven controls together.
RPG7 v5 passed isolated clip checks but its sprint hold differed from all three
native-adapted transitions by about115mm/46degrees. Reproduce the mismatch before
repair; retain the failing bank as a negative control. Choose a shared compatible
hold or explicitly adapt transition boundaries, then check intermediate blends
and inherited locomotion additives against their actual base. A full-weight FK/IK
match alone does not prove a partial-weight blend or the engine's final IK result.

### MP5 reload-to-rest and transition lesson (2026-11-03)

A matching wrist/weapon endpoint does not establish a matching held pose. The MP5
reload-to-idle review exposed an elbow/finger/skin jump that wrist-only checks
missed. Compare both shoulders, elbows, wrists, all digit chains and evaluated
skin on both sides of the handoff, then inspect continuous playback through it.
Use the user-accepted held pose as the measured reference; do not substitute an
older donor idle simply because its wrist position agrees. Check both hands.

For a bounded transition repair, preserve unrelated motion, anatomical local
translations/scales and lengths. Verify intermediate frames, not just endpoints,
and synchronize only controls whose ownership has been established. An elbow
swivel may preserve the wrist while changing the silhouette; its angle is a
per-rig measurement, never a reusable constant. Report skin/contact regressions
separately even when the boundary discontinuity improves.

Keep contact corrections phase-specific and object-relative. End a free-hand
reach adjustment before magazine contact/visibility begins; verify the actual
native event/key times. Audit every routed alias and body/ADS variant, but copy
motion only after verifying compatible rests, source action and channel semantics.
Merge into the current cumulative bank and independently verify that accepted
clips and events survive. Separate successful serialization, user preview
acceptance and in-game confirmation; none grants the other two.

The MP5 female idle-hand correction and primary hip tactical early-reach trial
received user preview acceptance. That acceptance did not cover installation,
sprint/empty/ADS trials, other body variants or remaining contact defects. The
visibility-key ordering correction was separately confirmed in game for both hip
reloads. Do not promote the entire MP5 from these individual results.

A fixed-length solve can still fold the arm unnaturally. RPG7's idle retained the
donor shoulder while fitting the source grip, giving an elbow inner angle near
28degrees versus78degrees in source. Compare the mapped source clavicle/upper-arm
placement, elbow plane, wrist/palm and skinned shoulder together even for static
holds. A source-directed clavicle test preserved grip/weapon/lengths and improved
the angle, but remained an unaccepted offline probe; it is not a universal fix.
Check adjoining actions and accepted manipulation before propagating a repair.

After changing an arm base pose, rebuild compatible additive motion from the
actual fitted base. Reapplying the raw source shoulder preference at every
additive key can preserve full-weight grips yet increase partial-blend drift.
Compare intermediate weights and between-key frames against the last passed
candidate, not only the original broken bank. RPG7 walking exposed this: the
first propagation increased the measured residual from1.07mm to1.89mm; carrying
the fitted base reduced it to1.27mm without changing the check tolerance. These
are diagnostic measurements, not universal tolerances or proof of engine IK.

## Finger articulation and timing

Use the [palm-relative rotation procedure](contact-and-ik.md#palm-relative-finger-rotation)
and [reference-grip check](contact-and-ik.md#do-not-preserve-a-broken-reference-grip).
Do not assume identically named bones have compatible axes or reference poses.

In the MP5 empty reload, the source index middle joint held roughly 39 degrees
of bend while the target reference held about 0.7 degrees. Transferring only
changes from those references retained an approximately 38-degree bias. Correcting
the source-relative articulation was a separate operation from a small, measured
base-knuckle offset for the replacement handguard.

The one-clip trial preserved other motion and passed its ten native pipeline
stages, but a stricter angular check measured 0.278 degrees against a 0.25-degree
target, and small magazine-contact intersections remained. Source hand skin was
unavailable; the comparison used labeled source joints and a preserved target
skin that was not verified against the user's customized body. The trial was
awaiting user review, not approved for the full set or installation.

The evaluated source also contained a roughly 43-degree one-frame fingertip
release at 60 Hz. Compare source and target signed bends/angular changes on the
same clock before calling a fast step a retarget twitch or smoothing it away.
Linear world-matrix interpolation between source samples is an estimate, not
proof of the source engine's interpolation. Preserve failed subframe comparisons.

## RPG7 validation failure

The RPG7 reload candidate was rejected for finger/thumb shape after native,
serialization and abstract direction checks passed. Actual matched wire/opaque
inspection had been omitted. This was a validation failure, not evidence that
numeric tests were wrong or that source/target body differences could be ignored.

| Demonstrated cause and missed check | Reusable prevention | Regression evidence |
| --- | --- | --- |
| The source animates its clavicle anchor by about255–260mm; the adapter kept the native anchor fixed. Endpoint reach passed while the native arm became nearly straight, adding18.6/36.4degrees of wrist bend at sampled keys. | Inventory complete source localT/S channels and their parent chain; declare handling before using a rotation-only adapter. Compare anatomical forearm/palm directions and extension ratio. Check the elbow-circle bound before changing a pole. | An animated-anchor synthetic fixture tests intermediate travel with equal endpoints. The private actual-channel and feasible-circle receipts reproduce the RPG7 failure; they do not prescribe native joint translations. |
| V3 phalanx directions matched within0.004degrees, but native knuckle layout, segment lengths, terminal surface directions and twist differed. | Compare actual wire AND opaque skin, joint centers, own inverse binds/weights and source/native anatomical frames. Treat inferred tip axes and absent source runtime layers as uncertainty. | The private matched mesh fixture shows different wrap even with direction agreement. The workflow eval must reject a direction-only surface pass. |
| A ring correction removed an isolated skin patch but opened distal articulation by20degrees. | Check source curl/twist, all digits, palm/wrist/arm and original contact together before propagating a local repair. Keep preservation checks and source fidelity separate. | Source/V3/V4 before-after comparison rejects the improved-penetration but damaged-articulation candidate. |

These are measurements for one rejected asset/clip. Do not reuse their offsets,
angles, tolerances or proposed reach bounds as another weapon's correction.
Wire/opaque inspection found no evidence of swapped digit weights or inverse-bind
substitution in the checked cases; that limited negative finding is not a whole
rig/runtime pass. A wire-only spike caused by thin-triangle overlay miters was
separated from unchanged actual geometry before interpreting it as a mesh defect.

The smallest next work is one measured anatomical/surface/contact adaptation,
with source travel handled explicitly, then the same joined checks and complete
motion review. No corrected RPG7 or gameplay acceptance is claimed. See the
[private evidence provenance](../../../PROVENANCE.md#rpg7-validation-learning-2026-11-02)
and the existing [failure ledger](failure-ledger.md).

## Review and first-install coverage

Use the existing [acceptance ledger](../../cyberpunk2077-modding/references/weapon-rigging-animation.md#acceptance-ledger).
For every included clip and variant, bind source/native/rig/assembly/skin hashes,
complete time range, cadence, views, video identity, observations and the user's
explicit acceptance. Repairs need before/after alongside synchronized source and
native playback. Review a batch together; an accepted clip does not approve others.

Cover idle/low ready, fire/recoil/dry fire, bolt/charging, tactical and empty
reloads, ADS and ADS reload where supported, walk/jog/run, sprint starts/stops,
equip/holster, melee and relevant interruptions. Missing source actions require
named, reviewed fallbacks. Use first-person plus side, underside and hand close-ups.
Review all digits, thumb opposition, mechanisms and contact across open, closed,
release and regrip phases. Label source joint proxies and missing layers visibly.

First installations must include sound coverage: firing, dry fire, reload variants
and applicable bolt/charging/equip/holster events. For BF6 audio record source
provenance, selected sample, routing, timing, listening and packaged-resource
checks. Native donor placeholders must be identified as such; disclose source-audio
gaps before review and never label donor audio BF6. Sounds in a folder do not prove
they are routed or play on the correct event.

For optics/muzzles, verify record compatibility and placement slots separately
from rail geometry. Test actual equip, position, ADS/reticle and removal; a visible
inventory slot is insufficient. Keep one weapon candidate unless variants are
requested. Extended magazines and staged reloads need explicit part/phase/reset
coverage. Scope interruption hooks to the intended weapons; do not enable a global
vanilla reload mod as a side effect of adapting two weapon records.

## What the reusable platform currently supplies

| Capability | Publication/evidence boundary |
| --- | --- |
| Source inventory, contract checks, archive/graph/mask inspection | Included helpers; supported formats and synthetic tests described in [agent tools](agent-tools.md). They do not decode every source game or execute the full graph. |
| Native conversion, independent readback, semantic checks, serial batches/resume | Included tools with input/tool/output fingerprints, bounded jobs and retained failure logs. Readback buffer batching and configurable bounded .NET heap are included in this update. |
| Measured calibration, connected native Blender preview, contact probes and one-action authoring | Implemented in the private development platform with project adapters and owned inputs. Not bundled as a portable Blender add-on here; installation of these skills does not install that platform. |
| Partial graph, IK, camera and transition replay | Diagnostic hypotheses with explicit inputs and narrow fixtures. No complete runtime parity or automatic release acceptance. |
| Source/native visual acceptance and gameplay | Per-candidate human evidence. Neither helper receipts nor this documentation creates it. |

Reuse measured contracts, fixtures and verified resume to remove repeated work.
Generalize from reviewed conversions, not from an ever-growing runtime simulator.
A complete conversion in under an hour remains a target without an end-to-end
measured and accepted port. The retained evidence is summarized in
[provenance](../../../PROVENANCE.md#bf6-findings-and-preview-gates-2026-11-02).
