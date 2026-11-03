# Motion adjustment and one concrete extraction sampler

Use for the first auxiliary MotionAdjuster output or a positively identified
uncompressed motion-extraction asset. This is saved Cyberpunk2.5 implementation
research, EXE SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`,
preferred-image addresses. It does not identify the accumulated auxiliary's
eventual gameplay recipient. Read [channel ownership](native-shared-pose.md)
before assigning camera, world-motion or skinning semantics to these values.

## MotionAdjuster inputs and descriptor

Native constructor14272EE90 binds primary1437344B8, evaluator14272F62C,
builder14272F16C and update14272F878. The pinned
[SDK declaration](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_MotionAdjuster.hpp)
corroborates input/target/duration names; instructions establish their operations.

Update visits nonnull input, target position, target direction and duration
children in that order, then copies node-update-context+8 unchanged to its dt
slot. Builder evaluates target getters; missing position is(0,0,0,1), missing
direction is authored forwardVector, missing duration0. Position/direction
presence bytes control ordinary correction. Resolved instance offsets and child
implementations are inputs. Activation14272F488 visits those same children then
sets elapsed0,k1; deactivation14272F5A0 visits them then sets elapsed0,k0.
Reset14272F7AC clears node/outgoing gates, writes previous position(0,0,0,1),
previous direction=authored forwardVector and dt0, but does not write elapsed/k.
Do not treat activation, deactivation and reset as the same operation.

Let P be the first auxiliary after input evaluation and C=[evalContext+58].
C supplies a quaternion Cq and three signed32-bit packed position coordinates
scaled by2^-17. The descriptor derives:

```text
currentPosition.xyz = packedPosition(C)*2^-17 + R(Cq,P.t).xyz
currentPosition.w = 1
currentDirection = R(Cq*P.q, forwardVector)
outputTranslation = (0,0,0,1)
outputAngles = (0,0,0)
```

Quaternion multiplication is in the shown order. Rotation14032B164 uses
`v + 2*q.w*(q.xyz cross v) + 2*q.xyz cross (q.xyz cross v)` for XYZ,
without normalizing q. Its literal fourth lane is `v.w+2*q.w+1` because its
two cross temporaries force w1. The position builder masks that result's w;
do not replace the helper everywhere with a homogeneous matrix rotation.
The builder also stores a yaw-like angle from P.q, but the decoded correction
helpers do not add it to their output angles. Neither QS scale is used here.
C's arithmetic does not by itself prove a world-space coordinate contract.

## State and correction

Let e be elapsed time, k the stored state and T total duration. If old k==1,
the evaluator proceeds directly to correction. Otherwise it tests changed
targets: enabled position squared XYZ distance from its previous value>2^-23,
or enabled direction `abs(dot(normalizedNew,normalizedOld)-1)>2^-23`.
Normalization preserves w; exact-zero vectors stay zero. Two zero direction
vectors therefore trigger the latter test. A change sets e0,k1; without a change,
old k0 skips correction, while other states enter it. Previous target vectors
are saved even on the skipped path.

Application14274604C tests **old** e before adding dt. If e>=T or
abs(T-e)<=2^-23, it writes full positional difference and the signed angle below,
regardless of enable bytes, then clears e,k. Otherwise it performs enabled
corrections and sets e+=dt,k2 when either is enabled; neither enabled clears e,k.
There is no `min(dt,T-e)` at this admission point.

For translation d=target-current, L=lengthXYZ(d), r=T-e, helper142745528
leaves the descriptor default if L<=2^-23. Otherwise it writes
`normalizeXYZ_preserveW(d)*(L/r*dt)`. In finite ordinary XYZ this is d*dt/r.
An overshoot helper can cause an earlier full-difference store, but an
unconditional store afterward overwrites it: dXYZ10,r1,dt2 produces20, not10.
The fourth lane is d.w*(L/r*dt), because normalization preserves w.

Signed Angle142745DF4 first replaces targetDirection.z with currentDirection.z,
then normalizes both XYZ. If either length<2^-23 it returns0. Otherwise:

```text
angle = sign * (180/pi) * acosClamped(dotXYZ(current,target))
sign = +1 if current.x*target.y-current.y*target.x > 0 else -1
```

It is not XY-only atan2: current(1,0,1),target(0,1,anyZ) gives+60 degrees;
opposite planar vectors choose-180. Native float constants/library rounding
remain separate from the displayed real-number equations.

For abs(angle)>2^-23, direction1427455F0 uses signed rate v=angle/r and calls
142745FE8 with current0,target=angle. The crossing test uses
`candidate=sign(angle)*v*dt`, then `(candidate-angle)*(-angle)<=0`.
A crossing writes the full angle; otherwise output is v*dt. Rate is already
signed: at r1,dt2, +90 writes+90 but -90 writes-180. Do not replace this with a
symmetric clamp. Tiny angles retain the descriptor's zero output angles.

After entered correction, evaluator replaces the first auxiliary translation
and quaternion, converting output angles through the known Euler helper and
normalizing again. It does not add the old translation or multiply the old
auxiliary quaternion into this result. Scale is unchanged. With this builder
the first two angles are0, so ordinary nondegenerate correction is a Z rotation.
If correction is skipped, the input-derived auxiliary is retained.

## Uncompressed extraction sampling

Registration1417FE5FC and inline constructor140DCF43C identify
`animUncompressedMotionExtraction`; the constructor's **final** primary is
14310F990, overwriting the base primary. Its+D8 sampler is140CF13F0 and+E0
endpoint141944950 returns duration at+30. Sample base+38/count+44 supplies
16-byte records `(positionXYZ, angleDegrees)`.

For finite t, T>0, populated count n>=1 and safe representable indexing:

1. t>=T selects the last record; t<0 selects the first.
2. Otherwise x=(n-1)*t/T, i=trunc(x), f=x-i. If i==n-1, emit that record;
   this also handles n1 without reading a second record.
3. If abs(angle[i]-angle[i+1])>180, adjust only the next angle by-360 when
   greater than the first, otherwise+360. Exactly180 is not adjusted.
4. Interpolate all four fields with(1-f),f. Emit translation with w0,
   quaternion(0,0,sin(phi),cos(phi)), phi=angle*pi/180/2, and four scale ones.

This is a **single** turn adjustment, not repeated modulo. Angles170,-170 at
midpoint give180, not0;0,180 give90;0,900 give270 after one adjustment.
The quaternion is not normalized again in this sampler. Exact CRT/CPU sin/cos
rounding is not established by analyst arithmetic.

The constructor sets duration1 and count0, so a newly constructed object alone
is not a sampled asset. This sampler has no count0 guard: the last-index path
then forms unsignedFFFFFFFF and addresses B+16*4294967295. That is an address
derivation, not an observed fault. Actual populated buffer, duration/count,
time domain and selected extraction subclass must be identified.

This sampler emits absolute time samples to the existing extraction-difference/
loop wrapper1405DF7F4. It does not itself compute loop delta or write the graph's
auxiliary wrapper. Other extraction subclasses remain separate implementations.

## SkAnimAdjuster's different correction

Primary1437340E8 binds evaluator14272B978 and its builder14272BF9C.
This is the second-auxiliary writer identified in the ownership chapter.
Its SDK names targetPositionWs/targetDirectionWs, initialForwardVector and
start/end adjustment event names. Use actual input coordinates; names alone
do not establish a correct source-to-game space conversion.

Let p,z be stored start/end, a active correction, t/u the base SkAnim state's
current/previous sample times. After plain SkAnim evaluation, a valid entry and
applyMotion are required for the additional path. In the finite ordered domain,
a new correction is initialized exactly when:

`p<=t AND u<=p AND (a==0 OR t>=z)`.

Initialization changes p=t only when t<=z, extracts loop0 motion Mfull over p..z,
gets target vectors (a missing link supplies four zeros), builds current context
QS C, calls the solver below, then sets a1. Missing direction here is **zero**,
not MotionAdjuster's authored-forward fallback. While a is active, progress
f=(t-p)/(z-p); only f>1 clamps to1 and clears a, with that call still applying
correction. Exactly1 stays active; no lower clamp or zero-denominator guard
appears. p=z=t can yield an unordered progress with masked exceptions. Actual
intervals/history are required to determine whether that branch is selected.

Correction state K and saved context C0 have this finite direct solver:

```text
R = compose(C,Mfull)
K.T = targetPosition - R.T                 # all four lanes
F = normalizeXYZ(initialForwardVector); F.w=0
D = normalizeXYZ(targetDirection); D.w=0
theta = acosClamped(dotXYZ(F,D))
if all(abs((F+D).xyz) < float32(1e-6)):
    axis = (0,0,1)
