# Source weapon and first-person animation adaptation

Use this alongside the [rigging workflow](weapon-rigging-animation.md), not instead
of its collision, visual and native checks. The HK416 supplied the measured examples;
its bone names, offsets, asset paths and thresholds are not a universal adapter.
Read the [current proven HK416 retargeting workflow](../../cyberpunk2077-animation-retargeting/references/ready-or-not-workflow.md)
for the CG replacement, user-confirmed locomotion fix and separate camera-comfort
revision. The [earlier case and issues](ron-hk416-case-study.md) retain historical scope.
For later full-state recovery, source FMOD audio and Scenario weight diagnostics,
read the [beta findings](ron-beta-source-audio.md); they do not supersede native
rest/weight preservation, visual review or gameplay acceptance.
The [historical project command contracts](hk416-project-commands.md) preserve
assembly/render/cook examples and explicitly identify unavailable private adapters.

## Tools and prerequisites

| Stage | Working route | Boundary |
| --- | --- | --- |
| Unreal recovery | Pinned native Linux CUE4Parse + original RonExtract helper; [commands and converter patch](ron-source-extraction.md) | Installed-build mappings, Oodle and actual codec must pass separately. No FModel/Wine or ACL playback acceptance inferred. |
| Source exchange | Pinned UEFormat importer in isolated Blender configuration | Full skeleton, additive base, component mounts and raw montage/curve metadata required. Import success is not faithful playback. |
| Native animation authoring | Installed WolvenKit 9.0.1 Modkit via [portable adapter and independent checks](native-animation-authoring.md) | First prove unchanged and controlled-edit round trips on copies. Preserve unrelated clips. |
| Adaptation/inspection | Blender scripting, explicit assembly mapping, [additive preview](../../weapon-animation-inspection/references/additive-preview.md), [contact sheets](../../weapon-animation-inspection/references/contact-sheets.md) | Included helpers do not supply a generic rig fitter or render every game's assembly. |
| Mesh/material cook | Project's established native/Wine WolvenKit route with compatible native containers | Actual geometry, binds, texture semantics and material references require readback. |

The recorded main-PC environment used CachyOS, Blender 5.2.2, .NET SDK 10.0.400
and WolvenKit 9.0.1. Use [configurable paths](environment.md). Match versions and
dependencies before reproducing; a different build needs its own compatibility gate.
No new MCP server was needed; retain the [existing tool-selection decisions](tool-selection.md).

## 1. Establish source identity and completeness

Record the installed build/executable and archive inventory. Follow the active
weapon class through its selected mesh, animation-data record and paired body/weapon
montages. Recover matching arms **and** the full player skeleton, separate magazines,
rounds, sockets, materials/textures, additive bases, curves, notifies, montage sections
and graph-driven visibility. A similar filename or rifle design proves none of this.

Distinguish index reads, payload decompression, package deserialization, actual codec
decoding and exchange export. Check every stage; identify the exact failed asset,
command and missing requirement. The [extraction reference](ron-source-extraction.md)
contains the bounded fixes for POSIX paths, endpoint timing, missing additive scales,
curve retention, quaternion normalization and hold endpoints. Never repair a decoder
error by scaling the entire weapon or smoothing away a discontinuity.

Record allowed origins per file. A renamed depot and absence of external mod
dependencies do not remove embedded donor animation, rigs, materials or calibration.
If those origins are forbidden, rebuild with original source exports and freshly
recovered official target resources. Audit native string and numeric resource
references, plus positive source lineage; a forbidden-word scan alone is insufficient.

## 2. Reconstruct faithful source playback

Establish units, handedness, local transforms, parent order and inverse binds.
Compare decoded local samples against exchange samples and independently accumulate
the hierarchy. For this source, 121 endpoint samples at 60 Hz span two seconds;
the exported body is already composed with its idle base. Adding that base twice
is wrong. A weapon clip whose name contains `add` was actually absolute.

Retain raw curve interpolation flags and montage metadata when the exchange format
omits them. Reconstruct documented graph actions separately from raw keyframes.
For this reload, attached-magazine visibility was controlled by an AnimBP scale
replacement, not raw bone keys. Dropped-prop physics and procedural hand IK were
unavailable: label their absence rather than claiming runtime parity.

Render complete source first-person and mechanism/contact views. Inspect the actual
numbered sheets and original frames, including endpoints and dense fast transitions.
Record the source camera and FOV; an approximate target camera is a different check.

## 3. Map assembly and graph contracts before fitting

Inventory source/target dimensions, pivots, attachment sockets, component transforms,
rig hierarchies, all skin influences and actual clip dispatch. Use explicit
player-to-receiver, receiver-to-weapon and magazine transforms; do not reuse a Lynx
or rejected donor calibration. Fit rigidly at the intended scale before making a
justified local geometry correction.

