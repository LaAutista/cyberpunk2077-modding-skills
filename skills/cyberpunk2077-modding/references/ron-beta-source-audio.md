# Source motion, standalone audio and Scenario diagnostics

Read this when recovering a larger Unreal weapon state set, replacing an author's
weapon-core dependency, or evaluating Scenario's local Blender helpers. Keep the
existing [port workflow](ron-port-workflow.md) and [native authoring gate](native-animation-authoring.md).
The results below are a dated 2026-10-24 HK416 beta investigation, not universal
compatibility claims. Native visual/package acceptance and gameplay remain separate.

## Recover actual state playback

Follow the active weapon class and animation-data record into paired body/weapon
montages, individual sequences and graph properties. Keep source package/build,
tool revision, mapping, codec and input hashes. In this build, pinned CUE4Parse
`990d4d7d4e0340a75a14323436d55568f1415e00` recovered 94 direct sequences,
73 body compositions over the common HK416 idle base, and 69 montage segments
across 64 FP state fields. These counts describe this manifest only.

- Montage start/end, segment rate and sequence RateScale determine playback.
  The draw sequence spans 1.5 seconds but plays from .583333 to 1.5; holster plays
  only its initial .422531 seconds. Hip/ADS firing selects G36C body motion at
  RateScale 2. A clip name containing HK416 or ADS does not identify its actual body.
- Preserve raw additive deltas independently of an absolute reference composition.
  Missing additive translation/scale channels mean zero delta, not unit scale.
  Do not treat a raw delta export with bind defaults as a true absolute pose.
  Compose over the selected weapon's actual idle so shared firing retains its grip.
- The observed local additive convention is `T=B.T+w*D.T`,
  `Q=normalize(nlerp(I,D.Q,w)*B.Q)`, `S=B.S*(1+w*D.S)`.
  The recovered ADS enter/exit graph weights are .2/.35 in this case; they are not
  generic defaults. Runtime masks, stance, procedural camera/IK and physics were
  not emulated. Keep unsupported shared interactions explicit.
- Exported montage samples may retain the entire underlying sequence. Consumers
  must apply the manifest's state-time mapping and trim; a recommended absolute
  sequence is not necessarily already trimmed. Keep raw curves/notifies/sections.
  The source holster metadata has a 14.33-microsecond duration/segment discrepancy;
  retain it instead of concealing the difference in a rounding tolerance.

Checks covered 4,765,896 sampled local channels in 94 exchange exports and 73
compositions; a separate Blender hierarchy check covered 19 core body/ADS clips
and 556,552 world matrices. The independent composition/readback paths still share
the compressed-channel decoder. All exercised raw codecs were UE per-track;
ACL and AnimScaled references were not validated. Two optional reference-base
interactions and two BlendSpaces retained failed-export evidence. Individual blend
samples were recovered; a BlendSpace is not one animation.

## Recover event audio and timing from the source

Inspect the active sound-data asset and animation notify class before searching
for loose WAVs. The HK416 FP clips lacked audio notifies, while associated active
TP body sequences/montages held `SoundSourceAnimNotify`. Preserve its time, trigger
offset, attachment and event reference. This yielded 27 actual source sound
notifies, 18 for the three reload variants; do not infer timing from waveform peaks.

The original source used FMOD banks. A small original adapter loaded the installed
game's FMOD 2.03.10 libraries and rendered events through `WAVWRITER_NRT`, without
starting a game or audio device. Match DLL ABI/version first: this version's
`System_GetVersion` takes a third build-number output argument. Source bank slicing
and names alone do not prove successful decode. Independent FSB frame/name checks,
ffprobe, finite/nonzero PCM and complete decoded lengths validated 54 embedded
HK416 samples. Keep original libraries/banks out of a redistributable helper package.

Enumerate the event's actual parameters. This event exposes `IsOutside`,
`IsSupressed` (source spelling), `Aim` and `FireMode`. Render controlled endpoints
with fixed RNG seeds and compare outputs before assigning meanings to them.

