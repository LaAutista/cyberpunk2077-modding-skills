# Evidence register and reproduction entry points

Snapshot: **2026-10-26**. This hub was synthesized by reading existing reports,
receipts, source text and checkpoints. Documentation validation did not rerun the
ports, native exporters, graph/shader runtime, GUI, VM, renders or game. Read the
fresh owning-project checkpoint before resuming; retain the exact receipt/hash
when later work supersedes a result. Do not replace a failed report with its summary.
M1911's general STATUS/README retain historical blocked sections; prefer the
candidate-specific raw receipts and certificate pinned under M1–M4 below over an
older prose status or a candidate directory name.

## Local roots

These are local project locations expressed through the user's home, not shipped
fixtures. Resolve them in this environment; another machine needs an explicit map.
Raw assets, third-party code and rendered game frames are not included in this hub.

```sh
CP2077_DEV="${HOME}/Documents/VibeCoding/CP2077Dev"
HALO_BR="${HOME}/Documents/Codex/2026-10-25/task-12/halo-br"
HALO_V4="$HALO_BR/work/deformation-validation-20261026"
M1911="${HOME}/Documents/Codex/2026-10-25/task-9/mods/m1911-beta"
MAX_EXPORT="$M1911/work/max-export-20261026"
M1911_TOOLS="${HOME}/Documents/Codex/2026-10-25/task-9/tools"
```

Use project copies and their hashes. Bingle archive/source is under
`$HALO_V4/bingle-reference`; FO4 extracted rig/readme/configs are under
`$HALO_BR/work/fo4-rig-reference-20261026/extracted`. The owner's completed
`$HALO_BR/source-inputs/preserved-downloads-20261026/manifest.json` verifies
RONRig, Shiagur ZIP, Haru extracted Data, Bingle and named MAX/NIF references.
Use its `projectCopy` paths relative to HALO_BR; historical Downloads paths are
acquisition provenance only. RON rig is now
`source-inputs/preserved-downloads-20261026/RONRig/ReadyOrNot_FPrig.blend`, SHA-256
`82bb07215c716ae07a1b27bc535513e9bf6081e68b03ab6a9ef73f0aeba9a7b0`.
Haru Main.ba2 uses the existing project copy under
`work/halo-animation-repository-20261026/fo4-br55-candidate/data`.
The missing original Haru 7z is not claimed preserved; its extracted three-file
Data set is retained. This named-input receipt does not clear unrelated Downloads
for deletion. M1911 source archive/scenes and Nif dependency artifact also have
their own project copies. Do not duplicate these inputs during hub maintenance.

## Halo and native deformation

### Active ownership and source choice

