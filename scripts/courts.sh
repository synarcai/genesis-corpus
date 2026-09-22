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
# КАК ЕГО ОСТАНОВИТЬ (12.09, прожито). Набор исполняет КОПИЮ, и в списке процессов его имени
# «scripts/courts.sh» БОЛЬШЕ НЕТ — стои́т «bash /tmp/courts-<pid>-<время>.sh». `pkill -f "bash
# scripts/courts.sh"` убивает лишь оболочку-запускателя, а копия идёт дальше и продолжает
# звать приборы: я полчаса принимал её живые шаги за сирот и снимал их поодиночке, пока она
# ставила новые.
#
# И ПЕРВЫЙ ЖЕ ЗАПИСАННЫЙ ЗДЕСЬ РЕЦЕПТ БЫЛ НЕВЕРЕН (12.09, вечер). Стояло `pkill -f
# "courts-[0-9]*\.sh"`, а копия зовётся `courts-<pid>-<время>.sh`: между цифрами и «.sh»
# стои́т ещё дефис и второе число, и образец не совпадает НИ С ЧЕМ. Проверено делом: после
# такого `pkill` набор жил и переходил к следующему прибору.
#
#     РЕЦЕПТ ОСТАНОВКИ, ЗАПИСАННЫЙ И НЕ ИСПЫТАННЫЙ, ЕСТЬ ХУДШИЙ РОД ЗАПИСИ: ему верят в тот
#     самый час, когда проверять некогда.
#
# ВЕРНЫЙ РЕЦЕПТ — по каталогу, а не по образцу имени:
#
#     pkill -f "\.tmp/courts-"          # снять сам набор
#     pkill -f "python3 -u courts/"     # снять прибор, который он держит
#
#     ЛЕКАРСТВО ОТ ПРАВКИ НА ХОДУ ОТНЯЛО У НАБОРА ЕГО ИМЯ, И ВМЕСТЕ С ИМЕНЕМ — СПОСОБ ЕГО
#     ОКЛИКНУТЬ. Всякая копия прячет подлинник не только от правки.
#
# Останавливать так:  pkill -f "courts-[0-9]*\.sh"    (копия зовётся по образцу, а не по месту)
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
        "courts/agreement_court.py" "courts/numgender_court.py" "courts/notation_court.py"
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
        "scripts/reproducible.py" "scripts/bash32_court.py" "scripts/empty_in_court.py" "scripts/lawfirst_court.py" "scripts/sign_intact.py" "scripts/property_named.py" "scripts/ladder_full.py" "scripts/name_crossed.py" "scripts/genre_measured.py" "scripts/second_copy.py" "scripts/unit_doors.py" "scripts/margin_census.py" "scripts/reports_index.py" "tools/law_atlas.py" "tools/court_atlas.py" "tools/genus_atlas.py" "scripts/permuted_fresh.py" "scripts/build_dated.py" "scripts/probe_present.py" "scripts/court_voice.py" "scripts/suite_guard.py" "scripts/forge_claim.py" "scripts/broken_law.py" "scripts/house_api.py" "scripts/json_hand.py" "scripts/suite_resume.py" "scripts/readme_court.py" "scripts/arith_debt.py" "scripts/twin_world.py" "scripts/orphan_world.py" "scripts/genus_shown.py" "scripts/oracle_named.py" "scripts/world_atlas.py" "scripts/trap_series.py" "scripts/house_selfcheck.py" "scripts/asked_uncounted.py" "scripts/refusal_only_word.py" "scripts/contrast_real.py" "scripts/genre_kinds.py" "scripts/refusal_house.py" "scripts/refusal_ground.py"
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
        "courts/disj_court.py" "courts/indu_court.py" "courts/houseshows_court.py" "courts/article_court.py" "courts/rowframe_court.py" "courts/opchoice_court.py" "courts/chance_court.py" "courts/lever_court.py" "courts/zerodiv_court.py" "courts/bound_court.py" "courts/prec_court.py" "courts/estim_court.py" "courts/both_court.py" "courts/likely_court.py" "courts/sameshare_court.py" "courts/factor_court.py" "courts/amend_court.py" "courts/divrule_court.py" "courts/reduce_court.py" "courts/cmpshare_court.py" "courts/wholeshare_court.py" "courts/addshare_court.py" "courts/mulshare_court.py" "courts/divshare_court.py" "courts/neg_court.py" "courts/signrul_court.py" "courts/opslaw_court.py" "courts/signadd_court.py" "courts/pow_court.py" "courts/dec_court.py" "courts/abs_court.py" "courts/handy_court.py" "courts/prop_court.py" "courts/rem_court.py" "courts/parity_court.py" "courts/pctchange_court.py" "courts/pctdiff_court.py" "courts/mapscale_court.py" "courts/divsense_court.py" "courts/plaus_court.py" "courts/point_court.py" "courts/need_court.py" "courts/inverse_court.py" "courts/ceilfloor_court.py" "courts/unitcmp_court.py" "courts/placeval_court.py" "courts/digitlen_court.py" "courts/nesuf_court.py" "courts/numlabel_court.py" "courts/onestep_court.py" "courts/closure_court.py" "courts/dist_court.py" "courts/primewalk_court.py" "courts/orderlaw_court.py" "courts/gender_court.py" "courts/measureprec_court.py" "courts/chancetrap_court.py" "courts/ratetrap_court.py" "courts/negquant_court.py" "courts/measuregrow_court.py" "courts/dim_court.py" "courts/fence_court.py" "courts/measure_court.py" "courts/turn_court.py" "courts/overlap_court.py" "courts/wmean_court.py" "courts/cond_court.py" "courts/numline_court.py" "courts/squnit_court.py" "courts/pctbase_court.py" "courts/leap_court.py" "courts/tzone_court.py" "courts/median_court.py" "courts/angle_court.py" "courts/homo_court.py" "courts/direct_court.py" "courts/analog_court.py" "courts/reply_court.py"
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
        # БЛОК ОТДАН НАРУЖУ (21.09) — страж двора `blocks/`, единственной части свода,
        # которую нельзя исправить задним числом: мир пересобирается, отчёт переписывается,
        # рубеж затягивается, а блок уже у читателя. Потому он один пересчитывает всякий
        # ответ ЗАНОВО, из одной истории вопроса, и сверяет область блока с областью домов.
        "scripts/block_court.py"
        # ИМЯ СМЕШАННОГО ПИСЬМА (21.09) — слово из двух алфавитов с омоглифом внутри:
        # «roды_плохи» читается глазом как «роды_плохи» и зовётся иначе. Найдено на живом
        # деле в доме акта; прибора на это у свода не было.
        "scripts/mixed_name.py"
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
        # СУД ДОМА ЛОВИТ ПОРЧУ — дом, чей суд зовёт ИСТИНОЙ порчу своей же страницы.
        # Спрашивает ДЕЛОМ: портит слово в странице и слушает суд дома, а самопроверки не
        # читает вовсе (замер по признаку письма считает стиль, а не дело).
        "scripts/house_mutant.py"
        # УЛОВ СУДА — сколько строк суд ловит ЕДИНСТВЕННЫЙ. Цена есть половина вопроса,
        # вторая — что пропадёт, если снять. Печатает числа и сайдкар, не падает: снятие
        # суда есть дело руки, а не прибора (`declarations/COURT-WORTH.md`).
        "scripts/court_catch.py"
        # ПЕРЕКОС СОГЛАСОВАНИЯ — две формы ОДНОГО слова, показанные врозь: «quantos tem»
        # 2 страницы против «quantas tem» 6. Ключ видит такое лишь там, где СПРАШИВАЕТ;
        # этот прибор считает формы порознь по всему своду и не ждёт вопроса.
        "scripts/agree_skew.py"
        # ДВУРОДОЕ ИМЯ — та же беда с другого конца и БЕЗ ПОРОГА: у имени один род, и
        # слово, стоящее и после «quanti», и после «quante», выдаёт ложь одной из двух
        # страниц. Прибор перекоса нашёл семь таких домов; этот не даёт им вернуться.
        "scripts/twogender.py"
        # ЧЕТЫРЕ ДОМА НЕНАЗВАННОГО ЗАКОНА (12.09, вечер): свод пользовался этими законами
        # тысячами строк и НИ РАЗУ их не называл — счётной формой имени при числе, французской
        # элизией, английским артиклем по звуку и польской связкой по счётной ячейке. Суды их
        # сверяют страницу с домом языка и своего закона не заводят.
        "courts/countlaw_court.py" "courts/elision_court.py"
        "courts/soundarticle_court.py" "courts/plcopula_court.py"
        # ШЕСТОЙ ДОМ: испанское «hay» не меняется при числе, а польский сосед
        # меняется — ловушка на ПЕРЕНОСЕ, и она ловит выучившего соседа.
        "courts/hay_court.py"
        # ВОСЬМОЙ ДОМ: два «быть» испанского. Суд читает ЧЕТЫРЕ закона, и четвёртый —
        # о звёздочке: показ запрещённого обязан быть помечен знаком, который читает суд.
        "courts/serestar_court.py"
        # ДЕВЯТЫЙ ДОМ: английское «do». Пять законов, и два последних — о ГРАНИЦАХ правила:
        # при связке и модальных вспомогательного нет, при вопросе о подлежащем — тоже.
        "courts/dosupport_court.py"
        # ДЕСЯТЫЙ ДОМ: слияние предлога с артиклем. Суд знает, что одна и та же пара слов
        # законна в одном языке и невозможна в другом, и границу свою называет вслух.
        "courts/fuseprep_court.py"
        # ОДИННАДЦАТЫЙ ДОМ: нидерландский «de/het». Артикль, не выводимый из слова,
        # проверяется только таблицей — и суд не пытается вывести его из звука или смысла.
        "courts/nlarticle_court.py"
        # ДВЕНАДЦАТЫЙ ДОМ: немецкий предлог двух падежей. Суд не решает, где место, а где
        # направление, — он судит согласие формы с таблицей, и этого довольно.
        "courts/decase_court.py"
        # ТРИНАДЦАТЫЙ ДОМ: класс в суахили. Показ отказа учит, что нельзя, и не учит, почему;
        # дом даёт причину — числительное согласуется с КЛАССОМ имени.
        "courts/swclass_court.py"
        # ЧЕТЫРНАДЦАТЫЙ ДОМ: индонезийское удвоение. Тот же третий род молчания — запрет без
        # причины, — и та же работа: дать причину вместо списка запретов.
        "courts/idredup_court.py"
        # ПЯТНАДЦАТЫЙ ДОМ: китайское счётное слово. Суд знает лишь таблицу; пустое место
        # счётным не считается, ибо его нет ни в одной таблице.
        "courts/zhclass_court.py"
        # ШЕСТНАДЦАТЫЙ ДОМ: турецкая гармония. Суд не умеет читать гласных и не должен — он
        # сверяет суффикс с таблицей основы, и одного сравнения довольно.
        "courts/trharm_court.py"
        # СЕМНАДЦАТЫЙ ДОМ: вьетнамское счётное. Суд не выводит разряд из значения — это была
        # бы ровно та ошибка, ради которой дом поставлен.
        "courts/viclass_court.py"
        # ВОСЕМНАДЦАТЫЙ ДОМ: корейская частица. Суд не умеет слышать и не должен — он сверяет
        # частицу с рядом, объявленным для последнего звука слова.
        "courts/koparticle_court.py"
        # СЛОВО ИЗ СВОДА: свод сам себе словарь. Слово, которого он не пишет нигде, не есть
        # слово этого свода — и подсадка, обрезавшая «equally» до «equall», выдаёт себя.
        "courts/corpusword_court.py"
        # ЗАЧИН ДЕЯТЕЛЯ: закон лица (М-131) жил внутри суда эпизода и до чужой рамки не
        # доходил — «Tom has 6 books» → «To has 6 books» проходило палату истиной. Здесь он
        # стои́т отдельно и судит всякую строку всякого мира, объявившего деятелей.
        "courts/actoropener_court.py"
        # ПАДЕЖ ЛИЦА: предлог правит падежом, и «у Иван было» проходило палату истиной — обе
        # формы русские. Пара, где одна половина есть падеж формы лица, объявленный пакетом.
        "courts/personcase_court.py"
        # ДЕВЯТНАДЦАТЫЙ ДОМ: украинская счётная ячейка. Свод показывал две ячейки из трёх, и
        # третью — пятью строками на пять слов.
        "courts/ukcount_court.py"
        # ДВАДЦАТЫЙ ДОМ: японское счётное. Суд читает МЕСТО знака, а не знак: «本» перед
        # частицей есть книга, «本» после числа есть мера длинных вещей.
        "courts/jaclass_court.py"
        # ДВАДЦАТЬ ПЕРВЫЙ ДОМ: финский партитив. Падеж и число суть разные вещи, и после
        # числа работает падеж: «kaksi taloa» — единственное, а не множественное.
        "courts/fipart_court.py" "courts/personplace_court.py" "courts/persondist_court.py" "courts/huobj_court.py" "courts/refusalwhy_court.py" "courts/deacc_court.py" "courts/svgender_court.py" "courts/romgender_court.py" "courts/numnoun_court.py" "courts/numplace_court.py"
        # СЕДЬМОЙ ДОМ: немецкое множественное без одного правила — ловушка на
        # НЕЗНАНИИ, и потому она стои́т после ловушки на переносе.
        "courts/deplur_court.py"
        # ПОЛОВИНЧАТЫЙ ЗАКОН — место, где дом пишет множественное литералом рядом с
        # числом: правота такой строки держится жребием, а не законом.
        "scripts/half_law.py" "scripts/unknown_name.py" "scripts/stale_world.py" "scripts/agree_traps.py" "scripts/wrong_sign.py" "scripts/debt_mark.py" "scripts/copula_band.py" "scripts/past_gender.py" "scripts/word_once.py" "scripts/article_sound.py" "scripts/elision.py"
        # ИМЯ КЛАССА — одна лексема, объявленная в одном пакете и именем, и глаголом.
        # Прибор не судит о части речи и не умеет; он спрашивает у ПАКЕТА О ПАКЕТЕ,
        # не стоит ли одна лексема в двух классах, чьи имена обещают разные части речи.
        "scripts/class_name_honest.py"
        # ДВА САЙДКАРА — РОДОВ И ЯЗЫКОВ. Внесены 16.09 по замеру суда состава: оба
        # объявили себя приборами (помета пустого обхода) и оба несут РУБЕЖИ-РАТЧЕТЫ —
        # покрытие рода 80 %, покрытие языка 91 %, спорящих домов 6, двойных 0, — а набор
        # их не звал, и рубежи эти не проверялись ни разу.
        #
        #     РУБЕЖ, КОТОРЫЙ НИКТО НЕ ПРОВЕРЯЕТ, ЕСТЬ ОБЕЩАНИЕ БЕЗ СВИДЕТЕЛЯ.
        #
        # Оба судят СОБРАННЫЙ сайдкар против свода и краснеют, когда свод ушёл вперёд, —
        # то есть стерегут ровно то, ради чего сделаны: адрес строки к её роду и языку.
        "scripts/genera_sidecar.py" "scripts/lang_sidecar.py"
        # РЫНОК ЗАЧИНА ДЕЯТЕЛЯ — третья полка того же рода: чем свод открывает предложение
        # перед словом при лице. Краснеет, когда свод ушёл вперёд покупки.
        "scripts/actorplace_market.py"
        # РЫНОК ПАДЕЖА ЛИЦА — четвёртая полка того же рода: в каком падеже свод ставит лицо
        # после слова. Краснеет, когда свод ушёл вперёд покупки.
        "scripts/personcase_market.py"
        # ЗОВ ПО СТАРОМУ АДРЕСУ — прибор, зовущий у соседа имя, какого у соседа нет.
        # Куплен 16.09 павшим прибором следа определений: разбор переехал из кузницы
        # в дом, зовущий остался при старом адресе и лежал павшим двое суток.
        # Читает ДЕРЕВО, а не запускает его, и потому идёт секунды на 1097 файлах.
        "scripts/stale_call.py"
        # МИР НЕИЗМЕНЕН — подпись мира до правки против подписи после. В наборе он
        # идёт ПРОБОЙ: судить ему нечего, покуда никто не объявил переезда, — но
        # доказать, что он умеет находить подсадку, он обязан всякий раз.
        "scripts/worlds_unchanged.py --проба"
        # ПЕРЕПИСЬ ПОРОГОВ — пай аудита «меры и пороги»: всякое число в роли
        # рубежа с ответом «объявлено / храповик / вкус». Печатает число, не падает.
        "scripts/threshold_census.py"
        # ЧИСЛО БЕЗ ЗНАМЕНАТЕЛЯ — последняя строка каждого прибора леджера: сказано
        # ли, из скольких. Ноль без объёма — FAIL (закон holon).
        "scripts/denominator_census.py"
        # НЕМОЙ ПРИБОР — кто стои́т в наборе, а вердикта в леджере не оставил НИ РАЗУ,
        # хотя обрывы его там есть. Двадцать два суда молчали шесть дней ценою в 38 с.
        "scripts/ledger_mute.py"
        # ЗАПРЕТ БЕЗ ПРИЧИНЫ — пласт отвергает форму, а объясняет ли её кто-нибудь. Связь
        # «пласт → дом» объявлена домом (`ЯЗЫК_ЗАКОНА`), а не угадывается по прозе.
        "scripts/refusal_reason.py"
        # ПЕРЕКОС ДОМА — во сколько раз дом показывает один свой род чаще другого. Дом,
        # у которого крайние расходятся в двадцать раз, учит одному в двадцать раз лучше —
        # и объявляет при этом оба. Рубеж стои́т лишь на крайних: мера, требующая ровности
        # от всего, заставляет писать лишнее.
        "scripts/house_skew.py"
        # ОБЕЩАНИЕ ДОМА — род, ОБЪЯВЛЕННЫЙ домом и показанный меньше закона массы.
        # Стои́т подле меры ровности, ибо чтит то же объявление `РОДЫ_ПО_ПРЕДМЕТУ`, а
        # спрашивает иное: не отношение крайних, а недобор от девяти.
        "scripts/house_promise.py"
        # РАЗНОГЛАСИЕ СУДОВ — четвёртое число о суде: ловит ли он порчу, которую сосед
        # пропускает. В наборе идёт УКОРОЧЕННОЙ выборкой (4 пробы на мир вместо 8): полная
        # стои́т 18 минут, и это цена, которую набор платить не обязан, покуда число не
        # двинулось. Полная мера 12.09 рукой: порч 2 873, поймано 97%, держат порчу
        # единственными 179 судов из 203 читающих.
        "scripts/court_split.py --проб 4"
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
        "courts/holdforms_court.py" "courts/cmpframes_court.py" "courts/sceneforms_court.py" "courts/toolforms_court.py" "courts/verifyforms_court.py" "courts/planforms_court.py" "courts/episodeforms_court.py" "courts/summaryforms_court.py" "courts/opforms_court.py" "courts/readnum_court.py" "courts/mandateforms_court.py" "courts/personforms_court.py" "courts/selfmodelforms_court.py" "courts/signedworld_court.py" "courts/beforetails_court.py" "courts/discountroad_court.py" "courts/nomention_court.py" "courts/clockforms_court.py" "courts/mixedunits_court.py" "courts/dateforms_court.py" "courts/clockwords_court.py" "courts/speedforms_court.py" "courts/roundforms_court.py" "courts/orderforms_court.py" "courts/quantforms_court.py" "courts/roman_court.py" "courts/place_court.py" "courts/unitfrac_court.py" "courts/enough_court.py" "courts/numphrase_court.py" "courts/kinbearer_court.py" "courts/pronobject_court.py" "courts/proform_court.py" "courts/degrees_court.py" "courts/actturn_court.py" "courts/tempscale_court.py" "courts/action_measure_court.py" "courts/numberline_court.py" "courts/countfacts_court.py" "courts/letters_court.py" "courts/langcount_court.py" "courts/propcompare_court.py" "courts/price_court.py" "courts/translate_court.py" "courts/timeunits_court.py" "courts/svamp_court.py" "courts/measure_langs_court.py"
        # ВОСЕМЬ МИРОВ ЛЕСТНИЦЫ (14.09, ступени 1 и 2, просьба holon-f9): цель, сказанная
        # речью; деление как дело без носителя; скобки; булевы выражения; азбучный порядок;
        # слежение за вещами через обмен; многошаговый счёт; DROP одним миром. Всякий из них
        # замкнут на себя (`closedworld`) и всякий ловит подсадки, объявленные в самом суде.
        "courts/goal_court.py" "courts/equalshare_court.py" "courts/dyck_court.py"
        "courts/boolexpr_court.py" "courts/alphaorder_court.py" "courts/handover_court.py"
        "courts/nestcalc_court.py" "courts/drop_court.py"
        # ДВУСТОРОННЯЯ СВЯЗЬ — «только если» и «тогда и только тогда», купленные нулём:
        # корпус 162 раза звал обращение импликации ошибкой и ни разу не показал, когда
        # оно верно. Суд выводит вид связи ОБХОДОМ РЯДА, а не берёт его у дома.
        "courts/bicond_court.py"
        # ЧТЕНИЕ ТАБЛИЦЫ — ещё один ноль пробы: «на пересечении» 0 строк при 3 085
        # упоминаниях слова «таблица» как имени чужой вещи. Суд строит таблицу заново
        # по записи и отказывает вопросу, у какого два ответа.
        "courts/grid_court.py"
        # ОКРУГЛЕНИЕ ПО ДЕЛУ — третий ноль пробы: округление ВВЕРХ в своде было (77 строк),
        # ВНИЗ не было вовсе, а обе стороны рядом — нигде. Суд не знает рода страницы: он
        # смотрит, какая рамка совпала, и тем узнаёт, что́ обещано.
        "courts/roundneed_court.py"
        # СРАВНЕНИЕ ДАТ — четвёртый ноль пробы: «какая дата» 0 строк при 480 страницах
        # счёта дней. Суд собирает страницу заново ЦЕЛИКОМ — и раннюю дату, и причину:
        # ответ без причины не есть ответ.
        "courts/datecmp_court.py"
        # ДЕЛО НАД БУКВАМИ — пятый ноль пробы: палиндром, анаграмма и сдвиг — по нулю
        # строк при 360 страницах СЧЁТА букв. Азбука взята у дома азбучного порядка, а
        # не объявлена вторым списком; перенос через край азбуки показан, а не умолчан.
        "courts/letterwork_court.py"
        # РАССАДКА ПО ОГРАНИЧЕНИЯМ — шестой ноль пробы: «кто где живёт» 0 строк. Суд
        # перебирает все шесть рассадок и требует ЕДИНСТВЕННОСТИ и НАИМЕНЬШЕГО набора:
        # задача с двумя решениями не есть задача, а лишнее условие не учит ничему.
        "courts/whodwells_court.py"
        # ТРИ НОЛЯ ПРОБЫ ПОДРЯД: два процента (второй берётся не от того же числа),
        # путь по дорогам (связь передаётся, а близость нет) и совпадение против
        # причины (числа говорят, что было, и молчат о том, почему).
        "courts/pctchain_court.py" "courts/roadpath_court.py"
        "courts/cooccur_court.py"
        # ЧИСЛО СЛОВОМ (21.09) — история, писанная словами, и выкладка, писанная цифрами:
        # страница учит РАВЕНСТВУ ДВУХ ПИСЕМ. До неё строк с количеством, названным словом,
        # было НОЛЬ на 471 605, и читатель, знавший число только цифрой, не узнавал его
        # словом. Замер соседа (holon-87, ключ ASDiv классов 1–2): 224 строки из 513 несут
        # числа словами.
        "courts/wordnum_court.py"
        # КОШЕЛЁК (21.09) — деньги как величина, которую тратят и которая остаётся. Свод
        # считал ЦЕНУ и не считал кошелька: покупка с остатком денег — НОЛЬ строк из
        # 471 605. ВЕЛИЧИНА, КОТОРУЮ ЧИТАТЕЛЬ ВИДЕЛ ТОЛЬКО ОТВЕТОМ, НЕ ОПОЗНАЁТСЯ ИМ В
        # ВОПРОСЕ.
        "courts/wallet_court.py"
        # МЕРА СВОЙСТВА (21.09) — свойство, названное ЧИСЛОМ, а не именем. Свод умел
        # сравнить свойство и не умел измерить: форма «X есть N единиц глубиной» стояла 86
        # раз, и все восемьдесят шесть по-английски об одном предмете.
        "courts/propmeasure_court.py"
        # ДВОЙНИК ЧИСЛА (21.09) — цифра и слово как равные: «40 — это сорок». Миров с
        # двойником у свода не было ни одного, и читатель, встречая цепь двадцаток, ценил
        # звено НОМЕРОМ В ЦЕПИ: «сорок» становилось двойкой, «сто» — пятёркой.
        "courts/numtwin_court.py"
        # ДВЕ РАМКИ НА ОДНОЙ ЗАПИСИ — порок, какого не видит ни один суд: он зелен,
        # покрытие полно, ложных нет, а род решается ПОРЯДКОМ ПЕРЕБОРА рамок, то есть
        # случайностью записи в дереве. Куплен домом двух процентов в тот же час.
        "scripts/frames_apart.py"
        # ОЧЕРТАНИЯ РОДА — тот же порок с другого конца: род, богатый страницами и
        # бедный очертаниями, повторяет одну мысль числами. Перекос дома видит это
        # лишь при двадцатикратности; здесь видно вчетверо раньше.
        "scripts/genus_shapes.py"
        # ПОДСАДКИ ВНЕ РАМКИ — прибор, купленный этой самой потерей: суд скобок доложил
        # «поймано 4 из 7», умолчав, что три строки он больше НЕ ЧИТАЕТ. Прибор читает все
        # объявления подсадок деревом разбора и спрашивает судимость у ПАЛАТЫ.
        "scripts/plants_read.py"
        # ПРОБА НА НОЛЬ — семейства дел, о каких свод не говорит ни строки. Рубеж здесь
        # РАСТЁТ: купленное не смеет вернуться в ноль. Мир, снятый с ковки или сломанный
        # переездом дома, уносит целое УМЕНИЕ, а покрытие считает строки и молчит.
        "scripts/zero_probe.py"
        # СТРАЖ ЧАСТНОГО ИТОГА — ПОСЛЕДНИМ, И ЭТО НЕ ПОРЯДОК, А УСЛОВИЕ МЕРЫ: он
        # судит СЛЕД ЭТОГО ЖЕ ПРОГОНА (reports/SUITE-TRACE.tsv, пишется по ходу), и
        # всякое место раньше конца дало бы ему неполный след. Дорогой прибор,
        # молчащий до самого вердикта, при обрыве отдаёт своду ноль байт за все
        # свои часы.
        "scripts/partial_guard.py")
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
  # ПОДСТАНОВКА КОМАНДЫ УБРАНА, И ЭТО КОРЕНЬ БЕДЫ СИРОТ (12.09, чистой мерой). `out=$(python3
  # …)` заводит ЕЩЁ ОДНУ оболочку между сторожем и питоном, и она несёт ТУ ЖЕ командную строку
  # набора — значит, `pkill -f` бьёт и по ней. Она умирает без обработчика, и питон остаётся
  # сиротой при init.
  #
  #     ЛИШНЯЯ ОБОЛОЧКА МЕЖДУ СТОРОЖЕМ И ДЕЛОМ ЕСТЬ ЛИШНЕЕ МЕСТО, ГДЕ ЦЕПЬ РВЁТСЯ.
  #
  # Ныне вывод идёт прямо в файл, питон запускается ФОНОМ и ждётся по имени: bash, стоящий в
  # `wait`, берёт сигнал НЕМЕДЛЕННО, а ждущий переднего дела — лишь по его окончании. Ловушка
  # берёт питона поимённо, а не надеется на группу.
  # ИМЯ ПЕРЕМЕННОЙ — ЛАТИНИЦЕЙ: bash 3.2 (тот, что несёт macOS) не берёт кириллицу в
  # имя и падает с «not a valid identifier». Точка сама писала этот закон строкою выше —
  # и я его нарушил, а прежние опыты дали от того числа 84 и 93 вместо истины.
  #
  #     СКРИПТ ПИШЕТСЯ ТЕМ ЯЗЫКОМ, КОТОРЫЙ ЕГО ЧИТАЕТ, А НЕ ТЕМ, КОТОРЫМ ЕГО ДУМАЮТ.
  # ВЫВОД ИДЁТ НЕБУФЕРИЗОВАННЫМ (`-u`), И ЭТО КУПЛЕНО ЗАМЕРОМ (12.09).
  #
  # CPython, чей stdout перенаправлен в ФАЙЛ, буферизует его блоками по 8 КБ.
  # Замер: скрипт, печатающий строку каждые 50 мс, снятый через две секунды,
  # оставил РОВНО НОЛЬ БАЙТ; он же под `-u` — 34 строки и 3 424 байта.
  #
  #     ОБОРВАННЫЙ ПРИБОР ТЕРЯЛ НЕ ТОЛЬКО ВЕРДИКТ, НО И ВСЮ РАБОТУ — даже тот,
  #     что честно печатал по ходу дела. Буфер стирал частный итог вернее, чем
  #     привычка печатать в конце: та хоть видна в исходнике, а этот невидим.
  #
  # Отсюда же поправка к ночному закону «прибор, печатающий только в конце,
  # оставляет по обрыве 0 байт»: печатать по ходу было НЕДОСТАТОЧНО, покуда
  # набор не просил вывода без буфера.
  local idx entry tool rc t0 t1 pypid watchpid
  idx="$1"; entry="$2"
  set -- $entry; tool="$1"; shift
  t0=$(date +%s)
  python3 -u "$tool" "$@" > "$TMPDIR_SUITE/$idx.out" 2>&1 &
  pypid=$!
  # СТОРОЖ ПЕРВОЙ СТРОКИ: сколько секунд прибор молчал, прежде чем сказал первое
  # слово. Число это — мера ЧАСТНОГО ИТОГА: прибор, молчащий до самого конца,
  # при обрыве не оставляет ничего, сколько бы часов он ни шёл. Судит его
  # `scripts/partial_guard.py`; здесь лишь замер, и он идёт на настоящем прогоне,
  # а не на лишнем — мера, требующая второго прогона, меряет второй прогон.
  ( while kill -0 "$pypid" 2>/dev/null; do
      [ -s "$TMPDIR_SUITE/$idx.out" ] && break
      sleep 1
    done
    printf '%s\n' "$(( $(date +%s) - t0 ))" > "$TMPDIR_SUITE/$idx.first" ) &
  watchpid=$!
  trap 'kill -TERM '"$pypid"' 2>/dev/null; exit 143' TERM INT
  wait "$pypid"; rc=$?
  trap - TERM INT
  wait "$watchpid" 2>/dev/null
  t1=$(date +%s)
  printf '%s\n' "$((t1 - t0))" > "$TMPDIR_SUITE/$idx.sec"
  printf '%s
