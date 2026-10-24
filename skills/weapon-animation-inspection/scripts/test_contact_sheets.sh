#!/usr/bin/env bash
# Asset-free regression checks for the included contact-sheet helper.
set -euo pipefail
helper=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/contact_sheets.sh
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
mkdir -- "$scratch/render"
printf '{"fps":30,"frames":[0,1,2,3,4]}\n' > "$scratch/render/render.json"
for frame in 0 1 2 3 4; do
    printf -v name '%04d.png' "$frame"
    magick -size 64x36 "xc:rgb($((frame * 50)),40,80)" "$scratch/render/$name"
done
bash "$helper" "$scratch/render" "$scratch/sheets" --every 3 --columns 2 --rows 1
jq -e '
  .renderedFrameCount == 5 and .selectedFrames == [0,3,4] and .every == 3
  and .includesEveryRenderedFrame == false
  and .visuallyReviewed == false and .runtimeVerified == false
  and (.sourceImageSHA256 | keys) == ["0000.png","0003.png","0004.png"]
  and [.sheets[].frames] == [[0,3],[4]]
' "$scratch/sheets/sheets.json" >/dev/null
[[ $(magick identify -format '%wx%h' "$scratch/sheets/sheet-000.jpg") == 640x204 ]]
digest=$(sha256sum -- "$scratch/render/render.json"); digest=${digest%% *}
jq -e --arg digest "$digest" '.renderManifestSHA256 == $digest' "$scratch/sheets/sheets.json" >/dev/null
for frame in 0 3 4; do
    printf -v name '%04d.png' "$frame"
    digest=$(sha256sum -- "$scratch/render/$name"); digest=${digest%% *}
    jq -e --arg name "$name" --arg digest "$digest" \
      '.sourceImageSHA256[$name] == $digest' "$scratch/sheets/sheets.json" >/dev/null
done
for name in sheet-000.jpg sheet-001.jpg; do
    digest=$(sha256sum -- "$scratch/sheets/$name"); digest=${digest%% *}
    jq -e --arg name "$name" --arg digest "$digest" \
      'any(.sheets[]; .file == $name and .sha256 == $digest)' "$scratch/sheets/sheets.json" >/dev/null
done
bash "$helper" "$scratch/render" "$scratch/all" --every 1 --columns 5 --rows 1
jq -e '.selectedFrames == [0,1,2,3,4] and .includesEveryRenderedFrame == true' \
  "$scratch/all/sheets.json" >/dev/null
expect_failure() {
    local label=$1
    shift
    if bash "$helper" "$@" > "$scratch/failure.log" 2>&1; then
        printf 'FAIL: expected rejection of %s\n' "$label" >&2
        exit 1
    fi
}
expect_failure 'existing evidence directory' "$scratch/render" "$scratch/sheets"
expect_failure 'zero cadence' "$scratch/render" "$scratch/zero" --every 0
[[ ! -e $scratch/zero ]]
rm -- "$scratch/render/0002.png"
expect_failure 'missing unselected frame' "$scratch/render" "$scratch/missing" --every 3
[[ ! -e $scratch/missing ]]
for manifest in '{"fps":0,"frames":[0]}' '{"fps":30,"frames":[]}' \
    '{"fps":30,"frames":[1,0]}' '{"fps":30,"frames":[0,0]}' \
    '{"fps":30,"frames":[-1]}' '{"fps":30,"frames":[0.5]}'; do
    printf '%s\n' "$manifest" > "$scratch/render/render.json"
    expect_failure 'invalid render manifest' "$scratch/render" "$scratch/invalid"
    [[ ! -e $scratch/invalid ]]
done
mkdir "$scratch/objects"
for frame in 0 1 2; do
    printf -v name '%04d.png' "$frame"
    magick -size 64x36 "xc:rgb($((frame * 50)),40,80)" "$scratch/objects/$name"
    digest=$(sha256sum -- "$scratch/objects/$name"); digest=${digest%% *}
    file=$name
    if (( frame == 1 )); then file=$scratch/objects/$name; fi
    jq -nc --argjson frame "$frame" --arg file "$file" --arg sha "$digest" \
       '{frame:$frame,time:($frame/60),path:$file,sha256:$sha}' >> "$scratch/frames.jsonl"
done
jq -s '{rendered:true,fps:60,frames:.}' "$scratch/frames.jsonl" > "$scratch/valid-objects.json"
cp "$scratch/valid-objects.json" "$scratch/objects/render-manifest.json"
bash "$helper" "$scratch/objects" "$scratch/object-sheets" --every 2
jq -e '.selectedFrames == [0,2] and .renderManifest == "render-manifest.json"
 and .sourceImageHashesVerifiedAgainstManifest == true and .visuallyReviewed == false
 and .runtimeVerified == false' "$scratch/object-sheets/sheets.json" >/dev/null
jq '.frames |= map(if (.path|startswith("/")) then . else .path=("objects/"+.path) end)' \
    "$scratch/valid-objects.json" > "$scratch/objects/render-manifest.json"
bash "$helper" "$scratch/objects" "$scratch/rooted-object-sheets" --path-root "$scratch" --every 2
jq -e '.selectedFrames == [0,2] and .sourceImageHashesVerifiedAgainstManifest == true' \
    "$scratch/rooted-object-sheets/sheets.json" >/dev/null
for mutation in '.rendered=false' '.frames[1].sha256=("0"*64)' '.frames[1].sha256="bad"' \
    '.frames[1].path="missing.png"' '.frames[1].frame=0' '.frames|=reverse' \
    'del(.frames[1].time)' '.frames[1].path="../0001.png"'; do
    jq "$mutation" "$scratch/valid-objects.json" > "$scratch/objects/render-manifest.json"
    expect_failure 'invalid/incomplete/stale frame-object evidence' "$scratch/objects" "$scratch/object-fail" --every 2
    [[ ! -e $scratch/object-fail ]]
done
cp "$scratch/valid-objects.json" "$scratch/objects/render-manifest.json"
printf '{"fps":60,"frames":[0]}\n' > "$scratch/objects/render.json"
expect_failure 'ambiguous manifests' "$scratch/objects" "$scratch/ambiguous"
[[ ! -e $scratch/ambiguous ]]
rm "$scratch/objects/render.json" "$scratch/objects/0001.png"
expect_failure 'missing unselected hashed frame' "$scratch/objects" "$scratch/object-missing" --every 2
[[ ! -e $scratch/object-missing ]]
printf 'PASS: both schemas, relative/absolute paths, selections, endpoint, dimensions, hashes, review flags and nineteen rejection cases.\n'