- `FireMode=1` continued firing throughout a six-second render. Playing that
  capture on every shot would stack automatic bursts. The beta instead uses a
  finite `FireMode=0` capture per actual native shot, for both trigger modes.
- Four fixed seeds produced four distinct variations per environment/suppressor
  condition. Aim 0/1 rendered identically for a fixed seed; no artificial ADS
  timbre change was added. The package retains both explicit routes.
- Rendered events preserve their original default bus/layer processing and tails.
  The first capture clipped; a uniform .25 master gain corrected output headroom.
  Remove only measured pre-start DSP silence and completed trailing silence.
  Keep the source event onset and DSP bus delay. Do not crop by an assumed latency.
- Binary inside/outside endpoints do not reproduce continuous spatial blending,
  map-specific acoustics, propagation or third-person occlusion. Final game mix,
  voice overlap at full rate, pause/resume and perceived synchronization require
  actual playback checks.

The resulting 54 PCM16 stereo/48 kHz events comprise 32 firing routes and 22
reload/handling events. All decoded with ffmpeg, had nonzero signal, no PCM rail
clipping and finished tails. That is media validation, not listening/gameplay proof.

## Use a standalone target contract

Inspect the exact installed core before deciding what to replace. Here the
reference was Weapon Core Mod (WWCM) 1.0.2.0 and SIG M7 Spear 1.0.7.0. Core supplied
shot dispatch, metadata/event registration, banks/mix routing, reload/IK/graph
services and other weapon behavior. Copying those services under new names would
retain the forbidden origin. The implemented audio needed only standard frameworks.

The tested standard route is installed AudioXL 0.8.1, Codeware and redscript on
the user's restored Cyberpunk 2.31 setup. Verify the current installed script
declarations, author documentation and DLL identity before adapting it:

- An original `ShootEvents.OnEnter` wrapper calls the original method once and
  plays audio only for a player-owned item carrying the beta's unique tag and
  live ammunition. Native state transitions own cadence; there is no second timer.
- Native `IsEntityInInteriorArea` and `CanSilentKill` select environment/suppressor
  captures. Plain 2D SFX playback retains captured firing tails; NPC audio stays
  on its existing native route in this implementation.
- Prefixed `sounds.json` rows load through the standard AudioXL directory.
  Register native event names and the private metadata through the installed
  `AudioXLAPI.RegisterEvent`/`Register` interfaces. Do not invent an API or globally
  replace a vanilla event name. This package uses no Spear/Core bank or code.
- A private `audioWeaponSettingsGroup` selected by the new item's `audioName`
  points to private normal/suppressed `audioPlayerWeaponSettings`. Fresh official
  Umbra metadata identifies the actual fields: clear `fireSound`, `autoFireSound`,
  `autoFireStop`, `burstFireSound`, `preFireSound` and `tails` in those private
  records. Retain dry fire, handling, shell, controller, melee and NPC references.
  Native serialize/readback must match; no original metadata name is overwritten.
- Put each source reload sound on one native playback owner. Remove donor sound
  events from the clips actually replaced; adding the same event to body and weapon
  clips can duplicate playback. Verify the native `animAnimEvent_Sound` descriptor
  and its frame clock with a controlled import, then read it back.

The standalone script compilation passed with only copied vanilla cache,
current Codeware, AudioXL and two original beta scripts. Neither reference weapon
nor author Core was present. Native private metadata roundtrip and installed
TweakDB resolution also passed. AudioXL startup, audible suppression, mapped-WAV
polyphony and in-game lifecycle remain user-controlled checks.

The source functional `FireRate=.0706` implies about 849.858 RPM; its UI text says
750. Native `CycleTimeBase` feeds `CycleTime`, and the weapon state machine compares
current simulation time against last-shot time plus `CycleTime`. Preserve the
native modifier chain rather than scheduling shots from an audio service.
For reload, `baseReloadTime/currentReloadTime` controls animation speed. Matching
the private base and stat to the source commit gives baseline speed 1:
tactical commit/end 2.5627425/.1039242 seconds, empty 1.9171239/.0828761 seconds.
Equip/holster **record values alone are insufficient**. The restored graph uses
phase-driven equip, while first equip is a plain sequence and holster is duration
driven. A controlled native import/readback proved active ticks0–27 and recover
ticks27–28 on the 30Hz event clock. Keep every source draw key through .916667s,
append only a .016666s endpoint hold to28/30s, and set EquipDuration=27/30s so the
active phase is not rescaled. First equip remains .916667s; holster .422531s.
This is an explicit integration choice without a source ready-notify. Game
transition/cancellation behavior still needs testing; a matching record is not proof.

