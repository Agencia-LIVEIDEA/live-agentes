#!/usr/bin/env bash
# Baixa a ÚLTIMA versão do design system LIVEIDEA (branch main do repositório no GitHub)
# para um cache local e monta o kit de aplicação (CSS, fontes, valores para Office).
#
# Uso:
#   bash sync_ds.sh                    # clona ou atualiza o cache a partir da main e monta o kit
#   bash sync_ds.sh --from-zip X.zip   # sem acesso ao GitHub: usa o ZIP baixado da main (Code > Download ZIP)
#   bash sync_ds.sh --local DIR        # usa uma pasta (conteúdo da main lido pelo conector, ou teste local)
#   bash sync_ds.sh --snapshot         # ÚLTIMO CASO: cópia que veio no ZIP da skill (só com consentimento do usuário)
#
# Variáveis opcionais:
#   LIVEIDEA_DS_REPO   URL do repositório (padrão: https://github.com/Agencia-LIVEIDEA/id-liveidea.git)
#   LIVEIDEA_DS_BRANCH branch de referência (padrão: main)
#   LIVEIDEA_DS_CACHE  pasta do cache (padrão: ~/.cache/id-liveidea)
#
# Saída (stdout, uma por linha, para ler com `eval` ou copiar):
#   DS_ROOT, DS_DIR, DS_KIT, DS_VERSION, DS_DATE, DS_COMMIT, DS_SOURCE, DS_LATEST_TAG
# Código de saída: 0 ok · 2 sem acesso ao repositório · 3 repositório inconsistente

set -euo pipefail
# No Windows o Python lê arquivos em cp1252 por padrão; força UTF-8 (tokens.json, CHANGELOG, READMEs).
export PYTHONUTF8=1

REPO="${LIVEIDEA_DS_REPO:-https://github.com/Agencia-LIVEIDEA/id-liveidea.git}"
BRANCH="${LIVEIDEA_DS_BRANCH:-main}"
CACHE="${LIVEIDEA_DS_CACHE:-$HOME/.cache/id-liveidea}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="git"; ARG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --from-zip) MODE="zip"; ARG="${2:?informe o arquivo .zip}"; shift 2 ;;
    --local)    MODE="local"; ARG="${2:?informe a pasta do checkout}"; shift 2 ;;
    --snapshot) MODE="snapshot"; shift ;;
    -h|--help)  sed -n 2,20p "$0"; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; exit 1 ;;
  esac
done

log() { echo "[liveidea-ds] $*" >&2; }
mkdir -p "$CACHE"
ROOT=""; COMMIT="desconhecido"; SOURCE=""; LATEST_TAG=""

