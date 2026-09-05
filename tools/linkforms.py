#!/usr/bin/env python3
"""ДОМ СВЯЗОК РАЗГОВОРА — вопрос, ссылающийся на СКАЗАННОЕ.

Заказ владельца (04.09, через holon, п.5): беседа — не набор пар
«вопрос-ответ». Ей нужен вопрос, чей предмет стоит в ПРЕДЫДУЩЕЙ реплике:
«а почему?», «а если наоборот?», «что дальше?», «правда ли?», «согласен ли
ты?». Полоса БЕСЕДА-100 меряет этот род немым ПОЛНОСТЬЮ: 15 из 15.

Дом ставит связку так, чтобы она осталась ПРОВЕРЯЕМОЙ. Это главное решение
здесь и оно не косметическое: «согласен ли ты?» о вкусе не судится ничем, а
«согласен ли ты?» о СЧЁТЕ судится пересчётом. Потому всякая связка этого
дома цепляется к факту с числом, и ответ несёт кузницу:

  ПОЧЕМУ      «у ани было 7 яблок. аня отдала 2 яблока. у ани 5 яблок.
               почему у ани 5 яблок? потому что было 7 и отдано 2: 7 − 2 = 5.»
  А ЕСЛИ      «у ани 5 яблок. а если бы их было вдвое больше? тогда у ани
               было бы 10 яблок: 5 × 2 = 10.»
  ЧТО ДАЛЬШЕ  «у ани 5 яблок. аня получила 3 яблока. что дальше? у ани
               8 яблок: 5 + 3 = 8.»
  ПРАВДА ЛИ   «у ани 5 яблок. правда ли это? да, у ани 5 яблок.»
  НЕПРАВДА    «у ани 5 яблок. правда ли, что у ани 9 яблок? нет, у ани
               5 яблок.» — вторая полярность, без которой «да» ничего не стоит.
  ПЕРЕСПРОС   «у ани 5 яблок. ты имеешь в виду 5 яблок? да, 5 яблок.»
  СОГЛАСЕН    «у ани 5 яблок. согласен ли ты? да, я согласен: у ани 5 яблок.»

СЛОВАРЬ НЕ ОБЪЯВЛЯЕТСЯ ЗАНОВО: имена, товары и их формы счёта берутся из
дома страниц действия — два дома, один словарь (тот же ход, что у дома
сочленений). Языков здесь ДЕВЯТЬ — все девять языков атаки. Голландский вошёл парой
«один/много»; польскому пары было мало (у него ТРИ формы при числе: 1 piłka,
2 piłki, 5 piłek), и потому в тот же час написан дом польского счёта
`tools/plgram.py` — тот же по устройству, что русский. Долг, названный утром,
погашен к вечеру.

    python3 tools/linkforms.py    # самопроверка с мутантами
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402
import json as _json

# ЧИСЛИТЕЛЬНЫЕ СЛОВАМИ БЕРУТСЯ ИЗ ПАКЕТА ЯЗЫКА, а не объявляются здесь заново:
# пакет — источник истины о слове языка, и второй список разошёлся бы с ним.
_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"


def _числительные(язык):
    п = _json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return {int(k): v for k, v in (п.get("numerals") or {}).items() if str(k).isdigit()}


ЧИСЛА_СЛОВОМ = {}
# ТАБЛИЦА УМНОЖЕНИЯ СЛОВАМИ: маленькая, вся в пределах объявленных числительных
ТАБЛИЦА = ((2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 5))

ФОРМЫ = ("почему", "почему_голый", "а_у", "а_если", "наоборот", "наоборот2", "а_союз", "повтори", "объясни", "объясни2", "объясни3", "счёт_да", "что_дальше", "правда", "неправда", "сказал_что", "переспрос", "согласен")

ЯЗЫКИ = {
    "en": dict(
        было="{X} had {n} {Тn}.", отдал="{X} gave away {k} {Тk}.", стало="{X} has {r} {Тr}.",
        получил="{X} got {k} {Тk}.",
        почему_голый="why? because {X} had {n} and gave away {k}: {л}",
        а_у="how many does {Y} have? {Y} has {m} {Тm}.",
        наоборот="{X} has {n} {Тn}, {Y} has {m} {Тm}. what if it were the other way round? then {X} would have {m} {Тm} and {Y} would have {n} {Тn}.",
        повтори="say that again, please. i repeat: {X} has {n} {Тn}.",
        объясни="i do not understand, explain. i explain: {X} had {n}, gave away {k}, and has {r} left: {л}",
        объясни3="i did not understand, explain it again. i explain again: {X} had {n}, gave away {k}, and has {r} left: {л}",
        сказал_что="you said that {X} has {м} {Тм}. is that right? no, {X} has {n} {Тn}.",
        а_союз="and {Y}? {Y} has {m} {Тm}.",
        # ВТОРАЯ ПОВЕРХНОСТЬ ЖИЛА ТОЛЬКО ПО-АНГЛИЙСКИ, и это нашёл прибор
        # щербатости (форма × язык): «объясни2» и «наоборот2» стояли на одном
        # языке из девяти — не по закону, а по недосмотру, и потому дописаны
        # на все девять. Вариация у каждой своя и естественная: у объяснения
        # переставлена вежливость («объясни, пожалуйста: я не понял»), у
        # обращения — голова вопроса («что если наоборот?» при «а если
        # наоборот?»). Вторая поверхность есть то, чем рынок отличает ФОРМУ от
        # строки; одна на девять языков этого не даёт.
        объясни2="i don't understand, explain. i explain: {X} had {n}, gave away {k}, and has {r} left: {л}",
        наоборот2="{X} has {n} {Тn}, {Y} has {m} {Тm}. and if it were the other way round? then {X} would have {m} {Тm} and {Y} would have {n} {Тn}.",
        счёт_да="is it true that {A} times {B} is {C}? yes, {A} times {B} is {C}: {a} × {b} = {c}.",
        счёт_нет="is it true that {A} times {B} is {D}? no, {A} times {B} is {C}: {a} × {b} = {c}.",
        почему="why does {X} have {r} {Тr}? because {X} had {n} and gave away {k}: {л}",
        а_если="what if there were twice as many? then {X} would have {д} {Тд}: {лд}",
        что_дальше="what happens next? {X} has {r} {Тr}: {л}",
        правда="is that true? yes, {X} has {n} {Тn}.",
        неправда="is it true that {X} has {м} {Тм}? no, {X} has {n} {Тn}.",
        переспрос="do you mean {n} {Тn}? yes, {n} {Тn}.",
        согласен="do you agree? yes, i agree: {X} has {n} {Тn}.",
    ),
    "ru": dict(
        было="у {Xр} было {n} {Тn}.", отдал="{X} отдал{а} {k} {Твk}.", стало="у {Xр} {r} {Тr}.",
        получил="{X} получил{а} {k} {Твk}.",
        почему_голый="почему? потому что было {n}, а отдано {k}: {л}",
        а_у="сколько у {Yр}? у {Yр} {m} {Тm}.",
        наоборот2="у {Xр} {n} {Тn}, у {Yр} {m} {Тm}. что если наоборот? тогда у {Xр} {m} {Тm}, а у {Yр} {n} {Тn}.",
        объясни2="объясни, пожалуйста: я не понял. объясняю: было {n}, отдано {k}, осталось {r}: {л}",
        наоборот="у {Xр} {n} {Тn}, у {Yр} {m} {Тm}. а если наоборот? тогда у {Xр} {m} {Тm}, а у {Yр} {n} {Тn}.",
        повтори="повтори, пожалуйста. повторяю: у {Xр} {n} {Тn}.",
        объясни="я не понял, объясни. объясняю: было {n}, отдано {k}, осталось {r}: {л}",
        объясни3="я не понял, объясни ещё раз. объясняю ещё раз: было {n}, отдано {k}, осталось {r}: {л}",
        сказал_что="ты сказал, что у {Xр} {м} {Тм}. это верно? нет, у {Xр} {n} {Тn}.",
        а_союз="а у {Yр}? у {Yр} {m} {Тm}.",
        счёт_да="правда ли, что {A}жды {B} — {C}? да, {A}жды {B} — {C}: {a} × {b} = {c}.",
        счёт_нет="правда ли, что {A}жды {B} — {D}? нет, {A}жды {B} — {C}: {a} × {b} = {c}.",
        # ВТОРАЯ ПОВЕРХНОСТЬ ТОЙ ЖЕ ФОРМЫ — БЕЗ СВЯЗОЧНОГО ТИРЕ. Полоса беседы
        # держала немой строку «правда ли, что дважды два четыре?», и корпус
        # нёс её же С ТИРЕ: тире есть знак ПИСЬМА, которого нет в речи, и
        # человек, пишущий бегло, его не ставит. Рынок, купивший рамку с тире,
        # не узнает ту же рамку без него — тире для него слово рамки.
        #
        # ЭТО ПОВЕРХНОСТЬ, А НЕ ФОРМА, и потому у прочих языков её нет и быть
        # не может: их связка есть СЛОВО («is», «ist», «to», «fa»), а слово не
        # опускается. Второй поверхностью, а не второй формой, дом обходится
        # без объявленного пропуска на восемь языков.
        счёт_да2="правда ли, что {A}жды {B} {C}? да, {A}жды {B} {C}: {a} × {b} = {c}.",
        счёт_нет2="правда ли, что {A}жды {B} {D}? нет, {A}жды {B} {C}: {a} × {b} = {c}.",
        почему="почему у {Xр} {r} {Тr}? потому что было {n}, а отдано {k}: {л}",
        а_если="а если бы их было вдвое больше? тогда у {Xр} было бы {д} {Тд}: {лд}",
        что_дальше="что дальше? у {Xр} {r} {Тr}: {л}",
        правда="правда ли это? да, у {Xр} {n} {Тn}.",
        неправда="правда ли, что у {Xр} {м} {Тм}? нет, у {Xр} {n} {Тn}.",
        переспрос="ты имеешь в виду {n} {Тn}? да, {n} {Тn}.",
        согласен="согласен ли ты? да, я согласен: у {Xр} {n} {Тn}.",
    ),
    "de": dict(
        было="{X} hatte {n} {Тn}.", отдал="{X} gab {k} {Тk} weg.", стало="{X} hat {r} {Тr}.",
        получил="{X} bekam {k} {Тk}.",
        почему_голый="warum? weil {X} {n} hatte und {k} weggab: {л}",
        а_у="wie viele hat {Y}? {Y} hat {m} {Тm}.",
        наоборот2="{X} hat {n} {Тn}, {Y} hat {m} {Тm}. was wäre, wenn es umgekehrt wäre? dann hätte {X} {m} {Тm} und {Y} {n} {Тn}.",
        объясни2="erkläre es bitte: ich habe es nicht verstanden. ich erkläre: es waren {n}, {k} wurden weggegeben, es bleiben {r}: {л}",
        наоборот="{X} hat {n} {Тn}, {Y} hat {m} {Тm}. und wenn es umgekehrt wäre? dann hätte {X} {m} {Тm} und {Y} {n} {Тn}.",
        повтори="sag das bitte noch einmal. ich wiederhole: {X} hat {n} {Тn}.",
        объясни="ich habe es nicht verstanden, erkläre es. ich erkläre: es waren {n}, {k} wurden weggegeben, es bleiben {r}: {л}",
        объясни3="ich habe es nicht verstanden, erkläre es noch einmal. ich erkläre noch einmal: es waren {n}, {k} wurden weggegeben, es bleiben {r}: {л}",
        сказал_что="du hast gesagt, dass {X} {м} {Тм} hat. stimmt das? nein, {X} hat {n} {Тn}.",
        а_союз="und {Y}? {Y} hat {m} {Тm}.",
        счёт_да="stimmt es, dass {A} mal {B} {C} ist? ja, {A} mal {B} ist {C}: {a} × {b} = {c}.",
        счёт_нет="stimmt es, dass {A} mal {B} {D} ist? nein, {A} mal {B} ist {C}: {a} × {b} = {c}.",
        счёт_да2="stimmt es, dass {A}mal {B} {C} ist? ja, {A}mal {B} ist {C}: {a} × {b} = {c}.",
        счёт_нет2="stimmt es, dass {A}mal {B} {D} ist? nein, {A}mal {B} ist {C}: {a} × {b} = {c}.",
        почему="warum hat {X} {r} {Тr}? weil {X} {n} hatte und {k} weggab: {л}",
        а_если="und wenn es doppelt so viele wären? dann hätte {X} {д} {Тд}: {лд}",
        что_дальше="was kommt dann? {X} hat {r} {Тr}: {л}",
        правда="stimmt das? ja, {X} hat {n} {Тn}.",
        неправда="stimmt es, dass {X} {м} {Тм} hat? nein, {X} hat {n} {Тn}.",
        переспрос="meinst du {n} {Тn}? ja, {n} {Тn}.",
        согласен="stimmst du zu? ja, ich stimme zu: {X} hat {n} {Тn}.",
    ),
    "es": dict(
        было="{X} tenía {n} {Тn}.", отдал="{X} dio {k} {Тk}.", стало="{X} tiene {r} {Тr}.",
        получил="{X} recibió {k} {Тk}.",
        почему_голый="¿por qué? porque {X} tenía {n} y dio {k}: {л}",
        а_у="¿cuántas tiene {Y}? {Y} tiene {m} {Тm}.",
        наоборот2="{X} tiene {n} {Тn}, {Y} tiene {m} {Тm}. ¿qué pasaría si fuera al revés? entonces {X} tendría {m} {Тm} y {Y} tendría {n} {Тn}.",
        объясни2="explícalo, por favor: no lo he entendido. explico: había {n}, se dieron {k}, quedan {r}: {л}",
        наоборот="{X} tiene {n} {Тn}, {Y} tiene {m} {Тm}. ¿y si fuera al revés? entonces {X} tendría {m} {Тm} y {Y} tendría {n} {Тn}.",
        повтори="repite, por favor. repito: {X} tiene {n} {Тn}.",
        объясни="no lo he entendido, explícalo. explico: había {n}, se dieron {k}, quedan {r}: {л}",
        объясни3="no entendí, explícalo otra vez. explico otra vez: había {n}, se dieron {k}, quedan {r}: {л}",
        сказал_что="dijiste que {X} tiene {м} {Тм}. ¿es cierto? no, {X} tiene {n} {Тn}.",
        а_союз="¿y {Y}? {Y} tiene {m} {Тm}.",
        счёт_да="¿es verdad que {A} por {B} es {C}? sí, {A} por {B} es {C}: {a} × {b} = {c}.",
        счёт_нет="¿es verdad que {A} por {B} es {D}? no, {A} por {B} es {C}: {a} × {b} = {c}.",
        почему="¿por qué {X} tiene {r} {Тr}? porque {X} tenía {n} y dio {k}: {л}",
        а_если="¿y si hubiera el doble? entonces {X} tendría {д} {Тд}: {лд}",
        что_дальше="¿qué pasa después? {X} tiene {r} {Тr}: {л}",
        правда="¿es verdad? sí, {X} tiene {n} {Тn}.",
        неправда="¿es verdad que {X} tiene {м} {Тм}? no, {X} tiene {n} {Тn}.",
        переспрос="¿quieres decir {n} {Тn}? sí, {n} {Тn}.",
        согласен="¿estás de acuerdo? sí, estoy de acuerdo: {X} tiene {n} {Тn}.",
    ),
    "fr": dict(
        было="{X} avait {n} {Тn}.", отдал="{X} a donné {k} {Тk}.", стало="{X} a {r} {Тr}.",
        получил="{X} a reçu {k} {Тk}.",
        почему_голый="pourquoi ? parce que {X} en avait {n} et en a donné {k} : {л}",
        а_у="combien en a {Y} ? {Y} a {m} {Тm}.",
        наоборот2="{X} a {n} {Тn}, {Y} a {m} {Тm}. que se passerait-il si c'était l'inverse ? alors {X} aurait {m} {Тm} et {Y} aurait {n} {Тn}.",
        объясни2="explique, s'il te plaît : je n'ai pas compris. j'explique : il y en avait {n}, {k} ont été donnés, il en reste {r} : {л}",
        наоборот="{X} a {n} {Тn}, {Y} a {m} {Тm}. et si c'était l'inverse ? alors {X} aurait {m} {Тm} et {Y} aurait {n} {Тn}.",
        повтори="répète, s'il te plaît. je répète : {X} a {n} {Тn}.",
        объясни="je n'ai pas compris, explique. j'explique : il y en avait {n}, {k} ont été donnés, il en reste {r} : {л}",
        объясни3="je n'ai pas compris, explique encore une fois. j'explique encore une fois : il y en avait {n}, {k} ont été donnés, il en reste {r} : {л}",
        сказал_что="tu as dit {que}{X} a {м} {Тм}. c'est vrai ? non, {X} a {n} {Тn}.",
        а_союз="et {Y} ? {Y} a {m} {Тm}.",
        счёт_да="est-il vrai que {A} fois {B} font {C} ? oui, {A} fois {B} font {C} : {a} × {b} = {c}.",
        счёт_нет="est-il vrai que {A} fois {B} font {D} ? non, {A} fois {B} font {C} : {a} × {b} = {c}.",
        почему="pourquoi {X} a {r} {Тr} ? parce que {X} en avait {n} et en a donné {k} : {л}",
        а_если="et s'il y en avait deux fois plus ? alors {X} aurait {д} {Тд} : {лд}",
        что_дальше="que se passe-t-il ensuite ? {X} a {r} {Тr} : {л}",
        правда="est-ce vrai ? oui, {X} a {n} {Тn}.",
        неправда="est-il vrai que {X} a {м} {Тм} ? non, {X} a {n} {Тn}.",
        переспрос="tu veux dire {n} {Тn} ? oui, {n} {Тn}.",
        согласен="es-tu d'accord ? oui, je suis d'accord : {X} a {n} {Тn}.",
    ),
    "it": dict(
        было="{X} aveva {n} {Тn}.", отдал="{X} ha dato {k} {Тk}.", стало="{X} ha {r} {Тr}.",
        получил="{X} ha ricevuto {k} {Тk}.",
        почему_голый="perché? perché {X} aveva {n} e ha dato {k}: {л}",
        а_у="quante ne ha {Y}? {Y} ha {m} {Тm}.",
        наоборот2="{X} ha {n} {Тn}, {Y} ha {m} {Тm}. che cosa succederebbe se fosse il contrario? allora {X} avrebbe {m} {Тm} e {Y} avrebbe {n} {Тn}.",
        объясни2="spiega, per favore: non ho capito. spiego: ce n'erano {n}, {k} sono stati dati, ne restano {r}: {л}",
        наоборот="{X} ha {n} {Тn}, {Y} ha {m} {Тm}. e se fosse il contrario? allora {X} avrebbe {m} {Тm} e {Y} avrebbe {n} {Тn}.",
        повтори="ripeti, per favore. ripeto: {X} ha {n} {Тn}.",
        объясни="non ho capito, spiega. spiego: ce n'erano {n}, {k} sono stati dati, ne restano {r}: {л}",
        объясни3="non ho capito, spiegalo ancora una volta. spiego ancora una volta: ce n'erano {n}, {k} sono stati dati, ne restano {r}: {л}",
        сказал_что="hai detto che {X} ha {м} {Тм}. è giusto? no, {X} ha {n} {Тn}.",
        а_союз="e {Y}? {Y} ha {m} {Тm}.",
        счёт_да="è vero che {A} per {B} fa {C}? sì, {A} per {B} fa {C}: {a} × {b} = {c}.",
        счёт_нет="è vero che {A} per {B} fa {D}? no, {A} per {B} fa {C}: {a} × {b} = {c}.",
        почему="perché {X} ha {r} {Тr}? perché {X} aveva {n} e ha dato {k}: {л}",
        а_если="e se fossero il doppio? allora {X} avrebbe {д} {Тд}: {лд}",
        что_дальше="che cosa succede dopo? {X} ha {r} {Тr}: {л}",
        правда="è vero? sì, {X} ha {n} {Тn}.",
        неправда="è vero che {X} ha {м} {Тм}? no, {X} ha {n} {Тn}.",
        переспрос="intendi {n} {Тn}? sì, {n} {Тn}.",
        согласен="sei d'accordo? sì, sono d'accordo: {X} ha {n} {Тn}.",
    ),
    "pt": dict(
        было="{X} tinha {n} {Тn}.", отдал="{X} deu {k} {Тk}.", стало="{X} tem {r} {Тr}.",
        получил="{X} recebeu {k} {Тk}.",
        почему_голый="porquê? porque {X} tinha {n} e deu {k}: {л}",
        а_у="quantas tem {Y}? {Y} tem {m} {Тm}.",
        наоборот2="{X} tem {n} {Тn}, {Y} tem {m} {Тm}. o que aconteceria se fosse ao contrário? então {X} teria {m} {Тm} e {Y} teria {n} {Тn}.",
        объясни2="explica, por favor: não percebi. explico: havia {n}, {k} foram dados, restam {r}: {л}",
        наоборот="{X} tem {n} {Тn}, {Y} tem {m} {Тm}. e se fosse ao contrário? então {X} teria {m} {Тm} e {Y} teria {n} {Тn}.",
        повтори="repete, por favor. repito: {X} tem {n} {Тn}.",
        объясни="não percebi, explica. explico: havia {n}, {k} foram dados, restam {r}: {л}",
        объясни3="não percebi, explica outra vez. explico outra vez: havia {n}, {k} foram dados, restam {r}: {л}",
        сказал_что="disseste que {X} tem {м} {Тм}. está certo? não, {X} tem {n} {Тn}.",
        а_союз="e {Y}? {Y} tem {m} {Тm}.",
        счёт_да="é verdade que {A} vezes {B} é {C}? sim, {A} vezes {B} é {C}: {a} × {b} = {c}.",
        счёт_нет="é verdade que {A} vezes {B} é {D}? não, {A} vezes {B} é {C}: {a} × {b} = {c}.",
        почему="porque é que {X} tem {r} {Тr}? porque {X} tinha {n} e deu {k}: {л}",
        а_если="e se fossem o dobro? então {X} teria {д} {Тд}: {лд}",
        что_дальше="o que acontece a seguir? {X} tem {r} {Тr}: {л}",
        правда="é verdade? sim, {X} tem {n} {Тn}.",
        неправда="é verdade que {X} tem {м} {Тм}? não, {X} tem {n} {Тn}.",
        переспрос="queres dizer {n} {Тn}? sim, {n} {Тn}.",
        согласен="concordas? sim, concordo: {X} tem {n} {Тn}.",
    ),
    "pl": dict(
        было="{X} miał{а} {n} {Тn}.", отдал="{X} oddał{а} {k} {Тk}.", стало="{X} ma {r} {Тr}.",
        получил="{X} dostał{а} {k} {Тk}.",
        а_союз="a {Y}? {Y} ma {m} {Тm}.",
        счёт_да="czy to prawda, że {A} razy {B} to {C}? tak, {A} razy {B} to {C}: {a} × {b} = {c}.",
        счёт_нет="czy to prawda, że {A} razy {B} to {D}? nie, {A} razy {B} to {C}: {a} × {b} = {c}.",
        почему="dlaczego {X} ma {r} {Тr}? ponieważ {X} miał{а} {n} i oddał{а} {k}: {л}",
        почему_голый="dlaczego? ponieważ {X} miał{а} {n} i oddał{а} {k}: {л}",
        а_у="ile ma {Y}? {Y} ma {m} {Тm}.",
        а_если="a gdyby było dwa razy więcej? wtedy {X} miał{а}by {д} {Тд}: {лд}",
        наоборот2="{X} ma {n} {Тn}, {Y} ma {m} {Тm}. co by było, gdyby było odwrotnie? wtedy {X} miał{а}by {m} {Тm}, a {Y} {n} {Тn}.",
        объясни2="wyjaśnij, proszę: nie rozumiem. wyjaśniam: było {n}, oddano {k}, zostało {r}: {л}",
        наоборот="{X} ma {n} {Тn}, {Y} ma {m} {Тm}. a gdyby było odwrotnie? wtedy {X} miał{а}by {m} {Тm}, a {Y} {n} {Тn}.",
        повтори="powtórz, proszę. powtarzam: {X} ma {n} {Тn}.",
        объясни="nie rozumiem, wyjaśnij. wyjaśniam: było {n}, oddano {k}, zostało {r}: {л}",
        объясни3="nie zrozumiałem, wyjaśnij jeszcze raz. wyjaśniam jeszcze raz: było {n}, oddano {k}, zostało {r}: {л}",
        сказал_что="powiedziałeś, że {X} ma {м} {Тм}. czy to prawda? nie, {X} ma {n} {Тn}.",
        что_дальше="co dalej? {X} ma {r} {Тr}: {л}",
        правда="czy to prawda? tak, {X} ma {n} {Тn}.",
        неправда="czy to prawda, że {X} ma {м} {Тм}? nie, {X} ma {n} {Тn}.",
        переспрос="czy chodzi ci o {n} {Тn}? tak, {n} {Тn}.",
        согласен="czy się zgadzasz? tak, zgadzam się: {X} ma {n} {Тn}.",
    ),
    "nl": dict(
        было="{X} had {n} {Тn}.", отдал="{X} gaf {k} {Тk} weg.", стало="{X} heeft {r} {Тr}.",
        получил="{X} kreeg {k} {Тk}.",
        а_союз="en {Y}? {Y} heeft {m} {Тm}.",
        счёт_да="is het waar dat {A} maal {B} {C} is? ja, {A} maal {B} is {C}: {a} × {b} = {c}.",
        счёт_нет="is het waar dat {A} maal {B} {D} is? nee, {A} maal {B} is {C}: {a} × {b} = {c}.",
        почему="waarom heeft {X} {r} {Тr}? omdat {X} er {n} had en {k} weggaf: {л}",
        почему_голый="waarom? omdat {X} er {n} had en {k} weggaf: {л}",
        а_у="hoeveel heeft {Y}? {Y} heeft {m} {Тm}.",
        а_если="en als het er twee keer zoveel waren? dan zou {X} {д} {Тд} hebben: {лд}",
        наоборот2="{X} heeft {n} {Тn}, {Y} heeft {m} {Тm}. wat zou er gebeuren als het omgekeerd was? dan zou {X} {m} {Тm} hebben en {Y} {n} {Тn}.",
        объясни2="leg het uit, alsjeblieft: ik begrijp het niet. ik leg uit: {X} had er {n}, gaf {k} weg, en houdt er {r} over: {л}",
        наоборот="{X} heeft {n} {Тn}, {Y} heeft {m} {Тm}. en als het omgekeerd was? dan zou {X} {m} {Тm} hebben en {Y} {n} {Тn}.",
        повтори="zeg dat nog eens, alsjeblieft. ik herhaal: {X} heeft {n} {Тn}.",
        объясни="ik begrijp het niet, leg het uit. ik leg uit: {X} had er {n}, gaf {k} weg, en houdt er {r} over: {л}",
        объясни3="ik heb het niet begrepen, leg het nog een keer uit. ik leg het nog een keer uit: {X} had er {n}, gaf {k} weg, en houdt er {r} over: {л}",
        сказал_что="je zei dat {X} {м} {Тм} heeft. klopt dat? nee, {X} heeft {n} {Тn}.",
        что_дальше="wat gebeurt er daarna? {X} heeft {r} {Тr}: {л}",
        правда="klopt dat? ja, {X} heeft {n} {Тn}.",
        неправда="klopt het dat {X} {м} {Тм} heeft? nee, {X} heeft {n} {Тn}.",
        переспрос="bedoel je {n} {Тn}? ja, {n} {Тn}.",
        согласен="ben je het ermee eens? ja, ik ben het ermee eens: {X} heeft {n} {Тn}.",
    ),
}


def слова_счёта(язык, i):
    """Показы о счёте СЛОВАМИ — обе полярности с кузницей.

    «правда ли, что дважды два — четыре?» есть вопрос об истине, а не о вещи,
    и потому судится не пересчётом предметов, а самой таблицей: слово «четыре»
    объявлено пакетом языка, произведение считается.

    ВТОРАЯ ПОЛЯРНОСТЬ — ОТКАЗ ОТ ЛЖИ С ОСНОВАНИЕМ: «правда ли, что дважды два —
    пять? нет, дважды два — четыре: 2 × 2 = 4.» Дом не смел её писать (граница
    04.09): суд арифметики читал предложение как утверждение и находил в вопросе
    «2 × 2 = 5». С 05.09 у суда есть ОКНО ВОПРОСА: равенство, процитированное
    вопросом, судится словом, открывающим ответ, — после «нет» оно обязано быть
    ложным; слово полярности объявляет пакет языка. Цитата лжи стала законной
    ровно тогда, когда суд научился её читать, — не раньше.
    """
    я = ЯЗЫКИ[язык]
    if "счёт_да" not in я:
        return ()
    if язык not in ЧИСЛА_СЛОВОМ:
        ЧИСЛА_СЛОВОМ[язык] = _числительные(язык)
    сл = ЧИСЛА_СЛОВОМ[язык]
    a, b = ТАБЛИЦА[i % len(ТАБЛИЦА)]
    c, d = a * b, a * b + 1
    if not all(n in сл for n in (a, b, c, d)):
        return ()
    поля = dict(A=сл[a], B=сл[b], C=сл[c], D=сл[d], a=a, b=b, c=c)
    поверхности = [я[к] for к in ("счёт_да", "счёт_нет", "счёт_да2", "счёт_нет2") if к in я]
    return tuple(п.format(**поля) for п in поверхности)


def _винительный(язык, Т, k):
    """Форма вещи после глагола отдачи — ОБЪЯВЛЕННАЯ, а не угаданная.

    Дом страниц действия отвечает None там, где падеж не объявлен («отдала
    1 монету» требует винительного, которого у «монеты» в парадигмах нет), и
    его собственный закон гласит: страница НЕ ПИШЕТСЯ. Подставить сюда
    именительный значило бы написать «отдала 1 монета» — верно счётом,
    ложно речью; тот самый род изъяна, ради которого падеж и объявляют.
    """
    в = A._вещь_вин(язык, Т, k)
    if в is None:
        raise ValueError("форма вещи не объявлена")
    return в


def _que(имя):
    """ЭЛИЗИЯ: французское «que» перед гласной или немым h есть «qu'» («tu as dit
    qu'Anna a 8 pièces»); перед согласной — «que » с пробелом. Поле страницы:
    рамка пишет «{que}{X}», а буква решается именем."""
    return "qu'" if имя[:1].lower() in "aeiouyhàâéèêëîïôûùœ" else "que "


def _поля(язык, X, Т, n, k):
    я, лицо = ЯЗЫКИ[язык], A.ЛИЦА[язык][X]
    r, д, м = n - k, n * 2, n + 4
    вещь = lambda с: A._вещь(язык, Т, с)
    return dict(
        X=лицо[0], Xр=лицо[2], а=A._а(язык, лицо[1]), que=_que(лицо[0]),
        n=n, k=k, r=r, д=д, м=м,
        Тn=вещь(n), Тk=вещь(k), Тr=вещь(r), Тд=вещь(д), Тм=вещь(м),
        Твk=_винительный(язык, Т, k),
        л=f"{n} − {k} = {r}.", лд=f"{n} × 2 = {д}.")



# ВЕЖЛИВЫЙ РЕГИСТР — второе лицо на «вы». Замер по своду нашёл в корпусе НОЛЬ
# строк с «вы» при девяноста двух с «ты», ноль «Sie» при двухстах двадцати
# «du», ноль «vous» при ста семнадцати «tu». Дом связок — самый разговорный в
# корпусе (279 строк обращаются к собеседнику), и потому регистр ему нужнее
# всех: организм, зовущий владельца на «ты», по-русски, по-немецки,
# по-французски, по-испански, по-итальянски и по-польски груб, а не краток.
#
# ВЕЖЛИВАЯ РАМКА ЕСТЬ НЕФОРМАЛЬНАЯ С ОБЪЯВЛЕННОЙ ЗАМЕНОЙ, а не вторая рукопись:
# так видно, ЧТО ИМЕННО меняет регистр, и так невозможно завести две рамки,
# разошедшиеся в чём-то, кроме обращения.
#
# АНГЛИЙСКИЙ РАЗЛИЧИЯ НЕ ИМЕЕТ («you» служит обоим) и пишет одну форму —
# объявлено списком. ПОЛЬСКИЙ ИДЁТ ТРЕТЬИМ ЛИЦОМ («czy pan się zgadza»), а не
# вторым, и потому его замены переписывают всю фразу.
БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА = frozenset({"en"})
ЗАМЕНЫ_ОБРАЩЕНИЯ = {
"ru": (("согласен ли ты?", "согласны ли вы?"), ("объясни ещё раз.", "объясните ещё раз."), ("ты сказал, что", "вы сказали, что"), ("ты имеешь в виду", "вы имеете в виду"),
       ("повтори, пожалуйста.", "повторите, пожалуйста."),
       ("объясни.", "объясните."), ("объясни, пожалуйста:", "объясните, пожалуйста:")),
"de": (("stimmst du zu?", "stimmen Sie zu?"), ("erkläre es noch einmal.", "erklären Sie es noch einmal."), ("du hast gesagt, dass", "Sie haben gesagt, dass"), ("meinst du", "meinen Sie"),
       ("sag das bitte noch einmal.", "sagen Sie das bitte noch einmal."),
       ("erkläre es.", "erklären Sie es."), ("erkläre es bitte:", "erklären Sie es bitte:")),
"fr": (("es-tu d'accord ?", "êtes-vous d'accord ?"), ("explique encore une fois.", "expliquez encore une fois."), ("tu as dit {que}", "vous avez dit {que}"), ("tu veux dire", "vous voulez dire"),
       ("répète, s'il te plaît.", "répétez, s'il vous plaît."),
       ("explique.", "expliquez."), ("explique, s'il te plaît :", "expliquez, s'il vous plaît :")),
"es": (("¿estás de acuerdo?", "¿está usted de acuerdo?"), ("explícalo otra vez.", "explíquelo otra vez."), ("dijiste que", "usted dijo que"), ("¿quieres decir", "¿quiere usted decir"),
       ("repite, por favor.", "repita, por favor."),
       ("explícalo.", "explíquelo."), ("explícalo, por favor:", "explíquelo, por favor:")),
"it": (("sei d'accordo?", "è d'accordo?"), ("spiegalo ancora una volta.", "lo spieghi ancora una volta."), ("hai detto che", "Lei ha detto che"), ("intendi", "intende"),
       ("ripeti, per favore.", "ripeta, per favore."),
       ("spiega.", "spieghi."), ("spiega, per favore:", "spieghi, per favore:")),
"pt": (("concordas?", "concorda?"), ("explica outra vez.", "explique outra vez."), ("disseste que", "o senhor disse que"), ("queres dizer", "quer dizer"),
       ("repete, por favor.", "repita, por favor."),
       ("explica.", "explique."), ("explica, por favor:", "explique, por favor:")),
"nl": (("ben je het ermee eens?", "bent u het ermee eens?"), ("leg het nog een keer uit.", "legt u het nog een keer uit."), ("je zei dat", "u zei dat"), ("bedoel je", "bedoelt u"),
       ("zeg dat nog eens, alsjeblieft.", "zegt u dat nog eens, alstublieft."),
       ("leg het uit.", "legt u het uit."), ("leg het uit, alsjeblieft:", "legt u het uit, alstublieft:")),
"pl": (("czy się zgadzasz?", "czy pan się zgadza?"), ("wyjaśnij jeszcze raz.", "proszę wyjaśnić jeszcze raz."), ("powiedziałeś, że", "powiedział pan, że"), ("czy chodzi ci o", "czy chodzi panu o"),
       ("powtórz, proszę.", "proszę powtórzyć."),
       ("wyjaśnij.", "proszę wyjaśnić."), ("wyjaśnij, proszę:", "proszę wyjaśnić:")),
}
ФОРМЫ_ВЫ = ("согласен", "переспрос", "повтори", "объясни", "объясни2", "объясни3", "сказал_что")

# ОБЪЯВЛЕННЫЙ ПРОПУСК: дыра, о которой дом ЗНАЕТ и которую держит нарочно.
# Прибор щербатости (scripts/form_matrix.py) читает это объявление и не зовёт
# такую дыру щербатостью: язык без различия регистров пишет одну форму, и
# требовать от него второй значило бы судить английский русской меркой.
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {ф + "_вы": БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА for ф in ФОРМЫ_ВЫ}


def _языки_вы():
    вон = {}
    for язык, пары in ЗАМЕНЫ_ОБРАЩЕНИЯ.items():
        своё = dict(ЯЗЫКИ[язык])
        for форма in ФОРМЫ_ВЫ:
            if форма not in своё:
                continue
            рамка = своё[форма]
            for стар, нов in пары:
                рамка = рамка.replace(стар, нов)
            assert рамка != своё[форма], (язык, форма)
            своё[форма] = рамка
        вон[язык] = своё
    return вон


ЯЗЫКИ_ВЫ = _языки_вы()

for _яз in ЯЗЫКИ:
    assert (_яз in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА) != (_яз in ЯЗЫКИ_ВЫ), _яз


def страница(язык, форма, X=0, Т=0, n=7, k=2, Y=None, вежливо=False):
    я = (ЯЗЫКИ_ВЫ if вежливо else ЯЗЫКИ)[язык]
    п = _поля(язык, X, Т, n, k)
    if форма in ("повтори", "объясни", "объясни2"):
        # ПОЧИНКА РАЗГОВОРА: «повтори, пожалуйста» и «я не понял, объясни» —
        # не вопросы, а просьбы, и ответ на них ПРОВЕРЯЕМ: повтор обязан
        # совпасть с фактом, объяснение — показать кузницу. Без этой пары
        # продукт, которого не поняли, не имеет второго хода.
        if форма == "повтори":
            зачин = я["стало"].format(**dict(п, r=n, Тr=п["Тn"]))
            return f"{зачин} {я['повтори'].format(**п)}"
        зачин = f"{я['было'].format(**п)} {я['отдал'].format(**п)} {я['стало'].format(**п)}"
        ключ = форма if форма in я else "объясни"
        return f"{зачин} {я[ключ].format(**п)}"
    if форма == "а_союз":
        # ТОТ ЖЕ ЭЛЛИПСИС, НО СОЮЗОМ: «а у тома?», «and tom?» — так и спрашивает
        # человек. Зачин здесь союз, а не вопросное слово, и это законная
        # поверхность вопроса ДА/НЕТ и эллипсиса во всех семи языках.
        Y = (X + 1 + (Т % 3)) % len(A.ЛИЦА[язык])
        второй = A.ЛИЦА[язык][Y]
        п2 = dict(п, Y=второй[0], Yр=второй[2], m=k + 2, Тm=A._вещь(язык, Т, k + 2))
        зачин = я["стало"].format(**dict(п, r=n, Тr=п["Тn"]))
        return f"{зачин} {я['а_союз'].format(**п2)}"
    if форма in ("наоборот", "наоборот2"):
        # КОНТРФАКТИЧЕСКОЕ ОБ ОБМЕНЕ: «а если наоборот?» ссылается на ДВА
        # числа предыдущей фразы разом, и ответ проверяется тем же пересчётом,
        # что и всякий показ дома, — величины меняются местами, а не меняются.
        Y = (X + 1 + (Т % 3)) % len(A.ЛИЦА[язык])
        второй = A.ЛИЦА[язык][Y]
        п2 = dict(п, Y=второй[0], Yр=второй[2], m=k + 2, Тm=A._вещь(язык, Т, k + 2),
                  n=n, Тn=A._вещь(язык, Т, n))
        ключ = форма if форма in я else "наоборот"
        return я[ключ].format(**п2)
    if форма == "а_у":
        # ЭЛЛИПСИС ССЫЛАЕТСЯ НА СКАЗАННОЕ: вещь во втором вопросе ОПУЩЕНА
        # («сколько у бори?»), и восстановить её можно лишь из первой фразы.
        # Это и есть связка разговора в чистом виде — вопрос, который без
        # предыдущей реплики не имеет смысла.
        Y = (X + 1 + (Т % 3)) % len(A.ЛИЦА[язык])
        если_свой = A.ЛИЦА[язык][Y]
        п2 = dict(п, Y=если_свой[0], Yр=если_свой[2], m=k + 2,
                  Тm=A._вещь(язык, Т, k + 2))
        зачин = я["стало"].format(**dict(п, r=n, Тr=п["Тn"]))
        return f"{зачин} {я['а_у'].format(**п2)}"
    if форма in ("почему", "почему_голый"):
        зачин = f"{я['было'].format(**п)} {я['отдал'].format(**п)} {я['стало'].format(**п)}"
    elif форма == "что_дальше":
        # тут «стало» есть ПРИБАВКА: факт до, приход, и вопрос о следующем
        п = dict(п, r=n + k, Тr=A._вещь(язык, Т, n + k), л=f"{n} + {k} = {n + k}.")
        зачин = f"{я['было'].format(**п)} {я['получил'].format(**п)}"
    else:
        зачин = я["стало"].format(**dict(п, r=n, Тr=п["Тn"]))
    return f"{зачин} {я[форма].format(**п)}"


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        лиц, вещей = len(A.ЛИЦА[язык]), len(A.ЯЗЫКИ[язык]["вещи"])
        for i in range(len(ТАБЛИЦА)):
            for с in слова_счёта(язык, i):
                вон[с] = (язык, "счёт_словами")
        for форма in ФОРМЫ:
            if форма == "счёт_да":
                continue          # они пишутся своим ходом выше
            if форма in ("наоборот2", "объясни2", "а_союз") and форма not in ЯЗЫКИ[язык]:
                continue          # язык не объявил второй поверхности
            for i in range(лиц):
                for t in range(вещей):
                    n = 5 + (i * 3 + t * 2) % 20
                    k = 1 + (i + t) % 4
                    for вежливо in (False, True):
                        if вежливо and (форма not in ФОРМЫ_ВЫ
                                        or язык in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА):
                            continue
                        имя = форма + ("_вы" if вежливо else "")
                        try:
                            вон[страница(язык, форма, i, t, n, k,
                                         вежливо=вежливо)] = (язык, имя)
                        except ValueError:
                            continue   # падеж не объявлен — страница не пишется
    return вон


ПОКАЗЫ = _все_показы()


def судить(строка):
    """(судимо, истинно) — показ дома истинен; строка той же рамки с иным
    числом есть ложь, ибо кузница в ней не сходится."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    return False, False


