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

# КОРЕНЬ БЕРЁТСЯ ОТ ФАЙЛА ЛИШЬ ОДИН РАЗ И ДАЛЬШЕ ИДЁТ ОКРУЖЕНИЕМ: копия набора лежит во
# временном дворе, и «каталог файла, шаг вверх» привёл бы её в домашний каталог, а не в
# корпус. Всякий прибор искался бы оттуда и не нашёлся.
if [ -z "${SUITE_ROOT:-}" ]; then
  SUITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
  export SUITE_ROOT
fi
cd "$SUITE_ROOT"

# НАБОР ИСПОЛНЯЕТ СВОЙ СПИСОК, А НЕ СВОЙ ФАЙЛ (12.09, прожито). Прогон suite8 шёл два с
# половиной часа и упал на последнем шаге:
#
#     scripts/courts.sh: line 366: syntax error near unexpected token `fi'
#
# Строки такой в файле нет, и `bash -n` его читает целиком. Беда в ином: ОБОЛОЧКА ЧИТАЕТ
# СКРИПТ ПО МЕРЕ ИСПОЛНЕНИЯ, держа БАЙТОВОЕ СМЕЩЕНИЕ в файле. Я трижды вписывал в этот
# набор новые приборы, пока он шёл, — и всякая вставка сдвигала хвост. Вернувшись за
# следующей порцией, оболочка прочла её со сдвинутого места и попала в середину условия.
#
#     СКРИПТ, ПРАВЛЕННЫЙ ВО ВРЕМЯ СВОЕГО ИСПОЛНЕНИЯ, ЧИТАЕТСЯ ДАЛЬШЕ СО СДВИНУТОГО МЕСТА,
#     И ПАДЕНИЕ ЕГО ГОВОРИТ О СТРОКЕ, КОТОРОЙ НЕТ.
#
# Это родня закону «ДЕРЕВО ДВИНУЛОСЬ ПОД НАБОРОМ», но тяжелее: там приборы читали разное
# дерево и вердикты расходились, здесь ГИБНЕТ САМ НАБОР — и гибнет на последнем шаге,
# потеряв два с половиной часа работы.
#
# Лечение: набор исполняет СВОЮ КОПИЮ, снятую в первый же миг. Копия лежит вне дерева, её
# никто не правит, и смещение её незыблемо. Правки дерева по ходу остаются видны приборам
# (они читают файлы сами) — и подпись дерева до и после по-прежнему их ловит.
# КОПИЯ УБИРАЕТ СЕБЯ САМА, А НЕ РОДИТЕЛЬ: `exec` ЗАМЕНЯЕТ ПРОЦЕСС, и `trap ... EXIT`,
# поставленный ДО него, не исполнится никогда — копии копились бы во временном дворе
# по одной за прогон. Оттого имя копии уходит в окружение, а убирает её сама копия.
if [ "${SUITE_SELF_COPY:-}" != "1" ]; then
  SUITE_COPY="${TMPDIR:-/tmp}/courts-$$-$(date +%s).sh"
  cp "$0" "$SUITE_COPY" || exit 2
  export SUITE_COPY SUITE_SELF_COPY=1
  exec bash "$SUITE_COPY" ${1+"$@"}
fi
# УБОРКА ЛОВИТ И УБИЕНИЕ, А НЕ ТОЛЬКО ВЫХОД: на одном лишь EXIT прерванный прогон
# оставлял копию во временном дворе — проверено убиением, копия осталась лежать.
trap 'rm -f "${SUITE_COPY:-}"; exit 130' INT TERM
trap 'rm -f "${SUITE_COPY:-}"' EXIT

# ПРОДОЛЖЕНИЕ ОБОРВАННОГО ПРОГОНА (11.09). Набор из 232 приборов идёт часами и за две смены
# не дошёл до конца ни разу: машина занята чужой работой, прогон рвётся на шестьдесят пятом
# приборе — и вся работа теряется. Между тем она НЕ ПОТЕРЯНА: вердикт каждого прибора лёг
# в reports/ledger.tsv по ходу дела.
#
#     ПАМЯТЬ У НАБОРА БЫЛА, НЕ БЫЛО ЧТЕНИЯ.
#
# `--продолжить` пропускает прибор, чей ПОСЛЕДНИЙ вердикт в леджере есть нуль, поставленный
# ПОЗЖЕ самой свежей правки дерева (`scripts/suite_resume.py`). Правка любого файла гонит
# заново весь набор: мера груба и ошибается в сторону лишней работы, а не пропущенной проверки.
# Без довода набор идёт, как шёл, — целиком.
RESUME=0
for arg in ${1+"$@"}; do
  case "$arg" in
    --продолжить) RESUME=1 ;;
  esac
