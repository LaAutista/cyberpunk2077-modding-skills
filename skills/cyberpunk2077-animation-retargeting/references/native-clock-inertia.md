# Native update clocks and inertialization

## Scope and provenance

These are offline implementation findings from the retained Cyberpunk 2077 2.5 executable with SHA256 `d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`. Addresses are preferred-image virtual addresses, not ASLR-adjusted runtime addresses. Re-establish artifact identity and class/constructor/vtable correspondence before using them on another build. This reference does not establish active gameplay settings, runtime timing, visual quality, or Saber acceptance.

Retained investigation evidence is grouped under `animation-graphs-research/transitions-deep/`: `clock-inertia-findings.md`, `clock-controls-setting-followup.md`, `frame-units-findings.md`, the `clock-*.asm`, `frame-unit-*.asm`, `inertia-*.asm`, matching JSON data/guard receipts, `check_frame_units.py`, `check_inertia_math.py`, and `check_inertia_followup.py`. Sibling `shared-pose-deep/` and `blending-deep/` contain the independently traced rig-view/pose ownership and QS-composition helpers. Evidence filenames here identify a retained research set; they are not installation dependencies or absolute local links.

## Clock producer and propagation

The concrete registered animation callback is `0x140d33bec`. Binder `0x14212f4f0` binds its function-pointer cell `0x14394b258`; registrar call `0x14153d70c` supplies bucket mask7, stage8, and literal `EntityAnimations/Update`. This corroborates the SDK's AnimationUpdate stage and all-three-buckets mask.

The callback reads a frame record's float+0 and details pointer+8. Its path is:

```text
0x140d33bec → 0x14079d980 → 0x14079e758
  → task submission 0x14212f9e0
  → wrapper 0x142131650 → task 0x1421301c0
  → chain host 0x1401b3e00 → 0x1401b5af4
  → graph host 0x1401b25dc → graph update 0x1403a9d90
  → root update dispatcher 0x1426dd068
```

Unwind ranges split the task body; do not treat each range as a complete logical function. The task initially uses its copied frame increment, but a nonnull component owner replaces it through owner virtual+0x120 (`0x1401f712c`). The returned pair's float+4 becomes chain context+0x40 at `0x14213060b`. Separate chain context+0x44 receives the detailed-time float+0; these are different fields.

The admitted host path copies chain context+0x40 → per-graph host context+0x50 (`0x1401b4071`, `0x1401b41df`) → graph-update context+0x80 (`0x1401b27bd`, `0x1401b28c3`) → node-update context+8 (`0x1403a9dab`, `0x1403a9e7e`). State-machine update `0x1403aa174` consumes the latter. Nested-graph bridge `0x1403a8fdc` also copies node increment through; it is not an independent clock source.

### Entity time policy

Concrete vtable identity ties base `entEntity` virtual+0x120 to `0x140c298a0` and `gamePuppet`'s override to `0x1401f7324`. Let d=details.float+0 and g=details.float+4. Base Entity returns scale g and increment d*g. Puppet supports the following ordered branches:

| First satisfied predicate | Returned scale | Node-bound increment |
|---|---:|---:|
| Recursive owner-chain flag bit0 at object+0x258 |1|d|
| Else recursive flag bit1 |e|d*e|
| Else recursive flag bit2 |e*g|d*e*g|
| Else |g|d*g|

Predicates `0x1401f73b0`, `0x1401f7444`, `0x1401f74dc` follow the weak owner handle at+0x248/+0x250. Scale helper `0x1401a4dfc` uses local `(object+0x240)->float+0x24` when local bit2 is set, otherwise an eligible ancestor's value, otherwise1. User-facing flag names are not assigned from these bits alone. Other entity overrides are outside this proof.

Discriminator: d=.02,g=.1,e=.5 gives increments .02,.01,.001,.002 across those four branches. Therefore substituting raw frame delta for every transition clock is wrong on this path. The active branch in a particular gameplay session still requires observation.