Latest directed ownership on 2026-10-26: **CP rig repair has a separate owner**
(thread prefix `01a17a31`, supplied by the coordinating parent). Halo owns source
preservation, Haru/NovaFinch FO4 BR55 HKX/native playback and the BR port, with
original HCE model/textures retained. Reach DMR is fallback; the original HCE
animation investigation is paused. CP rig/evaluator/shared-QA writes from Halo
are frozen. **Architecture clarification from Joseph, 2026-10-27:** that separate
human-facing animator/control rig is optional; its completion or accepted interface
is not a blanket prerequisite for a direct raw/native-skeleton port. The older
handoff's interface requirement applies when choosing that deliverable, not all
retarget paths. The preserved V4 diagnostic is not a complete accepted skin.
Only a demonstrated shared native-component defect used by a particular path
justifies blocking that path on shared rig repair; retain the exact failing
component/revision/dependency and let independent routes proceed. Native skeleton,
rest/binds, skin/required helpers and exporter checks, plus the universal visual
and later runtime gates, remain required for the selected route. See the
[direct-skeleton architecture](spaces-bind.md#native-skeleton-versus-animator-controls).

Authority: `$HALO_BR/work/halo-animation-repository-20261026/CP-RIG-HANDOFF.md`
and adjacent `CP-RIG-HANDOFF.json`. Current BR55 source and reader findings are in
`fo4-br55-candidate/REPORT.md` and `fo4-hkx-reader-review/REPORT.md` under that
workspace. Header/binding/event inspection is bounded evidence; full motion
decode, source skin/contact and CP retarget are not established by those reports.
The canonical 94-bone first-person map, actual per-file clock, codec and raw
blend hint need explicit validation; not every FO4 file is 30 Hz. The old Unreal
source-grip failure remains a historical branch result, not Haru acceptance data.

**Max/M1911 work is paused by the coordinating parent's instruction.** Preserve
its latest certificate, failed reload-v1 and stopped session evidence; do not
replay a queue, open a scene or export from a documentation pass. The existing
`$MAX_EXPORT/session-bridge/LIVE-ATTEMPT-20261026.json` records a stopped session
with no native inspection/export executed by that attempt. Its suggested future
actions do not override the current pause. No local pause receipt was found;
the pause and dedicated rig thread prefix are coordination instructions, not
claims inferred from stale project STATUS prose.

| ID | Exact local evidence | Bounded conclusion |
| --- | --- | --- |
| H1 | `$HALO_V4/STATUS.md`; `CHECKPOINT.json`; `rig-v4/README.md`; `rig-v4/build-verification.json`; `reference-playback/README.md` | V4 diagnostic; overall rig rejected, source contact FAIL, retarget/release BLOCKED. 892 exported Native152 reference comparisons pass; no full deformation/runtime acceptance. |
| H2 | `$HALO_V4/native-skin-parity/REPORT.md`; `$HALO_BR/work/deformation-evaluator-20261026/v2/README.md`; `graph-dependencies/REPORT.md` under that evaluator root | Static native graph/shader evidence, Twist-sign correction, nonlinear interpolation failures and posed-normal limits. |
| H2 views | `$HALO_V4/visual-review/pma-v4-full.md`, `visual-review/pwa-v4-full.md`; `full-sequence/full-v4-source-slerp-cpu/manifest.json`; `root-policy-review/palm-crescent/REPORT.md`; `root-policy-review/V4_FINAL_REVIEW.md` | Actual sampled visual review and root/input guards; interior palm crescent and hidden surfaces remain unaccepted. |
| H2 context | `$HALO_V4/condition-semantics/REPORT.md`; `sparse-mapping/REPORT.md`; `native-skin-parity/cache-mapping/REPORT.md` | Native condition sign, mapping and explicit LOD fixture; no live actor/GPU dispatch proof. |
| H3 | `$HALO_BR/SOURCE_SKIN_AUDIT.md`; `OFFLINE_WORKFLOW_DELTA.md`; `evidence/evaluated-pose-input-contract.json` | Raw source skin/extraction pass does not fix open support fingers. All 77 inspected BoneTree translations use Animation mode. Exact missing evaluated-pose contract retained. |

Recorded hashes identify the inspected code, not currently loaded runtime bytes:

| File | SHA-256 |
| --- | --- |
| `$HALO_V4/rig-v4/live_playback_v4.py` | `03f3c03e5f80ce42e08feae7bddb9dad7fdda939fff8a7f4ebd9b54a3d1c8e95` |
| `$HALO_V4/reference-playback/reference_sampler.py` | `a7c738d73e1ba41eb39cc2a759a314bbf3ef54b687ca60a46de17f9124ef1b7c` |
| `$HALO_V4/native-skin-parity/native_skin_evaluator.py` | `00072b1dec85986f7c47586725d9576b760dce1d5800a458791f96eb12c65253` |

V4 uses recorded Blender 5.2.3. Its exported-reference sampler is not a claim about
the hidden game interpolation path. The editable quaternion component-curve route
and immutable GLB SLERP route are intentionally separate.

## RoN / HK416 and target serialization

| ID | Exact evidence | Bounded conclusion |
| --- | --- | --- |
| R1 | [Port workflow](../ron-port-workflow.md), [beta source findings](../ron-beta-source-audio.md); `$CP2077_DEV/mods/ron-hk416-beta/work/source-motion` | Source identity, paired montage/base/attachment recovery and bounded offline source checks; missing procedural/graph/physics context retained. |
| R2 | [Recovery contract](../hk416-recovery-contract.md); `$CP2077_DEV/mods/ron-hk416-recovery/work/native-audit/FINDINGS.md`, `graph-control-check.json`, `v2-final-checks.json`, `v2-expanded-checks.json` | Stale-parent and destination-space failures. Core 14-clip checks pass; expanded 22 bindings still have nine strict absolute failures/body at frames 94–100. Relative regression pass does not waive them. |
| R3 | [Rest/bind inspection](../hk416-rest-scope-inspection.md); `$CP2077_DEV/mods/ron-hk416-ready/work/refinement-20261025` | Corrected control-rest/per-mesh-bind handoff and temporal contact envelope; bounded interchange evidence, no runtime thumb repair. |
| R4 | [Portable adaptation contract](../../scripts/ron-adaptation/README.md); `$CP2077_DEV/mods/ron-hk416-beta/work/index-diagnosis/HANDOFF.md`; `work/target-contract/renderer-audit/REPORT.md` | Analytic source IK approximation, selected finger correction and exact component-clock/route checks; fine contact/native muscle/runtime gaps remain. |
| R5 | [Native authoring and commands](../native-animation-authoring.md); [additive preview](../../../weapon-animation-inspection/references/additive-preview.md) | Tested bounded serialization/readback semantics and synthetic regressions. A new weapon/container needs its own controls and native checks. |
| R6 | [Fixed-animation parent/weight controls](../fo4-scenario-comparison.md); `$CP2077_DEV/mods/ron-hk416-clean/work/forensics/failed-native-bind/README.md` | Wrong-parent, lost-influence and incomplete-bind failures; preservation guards, not finger-skin/runtime certification. |

Recorded source build: Ready or Not Steam **25784851**, executable **5.3.2.0**;
CUE4Parse commit `990d4d7d4e0340a75a14323436d55568f1415e00`.
Per-track codecs were exercised; ACL/AnimScaled support is unverified. Target
adapter evidence is WolvenKit **9.0.1**, .NET SDK **10.0.400**; match installed
versions before reusing commands. The official analyzed player graph hash is
`dff7c3bdef154b9f9ccf87bdca0faf3eac4565e4428714fb52d46f4c4f7d0eb3`.
Effective mod override selection remains a runtime question.

## MAX / M1911

| ID | Exact local evidence | Bounded conclusion |
| --- | --- | --- |
| M1 | `$M1911/work/evidence/input-manifest.json`, `animation-inventory.json`; `$MAX_EXPORT/max-host-audit.txt`, `idle-native-inspection.txt`, `reload-native-inspection.txt` | 112 scene names; Max 2021 / 23.0.0.915. Idle 30 fps 0–100; reload 60 fps 0–180. Inventory is not all-scene motion acceptance. |
| M2 | `$MAX_EXPORT/HELPER-BONE-RECOVERY.md`; `exports/idle-v4/export-readback.txt`, `certified-surface-bounds.json`, `source-fbx-parity-v2.json`, `bvh-independent-counterexamples.json` | Two weighted terminal helpers recovered without changing source samples. Separate 5.55 µm static surface certificate; raw sampled-BVH failures retained. Bind/contact/runtime false. |
| M3 | `$MAX_EXPORT/exports/reload-v1/source-fbx-parity-v1.json`, `raw-fbx-keytime-diagnostics.json`, `time-alignment-diagnostics.json`; `session-bridge/REVIEW.md`; `export-reload-reset.ms` | Reload-v1 30 Hz changing curves rejected despite 60 fps metadata; maximum magazine discrepancy 48.878 mm at frame 41. Prepared reset route is not an accepted later export. |
| M4 | `$M1911/work/target-research/mapping-plan.md`, `CP-TARGET-RETARGET-STRATEGY.md`, `weapon-chain/FINDINGS.md`; `$M1911/SOURCE-EXPORT-REQUEST.md` | Explicit source/target topology, clocks, mechanisms and requested annotation retention; source bind, anatomical correspondence and completed target retarget remain unverified. |

Source archive `1911_Anims.zip` SHA-256 is
`6bb45a74341618f8b6316040d621355ca1f20f2dced7a469c97ef75798d13ce5`;
durable original is under `$CP2077_DEV/Animation Bullshit/`, isolated scenes under
`$M1911/work/inputs/1911_Anims/`. The idle certificate's raw-report hash is
`26285562ccbf73367ce4d04e15e5df77d0d4d2f01ce3f2122d74b2ea53f623dc`.
FBX import comparison uses recorded Blender **5.2.3 LTS**, built-in importer,
FBX7400/2014. No new addon is required by these receipts.

## Guides and reference construction

| ID | Source and inspection record | Actual review boundary |
| --- | --- | --- |
| F1 | [Shiagur guide](https://docs.google.com/document/d/1wIyKkPsvuPtR6B2ODGnIHMcGkaCOEm04cq3yC86mY98/edit), [synthesis](shiagur-reference.md); [FO4 file listing](https://www.nexusmods.com/fallout4/mods/82537?tab=files); `$HALO_BR/work/fo4-rig-reference-20261026/COMPARISON.md`, `archive-inventory.json`, `blend-data-inventory.json` | Full guide 2.0 returned text read through Google Drive on 2026-10-26; earlier web-reader gap is superseded. Separately, Human Animation Rigs 2.8.3 readme/code and Blender 4.3-file data were inspected with scripts/depsgraph disabled in 5.2.3. No images/linked videos, addon execution, Havok viewer, pose/export/runtime pass from this guide review. |
| F2 | [Bingle-linked guide](https://docs.google.com/document/d/1ItDjPkd4NkFYa-Q42Jk7RII9DniKJ32LRbinyTDcxnQ/edit); `$HALO_V4/bingle-reference/REPORT.md`, `FO4-WEAPON-PORTS.md`, `annotations-review.md`, `annotations-review.json` | Complete guide, linked archive and actual retargeter/PyNifly source inspected. Original Arca unavailable; sample video not watched. HKX loader candidate never executed/validated. |
| F3 | `$HALO_BR/work/ron-rig-comparison-20261026/COMPARISON.md` | Actual RON reference rig inspected; IK/poles found, one chain allows stretch, no IK/FK snap UI found. This is not the implemented CP control solver. |
| T1 | `$HALO_BR/work/tutorial-rigging-review/REVIEW.md` | Exactly eight actual sampled frames and transcripts, not entire videos. Transferable control/pivot ideas only. |

F1 exact title: **Fallout 4 Blender Rig Animation Guide**. Google Drive returned
229 paragraphs in tab `t.0`, covering document indexes 1–21835, revision
`AHj4eMRUsskJuoRzNYdeAOEQeqjY5lXLYD6E33liQofnxWV4e23oFpXB9sKFNkdGcm0t0KdJgPG3B75d4u467Q`.
Relevant source spans: matching skeleton/import 3443–3962 and 6729–6872;
attachment targets/named empties 5355–6423; WeaponParent/Root/COM/Camera and hand
controls 6883–9114; driver/follow spaces 9528–11277; Action protection/range/FPS
12855–13981; assembly/additive/third-person composition 14782–17291; annotations
17296–19939; standalone viewer/motion data 19942–21123. These indexes identify
the read revision, not stable anchors in future edits. The guide's 30 fps advice
does not override per-source evidence such as M1911 reload 60 fps.

Bingle archive **Fallout4 MMD VibePort v0.72.7z**, 22,313,417 bytes, SHA-256
`64b8275f8c7f6e07c69bd5dd9e6c0ca1b61e37cc88afe127970e5999e748d477`;
retargeter metadata **0.7.2**, inspected PyNifly metadata **28.1.0 / dev 20**.
Function spans in REPORT cover source delta 110–149, world/local mapping 927–978,
palm mapping 1006–1026, two-bone solve 1231–1321, frame ordering 1902–1935 and bake
2555–2666 of the recorded retargeter `__init__.py`. Annotation report pins exact
HKX module spans/hashes. These are inspected declarations, not verified upstream
release/license or direct reuse permission.

Tutorial actual samples: [Infima](https://www.youtube.com/watch?v=3iiwfU0JoYE),
22:00.28, 30:37.44, 34:59.93, 39:57.42 of 43:44;
[GAME WEAPONS](https://www.youtube.com/watch?v=rEB3cRr8uxo), 04:13.23, 10:33.08,
14:46.32, 18:59.55 of 21:06. Second transcript is mostly music/misrecognition.
No source-hand/Halo/CP export acceptance follows from those frames.

## Reproduction commands — documented, not run by hub maintenance

First inspect the referenced command contract and current file hash. Scripts can
contain fixed outputs or scene assumptions. Keep execution with the owning port
agent, use fresh isolated destinations, and do not touch its GUI/VM or accepted
outputs. Read-only report/hash checks are sufficient for hub maintenance:

```sh
sha256sum "$HALO_V4/rig-v4/live_playback_v4.py" \
  "$HALO_V4/reference-playback/reference_sampler.py" \
  "$MAX_EXPORT/exports/idle-v4/source-fbx-parity-v2.json"
```

M1911 existing comparison entry points (require original native captures):

```sh
blender --background --factory-startup --python "$M1911_TOOLS/compare_m1911_source_fbx.py" -- \
  --source-dir "$SOURCE_CAPTURE_DIR" --fbx "$CANDIDATE_FBX" --out "$NEW_PARITY_REPORT"
blender --background --factory-startup --python "$M1911_TOOLS/validate_m1911_fbx.py" -- \
  --fbx "$CANDIDATE_FBX" --source-receipt "$NATIVE_RECEIPT" --out "$NEW_STRUCTURAL_REPORT"
```

Halo V4 console start/stop and restoration contract is in `rig-v4/README.md`;
`start_reference` is exported-GLB reference sampling, `start` is editable-control
evaluation. Full-sequence README contains historical **V3** capture examples;
do not relabel those commands V4. Condition and graph-audit repro entry points:
`$HALO_V4/condition-semantics/verify_condition_contract.py` and
`$HALO_BR/work/deformation-evaluator-20261026/graph-dependencies/audit_graph.py`.
They establish their structural/math scope, not native runtime execution.

RoN commands and prerequisites are in [recovery](../hk416-recovery-contract.md#local-commands-and-prerequisites),
[native authoring](../native-animation-authoring.md) and [parent/weight comparisons](../fo4-scenario-comparison.md).
Do not run their native/Blender suites just to update prose. Preserve baseline,
one-channel, negative-control, semantics, readback, visual and runtime results as
distinct checks. COD/BF have no reproduction commands because no adapter is tested.
