# Read-only triage of WolvenKit JSON; no conversion, path resolution or fit verdict.
# Tested with WolvenKit 9.0.1 / WKitJsonVersion 0.0.9. Fail on unknown shapes.
def require($ok; $message):
  if $ok then . else error($message) end;
def cname:
  require(type == "object"; "missing typed name")
  | require(."$type" == "CName" and ."$storage" == "string"
      and (."$value" | type) == "string"; "name is not a decoded CName")
  | ."$value"
  | require(length > 0; "empty name");

.Data.RootChunk
| require(type == "object"; "missing Data.RootChunk")
| if ."$type" == "animAnimSet" then
    .animations
    | require(type == "array"; "missing animations array")
    | map(
        .Data.animation.Data
        | require(type == "object"; "missing wrapped animation data")
        | {name: (.name | cname), duration: .duration}
        | require((.duration | type) == "number" and .duration >= 0;
            "missing or invalid animation duration"))
    | {kind: "animations", animationCount: length, animations: .}
  elif ."$type" == "CMesh" then
    . as $root
    | .materialEntries
    | require(type == "array"; "missing materialEntries array")
    | map(
        require(type == "object"; "invalid material entry")
        | {name: (.name | cname), index, isLocalInstance}
        | require((.index | type) == "number" and .index >= 0
            and .index == (.index | floor); "invalid material index")
        | require(.isLocalInstance == 0 or .isLocalInstance == 1
            or (.isLocalInstance | type) == "boolean"; "unknown material ownership")) as $entries
    # Walk every explicit DepotPath, with no suffix whitelist, depth or result cap.
    | [$root | .. | objects | select(has("DepotPath")) | .DepotPath
        | require(type == "object"; "invalid DepotPath wrapper")
        | require(."$type" == "ResourcePath" and (."$storage" | type) == "string"
            and has("$value"); "unknown DepotPath schema")
        | require(."$storage" != "string" or (."$value" | type) == "string";
            "invalid string DepotPath")
        | {storage: ."$storage", value: ."$value"}] as $refs
    | {kind: "materials", materialCount: ($entries | length), materials: $entries,
       depotReferenceOccurrences: ($refs | length),
       depotReferences: ([$refs[] | select(.storage == "string" and .value != "") | .value] | unique),
       unresolvedDepotReferences: ([$refs[] | select(.storage != "string")] | unique),
       emptyDepotReferenceCount: ([$refs[] | select(.storage == "string" and .value == "")] | length)}
  else error("unsupported root type; expected animAnimSet or CMesh")
  end