The entity factor's producer is now joined. PuppetBase constructs the 88-byte
state at owner+0x240 through `0x140235734`, initially setting target/current factor
to1. TimeDilatable's registered callback `0x140f206b8` calls `0x142159050`, which
clamps requested factor to float32(1e-6)..10, sets policy bit2 when target differs
from1, and calls state setter `0x1420b4960`. That setter saves current factor as
the blend source, stores target/duration/curve names and resets elapsed.
Puppet virtual+0x198 leads through `0x1401f719c` to updater `0x1420b47a0`;
the animation clock reads the same state's+0x24.

The updater starts with the target plateau, but selected named curves can replace
it: blend-in gives `e=target*w+source*(1-w)` and blend-out gives
`e=target*w+(1-w)`. A negative source sentinel uses1. Curve evaluator `0x14062008c`
returns the decoded scalar kernels directly, with no [0,1] value clamp; the
factor store also has no final clamp. Preparation uses the last key time as the
phase span. Valid curve records, times and actual phase selection are required.

Consequently a direct requested0 becomes the positive minimum, but positive
targets alone do not bound the curve-driven result. With source1,target.5 and
a valid constant curve times[0,1],values[2,2], an active blend-in at elapsed.125
gives `.5*2+1*(1-2)=0`. Target.25 gives -.5. These are finite, asset-conditioned
examples; they do not claim shipped curves or Saber select them. If both endpoints
are positive and every selected w lies in [0,1], this route instead preserves
positivity. Selected assets/flags/history/timing remain the needed inputs.
Retained provenance: `transitions-deep/inertia-factor-followup.md`, typed
constructor/callback/writer joins and finite branch checks.

### Physical units, frame cap and global scale

The normal frame producer establishes seconds from QueryPerformanceCounter and QueryPerformanceFrequency. Timer provider `0x1405d6918` initializes singleton `0x143c37b48` through `0x1405d3ddc`: it stores reciprocal frequency and an offset equal to the negated initial counter divided by frequency. Microsoft's [QueryPerformanceFrequency contract](https://learn.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancefrequency) defines the frequency in counts per second.

Driver `0x1405d5828` computes double `now=counter/frequency+offset`, subtracts the previous value at engine+0xf8, stores the new value, converts elapsed time to float32 and applies an upper cap:

```text
d = min(float32(now - previous), float32_bits(0x3d872b02))
g = clamp(product(registered scale factors), float32(1e-6), 10)
details = {d, g, scale-list-owner}
FrameInfo.deltaTime = float32(d * g)
```

The cap is approximately .066 seconds. The proven callback runs only when capped d is ordered-positive. Binder `0x1407b3214` supplies callback `0x1405d4e2c`, which constructs the details record and multiplies d*g before engine virtual+0xb0. Scale producer `0x1405d3f54` multiplies +0x24 in each 0x88-byte registered entry, then clamps. These finite-input equations do not generalize nonfinite factor behavior.

Constructor/vtable and task-copy traces connect this callback through framework virtual+0x10, GSM driver `0x1404bde38` and state virtual+0x128, session virtual+0x18, scheduler `0x1408ecfa4`, bucket task `0x1404ba494` and descriptor invocation `0x1404ba638` to animation callback `0x140d33bec`. The intervening transfers copy the delta and details; Entity/Puppet then select the policy above. Their use of details d and g can replace the FrameInfo increment, so do not multiply by g again automatically.

The cap occurs **before** global scaling: elapsed .5 seconds with g=1 feeds approximately .066; with g=10 it feeds approximately .66. A 1/60-second interval with g=.5 feeds about .00833333 while details preserve about .01666667 and .5 separately. This is neither uncapped elapsed time nor `min(elapsed*g,.066)`.

This closes the unit question for the connected normal path without observing the actual timer frequency, Wine implementation, current scale factors or cadence. Preserve the same unit for duration and increment; do not introduce another frames-to-seconds conversion merely because Blender displays frames.

### Reflected graph time controls

Actual AnimGraph constructor `0x140ce99fc` stores primary vtable `0x1430e9b88`. Its QWORD store at `0x140ce9a90` initializes resource+0xE8 to float1 and resource+0xEC/+0xED to zero, matching reflected `timeDeltaMultiplier`, `isPaused`, `oneFrameToggle`.

Actual property registration at `0x140d17878`, `0x140d178ee` and `0x140d1794f` ties those names to resource offsets E8, EC and ED. The registrations add low flag bits 0x9; builder/finalizer paths carry them into final CProperty+0x28. The SDK calls bits 0 and 3 only b0/b3, so the flag value does not establish editor-only or transient behavior.

