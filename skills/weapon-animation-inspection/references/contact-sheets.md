# Contact sheets from completed renders

The [included Bash helper](../scripts/contact_sheets.sh) was used in the original
inspection workflow. It only consumes PNG files and a manifest; it does not load
game data, render Blender scenes or make visual judgments.

Prerequisites: Bash (including `mapfile`), jq, ImageMagick 7's `magick`, the
`DejaVu-Sans` font, and `realpath`, `sha256sum`, `awk`, `mktemp`. Use paths appropriate
to your environment. From this repository's root:

```bash
bash skills/weapon-animation-inspection/scripts/contact_sheets.sh \
  "$RENDER_DIRECTORY" "$NEW_SHEET_DIRECTORY" --every 3 --columns 6 --rows 6
```

Input `render.json` needs a positive numeric `fps` and a sorted, unique, nonempty
integer `frames` array, for example `{"fps":30,"frames":[0,1,2,3]}`. Corresponding
files are named `0000.png`, `0001.png`, and so on. Produce this manifest only after
render completion; include clip, revision/input hashes, camera, player and known
approximations in your renderer's manifest as well. This helper checks listed
frame existence, not whether the list covers the complete original animation.

It labels frame/time, retains the last listed frame even with `--every`, hashes
source images/manifest/sheets and writes `sheets.json`. It refuses an existing
output directory or any missing listed frame. Its output records the absolute
input path for local provenance; inspect or sanitize generated manifests before
publishing them. Do not commit private renders or their metadata by accident.

`--every 3` is 10 fps inspection material for a 30 fps render, not every-frame
review. `--every 1` includes all listed frames but still does not review them.
Open the sheets and critical full-size before/after frames yourself; record the
actual views, frames and findings separately. `visuallyReviewed` and
`runtimeVerified` remain false deliberately.

Run the synthetic regression check without any game assets:

```bash
bash skills/weapon-animation-inspection/scripts/test_contact_sheets.sh
```

It checks frame selection including the endpoint, labels' sheet geometry, hashes,
honest review flags and rejection of incomplete or invalid manifests and existing
destinations. This exercises helper behavior; it is not a weapon-animation test.
