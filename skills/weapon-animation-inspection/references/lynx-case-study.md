# Lynx: diagnosis, correction and evidence boundaries

This is an original account of work completed in the source modding project on
2026-10-22. The native assets, images, reports and project-specific adapters are
not distributed here. Reported measurements below are historical local results;
publication does not rerun or independently reproduce them. The included
contact-sheet and JSON-summary helpers have separate portable regression tests.
Use the [general workflow](../../cyberpunk2077-modding/references/weapon-rigging-animation.md)
for another weapon, not these offsets or donor mappings.

## Establishing the actual motion

The complete source blend had no authored Actions. Native receiver, barrel and
magazine animations plus mounted stock player clips still drove the weapon.
The investigation recovered the current native resources, component mounts,
player attachment/camera routes, native rigs and full arm meshes. The old donor
receiver export differed from the current authored animation and was unsuitable
as the acceptance input.

WolvenKit Linux CLI 9.0.1 exported 87 male and 88 female player clips and 19 clips
per component. Player export resolved stock skeletons through the real game path;
custom component export used an isolated resolver tree pointing to the donor
archive. Full arms were used; similarly named fists meshes are overlays. Four
native animations, two player GLBs, two arm GLBs, two component GLBs and four rig
JSON files had 14 preserved export hashes, rechecked during documentation. These
exports were not rerun merely to document or publish the case.

Playback used `glTF(x,y,z) -> Blender/native(x,-z,y)` and conjugated transforms
`M_glTF = C^-1 M_native C`. Actual arms retained all eight joint influences from
`JOINTS/WEIGHTS_0` and `_1`. Extra muscle joints followed the nearest shared
animated ancestor with original inverse binds: an explicit neutral corrective
approximation, not the game's muscle graph. Bind/rigid tests and five real action
samples passed locally.

An independent player comparison initially failed with a 0.648 mm position
discrepancy. Investigation reproduced Blender `FCurve.update()` merging close
imported keys at the 30 fps comparison timebase. Changing interpolation theory
did not explain it. Importing at 1000 fps, evaluating `timeSeconds * 1000`, and
asserting original component key counts and float32 timestamps preserved the
seconds and resolved the failure at the original thresholds. Both players passed
204 poses over 152 bones each; maximum position difference was 0.00545 mm.
The decoder and arm helpers needed no changes. Another asset needs its own
key-preservation assertions; 1000 fps is not a universal fix.

## Cause and accepted correction

The visible mechanism contained distinct mechanical parts inside merged chunks:

| Established defect | Local correction and preserved behavior |
| --- | --- |
| A rear disk followed the folding charging handle instead of the carrier. | Reassigned the disk to the carrier. Six unrelated GLBs stayed byte-identical in the isolated disk comparison. |
| After reassignment, the disk's upper cap still crossed the closing cover. | Retained the existing `.43` rear Y fit and relieved only the upper cap: 44 of 228 exported disk vertices above receiver Z=0.017 m, with the top brought to 0.0185 m. X/Y and lower geometry stayed unchanged. |
| A fixed bracket and pin folded with the moving lever leaf. | Moved bracket/pin ownership to the carrier; supplied a connected outer hinge and adapted handle channels. The accepted leaf fit used a 4% local extension and 5 mm outward move. |

Pivot-only, translation and fade candidates produced collisions or separation.
A direct donor-tip fit required about 32.75 mm extension, roughly 58% of the leaf,
and was rejected. The combined local weight, hinge, leaf and motion correction
preserved attachment and grasp better than these larger alternatives. None of
these dimensions is a generic fitting recipe. Do not apply `.43` without the
original assembly rule and coordinate context.

The reproducible lever baker used the preserved **pre-lever** animation. Applying
it again to corrected output would compound the adjustment. Reproduction matched
the adopted v6 JSON byte-for-byte. Checks preserved 11 complete clips, unrelated
raw keys/float tracks, events, durations, scale flags and other metadata exactly.
Independent decoding sampled 9,743 poses, with maximum error 14.094 micrometers
position and 0.018410 degrees rotation. These bounds establish codec reproduction,
not hand contact or body clearance. Native serialization then matched the
corrected JSON's `Data` exactly.

## Native geometry and collision evidence

The project exported receiver and matching shadow through its established Wine
toolchain, then round-tripped all eight meshes. Checks covered topology, native
position quantization, normals, UVs, named weights, bone identities and inverse
binds. Native readbacks, not an analytic candidate alone, fed the final probes.