done
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
        "scripts/reproducible.py" "scripts/bash32_court.py" "scripts/empty_in_court.py" "scripts/lawfirst_court.py" "scripts/sign_intact.py" "scripts/property_named.py" "scripts/ladder_full.py" "scripts/broken_law.py" "scripts/house_api.py" "scripts/json_hand.py" "scripts/suite_resume.py" "scripts/readme_court.py" "scripts/arith_debt.py" "scripts/twin_world.py" "scripts/orphan_world.py" "scripts/genus_shown.py" "scripts/oracle_named.py" "scripts/world_atlas.py" "scripts/trap_series.py" "scripts/house_selfcheck.py"
        "scripts/manifest_court.py" "scripts/prose_court.py" "tools/mutants.py" "scripts/lexicon_reach.py"
        "courts/inquiry_pt_nl_court.py" "courts/inquiry_pl_tr_court.py"
        "courts/metalang_court.py" "courts/glyph_court.py" "courts/space_court.py" "courts/stenogram_court.py"
        "courts/mathspaces_court.py" "courts/gsmforms_court.py" "courts/definitions_court.py" "courts/pronoun_court.py" "courts/money_court.py" "courts/holes_court.py" "courts/money_langs_court.py" "courts/geometry_langs_court.py" "courts/units_langs_court.py" "courts/stats_langs_court.py" "courts/calendar_langs_court.py" "courts/sequences_langs_court.py" "courts/compare_langs_court.py" "courts/share_langs_court.py" "courts/physics_langs_court.py"
        "courts/relation_court.py"
        "scripts/court_mutants.py" "scripts/panel_court.py"
        "scripts/concept_reach.py"
        "scripts/ask_reach.py" "scripts/band_reach.py" "scripts/biblio_reach.py" "courts/ruverbs_court.py" "courts/script_court.py" "scripts/word_mutants.py" "scripts/verdict_cover.py" "scripts/sentence_cover.py" "scripts/bench_leak.py" "scripts/shelf_court.py" "scripts/ask_width.py" "courts/notationvar_court.py"
        "courts/prosetree_court.py" "courts/longdiv_court.py"
        "scripts/form_census.py" "scripts/houses_census.py" "scripts/mass_census.py" "scripts/verbthings_court.py"
        "scripts/coverage.py"
        # ДОМА РАЗГОВОРА И РАССУЖДЕНИЯ (04.09). Их суды жили в палате и стерегли
        # ВОРОТА, но в этом списке не стояли, и потому вердикт «пало 0 из 103»
        # их не считал — ноль с укороченным знаменателем (М-264). Считает.
        "courts/behavior_court.py" "courts/topics_court.py" "courts/nature_court.py" "courts/links_court.py" "courts/scale_court.py" "courts/opposites_court.py" "courts/roles_court.py" "courts/joints_court.py" "courts/dialogue_court.py" "courts/worldfacts_court.py" "courts/infer_court.py" "scripts/circle_probe.py" "scripts/agree_probe.py" "scripts/shelf_declare.py" "scripts/house_reach.py" "scripts/head_census.py" "scripts/form_matrix.py"
        # …и четыре дома рассуждения, севшие 04.09 после снятия заморозки
        "courts/disj_court.py" "courts/indu_court.py" "courts/houseshows_court.py" "courts/article_court.py" "courts/rowframe_court.py" "courts/opchoice_court.py" "courts/chance_court.py" "courts/lever_court.py" "courts/zerodiv_court.py" "courts/bound_court.py" "courts/prec_court.py" "courts/estim_court.py" "courts/both_court.py" "courts/likely_court.py" "courts/sameshare_court.py" "courts/factor_court.py" "courts/amend_court.py" "courts/divrule_court.py" "courts/reduce_court.py" "courts/cmpshare_court.py" "courts/wholeshare_court.py" "courts/addshare_court.py" "courts/mulshare_court.py" "courts/divshare_court.py" "courts/neg_court.py" "courts/signrul_court.py" "courts/opslaw_court.py" "courts/signadd_court.py" "courts/pow_court.py" "courts/dec_court.py" "courts/abs_court.py" "courts/handy_court.py" "courts/prop_court.py" "courts/rem_court.py" "courts/parity_court.py" "courts/pctchange_court.py" "courts/pctdiff_court.py" "courts/mapscale_court.py" "courts/divsense_court.py" "courts/plaus_court.py" "courts/point_court.py" "courts/need_court.py" "courts/inverse_court.py" "courts/ceilfloor_court.py" "courts/unitcmp_court.py" "courts/placeval_court.py" "courts/digitlen_court.py" "courts/nesuf_court.py" "courts/numlabel_court.py" "courts/onestep_court.py" "courts/closure_court.py" "courts/dist_court.py" "courts/primewalk_court.py" "courts/orderlaw_court.py" "courts/gender_court.py" "courts/analog_court.py" "courts/reply_court.py"
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
        "scripts/prefix_traps.py" "scripts/sign_traps.py" "scripts/strat_slice.py" "scripts/house_rejects.py" "scripts/root_passport.py" "scripts/pack_singular_risk.py" "scripts/cell_shown.py"
        # ТРИ СУДА ОБЪЯВЛЕНИЯ (07.09, вечер): слово, объявленное языку и не
        # встречающееся в СВОДЕ (вооружает чужой суд); ячейка класса, не показанная
        # в СВОЁМ пласте; имя, показанное только во множественном при числе.
        "scripts/idle_word.py" "scripts/form_unshown.py" "scripts/one_singular.py"
        # СЛОВО ШАБЛОНА БЕЗ ОБЪЯВЛЕНИЯ — литерал, которым пакет пишет и которого не
        # объявляет: его строка получает знак ноль ото всех языков и достаётся
        # чужому суду (шрам «liczę 2 ruble.», 07.09).
        "scripts/template_word.py"
        # ПЕРЕПИСЬ БЕЗЗНАКОВЫХ — сколько строк пластов не несут знака ни одного
        # языка и потому подсудны всякому. Печатает число, не падает.
        "scripts/signless_census.py"
        # ДОЛЯ ОПЕРАТОРА — какую часть жизни в своде слово действия стои́т между
        # числами. «más» 3.8 % — на нём ядро и ошиблось (заказ holon 07.09).
        "scripts/operator_share.py"
        # КЛЮЧ БЕЗ ОПОРЫ — вопрос удержанного ключа, чей род свод пишет реже LAW³ = 8
        # раз: отказ читателя на таком роде есть свидетельство о своде, а не о нём.
        "scripts/key_support.py"
        # ПОЛОВИНЧАТЫЙ ЗАКОН — место, где дом пишет множественное литералом рядом с
        # числом: правота такой строки держится жребием, а не законом.
        "scripts/half_law.py" "scripts/unknown_name.py" "scripts/stale_world.py" "scripts/agree_traps.py" "scripts/wrong_sign.py" "scripts/debt_mark.py" "scripts/copula_band.py" "scripts/past_gender.py" "scripts/word_once.py" "scripts/article_sound.py" "scripts/elision.py"
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
        "courts/holdforms_court.py" "courts/cmpframes_court.py" "courts/sceneforms_court.py" "courts/toolforms_court.py" "courts/verifyforms_court.py" "courts/planforms_court.py" "courts/episodeforms_court.py" "courts/summaryforms_court.py" "courts/opforms_court.py" "courts/readnum_court.py" "courts/mandateforms_court.py" "courts/personforms_court.py" "courts/selfmodelforms_court.py" "courts/signedworld_court.py" "courts/beforetails_court.py" "courts/discountroad_court.py" "courts/nomention_court.py" "courts/clockforms_court.py" "courts/mixedunits_court.py" "courts/dateforms_court.py" "courts/clockwords_court.py" "courts/speedforms_court.py" "courts/roundforms_court.py" "courts/orderforms_court.py" "courts/quantforms_court.py" "courts/roman_court.py" "courts/place_court.py" "courts/unitfrac_court.py" "courts/enough_court.py" "courts/numphrase_court.py" "courts/kinbearer_court.py" "courts/pronobject_court.py" "courts/proform_court.py" "courts/degrees_court.py" "courts/actturn_court.py" "courts/tempscale_court.py" "courts/action_measure_court.py" "courts/numberline_court.py" "courts/countfacts_court.py" "courts/letters_court.py" "courts/langcount_court.py" "courts/propcompare_court.py" "courts/price_court.py" "courts/translate_court.py" "courts/timeunits_court.py" "courts/svamp_court.py" "courts/measure_langs_court.py")
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
# СНЯТЫЙ НАБОР ОСТАВЛЯЛ ЖИВЫХ ДЕТЕЙ (09.09). `pkill -f courts.sh` убивает оболочку, а её
# питоны переходят к init и продолжают есть машину: один такой прожил ТРИДЦАТЬ ЧЕТЫРЕ
# МИНУТЫ рядом со следующим прогоном и замедлил его вдвое. Прибор, переживший свой набор,
# не считает ничего — его вывод некому собрать, — но машину ест как живой.
#
#     ЛОВУШКА, УБИРАЮЩАЯ ЗА СОБОЙ ТОЛЬКО КАТАЛОГ, УБИРАЕТ СЛЕД, А НЕ ПРИЧИНУ.
#
# Бьём по СВОИМ фоновым задачам (`jobs -p`), а не по группе: `kill 0` снёс бы и того,
# кто набор позвал.
# ЛОВУШКА НА TERM БЕЗ ВЫХОДА ДЕЛАЕТ СКРИПТ НЕУБИВАЕМЫМ (09.09, вечер — своя же ошибка).
#
# Ловушка, поставленная утром против осиротевших детей, была написана одной строкой на EXIT,
# INT и TERM — и тем ЗАМЕНИЛА действие по умолчанию: обработчик отрабатывает, и bash ПРОДОЛЖАЕТ
# работу. Набор перестал умирать от `kill`, и два прогона шли разом, мешая друг другу и машине.
# Проверено опытом на пробном скрипте: «ловушка отработала» — и «ПЕРЕЖИЛ SIGTERM».
#
#     СТРАЖ, ПОСТАВЛЕННЫЙ ПРОТИВ ОДНОЙ БЕДЫ, ЗАВОДИТ ВТОРУЮ, ЕСЛИ НЕ ДОЧИТАН ДО КОНЦА.
#     Ловушка сигнала обязана ВЫЙТИ САМА — иначе она отменяет то, ради чего сигнал послан.
#
# Ныне уборка стои́т на EXIT (она нужна при всяком исходе), а сигнал бьёт детей и выходит кодом
# 128 + номер, как велит обычай оболочки.
trap 'rm -rf "$TMPDIR_SUITE"' EXIT
trap 'jobs -p | xargs kill 2>/dev/null; exit 130' INT
trap 'jobs -p | xargs kill 2>/dev/null; exit 143' TERM
mkdir -p reports

