#!/usr/bin/env bash
# СУДЫ КОРПУСА — все приборы разом, одним вердиктом.
#
# Всякий суд обязан быть НУЛЁМ: корпус, растящий исследователя, не
# вправе нести ни одного проверяемого утверждения, которое не сходится.
# Осанка та же, что в парке архитектуры: 0 чисто, 1 есть находка,
# 2 отказ судить.
#
# ИМЕНА ПЕРЕМЕННЫХ ЛАТИНИЦЕЙ: bash 3.2 (тот, что несёт macOS)
# кириллических идентификаторов не берёт вовсе — синтаксическая ошибка,
# а не предупреждение. Этот самый файл был написан с «СУДЫ=(...)» и
# упал, потому что страж, ловящий такое, оставался в другом репозитории;
# теперь он здесь.
set -u
cd "$(dirname "$0")/.."
COURTS=("courts/arith_court.py" "courts/algo_court.py"
        "courts/formula_court.py" "courts/logic_court.py"
        "courts/physics_court.py" "courts/cyber_court.py"
        "courts/agreement_court.py" "courts/notation_court.py"
        "courts/unit_court.py" "courts/number_court.py" "courts/inquiry_court.py" "courts/surfaces_court.py" "courts/markdown_court.py" "courts/doctree_court.py" "courts/rates_court.py" "courts/formula_lang_court.py" "courts/percent_court.py" "courts/average_court.py" "courts/equation_court.py" "courts/dataformat_court.py" "courts/everyday_court.py" "courts/story_chain_court.py" "courts/age_court.py" "courts/halves_court.py" "courts/inquiry_de_fr_court.py" "courts/ru_conversion_court.py" "courts/selfmeasure_court.py"
        "courts/ru_compare_court.py" "courts/ru_story_court.py" "courts/inquiry_es_it_court.py" "courts/share_court.py" "courts/compare_mult_court.py" "courts/sequence_court.py"
        "courts/geometry_court.py" "courts/linalg_court.py"
        "courts/calendar_court.py" "courts/speech_court.py"
        "courts/rugram_court.py" "courts/physlaw_court.py"
        "courts/compsci_court.py" "courts/case_court.py"
        "courts/valence_court.py"
        "scripts/shadow_court.py"
        "scripts/syllabus_court.py" "scripts/richness_court.py"
        "scripts/langpack_court.py" "courts/langrule_court.py"
        "scripts/claims_court.py"
        "courts/program_court.py" "courts/statistics_court.py"
        "courts/proof_court.py" "courts/machine_court.py"
        "courts/episode_court.py" "courts/copula_court.py"
        "courts/markup_court.py" "courts/langlayer_court.py"
        "courts/langform_court.py"
        "tools/gsm_census.py --court"
        "scripts/reproducible.py" "scripts/bash32_court.py"
        "scripts/manifest_court.py" "scripts/prose_court.py" "tools/mutants.py" "scripts/lexicon_reach.py"
        "courts/inquiry_pt_nl_court.py" "courts/inquiry_pl_tr_court.py"
        "courts/metalang_court.py" "courts/glyph_court.py" "courts/space_court.py" "courts/stenogram_court.py"
        "courts/mathspaces_court.py" "courts/gsmforms_court.py" "courts/definitions_court.py" "courts/pronoun_court.py" "courts/money_court.py" "courts/holes_court.py" "courts/money_langs_court.py" "courts/geometry_langs_court.py" "courts/units_langs_court.py" "courts/stats_langs_court.py" "courts/calendar_langs_court.py" "courts/sequences_langs_court.py" "courts/compare_langs_court.py" "courts/share_langs_court.py" "courts/physics_langs_court.py"
        "courts/relation_court.py"
        "scripts/court_mutants.py" "scripts/panel_court.py"
        "scripts/concept_reach.py"
        "scripts/ask_reach.py" "scripts/band_reach.py" "scripts/biblio_reach.py" "courts/ruverbs_court.py" "courts/script_court.py" "scripts/word_mutants.py" "scripts/shelf_court.py" "scripts/ask_width.py" "courts/notationvar_court.py"
        "courts/prosetree_court.py" "courts/longdiv_court.py"
        "scripts/form_census.py" "scripts/verbthings_court.py"
        "scripts/coverage.py"
        # ДОМА РАЗГОВОРА И РАССУЖДЕНИЯ (04.09). Их суды жили в палате и стерегли
        # ВОРОТА, но в этом списке не стояли, и потому вердикт «пало 0 из 103»
        # их не считал — ноль с укороченным знаменателем (М-264). Считает.
        "courts/behavior_court.py" "courts/topics_court.py" "courts/nature_court.py" "courts/links_court.py" "courts/scale_court.py" "courts/opposites_court.py" "courts/roles_court.py" "courts/joints_court.py" "courts/dialogue_court.py" "courts/worldfacts_court.py" "courts/infer_court.py" "scripts/circle_probe.py" "scripts/agree_probe.py" "scripts/shelf_declare.py" "scripts/house_reach.py" "scripts/head_census.py" "scripts/form_matrix.py"
        # …и четыре дома рассуждения, севшие 04.09 после снятия заморозки
        "courts/disj_court.py" "courts/indu_court.py" "courts/analog_court.py" "courts/reply_court.py"
        # ПАРА РЕГИСТРА — условие ПОКУПКИ, названное holon: вежливая строка обязана
        # отличаться от неформальной только обращением, иначе анти-унификация
        # вынесет в дыру лишнее и закон выйдет шире дома. Рубеж 0 пороков.
        "scripts/register_pairs.py"
        # ЧИСТОТА РЕГИСТРА — поверка с обратной стороны: не говорит ли
        # НЕФОРМАЛЬНАЯ рамка вежливыми словами. Прибор пары этого не видит:
        # он сличает написанное, а здесь беда в ненаписанном.
        "scripts/register_purity.py"
        # ЛОВУШКА НАЧАЛА — суд, зовущий строку ложной по её НАЧАЛУ, молчит до
        # дня, когда сосед напишет первую такую строку, и тогда ломает СОСЕДА.
        # Сличением показов не виден: показов, которые его тронут, ещё нет.
        "scripts/prefix_traps.py"
        # ПЕРЕПИСЬ ПОРОГОВ — пай аудита «меры и пороги»: всякое число в роли
        # рубежа с ответом «объявлено / храповик / вкус». Печатает число, не падает.
        "scripts/threshold_census.py"
        # ЧИСЛО БЕЗ ЗНАМЕНАТЕЛЯ — последняя строка каждого прибора леджера: сказано
        # ли, из скольких. Ноль без объёма — FAIL (закон holon).
        "scripts/denominator_census.py"
        # ПЕРЕПИСЬ ПОВТОРОВ — сколько строк свода суть точные копии (05.09: 50 %,
        # сверх LAW 40 %). Число, а не рубеж: потолок повтора — решение владельца.
        "scripts/repeat_census.py --свод"
        # СЛЕД РАЗБОРА ОПРЕДЕЛЕНИЙ — где разбор статьи остановился на каждом
        # понятии без определения; причина, не названная прибором, — FAIL.
        "scripts/definitions_reach.py"
        # ПЕРЕПИСЬ КОПИЙ — потолок LAW читается обратно: ни один показ мира через слой
        # не стоит больше LAW раз (М-402); сайдкар datasets/COPIES.tsv — суду кворума.
        "scripts/copies_census.py"
        # СВОД СПРАШИВАЕТ СЕБЯ — последний свип точки (reports/sweep/latest.tsv): ложь = 0;
        # немые классы — план следующей точки. Набор читает вердикт, не куёт.
        "scripts/sweep_self.py roster"
        # ДОСЯГАЕМОСТЬ СУДА (М-404) — вся палата по всем мирам показов: суд, выросший
        # головами или образцами после записи мира, судит его здесь, а не у чужих ворот.
        "scripts/court_reach.py"
        # УДЕРЖАННЫЙ КЛЮЧ — вопросы, которых свод не показывал: формы дома SVAMP с числами вне
        # таблиц дома; 0 прожитых строк; переписывается на каждой точке (ворота посадки читателя).
        "scripts/holdout_key.py"
        # МЕРА ДЕЙСТВИЯ — число меряет действие или считает носителей (род d5, 05.09)
        "courts/holdforms_court.py" "courts/cmpframes_court.py" "courts/sceneforms_court.py" "courts/toolforms_court.py" "courts/action_measure_court.py" "courts/numberline_court.py" "courts/countfacts_court.py" "courts/letters_court.py" "courts/propcompare_court.py" "courts/price_court.py" "courts/translate_court.py" "courts/timeunits_court.py" "courts/svamp_court.py" "courts/measure_langs_court.py")