Concrete lifecycle traces now give bit3 a bounded meaning: actual class+80
traversal262304C, normal stream-read27A460 and stream-write626A00 skip properties
with bit0x8 before their normal field handlers. The constructed control flags are
18B004009, so all three skip these controls on those routes. This is not a
universal serialization/editor-only label. External visitor callbacks and
specified malformed-input branches retain their own limits.

The separate class+88 named-input route2622FA0 does not apply that skip. For a
matched control, field-address helper27AA30 returns G+offset because bit21 is
clear, then passes that address to the property's type+88 handler. This proves
a typed address-access facility. Registered Float/Bool type+88 wrapper2624A3C
saves that address, requests text from the external input's+58, and only on
success calls type+70 with the field pointer and text. The actual external caller
and parser grammar remain unexpanded; successful arbitrary parsing or playback
semantics do not follow. Compiler pre-visitors change G118/G78 and node layout;
descriptor callbacks drop their captured G pointer.

The instance+78 route instead constructs a **source-object/property adapter**,
primary143042388, retaining a source handle at+58/+60. It does not clone the
source payload; the earlier1.8.4 label "A clone request" was unsupported.
Its promoted source is S=[G+8]; S=G requires the self-handle identity, which was
not independently re-established. Adapter-derived addresses are S+offset;
the direct named-input route above already carries G itself.

Adapter read fallback14EAD7C and write fallback2624170 use matched descriptors
without the serialization bit3 skip. With bit21 clear, their address helpers
return S+offset. Selected registered Float/Bool+90 readers require an empty
remaining path and load exactly four bytes or one byte. Corresponding+98
writers likewise require an empty remaining path for these field-access branches;
a nonempty remainder takes diagnostics instead. They accept value tag0 by
clearing exactly four bytes or one byte and returning
true; tag1 delegates to text parsers. Parsing, formatting, registry startup and
replacement behavior are not supplied by these bodies. An admitted adapter
write additionally requires a valid source/value, optionA30 zero, associated-owner
admission and successful path/type dispatch. Success invokes S+38 and then an
optional external notification; actual AnimGraph+38 is a no-op. Arbitrary external
callbacks are not assumed pure. These are concrete value operations, not pause,
delta scaling or one-frame advancement. Retained provenance is
`graph-control-deep/g1-lifecycle-findings.md` and
`g1-property-adapter-findings.md`; no global inactivity is inferred.

