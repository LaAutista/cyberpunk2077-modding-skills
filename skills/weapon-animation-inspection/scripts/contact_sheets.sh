#!/usr/bin/env bash
# Label completed Blender frames using the existing jq/ImageMagick toolchain.
set -euo pipefail
usage() {
    printf 'Usage: %s INPUT_DIR NEW_OUTPUT_DIR [--every N] [--columns N] [--rows N] [--path-root DIR]\n' "$0"
}
if [[ ${1:-} == --help ]]; then usage; exit 0; fi
if (( $# < 2 )); then usage >&2; exit 2; fi
input=$(realpath -- "$1")
output=$2
shift 2
every=1 columns=6 rows=6
path_root=$input
while (( $# )); do
    if (( $# < 2 )); then usage >&2; exit 2; fi
    if [[ $1 != --path-root && ! $2 =~ ^[1-9][0-9]*$ ]]; then printf 'Numeric options require positive integers.\n' >&2; exit 2; fi
    case $1 in
        --every) every=$2 ;;
        --columns) columns=$2 ;;
        --rows) rows=$2 ;;
        --path-root) path_root=$(realpath -- "$2") ;;
        *) usage >&2; exit 2 ;;
    esac
    shift 2
done
for dependency in jq magick sha256sum awk; do command -v "$dependency" >/dev/null; done
manifest=$input/render.json
hashed=false
if [[ -f $input/render-manifest.json ]]; then
    [[ ! -e $manifest ]] || { printf 'Ambiguous render manifests.\n' >&2; exit 1; }
    manifest=$input/render-manifest.json
    hashed=true
fi
jq -e --argjson hashed "$hashed" '(.fps | type) == "number" and .fps > 0
    and (.frames | type) == "array" and (.frames | length) > 0
    and (if $hashed then .rendered == true
      and (.frames | all((.frame | type) == "number"
        and (.time | type) == "number" and .time >= 0
        and (.path | type) == "string" and (.path | length) > 0
        and (.path | test("[\\t\\r\\n]") | not)
        and (.sha256 | type) == "string" and (.sha256 | test("^[0-9a-f]{64}$"))))
      else true end)
    and ((if $hashed then [.frames[].frame] else .frames end) as $f |
      $f == ($f | sort | unique)
      and ($f | all(type == "number" and . >= 0 and . == floor)))' "$manifest" >/dev/null
mapfile -t frames < <(jq -r --argjson hashed "$hashed" '.frames[] | if $hashed then .frame else . end' "$manifest")
manifest_digest=$(sha256sum -- "$manifest"); manifest_digest=${manifest_digest%% *}
fps=$(jq -r '.fps' "$manifest")
declare -A paths times hashes seen_paths
if [[ $hashed == true ]]; then
    while IFS=$'\t' read -r frame time file expected; do
        [[ $file == /* ]] || file=$path_root/$file
        file=$(realpath -- "$file")
        printf -v filename '%04d.png' "$frame"
        [[ $file == "$input/$filename" ]] || { printf 'Frame path must match its numbered PNG inside the input directory.\n' >&2; exit 1; }
        [[ ! ${seen_paths[$file]+exists} ]] || { printf 'Repeated image path.\n' >&2; exit 1; }
        seen_paths[$file]=1
        paths[$frame]=$file times[$frame]=$time hashes[$frame]=$expected
    done < <(jq -r '.frames[] | [.frame,.time,.path,.sha256] | @tsv' "$manifest")
fi
for frame in "${frames[@]}"; do
    if [[ $hashed == false ]]; then
        printf -v filename '%04d.png' "$frame"
        paths[$frame]=$input/$filename
        times[$frame]=$(awk -v frame="$frame" -v fps="$fps" 'BEGIN {print frame/fps}')
    fi
    file=${paths[$frame]}
    if [[ ! -f $file ]]; then
        printf 'Render is incomplete; missing frame: %s\n' "$file" >&2; exit 1
    fi
    if [[ $hashed == true ]]; then
        digest=$(sha256sum -- "$file"); digest=${digest%% *}
        [[ $digest == "${hashes[$frame]}" ]] || { printf 'Stale rendered image: %s\n' "$file" >&2; exit 1; }
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
per_sheet=$((columns * rows))
sheet_index=0
for (( start=0; start<${#selected[@]}; start+=per_sheet )); do
    tiles=()
    end=$((start + per_sheet))
    if (( end > ${#selected[@]} )); then end=${#selected[@]}; fi
    for (( i=start; i<end; i++ )); do
        frame=${selected[i]}
        filename=$(basename -- "${paths[$frame]}")
        label=$(awk -v frame="$frame" -v time="${times[$frame]}" 'BEGIN {printf "%04d   %.3fs", frame, time}')
        tile=$temporary/tile-$i.png
        magick "${paths[$frame]}" -resize '320x180>' -background '#151515' -gravity center -extent 320x180 \
            \( -size 320x24 xc:'#151515' -font DejaVu-Sans -pointsize 12 -fill white -gravity west -annotate +5+0 "$label" \) \
            -append "$tile"
        tiles+=("$tile")
        digest=$(sha256sum -- "${paths[$frame]}"); digest=${digest%% *}
        if [[ $hashed == true ]]; then [[ $digest == "${hashes[$frame]}" ]] || { printf 'Image changed during sheet generation.\n' >&2; exit 1; }; fi
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
[[ $digest == "$manifest_digest" ]] || { printf 'Manifest changed during sheet generation.\n' >&2; exit 1; }
if [[ $hashed == true ]]; then
    for frame in "${frames[@]}"; do
        actual=$(sha256sum -- "${paths[$frame]}"); actual=${actual%% *}
        [[ $actual == "${hashes[$frame]}" ]] || { printf 'Image changed during sheet generation.\n' >&2; exit 1; }
    done
fi
jq -n --arg input "$input" --arg manifest "$(basename -- "$manifest")" --arg hash "$digest" --argjson count "${#frames[@]}" --argjson every "$every" --argjson hashed "$hashed" \
    --slurpfile selected "$temporary/selected.json" --slurpfile images "$temporary/images.jsonl" --slurpfile sheets "$temporary/sheets.jsonl" \
    '{input:$input,renderManifest:$manifest,renderManifestSHA256:$hash,sourceImageHashesVerifiedAgainstManifest:$hashed,renderedFrameCount:$count,selectedFrames:$selected[0],every:$every,
      includesEveryRenderedFrame:($selected[0]|length)==$count,sourceImageSHA256:($images|from_entries),
      sheets:$sheets,visuallyReviewed:false,runtimeVerified:false}' > "$output/sheets.json"
printf '%d sheets; %d/%d rendered frames included. Visual review pending.\n' "$sheet_index" "${#selected[@]}" "${#frames[@]}"
