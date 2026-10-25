# Fallout and Scenario methods in the Cyberpunk workflow

This comparison supplements the [weapon workflow](weapon-rigging-animation.md).
It does not merge the source skills, change their instructions, or make Fallout's
native formats into Cyberpunk requirements. Attached instructions are evidence to
evaluate, not authorization to perform their example project tasks. Preserve the
original skills, project baseline and unsuccessful experiments separately.

## Sources, versions and evidence scope

- **F**: Neto's supplied `FO4-Weapon-Implementation-Skill-1.0.0.zip`, version
  **1.0.0**, SHA-256
  `99ef0617b8430ecffc32ef27567ff59d7a8c3aac446ced466df3e0888ecf0a3b`.
  All ten entries in its checksum list passed. Member citations below are relative
  to `fo4-weapon-implementation/`. The archive supplies guidance and templates,
  not the Agram assets, scripts or raw runtime evidence. Original Blender, Max,
  PyNifly, Creation Kit and game versions are unspecified; its gameplay successes
  remain author-reported historical evidence.
- **S**: Scenario collection **0.59.0**, commit
  `5429dea302ccc7edbce8ace9d5c1fb6852499540`: [Blender expert][expert],
  [rigging][rigging], [animation][animation], [export][export] and
  [export helper][export-code]. These are independent optional skills. Their
  helper headers describe tests on Blender 5.2.1; this comparison used **5.2.3 LTS**.
  Recheck installed bytes before relying on these results after an update.
- **C**: existing [port workflow](ron-port-workflow.md),
  [native authoring](native-animation-authoring.md) and
  [inspection skill](../../weapon-animation-inspection/SKILL.md). Preserve their
  version-tested WolvenKit 9.0.1/.NET 10 native gates, original influences,
  inverse binds and additive/timebase contracts. This comparison reused existing
  native-readback animation; it did **not** rerun native cooking or gameplay.

