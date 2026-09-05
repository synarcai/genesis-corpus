#!/usr/bin/env bash
# ВОРОТА ПОСАДКИ ЧИТАТЕЛЯ — удержанный ключ на состоянии точки (05.09, holon: «свод спрашивает
# себя» засчитывает память; ворота переводятся на вопросы, которых свод не показывал).
#   состояние клонируется (ozar clone), N первых вопросов ключа (или все) отвечаются в --pipe,
#   судья — scripts/sweep_self.py judge (значение = конец ответа), вердикт — OUTDIR/verdict.tsv.
# usage: scripts/holdout_run.sh STATE OUTDIR [N] [KEY]
#   STATE — состояние точки (…/canon/FULL-<sha8>.state); OUTDIR — куда класть прогон;
#   N — сколько первых вопросов (по умолчанию все); KEY — ключ (по умолчанию datasets/HOLDOUT-KEY.tsv).
# Читатель: OZAR_CORE (иначе ozar-core с пути). ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ (bash 3.2).
set -u
OZAR_CORE="${OZAR_CORE:-ozar-core}"
# ДОБАВОЧНЫЕ ФЛАГИ ЧИТАТЕЛЯ (OZAR_FLAGS, например --fresh — сброс живой ленты на каждой строке pipe:
# один --pipe-прогон есть один диалог, и числа соседних строк ключа перетекали в ответы — holon, 05.09)
OZAR_FLAGS="${OZAR_FLAGS:-}"
cd "$(dirname "$0")/.."
if [ $# -lt 2 ]; then
  echo "usage: scripts/holdout_run.sh STATE OUTDIR [N] [KEY]"; exit 2
fi
STATE="$1"; OUT="$2"; N="${3:-0}"; KEY="${4:-datasets/HOLDOUT-KEY.tsv}"
if [ ! -f "$STATE" ] || [ ! -f "$KEY" ]; then
  echo "ВОРОТА ЧИТАТЕЛЯ ОТКАЗ: нет состояния или ключа ($STATE, $KEY)"; exit 2
fi
for side in lex pos schema; do
  [ -f "$STATE.$side" ] || { echo "ВОРОТА ЧИТАТЕЛЯ ОТКАЗ: у состояния нет сайдкара .$side"; exit 2; }
done
mkdir -p "$OUT"
# ЧИТАТЕЛЬ КОПИРУЕТСЯ К СЕБЕ ПЕРЕД ПРОГОНОМ (05.09): бинарь коллеги пересобирается на ходу, и
# прогон, начатый на одном хеше, кончался бы на другом — мера обязана знать, чем мерила.
cp "$OZAR_CORE" "$OUT/reader.bin" 2>/dev/null && chmod +x "$OUT/reader.bin" && OZAR_CORE="$OUT/reader.bin"
shasum -a 256 "$OZAR_CORE" | cut -c1-16 > "$OUT/reader.sha"
# N ВОПРОСОВ БЕРУТСЯ С ШАГОМ ПО ВСЕМУ КЛЮЧУ, А НЕ С НАЧАЛА: ключ упорядочен по языкам и домам,
# и первые N строк были бы одним языком (проба 05.09: 60 первых = 60 английских)
if [ "$N" -gt 0 ]; then
  # N ВОПРОСОВ С ШАГОМ ПО ВСЕМУ КЛЮЧУ, А НЕ С НАЧАЛА: ключ упорядочен по домам и языкам, и
  # первые N строк были бы одним языком (проба 05.09: 60 первых = 60 английских).
  python3 - "$KEY" "$N" > "$OUT/key.tsv" <<'PYEOF'
import sys
ключ, n = sys.argv[1], int(sys.argv[2])
строки = list(open(ключ, encoding="utf-8"))
шаг = max(1, len(строки) // n)
sys.stdout.writelines(строки[::шаг][:n])
PYEOF
else
  cp "$KEY" "$OUT/key.tsv"
fi
cut -f2 "$OUT/key.tsv" > "$OUT/questions.txt"
CLONE="$OUT/reader.state"
if [ ! -f "$CLONE" ]; then
  ozar clone --base "$STATE" --state "$CLONE" > "$OUT/clone.log" 2>&1 || { echo "ВОРОТА ЧИТАТЕЛЯ ОТКАЗ: клон не удался"; exit 2; }
fi
T0=$SECONDS
"$OZAR_CORE" 250 0 --state "$CLONE" --pipe --no-ask $OZAR_FLAGS < "$OUT/questions.txt" > "$OUT/run.out" 2> "$OUT/run.err"
echo "RUN EXIT $?"
python3 scripts/sweep_self.py judge "$OUT/key.tsv" "$OUT/run.out" --классов 12 \
  --метка "удержанный ключ ($(wc -l < "$OUT/key.tsv" | tr -d ' ') вопросов) на $(basename "$STATE")" \
  --в "$OUT/verdict.tsv" --секунд $((SECONDS - T0))
