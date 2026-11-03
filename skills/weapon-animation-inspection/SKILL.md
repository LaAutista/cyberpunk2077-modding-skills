---
name: weapon-animation-inspection
description: Inspect and adapt Cyberpunk 2077 weapon meshes, rigs and animation using preserved assemblies, native tracks, Blender previews and export checks. Use for replacement fitting, moving-part collisions, magazine, trigger, grip or hand-contact work. Includes a verified local Lynx case study; other weapons require explicit rig and component adaptation.
---

# Weapon animation inspection

Follow the user's scope and project instructions. Preserve appearance, alignment,
mechanics, timing and unrelated motion. Inspection alone does not authorize game
launch, deployment or profile changes. This repository supplies instructions and
small helpers, not game assets, a universal retargeter or the original Lynx adapters.

Read the [reusable adaptation procedure](../cyberpunk2077-modding/references/weapon-rigging-animation.md)
and [tool-selection guide](../cyberpunk2077-modding/references/tool-selection.md).
Use the [Lynx case](references/lynx-case-study.md) for proven local reasoning and
bounded evidence; use its [command contracts](references/lynx-command-contracts.md)
only after supplying the described project-specific tools and owned assets.
For motion transfer, first use the sibling [retargeting state machine](../cyberpunk2077-animation-retargeting/SKILL.md)
to preserve a baseline, select one blocking fixture and bound failed correction loops.
For Unreal source recovery and graph-aware retargeting, use the
[HK416-derived reusable workflow](../cyberpunk2077-modding/references/ron-port-workflow.md).
Use the [additive preview helper](references/additive-preview.md) only with its
explicit bind-relative export contract and chosen normal base.
For state-dependent failures, trace [graph blends and transitions](../cyberpunk2077-animation-retargeting/references/animation-graphs.md)
and label the inputs and operators actually reproduced in Blender. A clip-only
preview cannot establish state selection, interruption or downstream IK behavior.
Start weapon work with the [acceptance ledger and behavior matrix](../cyberpunk2077-modding/references/weapon-rigging-animation.md#acceptance-ledger).
Keep source pairing, retarget, visual, native/package and runtime results explicitly
PASS, FAIL or UNVERIFIED in historical ledgers; new retarget receipts use the
[gate-specific vocabulary](../cyberpunk2077-animation-retargeting/references/pipeline.md).
Missing source variants require a disclosed fallback and
its own checks; they cannot become an invented source-fidelity pass.

For established RoN ports, use the [MP5 recipe](../cyberpunk2077-animation-retargeting/references/mp5-workflow.md).
Inspect current replacement geometry/skin and post-composition controls; source
model views or an IK curve alone do not prove final hand contact. Batch review
of compatible actions is valid; retain explicit user-accepted release exceptions.
For BF6 work, use the [native assembly and calibration findings](../cyberpunk2077-animation-retargeting/references/bf6-workflow.md).

## Work sequence

1. Preserve complete donor/replacement assemblies, native resources, build inputs
   and release identity. Record hashes, dimensions, axes, hierarchy, pivots,
   inverse binds, component mounts and every skin influence set. Inventory actual
   clips and material references with the maintained summary helper. Similar
   weapons or an empty Blender Actions list do not establish compatibility.
   Prove the source model/rig/clip pairing; flag duplicate rigs, double transforms
   and wrong mounts. Preserve source and target bind/rest contracts, scale, finger
   hierarchy and channel semantics; rotate joints for poses rather than translating
   or stretching them to conceal a mismatch.
2. Recover weapon/component and player-arm motion. Prove playback against an
   independent import where supported; preserve key counts/times, scale modes,
   float tracks and durations. Label missing runtime IK, graph blends, customized
   arms, visibility switching, shader substitutes and any approximated motion.
3. Inspect every animation included in the candidate through complete Blender
   playback, including draw, firing, reload variants and transitions, in matched
   first-person and useful close views. Actually inspect the motion and images.
   Show smooth videos to the user and obtain their acceptance before installation,
   following the [mandatory preview gate](../cyberpunk2077-animation-retargeting/SKILL.md#mandatory-blender-review-before-installation).
   Include synchronized source/native playback and repair before/after views under
   the [source comparison gate](../cyberpunk2077-animation-retargeting/SKILL.md#mandatory-source-versus-retarget-comparison).
   Label joint-only source proxies and body/skin differences; they cannot establish
   source surface contact. Use native component mounts, never preview-only offsets.
   Review every critical fast-motion/contact frame at full size and state the
   cadence elsewhere. Check receiver/bolt/handle/cover, magazine travel, trigger
   fingers, grips, neighboring parts, joints, visibility and sight alignment.
   Use the full behavior matrix, including idle/low ready, ADS when supported,
   locomotion, melee and interruptions. Compare source/retarget/final-native top,
   left and right matched poses; add palm/underside and close-ups until every
   thumb/finger and its deformed joints are accounted for through keys and
   interpolated motion. Source appearance is primary; anatomy references supplement it.
4. Diagnose before editing. Choose a local mesh, weight, pivot, rig or motion
   correction justified by evidence. Compare tradeoffs; preserve intended
   mechanics and unrelated motion. Do not hide parts or globally distort the
   weapon to force a fit. Reinspect the complete affected sequences afterward.
5. Export through the established native pipeline. Read back actual cooked
   meshes/tracks; check topology, quantization, normals, UVs, weights, binds,
   materials, keys/timing and unchanged payloads. Run collision/contact checks on
   those cooked inputs and inspect their rendered playback. If packaging is in
   scope, extract the final archive and compare the shipped resources.
6. Report implemented, automated, visually inspected and gameplay evidence
   separately. Give exact revision, frames/times/views and limitations. For an
   unresolved defect record evidence, attempted fixes, tradeoffs and the specific
   missing data or decision; failed attempts do not prove impossibility.

## Included preview helper

The [contact-sheet helper](scripts/contact_sheets.sh) labels completed PNGs from a
render manifest, retains hashes and refuses an existing output directory. See
its [usage and regression checks](references/contact-sheets.md). It deliberately
records `visuallyReviewed: false`: generating previews is not reviewing them.

Use the established Blender scripting API when necessary; use Bash, jq,
ImageMagick and FFmpeg for generic file, sheet and video work. Keep diagnostic
cameras/arms out of exports. Native readback, sampled collision gates and offline
views do not establish runtime graph, IK, material or gameplay behavior.

For a significant retargeting mistake or missed inspection, apply the existing
[validation learning rule](../cyberpunk2077-animation-retargeting/SKILL.md#learn-from-validation-failures):
record cause and missed detection, update the relevant shared prevention, and run
a regression. Deformation acceptance requires matched opaque/wire skin plus
joint/weight/orientation checks of the connected fingers, thumb, wrist and arm;
no numeric direction/contact result substitutes for those views and full motion.