# ПРИБОРЫ ИДУТ ПАЧКАМИ, А ВЕРДИКТ ОСТАЁТСЯ ОДНОЙ ЛЕНТОЙ (05.09).
#
# Набор шёл в один поток — 70 минут по меткам леджера на 144 прибора, — и точка
# ждала его одна. Приборы не зависят друг от друга: каждый читает корпус и пишет
# СВОЙ файл (перепись копий — COPIES.tsv, ключ — HOLDOUT-KEY, свип — свой вердикт),
# и единственное общее место было reports/ledger.tsv. Потому:
#
#   · рабочие НЕ ПИШУТ В ЛЕДЖЕР — они складывают вывод, код и время в свои
#     временные файлы, а строку леджера пишет РОДИТЕЛЬ, когда собирает пачку;
#   · вывод печатается В ИСХОДНОМ ПОРЯДКЕ СПИСКА, пачка за пачкой: чересполосицы
#     нет, а ход виден по мере готовности пачки, как и прежде;
#   · число рабочих — GENESIS_SUITE_JOBS, по умолчанию ЧЕТВЕРТЬ ядер: палата в
#     каждом процессе держит память, и щедрость здесь стоила дня — четыре ковки
#     точки умерли от исчерпания подкачки, когда рядом жили тяжёлые процессы.
#
# ПРИБОРЫ, КОТОРЫЕ ГОНЯТСЯ ОДНИ, названы поимённо и с причиной (SOLO): их бег
# рядом с другими есть переподписка машины, а не ускорение.
SOLO=("scripts/reproducible.py"   # разворачивает зеркало дерева и гоняет 139 порождателей
      "scripts/prose_court.py"    # сам параллелит палату по 207 мирам прозы (306 МБ)
      "courts/prosetree_court.py" # тот же корпус прозы, разбор дерева
      "scripts/court_reach.py"    # вся палата по всем мирам показов (292 тысячи строк)
      "courts/arith_court.py")    # самый долгий суд корпуса: 167 миров построчно

