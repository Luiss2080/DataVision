#!/usr/bin/env bash
# Instala la suite SDD en un proyecto o en la carpeta de usuario.
# Uso: ./install.sh <ruta-proyecto> [--copy] [--agents-md]
#      ./install.sh --global [--copy]
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/skills"
SKILLS="spec-generator sdd-test-design sdd-implement sdd-validate"
COPY=0; AGENTS_MD=0; TARGET=""
for a in "$@"; do
  case "$a" in
    --copy) COPY=1 ;;
    --agents-md) AGENTS_MD=1 ;;
    --global) TARGET="$HOME" ;;
    *) TARGET="$a" ;;
  esac
done
[ -z "$TARGET" ] && { echo "Uso: ./install.sh <ruta-proyecto> [--copy] [--agents-md] | --global [--copy]"; exit 2; }

ref="$SRC/spec-generator/references/conventions.md"
for s in $SKILLS; do
  cmp -s "$ref" "$SRC/$s/references/conventions.md" || echo "AVISO: conventions.md difiere en $s"
done

mkdir -p "$TARGET/.agents/skills" "$TARGET/.claude/skills"
for s in $SKILLS; do
  rm -rf "$TARGET/.agents/skills/$s"
  cp -R "$SRC/$s" "$TARGET/.agents/skills/$s"
  rm -rf "$TARGET/.claude/skills/$s"
  if [ "$COPY" = 1 ]; then
    cp -R "$SRC/$s" "$TARGET/.claude/skills/$s"
  else
    ln -s "../../.agents/skills/$s" "$TARGET/.claude/skills/$s"
  fi
  echo "✓ $s"
done

if [ "$AGENTS_MD" = 1 ] && [ "$TARGET" != "$HOME" ]; then
  f="$TARGET/AGENTS.md"
  if ! grep -qs "## Spec-Driven Development" "$f"; then
    cat >> "$f" << 'BLOCK'

## Spec-Driven Development
Este proyecto sigue SDD. Antes de cualquier cambio en código, configuración,
dependencias, datos o infraestructura, usa la skill `spec-generator`.
Flujo: spec-generator → sdd-test-design → sdd-implement → sdd-validate.
Constitución: docs/constitution.md. Specs: docs/specs/.
Nunca modifiques archivos listados en un tests.lock.
BLOCK
    echo "✓ Bloque SDD añadido a AGENTS.md"
  else
    echo "· AGENTS.md ya tiene el bloque SDD"
  fi
fi
echo "Instalado en $TARGET"
