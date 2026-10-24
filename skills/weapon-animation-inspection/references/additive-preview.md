# Local animation and additive preview

[weapon_animation_gltf.py](../scripts/weapon_animation_gltf.py) samples embedded
GLB local TRS channels and returns named world matrices in Blender Z-up.
[ron_additive_preview.py](../scripts/ron_additive_preview.py) composes an explicit
normal base with a WolvenKit bind-relative additive export. These are original
project preview helpers made portable; they do not assemble a weapon, import
meshes, render a scene, retarget bones, or run Cyberpunk's animation graph.

Use Blender's existing Python, NumPy and `mathutils`. Put the included scripts
directory on `sys.path`; no private project imports or package installation is
needed. For example, from a Blender script with paths supplied by your caller:

```python
import sys
sys.path.insert(0, str(preview_scripts_directory))
from weapon_animation_gltf import GltfAnimation
from ron_additive_preview import additive_pose

animation = GltfAnimation(native_readback_glb, normalize_rotations=True)
normal_worlds = animation.pose(normal_clip_name, seconds)
recoil_worlds = additive_pose(animation, additive_clip_name, seconds,
                             base_clip=normal_base_name, base_time=0.0)
```

Select the actual matching normal base explicitly, such as a verified shoulder
or ironsight pose. Inspect weapon/mechanism and magazine clips independently:
the player's additive clip name need not exist on the weapon. A missing required
clip must be reported; use a bind pose only when justified and labeled.

## Export and transform contract

The composer requires the WolvenKit 9.0.1 `additiveAddRelative=true` convention:
non-Normal exports contain bind-relative local transforms. Raw additive exports
are a different representation and are not detected automatically from metadata.
The caller must establish the export setting and input hashes. See the pinned
[animation exporter](https://github.com/WolvenKit/WolvenKit/blob/9.0.1/WolvenKit.Modkit/RED4/Tools/AnimationTools.cs)
and [normalization helpers](https://github.com/WolvenKit/WolvenKit/blob/9.0.1/WolvenKit.Modkit/RED4/Tools/Animation/Shared.cs).

For bind `B`, exported additive local transform `E`, and chosen base local pose `P`:

```text
T = P.T + E.T - B.T
Q = normalize(P.Q * inverse(B.Q) * E.Q)
S = P.S * E.S / B.S                 # componentwise
```

Sample locals first, compose them, then accumulate the hierarchy. Decomposing
world matrices loses information when nonuniform scales introduce shear.
Preserve small source scales, including values close to one. Singular/reflected
scales are rejected by the additive composer. The loader rejects matrix nodes,
ambiguous names/hierarchies, duplicate channels/clips, nonfinite data, sparse or
normalized accessors, external buffers and unsupported interpolation. Its bounded
contract is float32 LINEAR/STEP TRS; it is not a general glTF implementation.

`Additive` and `AdditiveWithoutFirstFrame` use the same bind-relative exporter
formula. Neither tells this helper to invent a base pose or drop the first frame.
The preview uses full weight and does not emulate runtime weights, masks, events,
procedural camera/IK, transitions or first-frame graph semantics. A Normal weapon
`recoil_shoulder` clip remains Normal even when paired with additive player recoil.

WolvenKit 9.0.1's `W == 1` quaternion shortcut can erase nonzero XYZ components
during import or compressed decode. This helper cannot recover already-lost
values from an exported GLB. Establish native-key readback fidelity separately;
do not conceal loss by increasing preview tolerances or perturbing quaternion W.

## Checks and evidence boundaries

Run asset-free regression checks from the repository root:

```bash
blender -t 2 -b --factory-startup --python-exit-code 1 \
  --python skills/weapon-animation-inspection/scripts/test_animation_preview.py
```

The tests independently construct expected matrices for noncommuting rotations,
nonuniform scales and hierarchy composition; check identity delta, both additive
types, LINEAR interpolation and STEP exact endpoints/clamping; and exercise
thirteen rejection fixtures. The portable sampler corrects the old project's
STEP endpoint bug, which selected the penultimate value at the final timestamp.
The frozen project helper and accepted assets were not modified by this port.

Optional read-only external checks use caller-owned files:

```bash
blender -t 2 -b --factory-startup --python-exit-code 1 \
  --python skills/weapon-animation-inspection/scripts/test_animation_preview.py -- \
  --asset "$WEAPON_READBACK_GLB" --asset "$PLAYER_READBACK_GLB"
```

The portable version parsed five clean native readbacks containing all 149 clips
and sampled 8,568 distinct per-clip key times with finite named transforms. Matching
player single-shot shoulder/ironsight additive composition is also checked when
present. These checks preserve and recheck input hashes; they do not establish
contacts, native encoding fidelity or visual/gameplay behavior. Output may contain
local paths, so sanitize logs before publishing them.

The earlier private raw-versus-bind export experiment covered male/female shoulder
and ironsight recoil, 53 samples per clip. It measured at most `4.769e-7` for
reconstructing the toolkit's bind export and `1.312e-6` for independent composed
world matrices. It also recorded an exporter-loss case of `2.153e-4` caused by the
quaternion shortcut above. These are bounded historical fixture results, not
accuracy guarantees for other rigs, new exporter versions or later assets. The
fixtures, game assets and third-party toolkit source are not included here.

For actual acceptance, render the complete applicable sequence, open the contact
sheets and critical full-size frames yourself, then record findings separately.
See [contact-sheet validation](contact-sheets.md). Every helper/test keeps visual
and runtime acceptance false.