def _самопроверка():
    мутанты = 0
    # ЧИСЛА САМОПРОВЕРКИ БЕРУТСЯ ТЕМ ЖЕ ПРАВИЛОМ, ЧТО И ПОКАЗЫ: показ,
    # написанный числом «на глазок», не есть показ дома, и проверка о нём
    # ничего бы не сказала.
    # (i=0, t=1) — первая клетка правила, где счёт отдачи равен двум, то есть
    # берётся счётная форма, объявленная всякой вещи
    i0, t0 = 0, 1
    n0, k0 = 5 + (i0 * 3 + t0 * 2) % 20, 1 + (i0 + t0) % 4
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            if форма == "счёт_да":
                for с in слова_счёта(язык, 0):
                    assert судить(с) == (True, True), (язык, с)
                continue
            if форма in ("наоборот2", "объясни2", "а_союз") and форма not in ЯЗЫКИ[язык]:
                continue
            с = страница(язык, форма, i0, t0, n0, k0)
            судимо, истинно = судить(с)
            assert судимо and истинно, (язык, форма, с)
        # МУТАНТ: подменённый итог кузницы не есть показ дома
        битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.",
                       страница(язык, "почему", i0, t0, n0, k0))
        assert судить(битая) == (False, False), (язык, битая)
        мутанты += 1
    for язык in ("ru", "en", "de"):
        for форма in ("почему", "а_если", "неправда", "а_союз"):
            print("  ", страница(язык, форма, i0, t0, n0, k0)[:118])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