is_solo() {
  local probe s
  set -- $1; probe="$1"
  for s in "${SOLO[@]}"; do
    [ "$probe" = "$s" ] && return 0
  done
  return 1
}

run_one() {
  # ЦЕНА ПРИБОРА ЗАПИСЫВАЕТСЯ, А НЕ УГАДЫВАЕТСЯ (10.09). Набор из 216 приборов идёт часами и
  # до сего дня не мог назвать СВОЙ САМЫЙ ДОРОГОЙ: ни леджер, ни след времени не хранили.
  # Рука узнавала цену только через `ps`, и то лишь пока прибор ещё жив; многопроцессный
  # прибор при этом врал вдвойне — время родителя у него ноль, а работают дети.
  #
  #     НАБОР, НЕ ЗНАЮЩИЙ СВОЕЙ ЦЕНЫ, НЕ МОЖЕТ ЕЁ И УБАВИТЬ.
  #
  # РАЗРЕШЕНИЕ — ЦЕЛАЯ СЕКУНДА, И ЭТО ГРАНИЦА, А НЕ НЕДОСМОТР: bash 3.2 (тот, что несёт
  # macOS) не знает `EPOCHREALTIME`, а BSD `date` не знает `%N`. Прибор, идущий доли
  # секунды, ляжет здесь нулём или единицей — и пусть: он ставится ради тех, что идут
  # МИНУТАМИ, а их целая секунда меряет с избытком.
  local idx entry tool out rc t0 t1
  idx="$1"; entry="$2"
  set -- $entry; tool="$1"; shift
  t0=$(date +%s)
  out=$(python3 "$tool" "$@" 2>&1); rc=$?
  t1=$(date +%s)
  printf '%s\n' "$((t1 - t0))" > "$TMPDIR_SUITE/$idx.sec"
  printf '%s
' "$out" > "$TMPDIR_SUITE/$idx.out"
  printf '%s
' "$rc" > "$TMPDIR_SUITE/$idx.rc"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$TMPDIR_SUITE/$idx.ts"
}

