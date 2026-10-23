#!/usr/bin/env bash
# Label completed Blender frames using the existing jq/ImageMagick toolchain.
set -euo pipefail
usage() {
    printf 'Usage: %s INPUT_DIR NEW_OUTPUT_DIR [--every N] [--columns N] [--rows N]\n' "$0"
}
if [[ ${1:-} == --help ]]; then usage; exit 0; fi
if (( $# < 2 )); then usage >&2; exit 2; fi
input=$(realpath -- "$1")
output=$2
shift 2
every=1 columns=6 rows=6
while (( $# )); do
    if (( $# < 2 )) || [[ ! $2 =~ ^[1-9][0-9]*$ ]]; then
        printf 'Options require positive integers.\n' >&2; exit 2
    fi
    case $1 in
        --every) every=$2 ;;
        --columns) columns=$2 ;;
        --rows) rows=$2 ;;
        *) usage >&2; exit 2 ;;
    esac
    shift 2
done
for dependency in jq magick sha256sum awk; do command -v "$dependency" >/dev/null; done
manifest=$input/render.json
jq -e '(.fps | type) == "number" and .fps > 0
    and (.frames | type) == "array" and (.frames | length) > 0
    and .frames == (.frames | sort | unique)
    and (.frames | all(type == "number" and . >= 0 and . == floor))' "$manifest" >/dev/null
mapfile -t frames < <(jq -r '.frames[]' "$manifest")
for frame in "${frames[@]}"; do
    printf -v filename '%04d.png' "$frame"
    if [[ ! -f $input/$filename ]]; then
        printf 'Render is incomplete; missing frame: %s\n' "$filename" >&2; exit 1
    fi
done
selected=()
for (( i=0; i<${#frames[@]}; i+=every )); do selected+=("${frames[i]}"); done
last=${frames[-1]}
if [[ ${selected[-1]} != "$last" ]]; then selected+=("$last"); fi
# Fail on an existing evidence directory instead of mixing revisions.
mkdir -p -- "$(dirname -- "$output")"
mkdir -- "$output"
temporary=$(mktemp -d)
trap 'rm -rf -- "$temporary"' EXIT
printf '%s\n' "${selected[@]}" | jq -s . > "$temporary/selected.json"
: > "$temporary/images.jsonl"
: > "$temporary/sheets.jsonl"
fps=$(jq -r '.fps' "$manifest")
per_sheet=$((columns * rows))
sheet_index=0
for (( start=0; start<${#selected[@]}; start+=per_sheet )); do
    tiles=()
    end=$((start + per_sheet))
    if (( end > ${#selected[@]} )); then end=${#selected[@]}; fi
    for (( i=start; i<end; i++ )); do
        frame=${selected[i]}
        printf -v filename '%04d.png' "$frame"
        label=$(awk -v frame="$frame" -v fps="$fps" 'BEGIN {printf "%04d   %.3fs", frame, frame/fps}')
        tile=$temporary/tile-$i.png
        magick "$input/$filename" -resize '320x180>' -background '#151515' -gravity center -extent 320x180 \
            \( -size 320x24 xc:'#151515' -font DejaVu-Sans -pointsize 12 -fill white -gravity west -annotate +5+0 "$label" \) \
            -append "$tile"
        tiles+=("$tile")
        digest=$(sha256sum -- "$input/$filename"); digest=${digest%% *}
        jq -nc --arg name "$filename" --arg hash "$digest" '{key:$name,value:$hash}' >> "$temporary/images.jsonl"
    done
    printf -v name 'sheet-%03d.jpg' "$sheet_index"
    magick montage "${tiles[@]}" -tile "${columns}x${rows}" -geometry +0+0 -background '#151515' -quality 92 "$output/$name"
    digest=$(sha256sum -- "$output/$name"); digest=${digest%% *}
    jq -nc --arg name "$name" --arg hash "$digest" --argjson start "$start" --argjson end "$end" \
        --slurpfile selected "$temporary/selected.json" \
        '{file:$name,frames:$selected[0][$start:$end],sha256:$hash}' >> "$temporary/sheets.jsonl"
    sheet_index=$((sheet_index + 1))
done
digest=$(sha256sum -- "$manifest"); digest=${digest%% *}
jq -n --arg input "$input" --arg hash "$digest" --argjson count "${#frames[@]}" --argjson every "$every" \
    --slurpfile selected "$temporary/selected.json" --slurpfile images "$temporary/images.jsonl" --slurpfile sheets "$temporary/sheets.jsonl" \
    '{input:$input,renderManifestSHA256:$hash,renderedFrameCount:$count,selectedFrames:$selected[0],every:$every,
      includesEveryRenderedFrame:($selected[0]|length)==$count,sourceImageSHA256:($images|from_entries),
      sheets:$sheets,visuallyReviewed:false,runtimeVerified:false}' > "$output/sheets.json"
printf '%d sheets; %d/%d rendered frames included. Visual review pending.\n' "$sheet_index" "${#selected[@]}" "${#frames[@]}"
