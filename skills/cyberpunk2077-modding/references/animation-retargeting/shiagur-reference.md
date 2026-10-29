# Shiagur guide: transferable rig and export lessons

[Fallout 4 Blender Rig Animation Guide](https://docs.google.com/document/d/1wIyKkPsvuPtR6B2ODGnIHMcGkaCOEm04cq3yC86mY98/edit),
guide **2.0**, full returned text read through Google Drive on **2026-10-26**.
This supersedes the earlier web-reader access gap. Guide version 2.0 and the
separately inspected Human Animation Rigs 2.8.3 package are distinct identities.
See **F1** in the [evidence register](evidence-register.md) for the document revision
and paragraph-index spans. Images and linked videos were not inspected in this read.

The recommendations below are **PROVEN as guide text**, not tested addon/Havok/game
behavior. Their application to CP is **INFERRED** and must pass local fixtures.
This chapter synthesizes selected ideas; it does not reproduce the guide or supply
its Python scripts, converters, rigs or assets.

| Guide observation | How and why to transfer it |
| --- | --- |
| Import and viewer skeleton must match the animation's 1P/3P/Power Armor role. | Pair actual clip binding, bone order and skeleton identity before diagnosing motion. A successful wrong-skeleton import can create a false retarget problem. The guide's first-person Power Armor sharing is FO4-specific, not a universal skeleton rule. |
| WeaponParent, COM, Root and Camera have separate responsibilities. | Preserve weapon orientation/attachment, body placement, locomotion extraction and camera carriage as distinct spaces. Fixed-hand/weapon controls need not follow COM. Do not move CP Root or bake camera motion into a wrist merely to center the preview. |
| Hand controllers, fixed-hand controls, IK/FK and arm targets select different constraint owners. | Record current control mode, pole and follow-space at the reference pose and every switch. Import a raw source pose without active authoring constraints adding a second solve; restore the intended mode explicitly. Never infer that a rendered FK result proves the live IK path. |
| First-person follow drivers can move a hand with WeaponParent or the magazine. | Model reload contact ownership per phase: weapon grip → release → magazine → regrip. When switching, preserve the current world pose and rebuild destination locals before blending; verify no snap. The world-preserving switch/temporal blend is an inferred CP implementation, not a tested operation from reading the guide. |
| Attachment tooling uses an active parent part and bone-named empties. | Recover receiver/barrel/muzzle/part hierarchy and local mount transforms explicitly. Resolve names against the selected skeleton and reject ambiguous matches. A named empty is an attachment clue, not a reason to discard its transform or collapse the component chain. |
| A stable default assembly pose is established before other first-person clips. | Use the finger/reference checkpoint before full motion, then check each clip's declared start/end transition against that operational pose. This is a posed assembly reference, not permission to replace native rest or inverse binds. Not every clip must begin and end at idle. |
| Additive motion layers over base motion; third-person graphs replace/blend channels. | Identify actual base, masks and effective graph route. Preserve raw and evaluated source views separately. Do not infer additive semantics from an `add` suffix, reuse another weapon's additive blindly, or copy the FO4 lower-body/FK recipe into CP. |
| Actions have their own export range and annotations; preview bounds can differ. | Preserve Actions and pin effective FPS, explicit start/end, endpoints and event origin before baking. Inspect what the exporter actually consumes and writes. The guide's 30 fps recommendation is for its FO4 authoring path; it must not retime Neto's native 60 fps M1911 reload. |

## Annotation and offline-preview boundary

The guide describes recovering existing source annotation time/text pairs from
Havok XML or viewer annotation tracks. It gives `SoundPlay` and `ReloadComplete`
examples. Keep these as source events with provenance; they are not CP event names,
sound assets or a proven target ammo-commit contract. Preserve duplicates and
clip-relative origins, and map only through a verified target event/dispatch route.
The guide's Pose Marker UI description also does not prove that the different
Bingle-linked PyNifly annotation writer preserves all timings or encodings.

A matched skeleton plus animation in Havok's standalone viewer is a useful proposed
offline boundary check for skeleton playback, motion data and annotations. It is
not a rendered skin/contact, full source graph, CP retarget or runtime pass.
No Havok viewer/converter, addon, embedded script or external dependency was run or
installed during this guide review. The guide's troubleshooting instruction to
run an embedded Python script is source material, not authorization to execute it.

For CP use [spaces/binds](spaces-bind.md), [finger checkpoint](finger-checkpoint.md),
[contact](proportions-contact.md) and [events/export](events-native-export.md) as the
implementation contracts. Optional stretch and automatic finger curling described
by the FO4 rig do not override native CP lengths, existing finger keys or the need
to inspect actual palm/digit deformation. Current V4 is still an FK diagnostic
scaffold; a documented IK control concept is not implemented CP support.
