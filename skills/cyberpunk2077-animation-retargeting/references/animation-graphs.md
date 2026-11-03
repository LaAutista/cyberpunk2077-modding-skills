# Animation graphs, blending and transitions

Researched 2026-11-02. Use this for a pose that changes between clip playback,
graph composition and the game, or a failure at state entry, exit or interruption.
It is a bounded investigation workflow, not a complete REDengine evaluator.
Fix demonstrated geometry/motion defects in the existing preview first. An engine
reconstruction or custom observer is not a prerequisite for ordinary animation work.

The deeper [native implementation supplement](native-graph-semantics.md) now
answers transform/additive math, quaternion interpolation, sparse-track behavior,
weight history, transition arbitration, effective duration, capture/curve formulas,
clock/inertia, synchronization/events and shared-pose publication for the identified
2.5 branches. The declaration-only limits below explain why
names/fields alone are insufficient; they do not supersede that newer evidence.

## Evidence and ownership

Keep these separate: reflected declarations, converter implementation, native
static analysis, offline composed replay, and identified in-game observation.
Public SDK declarations describe fields, not their complete evaluation algorithm.
Record the source revision and executable/resource/tool hashes for each finding.
Offsets and node IDs below belong to their cited snapshot, never an arbitrary build.

Start at the actual entity/appearance and animated components. Record each
component's rig, graph, animation sets, parent/control binding, local mount and
mesh inverse-bind owner. A known-good NPC replacer can demonstrate that strategy;
it does not establish compatibility with the player's graph or motion.
[AnimatedComponent](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/ent/AnimatedComponent.hpp)
declares these resource/control fields, but does not establish update order.

An `.anims` supplies clips and metadata; a `.rig` supplies hierarchy/reference
data and mask definitions; an `.animgraph` connects pose/value nodes, variables,
state machines and output. The
[graph](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimGraph.hpp)
also has initialization, feature/database and time controls. Follow pose/value
links and state ownership while preserving handle aliases. JSON nesting order is
not execution order. Local-space pose, model-space pose, component/world transform
and mesh skinning matrix are different quantities; convert only at proven boundaries.

## Blend operators and masks

| Operator | Preserve and inspect | Do not infer from its name |
| --- | --- | --- |
| Blend2 | Both pose links, weight link/range, time warping and sync | Clamping, extrapolation or the quaternion interpolation algorithm |
| BlendAdditive | Base/add pose, weight/bias/scale, additive type, track mode, mask, previous-frame weight/default, sync and postprocess | Universal delta basis, multiplication order or stateless evaluation |
| BlendByMaskDynamic | Base/blend pose, mask selector/list, weight and actual consumer rig | That every bone receives the blend or a named mask resolves |
| BlendOverride | Per-bone/per-track settings, blendAllTracks, delta-motion source, sync/postprocess | That override means a full unconditional pose replacement |
| BlendMultiple / BlendFromPose | Input ranges/radial mode or captured-pose mode/time/curve/tag | Selection, historic-pose capture or interruption/reset rules |

The reflected
[BlendAdditive](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_BlendAdditive.hpp)
contract separates additive space (`AGAT_Local`, `AGAT_Ref`) from track policy
(`BasePose`, `Interpolate`, `Add`). Do not rename Ref to model space without
additional evidence. Its previous-frame track field requires investigating
history, read/write role and reset semantics before claiming a stateless model;
the declaration alone does not establish those behaviors. Keep transform and float-track
composition separate. The [authoring adapter](cyberpunk-animation-semantics.md)
is a specific bind-relative interchange contract, not all these engine operators.

