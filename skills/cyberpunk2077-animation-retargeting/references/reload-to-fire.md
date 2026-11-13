# Mandatory reload-to-fire integration for weapon ports

Every weapon port must demonstrate responsive reload-to-fire behavior before
claiming the port complete. Both tactical and empty hip reloads must permit firing
as soon as the support hand and mechanism reach the measured fire-ready pose, with
a smooth transition into actual firing once ammo and normal shot eligibility also permit it.
Correct behavior already meeting this gate needs no script changes. Applicable body variants and supported
speed modifiers belong in the coverage record. User-deferred routes stay explicitly
OPEN; this rule does not silently expand an ADS task or authorize installation.

## Trace the installed behavior before adapting it

1. Identify the effective mod profile, winning script/tweak/archive paths and hashes.
   Inspect the working reference weapon and responsiveness mod (for example ARR /
   Hyper-FPS), plus reload frameworks and staged-reload/dual-wield overrides, if present.
   For standalone ports, trace the existing vanilla/custom implementation instead.
   Do not add ARR, WWCM, CET or a staged framework just to satisfy this gate.
2. Trace reload entry, ammo commit, update, ExitCondition, ToFullAuto/ToSemiAuto,
   shot eligibility and cleanup. Distinguish ammo insertion, hand return, full clip
   duration and firing eligibility; they are not the same clock or event.
3. Verify the effective compiled wrapper/replacement chain when mods share these
   methods. Source annotations and compile success do not prove which body wins.
   Use REA with the existing redscript decompiler for this compiled-artifact question;
   ordinary source inspection needs no native-binary detour. Record cache identity,
   recovered methods and decompiler errors. Do not claim full recovery from a partial
   decompile or runtime execution from static call-chain evidence.
4. Reuse the reference implementation's actual commit latch, held-fire exit and
   shot checks at the port's narrow integration point. Do not copy the whole mod,
   add global replacements, or hardcode another weapon's name, time or wrapper ID.
   If a framework bypasses its entry initialization or another mod replaces its
   exit branch, restore the missing behavior for the intended weapon/route only.

For the MP5, ARR observed magazine ammo increasing, latched the commit, waited its
configured short delay, then allowed held-fire exit and normal shot eligibility.
WWCM could bypass ARR's OnEnter, and Expanded Dual Wielding replaced ARR's
ExitCondition. Fixing only the animation gate could not restore that removed branch.
Preserve other weapons, left-hand behavior and framework cleanup; inspect current
sources because mod names and historical wrapper numbers do not prove current order.

Unsupported staged-reload or speed-modifier routes are N/A, not a reason to add a
dependency; record which supported routes were actually checked.

## Gate by measured motion without introducing another delay

Measure fireReady independently for each reload from the final native motion and
mechanisms: the hand is back in position and a firing blend is visually safe. Do not
use magazine insertion alone. Keep ammo commit and source duration intact unless a
separate measured change requires editing them. For staged reloads, map checkpoint
seek and playback speed onto the same source position used by this readiness gate.

Before readiness, compute the remaining time consistently with the consumer's clock.
Once source position reaches fireReady, latch the gate open for that reload session
(or use a fixed deadline that stays passed). Never keep assigning an advancing
elapsed time to the deadline after readiness: a different decision clock can remain
behind it indefinitely. Reset per-session state on exit, forced exit, weapon switch
and detach; preserve the existing staged-reload restoration and shot checks.

CET cannot necessarily read protected redscript fields: nil does not prove the
engine failed to initialize them. Verify access against runtime data. When needed,
use narrow typed public getters and update every Lua caller. Log early-return causes
and caught errors. Test with protected fields inaccessible, not permissive mocks.
A framework's managed-reload boolean may also be true during hip fire; classify
hip versus ADS from the actual aim state, not that boolean alone.

## Required evidence before completion

- Inspect continuous actual reload-to-fire motion for both reloads, including the
  firing/recoil destination and blend, in first-person and a useful complementary
  view. A countdown, ready label, isolated endpoint or reload-only video is not proof.
  Label offline reconstructions; they do not establish live graph selection.
- Compile against the effective profile, and check both modes, supported speeds,
  staged resume, gate remaining open after readiness, route exclusions and unchanged
  weapons. A test must reject the demonstrated failure, not merely parse the script.
- Capture module/build identity, callback entry and rejection/error reasons, reload
  mode/source position/seek, state time and gate, ammo-commit active/seen/elapsed,
  firing input and relevant exit/shot decisions. Reading status must not alter them.
  Confirm callbacks actually run; then distinguish a closed gate, missing commit,
  overwritten exit, shot restriction and graph/visibility failure.
- Bind preview, package and installed script hashes to the authorized test. Hold fire
  before hand return during tactical and empty hip reloads, then test a fresh press
  after return and supported interruptions. Verify the actual shot and smooth motion
  in game; log presence or compiler success is insufficient. When access is missing,
  leave this gate OPEN with the precise remaining test rather than claiming completion.

Reuse unchanged accepted motion evidence for script-only corrections; do not reauthor
poses or demand redundant preview approval. Use existing installation authorization
and the user's manager workflow. A game relaunch may be required to load redscript;
a mod-manager restart is not automatically required.

## MP5 result and limits

On 2026-11-13, the user confirmed “You fixed it” after testing the v4 MP5 integration.
The preceding v3 trace showed both reloads running to full duration with no adapter
errors, so successful callback execution alone was demonstrably insufficient.
The accepted v4 restored ARR's committed + held-fire exit for MP5 hip reloads and
opened the hand-return gate permanently after readiness. It retained accepted native
animations and added gate/commit/input diagnostics. These interventions were tested
together: do not claim an isolated runtime attribution to either one.

Private project evidence: `work/reload-qol-20261113/fire-exit-fix/FINDINGS.md`,
`installation-receipt.json`, `rea-evidence.json`, and `runtime-acceptance.json`.
REA records `ev_276508879bbf82f89d8fb9092c6fd845c7ba82ec1fb31b7a87e58bb474716614`
and `ev_afbf763c46032ed7fed8815855fd99340718953ea535a9c54ea356c4409f2974`
cover live-cache and candidate decompilation, not game execution. Both had four
reported definition errors; inspected reload decision methods were recovered.
The confirmed scope is the user's two hip reload tests. ADS reload, every body,
all speed modifiers and all staged-interruption combinations are not implied.
