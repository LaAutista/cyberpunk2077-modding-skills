# Repeatable ports after MP5 1.0

The user accepted CG MP5 v14 as release 1.0 after extended play on 2026-10-30.
Tested archive SHA-256:
`4e5a04cd1647141490c964d44da7bc9f6151b69f276c3b8604e04535fb6dc50f`.
Known issues remain: reload while ADS and minor empty-reload visual defects.
This is scoped user acceptance, not perfect source parity or every body/attachment
combination. Holster, player recoil and some locomotion remain native fallbacks.
The package has its own item/icon and private resources; ADD Vantage and Perfecto
were specifically reported working. Preserve acceptance and exceptions together.
Do not reopen an accepted release to satisfy a more expansive assistant checklist.

## Reuse the established route

For a new skeleton, decoder, control graph or native writer, retain the
[one-clip vertical slice](runtime-validation.md). After that route is verified and
accepted, batch compatible actions against the same measured contract. Do not
restart discovery or demand another isolated game test for every clip. New
semantics or failures get their own bounded discriminator.

Keep one **private per-weapon recipe** using the existing project format:

| Recipe field | Required meaning |
| --- | --- |
| Baseline/deployment | Accepted package and installed hashes, enabled manager folder, rollback, user feedback and known issues. |
| Source | Game/decoder identity, AnimData hash, exact property/index and paired body/weapon references, montages, additive bases and clocks. |
| Target/fit | Current native container and matching rig hashes per body/weapon role, replacement components, measured fit/landmarks and control mapping. |
| Action plan | Source pair to native clip names, contact windows, event/sound schedule, adaptations and native fallbacks. |
| Build/checks | Existing authoring commands/configs, native batch manifest, current geometry/skin preview inputs, package outputs and evidence paths. |

Use [agent tools](agent-tools.md) to inventory references once, queue body/weapon
fixtures, resume hash-verified work and compare per-clip coverage. Extract selected
dependencies; arrays such as `FireSingle` contain paired variants and must not be
skipped. Reuse evidence only for unchanged inputs/tools and its exact covered scope.
Run heavy jobs serially under the same lock. Read summaries first, then the failed
stage log; avoid dumping full graphs or repeating equivalent previews.

## Decisions that made this port work

**Source composition.** AnimData selects the action; CG railed furniture does not
silently switch A2 motion to A3. Compare raw local channels and actual additive
bases independently of exchange playback. For the inspected raw RoN convention,
compose `T = base + delta`, `Q = normalize(delta * base)`,
`S = base * (1 + delta)`; this is not a universal Unreal convention. A
self-referencing base exposed an incorrect composed-export assumption.

**Hands and camera.** Reconstruct parents first, normalize blended quaternions
and preserve anatomical translations/scales. Inspect the actual composing mask
and downstream chest/hand/weapon controls. MP5 v10's excluded Hips/COG motion left
camera compensation active; v11 used the retained chest control and the user
confirmed sprint worked. That graph-specific result is not a universal carrier.
Check partial weights and sprint-exit/lowered transitions. Preserve accepted gun
motion when reducing camera-owned motion. Compare contact with post-composition
controls. An IK curve reaching 1 does not prove its target is stationary: MP5
first-draw contact settled one frame later. Derive windows from both trajectories.

**Native timing and pairing.** Keep exact decoded/quantized key times; avoid adding
a regular grid alongside nearly identical native ticks. Sound/phase frames are
unsigned integers on the native 30 Hz event clock, independent of source sampling.
The draw kept 56 source keys at 60 Hz and added a disclosed 16.7 ms terminal hold
for integer phase coverage. Do not round all keys to fix one event. Use the
matching **current packaged rig**: a stale donor weapon rig caused a semantics
failure even with correct authored motion.

**Dispatch and audio.** Scope wrappers to the actual equipped private item and
affected body variants; test a vanilla weapon for leakage. Body draw and weapon
mechanics need their actual dispatch names and compatible timing. Reload audio
requires its own event/sound-bank checks. Reuse script compilation evidence only
for byte-identical payloads with unchanged relevant dependencies.

**Attachments and sights.** A visible slot does not prove optic eligibility.
Check blueprint, slot and allowed-part records separately from rail geometry,
mount helpers and ironsight transforms. Update helpers in the matching rig and
all clips carrying them. Inspect the chosen replacement's actual rail, stock and
handguard with optics attached and removed.

**Visuals and release.** Review full affected motion on current replacement
geometry and the actual skin/body setup. Retain partial-skin and engine-IK limits.
Extract the archive and compare shipped resources; check loose files and ZIP
members/CRC. Authorized installs use the existing mod folder with rollback,
preserving profiles and other mods. Feedback belongs to the identified artifact;
carry accepted exceptions into release notes instead of erasing them.

## Measure the sub-hour target

Under an hour is a throughput target for the next comparable port with cached
tools, supported source semantics, a mapped rig and an available fitted model.
It is not yet an end-to-end benchmark or a promise for a new skeleton/graph.
Record discovery/fit, authoring, native gates, visual review, packaging and user
runtime waiting separately. Batch timings cover that invocation only; reused
checks are not fresh conversions. These helpers reduce repeated investigation
and command work. Model fitting, retarget authoring and visual judgment still
require a weapon-specific adapter and agent work.
