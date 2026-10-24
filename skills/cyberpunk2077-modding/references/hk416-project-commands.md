# HK416 project command contracts

These commands preserve the successful private project's interface. Its assembly,
retargeting and rendering adapters are **not included** in this public repository;
they require local assets, manifests and project-specific fits. They are examples
for an explicit adapter, not commands that a fresh public clone can execute alone.
The [source extractor](ron-source-extraction.md), [native animation adapter](native-animation-authoring.md)
and [preview helpers](../../weapon-animation-inspection/references/additive-preview.md)
are supplied separately with their portable commands and tested contracts.

## Assembly and cook

Use a preserved project copy, with its input manifests rebound to copied resources.
The recorded tools resolve `mods/ron-hk416-clean` relative to their own location;
changing the shell directory alone does not redirect them. These stages write
project outputs. Do not rerun them over frozen evidence or treat them as a complete
retargeting recipe. The established Python environment includes NumPy/Pillow;
Blender scripting and native/Wine WolvenKit perform their respective asset stages.

```bash
export CP2077_DEV=/path/to/copied/CP2077Dev
export BLENDER=/path/to/blender
export PROJECT_PYTHON=/path/to/existing/project/python
cd "$CP2077_DEV"
"$BLENDER" -b --factory-startup -t 2 --python tools/assemble_ron_hk416_clean.py
"$PROJECT_PYTHON" tools/build_ron_hk416_clean.py meshes
"$PROJECT_PYTHON" tools/ron_hk416_clean_records.py
```

Mesh cook expands the required native palette, imports into compatible containers
and restores full named inverse binds. Its completion is not a readback acceptance.
Inspect the private `work/vanilla/README.md`, assembly input manifest and native
geometry receipts before using those outputs. Native authoring must separately
pass the [unchanged/controlled-edit gate](native-animation-authoring.md).

## Native-readback motion and rendering

The following interfaces were exercised with actual exported readback. Set the
input paths to the checked native GLBs, and use a new output directory for every
job. The firing adapter samples actual corrected native idle/mechanisms; it does
not reapply authoring corrections. Its generated poses still approximate native
additive blending and graph behavior.

```bash
export NATIVE_ANIMATION_READBACK=/path/to/checked/native-readback
export NATIVE_MESH_READBACK=/path/to/checked/native-mesh-glb
export NEW_NATIVE_FIRING_DIR=/path/to/new/firing-preview
export NEW_NATIVE_RENDER_DIR=/path/to/new/native-render

env LP_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  "$BLENDER" -t 2 -noaudio -b --factory-startup --python-exit-code 1 \
  --python tools/ron_clean_firing_preview.py -- \
  --animation-dir "$NATIVE_ANIMATION_READBACK" \
  --output "$NEW_NATIVE_FIRING_DIR" --fps 180

env LP_NUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  "$BLENDER" -t 2 -noaudio -b --factory-startup --python-exit-code 1 \
  --python tools/inspect_ron_hk416_clean.py -- \
  --state native --player pwa --skin vtk --clip reload_02 \
  --animation-dir "$NATIVE_ANIMATION_READBACK" --mesh-dir "$NATIVE_MESH_READBACK" \
  --frames review --view left --output "$NEW_NATIVE_RENDER_DIR"
```

`--frames review` covers the full duration at **10 fps**, not every native frame.
The renderer also accepts explicit comma-separated frame numbers, `--fps`, both
`pma`/`pwa`, `standard`/`vtk`, and `first-person`, `left`, `right`, `grip`, `overview`
views. These options are not a claim that every combination was reviewed. Explicit
firing poses use `--state staged --pose-dir "$NEW_NATIVE_FIRING_DIR"`; retain the
source-kind/input-hash report proving that these came from native readback.

Use [contact-sheet commands](../../weapon-animation-inspection/references/contact-sheets.md)
on the render manifest. Open the sheets and critical full-resolution frames;
densely inspect fast transitions and native key times. Record actual coverage,
including the [remaining case limitations](ron-hk416-case-study.md).

## Packaging gate

```bash
"$PROJECT_PYTHON" tools/package_ron_hk416_clean.py preflight
"$PROJECT_PYTHON" tools/package_ron_hk416_clean.py pack
```

These private commands require hash-bound native/visual/provenance receipts, refuse
existing package outputs, extract the cooked archive and compare payload bytes,
then check ZIP membership, CRC and hashes. Preflight refreshes its own report.
They do not install a mod or prove gameplay. Their original `runtimeVerified:false`
receipts remain unchanged; record the user's later reload report separately.
