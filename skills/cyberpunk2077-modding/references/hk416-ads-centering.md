# Weapon neutral alignment, camera-relative motion and reload variants

**Rejected runtime iteration:** the user reported equip-triggered displacement,
hand/sight regression and nonworking ADS reloads for this ADS beta (ZIP SHA-256
`26c1270b8bf2809c78ed8875ab144d835b2c8f5ebc7aac6a0cfa8c8f683d15b1`).
Its commands and conclusions below are historical experiments, not an accepted
recipe. The [recovery contract](hk416-recovery-contract.md) corrects demonstrated
parent-space/control errors and records the remaining runtime uncertainty.

Local HK416 evidence, 2026-10-25. Continue the [rest/scope inspection](hk416-rest-scope-inspection.md),
[weapon workflow](weapon-rigging-animation.md) and [native authoring](native-animation-authoring.md).
This is offline/native/compiler evidence; the new reload routing awaits gameplay.
The user called the preceding Ready port solid, which is evidence for that package.

## Diagnose the physical baseline

Trace the reticle implementation before changing HUD or pose. The inspected ReArmament
code projects `muzzleOrigin + muzzleForward * 500`; the native attachment chain is
`WeaponRight → barrel_slot → fx_muzzle`, with local Y forward. The ready attachment
produced 0.571° yaw / 0.788° pitch relative to the camera-forward baseline. Correcting
the weapon/hand assembly locally, re-solving arm rotations and retaining joint offsets
centered the exported ready direction. Equip and idle-adjustment endpoints must receive
the same correction; check neutral return after every action, not just a static pose.
Retain breathing, recoil, low ready and ADS. FOV changes projection/visibility, not this
joint-space cause; no FOV or HUD change was needed.

For locomotion, compare source camera, arms and weapon in the same space. Recovered
RoN run/walk rotate `fp_camera` by about 0.666°/0.795°. A fixed target camera needs
`sourceAnchorCamera * inverse(sourceAnimatedCamera)` composed with the existing
source-to-target adapter. Apply it to the weapon and hand goals together, preserve
limb lengths, rebuild additive deltas against the corrected base, then check fractional
blends and loop closure. This removes a demonstrated omitted transform; it does not
prove the runtime blend graph is reproduced. Do not relabel a run clip as sprint.
The HK416 retains its official Cyberpunk rifle sprint fallback.

## Inventory timelines and synchronize selection

Inspect montage `body.timeline` as well as direct `body.clip`. Names suggesting ADS
are insufficient: this source build's ADS speed and ADS empty entries alias their hip
montages. Tactical ADS has a distinct body animation. Its metadata lacks a separate
weapon montage, so the established tactical component motion is paired explicitly.

Installed MCX Spear sets `mwPortAdsReloadProfile: 3`; Weapon Core uses private graph
inputs, per-variant clocks, aim gating and component dispatch. FAMAS and revolver
implementations illustrate that this is graph-dependent. Do not add that author Core
when the target's existing official graphs already provide the required selectors.
The HK416 candidate uses native `RandomSync` slots 0/1/2 in player/receiver/magazine
sets, selected before the Reload event. `base1` has no partial reload tracks and stays
static. A small exact-item script retains native StartReload, ammo/cancel handling,
stat speed scaling and normal/forced cleanup. Aim interruption is suppressed only
for ADS tactical. This compiled with essential frameworks and 1,933 copied enabled
profile scripts; runtime aim retention and wrapper interactions remain unverified.

| Selection | Source length | Source ReloadComplete |
| --- | ---: | ---: |
| Empty, including starting in ADS | 2.0000 s | 1.9171 s |
| Hip partial outside combat: tactical | 2.6667 s | 2.5627 s |
| Hip partial in combat: fast | 1.5667 s | 1.4921 s |
| ADS partial: ADS tactical | 2.6667 s | 2.5463 s |

The combat fast rule is this user's choice, not a universal mapping. Snapshot route
at entry; do not switch clips mid-reload. Verify timestamps against animation speed,
magazine visibility, audio events, ammo commitment, interruption and return-to-aim.

## Export failures that became regression checks

- Native import rejected the glTF exchange-parent `Armature` on weapon components.
  Use only original native animation target nodes; do not guess a rig binding.
- Static inherited arm channels kept the old 2.667-second duration around a new
  1.567-second fast clip. Compilation and numeric authored/native equality did not
  catch the authoring mistake. Rescale only proven-constant retained channels;
  assert final duration against source and independently compare all component clocks.
- Do not silently loosen precision claims: a strict 0.01 mm baseline comparison
  failed at the resampled hand adjustment. Maximum measured joint/contact changes
  were 0.0404/0.0934 mm. Native transport passed separately (max numeric error 6.12e-7).
  Report these as bounded resampling differences, not exact channel preservation.
- If rerendering only a changed clip, certify other decoded channels, times, extras
  and skeleton nodes as identical. Keep the old render receipts and original input
  hashes plus an explicit equivalence report; never rewrite their provenance.

## Existing local project commands

These are project helpers, not a universal converter. They require the local recovered
source manifest, source poses, private meshes, prior Ready readback, Neto transfer,
Blender 5.2.3, Node, the established .NET SDK and WolvenKit 9.0.1 adapter. No assets
are distributed with the skill. Use `$CP2077_DEV` for the existing checkout.

```sh
cd "$CP2077_DEV"
blender -b -t 2 --python tools/ron_ads_motion.py
node --max-old-space-size=12288 tools/ron_ads_author.mjs
bash tools/ron_ads_native.sh
node mods/ron-hk416-ads/work/check-clock.mjs
blender -b -t 2 --python mods/ron-hk416-ads/work/audit-native.py
bash mods/ron-hk416-ads/work/render.sh pwa
bash mods/ron-hk416-ads/work/render.sh pma
bash mods/ron-hk416-ads/work/render-details.sh
python mods/ron-hk416-ads/work/compile_scripts.py dependencies-only --suffix review
python mods/ron-hk416-ads/work/compile_scripts.py profile --suffix review
python tools/package_ron_hk416_ads.py check
python tools/package_ron_hk416_ads.py pack
```

Outputs refuse overwriting. Preserve attempts; use a fresh suffix/output when appropriate.
Read the project's `work/commands.md`, manifests and `REPORT.md` for executed attempts,
actual view/frame coverage and unresolved issues. Generating sheets does not establish
visual inspection. The complete source/preview/export gates in the linked workflow
still apply. Native muscle/IK, current live VTK deformation, ADS jog fallback, shot
alignment, cancellation, sound mixing and actual reload selection need gameplay.
