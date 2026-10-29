# Diagnostic slice, accepted beta and runtime

As soon as one source clip, mapping and writable compatible container exist, take
that clip through the remaining native/package checks. Do not spend the main
workstream polishing fingers or porting a complete set before testing the plumbing.

The current vertical-slice policy permits an **isolated diagnostic package** with
explicitly disclosed visual defects or missing visual review. Keep its visual
gate FAILED or OPEN; name the exact clip, intended falsification test, known
defects and missing audio/events/features. Never overwrite or promote the working
baseline. A native mismatch, changed unrelated resources or unidentified shipped
bytes blocks even the diagnostic package. This exception does not authorize
installation, profile changes or game launch outside the user's current scope.

An **accepted beta** requires the existing
[full-motion Blender visual receipt](../../cyberpunk2077-modding/references/animation-retargeting/qa-debugging.md#mandatory-blender-visual-acceptance)
for the current candidate: matched source/target throughout the timeline and
transitions, full 360-degree coverage including above/below/hidden areas and all
relevant digit/contact/mechanism close-ups. Visible defects fail acceptance.
Generating renders is not inspecting them. A diagnostic runtime pass does not
waive visual failure or authorize full-set expansion.

Record package hash, source/target/container hashes, game/tool versions, selected
clip and body variant, prerequisites, mutually exclusive packages and effective
profile/override. Extract the isolated archive and compare every resource to the
intended checked output. Leave deployment to the authorized manager/profile path.

For an authorized user runtime test:

1. Preserve the profile and working package; enable only the intended test variant
   with its recorded dependencies and confirm which resource override wins.
2. Trigger the named clip and observe beginning, middle and ending. Confirm the
   expected motion actually replaces the intended state.
3. Enter/leave the state, loop if applicable, test relevant interruptions and
   repeat in each affected first-person/body/weapon variant.
4. Inspect hand/weapon contact, controls/IK, mechanisms and visibility; check
   audio/events only if part of this clip's acceptance scope. Record deviations.
5. Record the user's confirmation or failure with exact archive hash, environment,
   conditions and observations. Restore the baseline using the preserved profile
   when testing ends or the diagnostic fails.

Expected success is correct named motion with stable transitions and required
contact/IK in that tested scope. Missing game access leaves runtime OPEN with
these manual steps. Only identified user confirmation earns USER_RUNTIME_VERIFIED;
another build's report or static graph inspection cannot. Expand to other clips
only after all applicable gates for the slice pass. A later package needs its own
runtime evidence; a changed hash invalidates reuse of the old confirmation.
