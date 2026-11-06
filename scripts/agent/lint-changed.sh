#!/usr/bin/env bash
# Ruff (lint + format) sur les seuls fichiers Python modifiés par rapport à la
# branche de base. Le dépôt n'est pas encore entièrement propre (erreurs ruff,
# fichiers non formatés) : on ne bloque l'agent que sur ce qu'il a touché.
#
# Indentation : le dépôt mélange fichiers à tabulations (voir .editorconfig) et
# fichiers à espaces. `ruff format` convertirait un fichier à tabulations en
# entier vers des espaces, ce qui noierait la revue : ces fichiers-là ne sont
# que lintés, pas formatés. Les fichiers à espaces et les nouveaux fichiers
# sont lintés et formatés.
#
# Usage : bash scripts/agent/lint-changed.sh [--check|--fix]   (défaut : --check)
# Env   : BASE_REF (défaut : origin/main)
set -euo pipefail

mode="${1:---check}"
base="${BASE_REF:-origin/main}"

mapfile -t files < <(
  {
    git diff --name-only --diff-filter=ACMR "$base" -- 2>/dev/null || true
    git ls-files --others --exclude-standard
  } | sort -u | grep -E '\.py$' | grep -v '/migrations/' || true
)

if [ "${#files[@]}" -eq 0 ]; then
  echo "Aucun fichier Python modifié à vérifier."
  exit 0
fi

format_files=()
for f in "${files[@]}"; do
  # Un fichier qui existe sur la branche de base et y est indenté en
  # tabulations garde son style.
  if git show "$base:$f" 2>/dev/null | grep -qP '^\t'; then
    continue
  fi
  format_files+=("$f")
done

printf 'Fichiers lintés :\n'
printf '  %s\n' "${files[@]}"
printf 'Fichiers formatés : %s sur %s (les autres sont indentés en tabulations)\n' \
  "${#format_files[@]}" "${#files[@]}"

if [ "$mode" = "--fix" ]; then
  ruff check --fix "${files[@]}"
  [ "${#format_files[@]}" -eq 0 ] || ruff format "${format_files[@]}"
else
  ruff check "${files[@]}"
  [ "${#format_files[@]}" -eq 0 ] || ruff format --check "${format_files[@]}"
fi
