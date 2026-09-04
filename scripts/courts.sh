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
        "scripts/threshold_census.py")
FELL=0
for entry in "${COURTS[@]}"; do
  set -- $entry; tool="$1"; shift
  out=$(python3 "$tool" "$@" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | tail -1)
  # ЛЕДЖЕР ПРИБОРОВ: последняя строка каждого суда — с датой и кодом —
  # дописывается в reports/ledger.tsv; отчёт «состояние кристалла»
  # (scripts/crystal.py) читает оттуда последний вердикт каждого прибора.
  mkdir -p reports
  printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(basename "$tool")" "$rc" "$last" >> reports/ledger.tsv
  if [ "$rc" = 0 ]; then
    printf 'СУД ЦЕЛ   %-26s %s\n' "$(basename "$tool")" "$last"
  else
    FELL=$((FELL+1))
    printf 'СУД ПАЛ   %-26s (rc=%s)\n' "$(basename "$tool")" "$rc"
    printf '%s\n' "$out" | tail -6 | sed 's/^/    /'
  fi
done
echo "---"
if [ "$FELL" = 0 ]; then
  echo "СУДЫ КОРПУСА: все ${#COURTS[@]} целы"
else
  echo "СУДЫ КОРПУСА: ПАЛО $FELL из ${#COURTS[@]}"
fi
exit $((FELL > 0))