# ЧИСЛО РАБОЧИХ УСТУПАЕТ НАГРУЗКЕ МАШИНЫ, И ЭТО ЗАМЕРЕНО, А НЕ УГАДАНО.
# Малый набор из двенадцати приборов на машине с load average 99 при 16 ядрах:
# один поток 176 с, пачки по четыре — 282 с. Переподписанная машина от новых
# процессов не ускоряется, а глохнет: они делят ту же память и ту же подкачку
# (в тот час её было занято 33 ГБ из 35, и четыре ковки точки умерли от этого).
# Потому по умолчанию берётся четверть ядер, но не больше свободных по load
# average, а при нагрузке выше числа ядер — один рабочий. GENESIS_SUITE_JOBS,
# если объявлен, слушается: зовущий знает, чем занята машина.
JOBS="${GENESIS_SUITE_JOBS:-}"
if [ -z "$JOBS" ]; then
  CORES=$(sysctl -n hw.ncpu 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)
  JOBS=$((CORES / 4))
  LOAD=$(uptime | sed 's/.*averages*: *//; s/[ ,].*//' | cut -d. -f1)
  case "$LOAD" in ''|*[!0-9]*) LOAD=0 ;; esac
  if [ "$LOAD" -gt "$CORES" ]; then
    JOBS=1
  else
    FREE=$((CORES - LOAD))
    [ "$FREE" -lt "$JOBS" ] && JOBS=$FREE
  fi
