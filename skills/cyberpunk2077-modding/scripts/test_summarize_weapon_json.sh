#!/usr/bin/env bash
# Synthetic regressions always run; optional preserved copies check exact full results.
set -euo pipefail
tool_dir=$(cd -- "$(dirname -- "$0")" && pwd)
filter="$tool_dir/summarize_weapon_json.jq"
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
if (( $# != 0 && $# != 2 )); then
  printf 'Usage: bash %s [COPIED_JSON_DIRECTORY EXPECTED_SUMMARY_DIRECTORY]\n' "$0" >&2
  exit 2
fi

cat > "$scratch/animation.json" <<'JSON'
{"Data":{"RootChunk":{"$type":"animAnimSet","animations":[
  {"Data":{"animation":{"Data":{"name":{"$type":"CName","$storage":"string","$value":"draw"},"duration":1.25}}}},
  {"Data":{"animation":{"Data":{"name":{"$type":"CName","$storage":"string","$value":"reload"},"duration":3}}}}
]}}}
JSON
cat > "$scratch/material.json" <<'JSON'
{"Data":{"RootChunk":{"$type":"CMesh","materialEntries":[
  {"name":{"$type":"CName","$storage":"string","$value":"body"},"index":0,"isLocalInstance":1}
],"localMaterialBuffer":{"materials":[
  {"baseMaterial":{"DepotPath":{"$type":"ResourcePath","$storage":"string","$value":"engine\\materials\\metal_base.remt"}}},
  {"texture":{"DepotPath":{"$type":"ResourcePath","$storage":"string","$value":"test\\body.xbm"}}},
  {"unresolved":{"DepotPath":{"$type":"ResourcePath","$storage":"uint64","$value":"123456789"}}}
]}}}}
JSON
jq -e -f "$filter" "$scratch/animation.json" > "$scratch/animation-summary.json"
jq -e '.animationCount==2 and .animations==[{"name":"draw","duration":1.25},{"name":"reload","duration":3}]' "$scratch/animation-summary.json" >/dev/null
jq -e -f "$filter" "$scratch/material.json" > "$scratch/material-summary.json"
jq -e '.materialCount==1 and .materials==[{"name":"body","index":0,"isLocalInstance":1}] and .depotReferenceOccurrences==3 and .depotReferences==["engine\\materials\\metal_base.remt","test\\body.xbm"] and .unresolvedDepotReferences==[{"storage":"uint64","value":"123456789"}] and .emptyDepotReferenceCount==0' "$scratch/material-summary.json" >/dev/null

# No silent 100-item cap, deduplication of clips, or recursion-depth limit.
jq '.Data.RootChunk.animations = [range(121) as $i | .Data.RootChunk.animations[0] | .Data.animation.Data.name."$value" = ("clip-"+($i|tostring))]' "$scratch/animation.json" | jq -e -f "$filter" | jq -e '.animationCount==121 and .animations[-1].name=="clip-120"' >/dev/null
jq '.Data.RootChunk.animations[1].Data.animation.Data.name."$value"="draw"' "$scratch/animation.json" | jq -e -f "$filter" | jq -e '.animationCount==2 and .animations==[{name:"draw",duration:1.25},{name:"draw",duration:3}]' >/dev/null
jq '.Data.RootChunk.deep = (reduce range(25) as $i ({"DepotPath":{"$type":"ResourcePath","$storage":"string","$value":"test\\new.suffix"}}; {nested:.}))' "$scratch/material.json" | jq -e -f "$filter" | jq -e '.depotReferences|index("test\\new.suffix")!=null' >/dev/null

expect_rejected() {
  local fixture=$1 mutation=$2
  jq "$mutation" "$scratch/$fixture.json" > "$scratch/bad.json"
  if jq -e -f "$filter" "$scratch/bad.json" > "$scratch/bad-output" 2> "$scratch/error"; then
    printf 'FAIL: accepted malformed %s: %s\n' "$fixture" "$mutation" >&2;exit 1
  fi
  test ! -s "$scratch/bad-output"
}
expect_rejected animation 'del(.Data.RootChunk.animations)'
expect_rejected animation 'del(.Data.RootChunk.animations[1].Data.animation.Data.name)'
expect_rejected animation 'del(.Data.RootChunk.animations[1].Data.animation.Data.duration)'
expect_rejected animation '.Data.RootChunk.animations[0].Data.animation.Data.duration=-1'
expect_rejected animation '.Data.RootChunk."$type"="unknown"'
expect_rejected material 'del(.Data.RootChunk.materialEntries)'
expect_rejected material 'del(.Data.RootChunk.materialEntries[0].name)'
expect_rejected material 'del(.Data.RootChunk.localMaterialBuffer.materials[0].baseMaterial.DepotPath."$value")'
expect_rejected material '.Data.RootChunk.localMaterialBuffer.materials[0].baseMaterial.DepotPath."$value"=42'
printf 'PASS: wrapped fields, complete lists, deep/unknown suffix references, explicit unresolved hashes, nine malformed-input rejections\n'

if (( $# == 2 )); then
  copied=$1
  expected=$2
  jq -e -f "$filter" "$copied/receiver.anims.json" > "$scratch/real-animations.json"
  jq -e -f "$filter" "$copied/receiver.mesh.json" > "$scratch/real-materials.json"
  jq -S '.animations' "$scratch/real-animations.json" > "$scratch/actual-animations"
  jq -S '.' "$expected/animations.json" | cmp - "$scratch/actual-animations"
  jq -S '.depotReferences' "$scratch/real-materials.json" > "$scratch/actual-references"
  jq -S '.' "$expected/depot-references.json" | cmp - "$scratch/actual-references"
  jq -e '.materialCount==21 and (.materials|length)==21 and (.depotReferences|length)==24 and .unresolvedDepotReferences==[] and (.depotReferences|index("engine\\materials\\metal_base.remt")!=null)' "$scratch/real-materials.json" >/dev/null
  printf 'PASS: preserved Lynx copies match every golden animation name/duration and all 24 depot paths; all 21 material entries retained\n'
fi