FELL=0
# СБОР ПАЧКИ: вывод по порядку индексов, строка леджера — здесь же, из родителя.
flush_range() {
  # ИМЕНА ЗДЕСЬ МЕСТНЫЕ, И ЭТО НЕ ВКУС (09.09). Глобальная `entry` этой сборки ЗАТИРАЛА
  # `entry` цикла, а одиночная ветвь звала `run_one "$i" "$entry"` ПОСЛЕ сборки — и гоняла
  # НЕ ТОТ ПРИБОР: вместо одиночки второй раз шёл сосед, а его вердикт ложился в леджер под
  # именем одиночки. В SOLO стоя́т пять самых тяжёлых приборов корпуса; всякий из них,
  # ставший после непустой пачки, НЕ ГОНЯЛСЯ ВОВСЕ, и набор об этом молчал зелёным.
  #
  #     ПРИБОР, ЧЕЙ ВЕРДИКТ ПРИНАДЛЕЖИТ СОСЕДУ, ХУЖЕ НЕ ЗАПУЩЕННОГО: не запущенный оставляет
  #     пустоту, а этот оставляет ЧУЖОЙ ЗЕЛЁНЫЙ. Найдено ледждером: 09.09 `prosetree_court.py`
  #     записан с вердиктом `notationvar_court.py`, слово в слово, при своём коде 0.
  local k last_idx entry tool rc stamp out last sec
  k="$1"; last_idx="$2"
  while [ "$k" -le "$last_idx" ]; do
    entry="${COURTS[$k]}"
    set -- $entry; tool="$1"
    if [ -f "$TMPDIR_SUITE/$k.skip" ]; then
      printf 'СУД ЗЕЛЁН %-26s (леджер: дерево не менялось)\n' "$(basename "$tool")"
      SKIPPED=$((SKIPPED+1))
      k=$((k+1))
      continue
    fi
    rc=$(cat "$TMPDIR_SUITE/$k.rc" 2>/dev/null || echo 2)
    stamp=$(cat "$TMPDIR_SUITE/$k.ts" 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)
    out=$(cat "$TMPDIR_SUITE/$k.out" 2>/dev/null)
    # ЛЕДЖЕР БЕРЁТ ВЕРДИКТ, А НЕ ПОСЛЕДНЮЮ СТРОКУ (07.09).
    #
    # Правило «последняя строка» держалось на обычае: вердикт печатается в конце.
    # Обычай нарушается молча. `scripts/sweep_self.py` печатает после вердикта
    # подробности по одной на строку, и в леджер от него НИ РАЗУ с 05.09 не попал
    # вердикт — все его записи суть «    pl · session-recall · X ma · 8», строка
    # разбора. Прибор при этом честно возвращал код; лгала ЗАПИСЬ О НЁМ.
    #
    #     ЛЕДЖЕР, ЧИТАЮЩИЙ ПОСЛЕДНЮЮ СТРОКУ, ЧИТАЕТ НЕ ВЕРДИКТ, А ПРИВЫЧКУ. Отчёт
    #     «состояние кристалла» берёт последний вердикт каждого прибора отсюда — и
    #     показывал вместо вердикта обрывок чужого разбора.
    #
    # Ныне берётся ПОСЛЕДНЯЯ СТРОКА С ПОЗОЙ (PASS, FAIL или ОТКАЗ) — так вердикт
    # находится, где бы он ни стоял; если позы нет ни в одной строке, берётся, как
    # прежде, последняя, ибо прибор без позы всё же должен оставить след.
    last=$(printf '%s
' "$out" | grep -E "(PASS|FAIL|ОТКАЗ)" | tail -1)
    [ -z "$last" ] && last=$(printf '%s
' "$out" | tail -1)
    printf '%s\t%s\t%s\t%s\n' "$stamp" "$(basename "$tool")" "$rc" "$last" >> reports/ledger.tsv
    # ЦЕНА ИДЁТ В СВОЙ СЛЕД, А НЕ ПЯТЫМ ПОЛЕМ ЛЕДЖЕРА: леджер читают `crystal.py` и
    # `denominator_census.py`, и новое поле в нём было бы правкой чужого договора.
    sec=$(cat "$TMPDIR_SUITE/$k.sec" 2>/dev/null || echo -1)
    printf '%s\t%s\t%s\n' "$stamp" "$(basename "$tool")" "$sec" >> "$TMPDIR_SUITE/cost"
    printf '%s\t%s\t%s\n' "$stamp" "$(basename "$tool")" "$sec" >> reports/SUITE-COST.tsv
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

SKIP_LIST=""
SKIPPED=0
if [ "$RESUME" = 1 ]; then
  SKIP_LIST=$(python3 scripts/suite_resume.py --пропустить 2>/dev/null || true)
  printf 'ПРОДОЛЖЕНИЕ: %s\n' "$(python3 scripts/suite_resume.py --метка 2>/dev/null || echo 'метки нет')"
  printf 'ПРОДОЛЖЕНИЕ: зелены на этом дереве и не гонятся — %s\n' \
    "$(printf '%s\n' "$SKIP_LIST" | grep -c . || true)"
fi

# ПОДПИСЬ ДЕРЕВА СНИМАЕТСЯ ДО И ПОСЛЕ (12.09).
#
#     НАБОР, ИДУЩИЙ ПО ЖИВОМУ ДЕРЕВУ, СУДИТ ДЕРЕВО, КОТОРОГО УЖЕ НЕТ.
#
# Прогон этой ночи шёл два с половиной часа, покуда дерево правилось непрерывно, —
# и один прибор из восьми павших пал НЕ ПО ДЕЛУ: он прочёл НОВЫЙ файл мира модуля
# СТАРОЙ палатой, собранной до правки дома. Краснота его говорила о мгновении между
# двумя правками, а читалась как о своде.
#
# Здесь не запрещается править дерево при живом наборе — запретить значило бы
# остановить работу на два часа. Здесь лишь ГОВОРИТСЯ ВСЛУХ, двинулось ли дерево:
# прогон по неподвижному дереву и прогон по живому суть разные свидетельства, и
# читатель вправе знать, какое перед ним.
#
# ИМЕНА ЗДЕСЬ ЛАТИНСКИЕ, И ЭТО КУПЛЕНО ПАДЕНИЕМ В ТОТ ЖЕ ЧАС: первая редакция звала их
# «ПОДПИСЬ_ДО» и «ПОДПИСЬ_ПОСЛЕ», и суд bash 3.2 упал немедля — /bin/bash макоси
# кириллического имени переменной не ест вовсе.
#
#     СКРИПТ ПИШЕТСЯ ТЕМ ЯЗЫКОМ, КОТОРЫЙ ЕГО ЧИТАЕТ, А НЕ ТЕМ, КОТОРЫМ ЕГО ДУМАЮТ.
TREE_BEFORE=$(python3 scripts/suite_resume.py --метка 2>/dev/null | tr -d '\n' || echo '?')

TOTAL=${#COURTS[@]}
i=0
batch_start=0
running=0
while [ "$i" -lt "$TOTAL" ]; do
  entry="${COURTS[$i]}"
  # ПРОПУЩЕННЫЙ ПОМЕЧАЕТСЯ ФАЙЛОМ, А НЕ ВЫЧЁРКИВАЕТСЯ ИЗ СПИСКА: сборка пачки ходит
  # по тем же ИНДЕКСАМ, и вычерк сдвинул бы вердикты на соседей — ту самую беду,
  # от которой стои́т предупреждение в `flush_range`.
  if [ "$RESUME" = 1 ] && printf '%s\n' "$SKIP_LIST" | grep -qx "$(basename "${entry%% *}")"; then
    : > "$TMPDIR_SUITE/$i.skip"
    i=$((i+1))
    continue
  fi
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
# ХВОСТ СОБИРАЕТСЯ ПО НЕСОБРАННОМУ, А НЕ ПО ЖИВЫМ РАБОЧИМ: прогон, чьи последние приборы
# ПРОПУЩЕНЫ, оставляет running = 0 при несобранном хвосте, и прежнее условие молчало о них.
if [ "$running" -gt 0 ]; then
  wait
fi
if [ "$batch_start" -le $((TOTAL-1)) ]; then
  flush_range "$batch_start" $((TOTAL-1))
fi
echo "---"
if [ "$FELL" = 0 ]; then
  echo "СУДЫ КОРПУСА: все ${#COURTS[@]} целы"
else
  echo "СУДЫ КОРПУСА: ПАЛО $FELL из ${#COURTS[@]}"
fi
TREE_AFTER=$(python3 scripts/suite_resume.py --метка 2>/dev/null | tr -d '\n' || echo '?')
if [ "$TREE_BEFORE" != "$TREE_AFTER" ]; then
  echo "ДЕРЕВО ДВИНУЛОСЬ ПОД НАБОРОМ: было $TREE_BEFORE, стало $TREE_AFTER —"
  echo "  вердикты выше сняты с РАЗНЫХ деревьев, и краснота иных может говорить"
  echo "  о мгновении между двумя правками, а не о своде"
else
  echo "ДЕРЕВО НЕПОДВИЖНО ВЕСЬ ПРОГОН: $TREE_BEFORE"
fi
# ПРОПУЩЕННОЕ НАЗЫВАЕТСЯ ВСЛУХ: прогон, молчащий о том, чего не гонял, отчитывается
# зелёным за чужую работу.
if [ "$SKIPPED" -gt 0 ]; then
  echo "СУДЫ КОРПУСА: пропущено по леджеру $SKIPPED (зелены на этом же дереве)"
fi
# ПЯТЬ САМЫХ ДОРОГИХ ПРИБОРОВ ЭТОГО НАБОРА — чтобы цена была видна тому, кто ждал.
if [ -s "$TMPDIR_SUITE/cost" ]; then
  echo "--- дороже всех (секунд):"
  sort -t"$(printf '\t')" -k3,3nr "$TMPDIR_SUITE/cost" | head -5 \
    | while IFS="$(printf '\t')" read -r _ nm sc; do printf '    %-28s %6s\n' "$nm" "$sc"; done
  awk -F"\t" '{s+=$3} END {printf "    %-28s %6d\n", "ВСЕГО МАШИННЫХ СЕКУНД", s}' "$TMPDIR_SUITE/cost"
fi

# СЛЕД НАБОРА — ПРОТИВ МОЛЧАЛИВОГО ПАДЕНИЯ (09.09).
#
# Дважды за два дня прибор набора оказывался красным месяцами, и оба раза число нашлось лишь
# оттого, что рука позвала его сама: точка гоняет ВОСЕМЬ приборов, а набор — ВЕСЬ СПИСОК
# (на 09.09 их 116, и число растёт всякий раз, как ставят прибор; сверяет его `panel_court`),
# и между ними лежит вся разница между «свод цел» и «свод проверен».
#
#     ПРИБОР, КОТОРОГО ТОЧКА НЕ ГОНЯЕТ, ПАДАЕТ МОЛЧА. Лекарство не в том, чтобы гонять всё
#     при каждой точке — набор идёт ЧАСАМИ, — а в том, чтобы ТОЧКА ЗНАЛА, КОГДА НАБОР
#     ХОДИЛ В ПОСЛЕДНИЙ РАЗ И ЧТО СКАЗАЛ.
#
# След пишется ВСЕГДА — и при целости, и при падении: след, пишущийся лишь при удаче, лжёт
# молчанием так же, как прибор.
printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "$([ "$FELL" = 0 ] && echo ЦЕЛ || echo ПАЛО)" "$FELL" "${#COURTS[@]}" \
  > reports/SUITE-LAST.tsv
exit $((FELL > 0))
