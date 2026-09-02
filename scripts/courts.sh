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
        "scripts/manifest_court.py" "scripts/prose_court.py" "scripts/shelf_court.py" "tools/mutants.py" "scripts/lexicon_reach.py"
        "courts/inquiry_pt_nl_court.py" "courts/inquiry_pl_tr_court.py"
        "courts/metalang_court.py"
        "courts/relation_court.py"
        "scripts/court_mutants.py" "scripts/panel_court.py"
        "scripts/concept_reach.py"
        "scripts/ask_reach.py" "scripts/band_reach.py" "scripts/biblio_reach.py" "scripts/shelf_court.py" "scripts/ask_width.py" "courts/notationvar_court.py"
        "courts/prosetree_court.py" "courts/longdiv_court.py"
        "scripts/coverage.py")
FELL=0
for entry in "${COURTS[@]}"; do
  set -- $entry; tool="$1"; shift
  out=$(python3 "$tool" "$@" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | tail -1)
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
