#!/usr/bin/env bash
# Build only original adapter code against an existing toolkit; no NuGet sources.
set -euo pipefail
if [[ ${1:-} == --help || $# -lt 4 ]]; then
  printf '%s\n' 'Usage: native-animation.sh export NATIVE RIG NEW.glb [CLIP]' \
    '       native-animation.sh import NATIVE RIG PREPARED.glb NEW.anims' \
    'Required: WOLVENKIT_ROOT, DOTNET_SDK (.NET 10 executable), NATIVE_ANIMATION_WORK (private build directory).' \
    'Optional: DOTNET_RUNTIME (defaults to DOTNET_SDK). Only WolvenKit 9.0.1 is supported.'
  [[ ${1:-} == --help ]] && exit 0
  exit 2
fi
: "${WOLVENKIT_ROOT:?Set WOLVENKIT_ROOT to an existing WolvenKit Console Linux 9.0.1 directory}"
: "${DOTNET_SDK:?Set DOTNET_SDK to an existing .NET 10 SDK dotnet executable}"
: "${NATIVE_ANIMATION_WORK:?Set NATIVE_ANIMATION_WORK to a private build directory}"
native_source="$(cd -- "$(dirname -- "$0")" && pwd)"
native_wkit="$(realpath -- "$WOLVENKIT_ROOT")"
native_sdk="$(realpath -- "$DOTNET_SDK")"
native_runtime="$(realpath -- "${DOTNET_RUNTIME:-$native_sdk}")"
native_work="$(realpath -m -- "$NATIVE_ANIMATION_WORK")"
[[ "$native_work" != "$native_source" && "$native_work" != "$native_source/"* ]] || { printf 'Build directory must be outside the published source.\n' >&2; exit 2; }
[[ -x "$native_sdk" && -x "$native_runtime" ]] || { printf 'SDK/runtime executables are missing.\n' >&2; exit 2; }
for native_dll in WolvenKit.RED4 WolvenKit.Core WolvenKit.Common WolvenKit.Modkit SharpGLTF.Core; do
  [[ -f "$native_wkit/$native_dll.dll" ]] || { printf 'Missing assembly: %s\n' "$native_dll" >&2; exit 2; }
done
mkdir -p -- "$native_work"
export DOTNET_CLI_HOME="$native_work/dotnet-home"
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
[[ $("$native_sdk" --version) == 10.* ]] || { printf 'An existing .NET 10 SDK is required.\n' >&2; exit 2; }
cat > "$native_work/NuGet.Config" <<'XML'
<configuration><packageSources><clear /></packageSources></configuration>
XML
if ! "$native_sdk" build "$native_source/NativeAnimation.csproj" --nologo \
  --configfile "$native_work/NuGet.Config" -p:NuGetAudit=false \
  -p:WKit="$native_wkit" -p:BaseIntermediateOutputPath="$native_work/obj/" \
  -p:OutputPath="$native_work/bin/" > "$native_work/build.log" 2>&1; then
  cat "$native_work/build.log" >&2
  exit 1
fi
export LD_LIBRARY_PATH="$native_wkit${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$native_runtime" "$native_work/bin/NativeAnimation.dll" "$native_wkit" "$@"