Inspect the player graph's controls as well as FK bones. The tested graph reads
hand IK controls and copies a weapon control into `WeaponRight`. A visually clean
FK-only preview can still disagree with this contract. Preserve exact native limb
local translations/scales, solve rotations for reach, synchronize required controls,
and preserve unrelated helpers relative to their parents. Report unreachable targets;
do not stretch arms to conceal a mismatch.

Use the actual player skin, including every influence set. The inspected VTK skin
had up to eight influences and weighted corrective bones outside the principal rig.
Ancestor-following correctives are an offline approximation of the muscle graph.
Matching main-PC binds does not identify the laptop's installed skin or winning mod.

## 4. Correct contact and mechanisms locally

- Derive grip targets from the fitted geometry and source operational pose. Keep
  the tactical magazine path independent of the foregrip correction; a correction
  that helps idle can pull the reload hand away from the magazine.
- Use contact-surface landmarks, not only bone pivots. For rear-latch contact,
  preserving hand world orientation folded the wrist. Preserving wrist-local
  rotation while solving the shoulder/elbow and forearm-to-fingertip segment
  removed that established regression. Inspect skinned fingers afterward.
- Recover closed/open transforms relative to the weapon root. Reuse appropriate
  target timing envelopes while mapping travel direction and amplitude to the
  source mechanism. The HK416's manual handle moves with the bolt; its handle
  does not reciprocate during firing. A child catch must not inherit unwanted
  handle travel. Bone-name similarity does not establish these mechanics.
- Check constant operational offsets. The selector was stationary during reload
  but rotated relative to mesh bind. Prepose only that geometry/normals when
  supported by source evidence; do not add unnecessary animation or distort the rifle.
- Sample native key times as well as regular preview frames. A 60 Hz grid missed
  the original 22.222 ms recoil peak; the firing preview used 180 Hz plus exact
  native-key checks. Compose additive **player** recoil over the chosen corrected
  normal base, while selecting the weapon's actual Normal recoil clip separately.

Reinspect all affected variants, including tactical reload, first equip, firing and
ADS. In ambiguous 2D overlap, inspect another angle and the posed surface geometry.
Use a positive control for collision probes; no surface crossings is not proof of
closed-volume clearance or native muscle-graph behavior. Preserve failed attempts.

## 5. Export, read back and inspect the exported result

Follow the [native authoring gate](native-animation-authoring.md). Preserve complete
sets, untouched chunks, skeleton metadata, float tracks, events, fallback lookup
arrays and interpolation modes. Do not infer key count from a compressed header's
nominal frame field. Compare against the unprepared expected data and keep clock
quantization separate from spatial or interpolation error.

The mesh importer in the recorded route lost inverse-bind rotations. Restore the
complete expected palette **by bone name**, then independently inspect actual native
topology, UV sets, normals, named weights and inverse binds for every component.
Material slots and source texture hashes are not an engine PBR test: check channel
packing, gamma, normal convention, orientation, compression and mip chains too.

Render the actual native readback through the same inspection path without applying
authoring corrections again. Hash inputs before loading and after rendering. Join
short completed jobs only when input identities and frame coverage agree; failed
or partial jobs are not accepted evidence. A byte-exact clip-continuity proof can
preserve earlier scoped reviews after unrelated clips change, but must cover
descriptors, events, sample values/times and renderer skeleton data.

Keep the existing [animation/material summaries and regressions](tool-selection.md).
After packing, extract the archive and compare its files byte-for-byte to checked
inputs; verify loose files and ZIP contents. Package integrity does not prove
resource selection, shader appearance, reload events or sound in the game.

## 6. Carry evidence and open defects between machines

Separate source, automated, visual, native-export, package and user gameplay evidence.
For visual review, state exact clip, player/skin, camera, frames and cadence. For a
game report, record only what the user confirmed; ask for package identity when it
matters instead of inventing it. Keep native defects and rendering approximations
distinct from observed runtime defects.

For unresolved contact, optic, material or sound problems, record location/time,
image or log, attempted changes, tradeoffs and the next discriminating check.
The [HK416 issue table](ron-hk416-case-study.md#current-user-reported-status) is an
example. A reload playing is valuable evidence, but it does not close its thumb,
aiming, texture or audio issues or validate every player/animation/platform.

For the later editing-rig/rest-frame failure, private equip gate, shared locomotion
contact constraints and actual ReArmament aiming audit, see
[HK416 rest, scope and inspection findings](hk416-rest-scope-inspection.md).
Its numeric/export results and unresolved Neto MAX/gameplay boundaries are separate.