| Actual native gate | Recorded result and limit |
| --- | --- |
| Disk and all current moving neighbors | 19 clips / 3,146 poses; zero fixed-wall crossings and zero cross-bone contacts. Sampling included full clips at 30 Hz, 21 exact historical keys and contact intervals at 240 Hz. Native quantization reconstruction error was 1.608e-8 m. |
| Disk baseline selfcheck | Deliberately failed collision acceptance with 489 cross-bone samples, reproducing the historical 27/8/25-pair fault keys. This established that the probe detected the original defect. |
| Disk rigid joins | 38 disk/carrier pairs remained constant on the same rigid bone. This narrow intentional join did not exempt the moving cover or other neighbors. |
| Visible and shadow lever | Both passed 19 clips / 9,731 poses at 120 Hz: zero environment crossings, zero leaf/bracket separations and exactly 29 constant pin/carrier join pairs. |

The fast lever gate cached fixed-body BVHs only after verifying identity in body
coordinates (maximum error 2.13e-14). An earlier job exited 143 without a complete
result and was not accepted; a fresh complete run passed. These are sampled
geometric checks, not continuous-time collision proof or visual/gameplay evidence.

The old `verify_lynx_reload.py` bolt check only tested a selected chunk against a
rear-stock bound `Y > -0.48 m`, plus certain cover/animation/ammunition invariants.
It was not a receiver-surface, lever or hand-contact gate. Keep check descriptions
specific enough that a broad success message cannot substitute for missing tests.

## Rendered images that were actually inspected

The local review generated complete 30 fps sequences, then explicitly opened
images at declared cadences and denser critical intervals. Rendering alone was
never acceptance. Regular reload had 148 intervals, empty reload 186 and first
equip 305; endpoints were retained. Those durations belong to the tested clips.

| Review | Actual inspected coverage |
| --- | --- |
| First-person before/after | 166 matched empty-reload/first-equip frame pairs at 10 fps including endpoints, plus eight full-size critical pairs. Alternate empty and regular reload received separate 10 fps reviews. |
| Arms-disabled native close view | Whole first equip at 10 fps; every critical empty-reload frame 120–151 and first-equip frame 180–259 on sheets; 24 full-resolution matched before/after pairs. No remaining visible mechanism defect was found in that coverage; attachment and cover/carrier travel were retained. |
| Opaque hands for both player variants | 30 inspected images, including ten final native frames. No clear exterior palm/thumb/knuckle breakthrough or detached grasp was visible. Internal finger/metal overlap remained: sampled worst about 2.9 mm versus about 2.1 mm for the donor. |

The hands needed a crop centered on index/middle/thumb landmarks, with 0.24 m
orthographic scale, rather than the earlier wrist crop that cut off fingers.
Full-resolution checks included empty-reload frames 125, 128, 133, 135 and 142,
and first-equip frames around 206 and 222–225. Dense numeric sampling did not
imply equally dense visual review. Arms-disabled clearance review did not establish
first-person or hand acceptance; those had separate review receipts.

Interrupted rendering without a completion manifest was retained as incomplete.
A project batching script rendered at most 80 frames per job and only combined
batches with matching settings/input hashes and a complete contiguous endpoint-
inclusive frame list. Leftover PNGs were not treated as a finished sequence.

## Package and remaining limits

All 22 archive resources matched verified inputs. Only the receiver's visible
mesh, shadow and animation changed; the other 19 were byte-identical. ZIP integrity
and payload comparisons passed. The original completion work did not install or
game-test that release.

The offline previews did not reproduce native material/shader graphs, scope
transparency, game camera effects, animation blending, runtime IK or customized
arms. Native readback previews reused source preview materials. First-person FOV
was deliberately set to 75 degrees. Graph-driven normal/reload magazine visibility
switching was not reconstructed. Recoil held `idlepose_shoulder` frame zero while
playing receiver recoil: a **static-arm illustration**, not full recoil hand-graph
verification. Trigger contact and all firing/player/graph combinations were not
exhaustively checked. Preserve these limits when applying the broader checklist.

## User-reported laptop reload test

The user later reported a **clean Lynx reload on the unupdated laptop**. This is
positive user-reported gameplay evidence for the package they tested. Its exact
hash, game/dependency versions, player rig and reload variant were not supplied;
identity was not independently reconciled with the completion release or a later
combined ZIP. Do not assign either artifact's hash to that test without evidence.

The report does not establish every animation, platform, customized arm setup,
additive graph or future package as flawless. Broader runtime coverage needs an
identified package and explicit test conditions. The reusable result is the
diagnosis, bounded correction and layered verification method—not a universal
animation-compatibility claim.