' "$rc" > "$TMPDIR_SUITE/$idx.rc"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$TMPDIR_SUITE/$idx.ts"
}

FELL=0
TORN=0
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
  local k last_idx entry tool rc stamp out last sec first lines
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
    # ОБРЫВ НЕ ЕСТЬ СУД, И В ЛЕДЖЕР НЕ ИДЁТ (12.09).
    #
    # Файла `.rc` нет ровно в одном случае: `run_one` не дожил до его записи — прибор
    # убит сигналом, либо набор прерван рукой. Прежде здесь стояло `|| echo 2`, и
    # родитель писал в леджер СТРОКУ СУДА: код 2, вердикт пуст. Замер 12.09: строк
    # леджера 7 997, из них с ПУСТЫМ вердиктом 1 982 (24%), из них 1 966 — за один
    # день; приборов, чья ПОСЛЕДНЯЯ строка есть такой обрыв, — 221 из 316, при девяти
    # действительно павших. Читатели леджера (`crystal.py`, `denominator_census.py`,
    # точка) принимали это за вердикт: точка объявила «пало 311 из 311» о наборе,
    # который не судил НИ РАЗУ.
    #
    #     ЗАПИСЬ ОБ ОБРЫВЕ, НЕОТЛИЧИМАЯ ОТ ЗАПИСИ О СУДЕ, ХУЖЕ МОЛЧАНИЯ: молчание
    #     видно, а такая запись КРАСНА И ПРАВДОПОДОБНА. Это тот же род беды, что
    #     «вердикт, принадлежащий соседу», — но наоборот: не чужой зелёный, а СВОЙ
    #     КРАСНЫЙ ЗА РАБОТУ, КОТОРОЙ НЕ БЫЛО.
    #
    # Ныне обрыв называется вслух, считается отдельно и в леджер не пишется: леджер
    # есть запись СУДОВ. Прибор, оборванный на дереве, где его прежний вердикт зелён,
    # при следующем `--продолжить` законно пропустится — дерево не двигалось.
    if [ ! -f "$TMPDIR_SUITE/$k.rc" ]; then
      printf 'СУД ОБОРВАН %-24s (кода не оставил — прерван, не судил)\n' "$(basename "$tool")"
      TORN=$((TORN+1))
      k=$((k+1))
      continue
    fi
    rc=$(cat "$TMPDIR_SUITE/$k.rc")
    # СНЯТЫЙ СИГНАЛОМ ЕСТЬ ТОТ ЖЕ ОБРЫВ, ХОТЬ И С КОДОМ (12.09, вечер, поймано на живом деле).
    #
    # Первая редакция этого места узнавала обрыв по ОТСУТСТВИЮ файла с кодом — так выглядит
    # снятый `run_one`. Но когда снимают САМОГО ПИТОНА, `run_one` доживает до конца и честно
    # пишет код 143 (128 + SIGTERM), а вердикт остаётся пуст. В леджер легла строка
    # «arith_court.py 143» — с виду суд, сказавший FAIL, на деле прибор, убитый на 285-й
    # секунде и не сказавший ни слова.
    #
    #     ПРИЗНАК ОБРЫВА, ВЗЯТЫЙ ПО ОДНОМУ ЕГО ВИДУ, ПРОПУСКАЕТ ВТОРОЙ. Обрыв узнаётся не тем,
    #     ЧЕГО прибор не оставил, а тем, ЧТО он оставил: код снятия (>= 128) есть снятие,
    #     кем бы оно ни было послано.
    if [ "$rc" -ge 128 ] 2>/dev/null; then
      printf 'СУД ОБОРВАН %-24s (снят сигналом, rc=%s — не судил)\n' "$(basename "$tool")" "$rc"
      TORN=$((TORN+1))
      k=$((k+1))
      continue
    fi
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
    # СЛЕД ЧАСТНОГО ИТОГА — СВОЙ ФАЙЛ, А НЕ ПЯТОЕ ПОЛЕ ЧУЖОГО: у следа цены свой
    # договор о трёх полях, и `court_catch` с `crystal` читают его по местам.
    # Поля: метка, имя, секунд всего, секунд до ПЕРВОЙ строки, строк вывода.
    first=$(cat "$TMPDIR_SUITE/$k.first" 2>/dev/null || echo -1)
    lines=$(printf '%s\n' "$out" | grep -c . || true)
    printf '%s\t%s\t%s\t%s\t%s\n' "$stamp" "$(basename "$tool")" "$sec" "$first" "$lines" \
      >> reports/SUITE-TRACE.tsv
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
    # ОДИНОЧНЫЙ ПРИБОР ИДЁТ ФОНОВОЙ ЗАДАЧЕЙ, ХОТЬ И ОДИН (12.09, чистой мерой). Прежде он
    # шёл В ПЕРЕДНЕМ ПЛАНЕ, и ловушка набора НЕ СРАБАТЫВАЛА ВОВСЕ: bash, ожидающий переднего
    # дела, откладывает обработчик до его конца, а снятый родитель оставляет питона при init.
    #
    #     ЛОВУШКА, ЖДУЩАЯ КОНЦА ТОГО, ОТ ЧЕГО СТЕРЕЖЁТ, НЕ СТЕРЕЖЁТ.
    #
    # Замерено СПИСКОМ ПОТОМКОВ этого самого набора, а не образцом командной строки: прежде
    # переживал снятие ровно один потомок из двух — питон одиночного суда.
    #
    #     МЕРА ПО ОБРАЗЦУ СТРОКИ СЧИТАЕТ ЧУЖОЕ; МЕРА ПО СПИСКУ ПОТОМКОВ НЕ МОЖЕТ ОШИБИТЬСЯ.
    #
    # `wait` держит исключительность — рядом по-прежнему никто не идёт, — а ловушка набора
    # успевает отработать, ибо ждущий `wait` bash берёт сигнал немедленно.
    run_one "$i" "$entry" &
    wait
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
# ОБОРВАННОЕ НАЗЫВАЕТСЯ ВСЛУХ ТОЧНО ТАК ЖЕ, И ПО ТОЙ ЖЕ ПРИЧИНЕ: прогон, молчащий об
# оборванном, отчитывается за работу, которой не было, — только красным, а не зелёным.
if [ "$TORN" -gt 0 ]; then
  echo "СУДЫ КОРПУСА: ОБОРВАНО $TORN из ${#COURTS[@]} — не судили и в леджер не писаны"
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
# ПОЗА СЛЕДА РАЗЛИЧАЕТ ПАДЕНИЕ И ОБРЫВ: «ПАЛО» есть суд, сказавший FAIL; «ОБОРВАН»
# есть набор, не досчитанный до конца. Полей по-прежнему четыре — договор со `point.sh`
# не тронут, третье поле остаётся числом ПАВШИХ, а не суммой павших с оборванными.
printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "$([ "$FELL" != 0 ] && echo ПАЛО || { [ "$TORN" != 0 ] && echo ОБОРВАН || echo ЦЕЛ; })" \
  "$FELL" "${#COURTS[@]}" \
  > reports/SUITE-LAST.tsv
exit $(( (FELL > 0) || (TORN > 0) ))