The official Blender add-on at revision7a4ee793 likewise transports these names
as source metadata: [import](https://github.com/WolvenKit/Cyberpunk-Blender-add-on/blob/7a4ee793c36d9615946fe87ec9d42cde7568021d/i_scene_cp77_gltf/importers/animgraph/parser.py)
stores them in `red_rootchunk_scalars_json`, and [export](https://github.com/WolvenKit/Cyberpunk-Blender-add-on/blob/7a4ee793c36d9615946fe87ec9d42cde7568021d/i_scene_cp77_gltf/exporters/animgraph/root.py)
copies that metadata over defaults0/0/1. These two functions do not implement
native graph time control. Source inspection is not an executed Blender round trip.

Those declarations/defaults do **not** prove their shipping evaluation behavior. Normal graph entry `0x1403a9d90` copies incoming context+0x80 unchanged into node context+8 before dispatch; it does not apply resource E8/EC/ED. Its apparent +E8 read is from the incoming context, not the resource. The resource+C8 condition helper `0x1403ab21c` searches ID/pointer entries without changing that clock. Inspected typed resource hooks likewise supply no pause/scalar operation. The node context retains the graph pointer, however, so arbitrary downstream node use is not excluded by this entry trace.

Concrete Root registration/constructor ties primary1430C0000+120 to1403A9FE4.
That complete callback selects node68 when nonnull, otherwise the first array48
child when unsigned count54 is positive, otherwise returns. It forwards node
context N (N[0]=G,N+8=the incoming increment) and instance unchanged. It does not
read N or G. This closes the Root bridge, not the selected child's implementation
or actual topology; no universal absence of a control consumer follows.
Retained provenance: `graph-control-deep/g1-root-node-update-findings.md`.

The outer ordinary host has a distinct admission gate. At `0x1401B27B0`,
`0x140BF2880` takes instance I, obtains G=[I+20], and evaluates this ordered
predicate (offsets hexadecimal; q unsigned32, L signed32):

```text
if byte[G+A2] != 0: reject
if byte[I+25B0] != 0: reject
R = pointer[I+40]
if byte[R+94] == 0: admit
L = signed32[R+90]
if L < 0: admit
admit exactly when q < unsigned32(L)
```

A false result skips this host's ordinary update call at `0x1401B2A50`.
Nested GraphSlot reaches the inner update without this gate; A2 does not
therefore disable every graph update. The leaf has no calls/writes and does
not access E8/EC/ED. These gates are not substitutes for pause semantics.

Before this gate, `0x1401B25A8` computes q from h=unsigned32[H+C0],
K=unsigned32[R+7C], n=unsigned32[R+8C]. If n=0, q=min_unsigned(h,K).
Otherwise i=min_unsigned(h,n-1), v=unsigned32(sign_extend_int16([R+80][i])),
and q=min_unsigned(v,K). Negative map entries are not rejected: -1 with K=5
gives 5; -2 with K=FFFFFFFF gives FFFFFFFE. A map need not be monotone:
map[2,0,4], K=4, L=2 gives reject/admit/reject for h=0/1/2 when other gates
admit. Equality rejects; negative L admits before that comparison.
Because q is computed first, its storage requirements remain even when A2
would reject. The SDK's rig field names corroborate the R layout, but the
I+40 producer/type join and H/b/c/L producers are not established by these
leaves. Their policy and actual values remain distinct boundaries. Provenance:
`g1-admission-gate-findings` and `g1-admission-q-findings`.

Bounded byte-load/test plus MOVSS/MULSS displacement scans found unrelated owners and a countdown-like reader, without identifying a typed AnimGraph consumer. Alternate/debug callers, additional instructions and indirect handling remain open. Do not claim globally unused, deprecated, or editor-only; do not add an offline multiplier/pause implementation solely from names. A causal test would hold other inputs fixed, vary each resource field separately, and observe both update admission and node delta at the actual dispatcher. Such a test has not run.

## Inertia request, history and elapsed ordering

Registration/class/constructor identity establishes `animAnimNode_Inertialization`'s instance vtable `0x1431cddc8`: update slot36 is `0x140bb710c`, evaluate slot37 is `0x14060e9f4`. Constructor is `0x14127f800`.

Update evaluates its input's update first. In its admitted branch it shifts previous/current stored increments and reads current node context+8. Request byte context+0x68 and duration+0x6C become instance state. While already active, duration selection uses remaining=oldDuration-elapsed and the signed `InertiaBlend / OverrideMode` setting at `0x143bfddf0`: negative selects min(remaining,new), zero selects new, positive selects max(remaining,new). Enable, reset and LOD gates prevent treating every request as guaranteed smoothing.

### Duration override setting

Initializer `0x1400a01b0` supplies group `InertiaBlend`, key `OverrideMode` and explicit default integer 0 to constructor `0x141197f50`. The current value is configuration object `0x143bfddc0`+0x30; default is +0x3c. Thus the initialized default replaces the remaining duration with the newly requested duration. With remaining=.4 and new=.6, negative/zero/positive modes yield .4/.6/.6; with new=.2 they yield .2/.2/.4.

Registration `0x140757544` looks for an existing group/member override through `0x1407577e0`. A successful text lookup dispatches to `0x1405a815c`, whose signed 32-bit parser reaches setter `0x1405a82f0` only on success. That setter writes current+0x30 and notifies only on a changed final value. This registration leaves its optional numeric clamp disabled. Typed input and reset paths reach the same setter; reset supplies default+0x3c.

The initializer establishes a default, not the effective value in a running session. Record the signed value at module-relative RVA 0x3bfddf0 when the request is consumed, along with remaining/new durations and gates, if the selected branch matters. The trace does not establish a configuration filename, file precedence or accepted INI syntax; do not invent an editing recipe from the group/key strings.

Evaluation obtains the current input pose, handles the Trajectory stage below, normalizes dense quaternions and ensures two history records exist. A pending request resets elapsed to0, marks active and initializes correction state through `0x140a019cc`. In the active branch it then adds the stored current increment to elapsed, applies `0x140a021fc` while elapsed<duration, otherwise clears active. A new correction is therefore first sampled after one stored update increment on this branch, not necessarily at t=0. This is local execution order, not a universal scheduler claim.

History save `0x14060ec78` alternates two saved-pose slots and saturates the history count at2. The main path saves after correction and before final Trajectory restoration. H1 is the latest saved pose (`0x14060ecfc`), H2 the other (`0x140a021cc`). This is temporal smoothing of retained evaluated poses, not an ordinary source-target crossfade.

## Correction construction and decay

Let P be current input in this operator's working domain. Translation initialization uses:

```text
u = normalize(H1.t-P.t)
x = length(H1.t-P.t)
b = dot(H2.t-P.t, u)
v = (x-b)/previousStoredIncrement
```

Near-zero x produces zero direction/offset; a separate small-vector threshold can zero b. This is projection onto the present correction direction, not three independent velocity components. Float-track offsets use x=H1.track-P.track and b=H2.track-P.track with the same derivative, subject to the exclusions below.

Rotation initialization at `0x140a01e4d..0x140a01edb` constructs Q1=H1.q*conjugate(P.q), Q2=H2.q*conjugate(P.q). Axis is normalize(Q1.xyz), negated when Q1.w<0. Current scalar angle is2*acos(abs(Q1.w)); preceding scalar is2*atan(dot(Q2.xyz,axis)/Q2.w), with nonfinite preceding output replaced by0. Near-equivalent checks and small thresholds also apply. Do not reverse quaternion operands or replace the projected preceding angle with an independently measured angular speed.

Derivative helper `0x140a021a4` returns0 in safeMode when v*x>=0 for finite values. Duration helper `0x140a02544` starts from requested T and, in safeMode with abs(v)>=float32(1e-6), selects min(T,-5*x/v). Application is gated by elapsed below that per-channel duration.

The scalar correction uses `0x140a02584`, a quintic:

```text
a = (-8*v*T - 20*x)/(T*T)
if safeMode and a*x <= 0: a = 0
A = -(6*v*T + a*T*T + 12*x)/(2*T^5)
B =  (16*v*T + 3*a*T*T + 30*x)/(2*T^4)
C = -(12*v*T + 3*a*T*T + 20*x)/(2*T^3)
y(t) = ((((A*t+B)*t+C)*t+a/2)*t+v)*t+x
```

This is explanatory finite, nonsingular algebra, not a promise of bit-identical float32 grouping. Exact-arithmetic endpoint constraints are y(0)=x,y′(0)=v,y(T)=y′(T)=y″(T)=0. With x=1,v=0,T=1,safeMode, y(.25)=459/512=.896484375; linear decay would give .75. Zero duration, zero previous increment, NaNs and later constraints are not covered by this idealized equation.

Application adds y*u to translation, constructs an axis-angle quaternion from half the scalar angle and applies **correction*currentRotation** at `0x140a02405..0x140a02436`, and adds scalar track corrections. Hamilton helper `0x14032afc0` fixes the operand order. The inner application body does not write scale, but the surrounding Trajectory stage can affect scale; do not generalize the inner observation to the whole node.

## Reset, zero-time and nonfinite branches

Reset leaf `0x140bb7378` explicitly zeros history selector/count, previous/current
increments, elapsed, active/pending, duration and remembered-enable state.
Activation calls it; selected reset/enable/distance branches also call it. A reset
does not universally return before handling the current update's new request.
For finite distance d, the inspected update/eval admission is
`not(d>=40 and unsignedCategory>=2) and not(specialDistanceFlag and d>=15)`.
These are distance/category gates, not checks for positive time or duration.

With history count0, update sets both stored increments from its incoming dt;
otherwise it shifts old current to previous. No local zero guard intervenes.
Evaluation fills two history poses and can process the pending request in the
same call. Derivative initialization runs **before** elapsed/duration termination.
Helper `0x140a021a4` divides `(x-b)/previousDt` before applying safeMode. Its ordered
`v*x>=0` test zeros v; negative or unordered products retain it.

An authored duration0 and true inertia-request Boolean can reach a request with
duration0 when the accumulated request duration is0. That is distinct from
actually applying the quintic:

| Selected state | Initialization | Application |
| --- | --- | --- |
| T=0, finite nonnegative elapsed | runs | outer ordered elapsed>=T excludes |
| T>0, previousDt=0, 0<=elapsed<T | runs; included x=b=0 can yield NaN velocity | admitted; safeMode does not reject NaN v |
| Finite elapsed, T=NaN, or elapsed=NaN | may already have run | unordered termination comparison admits |

The per-channel application repeats ordered elapsed>=channelT. For finite
nonnegative elapsed this excludes zero/negative channel durations too. Therefore
T0 alone does not prove a divide inside the quintic, although the derivative
division already occurred. NaN velocity skips the safeMode duration-shortening
test; finite x=1,v=-Inf instead produces a +0 duration candidate and is skipped
at nonnegative elapsed. MINSS uses storedT as its second operand; preserve its
source-sensitive NaN behavior rather than a language's generic min/max rule.

Local offset/angle thresholds and excluded tracks sanitize some correction
fields, not all source poses or velocities. The quintic contains no universal
finite/positive-T check. Its safeMode acceleration test retains a only when a*x
is ordered-positive; an unordered product resets a to0. This differs from using
the finite-only `a*x<=0` formula above on NaNs, and still leaves NaN velocity
terms in the polynomial. These unordered/division conclusions assume masked SIMD
exceptions; an unmasked exception may trap earlier. Live MXCSR is unobserved.
They are implementation counterexamples to universal safeMode guarantees, not
an observed fault or a diagnosis of Saber's deformation.

The normal QPC driver excludes raw dt0 and clamps finite global scale positive.
Puppet's curve-driven factor above is a separate, asset-conditioned producer;
actual flags, factor/curve values and transferred history are required before
asserting which solver boundary occurs. Do not turn a locally admitted input
into a claim that the default frame clock produces it. Retained provenance:
`transitions-deep/inertia-degenerate-findings.md`, exact reset/cold bodies and
branch/IEEE discriminator checks, with independent retained-code review.

## Conditional foot-track exclusions

Native CName initializers `0x1426e2598..0x1426e2773` and their literal strings identify `footSnapIkEnabled` as the selector. At `0x140a02057..0x140a020b8`, if its track index is in range and its current finite magnitude is at least float32(1e-6), the node resolves six names:

| Excluded correction track | Native CName storage |
|---|---|
|leftFootPhase|0x143bfce58|
|rightFootPhase|0x143bfce60|
|footPlantOffsetFoot|0x143bfce68|
|footPlantOffsetX|0x143bfce70|
|footPlantOffsetY|0x143bfce78|
|footPlantOffsetZ|0x143bfce80|

Matching indices receive zero stored correction offset and velocity (`0x140a020e4..0x140a02165`). Their current input values remain intact. Missing names do not become valid indices. Thus “all float tracks are smoothed” and “excluded tracks are zeroed” are both incorrect descriptions.

## Trajectory extraction and restoration

Initialization `0x140bb7333..0x140bb734f` resolves hash `0x890372f036e9bef8`, matching FNV1a64(`Trajectory`), and stores its signed16 index through node runtime-offset+0x1E8. It is not assumed to be bone0.

For a valid selected transform R, `0x14060ed2c` saves R and constructs the following inverse-like transform through `0x140326e80`:

```text
A.t = rotate(conjugate(R.q), -R.t)
A.q = conjugate(R.q)
A.s = 1/R.s
```

For unit quaternions, finite nonzero scales and the same QS representation, composition helper `0x14032911c` is:

```text
C(X,Y).t = X.t + rotate(X.q, X.s * Y.t)
C(X,Y).q = X.q * Y.q
C(X,Y).s = X.s * Y.s
```

Extraction applies C(A,T_i) to each transform with graph-rig-view parentIndex[i]==0, then sets selected Trajectory to identity. The parent test is neither a name test nor recursive traversal. Its identity is traced: node eval context+0x40 points to a rig-view wrapper, and `0x1401b5a44` copies raw animRig.parentIndices(+0x40) to wrapper+0x28. Builder `0x1401b5e08` also resolves appended virtual-transform parents.

After inertia correction and history save, tolerant identity test `0x14060ef0c` checks saved R. If not near identity, `0x14060cd88` applies C(R,T_i) to the same parentIndex==0 entries. Consequently stored history is in the extracted domain in this admitted branch, while the returned pose has restoration applied.

Do not substitute a general inverse for A. It visibly omits reciprocal scale in A.t. With identity rotations, R.t=10,R.s=2 and child.t=14, extraction gives -3 and restoration gives4. Unit scale round-trips14. This is a useful arithmetic discriminator for an offline transcription; it is not a demonstrated Saber failure cause or evidence that those scale values occur in gameplay.

## Rotation limits: degrees and component order

After corrections, each valid rotation-limit entry uses quaternion→angles `0x1403b1a88`, scalar clamp `0x140a02808`, and angles→quaternion `0x1403b1950`. The finite clamp is min(max(value,lower),upper) when enabled, otherwise unchanged.

Constants float32(pi/360) at `0x1437b9910` and float32(180/pi) at `0x1437ba198` establish degree storage. For stored(a,b,c), forward quaternion reconstruction is **Qz(c)*Qx(b)*Qy(a)** followed by normalization. Generated EulerAngles labels are Roll(+0),Pitch(+4),Yaw(+8), giving these concrete mappings:

| Configuration | Stored Euler channel | Mathematical axis |
|---|---|---|
|limitOnX(+0x18)|Pitch(+4)|X|
|limitOnY(+0x24)|Roll(+0)|Y|
|limitOnZ(+0x30)|Yaw(+8)|Z|

For a unit quaternion(x,y,z,w) away from poles, inverse arithmetic is:

```text
a = degrees(atan2(2*(w*y-x*z), 1-2*(y*y+x*x)))
b = degrees(asin(2*(y*z+w*x)/normSquared))
c = degrees(atan2(2*(w*z-x*y), 1-2*(z*z+x*x)))
```

At test=y*z+w*x greater than float32(.499)*normSquared, it selects(a,b,c)=(0,90,2*degrees(atan2(y,w))); below the negative threshold it selects(0,-90,-2*degrees(atan2(y,w))). These are explicit pole conventions, not globally unique coordinates. Native asin's error string confirms `asinf`; the two-argument helper has atan2's signed-quadrant/range-reduction structure. CPU-specific sin/cos kernels and bit-exact CRT rounding were not reimplemented.

The later [native inverse-Euler measurement](native-transform-numerics.md#inverse-euler-poles-and-float32-boundary-changes)
executes this inverse and its actual atan2/asin dependencies. It measures
float32 boundary alternation and pole reconstruction loss, while keeping the
native forward conversion and constraint application unexecuted. Use its rounded
branch contract when reproducing a selected input; a continuous double inverse
does not preserve these pole decisions.

Post-correction clamping and Trajectory restoration mean quintic endpoint constraints alone do not prove the final returned bone follows those constraints.

## Verification boundaries and use

The retained bounded checks passed512 exact-rational quintic endpoint cases,8,208 finite signed atan transcription cases,125 nonsingular Euler composition/inverse cases, quaternion-order and single-axis discriminators, seven native CName hashes, entity-clock examples and the nonunit-scale counterexample. These exercise analyst equations in Python, not the native executable. A first atan transcription failed because two constants were swapped; the failed script/receipt were preserved and the constant mapping corrected before the successful run. No test assertion was weakened.

Use these results to choose meaningful offline fixtures: entity dilation, previous/current increment differences, requested duration during active smoothing, nonzero foot-snap tracks, noncommuting rotations, Euler clamps, Trajectory extraction and nonunit scale. Preserve zero-duration/history-increment and nonfinite cases as explicit branches, not silently repaired math.

Still distinct from this implementation proof: shipping behavior of reflected graph pause/time fields; other entity overrides; effective live duration-mode/request/flag values; runtime scheduler cadence; bit-exact CRT kernels; actual model inputs and visual/gameplay acceptance. The named CPU skinning preparation path is documented separately in [native skinning](native-skinning.md). A Blender pose or passing algebra fixture does not close runtime questions.
