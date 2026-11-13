# Visual acceptance for converted animation

Use for changed motion or changed relevant source/rig/skin/assembly/evaluation inputs.
The [entrypoint evidence-reuse rule](../SKILL.md#mandatory-blender-review-before-installation)
retains acceptance for proved-unchanged covered motion; runtime stays package-specific.

## Mandatory Blender review before installation

Inspect **every animation included in the candidate** in Blender, through its
complete timeline and relevant starts/stops, loops, blends and state transitions.
Review the connected target assembly: skinned arms/body, weapon, magazine, bolt
and other moving parts together. Use the exact candidate's native readback and
verified assembly inputs; an older mechanism bank or a preview-only placement
offset cannot stand in for the shipped data.

Run the required [final-readback clipping audit](../../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#final-readback-clipping-audit)
on the assembled, deformed candidate before installation. Check every affected
frame and relevant alias/body variant; bind findings to final resource hashes.
Also verify that [previously approved clips survived the merge](native-readback.md#cumulative-candidate-preservation). A draft audit or preservation against a
stale import baseline cannot clear the final build.

Actually inspect continuous playback at normal speed, plus slow playback/scrubbing
of fast contacts. Use first-person and complementary side/close views and the
[full-motion review checklist](../../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#mandatory-blender-visual-acceptance).
For skin creases, also verify the renderer's normal source and evaluated corner
normals at a fixed pose; positions/weights passing does not prove that authored
normals survived import. Use the existing [skin/normal boundary check](../../cyberpunk2077-modding/references/animation-retargeting/native-deformation.md#next-diagnostic-when-skin-still-fails).
Record clip, variant, candidate hash, complete time range, views, observed defects
and evidence. Unwatched renders, a few poses, contact sheets, numeric checks and
successful native exports do not pass this gate. Missing coverage stays OPEN;
visible hand separation, broken bolt/magazine motion, clipping or deformation
stays FAILED regardless of other passed checks.

**Show the user smooth video previews and obtain their explicit acceptance of the
identified candidate before installing it.** Render actual motion at least 30 fps
(or the higher source cadence where fast motion requires it); do not interpolate
a sparse slideshow and call that a full review. Show complete affected actions
and transitions, with first-person and useful side/close views. Record the user's
answer against the preview and candidate identities. Review a batch together;
do not require a separate conversation per clip. Changed motion requires an updated
preview and acceptance. A diagnostic label does not waive this installation gate.

Fix Blender-visible failures offline before requesting game tests. Runtime testing
addresses remaining integration questions; it must not replace the visual homework.
State preview limitations honestly, but never use absent runtime parity to dismiss
a defect already visible in Blender. Do not expand engine reconstruction to avoid
correcting a demonstrated motion defect.

## Mandatory source-versus-retarget comparison

For every port, show the original source animation and the exact native target
readback side by side, synchronized through every retargeted clip's full timeline.
Use normal-speed playback (at least 30 fps, or source cadence for fast contacts),
slow review, matched anatomical views and the connected target weapon assembly.
A target-only preview cannot clear this gate. Include before/after when repairing
an existing port; record source, target and preview hashes and the user's review.

Inspect both hands digit by digit, including thumb, open/released poses, closed
grips and regrip, plus wrists, arms, mechanisms and weapon contact. Compare actual
anatomical joint directions/bends in measured palm frames, not similarly named
bone Euler angles. Preserve source articulation and timing; explain deliberate
replacement-model grip offsets. A plausible-looking target or a numerical pass
cannot substitute for the comparison. If the source is itself defective, report
that instead of silently correcting or attributing it to the game runtime.

Use verified source skin when available. Label joint-only proxies, inferred tip
axes, missing source runtime layers and target body differences explicitly; they
do not establish source skin/contact equivalence. Missing comparison coverage
stays OPEN and visible mismatches stay FAILED. Show the user the limited evidence
before any approval request; never hide its limitations in a receipt alone.
Start a finger repair with one reversible clip and obtain its review before
propagating the change. Preserve anatomical Normal translations/scales/lengths,
wrist/body motion, other digits and unrelated clips. When the base changes,
re-encode dependent additive offsets as described in the [playbook](weapon-retargeting-playbook.md#6-rebase-dependent-motion-instead-of-retaining-stale-offsets). See [contact](contact-and-ik.md)
for the reference-pose trap and the existing visual gate for installation approval.
