#!/usr/bin/env bash
# ПОСАДКА МИРА ОДНОЙ КОМАНДОЙ (05.09, мандат ускорения разработки): генератор через ворота палаты,
# затем суд мира (подсадки + свой мир), итог одной строкой; для долгих миров — под nohup:
#   nohup bash scripts/land_world.sh tools/gen_genesis_x.py courts/x_court.py > /tmp/land_x.txt 2>&1 &
# usage: scripts/land_world.sh GENERATOR [COURT]
# ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ (bash 3.2).
set -u
cd "$(dirname "$0")/.."
if [ $# -lt 1 ]; then echo "usage: scripts/land_world.sh GENERATOR [COURT]"; exit 2; fi
GEN="$1"; COURT="${2:-}"
if [ ! -f "$GEN" ]; then echo "ПОСАДКА ОТКАЗ: генератора нет ($GEN)"; exit 2; fi
T0=$SECONDS
python3 "$GEN"; RC=$?
if [ "$RC" != 0 ]; then echo "ПОСАДКА FAIL: ворота не пустили $GEN (rc=$RC, $((SECONDS - T0)) с)"; exit 1; fi
if [ -n "$COURT" ]; then
  if [ ! -f "$COURT" ]; then echo "ПОСАДКА ОТКАЗ: суда нет ($COURT)"; exit 2; fi
  OUT=$(python3 "$COURT" 2>&1); RC=$?
  echo "$OUT" | tail -1
  if [ "$RC" != 0 ]; then echo "ПОСАДКА FAIL: суд $COURT пал (rc=$RC, $((SECONDS - T0)) с)"; exit 1; fi
fi
echo "ПОСАДКА PASS: $GEN${COURT:+ + $COURT} за $((SECONDS - T0)) с"