## Diagnose contact in the correct coordinate space

Compare bone chains and skin separately. In the demonstrated left-thumb defect,
the old distal direction already matched the source, but source/native proximal
length differences made endpoint IK redistribute the two joint bends. Preserving
the source proximal segment directions removed the offline kink while retaining
native local lengths/scales, distal orientation and all unrelated motion. The idle
distal joint moved6.08mm (up to7.873mm over the inspected empty reload); record that
contact tradeoff instead of claiming endpoint preservation. Do not rotate the nail
arbitrarily when the source itself points forward along the handguard.

The [original adaptation helpers](../scripts/ron-adaptation/README.md) expose these
bounded thumb, index and source-camera/IK operations without project paths or
asset readers. Actual-input extraction-equivalence checks covered160 cases across
the canonical and portable copies, with zero matrix difference. They are pose
operations inside an explicit adapter, not a one-command weapon converter.

The native skin has up to eight influences and thumb muscle-helper weights above
.9. Recover the actual graph order, helper transforms and axes before attributing a
runtime skin problem solely to animation. This case recovered the point/aim/bounce
chain, but the native SimpleBounce transfer/composition semantics remain unknown.
The Blender renderer uses a declared corrective-ancestor approximation. A cleaner
render is not proof that the user's VTK thumb is repaired in-game.

Two further defects established why faithful sequence export alone is insufficient:

- Shared source automatic-fire clips shift the weapon213–229mm relative to the
  root, but only13.55–28.90mm relative to their animated source camera. Their FK
  support hand drifts35–41mm while weapon-hand IK targets stay fixed. The bounded
  adaptation solves the source two-bone arms to calibrated targets
  `IK_current @ IK_idle^-1 @ hand_idle`, retains finger locals, then maps the current
  source camera onto its idle camera for the target's fixed-camera preview. Whole
  source and corrected sequence views showed the prior drop/air grip disappear.
  This analytic solve is not the native RoN solver: LeftHandIKAlpha, twist details
  and the native bUseFireLoopAnims default/selection remain unresolved.
- Shared G36C ADS firing carries a persistent right-index offset on HK416 idle.
  The targeted rebase removes its initial local rotation offset onto HK416 idle
  while retaining time-varying trigger motion. Both target rigs were checked:
  only three index rotations change, native translations are exact, all other
  world matrices and all weapon poses remain unchanged. Inspect the guard at
  frame12/.1s and through the whole .5s shot, not just the corrected first frame.

## Respect native state contracts and inspection coverage

Trace actual graph dispatch before assigning names. Here reload/_01/_02 are random
aliases, not ADS states. When they receive one identical source sequence, copy the
canonical chest stretch track2 policy across them: the old reload_02 zero still
drives a chest constraint even if the exported bone poses look identical. Preserve
other float tracks. Keep named source variants without target routes explicit.

The target ADS graph layers automatic and per-shot recoil. Its extra automatic
layer is deliberately neutralized where no distinct source ADS loop was recovered;
the recovered ADS per-shot remains active. The actual ADS transition is a native
parameter blend, not a named transition clip. Recovered source enter/exit sequences
remain inspection-only until a justified private graph route is implemented.

Native safe_action has a real conditional dispatch and inherited mechanisms moved
10.25cm on mapped HK416 parts. Neutralizing those local channels exposed an inherited
hand pinching empty space behind the receiver at .30–1.20s. The bounded policy then
holds the new shoulder grip for that unsupported action while preserving its state
clock. Do not silently call that neutral hold recovered RoN motion.

