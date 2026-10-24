# Ready or Not HK416: evidence and remaining work

This is a bounded case for the [reusable port workflow](ron-port-workflow.md).
Source assets, native files, private receipts and game-derived previews are not
distributed here. Use your own installed resources and keep extraction local.

## Current user-reported status

On 2026-10-24, the user asked that their **in-game confirmation that the reload
plays** be retained alongside unresolved **thumb/contact, optic, texture and sound
issues**. This is positive user-reported reload-playback evidence. This update did
not launch the game, independently reproduce the report, or receive a tested ZIP
hash, selected clip, player variant, exact frames or complete laptop mod list.
Do not attribute it automatically to every artifact or claim all issues are fixed.

| Open issue | Established evidence | Next discriminating check |
| --- | --- | --- |
| Thumb/contact | User says contact remains unresolved; exact joint/pose/frame was not supplied in this update. Previous offline checks do not override the report. | Record tested package, player/VTK skin and clip/time; compare actual skin and FK/IK control evaluation around that contact. Preserve wrist-local anatomy and check adjacent fingers. |
| Optic / sight picture | User reports an unresolved optic issue. Separately, the direct-bone offline ADS preview put the front sight above the rear aperture at frame 0; native ADS alignment was not emulated. These are not proven to be the same fault. | Identify attachment versus iron-sight problem, inspect active slots, aim graph and `pos_ironsight` alignment, then compare in-game ADS. Do not move the whole rifle merely to align an approximate camera. |
| Texture / material | User reports unresolved texture issues. Source pixels, gamma/mips and resource references passed offline checks, which did not exercise the game shader. | Capture the affected surface/material in-game; inspect the winning native material, normal convention, channel packing, gamma, mip/compression and shader parameters. |
| Sound | User reports unresolved sound issues. The clean package uses official target resources; source notifies were not automatically converted into equivalent audio behavior. | Identify the silent/wrong action, inspect active sound names/resources and event time domains, and test event dispatch in-game. Do not reintroduce forbidden donor audio as a shortcut. |

Ammo commitment, reload cancellation, speed modifiers, graph blending, both player
variants, exact laptop VTK identity and unreviewed motion remain separately open.
A useful next task is to capture one repeatable affected reload/ADS sequence with
package identity and timestamps, then correct its demonstrated contact/material/
audio issues using the native-readback inspection loop.

## Why the clean rebuild was necessary

The earlier standalone attempt removed external weapon-mod requirements but kept
COD-derived native containers, inherited motion and calibration. The user rejected
equipped deformation and the tactical/empty reload behavior with a custom VTK body.
Renaming resources did not satisfy the asset-origin requirement.

The subsequent clean build used individually checked original RoN inputs and fresh
official Cyberpunk resources. It kept a separate `Items.RON_HK416` item, essential
RED4ext/ArchiveXL/TweakXL loaders, RoN empty reload and Cyberpunk-derived tactical
reload. VTK meshes were diagnostic inputs, not shipped assets. The source audit
supports that clean artifact's origin; the later gameplay report has no supplied
hash and must remain scoped as described above.

## Measured local results

| Stage | Actual bounded result |
| --- | --- |
| Recovery | Steam build 25784851 / executable 5.3.2.0; 26 PAKs, 467,074 index entries, 40 packages / 97 raw companions, 34 exported objects. Per-track animation and Linux Oodle exercised; ACL clip playback untested. |
| Source motion | Matching 60-bone arms plus full 292-bone player skeleton; 23-bone weapon; 121 endpoint samples at 60 Hz over 2 seconds. Source body additive composition and graph visibility reconstructed with explicit limits. |
| Native animation | 58 selected Normal clips and 91 untouched clips across five sets; maximum checked numeric delta 3.651e-7. Independent checks included 15,938 float keys and 6,716 constant keys. All 15 empty aliases remained byte-exact against the reviewed empty stage. |
| Geometry | All 83,938 body/magazine triangles, named weights, topology, UV sets, normals and binds checked. Moving empty geometry differed by at most 5.95 micrometres at decoded keys. Ideal-clock and local-hierarchy interpolation residuals were reported separately. |
| Mechanisms/contact | Corrected rear latch reach and wrist regression; source stroke 102.49 mm; independent handle/catch behavior during firing; constant selector operational offset. These values belong to this assembly only. |
| Package | 26 native files plus two loose resources audited; archive extraction matched checked native inputs byte-for-byte and ZIP checks passed. No live installation was performed by that build workflow. |

Historical clean ZIP SHA256:
`cd8a01cd802bfb2e0cde336404358baa1116adc7174cf258c49765ed7f17c082`.
This identifies the offline-checked artifact, **not** an inferred identity for the
user's un-hashed gameplay report. The archive itself is not published here.

## Visual coverage and failed attempts

Complete empty sequences were inspected at 10 fps from first-person/side views
for both player variants; main-PC VTK and standard feminine skin were included.
Feminine VTK insertion frames 24-50 and bolt-release frames 72-96 received every
60 Hz frame review. Dense masculine first-equip frames 180-240 were inspected;
exported readback added complete selected tactical/first-equip sequences and
critical contact checkpoints for both players. Explicit firing used 180 Hz samples
with native checkpoints. See the private receipts for precise view/variant coverage;
this is not a statement that all 149 clips were visually inspected.

A world-oriented contact solution bent the wrist about 107 degrees versus roughly
36 degrees originally. Preserving wrist-local rotation corrected that observed
regression. Suspected first-equip hand overlap at frame 230 was projection in the
offline model: another view and skinned surface tests at every frame 216-246 for
both variants found no crossing, while positive controls detected intersections.
This result does not close the user's later, unspecified thumb/contact issue.

Native graphs, procedural cameras, muscle correctives, dropped-mag physics and
runtime sound/visibility/event scheduling were not emulated. Sprint, slide, melee,
vault, friendly-idle, idle-break and equip-safe variants were structurally adapted
but not all visually reviewed. Workbench previews did not establish PBR appearance.

## Private evidence locators

If the original workspace is available, inspect these under `$CP2077_DEV`; they
are locators, not files supplied by this repository:

- `mods/ron-hk416/work/source-export/EXTRACTION-REPORT.md` and source manifests.
- `mods/ron-hk416-clean/work/vanilla/README.md` and `inherited-native-v3/` checks.
- `mods/ron-hk416-clean/work/motion-audit/inherited-workflow.md` and visual receipts.
- `mods/ron-hk416-clean/work/verification/{visual-review,package}.json`.
- `mods/ron-hk416-clean/work/forensics/final-asset-provenance.json`.

Preserve these historical receipts rather than changing their original
`runtimeVerified:false` fields after an unrelated or incompletely identified report.
Add dated user evidence separately and link it when the tested package is established.