else:
    axis = normalizeXYZ(F cross D)
Qaim = (axis*sin(theta/2), cos(theta/2))
K.Q = normalize(Qaim * conjugate(R.Q))
C0 = C
```

K.scale is untouched by this solver. The fallback is fixed+Z; it is not an
arbitrary perpendicular axis for every authored F. This is full3D direction
alignment arithmetic, without MotionAdjuster's shared-Z/signed-yaw rule.
Conjugation is not a general inverse for nonunit quaternions.

The caller computes Kf=ordinaryInterpolate(identity,K,f), where that identity's
translation.w is1. It extracts Mpartial over p..t and W=compose(C0,Mpartial),
then replaces **second auxiliary** translation and rotation:

```text
output.T.xyz = W.T.xyz + Kf.T.xyz - currentContextPosition.xyz
output.T.w = Kf.T.w
output.Q = normalize((Kf.Q * W.Q) * conjugate(currentContext.Q))
```

Both context positions use signed packed coordinates*2^-17. The final current
quaternion conjugate multiplies on the **right**. These instructions do not
rotate the translation difference by that inverse. Existing auxiliary scale is
not replaced. Reordering the quaternion factors changes noncommuting cases.

Reset14272BE14 initializes K/C0 T/Q to(0,0,0,1), scales to ones, p/z0 and the
active/first-update bytes0. Activation calls base SkAnim, activates target links,
sets first-update1 and supplies p/z from named event ticks*float32(1/30), with
start0/end-animation-duration fallbacks. On the first update, a later previous
sample time replaces p; the first-update byte then clears. Derived deactivation
clears that byte but does not itself clear active correction. Base methods and
configured child side effects retain their own contracts; do not assume arbitrary
callbacks cannot write shared state.

## Scope and discriminators

Private `motion-adjuster-math-findings.md`,
`motion-extraction-uncompressed-findings.md` and `skadjust-root-findings.md` retain constructor/table/call joins,
guarded captures, failed-check records and independent finite discriminators.
Useful cases distinguish translation overshoot, negative angular overshoot,
shared-Z angle, completion-before-increment, missing versus enabled targets,
exact180 and single-turn wrapping. These checks are not native execution.

The SkAnimAdjuster solver/caller and MotionAdjuster lifecycle received separate
instruction review and finite gate/quaternion-order discriminators. Actual
children/state/coordinates, delegated base-method details, other extraction subclasses,
accumulated-channel application and final visual/game behavior retain their
separate evidence requirements. Do not expand native reconstruction to avoid
fixing a defect already demonstrated in a Blender motion review.