Render the native readback through the same assembly and full skin-weight path.
Player per-shot names differ from the weapon's actual `recoil_shoulder` route;
explicitly pair them and fail if required component clips are missing. A same-name
lookup that falls back to bind can silently omit moving parts. Clamp each component
to its own duration without rescaling. Record the actual sampled endpoint: the
holster's final sample is .422531s, not its requested frame26/60=.433333s.

Record source/staged/native datasets, player/body variant, exact frame/time cadence,
angles, original images actually viewed, contact sheets and unresolved locations.
Use dense contact/fast-motion samples and full-resolution critical views in addition
to sequence overviews. Keep original input hashes or exact helper snapshots when
the adapter changes. A render manifest records generation; only the personal image
review receipt records inspection.

## Scenario: installed capability and actual evidence

The [Scenario collection](https://github.com/scenario-labs/skills) was installed
from commit `5429dea302ccc7edbce8ace9d5c1fb6852499540`, repository version .59.0,
using its supported `skills` CLI 1.7.4. It contains **166 public skills** and seven
maintainer/development skills, 173 manifests total. The installer distributed the
166 public skills, preserved 466 pre-existing tree entries, and all 1,537 installed
files matched the pinned source. Actual Codex app-server `skills/list` discovery
found all 166 with zero parse errors in both tested workspaces.

The supported local-source installation used `--skill '*' --agent codex --global`
with copied directories, not `--all` (which targets every agent). For reproduction,
select an authorized destination and pinned source, record installer integrity,
preserve prior files/settings, then verify installed bytes, lock entries and real
client discovery. A local-source lock needs an explicit source advance for later
updates. Installation does not make every optional tool/service available or put
every skill body into the initial model context.

Scenario's Blender `bx_rig.weight_report` and `bx_anim.world_pose` were exercised
on synthetic fixtures in Blender 5.2.2. Contact-centered rotation held the fixture
contact within 3.43e-7 m; a deliberately unweighted vertex was detected. A later
read-only actual-asset check covered two RoN meshes and seven VTK arm submeshes:
zero unweighted vertices/weight-sum deviations, with a one-vertex negative control
detected. VTK retained up to eight influences. This is a real weight diagnostic;
it does not establish thumb/contact repair, native muscle-graph behavior or skin
acceptance. No asset was edited by those tests.

Use those helpers as bounded diagnostics or target geometry. `world_pose` ignores
constraints on the bone itself and returns translations as well as rotations;
do not copy its output directly into a target rig whose local translations/scales
must remain exact. Convert a useful contact target through the existing explicit
rotation/control adapter. Preserve all eight skin influences and native rest binds.
`over4` is informative, not a Cyberpunk failure. Generic four-weight limiting,
rebind, model-fix defaults and Rigify bone assumptions are inappropriate here.

Local expert instructions/helpers do not require Scenario hosted generation.
Optional GUI bridges, Maya/ZBrush/engine applications, hosted account/OAuth/API
access and generation credits have their own prerequisites. No Scenario MCP was
connected, credentials inspected, asset uploaded or paid job run in these checks.
If a later authorized task uses hosted generation, check the actual payload's
dry-run cost and service access; skill installation alone authorizes neither.

## Evidence to retain

Keep separate source/composition, media, compiler, native readback, installed
record, actual rendered-frame, package and gameplay receipts. This beta retained
`core-manifest.json`, `exchange-checks.json`, `composition-checks.json`,
`blender-checks.json`, `source-notify-timings.json`, `source-render-manifest.json`,
`media-verification.json`, `private-metadata-verification.json`, isolated compiler
results, `record-checks.json` and Scenario installation/actual-asset reports.
No local commercial assets, banks, DLLs or fixed-path project adapters accompany
this portable reference. Configurable extraction/native helpers and the bounded
pose operations above are the reproducible code; case-specific composition/audio adapters remain
local until separately parameterized and validated for portable use.

Public FMOD API anchors: [System](https://www.fmod.com/docs/2.03/api/core-api-system.html),
[Sound](https://www.fmod.com/docs/2.03/api/core-api-sound.html),
[Studio System](https://www.fmod.com/docs/2.03/api/studio-api-system.html).