fi
[ "$JOBS" -lt 1 ] && JOBS=1

TMPDIR_SUITE=$(mktemp -d "${TMPDIR:-/tmp}/courts.XXXXXX") || exit 2
trap 'rm -rf "$TMPDIR_SUITE"' EXIT
mkdir -p reports

is_solo() {
  set -- $1; probe="$1"
  for s in "${SOLO[@]}"; do
    [ "$probe" = "$s" ] && return 0
  done
  return 1
}

run_one() {
  idx="$1"; entry="$2"
  set -- $entry; tool="$1"; shift
  out=$(python3 "$tool" "$@" 2>&1); rc=$?
  printf '%s
' "$out" > "$TMPDIR_SUITE/$idx.out"
  printf '%s
' "$rc" > "$TMPDIR_SUITE/$idx.rc"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$TMPDIR_SUITE/$idx.ts"
}

FELL=0
# СБОР ПАЧКИ: вывод по порядку индексов, строка леджера — здесь же, из родителя.
flush_range() {
  k="$1"; last_idx="$2"
  while [ "$k" -le "$last_idx" ]; do
    entry="${COURTS[$k]}"
    set -- $entry; tool="$1"
    rc=$(cat "$TMPDIR_SUITE/$k.rc" 2>/dev/null || echo 2)
    stamp=$(cat "$TMPDIR_SUITE/$k.ts" 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)
    out=$(cat "$TMPDIR_SUITE/$k.out" 2>/dev/null)
    last=$(printf '%s
' "$out" | tail -1)
    # ЛЕДЖЕР ПРИБОРОВ: последняя строка каждого суда — с датой и кодом —
    # дописывается в reports/ledger.tsv; отчёт «состояние кристалла»
    # (scripts/crystal.py) читает оттуда последний вердикт каждого прибора.
    printf '%s\t%s\t%s\t%s\n' "$stamp" "$(basename "$tool")" "$rc" "$last" >> reports/ledger.tsv
    if [ "$rc" = 0 ]; then
      printf 'СУД ЦЕЛ   %-26s %s\n' "$(basename "$tool")" "$last"
    else
      FELL=$((FELL+1))
      printf 'СУД ПАЛ   %-26s (rc=%s)\n' "$(basename "$tool")" "$rc"
      printf '%s\n' "$out" | tail -6 | sed 's/^/    /'
    fi
    k=$((k+1))
  done
}

TOTAL=${#COURTS[@]}
i=0
batch_start=0
running=0
while [ "$i" -lt "$TOTAL" ]; do
  entry="${COURTS[$i]}"
  if is_solo "$entry"; then
    if [ "$running" -gt 0 ]; then
      wait
      flush_range "$batch_start" $((i-1))
      running=0
    fi
    run_one "$i" "$entry"
    flush_range "$i" "$i"
    batch_start=$((i+1))
  else
    run_one "$i" "$entry" &
    running=$((running+1))
    if [ "$running" -ge "$JOBS" ]; then
      wait
      flush_range "$batch_start" "$i"
      running=0
      batch_start=$((i+1))
    fi
  fi
  i=$((i+1))
done
if [ "$running" -gt 0 ]; then
  wait
  flush_range "$batch_start" $((TOTAL-1))
fi
echo "---"
if [ "$FELL" = 0 ]; then
  echo "СУДЫ КОРПУСА: все ${#COURTS[@]} целы"
else
  echo "СУДЫ КОРПУСА: ПАЛО $FELL из ${#COURTS[@]}"
fi
exit $((FELL > 0))
