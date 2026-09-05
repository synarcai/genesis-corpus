#!/usr/bin/env bash
# ВОРОТА ПОСАДКИ МИРА — свип вопросов ОДНОГО мира на ТЕКУЩЕМ читателе (05.09, слово
# владельца «прибор как ворота каждой посадки»; принято holon):
#   мир ложится, если его вопросы на текущем читателе не рождают ЛЖИ; немые —
#   план ковки (классы читателя), а не долг мира.
# Читатель не куётся: состояние точки клонируется (ozar clone) и открывается
# мгновенно; N вопросов отвечаются в --pipe; судья — scripts/sweep_self.py judge,
# вердикт пишется в OUTDIR/verdict.tsv (--в), latest.tsv точки не трогается.
#
# usage: scripts/sweep_world.sh WORLD.txt STATE N SEED OUTDIR
#   WORLD  — файл мира (datasets/genesis_x.txt); STATE — состояние точки
#            (~/projects/oldman/synarcai/canon/FULL-<sha8>.state); N — скелетов;
#   SEED   — семя выборки; OUTDIR — куда класть выборку, прогон и вердикт.
# ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ: bash 3.2 macOS кириллических не берёт.
# ЧИТАТЕЛЬ БЕРЁТСЯ ИЗ OZAR_CORE, ИНАЧЕ С ПУТИ: установленный бинарь может отстать от main
# (05.09: ~/.cargo/bin/ozar-core от 08:37 отвечал всему миру «not_mine: session-recall»,
# текущий main — сертификатами и честными отказами).
set -u
OZAR_CORE="${OZAR_CORE:-ozar-core}"
cd "$(dirname "$0")/.."
if [ $# -lt 5 ]; then
  echo "usage: scripts/sweep_world.sh WORLD.txt STATE N SEED OUTDIR"; exit 2
fi
WORLD="$1"; STATE="$2"; N="$3"; SEED="$4"; OUT="$5"
if [ ! -f "$WORLD" ] || [ ! -f "$STATE" ]; then
  echo "ВОРОТА МИРА ОТКАЗ: нет мира или состояния ($WORLD, $STATE)"; exit 2
fi
mkdir -p "$OUT"
python3 scripts/sweep_self.py gen "$WORLD" "$N" "$SEED" "$OUT" || exit 2
CLONE="$OUT/reader.state"
if [ ! -f "$CLONE" ]; then
  ozar clone --base "$STATE" --state "$CLONE" > "$OUT/clone.log" 2>&1 || { echo "ВОРОТА МИРА ОТКАЗ: клон не удался"; exit 2; }
fi
# СОСТОЯНИЕ ЕСТЬ ФАЙЛ С САЙДКАРАМИ (.lex .pos .schema): состояние без них читатель открывает
# и отвечает всему «not_mine: session-recall» (05.09 — симлинк на один файл вместо клона)
for side in lex pos schema; do
  [ -f "$CLONE.$side" ] || { echo "ВОРОТА МИРА ОТКАЗ: у состояния нет сайдкара .$side — клонируйте ozar clone, не копируйте один файл"; exit 2; }
done
"$OZAR_CORE" 250 0 --state "$CLONE" --pipe --no-ask < "$OUT/sweep_q.txt" > "$OUT/run.out" 2> "$OUT/run.err"
echo "RUN EXIT $?"
python3 scripts/sweep_self.py judge "$OUT/sweep_key.tsv" "$OUT/run.out" --классов 12 \
  --метка "мир $(basename "$WORLD") на $(basename "$STATE")" --в "$OUT/verdict.tsv"
