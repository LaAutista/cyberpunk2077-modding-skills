# Failure ledger and loop breaker

These are bounded lessons from the existing [evidence register](../../cyberpunk2077-modding/references/animation-retargeting/evidence-register.md)
and the user's refactoring brief. They are not newly reproduced game results.
Rows without a linked local reproduction remain proposed discriminators.

| Failure / symptom | Invariant and smallest discriminator |
| --- | --- |
| Old-parent reconstruction / native constraint misalignment | Rebuild parent-first with `L = inverse(W_updated_destination_parent) * W_desired_child`. Change a nonidentity parent with noncommuting child rotation; compare world reconstruction before/after controls. [Recovery](../../cyberpunk2077-modding/references/hk416-recovery-contract.md). |
| Doubled additive base / wrong stance or rotation | Declare source and target bases/orders independently; strip bind once. Compare noncommuting rotation plus nonunit scale against an independently composed desired pose. [Native semantics](cyberpunk-animation-semantics.md). |
| Missing additive scale default / collapse or enlargement | Determine what an absent scale channel means for this codec/type; compare a missing-channel fixture and explicit nonunit base. Do not inject an absolute unit default. [Source extraction](../../cyberpunk2077-modding/references/ron-source-extraction.md). |
| Removed hold/endpoint keys / premature magazine motion | Preserve authored holds and actual endpoints. Compare just before/at/after the retained key against native source time. [Source extraction](../../cyberpunk2077-modding/references/ron-source-extraction.md). |
| Wrong FPS / matching header but shifted mechanisms | Compare key times in seconds and native frame ticks, not header FPS. M1911's rejected reload is a bounded example. [Source adapters](source-adapters.md). |
| Incomplete skeleton / missing motion or terminal deformation | Recover full motion hierarchy and weighted helper influences; compare a terminal-helper pose with source-native skin. Counts from HK416 are not universal. [Source playback](../../cyberpunk2077-modding/references/animation-retargeting/source-playback-adapters.md). |
| Control rest mixed with inverse binds / misleading pose agreement | Separate native control locals from each mesh's skin bind; hold motion fixed and vary only the representation. [Spaces/bind](../../cyberpunk2077-modding/references/animation-retargeting/spaces-bind.md). |
| Static arm roll / correct endpoint but twisted wrist or elbow | Compare source-guided pole/axial orientation at reach extremes and between keys without changing lengths. [Contact](contact-and-ik.md). |
| Locked grip through manipulation / one phase improves, another breaks | Establish extraction/hold/reinsertion ownership independently; measure three phase contact frames and transition clearance before interpolation. [Contact phases](../../cyberpunk2077-modding/references/animation-retargeting/proportions-contact.md). |
| Nearest-parent helper substitution / bind pass, posed surface fail | Preserve actual helper ownership and weights; use a fixed animation with independent posed-surface comparison. [Native deformation](../../cyberpunk2077-modding/references/animation-retargeting/native-deformation.md). |
| Linearized nonlinear helpers / endpoints pass, intermediate fold | Sample between noncommuting keys and compare the native helper formula against the approximation. [Native deformation](../../cyberpunk2077-modding/references/animation-retargeting/native-deformation.md). |
| Tiny-quaternion snapping / small rotation disappears | Read stored XYZ/W independently for float32 W==1, XYZ!=0, both raw and constant keys. [Native authoring](../../cyberpunk2077-modding/references/native-animation-authoring.md). |
| SIMD resampling / dropped source cadence | Compare stored native key times to the unprepared source expectation; raw keyed output has a separate contract. [Native readback](native-readback.md). |
| Filename-inferred semantics / plausible but wrong composition | Query actual animation/base/container metadata and evaluate a source pose; a name is not evidence. [Source adapters](source-adapters.md). |
| Stale preview/controller arrays / clean preview, wrong export | Bind final arrays/native readback to the current candidate hash; compare controllers after parent/FK updates. [Recovery](../../cyberpunk2077-modding/references/hk416-recovery-contract.md). |
| Mixed source hold/native transition / sprint start-stop snaps | Compare exact final native endpoints and partial blends on both body variants; include downstream wrist/weapon controls and retained additive bases. Isolated clip checks missed RPG7's115mm/46degree sprint boundary mismatch. [BF6 transitions](bf6-workflow.md#reconcile-authored-arms-controls-and-transitions). |
| Donor shoulder retained / valid lengths but over-folded arm | Compare source-mapped clavicle/upper-arm location, elbow inner angle and forearm/palm direction with skin, not reach alone. Keep hand/weapon contact fixed in the discriminator; reject shoulder/wrist damage or new adjoining-state jumps. [BF6 posture](bf6-workflow.md#reconcile-authored-arms-controls-and-transitions). |
| Package success called gameplay success | Extract and hash shipped bytes, then obtain identified runtime observation. Until then runtime is OPEN. [Runtime](runtime-validation.md). |

The [BF6 MP5 success case](bf6-mp5-success.md) adds these demonstrated controls:

| Failure / symptom | Invariant and smallest discriminator |
| --- | --- |
| Wrist/elbow match but the rest grip snaps | Compare both arm chains, every digit and evaluated skin across the boundary; retain the original visible jump as a negative control. |
| Corrected Normal base plus old additive offsets | Compose old/new bases and re-encoded offsets at full and partial weights; preserve evaluated contact, not stale encoded translations. |
| Native key multiset passes but equip breaks in game | Audit actual dynamic record order separately from per-channel values; reject the channel-major stream and accept canonical original/fixed controls. [Native gate](native-readback.md#compressed-native-record-order). |
| Better collision totals but worse shape or seated alignment | Keep phase ownership, anatomical shape, self-clearance and actual skin/prop penetration separate; verify constant mount offsets before moving the prop. |
| Comparison camera follows an edited digit | Reuse an unchanged reference camera/anchor and clock; compare framing before interpreting the images. |

After two failed corrections at the same gate, write this in the owning project:

```text
# FAILURE
Gate/question; baseline, fixture and candidate paths/hashes:
Observed failure: time/view/bone/component and measured or visible discrepancy:
Attempt 1: hypothesis, change, exact command, result, evidence path/hash:
Attempt 2: hypothesis, change, exact command, result, evidence path/hash:
Why existing validation missed it:
Reusable prevention change and affected helper/reference:
Regression: original failing fixture, expected rejection, corrected control, actual result:
Remaining hypothesis A:
Remaining hypothesis B:
Discriminator: smallest test with distinct predicted observations for A and B:
Result: OPEN until run; then actual observation and evidence path/hash:
Next permitted correction: only after the discriminator has a result:
```

Changing a file name, a nearby offset or the prose explanation does not restart the
budget. Do not destroy failures when a later narrow result passes. If the required
environment is unavailable, report exact manual steps and expected observations;
continue independent tasks only, with the blocking gate visibly OPEN/FAILED.

Treat a significant missed inspection as a validation defect even when technical
checks passed. Identify the limited invariant those checks actually exercised;
record the missing visual/channel/geometry coverage rather than weakening their
thresholds. A prevention change is complete only when its regression catches the
old failure (or is explicitly unrun), with a legitimate control to avoid an
always-failing check. Use the existing project evidence and workflow evals. Keep
real-asset, synthetic, visual and runtime results separate.
