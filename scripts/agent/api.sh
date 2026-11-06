#!/usr/bin/env bash
# Appelle l'API locale (lancée par start-app.sh) pour vérifier un endpoint.
# Seule l'app locale est joignable : l'URL de base est figée et le chemin
# validé, ce qui permet d'autoriser ce script aux agents sans leur ouvrir le
# réseau.
#
# Usage : bash scripts/agent/api.sh [--as demo-admin|demo-author|demo-reader] METHODE /chemin [corps-json]
#   bash scripts/agent/api.sh GET /api/v1/fanfics/
#   bash scripts/agent/api.sh --as demo-author GET /api/v1/accounts/user/
#   bash scripts/agent/api.sh --as demo-reader POST /api/v1/accounts/like/ '{"id":1}'
#
# Authentification : jeton JWT obtenu sur /api/auth/token/ avec le mot de passe de
# démo, envoyé en `Authorization: Bearer`.
# La réponse est affichée et copiée dans .agent-out/api/last.json.
set -euo pipefail

BASE_URL=http://127.0.0.1:8000
PASSWORD=demo-password-123
user=""

if [ "${1:-}" = "--as" ]; then
  user="${2:-}"
  shift 2
fi
method="${1:-}"
path="${2:-}"
body="${3:-}"

usage() {
  sed -n '7,10p' "$0" >&2
  exit 2
}

case "$user" in
  "" | demo-admin | demo-author | demo-reader) ;;
  *) echo "Compte inconnu : $user (demo-admin, demo-author ou demo-reader)" >&2; exit 2 ;;
esac
case "$method" in
  GET | POST | PUT | PATCH | DELETE | OPTIONS) ;;
  *) usage ;;
esac
if ! [[ "$path" =~ ^/[A-Za-z0-9._~/?\&=%+,-]*$ ]] || [[ "$path" == //* ]]; then
  echo "Chemin invalide : $path (doit commencer par /, sans hôte)" >&2
  exit 2
fi

mkdir -p .agent-out/api
args=(-sS -X "$method" -H 'Accept: application/json' -o .agent-out/api/last.json -w '%{http_code}')
if [ -n "$user" ]; then
  token=$(curl -sS -X POST -H 'Content-Type: application/json' \
    --data-binary "{\"username\":\"$user\",\"password\":\"$PASSWORD\"}" \
    -- "$BASE_URL/api/auth/token/" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("access", ""))
except ValueError:
    pass')
  if [ -z "$token" ]; then
    echo "Impossible d'obtenir un jeton pour $user (seed_demo a-t-il tourné ?)" >&2
    exit 1
  fi
  args+=(-H "Authorization: Bearer $token")
fi
if [ -n "$body" ]; then
  args+=(-H 'Content-Type: application/json' --data-binary "$body")
fi

status=$(curl "${args[@]}" -- "$BASE_URL$path")
echo "HTTP $status — $method $path${user:+ (en tant que $user)}"
python3 -m json.tool .agent-out/api/last.json 2>/dev/null | head -c 8000 || head -c 4000 .agent-out/api/last.json
echo
