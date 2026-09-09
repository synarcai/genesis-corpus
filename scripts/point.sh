#!/usr/bin/env bash
# ТОЧКА СВОДА ОДНОЙ КОМАНДОЙ (05.09, мандат ускорения): сборка свода и приборы точки по порядку —
# свод → манифест → ширина вопроса → состав палаты → перепись копий → удержанный ключ →
# воспроизводимость (после свода: свод есть цель генератора и обязан совпасть) → подпись.
# Полный набор судов (~45 мин) — отдельно: scripts/point.sh --suite. Под nohup:
# ПОД ЗАМКОМ НАБОР ГОНЯТЬ ЧЕРЕЗ scripts/suite.sh: он берёт имя со штампом времени
# (свой прогон не ждёт сам себя) и ЧИТАЕТ код 75 — «набор не запускался», который
# иначе молчит в логе до утра (шрам 07.09).
#   nohup bash scripts/point.sh > /tmp/point.txt 2>&1 &
# ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ (bash 3.2).
set -u
cd "$(dirname "$0")/.."
SUITE=0
for a in "$@"; do [ "$a" = "--suite" ] && SUITE=1; done
FELL=0
run() {
  local title="$1"; shift
  local out; out=$("$@" 2>&1); local rc=$?
  echo "== $title: $(printf '%s\n' "$out" | tail -1)"
  [ "$rc" = 0 ] || FELL=$((FELL + 1))
}
run "свод" python3 tools/gen_genesis_full.py
run "манифест" python3 scripts/manifest_court.py
run "ширина" python3 scripts/ask_width.py
run "состав" python3 scripts/panel_court.py
run "перепись копий" python3 scripts/copies_census.py
run "удержанный ключ" python3 scripts/holdout_key.py
run "воспроизводимость" python3 scripts/reproducible.py
echo "== подпись: sha $(shasum -a 256 datasets/GENESIS-FULL.txt | cut -c1-16), байт $(wc -c < datasets/GENESIS-FULL.txt | tr -d ' '), строк $(grep -c . datasets/GENESIS-FULL.txt)"
if [ "$SUITE" = 1 ]; then
  bash scripts/suite.sh | tail -3
fi
# ТОЧКА ЧИТАЕТ СЛЕД НАБОРА И ГОВОРИТ О НЁМ ВСЛУХ. Она не гоняет всего набора —
# на это есть `scripts/courts.sh`, — но и не смеет молчать о том, что о них НЕ ЗНАЕТ.
#
#     ТОЧКА, НЕ СКАЗАВШАЯ, КОГДА ХОДИЛ НАБОР, ОБЪЯВЛЯЕТ СВОД ЦЕЛЫМ ПО ВОСЬМИ ПРИБОРАМ ИЗ
#     СОТНИ С ЛИШНИМ И МОЛЧИТ ОБ ОСТАЛЬНЫХ.
#
# ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ: bash 3.2 (тот, что несёт macOS) кириллических идентификаторов
# не берёт вовсе — синтаксическая ошибка, а не предупреждение. Закон записан в наборе, страж
# его стоит там же (`bash32_court`), и он поймал эту самую правку в час, когда её писали.
#
#     ЗАКОН, ЗАПИСАННЫЙ В СОСЕДНЕМ ФАЙЛЕ, НЕ ЧИТАЕТСЯ САМ СОБОЮ: его читает СТРАЖ.
#
# След старее СУТОК или несущий падение роняет точку: свод, чьи приборы не звали сутки, не
# заверен, а лишь подписан.
TRACE=reports/SUITE-LAST.tsv
if [ -f "$TRACE" ]; then
  WHEN=$(cut -f1 "$TRACE"); VERDICT=$(cut -f2 "$TRACE"); FELL_N=$(cut -f3 "$TRACE"); TOTAL_N=$(cut -f4 "$TRACE")
  AGE_H=$(( ( $(date -u +%s) - $(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$WHEN" +%s 2>/dev/null || echo 0) ) / 3600 ))
  echo "== набор: $VERDICT (пало $FELL_N из $TOTAL_N), след ${AGE_H} ч назад — $WHEN"
  if [ "$VERDICT" != "ЦЕЛ" ]; then echo "== набор: СЛЕД НЕСЁТ ПАДЕНИЕ"; FELL=$((FELL+1)); fi
  if [ "$AGE_H" -gt 24 ]; then echo "== набор: СЛЕД СТАРШЕ СУТОК"; FELL=$((FELL+1)); fi
else
  echo "== набор: СЛЕДА НЕТ — набор не ходил ни разу"; FELL=$((FELL+1))
fi
if [ "$FELL" = 0 ]; then echo "ТОЧКА PASS: все приборы точки целы"; exit 0; fi
echo "ТОЧКА FAIL: пало приборов $FELL"; exit 1