case "$MODE" in
  git)
    ROOT="$CACHE/repo"
    try_git() {
      if [ -d "$ROOT/.git" ]; then
        git -C "$ROOT" remote set-url origin "$REPO" &&
        git -C "$ROOT" fetch --quiet --depth 1 origin "$BRANCH" &&
        git -C "$ROOT" checkout --quiet -B "$BRANCH" FETCH_HEAD &&
        git -C "$ROOT" reset --quiet --hard FETCH_HEAD
      else
        rm -rf "$ROOT" && git clone --quiet --depth 1 --branch "$BRANCH" "$REPO" "$ROOT"
      fi
    }
    try_gh() {
      command -v gh >/dev/null 2>&1 || return 1
      local slug; slug="$(echo "$REPO" | sed -E 's#^https://github.com/##; s#\.git$##')"
      rm -rf "$ROOT" && gh repo clone "$slug" "$ROOT" -- --quiet --depth 1 --branch "$BRANCH"
    }
    if try_git 2>/dev/null; then :; elif try_gh 2>/dev/null; then :; else
      log "Sem acesso ao repositório $REPO (branch $BRANCH)."
      log "Opções: conectar o GitHub (git/gh autenticado ou conector GitHub) ou rodar com --from-zip <zip da main>."
      log "Não aplique o design system de memória."
      exit 2
    fi
    COMMIT="$(git -C "$ROOT" rev-parse --short HEAD)"
    SOURCE="github:$BRANCH"
    LATEST_TAG="$(git ls-remote --tags --refs "$REPO" 'v*' 2>/dev/null | sed 's#.*refs/tags/##' | sort -V | tail -1 || true)"
    ;;
  zip)
    [ -f "$ARG" ] || { log "Arquivo não encontrado: $ARG"; exit 1; }
    rm -rf "$CACHE/zip" && mkdir -p "$CACHE/zip"
    python3 -I -c 'import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' "$ARG" "$CACHE/zip"
    ROOT="$(dirname "$(find "$CACHE/zip" -path '*/design-system/tokens.json' | head -1)")"
    ROOT="$(dirname "$ROOT")"
    SOURCE="zip:$(basename "$ARG")"
    ;;
  local)
    ROOT="$(cd "$ARG" && pwd)"
    COMMIT="$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo desconhecido)"
    SOURCE="local:$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo pasta)"
    log "ATENÇÃO: usando a pasta $ROOT, não o clone da main. Confirme que ela tem o conteúdo da main (conector GitHub) ou é teste de mudança ainda não mergeada."
    ;;
  snapshot)
    ROOT="$(cd "$HERE/.." && pwd)/snapshot"
    [ -f "$ROOT/design-system/tokens.json" ] || { log "Este pacote da skill não tem a cópia do design system (snapshot/)."; exit 2; }
    SNAP="$(cat "$ROOT/VERSION" 2>/dev/null || echo 'versão não registrada')"
    COMMIT="$(echo "$SNAP" | grep -oE '@[0-9a-f]{7,}' | tr -d @ || true)"; COMMIT="${COMMIT:-desconhecido}"
    SOURCE="copia-do-pacote"
    log "ÚLTIMO CASO: usando a cópia do design system que veio no pacote da skill ($SNAP)."
    log "Ela pode estar desatualizada em relação à main. Informe isso ao usuário e registre na entrega."
    ;;
esac

DS="$ROOT/design-system"
[ -f "$DS/tokens.json" ] && [ -f "$DS/README.md" ] || { log "design-system/ incompleto em $ROOT"; exit 3; }

# Versão: tokens.json (meta.release) e CHANGELOG.md precisam concordar.
VERSION="$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["meta"].get("release",""))' "$DS/tokens.json")"
CL_LINE="$(grep -m1 -E '^## [0-9]+\.[0-9]+\.[0-9]+' "$DS/CHANGELOG.md" 2>/dev/null || true)"
CL_VERSION="$(echo "$CL_LINE" | sed -E 's/^## ([0-9.]+).*/\1/')"
DATE="$(echo "$CL_LINE" | sed -E 's/^## [0-9.]+ · ?//')"
if [ -n "$CL_VERSION" ] && [ "$CL_VERSION" != "$VERSION" ]; then
  log "INCONSISTÊNCIA: tokens.json diz $VERSION e CHANGELOG.md diz $CL_VERSION. Avise o responsável pelo design system."
  exit 3
fi
if [ -n "$LATEST_TAG" ] && [ "$LATEST_TAG" != "v$VERSION" ]; then
  log "Aviso: a main está na $VERSION e a última tag é $LATEST_TAG (tag pendente ou main à frente). Vale a main."
fi

KIT="$CACHE/kit"
# fontTools + brotli leem os nomes de fonte que o Office usa e convertem woff2 -> otf/ttf.
python3 -c "import fontTools, brotli" 2>/dev/null || pip install --quiet fonttools brotli >/dev/null 2>&1 ||
  log "Aviso: sem fonttools/brotli. Nomes de fonte do Office serão estimados; confira no office.json."
python3 "$HERE/build_kit.py" --ds "$DS" --out "$KIT" --commit "$COMMIT" --source "$SOURCE" >&2

cat <<EOF
DS_ROOT=$ROOT
DS_DIR=$DS
DS_KIT=$KIT
DS_VERSION=$VERSION
DS_DATE="$DATE"
DS_COMMIT=$COMMIT
DS_SOURCE=$SOURCE
DS_LATEST_TAG=$LATEST_TAG
EOF
