#!/usr/bin/env bash
# ТОЧКА СВОДА ОДНОЙ КОМАНДОЙ (05.09, мандат ускорения): сборка свода и приборы точки по порядку —
# свод → манифест → ширина вопроса → состав палаты → перепись копий → удержанный ключ →
# воспроизводимость (после свода: свод есть цель генератора и обязан совпасть) → подпись.
# Полный набор судов (courts.sh, ~45 мин) — отдельно: scripts/point.sh --suite. Под nohup:
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
  bash scripts/courts.sh | tail -3
fi
if [ "$FELL" = 0 ]; then echo "ТОЧКА PASS: все приборы точки целы"; exit 0; fi
echo "ТОЧКА FAIL: пало приборов $FELL"; exit 1
