#!/bin/bash
# Renderiza os blocos de animação (PNG com transparência) em hf/out/bNN.
# Uso (na pasta videos/NN-tema/work/hf):  bash render_blocos.sh 01 02 03 ...
# Dica: rode duas filas em paralelo (metade dos blocos em cada) para ir mais rápido.
cd "$(dirname "$0")"
KIT="$(cd ../../../.. && pwd)"
HF="$KIT/ferramentas/hyperframes"
for b in "$@"; do
  d=blocks/b$b; rm -rf "$d" out/b$b; mkdir -p "$d/assets"
  cp mg_b$b.html "$d/index.html"; cp assets/* "$d/assets/"; cp hyperframes.json "$d/"
  cp -r cut panels "$d/"
  (cd "$d" && npx --prefix "$HF" hyperframes render --format png-sequence -o ../../out/b$b -w 4 > ../../render_b$b.log 2>&1)
  echo "b$b: $(ls out/b$b 2>/dev/null | wc -l) quadros"
done
