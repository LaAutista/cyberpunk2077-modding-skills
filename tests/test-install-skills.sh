#!/usr/bin/env bash
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
scratch=$(mktemp -d)
fixture_cache="$repo/skills/cyberpunk2077-modding/scripts/setup/__pycache__/installer-fixture.pyc"
[[ ! -e $fixture_cache ]]
mkdir -p -- "$(dirname -- "$fixture_cache")"
printf 'generated fixture cache\n' > "$fixture_cache"
trap 'rm -f -- "$fixture_cache"; rm -rf -- "$scratch"' EXIT
dest=$scratch/agent/skills
run() { bash "$repo/scripts/install-skills.sh" --dest "$dest" "$@"; }
run
for skill in cyberpunk2077-modding weapon-animation-inspection; do diff -qr -x __pycache__ -x '*.pyc' -x '*.pyo' "$repo/skills/$skill" "$dest/$skill" >/dev/null; done
[[ -f $dest/cyberpunk2077-modding/scripts/setup/provision.mjs ]]
[[ -f $dest/cyberpunk2077-modding/scripts/comparison/diagnostic-dependencies.json ]]
[[ -z $(find "$dest" -type d -name __pycache__ -print -quit) ]]
if run >"$scratch/reject.log" 2>&1; then printf 'Existing install was not rejected.\n' >&2; exit 1; fi
run --update
[[ ! -e $scratch/agent/skill-backups ]]
mkdir "$dest/unrelated"
printf 'keep\n' > "$dest/unrelated/settings"
printf 'custom\n' > "$dest/cyberpunk2077-modding/local-note.md"
run --update
mapfile -t backups < <(find "$scratch/agent/skill-backups" -mindepth 1 -maxdepth 1 -type d)
[[ ${#backups[@]} == 1 ]]
[[ $(cat "${backups[0]}/cyberpunk2077-modding/local-note.md") == custom ]]
[[ ! -e $dest/cyberpunk2077-modding/local-note.md ]]
[[ $(cat "$dest/unrelated/settings") == keep ]]
# Force a failure between promoting the two folders; both old copies must return.
printf 'rollback\n' > "$dest/cyberpunk2077-modding/local-note.md"
cp -R "$dest" "$scratch/expected"
mkdir "$scratch/bin"
real_mv=$(command -v mv)
cat > "$scratch/bin/mv" <<'SH'
#!/usr/bin/env bash
for arg in "$@"; do
    case $arg in */.cyberpunk-skill-stage.*/weapon-animation-inspection) exit 91 ;; esac
done
exec "$REAL_MV" "$@"
SH
chmod +x "$scratch/bin/mv"
if REAL_MV="$real_mv" PATH="$scratch/bin:$PATH" run --update >"$scratch/rollback.log" 2>&1; then exit 1; fi
diff -qr "$scratch/expected" "$dest" >/dev/null
if bash "$repo/scripts/install-skills.sh" --dest "$repo/skills" --update >"$scratch/overlap.log" 2>&1; then exit 1; fi
printf 'PASS: install, explicit update, no-op, backup, unrelated files, rollback and source-overlap rejection.\n'
