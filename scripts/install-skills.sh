#!/usr/bin/env bash
# Install these three sibling skills. Updates retain originals outside discovery.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
dest=${HOME:?}/.agents/skills
update=false
while (( $# )); do
    case $1 in
        --dest) (( $# >= 2 )) || exit 2; dest=$2; shift 2 ;;
        --update) update=true; shift ;;
        --help) printf 'Usage: bash scripts/install-skills.sh [--dest DIR] [--update]\n'; exit 0 ;;
        *) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
    esac
done
dest=$(realpath -m -- "$dest")
case "$dest/" in "$repo/skills/"*) printf 'Destination overlaps source skills.\n' >&2; exit 1 ;; esac
skills=(cyberpunk2077-modding weapon-animation-inspection cyberpunk2077-animation-retargeting)
same_skill() { diff -qr -x __pycache__ -x '*.pyc' -x '*.pyo' -- "$1" "$2"; }
unchanged=true
for skill in "${skills[@]}"; do
    [[ -f $repo/skills/$skill/SKILL.md ]]
    if [[ -e $dest/$skill || -L $dest/$skill ]]; then
        if ! $update; then printf 'Already exists: %s (use --update to back up and replace)\n' "$dest/$skill" >&2; exit 1; fi
    fi
    if ! same_skill "$repo/skills/$skill" "$dest/$skill" >/dev/null 2>&1; then unchanged=false; fi
done
if $unchanged; then printf 'Already current: %s\n' "$dest"; exit 0; fi
mkdir -p -- "$dest"
stage=$(mktemp -d "$dest/../.cyberpunk-skill-stage.XXXXXXXX")
backup=''
installed=() backed=()
success=false
cleanup() {
    status=$?
    trap - EXIT
    if ! $success; then
        for skill in "${installed[@]}"; do rm -rf -- "$dest/$skill"; done
        for skill in "${backed[@]}"; do mv -- "$backup/$skill" "$dest/$skill" || status=1; done
    fi
    rm -rf -- "$stage"
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Complete and compare all staged copies before changing any installed skill.
for skill in "${skills[@]}"; do
    cp -R -- "$repo/skills/$skill" "$stage/$skill"
    # Bytecode is generated locally and can embed private source paths.
    find "$stage/$skill" -type d -name __pycache__ -prune -exec rm -rf -- {} +
    find "$stage/$skill" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
    same_skill "$repo/skills/$skill" "$stage/$skill" >/dev/null
done
for skill in "${skills[@]}"; do
    if [[ -e $dest/$skill || -L $dest/$skill ]]; then
        if [[ -z $backup ]]; then
            mkdir -p -- "$dest/../skill-backups"
            backup=$(mktemp -d "$dest/../skill-backups/cyberpunk.XXXXXXXX")
            printf 'Preserved prior installation: %s\n' "$backup"
        fi
        mv -- "$dest/$skill" "$backup/$skill"
        backed+=("$skill")
    fi
    mv -- "$stage/$skill" "$dest/$skill"
    installed+=("$skill")
done
for skill in "${skills[@]}"; do same_skill "$repo/skills/$skill" "$dest/$skill" >/dev/null; done
success=true
printf 'Installed all three skills: %s\n' "$dest"
printf 'Use $cyberpunk2077-modding, $weapon-animation-inspection or $cyberpunk2077-animation-retargeting in Codex.\n'
