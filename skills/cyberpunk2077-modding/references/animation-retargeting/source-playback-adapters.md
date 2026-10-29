# Source playback and format adapters

Contents: [adapter boundary](#adapter-boundary), [Unreal/RoN/Halo](#unreal-ron-and-halo),
[MAX/FBX](#max-and-fbx), [FO4/NIF/HKX](#fo4-nif-and-hkx), [CP target](#cyberpunk-target),
[future adapters](#future-adapters). Evidence IDs resolve in the [register](evidence-register.md).

## Adapter boundary

Use an explicit source profile: input build/hash, mesh/skeleton/clip binding,
timebase/range, coordinate basis, rest/binds, evaluated pose dependencies,
component/mount graph, events/curves and codec limitations. Produce a neutral
description of sampled local/world transforms, named skin influences, component
tracks and clip-relative events with provenance. This is a design contract, not
an implemented common file format or advertised cross-engine converter.

Separate native decoding → source evaluation → coordinate exchange → target
retarget → target native serialization. Compare across each boundary independently.
An exchange roundtrip can faithfully preserve an incorrectly evaluated source.

## Unreal, RoN and Halo

**PROVEN, R1:** RoN recovery used pinned CUE4Parse/RonExtract, complete player
skeleton, paired weapon/body montages, additive bases and raw metadata. Index
reading, payload decompression, deserialization, codec decoding and exchange export
are separate gates. A PAK inventory is not animation playback proof.

Recover the effective sequence/montage segment, trims, rate scale, base pose,
notifies, interpolation, visibility/masks, attachments and graph-driven controls.
Record what remains absent: procedural hand IK, camera, physics, live branch
selection. Source body reload was already base-composed once; the weapon reload
was absolute despite `add` in its name. Do not add an idle base twice or infer
semantics from filenames.

The recorded RoN additive convention was
`T=B.T+w*D.T`, `Q=normalize(nlerp(I,D.Q,w)*B.Q)`, `S=B.S*(1+w*D.S)`.
It differs from the target bind-relative exchange contract below. Preserve
noncommuting-rotation and first/last-sample regressions.

**Historical original-Unreal BR boundary, H1/H3:** Halo raw source skin samples match native section
BoneMap/weights/binds within the recorded bound, while viewed support fingers
remain open. Source grip still FAILS. The missing input is a provenance-matched
final evaluated settled-idle pose (76 arm / 10 weapon matrices and attachment
state), or an identified additional pose-changing writer. Do not declare offline
exhaustion or require a game launch merely because current reconstruction fails.
A generic marker-IK fixture used an inapplicable descriptor and is rejected for BR.
These failures remain evidence for that branch. The current owner has selected
Haru/NovaFinch FO4 BR55 HKX as primary animation source while retaining HCE visuals;
see the [ownership/source snapshot](evidence-register.md#active-ownership-and-source-choice).
Do not apply the old Unreal 76/10-matrix input contract to a different HKX source
or infer that Haru native playback has passed from source selection alone.

RoN workflow: native source playback → explicit target mapping/retarget → matched
source/retarget/native finger views. Borrow that order, not RoN offsets, helpers,
source camera, mounts or grip corrections for Halo.

## MAX and FBX

**PROVEN, M1–M3:** M1911 inventory contains 112 MAX scene names; inspected native
application is Max 2021 / 23.0.0.915. Idle is 30 fps, 0–100, 160 ticks/frame;
reload is 60 fps, 0–180, 80 ticks/frame, 3.0 s between endpoints. Query every
scene's actual clock/units/dependencies. Filename coverage is not evaluated coverage.

Capture native evaluated mesh positions, faces, named weights, node/object/bone
matrices and Skin cluster binds alongside FBX. Preserve each mesh's own cluster
Transform/TransformLink: identical bone names do not establish identical mesh binds.
Frame 0 is not proven initial Skin bind. FBX scene FPS is not curve sampling proof.

The reload-v1 FBX had 60 fps metadata yet changing curves contained 91 keys / 30 Hz.
It fails surface parity, including 48.878 mm magazine error at source frame 41.
The 60 Hz regression checks raw FBX tick spacing **769,769,300** at
**46,186,158,000 ticks/s**, inclusive samples k=0..180, and source odd frames 39–49.
Retiming, offsetting a frame, interpolating duplicate keys or relaxing tolerance
would conceal the failed source exchange. Exporter cached clock state remains a
hypothesis; do not label the prepared ResetExport route a proven fix without its
new output/readback receipt. FBX `Resampling` is an unroll-filter parameter, not
a request to set sampling rate to 60.

Two weighted terminal Point helpers survived raw FBX clusters but were omitted as
bones by the Blender importer. `GeomAsBone=true` alone failed. The idle-v4 case
temporarily enabled exactly those two helpers as bones, proved zero source geometry
change over 101 frames, exported, then restored their flags. Preserve weights and
identities; do not reassign missing weights to an ancestor or change every Point
mechanism node. This case-specific route needs a new proof on another source.

Idle-v4's separate paired-topology certificate bounds all captured static surfaces
to 5.55 µm. The raw sampled-BVH report still FAILS; bind/contact/moving playback
remain unverified. Static idle cannot validate the rejected moving reload.

## FO4, NIF and HKX

**PROVEN static inspection, F1/F2:** Human Animation Rigs 2.8.3 has explicit
control/proxy/IK/torsion systems and a 94-bone first-person export list distinct
from 162 deform flags. Some inspected female weights use five influences. Its
code forces 30 fps; no export or addon evaluation was run. Do not import its
scale, forearm torsion coefficients, bonelist or timing as CP defaults.
The [full Shiagur guide text is now reviewed](shiagur-reference.md), independently
of that earlier data-only inspection: matched skeletons, separated root/body/weapon/
camera spaces, fixed-hand/follow controls, assembly pose, events and offline viewer
are useful concepts. Its authoring recommendations remain distinct from validated
source playback, native CP controls and actual exporter compatibility.

Bingle-linked VibePort v0.72 (metadata 0.7.2) supplies calibrated source deltas,
separate world/local rotation mapping, palm frames, ordered FK/IK, nonstretch
two-bone reach, quaternion continuity and clip-owned annotations. The mapping has
30 finger rows within 44 mappings and **zero weapon/mechanism rows**. A weapon
adapter still needs actual 1P/3P mesh/NIF/skeleton/clip pairing, pivots, component
ownership, mechanism motion, contact intervals and explicit target event mapping.

The inspected PyNifly `hk_2014` native loader is a **candidate only**. No weapon
HKX import, roundtrip or runtime validation was executed. Legacy hkxcmd fallback,
native loader/writer and XML paths are separate. Animation parsing does not recover
source gameplay graph evaluation. Direct code reuse licensing/provenance remains
unverified; this hub synthesizes techniques without shipping that addon.

Current Haru BR55 header inspection is a separate owned data-only check, recorded
in `fo4-hkx-reader-review/REPORT.md` under the active source workspace. It finds
53 spline and 19 lossless clips; the unmodified candidate reader handles no
lossless clips and does not preserve raw blend semantics. Reload has 94 tracks,
103 frames at 30 Hz / 3.4 s; the inspected single-fire clip has 23 frames at
60 Hz. Empty binding maps/blank annotation names require the canonical external
94-bone order, not Blender HUM1 enumeration. These header/event facts do not prove
motion decoding, correct source skin/contact or target retargeting. Keep the
parent's selected source separate from a validated source-playback result.

Before any future reviewed adaptation, validate a known source skeleton/weapon
fixture independently. Account for Blender 5.2 channelbags: the inspected retargeter
uses legacy `Action.fcurves` and can delete same-named Actions. Preserve originals.
Do not install or execute this inspected code merely because it is linked here.

## Cyberpunk target

Choose the installed native rig, mesh, graph, component containers and actual clip
dispatch. Preserve Normal, Additive and AdditiveWithoutFirstFrame semantics;
do not place absolute source poses directly into additive slots. CP bind-relative
exchange uses original native bind B:
`E.T=B.T+D.T`, `E.Q=normalize(B.Q*D.Q)`, `E.S=B.S*D.S`.
For desired pose P over selected normal base L, use
`D.T=P.T-L.T`, `D.Q=inverse(L.Q)*P.Q`, `D.S=P.S/L.S`.
Keep the first authored sample of AdditiveWithoutFirstFrame.

Use the existing [native authoring contract](../native-animation-authoring.md)
and [event/export chapter](events-native-export.md). It covers a bounded installed
WolvenKit 9.0.1 adapter, not new skeletons, arbitrary events or full runtime graph.

## Future adapters

**COD and Battlefield: UNTESTED.** There is no validated source profile, decoder,
evaluated reference pose, clip/event mapping or CP retarget fixture in this hub.
Before support claims, identify exact game/build/format, obtain authorized inputs,
validate source playback independently, and repeat the same source/bind/finger/
retarget/native/runtime gates. Similar file extensions do not establish support.
