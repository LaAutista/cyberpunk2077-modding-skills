# Animation retargeting knowledge hub

For project execution, start with the [retargeting state machine](../../../cyberpunk2077-animation-retargeting/SKILL.md):
one baseline, one gate, one fixture and a two-failure loop breaker. This hub retains
the detailed technical references.

Load the chapter for the current stage or defect. These references supply methods
and evidence contracts, not a universal converter. Exact receipts and source
identities live in the [evidence register](evidence-register.md); read the owning
project's fresh checkpoint before resuming a historical case.

## Choose the next chapter

| Current decision or failure | Read |
| --- | --- |
| Axes, rest/bind, hierarchy, or direct skeleton versus optional animator controls | [Spaces and bind contracts](spaces-bind.md) |
| Recover original motion; choose Unreal, MAX, NIF/HKX or CP adapters | [Source playback and adapters](source-playback-adapters.md) |
| Transfer Shiagur's FO4 advice without importing engine-specific assumptions | [Guide synthesis](shiagur-reference.md) |
| Arm proportions, elbow flips, grip, magazine release/regrip or other contacts | [Proportions and contact](proportions-contact.md) |
| Begin hand fitting or diagnose a thumb/finger defect | [Finger checkpoint](finger-checkpoint.md), before full motion transfer |
| Native helpers, muscle graph, weights, palm folds or normals | [Native deformation](native-deformation.md) |
| Preserve timing, annotations, mechanisms and native clip semantics | [Events and native export](events-native-export.md) |
| Promote any converted animation, or decide visual acceptance | [Mandatory Blender full-motion/360° review and receipt](qa-debugging.md#mandatory-blender-visual-acceptance) |
| Isolate a regression or choose a discriminating test | [QA gates and debugging trees](qa-debugging.md) |
| Find versions, case status, ownership, exact receipts or reproduction entry points | [Evidence register](evidence-register.md) |

## Shared contracts

- A custom animator/control rig is optional. Direct raw/native-skeleton retargeting
  is valid; validate calibration/FK, needed IK/contact compensation and the chosen
  target skin/helper/export path. Block an independent path only on a demonstrated
  shared component defect with an identified revision and failing fixture.
- Work in order: preserve identities and source pairing → establish evaluated
  source playback → validate target rest/binds/skin/helpers → pass relevant
  reference alignment (including fingers when present) → transfer motion/contact
  → pass converted-target Blender review → verify native/package → test runtime.
- The Blender gate applies to **all animations**, including bodies, faces,
  creatures, props, interactions, cameras and mechanisms. Review matched source
  and converted target through full motion/transitions and full 360° coverage,
  including above/below/hidden areas and relevant close-ups. Visible defects fail;
  correct and re-review. Diagnostic exports and isolated test packages follow the
  [vertical-slice policy](../../../cyberpunk2077-animation-retargeting/references/runtime-validation.md);
  they do not imply accepted-beta or runtime acceptance.
- Preserve raw source, evaluated source and converted target evidence separately.
  Offline numerical agreement, rendered images and live behavior establish
  different facts. Keep source/visual/native/runtime gates separate.

## Read the evidence level

**PROVEN (bounded)** requires an identified receipt and its scope. **INFERRED**
methods need a fixture; **UNVERIFIED** means missing/unrun evidence.
**FAILED/REJECTED** results remain beside any later narrow pass. Existing
**PASS / FAIL / UNVERIFIED / BLOCKED** stage receipts retain their scope; new
retarget receipts use the [gate-specific vocabulary](../../../cyberpunk2077-animation-retargeting/references/pipeline.md),
never one combined success flag.

The [register](evidence-register.md) retains the RoN/HK416, Halo V4, M1911 and
FO4/Bingle snapshots, failures and ownership restrictions. The
[adapter chapter](source-playback-adapters.md) distinguishes actual source
inspection from unexecuted HKX candidates and untested COD/Battlefield adapters.
These dated records are not current blanket acceptance. Keep new findings in the
relevant chapter with source identity/evidence paths; keep raw assets and private
logs in their owning projects.
