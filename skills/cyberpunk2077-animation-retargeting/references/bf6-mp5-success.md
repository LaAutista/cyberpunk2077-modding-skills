# BF6 MP5: successful retarget and failure recovery

User gameplay acceptance: **2026-11-12**. This is the BF6 PW5A3/MP5 project, not the
older Ready or Not MP5. Its reusable procedure is the
[weapon playbook](weapon-retargeting-playbook.md). Exact private assets, source
receipts and scripts remain in the owning MP5 project; they are not distributed.

## What the user actually accepted

The user confirmed that snapping was gone, reload contact was broadly acceptable,
and idle, walking, running, inspect, ADS aiming and firing were smooth and met their
standard. Very minor tactical reload clipping was explicitly deferred. ADS reload
through the WWCM experiment remains deferred; ADS aiming is a separate result.

| Artifact | SHA256 | Evidence |
| --- | --- | --- |
| Final repaired archive | `0b855427bce062c9024d54a860a26950766950e30420cb36648c2a230a54855c` | USER_RUNTIME_VERIFIED for the user's tested scope, with named exceptions |
| Rejected approved-pose serialization | `630e38bde3d3026daf18337759db4e7b4279c1f2640b2149dbd2a0177266c041` | Failed immediately on equip: extreme player displacement |
| Pre-handoff archive | `2ce4964efb99b8648cb0d6b80f48372eed959103675f3081f70435912c75b6b2` | Temporary rollback artifact; its old grip was not the desired final result |

Four player banks (`pwa`, `pwa_ads`, `pma`, `pma_ads`) contain 62 clips each. The final
package check covered 248 clips and 5,521,454 native records. All four decoded preview
GLBs were byte-identical before/after the ordering repair. The other 54 of 58 archive
resources and the other 40 files in the installed mod were unchanged.

This does not claim every body/attachment/interrupt combination was game-tested,
perfect source-skin parity, zero clipping, or a complete live trace of the engine decoder.

## Why the arm snapped despite passing earlier checks

There were multiple defects, not one magic offset:

1. The old hip elbow differed from the accepted reload endpoint by about 72.6 mm
   while the wrist nearly matched. A measured shoulder-to-wrist swivel corrected
   the elbow while preserving the hand transform and anatomical lengths.
2. Correcting only Normal holds left stale additive offsets. Applying them to the
   new base produced up to 102.18 mm of wrist drift in the rejected experiment.
   Each compatible additive had to be evaluated and re-encoded against its new base.
3. The later left-elbow-only result still retained the old right-arm and finger pose.
   At the handoff, right arm/wrist rotation differed by roughly 9 degrees, some
   fingers by up to 68 degrees, and evaluated skin jumped as much as 46.58 mm.
   Wrist/elbow positions alone did not test the complete visible grip.
4. The successful repair used the user-approved native reload-ending grip as the
   reference for both arms and every digit. Each body and hip/ADS role had its own
   reference; static shoulder and ironsight clips used their semantic pose role,
   even when stored inside another bank.

For held moving clips, the fingers used the accepted shape while arm motion retained
its trajectory with measured plane compensation. Compatible tactical aliases received
the primary reload's finger motion only after their arm trajectories were compared.
Empty-reload manipulation retained its middle phase while departure/return were corrected.
The inventory also covered safe/friendly, equip/unequip, idle break, sprint, slide, vault
and melee paths. It did not prove every external/procedural state impossible.

## Contact improved through smaller, phase-aware changes

The successful ring/pinky lift touched four proximal rotation channels:
`LeftInHandRing`, `LeftHandRing1`, `LeftInHandPinky`, `LeftHandPinky1`. It retained distal
curl, native anatomy, wrist/arm motion, other digits, prop tracks and events. Earlier
index/middle work was separately retained. The fitted axes and amplitudes belong to
this source/replacement hand only.

Rejected approaches are useful negative controls:

- A nearest-wall fit escaped into the hollow magazine. A lower collision total did
  not mean the hand was correctly outside the prop.
- Some fits lowered counts while moving skin by about 40 mm or damaging pinky shape.
- The native magazine was seated by source frame 91; moving it at frame 92 would
  disturb valid seated alignment instead of repairing the finger.
- Apparent removed-magazine drift came from an omitted constant hand-origin offset
  of about 8 mm. Restoring that calibration reduced held-phase discrepancy to about
  0.048 mm RMS without editing magazine motion.
- A static correction applied across other phases created new finger overlap.
- A close-up camera anchored to the edited pinky changed the viewing angle with the
  correction. Replaying the previous bank's unchanged camera made the comparison fair.

MP5-specific timing is evidence, **not a preset**: the lift used the original 60 Hz
frame clock and a bounded ramp/hold/release; the empty return retained native middle
keys from 0.15 to 3.0 seconds and completed the corrected held shape by 3.2 seconds.
Other weapons need windows derived from their own events, contact and visibility.
Supplemental samples were excluded near existing keys to avoid native time quantization
collapsing two times. Original source times, holds and endpoints remained present.

## Additive and anatomical preservation were different checks

