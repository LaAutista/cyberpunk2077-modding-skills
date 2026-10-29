# Proportions, elbow poles and contact

Use after source playback and [finger alignment](finger-checkpoint.md) have a
declared baseline. These are **INFERRED reusable solver methods** unless a bounded
case result is explicitly cited in the [evidence register](evidence-register.md).

## Solve target reach without changing limb lengths

Transfer the intended wrist/weapon goal into the actual target frame. Keep target
shoulder/elbow/wrist local offsets and scales. Different body proportions make
source joint positions unsuitable as target local translations.

For a two-bone chain with lengths `a`, `b`, shoulder `S` and desired wrist `T`,
let `d = |T-S|`. A nonstretch solver can reach only
`|a-b| + epsilon <= d_clamped <= a+b-epsilon`. Keep the original desired `T`.
Use the cosine law to obtain the along-axis elbow distance
`x = (a²-b²+d_clamped²)/(2 d_clamped)` and height
`h = sqrt(max(0, a²-x²))`. With axis `u` toward `T` and unit pole direction `v`
perpendicular to `u`, elbow `E = S + x u + h v`. Solve rotations with the rig's
actual rest axes; recompute downstream transforms parent-first.

Report **desired-target residual**, **clamped-target residual**, clamp amount and
unchanged lengths separately. A zero residual to a clamped goal does not establish
contact with the intended handle. Change root/shoulder placement only when supported
by the source/target contract, then recheck other contacts and first-person framing.

## Keep a stable elbow plane

Derive a pole from the calibrated source bend plane or a declared target reference.
Transform it into the solver's frame, remove its component along `u`, normalize,
and retain temporal sign/continuity. Near full extension or a degenerate pole,
use the prior valid plane or an explicit calibrated fallback; record the condition.
Check both left/right handedness and wrist roll. An elbow that flips only near
extension usually points to an unstable plane, not a reason to stretch the arm.

**PROVEN boundary, R1/R4:** the available source auto-IK helper is an analytic
approximation using the current elbow plane. It does not recreate the complete
Unreal LegIK/runtime graph. Native helper deformation is a separate stage.

## Work in attachment space

For weapon world `W_weapon` and source hand world `W_hand`, capture
`G_hand_weapon = inverse(W_weapon) W_hand` only during genuine weapon contact.
Apply it as `W_hand_target = W_weapon_target G_hand_weapon_mapped`, with explicit
source/target grip calibration. Use magazine space while a hand carries a magazine,
or another component space for charging handles. Do not lock every reload frame
to receiver space; it destroys release and prop motion.

Declare a contact timeline per hand/component:

| Phase | Target and checks |
| --- | --- |
| Stable grip | Weapon-relative wrist orientation, palm surface and each digit contact. |
| Release | Blend contact constraint out over an explicit time interval; retain source departure. |
| Free motion | Follow transferred source wrist/fingers; preserve mechanism/prop independence. |
| Magazine/tool contact | Follow that component's frame and intended articulation. |
| Regrip | Blend into calibrated grip while checking approach clearance and finger closure. |
| Settled return | Match idle/control endpoints without a snap or unexplained scale/translation. |

Blend orientation with normalized quaternion interpolation and hemisphere
continuity. Blend in a declared space, not between unrelated local channels.
Preserve source time and event identities when fitting a transition.

**PROVEN, R3:** a spatial-only fade was crossed in one frame by a fast reload;
an explicit 120 ms release/return envelope was used in that case. The duration is
a case measurement, not a universal constant. **FAILED approach:** a constant
foregrip/idle correction applied through reload pulled the hand off the magazine.
Use phase-specific goals; inspect the source before inventing contact ownership.

## Diagnose contact before editing fingers

If all digits move together away from the weapon, inspect wrist/control parents,
weapon placement and graph copies first. If a fingertip fits but the palm floats,
inspect source/target proportions, thumb opposition and reference alignment. If
the skeleton fits but skin folds, go to [native deformation](native-deformation.md).

For a local correction record frame/time, owner component, space, affected channels,
before/after target error and visible tradeoff. Check palms and thumb webs from the
underside, not only fingertip distances. Recheck neighboring contact phases and all
matrix rows sharing the corrected controls. Do not widen a tolerance simply to
turn an unreachable desired goal into a pass.
