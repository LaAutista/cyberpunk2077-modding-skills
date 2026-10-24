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

Two manifest schemas are supported; having both files is rejected as ambiguous.

* Legacy `render.json`: positive numeric `fps` and a sorted, unique, nonempty
  integer `frames` array, for example `{"fps":30,"frames":[0,1,2,3]}`. Files are
  named `0000.png`, `0001.png`, and so on. This schema has no previous image hashes,
  so the helper records current hashes but cannot establish earlier image identity.
* `render-manifest.json`: `rendered:true`, positive `fps`, and sorted unique frame
  objects containing integer `frame`, nonnegative numeric `time`, `path`, and a
  lowercase 64-digit `sha256`. Every image hash is checked before output, including
  frames omitted by `--every`, and rechecked before writing the receipt. Paths must
  resolve to the matching numbered PNG inside the input directory. Absolute paths
  work directly; relative paths default to the manifest directory. When a renderer
  recorded paths relative to its project directory, pass `--path-root` explicitly:

```bash
bash skills/weapon-animation-inspection/scripts/contact_sheets.sh \
  "$RENDER_DIRECTORY" "$NEW_SHEET_DIRECTORY" --path-root "$PROJECT_ROOT" \
  --every 1 --columns 4 --rows 4
```

Produce the manifest only after render completion; retain clip, input hashes,
camera, player and approximations in the renderer's manifest. The helper checks
all **listed** images, not whether the list covers the complete source animation
or whether underlying asset inputs are still current. Audit those separately.

It labels frame/time, retains the last listed frame even with `--every`, hashes
source images/manifest/sheets and writes `sheets.json`. It refuses an existing
output directory, missing listed frame, stale supplied image hash, or changing
manifest/image during sheet creation. Hashed-schema receipts explicitly set
`sourceImageHashesVerifiedAgainstManifest:true`; legacy receipts set it false.
Its output records the absolute
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
destinations. Both schemas, explicit relative-path roots and nineteen rejection
cases passed. The portable helper was also run read-only on a completed external
clean HK416 render manifest (four frames, output in a temporary directory); image
hashes matched. No renders or game assets are distributed. This exercises helper
behavior; it is not a weapon-animation or visual-acceptance test.