The repair composed the old evaluated arm motion, applied the measured correction,
then encoded offsets against the corrected Normal base. It reconstructed the composed
result and checked intermediate weights, including 0.25, 0.5 and 0.75. Normal anatomical
translations/scales were protected; encoded additive translations could change to
retain the evaluated contact. Freezing those offsets would have preserved the defect.

The preview used a declared `base_rotated_hypothesis` and explicit graph inputs.
That contract was useful for offline diagnosis; it was not a claim that every live
engine state used identical masks, weights or downstream constraints.

## Why the first installed fixed-pose build launched V around the map

The pose work itself survived: the corruption was in native record ordering.
Both custom splicers grouped records as `(bone, kind, time)`. The inspected WolvenKit
9.0.1 `CompressedBuffer.EncodeAnimationData` comparator sorts by `(bone, time, kind)`
with position=0, rotation=1, scale=2. Quantized/raw sections are separate streams.

All 248 original baseline clips followed the writer's order. All 248 failed-candidate
clips had inversions; each equip-family clip had 114. One concrete equip sequence
advanced bone 0's translation to the last time, then returned to time 0 for its rotation.

The old checks still passed because:

- Native preservation compared unordered record multisets.
- Independent preview decoding collected channels without enforcing physical order.
- Low-level native serialization accepted the supplied arrays.
- Visual review could therefore show the intended motion while the stored stream
  differed from the established writer contract.

Read-only inspection found root/trajectory records, motion-extraction state and
relevant metadata unchanged. That ruled out newly authored root travel as an explanation
in those fields, but did not prove how the native engine misinterpreted the stream.

The recovery changed **only the permutation of existing dynamic records**. It retained
all bytes within each record, timestamps, per-channel sequences, constants, float tails,
counts, addresses, chunks, metadata, events and fallback data. Actual rebuilt native
files were reserialized and compared against that exact expected permutation. Decoded
preview GLBs matched byte-for-byte; packaging was re-extracted and checked again.
The user then accepted the repaired build in game.

This is strong artifact/intervention evidence for the ordering defect; the exact live
decoder mechanism was not recovered. Do not turn this into a generic explanation for
all player displacement, or treat every compressed codec as this writer's format.

The shared reader now enforces the supported dynamic order before emitting a GLB.
Its regression accepts the original/fixed controls and rejects the failed files.
See [native ordering checks](native-readback.md#compressed-native-record-order).

## What was actually measured versus reviewed

The earlier offline verification covered 16,024 timeline samples at 60 Hz plus native
keys and focused blend/boundary checks. The primary full-skin camera-space handoff
jump was approximately 0.005812 mm after repair; idle-break and empty returns measured
about 0.118 mm and 0.991 mm. These are case results, not universal acceptance tolerances.
The bad 46.58 mm skin join remained a negative control.

Core review video ran at 60 fps. The recorded agent inspection used 6 Hz sheets and
full-size critical boundary frames, not a full-rate viewing of every variant. Preview
skin used V4 and was not the same as the user's customized runtime skin. The user
accepted the named gameplay scope despite those offline coverage limits. Do not rewrite
that history into perfect source comparison, full male/female visual coverage or a
zero-clipping result. The deliberately inserted two-second review hold before breathing
also did not establish a two-second live-game delay.

## Private evidence and safe reuse

Within the owning project, start at current `STATUS.json` and these relative paths:

| Need | Evidence |
| --- | --- |
| Actual accepted build and user quote | `work/grip-handoff-20261112/order-fixed/runtime-acceptance.json` |
| Earlier incomplete correction and native-order failure | `work/idle-snap-20261112/FAILURE.md`, `work/grip-handoff-20261112/FAILURE.md` |
| Phase/contact discriminators and rejected fits | `work/magazine-repair/STATUS.md` |
| Final arm/base authoring and bounded empty return | `work/grip-handoff-20261112/author_mp5_handoff.py`, `author_mp5_empty_return.py` in that directory |
| Full motion/skin checks | `verify_mp5_handoff.py`, `verify_mp5_skin_handoff.py` in that directory |
| Actual order-only recovery | `repair_mp5_key_order.py`, `order-fixed/independent-packed-native-audit.json` in that directory |
| Encoder comparator evidence | `work/grip-handoff-20261112/runtime-investigation/mp5-native-key-order-evidence.json` |
| Installation identity and preserved files | `work/grip-handoff-20261112/order-fixed/installation/install-receipt.json` |

Historical scripts have hardcoded paths, hashes, source bodies and assumptions; use them
as evidence, not parameter-free templates. In particular, `build_mp5_static_grip.py` is
a rejected diagnostic that retains the old sorting pattern. The shared checked pipeline
is the reusable route. Do not copy private assets, raw disassembly or proprietary clips
into this skill. Transfer the method to M277/Neto work, not MP5 angles, timing or mounts.

## Reload-to-fire follow-up accepted 2026-11-13

The user later confirmed the v4 hip tactical/empty firing-delay repair. See
[mandatory reload-to-fire integration](reload-to-fire.md) for the compiled ARR/WWCM/EDW
conflict, protected-field access failure, moving-deadline defect and bounded runtime
acceptance. This extends the case's evidence; it does not certify ADS reload or every
speed/body/interruption combination. Preserve the earlier animation success separately.