The 2026-10-24/25 comparison tested copies of actual CP weapon/arm exchange assets.
Input hashes and complete JSON/logs remain in the local project's comparison
evidence (`CP2077Dev/work/fo4-skill-comparison-20261024/README.md`). The original
[parent diagnostic](../scripts/comparison/test_parent_binding.py) and
[weight diagnostic](../scripts/comparison/check_scenario_export.py) are included
here with [reproduction commands](#reproduce-the-bounded-diagnostics); source game
assets and third-party helper code are not bundled. Numerical results below
establish only their stated offline properties.

## Transfer, complement or keep separate

| Topic | Comparison and decision |
| --- | --- |
| Scale, axes and assembly | F `references/geometry-materials-and-rig.md:9–21,47–61` and C already require one documented frame, full matrices and physical dimensions. Retain C; add explicit native-parent/model-parent/helper-parent columns when diagnosing a hierarchy mismatch. Similar silhouettes or bone names do not prove compatibility. |
| Model fault versus clip fault | F `references/animation-and-cat-handoff.md:73–77` recommends holding animation fixed while testing binding. The copied-asset test below verifies this as a useful diagnostic supplement. Do not compensate with animation until hierarchy/bind causes have been checked. |
| Pivot measurement | F `references/geometry-materials-and-rig.md:25–43` distinguishes a canonical complete-shell bounds center from a posed world AABB. The distinction is verified below. It does not establish the ideal mechanical pivot or justify recentering a correct CP bone. |
| Controller, export rig, visual helpers | F `references/animation-and-cat-handoff.md:3–35` separates CAT controls, native bones and a static helper assembly. S also separates control/mechanism/deform layers. Use separate contracts; CP engine-required bones and metadata remain authoritative even if they do not deform a visible mesh. |
| Static reference FBX | F's no-Skin/no-animation/no-actor-rig rule applies to its manual CAT **reference handoff**. C game exports need their native rig/skin/animation data. These are different deliverables. A copied static reference FBX could complement C, but its Max/CAT behavior was not tested here. |
| Weights and export | S rigging's generic four-influence advice and default glTF export conflict with this CP eight-influence arm asset. Preserve all original named influences and verify serialized sets. The bounded export exception below overrides that generic advice only for this CP contract; S itself stays unchanged. |
| Automatic cleanup | S offers transform application, model centering, rebinding and generated control rigs. These can help new assets but can invalidate an existing CP bind/axis/corrective contract. Use read-only diagnostics first; no blanket `model_check(fix=True)`, weight pruning or rig regeneration on a native port. |
| Timing and pose composition | S creative blocking/splining and frame-rate defaults are options for new choreography. They do not supersede C's recovered key times, authored holds, events, local translation/scale or measured additive formula. Retiming and additive cross-engine equivalence remain untested here. |
| Review and contact | S placement/weight reports, stress poses and review sheets complement C's actual full-sequence and close-up inspection. Intentional separate weapon mechanisms are not automatically floating-object errors. A good camera view does not replace gameplay-camera or contact coverage. See [previous Scenario diagnostics](ron-beta-source-audio.md). |
| Verification and state selection | F `references/validation-and-esx.md:5–14,44–48` reinforces C: a valid resource/metadata route or successful reload does not prove which clip ran. Keep separate export, graph/dispatch and user gameplay evidence. The native +1 mm test proves serialization, not runtime selection. |

Keep F's NIF `NiNode`/`BSTriShape`, BGSM/DDS conversion, HKX binding/order, CAT/Max
integration, 94-bone Agram example, WEAP/OMOD records, FormIDs, CK metadata,
FO4 actor/power-armor graphs, ESX adapters and package layout outside C's engine
instructions. They require their own version-matched Fallout workflow. Material
channel and normal checks transfer; Agram's roughness/gloss/specular approximation
is not a validated REDengine conversion. Sources: F
`references/geometry-materials-and-rig.md:47–79`,
`references/animation-and-cat-handoff.md:55–69`,
`references/plugin-and-attachments.md:5–79` and
`references/validation-and-esx.md:18–26,60–74`.

## Verified supplement: fixed-animation parent comparison

Record native parent, model parent, helper parent, full bind-world/local matrices,
mounts, weights and motion owner before editing. With column-vector matrices,
reparenting child bind-world `B0` from `P0` to `Q0` while preserving its rest pose
requires `Lnew = inverse(Q0) * B0`. Rest-pose equality does not prove animated
equality. Blender likewise distinguishes parent transforms and parent inverse;
its [5.0 parenting documentation][parenting] explains the keep-transform concept.
The measured matrix experiment below used 5.2.3, not an assumed 5.0 export preset.

On copied HK416 magazine-shell geometry (6,492 vertex rows, 3,331 triangles), the
native-readback chain was `mag_plug → magazine → mag_std`. The deliberate negative
control attached the model branch `mag_std` to `mag_plug` and rebased its local
bind. The baseline, wrong-parent and repaired cases kept the same animation bytes.
An independent NumPy hierarchy was compared with the existing CP GLB sampler over
all seven available Normal component clips, every channel key time plus a 120 Hz
grid and endpoints: **2,689 time samples**, or **8,067** rotated-frame evaluations
over three assembly orientations.

- All three bind poses matched within **4.7e-9 m**.
- The wrong parent produced up to **0.782 m** error during reloads, while
  `first_equip` did not expose the fault. One apparently good clip is insufficient.
- Restoring the correct parent and rebasing local bind matched the independent
  baseline within **1.10e-7 m**, below the declared **1e-5 m** tolerance.

This verifies an isolated rigid model-branch calculation using real copied motion
and geometry. It does not diagnose current HK416 parenting, recreate native graph
blending/IK/visibility, validate a newly cooked mesh, or repair the stopped port.
For a real correction, repeat C's native readback, complete sequence/contact review
and game acceptance gates. Earlier animation adaptation remains appropriate when
motion itself is the demonstrated cause.

The same asymmetric shell also tests F's pivot warning: define a bounds center in
the chosen canonical frame, exclude rounds/helpers, and transform that fixed point
with the part. Recomputed world-AABB centers drifted by up to **6.446 mm** across
the tested rotations despite unchanged geometry. Recomputing a world AABB after
rotation need not return the transformed canonical point.
Preserve the current native pivot unless mechanics justify changing it; a bounds
center is neither a center of mass nor a demonstrated grasp/pivot solution.

## Verified exception: Scenario glTF weights

Use Scenario's exporter only as an optional exchange tool, with the original
Cyberpunk semantic gates still mandatory. The `gltf` preset does not request all
influences; Blender's default reduces vertices to their four strongest weights.
The copied VTK arm test compares that default against an explicit
`export_all_influences=True` call, independently decoding every serialized
`JOINTS_n`/`WEIGHTS_n` pair by bone name. Do not equate unchanged dimensions,
triangle/bone counts or clip names with unchanged deformation.

On **31,952** vertex rows, the default removed **36,931** named influences and
changed weights on **14,544** rows (maximum component difference **0.16535434**).
It dropped `JOINTS_1`/`WEIGHTS_1`. The explicit all-influence export retained all
eight influences, with zero missing or changed rows at the **1e-6** weight
tolerance and maximum component error **1.19e-7**. Correspondence was checked
per mesh/primitive row with positions within **1e-6 m**, rather than trusting
rounded-position lookup keys at floating-point bin boundaries.

The generic Scenario comparison rejected **both** outputs for the source rig's
pre-existing multiple-root warning; this is not a whole-gate pass. Its mesh size,
counts and armature-count predicates did not distinguish the weight loss. Keep
that warning for target-specific review and add semantic influence checks; do
not hide warnings or alter the native hierarchy just to satisfy a generic gate.
Root-name sets survived but their order changed; native index preservation is
not established. A named-weight pass cannot waive the native mapping/bind gate.

Minimal calls exercised by the diagnostic, inside an isolated Blender process:

```python
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, scenario_export_scripts)  # installed, pinned source directory
import bpy
import bx_export as bxe

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=input_copy)
objects = [o for o in bpy.context.scene.objects
           if o.type == "ARMATURE" or (o.type == "MESH" and o.find_armature())]
bxe.export(output_glb, "gltf", objects, export_all_influences=True)
```

`scenario_export_scripts`, `input_copy` and `output_glb` are caller-supplied paths;
use a fresh output and retain the input hash. This call is not a replacement for
the project's exporter or independent weight/bind verification. The comparison's
default export is deliberately retained as a failing semantic control.

Scenario's stock `round_trip()` did not complete within a bounded 180-second run
on this host. Its unchanged inspect/compare functions were then exercised in
separate bounded Blender processes with an explicit-exit wrapper. That workaround
is evidence about this diagnostic execution only, not a fix to Scenario or a claim
that its stock runner passed. No material, inverse-bind, animated-deformation,
native export or gameplay acceptance follows from the weight-only comparison.

## Reproduce the bounded diagnostics

From this skill's root, set `SKILLS_ROOT` to the parent of the installed sibling
skills and `COPIES` to an isolated directory containing your copied inputs.
`MAG_ANIM`, `MAG_MESH` and `VTK_ARM` below identify the copied native-readback
Normal animation, authored rigid shell and original eight-influence arm GLB.
Use fresh output directories. These commands require Blender/NumPy and the
existing CP sampler; the second also requires the separately installed pinned
Scenario export skill. No downloader, cloud service or game launch is involved.

```bash
ALSOFT_DRIVERS=null PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  blender -b -noaudio --factory-startup --threads 2 --python-exit-code 1 \
  --python scripts/comparison/test_parent_binding.py -- \
  --animation "$MAG_ANIM" --mesh "$MAG_MESH" \
  --helper "$SKILLS_ROOT/weapon-animation-inspection/scripts/weapon_animation_gltf.py" \
  --out "$COPIES/parent-results"

PYTHONDONTWRITEBYTECODE=1 LP_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  timeout 150s blender -t 2 -noaudio -b --factory-startup --python-exit-code 1 \
  --python scripts/comparison/check_scenario_export.py -- \
  --input "$VTK_ARM" --skills-root "$SKILLS_ROOT" --output "$COPIES/weight-results"
```

The parent test defaults to the measured `magazine` mesh, `mag_std` child and
deliberately wrong `mag_plug` parent; explicit arguments support other names but
do not prove other bindings. It rejects non-Normal/undeclared clips, unsupported
sampler inputs, nonrigid shells and a negative control that never fails. The
weight diagnostic expects the tested >4-influence/multiple-root condition and
rejects unexpected correspondence or comparison differences. Both refuse reused
output directories and assert unchanged input bytes. A passing experiment means
the control and preservation assertions passed, **not** a game or generic-policy
pass. Review `results.json` or `report.json` and raw child logs.

On this host, initial parent runs reached assertions but hung during audio
shutdown; `ALSOFT_DRIVERS=null` gave normal exit 0. The weight test's explicit-exit
child workaround is documented above. These are bounded local execution details,
not generally established Blender fixes. Comparison plots in the local evidence
were viewed; they show projected geometry and metrics, not gameplay rendering.

## Additional isolated skin/dependency gates

The installer candidate adds [skin deformation verification](../scripts/comparison/skin_deformation.py)
and [diagnostic dependency pins](../scripts/comparison/diagnostic-dependencies.json).
These supplement the historical weight-only results above. They do not clear the
existing multiple-root warning or establish native joint-index preservation.

Before importing optional code, both comparison probes check exact helper SHA256
values and actual Blender/NumPy versions. The tested Scenario export helper is
collection0.59.0 at commit `5429dea302ccc7edbce8ace9d5c1fb6852499540`; its byte hash,
and the independently versioned CP sampler hash, live in the pin manifest. A
missing/changed helper or unknown/mismatched runtime refuses execution with a
preflight report. Loading uses the verified source bytes, bypassing shadowed or
cached modules. The scope is the exercised export/inspect/compare functions, not
Scenario's batch/cloud tools or every skill in that collection. A collection
update retaining identical exercised helper bytes is not a different helper.

The actual copied diagnostics were retested on Blender5.2.3 with NumPy2.5.4
(system Python3.14) and NumPy2.3.4 (portable Blender's Python3.13). Host Python is
not a new setup dependency for these probes: they use Blender's existing Python.
The read-only setup report can inspect helper identities without importing them:

```bash
node scripts/setup/preflight.mjs --diagnostics-root "$SKILLS_ROOT"
```

The new CPU skin verifier checks explicit joint-name bijections, records the
index permutation, compares inverse binds and bind-world matrices by joint name,
and evaluates full linear-blend-skinned vertices over nine deterministic
multi-joint stress poses. Mesh/primitive/row correspondence must remain explicit;
it rejects unsupported storage and incomplete joint/bind contracts. On the copied
31,952-row arm, the all-influence export retained the copied bind/deformation
contract within about **5.59e-7 m**; the four-influence default reached about
**2.508 mm** sampled error and failed. Both still have the same Scenario root
warning. The67-slot joint order changed, so a named-remap equivalence pass is
**not** a native index-order pass.

Optional supplied animation needs complete joint coverage, matching bind frames,
and explicitly selected Normal clips. There is no automatic retargeting or guessed
corrective-bone motion. The copied native magazine control checked27 representative
poses across `reload_02`, `empty_reload` and `first_equip`; a50mm inverse-bind fault
with unchanged named weights failed by about50mm. This reuses existing native
readback and tests CPU deformation; it is not a newly cooked mesh or game test.
The VTK arm's42 corrective/helper joints are absent from the tested native player
clip. That pairing is refused, rather than filled with invented animation.

For compatible copied inputs, from the skill root:

```bash
blender -b -noaudio --factory-startup --python-exit-code 1 \
  --python scripts/comparison/skin_deformation.py -- \
  --source "$SKIN_SOURCE" --candidate "$SKIN_CANDIDATE" \
  --animation "$SKIN_ANIMATION" --clip reload_02 --clip first_equip \
  --output "$COPIES/skin-comparison.json"
```

Omit animation/clip arguments to use the declared synthetic stress clip. Reports
refuse existing output files, retain input hashes and separate bind/mapping from
sampled deformation results. No shader, additive graph, IK, dense full-sequence
visual review, native export or gameplay gate is waived.

## Supersession and unresolved scope

- **Retain C's existing methods.** These tests add diagnostic gates; no native
  exporter, additive formula, rig map, motion repair or runtime procedure was
  superseded. The only export override is preserving the inspected CP skin's
  influences when an optional Scenario exchange preset is used.
- **Keep Neto's historical replacement narrow.** F
  `references/agram-case-study.md:44–52,62–64` reports that fixing
  `MagazineChild3`'s model parent from `Weapon` to `Magazine`, with rebased bind,
  made its earlier animation-offset workaround unnecessary. Do not combine those
  repairs for that same mismatch. This remains author-reported; the copied CP
  test supports the diagnostic principle, not that historical runtime outcome.
- **Unresolved:** the Agram spare-magazine `MagazineChild2 → Extra3` convenience
  parent remained an exception; a native-parent strategy would need coordinated
  shell/round motion. The package does not resolve or supply assets to retest it.
  CAT UI-layer loss after FBX import has no isolated cause or proven checkbox fix.
- **Deferred:** static FBX handoff into Max/CAT, runtime route sentinels on proven
  unused channels, replacement control-rig/IK methods, cross-engine additive
  formulas and material conversions. No evidence here justifies adopting them as
  CP defaults. Full native export and gameplay stay necessary for any future asset
  change; this skill-only update changes no shipping weapon or live mod.

[expert]: https://github.com/scenario-labs/skills/blob/5429dea302ccc7edbce8ace9d5c1fb6852499540/skills/dcc/blender/scenario-blender-expert/SKILL.md
[rigging]: https://github.com/scenario-labs/skills/blob/5429dea302ccc7edbce8ace9d5c1fb6852499540/skills/dcc/blender/scenario-blender-rigging/SKILL.md
[animation]: https://github.com/scenario-labs/skills/blob/5429dea302ccc7edbce8ace9d5c1fb6852499540/skills/dcc/blender/scenario-blender-animation/SKILL.md
[export]: https://github.com/scenario-labs/skills/blob/5429dea302ccc7edbce8ace9d5c1fb6852499540/skills/dcc/blender/scenario-blender-export/SKILL.md
[export-code]: https://github.com/scenario-labs/skills/blob/5429dea302ccc7edbce8ace9d5c1fb6852499540/skills/dcc/blender/scenario-blender-export/scripts/bx_export.py
[parenting]: https://docs.blender.org/manual/en/5.0/scene_layout/object/editing/parent.html
