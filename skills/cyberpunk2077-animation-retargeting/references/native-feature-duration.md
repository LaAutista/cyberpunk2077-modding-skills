# Feature-driven transition duration

Implementation evidence for the retained Cyberpunk2.5 executable SHA256
`d36e74c47592e9c656ae250078cb40b2be63c782af5bfbeff2280d43e653fab4`.
Addresses are preferred-image VAs. These are inspected native branches and
analyst fixtures, not game observations. Use with
[state transitions](native-graph-semantics.md#duration-progress-curves-and-inertialization)
and [clock/inertia](native-clock-inertia.md).

## Three sources of the selected values

Duration getter `0x1403aaea4` and inertia getter `0x1403aae78` select:

| Descriptor configuration | Duration | Inertia request |
| --- | --- | --- |
| No `animFeatureName` | authored float+0x70 | authored byte+0x74 |
| Named feature, ordinary transition | instance slot from descriptor+0xa8 | slot from+0xb8 |
| Named feature, out-of-action transition | slot from+0xf8 | slot from+0x108 |

The second and third rows are different producers. Do not assume an outgoing
transition repeats the lookup performed for an incoming transition, or that
serialized `duration` is a fallback whenever the resource is missing.

## Ordinary transition refresh and database selection

Start wrapper `0x140585800` calls refresh `0x140585760` before reading either
getter. Refresh skips unnamed and out-of-action descriptors. Otherwise it loads
`actionAnimDatabaseRef` at+0x80, resolves the resource handle through
`0x14032cf98`, and checks its type through `0x1405884cc`. The native RTTI
initializer `0x140d16398` identifies the expected type as
`animActionAnimDatabase`; the cast also walks base-class types.

Registration `0x14058b8a4` binds three inputs under the descriptor's feature
group: `animFeatureName`, `state`, `animVariation`. Their current instance
values come from the offsets stored at+0xc8,+0xd8,+0xe8. In particular, the
current row's feature name is an input value; it need not equal the descriptor's
feature-group name.

Lookup `0x140588718` scans resource.rows at+0x40, count+0x4c, stride0x38,
in stored order. A row matches when all three tests hold:

- Row feature equals the current feature, or equals literal `*`.
- Row state equals the current state, or is signed -1.
- Row variation equals the current variation, or is signed -1.

The **first** matching row wins. There is no preference for a later exact row
over an earlier wildcard. The star initializer `0x142740d30` supplies CName
hash `0xaf63a74c8601927d`, with the `*` string at `0x1435757b8`.

The returned row.animationData starts at row+0x10. Refresh copies its
`inTransitionDuration` (+0x18) into the ordinary duration slot and
`inCanRequestInertialization` (+0x20) into the inertia slot. The getter then reads
those values for the impending transition. A valid database with no matching
row returns the zero-filled default record at `0x1435b2400`, yielding duration0
and false in this branch. A missing/wrong-type resource takes the cold path
`0x142492726` and does **not** write either slot. Its previous/initial values
therefore matter; do not silently replace this case with the no-match result.

### Fresh state versus reused state

Typed graph-state creation `0x140222f3c -> 0x140222f58 -> 0x140222fe8`
explicitly fills the requested compiled payload with zero at `0x1402230ca`.
The size comes from layout+0 or+4 according to the creation mode. Unkeyed
duration/inertia registration supplies size/alignment4/4 and1/1; finalizer
`0x1403cbd10` assigns their offsets but does not initialize payload itself.
Thus a fresh valid cache starts at0/false. If no intervening writer/transfer
occurs, its first missing-resource refresh retains0/false. After a successful
refresh writes .4/true, the same failure retains .4/true. Authored no-feature
fallback and valid-database/no-row zero are distinct branches.

Graph setup `0x14026a6cc` then performs feature/variable setup and node callbacks.
Mode selects a prefix count at G+0x70 or+0x84 of the same16-byte array at G+0x78.
It is not a universal clear on every activation. Configured primitive graph
variables have explicit default stores; other categories delegate helpers.
State replacement can subsequently transfer values from another graph.
Fresh zero therefore does not certify the post-setup/post-transfer value of
every slot. For an affected path, identify its last initializer, refresh,
alias writer and transfer instead of reading only the serialized default.

Retained `state-defaults-deep/findings.md` and its independently reviewed checks
establish these stores and the no-write discriminators. Delegated condition,
postprocess and state-transfer categories are not claimed universally traced.

For a concrete discriminator, place wildcard `(*,-1,-1,duration=.8)` before
exact `(attack,2,4,duration=.2)`. Inputs `(attack,2,4)` select .8. Reversing
the rows selects .2. Eight analyst fixtures cover order, state/variation
wildcards, name mismatch and empty rows; they do not execute the game.

## Out-of-action producer

`AnimNode_SkPhaseSlotWithDurationAnim` has a separate activation method
`0x1405883b4` (instance vtable `0x1430f0ae8`, slot30/+0xf0). It resolves its
own database at node+0x100 and uses the same row lookup with feature/state/
variation instance slots+0x130/+0x140/+0x150. On a valid resource it writes:

- Row `animationName` into node slot+0x120.
- Row `outTransitionDuration` into node slot+0x160.
- Row `outCanRequestInertialization` into node slot+0x170.

Registration `0x14056d1ec` binds the latter two variable descriptors under
node.animFeatureName(+0xf8) and members `privateOutTransitionDuration` and
`privateOutCanRequestInertialization`. Transition registration uses those same
group/member keys for its out-of-action slots. The graph compiler's
[keyed allocation](native-synchronization.md) aliases matching keys to the same
instance storage. Thus an activated action node can supply the outgoing
transition's duration and inertia request. This is not a direct read of the
transition's own database reference on every outgoing transition.

Missing resources leave these writes undone; active node selection, activation
order and the current feature payload remain inputs to an actual project.
The identity chain is class registration `0x1417e90bc` → type table
`0x1433b1088` → constructor thunk `0x140d36820` → constructor
`0x140d36828` → the instance vtable above. That table also identifies the
registration method at slot28, rather than relying only on similar field offsets.

## Sources and boundary

Pinned SDK declarations corroborate names/layout, not the recovered selection:
[transition description][transition], [database][database], [row][row],
[animation data][data], and [action node][node]. Local native evidence includes
the getter, start, refresh, row lookup, type/wildcard initialization, registration
and activation disassemblies plus `feature-lookup-checks.json`. No executable
or disassembly is redistributed with the skill.

This explains selected-value production on the named paths. It does not identify
a particular loaded database, live feature/state/variation, post-transfer cache
value after a failed resource resolution, or the selected transition in gameplay.

[transition]: https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimStateTransitionDescription.hpp
[database]: https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/ActionAnimDatabase.hpp
[row]: https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/ActionAnimDatabase_DatabaseRow.hpp
[data]: https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/ActionAnimDatabase_AnimationData.hpp
[node]: https://github.com/wopss/RED4ext.SDK/blob/8ebb8da485b4ab22081e9be65de70fe1193538da/include/RED4ext/Scripting/Natives/Generated/anim/AnimNode_SkPhaseSlotWithDurationAnim.hpp