[BlendByMaskDynamic](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_BlendByMaskDynamic.hpp)
selects a mask whose data lives on the
[RigPart](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/RigPart.hpp):
tree/single-bone declarations, compiled weights and model-space rotation masks
are distinct representations. Use the existing [rig-mask inspector](agent-tools.md#inspect-the-composing-body-mask).
Its declared weights do not prove active selection; it explicitly rejects
unsupported compiled masks and conflicting declarations.

In the retained Cyberpunk 2.5 positive-weight, valid-selector branch,
BlendByMaskDynamic evaluates base
and second pose, looks up the selected name in rig parts, and leaves the base when
lookup returns -1. The ordinary branch multiplies per-bone mask and blend weights
before transform copy/interpolation; there is a separate model-space-rotation
branch. This explains a plausible silent no-op for a missing mask in that build.
It does not define invalid selector behavior, every mask format or every build.
See the private evidence locator below before reusing this result.

For a carrier/contact defect, inspect mask weights for hips, chest, camera,
weapon/hand controls and the actual skinned chain. Check zero, partial and full
weights with the downstream constraints present. A weight-1 success can conceal
a carrier that disappears or conflicts at partial weight. Do not move motion to
the pelvis or zero float tracks as a generic fix.

## State machines and transition clocks

The reflected
[state machine](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_StateMachine.hpp)
contains states, conditional entries, local/global transitions, default/frozen
state options and an any-state interpolator. Preserve each
[state's](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_State.hpp)
tags, outgoing indices, quality conditions and activation-frame transition guards. A
[transition](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimStateTransitionDescription.hpp)
has a condition/target, priority/enabled/forced settings, duration, interpolator,
sync, blend-from-pose and inertialization options. Conditional entries can select
activation differently from an ordinary outgoing transition.

Keep at least four clocks distinct: clip sample/progress, feature/event timing,
transition blend time and graph update time. Clip speed or a timed condition's
threshold is not automatically the crossfade duration. Linear/EaseIn/EaseOut/
EaseInOut are declared interpolation choices, not published exact formulas.
The declarations alone do not establish priority direction/ties, global/local
precedence, interruption/restart rules, zero-duration event ordering, the duration
clock or whether requested inertialization runs. For the matching executable,
use [native transition semantics](native-graph-semantics.md),
[feature duration](native-feature-duration.md) and
[clock/inertialization](native-clock-inertia.md) to replace those declaration-only
unknowns with the traced branches. For other builds or paths, investigate rather
than importing Unity, Unreal or Witcher behavior.

### Concrete native reload example

The retained `player_ranged.animgraph` resource, SHA256
`fcb4bb85300d8534fc683e5c7041a441ca69b62ea548717e7024770971dcd461`,
has 29 machines and 181 transition descriptions. Main machine handle 5 contains
Ready, Reload (state 1851), Equip and other states. Its ordinary reload branch
selects normal/empty through `RightReloadData.emptyReload` and a FloatLatch,
then three variants through `RandomSync.value`. Leaves are **SkSpeedAnim**:
`reload`, `reload_01`, `reload_02` use `ReloadSpeed.reloadSpeed`; their empty
counterparts use `ReloadSpeed.emptyReloadSpeed`. A plain SkAnim-only scan misses
all six. Trace inherited sampler types and their speed/value inputs.

The normal sampler H1923 feeds variant switch H1922, then normal/empty switch
H1921 inside Reload H1851. Additional switches/additive/state branches connect
that subtree to the state output; preserve them instead of inventing a direct
edge. The containing main contribution is StateMachine H5 → Switch H4 → Join H3
→ Blend2 H2 → Output H1. Each has other inputs/conditions, so this is a configured
route, not a claim that reload always supplies the final pose. Source states are
recovered from `outTransitionIndices`; a transition's target index alone is not
an edge inventory.

| Source | Trigger | Target | Declared blend duration |
| --- | --- | --- | ---: |
| Ready | RightReloadData.isActive | Reload | 0.20 s |
| Reload | InterruptReload | Ready | 0.20 s |
| Reload | reload_end | Ready | 0 s |
| Reload | RightShoot | Ready | 0.10 s |
| Equip | RightShoot | Ready | 0.12 s |

These are serialized-resource findings, not observed transitions. The inspected
descriptions have null syncMethod; that does not prove absence of implicit sync.
For example, Ready-to-Reload is Linear with priority 20 and inertialization request
disabled; reload_end priority 10 and InterruptReload priority 200 do not by
themselves prove a tie/priority algorithm. The normal leaves loop, the empty
leaves do not, and all specify `reload_end` as a loop event. Actual emission and
latch lifetime remain separate inputs for this actual graph. The
[event trace](native-synchronization.md#event-looping-and-delivery-are-separate-stages)
now establishes normal emission, reconciliation and previous-update signal
feedback without asserting this graph's live state. Identical clip names in two
weapon banks have different durations; bind the example to its bank and variant.

Inspect a transition as a sequence: established source state, trigger edge,
entry, intermediate blend, completion, interruption, re-entry and loop seam where
applicable. Log state, trigger/feature values, clip times, weight/curve and events
together. Testing only the two endpoint poses cannot establish the intervening
contact, camera motion or event/reset behavior.

## Sync, root motion and converter boundaries

Progress, event and foot-phase sync strategies and tagged master/slave samplers
are declared. For example,
[SyncMethodByEvent](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/SyncMethodByEvent.hpp)
names an event. Preserve strategy, event/tag and time-warp options. Their presence
does not establish phase alignment, leader selection or wrap rules. If sync is
the failing gate, use unequal-duration clips and a loop/event seam discriminator.
The [native synchronization chapter](native-synchronization.md) resolves the
configured methods, timewarp method, tag aliases, concrete receivers and ordinary
loop/re-entry behavior for the pinned build; those mechanisms are not equivalent.

Keep actor displacement, animated root-bone motion and component placement
separate. The
[Animation](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/Animation.hpp)
contains `motionExtraction` separately from its animation buffer and extra tracks;
graph nodes also select whether/how motion contributes. A preview root channel
alone cannot establish gameplay displacement.

Pinned WolvenKit source `6ab5da88c009b99e653ce87be5251a9c5bd15330` demonstrates:

- [Additive export](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/AnimationTools.cs#L199-L271)
  can add bind-local TRS for display;
  [import stripping](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/AnimationTools.cs#L431-L504)
  reverses that representation when selected. Record those options;
  an exported action may not contain raw deltas. Do not strip twice.
- [Root-motion import policy](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/Animation/AnimRootMotion.cs#L237-L265)
  distinguishes None (remove existing extraction) from Unknown (preserve existing
  extraction when available). Do not select None merely because a preview lacks it.
- [Current extras schema](https://github.com/WolvenKit/WolvenKit/blob/6ab5da88c009b99e653ce87be5251a9c5bd15330/WolvenKit.Modkit/RED4/Tools/Animation/Shared.cs)
  is v5 and includes events/tracks and other metadata. This is current upstream
  source, not a migration of the existing toolchain pinned to WolvenKit 9.0.1.
  Verify the installed importer/writer contract and preserve its compatible extras.

These are converter-source findings, not engine blend or gameplay execution.

## Shared poses, constraints and final output

[SharedMetaPose](https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_SharedMetaPose.hpp)
declares a pose input and weight; its additive sibling adds its own space/track
options. Neither declaration promises a complete final parent pose, name remap,
same-frame publication or post-IK data.

The retained 2.5 weight-1 native branch copies indexed transform and float-track
records into an evaluated/initialized input pose. Its transform branch checks the
low 16 bits of the index but addresses with the full 32-bit value; that is not a
complete malformed-index validation. No destination-index bounds check was
established for its float-track stores. That supports
a sparse indexed overlay, not an arbitrary skeleton-to-skeleton conversion.
Prove source/consumer rig index compatibility, coordinate frame, producer,
coverage and frame ownership before adding a conversion. Otherwise a second
conversion can corrupt an already converted pose. For a demonstrated shared-pose
mismatch, existing logs or a coordinated capture can discriminate inputs; this
does not make a custom observer mandatory for unrelated graph work.

The [producer and scheduling trace](native-shared-pose.md) now establishes mapped
current/reference ranges, local-domain ordinary entries, a Root-child exception,
sequential same-call graph publication, persistent float lifetime, the synchronous
command dispatcher and later skinning submission. Use its concrete boundaries
before requesting another observation or inventing an additional conversion.

Trace the selected pose path to constraints and output, and separately inventory
component/deformation/dangle work. A structural dependency through conditional
states is only a possible path. In the retained player-base investigation, an
ownership-expanded path reaches Ik2 nodes while a pure pose-link walk stops at
nested states; neither proves every listed node runs or fixes the final IK order.
Constraint flags/space and weight matter: a scoped static model-space orientation
write may preserve translation/scale, while a point constraint writes position.
Do not generalize that to every mode or assume correct FK survives later IK.

One retained generic deformation graph explicitly starts ReferencePoseTerminator
→ SharedMetaPose → PoseLsToMs and ends its conditional network with PoseMsToLs
→ Output. These are actual space-conversion boundaries; the middle is not an
unconditional chain. Stored `boneTransforms`, `aPoseLS`, `aPoseMS` and
`referencePoseLS` also must not be substituted for one another without checking
their contract against that rig.

## Trace one affected path

1. Preserve the current working baseline and failing candidate. Pin executable,
   entity/appearance, rigs, graphs, clip banks, tools and effective profile. Locate
   actual resources with [asset_inspect](agent-tools.md#find-the-archive-before-extracting);
   an archive match alone does not determine mod precedence.
2. Use bounded `asset_inspect.py graph` summaries, then inspect the relevant
   node/condition fields in the serialized resource. Trace actual output backward
   through containers, states and pose/value links. Preserve aliases; flag missing
   references/cycles. Do not equate a clip-name search with a complete sampler list.
3. Write one composition recipe: selected state/variant/bank, parameter producer
   and timeline, clip speed/phases, additive basis, mask/track policy, spaces,
   component mounts, root motion and downstream constraints. Mark unknown
   selection, scheduling or operators explicitly. Do not silently replace them.
4. For an offline replay, label the assumed clocks, blend formula and operator
   subset. Use noncommuting rotations and nonunit scales when validating additive
   math; weight 0/0.5/1 and excluded/partial-mask bones for composition; entry,
   midpoint, exit and interruption for transitions. Repair visible defects there.
5. Compare authored/readback graphs with `compare-graphs`, plus native clip/rig
   checks. Review continuous affected source/composed-native motion in Blender
   using the [existing acceptance contract](../SKILL.md#mandatory-blender-review-before-installation).
   A declared linear 0.20-second blend permits a labeled linear diagnostic; it
   does not establish the game's clock, quaternion method or interrupted history.
6. Choose the smallest remaining discriminator: missing-mask versus wrong-rig,
   wrong bank/speed versus blend clock, overwritten controls versus source motion,
   or shared-input frame versus double conversion. Reuse existing evidence first.
   If runtime is required and unavailable, give exact states/triggers/observables
   and expected distinctions; keep that gate OPEN instead of guessing a repair.

### Retained native evidence locator

Private owning-project evidence (not redistributed):
`body-analysis/weapon-transition-v38/README.md`, `test_transition_contract.py`,
`reload-speed-nodes.json`, transition JSON and both post-slot path reports;
`body-analysis/native-playback-v35/mask-eval.asm`, `mask-lookup.asm`,
`shared-eval.asm`, `shared-copy.asm`; and
`integration/runtime-assembly-v75/research/native25-operator-notes.md`.

Executable snapshot SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Preferred-image addresses: mask evaluator `0x140b3bb94`, lookup `0x1403a8a4c`,
SharedMetaPose evaluator `0x1403a5ddc`, weight-1 copy `0x1403a5e6c`.
These are static evidence locators, not portable hooks or live addresses.
Reuse requires matching identities and checking the scoped branch. This research
re-read existing traces/resources; it did not run the game or establish complete
graph, cloth, face, final-IK or render-pose parity.
