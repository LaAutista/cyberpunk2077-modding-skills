# Timed events, mechanisms and native export

Use with the [native authoring contract](../native-animation-authoring.md).
Evidence IDs resolve in the [register](evidence-register.md).

## Keep clocks and ownership explicit

Maintain clip-owned event lists with original text/payload, duplicates, time origin,
effective rate (`fps / fps_base` where applicable) and source interval. Timeline
markers can be a rebuildable UI mirror; they must not silently repopulate an
intentionally empty list. Replace only events the tool owns. Preserve unmanaged
events and same-frame multiplicity.

Transform samples, montage/state clocks, source annotations, target event ticks,
reload speed scaling and gameplay ammo commit are separate contracts. Convert once
at a named boundary. Do not equate a magazine insertion frame or sound event with
gameplay commitment, or a donor sound timeline with recovered source annotations.

**PROVEN inspected caveats, F2:** the Bingle-linked PyNifly sources preserve Action
JSON annotations and duplicate markers, but contain differing time origins,
ignored fps_base, ASCII writer limits, and frame-0 events filtered by later Action
starts. Legacy XML and native HKX paths differ; operator status code also needs
review. No addon execution, HKX roundtrip or event dispatch was validated. These
findings justify explicit event contracts, not adoption of that code.

**PROVEN boundary, M1/M4:** M1911 requests source event sidecars, but complete
original annotation recovery is not established. No source audio was supplied;
do not invent it or borrow another port's assets as source evidence.

## Preserve mechanism tracks and attachment chains

Inventory receiver, barrel, slide/bolt, magazine, trigger, latch, rounds and props,
their actual parent/component frame, pivot, rigid/deforming weights and channel
semantics. Retain stationary operational offsets and authored translation/scale.
Native component clips may have different names from player clips. Missing routing
must fail loudly unless a labeled fallback is part of the inspection contract.

**PROVEN, R1/R4:** RoN receiver/base recoil routes to `recoil_shoulder`; a same-name
fallback silently showed bind instead. A 60 Hz preview missed a 22.222 ms recoil
peak, so exact native-key checks and denser firing samples were needed. Independent
component clocks clamp at their own endpoints; rescaling them changes the assembly.
Reload `_01/_02` aliases were random variants, not automatically ADS states.

**PROVEN, M4:** inspected CP M1911 target chains separate Receiver → Barrel →
Magazine/MagazineReload ownership. The donor mechanism rig lacks a separately
tilting physical barrel. A fitted idle does not prove a compatible mechanism route.
Choose/extend a target only after evaluating actual source mechanisms and checking
native graph/slot behavior. Do not reuse rifle mounts or copy source Euler keys.

## Native serialization gates

Pin actual input/tool hashes. On copies, run unchanged and one-channel controlled
roundtrips first. Then prepare authored clips, import selected native containers,
serialize and independently decode actual stored bytes; compare to the **unprepared**
authored expectation. Require both numeric channel and semantic checks, with
unselected chunks, metadata, scale/float/fallback/root tables and events retained.
After sequential imports, decode all inherited clips needed by the preview.

**PROVEN bounded adapter, R5:** selected WolvenKit 9.0.1 path preserves supported
Normal/additive, raw/constant tiny rotations, declared scale/float/event cases and
key sampling. Quaternion stripping order and float32 `W==1` shortcuts previously
caused loss; independent readback plus negative cases guard them. Unknown layouts,
new names/skeletons, arbitrary event classes and unsupported interpolation fail.

Compressed transform time uses uint16 ticks; over two seconds its half-tick is
about 15.26 µs. Supported Sound/Phase event starts/durations use uint32 ticks at
30 Hz. `numFrames=ceil(duration*30)` is a header field, not the stored key count or
proof of runtime sampling frequency. Event serialization does not prove audible
dispatch, ammo timing or phase behavior.

Re-render actual readback with the same source/retarget cameras and assembly;
do not reapply authoring corrections to readback. If packaging is in scope,
re-extract the exact candidate archive, compare shipped hashes/resources and inspect
those inputs. Native compile/pack success is not runtime acceptance. Use the
[behavior matrix](../weapon-rigging-animation.md#behavior-coverage-matrix) for
authorized equip/fire/reload/ADS/movement/interruption tests on that package.
