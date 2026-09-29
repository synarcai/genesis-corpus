#!/usr/bin/env python3
"""ДОМ АКТОВ В РЕПОЗИТОРИИ — руки агента, вторая ступень: приказ, ход мира, итог (25.09, мера ведущего, М-2013).

Дом `toolacts` научил ход тела над плоской папкой. Мера ведущего (ядро М-2008, ключ агента на песочном репозитории:
2 из 50) назвала, чем школа нема: приказ сказан не формой дома («an empty file», без «the file», «into» вместо «to»),
имя файла — литерал рамки, пути с папкой нет, вопросов о репозитории нет. Этот дом — те же руки в РЕПОЗИТОРИИ С
ПАПКАМИ (`repoworld`): создать (путём, голым путём, «пустой», «новый», в названной папке), удалить, перенести в папку,
переименовать, заменить текст в кавычках из нескольких слов и слово, дописать строку, прогнать тесты по языку
проекта, план из двух актов «сделай A, затем B» — и вопросы-поиски: в каком файле или файлах текст, на какой строке,
первая, вторая, последняя строка, строка с номером, что файл настроек говорит о ключе и его значение, сколько
строк, сколько раз слово в папке и во всём репозитории, сколько файлов в папке.

ТРИ ГОЛОСА НА СТРАНИЦЕ (коллегия ведущего «ответ мира в словах дома»): место итога, какое заполняет мир — найденный
файл, номер строки, текст строки, значение ключа, число строк, байт или тестов, — рынок покупает только ЭХОМ: текст
итога равен клетке хода мира на той же странице. Потому между словом пользователя и итогом организма стоит ход мира
(метка «мир» — у двери хода `actturn`): у акта — после «да/нет», у вопроса — сразу после вопроса; на отказе
пользователем — чтение «до», на невозможном — отказ мира по имени. Ход мира печатает мир папки (`folderworld` —
семантика ядра `world.rs` строка в строку) на репозитории страницы, прогон — настоящий вывод бегуна, снятый прибором
`toolrepo_capture.py`; содержимое хода одно на всех языках, различается только метка. ЧИСЛО ИТОГА — ЛИШЬ СТОЯЩЕЕ В
ХОДЕ МИРА: из отчёта «Ran 8 tests … OK» итог говорит «all 8 tests passed», из «4 passed; 1 failed» — «4 tests
passed, 1 failed», а не «6 из 7», какого мир не писал.

ПЛАН С МЕСТОИМЕНИЕМ (вопрос 4 коллегии, роды ведущего): второй приказ называет объект первого местоимением («create
the file X, then append the line "…" to it», «…, puis supprime-le»). Предложение называет путь, какой определяет сам
приказ (создание — созданный файл, переименование — новое имя в той же папке, перенос — папка/имя); мир ходит после
каждого акта, второй акт идёт туда, куда строка path первого хода положила объект, и итог называет этот путь.
Первый акт невозможен — мир отказывает по имени, второй не идёт; находка слова в одном файле — второй акт идёт туда,
в нескольких — ответ всеми путями, а второй акт ждёт одного места: организм не угадывает.

РОДЫ ЖИВЫХ ПРОСЬБ (26.09, третий заказ ведущего — по переписи живых просьб к агенту, не по ключам): план из трёх
актов (второй и третий идут на место из строки path хода мира; третий — «сколько строк» или прогон); условный приказ
на ходе мира — мир проверяет условие (read файла, find текста), ветка — его ход: итог проверки называет исход, акт
ветки — вторым ходом, ветка без акта — «условие не выполнено, акт не совершён»; «все файлы папки, кроме n» — мир
читает папку (list), акт идёт на всякий файл, кроме названного, с правкой «…, но не трогай n»; два объекта в одном
приказе — правка плана из двух актов; ссылка «этот файл», «тот же файл» — правка плана с местоимением.
ПАРЫ У МНОГОАКТНЫХ СТРАНИЦ (перепись 26.09: у планов пар «минус слова» не было): каноническая форма многоактного рода —
ещё и вежливой просьбой (`вежливо`); вопрос «сколько тестов проходит» (ответ берёт прогон), план «прогони тесты, затем
скажи, сколько прошло», находка файла со словом, затем «сколько в нём строк».
КОНТРАСТНЫЕ ПАРЫ И СОСТОЯНИЯ ПРОЕКТА (27.09, наряд ведущего): зачин просьбы сказать перед вторым вопросом плана
(ПЛАН_СКАЖИ: «…, then tell me what its first line is» — два вида зачина, `toolacts.ЗАЧИН`; «…, then let me know
which file contains the word "x"» дверь знает, но свод не показывает — ядро берёт зачин перед вопросом, какой его рамка
укладывает целым, соперницей связки плана); связки акта и вопроса «and» и «;» у плана прогона; модификаторы приказа — хранители
акта («now», «just», «right now»: тот же ход мира) и слова, какие акт меняют («later», «tomorrow», «don't …»,
«pretend to …» — `toolacts.МЕНЯЮЩИЕ`, `ОТМЕНА`: организм акта не предлагает, мир читает «до», итог — отказ с
причиной); вопрос о прошлом акте («did you delete F?»: мир читает файл, удаления нет); правка кода одним актом мира, затем прогон — отчёт бегуна снят с проекта в этом состоянии
(`repoworld.ПРАВКИ_ПРОЕКТА`), числа итога — из отчёта бегуна (у полного прогона крейта `gauge` строк итога
несколько, дом их складывает леджером: «all 6 tests passed: 2 + 3 + 1 = 6»).
ИСХОДЫ ПРОГОНА (28.09, наряд ведущего): приказ прогона одним актом на проекте в том состоянии, какое держит мир, — всякий
исход, какого прогон на объявленном проекте не показывал: провал и ошибка unittest («7 of 8 tests passed: 8 − 1 = 7»,
«3 of 8 tests passed: 8 − 4 − 1 = 3»), прогон без тестов («no tests ran», код 5), провал полного прогона крейта.
ДВА РАЗНЫХ АКТА (28.09, заказ руки joins2 через ведущего, к М-2090): план из двух разных актов над разными файлами,
какие дом кладёт и одиночными страницами (перенос и дописывание, создание и удаление, дописывание и замена,
переименование и дописывание, удаление и создание), — связкой плана и союзом «and»; союзом же — «…, then let me know
how many lines it has» после переименования и переноса и «…, then tell me what its first line is» после дописывания.

УСЛОВИЯ РЫНКА (ведущий, М-2013), и как дом их держит (самопроверка `условия_рынка` — бед 0):
  1. дыра учится парой: итог называет каждое слово каждой дыры приказа канонической фразой; у всякой формы и языка —
     пара исполненных страниц, где разнятся все дыры;
  2. текст в кавычках — одна дыра; кавычки приказа и итога одни (`toolacts.КАВЫЧКИ`); в ходе мира — ASCII-кавычки;
  3. путь с папкой — одно слово органа; имена, перед какими французское «de» сократилось бы, не заводятся;
  4. английский глагол приказа не равен отчёту, у акта один глагол на язык;
  5. исполненных страниц всякой формы больше, чем отказов;
  6. у условного приказа итог называет дыры проверки и исполненной ветки: дыру другой ветки мир не брал.
РАЗВЕДЕНИЕ ИСТОЧНИКОВ (коллегия): на всякое место, какое заполняет мир, у всякой формы и языка — не меньше четырёх
страниц, где верная клетка отличается от каждой соперницы (номер строки ≠ 1 и ≠ мерам; files ≠ lines ≠ bytes;
вхождения ≠ совпавшим строкам — слово дважды в одной строке); слово выбора (first, second, last) — не меньше четырёх
страниц на файлах в три строки и больше. Строки хода мира — без двойных кавычек и без «слово:» после конца фразы.

ОДНА ДВЕРЬ НА ПОНЯТИЕ: роли, «да/нет», отказ, «уже есть», «нет», метка мира, глаголы создать и удалить, счётные слова
файлов и запусков — у `actturn`; шаблоны замены, дописывания, переименования, переноса и прогона, фразы объектов в
падеже шаблона, кавычки, связка плана, «раз», «строк», исход прогона — у `toolacts`; мир и его ход — `repoworld` и
`folderworld`. Здесь — речь вопросов, формы «создать пустой / новый», инфинитив акта двери хода и страницы.

ЧЕГО ДОМ НЕ МЕРИТ, НАЗВАНО: ответ «сколько строк» берёт меру `lines`, и она у хода `lines` всегда равна номеру
последней строки — разводит их лишь покупка по имени меры; невозможный акт о двух объектах называет лишь недостающий;
папка с подпапками («tally») в вопросах о числе файлов не спрашивается.
"""
import collections
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actturn as A  # noqa: E402 — дверь хода: роли, да/нет, отказ, «уже есть», «нет», метка мира, глаголы
import folderworld as W  # noqa: E402 — мир папки: ход мира строкой
import svampforms as S  # noqa: E402 — счётная ячейка пакета (согласие глагола исхода с числом)
import toolacts as T  # noqa: E402 — дверь рук: шаблоны актов, фразы объектов, кавычки, связка плана, исход
from repoworld import *  # noqa: E402,F401,F403 — объявление мира: пути, содержимое, прогоны, слова вопросов
import repoworld as Р  # noqa: E402

ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# РЕЧЬ: инфинитив акта двери хода, «создать пустой / новый», тесты по языку, вопросы и ответы
# ======================================================================================================
# слоты: {Ф} файл, {Фр} «файла», {М} «в файле», {Дв} «в папке» — формы у двери `toolacts.ОБЪЕКТЫ`; {K}/{Kо} ключ;
# {W}/{Wи}/{Wнет} текст; {С} — список файлов; {c} — слово выбора; {N}, {P}, {F} — числа отчёта прогона
РЕЧЬ = {
    "en": dict(место="{позиция} {Фр}", инф_акта="{V} {Ф}", пустой="an empty file {f}", новый="a new file {f}",
               тесты_языка="the {Я} tests", и="and",
               q_файл="which file contains {W}?", q_файлы="which files contain {W}?", нигде="no file contains {W}",
               в_файлах="{Wи} stands in the files {С}",
               q_строка="on which line {Фр} is {Wи}?",
               выбор=("first", "second", "last"), q_выбор="what is the {c} line {Фр}?", a_выбор="the {c} line {Фр} is {T}",
               q_строка_н="what does line {a} {Фр} say?", a_строка="line {a} {Фр} says {T}",
               q_о_ключе="what does {Ф} say about {k}?", a_о_ключе="{Ф} says {T} about the key {k}",
               ключ=("the key {k}", "{k}"), ключ_о=("of the key {k}", "of {k}"),
               q_ключ="what is the value {Kо} {М}?", ключ_ответ="{K} {М} has the value {v}",
               q_строк="how many lines are {М}?", q_папка="how many files are {Дв}?",
               все_прошли="all {N} passed", прошли_упали="{P} passed, {F} failed", из_прошли="{P} of {N} passed",
               q_файл2="where is {Wи}?",
               q_строка2="which line {Фр} contains {W}?",
               q_строка_н2="what is on line {a} {Фр}?",
               q_строк2="how many lines does {Ф} have?",
               q_ключ2="what value does {K} have {М}?",
               q_папка2="how many files does {Дп} contain?",
               q_файл3="which file mentions {W}?",
               q_строка3="on which line {Фр} does {W} appear?",
               q_выбор2="what does the {c} line {Фр} say?",
               q_конец="what is written at the end {Фр}?",
               q_читай="read line {a} {Фр}.",
               q_покажи="show line {a} {Фр}.",
               q_ключ_бк="what is the value of {k} {М}?"),
    "ru": dict(место="{М} {позиция}", инф_акта="{V} {Ф}", пустой="пустой файл {f}", новый="новый файл {f}",
               тесты_языка="тесты {Я}", и="и",
               q_файл="в каком файле есть {Wи}?", q_файлы="в каких файлах есть {Wи}?",
               нигде="{Wнет} нет ни в одном файле", в_файлах="{Wи} стоит в файлах {С}",
               q_строка="в какой строке {Фр} стоит {Wи}?",
               выбор=("первая", "вторая", "последняя"), q_выбор="какая {c} строка {Фр}?",
               a_выбор="{c} строка {Фр} гласит {T}",
               q_строка_н="что написано {М} в строке {a}?", a_строка="{М} в строке {a} написано {T}",
               q_о_ключе="что {Ф} говорит о {k}?", a_о_ключе="о ключе {k} {Ф} говорит {T}",
               ключ=("ключ {k}", "{k}"), ключ_о=("у ключа {k}", "у {k}"),
               q_ключ="какое значение {Kо} {М}?", ключ_ответ="{Kо} {М} значение {v}",
               q_строк="сколько строк {М}?", q_папка="сколько файлов {Дв}?",
               все_прошли="все {N} прошли", прошли_упали="{P} {прошли}, {F} {упали}", из_прошли="{прошли} {P} из {N}",
               прошли=("прошёл", "прошли", "прошли"), упали=("упал", "упали", "упали"),
               q_файл2="где стоит {Wи}?",
               q_строка2="какая строка {Фр} содержит {W}?",
               q_строка_н2="что стоит {М} в строке {a}?",
               q_строк2="сколько строк содержит {Ф}?",
               q_ключ2="каково значение {Kо} {М}?",
               q_папка2="сколько файлов содержит {Дп}?",
               q_файл3="где встречается {Wи}?",
               q_строка3="на какой строке {Фр} стоит {Wи}?",
               q_выбор2="какая {c} строка {М}?",
               q_конец="что написано в конце {Фр}?",
               q_читай="прочитай строку {a} {Фр}.",
               q_покажи="покажи строку {a} {Фр}.",
               q_ключ_бк="какое значение {k} {М}?"),
    "de": dict(место="{позиция} {Фр}", инф_акта="{Ф} {V}", пустой="eine leere Datei {f}", новый="eine neue Datei {f}",
               тесты_языка="die Tests für {Я}", и="und",
               q_файл="welche Datei enthält {W}?", q_файлы="welche Dateien enthalten {W}?",
               нигде="keine Datei enthält {W}", в_файлах="{Wи} steht in den Dateien {С}",
               q_строка="in welcher Zeile {Фр} steht {Wи}?",
               выбор=("ersten", "zweiten", "letzten"), q_выбор="was steht in der {c} Zeile {Фр}?",
               a_выбор="in der {c} Zeile {Фр} steht {T}",
               q_строка_н="was steht in Zeile {a} {Фр}?", a_строка="in Zeile {a} {Фр} steht {T}",
               q_о_ключе="was sagt {Ф} über {k}?", a_о_ключе="{Ф} sagt über den Schlüssel {k} {T}",
               ключ=("der Schlüssel {k}", "{k}"), ключ_о=("der Schlüssel {k}", "{k}"),
               q_ключ="welchen Wert hat {Kо} {М}?", ключ_ответ="{K} {М} hat den Wert {v}",
               q_строк="wie viele Zeilen hat {Ф}?", q_папка="wie viele Dateien sind {Дв}?",
               все_прошли="alle {N} bestanden", прошли_упали="{P} bestanden, {F} fehlgeschlagen",
               из_прошли="{P} von {N} bestanden",
               q_файл2="wo steht {Wи}?",
               q_строка2="welche Zeile {Фр} enthält {W}?",
               q_строка_н2="was enthält Zeile {a} {Фр}?",
               q_строк2="wie viele Zeilen enthält {Ф}?",
               q_ключ2="welchen Wert besitzt {Kо} {М}?",
               q_папка2="wie viele Dateien enthält {Дп}?",
               q_файл3="welche Datei erwähnt {W}?",
               q_строка3="in welcher Zeile {Фр} taucht {Wи} auf?",
               q_выбор2="was ist in der {c} Zeile {Фр} zu lesen?",
               q_конец="was steht am Ende {Фр}?",
               q_читай="lies Zeile {a} {Фр}.",
               q_покажи="zeig Zeile {a} {Фр}.",
               q_ключ_бк="welchen Wert hat {k} {М}?"),
    "fr": dict(место="{позиция} {Фр}", инф_акта="{V} {Ф}", пустой="un fichier vide {f}", новый="un nouveau fichier {f}",
               тесты_языка="les tests {Я}", и="et",
               q_файл="quel fichier contient {W} ?", q_файлы="quels fichiers contiennent {W} ?",
               нигде="aucun fichier ne contient {W}", в_файлах="{Wи} se trouve dans les fichiers {С}",
               q_строка="à quelle ligne {Фр} se trouve {Wи} ?",
               выбор=("première", "deuxième", "dernière"), q_выбор="quelle est la {c} ligne {Фр} ?",
               a_выбор="la {c} ligne {Фр} est {T}",
               q_строка_н="que dit la ligne {a} {Фр} ?", a_строка="la ligne {a} {Фр} dit {T}",
               q_о_ключе="que dit {Ф} sur {k} ?", a_о_ключе="{Ф} dit {T} sur la clé {k}",
               ключ=("la clé {k}", "{k}"), ключ_о=("de la clé {k}", "de {k}"),
               q_ключ="quelle est la valeur {Kо} {М} ?", ключ_ответ="{K} {М} a la valeur {v}",
               q_строк="combien de lignes contient {Ф} ?", q_папка="combien de fichiers y a-t-il {Дв} ?",
               все_прошли="les {N} ont réussi", прошли_упали="{P} {прошли}, {F} en échec",
               из_прошли="{P} sur {N} {прошли}",
               прошли=T.ПРОШЛО["fr"],
               q_файл2="où se trouve {Wи} ?",
               q_строка2="quelle ligne {Фр} contient {W} ?",
               q_строка_н2="que contient la ligne {a} {Фр} ?",
               q_строк2="combien de lignes a {Ф} ?",
               q_ключ2="que vaut {K} {М} ?",
               q_папка2="combien de fichiers contient {Дп} ?",
               q_файл3="quel fichier mentionne {W} ?",
               q_строка3="à quelle ligne {Фр} apparaît {Wи} ?",
               q_выбор2="que dit la {c} ligne {Фр} ?",
               q_конец="qu'est-ce qui est écrit à la fin {Фр} ?",
               q_читай="lis la ligne {a} {Фр}.",
               q_покажи="montre la ligne {a} {Фр}.",
               q_ключ_бк="quelle est la valeur de {k} {М} ?"),
    "es": dict(место="{позиция} {Фр}", инф_акта="{V} {Ф}", пустой="un archivo vacío {f}", новый="un archivo nuevo {f}",
               тесты_языка="las pruebas de {Я}", и="y",
               q_файл="¿qué archivo contiene {W}?", q_файлы="¿qué archivos contienen {W}?",
               нигде="ningún archivo contiene {W}", в_файлах="{Wи} está en los archivos {С}",
               q_строка="¿en qué línea {Фр} está {Wи}?",
               выбор=("primera", "segunda", "última"), q_выбор="¿cuál es la {c} línea {Фр}?",
               a_выбор="la {c} línea {Фр} es {T}",
               q_строка_н="¿qué dice la línea {a} {Фр}?", a_строка="la línea {a} {Фр} dice {T}",
               q_о_ключе="¿qué dice {Ф} sobre {k}?", a_о_ключе="{Ф} dice {T} sobre la clave {k}",
               ключ=("la clave {k}", "{k}"), ключ_о=("de la clave {k}", "de {k}"),
               q_ключ="¿cuál es el valor {Kо} {М}?", ключ_ответ="{K} {М} tiene el valor {v}",
               q_строк="¿cuántas líneas tiene {Ф}?", q_папка="¿cuántos archivos hay {Дв}?",
               все_прошли="pasaron las {N}", прошли_упали="{P} {прошли}, {F} {упали}", из_прошли="{P} de {N} {прошли}",
               прошли=T.ПРОШЛО["es"], упали=("fallida", "fallidas"),
               q_файл2="¿dónde está {Wи}?",
               q_строка2="¿qué línea {Фр} contiene {W}?",
               q_строка_н2="¿qué contiene la línea {a} {Фр}?",
               q_строк2="¿cuántas líneas contiene {Ф}?",
               q_ключ2="¿qué valor tiene {K} {М}?",
               q_папка2="¿cuántos archivos contiene {Дп}?",
               q_файл3="¿qué archivo menciona {W}?",
               q_строка3="¿en qué línea {Фр} aparece {Wи}?",
               q_выбор2="¿qué dice la {c} línea {Фр}?",
               q_конец="¿qué pone al final {Фр}?",
               q_читай="lee la línea {a} {Фр}.",
               q_покажи="muestra la línea {a} {Фр}.",
               q_ключ_бк="¿cuál es el valor de {k} {М}?"),
    "it": dict(место="{позиция} {Фр}", инф_акта="{V} {Ф}", пустой="un file vuoto {f}", новый="un nuovo file {f}",
               тесты_языка="i test {Я}", и="e",
               q_файл="quale file contiene {W}?", q_файлы="quali file contengono {W}?",
               нигде="nessun file contiene {W}", в_файлах="{Wи} si trova nei file {С}",
               q_строка="in quale riga {Фр} si trova {Wи}?",
               выбор=("la prima", "la seconda", "l'ultima"), q_выбор="qual è {c} riga {Фр}?",
               a_выбор="{c} riga {Фр} è {T}",
               q_строка_н="cosa dice la riga {a} {Фр}?", a_строка="la riga {a} {Фр} dice {T}",
               q_о_ключе="cosa dice {Ф} su {k}?", a_о_ключе="{Ф} dice {T} sulla chiave {k}",
               ключ=("la chiave {k}", "{k}"), ключ_о=("della chiave {k}", "di {k}"),
               q_ключ="qual è il valore {Kо} {М}?", ключ_ответ="{K} {М} ha il valore {v}",
               q_строк="quante righe ha {Ф}?", q_папка="quanti file ci sono {Дв}?",
               все_прошли="superati tutti gli {N}", прошли_упали="{P} {прошли}, {F} {упали}",
               из_прошли="{P} su {N} {прошли}",
               прошли=T.ПРОШЛО["it"], упали=("fallito", "falliti"),
               q_файл2="dove si trova {Wи}?",
               q_строка2="quale riga {Фр} contiene {W}?",
               q_строка_н2="cosa contiene la riga {a} {Фр}?",
               q_строк2="quante righe contiene {Ф}?",
               q_ключ2="che valore ha {K} {М}?",
               q_папка2="quanti file contiene {Дп}?",
               q_файл3="quale file menziona {W}?",
               q_строка3="in quale riga {Фр} compare {Wи}?",
               q_выбор2="cosa dice {c} riga {Фр}?",
               q_конец="cosa c'è scritto alla fine {Фр}?",
               q_читай="leggi la riga {a} {Фр}.",
               q_покажи="mostra la riga {a} {Фр}.",
               q_ключ_бк="qual è il valore di {k} {М}?"),
    "pt": dict(место="{позиция} {Фр}", инф_акта="{V} {Ф}", пустой="um ficheiro vazio {f}", новый="um novo ficheiro {f}",
               тесты_языка="os testes de {Я}", и="e",
               q_файл="que ficheiro contém {W}?", q_файлы="que ficheiros contêm {W}?",
               нигде="nenhum ficheiro contém {W}", в_файлах="{Wи} está nos ficheiros {С}",
               q_строка="em que linha {Фр} está {Wи}?",
               выбор=("primeira", "segunda", "última"), q_выбор="qual é a {c} linha {Фр}?",
               a_выбор="a {c} linha {Фр} é {T}",
               q_строка_н="o que diz a linha {a} {Фр}?", a_строка="a linha {a} {Фр} diz {T}",
               q_о_ключе="o que diz {Ф} sobre {k}?", a_о_ключе="{Ф} diz {T} sobre a chave {k}",
               ключ=("a chave {k}", "{k}"), ключ_о=("da chave {k}", "de {k}"),
               q_ключ="qual é o valor {Kо} {М}?", ключ_ответ="{K} {М} tem o valor {v}",
               q_строк="quantas linhas tem {Ф}?", q_папка="quantos ficheiros há {Дв}?",
               все_прошли="passaram todos os {N}", прошли_упали="{P} {прошли}, {F} {упали}",
               из_прошли="{P} de {N} {прошли}",
               прошли=T.ПРОШЛО["pt"], упали=("falhou", "falharam"),
               q_файл2="onde está {Wи}?",
               q_строка2="que linha {Фр} contém {W}?",
               q_строка_н2="o que contém a linha {a} {Фр}?",
               q_строк2="quantas linhas contém {Ф}?",
               q_ключ2="que valor tem {K} {М}?",
               q_папка2="quantos ficheiros contém {Дп}?",
               q_файл3="que ficheiro menciona {W}?",
               q_строка3="em que linha {Фр} aparece {Wи}?",
               q_выбор2="o que diz a {c} linha {Фр}?",
               q_конец="o que está escrito no fim {Фр}?",
               q_читай="lê a linha {a} {Фр}.",
               q_покажи="mostra a linha {a} {Фр}.",
               q_ключ_бк="qual é o valor de {k} {М}?"),
    "nl": dict(место="{позиция} {Фр}", инф_акта="{Ф} {V}", пустой="een leeg bestand {f}", новый="een nieuw bestand {f}",
               тесты_языка="de tests voor {Я}", и="en",
               q_файл="welk bestand bevat {W}?", q_файлы="welke bestanden bevatten {W}?",
               нигде="geen bestand bevat {W}", в_файлах="{Wи} staat in de bestanden {С}",
               q_строка="in welke regel {Фр} staat {Wи}?",
               выбор=("eerste", "tweede", "laatste"), q_выбор="wat is de {c} regel {Фр}?",
               a_выбор="de {c} regel {Фр} is {T}",
               q_строка_н="wat staat er in regel {a} {Фр}?", a_строка="in regel {a} {Фр} staat {T}",
               q_о_ключе="wat zegt {Ф} over {k}?", a_о_ключе="{Ф} zegt {T} over de sleutel {k}",
               ключ=("de sleutel {k}", "{k}"), ключ_о=("van de sleutel {k}", "van {k}"),
               q_ключ="wat is de waarde {Kо} {М}?", ключ_ответ="{K} {М} heeft de waarde {v}",
               q_строк="hoeveel regels heeft {Ф}?", q_папка="hoeveel bestanden zitten er {Дв}?",
               все_прошли="alle {N} geslaagd", прошли_упали="{P} geslaagd, {F} mislukt", из_прошли="{P} van de {N} geslaagd",
               q_файл2="waar staat {Wи}?",
               q_строка2="welke regel {Фр} bevat {W}?",
               q_строка_н2="wat bevat regel {a} {Фр}?",
               q_строк2="hoeveel regels bevat {Ф}?",
               q_ключ2="welke waarde heeft {K} {М}?",
               q_папка2="hoeveel bestanden bevat {Дп}?",
               q_файл3="welk bestand noemt {W}?",
               q_строка3="in welke regel {Фр} komt {Wи} voor?",
               q_выбор2="wat zegt de {c} regel {Фр}?",
               q_конец="wat staat er aan het eind {Фр}?",
               q_читай="lees regel {a} {Фр}.",
               q_покажи="toon regel {a} {Фр}.",
               q_ключ_бк="wat is de waarde van {k} {М}?"),
    "pl": dict(место="{М} {позиция}", инф_акта="{V} {Ф}", пустой="pusty plik {f}", новый="nowy plik {f}",
               тесты_языка="testy {Я}", и="i",
               q_файл="który plik zawiera {W}?", q_файлы="które pliki zawierają {W}?",
               нигде="żaden plik nie zawiera {Wнет}", в_файлах="{Wи} jest w plikach {С}",
               q_строка="w której linii {Фр} jest {Wи}?",
               выбор=("pierwsza", "druga", "ostatnia"), q_выбор="jaka jest {c} linia {Фр}?",
               a_выбор="{c} linia {Фр} to {T}",
               q_строка_н="co jest {М} w linii {a}?", a_строка="{М} w linii {a} jest {T}",
               q_о_ключе="co {Ф} mówi o {k}?", a_о_ключе="{Ф} mówi o kluczu {k} {T}",
               ключ=("klucz {k}", "{k}"), ключ_о=("klucza {k}", "{k}"),
               q_ключ="jaka jest wartość {Kо} {М}?", ключ_ответ="{K} {М} ma wartość {v}",
               q_строк="ile linii ma {Ф}?", q_папка="ile plików jest {Дв}?",
               все_прошли="zaliczono wszystkie {N}", прошли_упали="zaliczono {P}, oblano {F}",
               из_прошли="zaliczono {P} z {N}",
               q_файл2="gdzie jest {Wи}?",
               q_строка2="która linia {Фр} zawiera {W}?",
               q_строка_н2="co stoi {М} w linii {a}?",
               q_строк2="ile linii zawiera {Ф}?",
               q_ключ2="ile wynosi {K} {М}?",
               q_папка2="ile plików zawiera {Дп}?",
               q_файл3="w którym pliku występuje {Wи}?",
               q_строка3="w której linii {Фр} pojawia się {Wи}?",
               q_выбор2="co mówi {c} linia {Фр}?",
               q_конец="co jest napisane na końcu {Фр}?",
               q_читай="przeczytaj linię {a} {Фр}.",
               q_покажи="pokaż linię {a} {Фр}.",
               q_ключ_бк="jaka jest wartość {k} {М}?"),
}
# ВВОДНОЕ «СЕЙЧАС» У ВОПРОСА О ЧИСЛЕ ФАЙЛОВ — пара «одна форма = другая минус слова» там, где голая форма папки ей не
# пара (немецкое «im Ordner» ↔ «in», итальянское «nella cartella» ↔ «in», португальское «na pasta» ↔ «em»)
for _я, (_q1, _q2) in {"en": ("how many files are {Дв} now?", "how many files does {Дп} contain now?"),
                       "ru": ("сколько файлов сейчас {Дв}?", "сколько файлов сейчас содержит {Дп}?"),
                       "de": ("wie viele Dateien sind jetzt {Дв}?", "wie viele Dateien enthält {Дп} jetzt?"),
                       "fr": ("combien de fichiers y a-t-il maintenant {Дв} ?", "combien de fichiers contient {Дп} maintenant ?"),
                       "es": ("¿cuántos archivos hay ahora {Дв}?", "¿cuántos archivos contiene {Дп} ahora?"),
                       "it": ("quanti file ci sono adesso {Дв}?", "quanti file contiene {Дп} adesso?"),
                       "pt": ("quantos ficheiros há agora {Дв}?", "quantos ficheiros contém {Дп} agora?"),
                       "nl": ("hoeveel bestanden zitten er nu {Дв}?", "hoeveel bestanden bevat {Дп} nu?"),
                       "pl": ("ile plików jest teraz {Дв}?", "ile plików zawiera {Дп} teraz?")}.items():
    РЕЧЬ[_я]["q_папка_сейчас"], РЕЧЬ[_я]["q_папка2_сейчас"] = _q1, _q2
# ВОПРОС «СКОЛЬКО ТЕСТОВ ПРОХОДИТ» — ответ берёт прогон мира-процесса (слот {Т} — тесты языка проекта, {Я} — сам язык)
for _я, _q in {"en": "how many of {Т} pass?", "ru": "сколько тестов {Я} проходит?", "de": "wie viele Tests für {Я} bestehen?",
               "fr": "combien de tests {Я} réussissent ?", "es": "¿cuántas pruebas de {Я} pasan?",
               "it": "quanti test {Я} passano?", "pt": "quantos testes de {Я} passam?",
               "nl": "hoeveel tests voor {Я} slagen?", "pl": "ile testów {Я} przechodzi?"}.items():
    РЕЧЬ[_я]["q_тесты"] = _q
# zu/te-форма инфинитива акта двери хода — ветка «иначе» в предложении условного приказа («sonst die Datei X zu
# erstellen»); у прочих языков она — сам инфинитив
for _я, _р in РЕЧЬ.items():
    _р["zu_акта"] = {"de": "{Ф} zu {V}", "nl": "{Ф} te {V}"}.get(_я, _р["инф_акта"])
# ГЛАГОЛЫ ЧТЕНИЙ (27.09, наряд ведущего (d)) — повелительные формы вопроса тем же ходом мира: найди текст («search for
# the word "x"», «поищи слово «x»»), покажи строку («display line 2 of the file F», «give me line 2 …»), посчитай
# файлы папки и строки файла; ответ — тот же, что у вопроса
for _я, _речь in {
        "en": dict(q_ищи=("search for {W}.", "look for {W}.", "locate {W}."), q_выведи="display line {a} {Фр}.",
                   q_дай="give me line {a} {Фр}.", q_посчитай=("count the files {Дв}.", "tally the files {Дв}."),
                   q_посчитай_строки="count the lines {М}."),
        "ru": dict(q_ищи=("поищи {W}.", "отыщи {W}.", "разыщи {W}."), q_выведи="выведи строку {a} {Фр}.",
                   q_дай="дай мне строку {a} {Фр}.", q_посчитай=("посчитай файлы {Дв}.", "пересчитай файлы {Дв}."),
                   q_посчитай_строки="посчитай строки {М}."),
        "de": dict(q_ищи=("suche {W}.", "finde {W}.", "spüre {W} auf."), q_выведи="zeige Zeile {a} {Фр} an.",
                   q_дай="gib mir Zeile {a} {Фр}.",
                   q_посчитай=("zähle die Dateien {Дв}.", "zähl die Dateien {Дв} durch."),
                   q_посчитай_строки="zähle die Zeilen {М}."),
        "fr": dict(q_ищи=("cherche {W}.", "trouve {W}.", "repère {W}."), q_выведи="affiche la ligne {a} {Фр}.",
                   q_дай="donne-moi la ligne {a} {Фр}.",
                   q_посчитай=("compte les fichiers {Дв}.", "dénombre les fichiers {Дв}."),
                   q_посчитай_строки="compte les lignes {Фр}."),
        "es": dict(q_ищи=("busca {W}.", "encuentra {W}.", "localiza {W}."), q_выведи="visualiza la línea {a} {Фр}.",
                   q_дай="dame la línea {a} {Фр}.",
                   q_посчитай=("cuenta los archivos {Дв}.", "haz el recuento de los archivos {Дв}."),
                   q_посчитай_строки="cuenta las líneas {Фр}."),
        "it": dict(q_ищи=("cerca {W}.", "trova {W}.", "individua {W}."), q_выведи="visualizza la riga {a} {Фр}.",
                   q_дай="dammi la riga {a} {Фр}.", q_посчитай=("conta i file {Дв}.", "fai il conto dei file {Дв}."),
                   q_посчитай_строки="conta le righe {Фр}."),
        "pt": dict(q_ищи=("procura {W}.", "encontra {W}.", "localiza {W}."), q_выведи="apresenta a linha {a} {Фр}.",
                   q_дай="dá-me a linha {a} {Фр}.",
                   q_посчитай=("conta os ficheiros {Дв}.", "faz a contagem dos ficheiros {Дв}."),
                   q_посчитай_строки="conta as linhas {Фр}."),
        "nl": dict(q_ищи=("zoek {W}.", "vind {W}.", "spoor {W} op."), q_выведи="geef regel {a} {Фр} weer.",
                   q_дай="geef me regel {a} {Фр}.", q_посчитай=("tel de bestanden {Дв}.", "tel de bestanden {Дв} na."),
                   q_посчитай_строки="tel de regels {М}."),
        "pl": dict(q_ищи=("znajdź {W}.", "odszukaj {W}.", "wyszukaj {W}."), q_выведи="wyświetl linię {a} {Фр}.",
                   q_дай="daj mi linię {a} {Фр}.", q_посчитай=("policz pliki {Дв}.", "przelicz pliki {Дв}."),
                   q_посчитай_строки="policz linie {М}.")}.items():
    РЕЧЬ[_я].update(_речь)
# СЛОВАРЬ ЖИВЫХ ПРОСЬБ (27.09, наряд ведущего (d)): «which file in the repo contains …?» ({Мр} — имя двери `РЕПО`),
# значение «настройки», «параметра», «записи» у ключа и «посмотри значение ключа …», «сколько вхождений …?», «число
# файлов в папке», «число строк файла», перечень файлов папки (прямо, вопросом, «покажи»)
for _я, _речь in {
        "en": dict(q_файл_репо="which file {Мр} contains {W}?",
                   ключ_ед=("of the setting {k}", "of the option {k}", "of the entry {k}"),
                   q_ключ_найди="look up the value of the key {k} {М}.",
                   q_вхождений="how many occurrences of {Wи} are there {М}?",
                   q_число_файлов="what is the file count {Дв}?", q_число_строк="what is the line count {Фр}?",
                   q_список=("list the files {Дв}.", "what files are there {Дв}?", "show the files {Дв}.")),
        "ru": dict(q_файл_репо="в каком файле {Мр} есть {Wи}?", ключ_ед=("у настройки {k}", "у параметра {k}", "у записи {k}"),
                   q_ключ_найди="посмотри значение ключа {k} {М}.", q_вхождений="сколько вхождений {Wнет} {М}?",
                   q_число_файлов="каково число файлов {Дв}?", q_число_строк="каково число строк {М}?",
                   q_список=("перечисли файлы {Дв}.", "какие файлы есть {Дв}?", "покажи файлы {Дв}.")),
        "de": dict(q_файл_репо="welche Datei {Мр} enthält {W}?",
                   ключ_ед=("die Einstellung {k}", "die Option {k}", "der Eintrag {k}"),
                   q_ключ_найди="schau den Wert des Schlüssels {k} {М} nach.",
                   q_вхождений="wie viele Vorkommen hat {Wи} {М}?",
                   q_число_файлов="wie hoch ist die Anzahl der Dateien {Дв}?",
                   q_число_строк="wie hoch ist die Zeilenzahl {Фр}?",
                   q_список=("liste die Dateien {Дв} auf.", "welche Dateien gibt es {Дв}?", "zeig die Dateien {Дв}.")),
        "fr": dict(q_файл_репо="quel fichier {Мр} contient {W} ?",
                   ключ_ед=("du paramètre {k}", "de l'option {k}", "de l'entrée {k}"),
                   q_ключ_найди="cherche la valeur de la clé {k} {М}.",
                   q_вхождений="combien d'occurrences compte {Wи} {М} ?",
                   q_число_файлов="quel est le nombre de fichiers {Дв} ?",
                   q_число_строк="quel est le nombre de lignes {Фр} ?",
                   q_список=("liste les fichiers {Дв}.", "quels fichiers y a-t-il {Дв} ?", "montre les fichiers {Дв}.")),
        "es": dict(q_файл_репо="¿qué archivo {Мр} contiene {W}?",
                   ключ_ед=("del ajuste {k}", "de la opción {k}", "de la entrada {k}"),
                   q_ключ_найди="consulta el valor de la clave {k} {М}.",
                   q_вхождений="¿cuántas apariciones tiene {Wи} {М}?",
                   q_число_файлов="¿cuál es el número de archivos {Дв}?",
                   q_число_строк="¿cuál es el número de líneas {Фр}?",
                   q_список=("enumera los archivos {Дв}.", "¿qué archivos hay {Дв}?", "muestra los archivos {Дв}.")),
        "it": dict(q_файл_репо="quale file {Мр} contiene {W}?",
                   ключ_ед=("dell'impostazione {k}", "dell'opzione {k}", "della voce {k}"),
                   q_ключ_найди="controlla il valore della chiave {k} {М}.",
                   q_вхождений="quante occorrenze ha {Wи} {М}?",
                   q_число_файлов="qual è il numero di file {Дв}?", q_число_строк="qual è il numero di righe {Фр}?",
                   q_список=("elenca i file {Дв}.", "quali file ci sono {Дв}?", "mostra i file {Дв}.")),
        "pt": dict(q_файл_репо="que ficheiro {Мр} contém {W}?",
                   ключ_ед=("da definição {k}", "da opção {k}", "da entrada {k}"),
                   q_ключ_найди="consulta o valor da chave {k} {М}.",
                   q_вхождений="quantas ocorrências tem {Wи} {М}?",
                   q_число_файлов="qual é o número de ficheiros {Дв}?",
                   q_число_строк="qual é o número de linhas {Фр}?",
                   q_список=("lista os ficheiros {Дв}.", "que ficheiros há {Дв}?", "mostra os ficheiros {Дв}.")),
        "nl": dict(q_файл_репо="welk bestand {Мр} bevat {W}?",
                   ключ_ед=("van de instelling {k}", "van de optie {k}", "van het item {k}"),
                   q_ключ_найди="zoek de waarde van de sleutel {k} {М} op.",
                   q_вхождений="hoe vaak komt {Wи} {М} voor?",
                   q_число_файлов="wat is het aantal bestanden {Дв}?", q_число_строк="wat is het aantal regels {Фр}?",
                   q_список=("noem de bestanden {Дв} op.", "welke bestanden staan er {Дв}?", "toon de bestanden {Дв}.")),
        "pl": dict(q_файл_репо="który plik {Мр} zawiera {W}?", ключ_ед=("ustawienia {k}", "opcji {k}", "wpisu {k}"),
                   q_ключ_найди="sprawdź wartość klucza {k} {М}.", q_вхождений="ile wystąpień ma {Wи} {М}?",
                   q_число_файлов="jaka jest liczba plików {Дв}?", q_число_строк="jaka jest liczba linii {М}?",
                   q_список=("wypisz pliki {Дв}.", "jakie pliki są {Дв}?", "pokaż pliki {Дв}."))}.items():
    РЕЧЬ[_я].update(_речь)
# СЧЁТ ВХОЖДЕНИЙ ПОВЕЛИТЕЛЬНО (27.09, наряд ведущего (h1)): «count» у акта find — «count the occurrences of the word "x"
# in the repository», «count how many times the word "x" occurs in the folder D»; у голоса — свой вид («посчитай,
# сколько раз слово «x» встречается …», «zähle, wie oft das Wort „x“ … vorkommt»); «вхождения» — лишь где у двери есть
# родительный текста ({Wнет}: «вхождения слова «x»», «wystąpienia słowa „x”»): французское «de le mot» элизия в «du»
# не сводит, испанское «de el texto» — тоже. Ответ — тот же, что у вопроса «сколько раз»
for _я, _q in {"en": ("count the occurrences of {Wнет} {М}.", "count how many times {Wи} occurs {М}."),
               "ru": ("посчитай, сколько раз {Wи} встречается {М}.", "посчитай вхождения {Wнет} {М}."),
               "de": ("zähle, wie oft {Wи} {М} vorkommt.",),
               "fr": ("compte combien de fois {Wи} apparaît {М}.",),
               "es": ("cuenta cuántas veces aparece {Wи} {М}.",),
               "it": ("conta quante volte compare {Wи} {М}.",),
               "pt": ("conta quantas vezes aparece {Wи} {М}.",),
               "nl": ("tel hoe vaak {Wи} {М} voorkomt.",),
               "pl": ("policz, ile razy {Wи} występuje {М}.", "policz wystąpienia {Wнет} {М}.")}.items():
    РЕЧЬ[_я]["q_посчитай_раз"] = _q
# ЗАПИСЬ ПО ИМЕНИ (М-2075): «find the file F» — глаголом поиска двери (`toolacts.РЕЧЬ` «поиск», самопроверка мира
# его держит); «where is the file F?» — вторая форма; «find the file named F» — английское «named» рядом с «called»
# двери имени (пара канонической: форма минус слово); ответ — путь хода мира (одна запись), число записей и пути
# (несколько), «нет» (ни одной); у числа — подлежащее «репозиторий»: глагол не гнётся по числу найденного
for _я, _речь in {
        "en": dict(q_найди="find {Ф}.", q_найди2="where is {Ф}?", q_найди_имя="find the file named {f}.",
                   q_имён="how many files are named {f}?", q_имён_сейчас="how many files are named {f} now?",
                   a_путь="the path {Фр} is {С}", a_имён="the repository has {N} named {f}",
                   a_нет_имени="the repository has no file named {f}"),
        "ru": dict(q_найди="найди {Ф}.", q_найди2="где лежит {Ф}?",
                   q_имён="сколько файлов с именем {f}?", q_имён_сейчас="сколько сейчас файлов с именем {f}?",
                   a_путь="путь {Фр} — {С}", a_имён="в репозитории {N} с именем {f}",
                   a_нет_имени="в репозитории нет файла с именем {f}"),
        "de": dict(q_найди="suche {Ф}.", q_найди2="wo liegt {Ф}?",
                   q_имён="wie viele Dateien heißen {f}?", q_имён_сейчас="wie viele Dateien heißen jetzt {f}?",
                   a_путь="der Pfad {Фр} ist {С}", a_имён="das Repository hat {N} namens {f}",
                   a_нет_имени="das Repository hat keine Datei namens {f}"),
        "fr": dict(q_найди="cherche {Ф}.", q_найди2="où se trouve {Ф} ?",
                   q_имён="combien de fichiers s'appellent {f} ?",
                   q_имён_сейчас="combien de fichiers s'appellent {f} maintenant ?",
                   a_путь="le chemin {Фр} est {С}", a_имён="le dépôt contient {N} portant le nom {f}",
                   a_нет_имени="le dépôt ne contient aucun fichier portant le nom {f}"),
        "es": dict(q_найди="busca {Ф}.", q_найди2="¿dónde está {Ф}?",
                   q_имён="¿cuántos archivos se llaman {f}?", q_имён_сейчас="¿cuántos archivos se llaman {f} ahora?",
                   a_путь="la ruta {Фр} es {С}", a_имён="el repositorio tiene {N} con el nombre {f}",
                   a_нет_имени="el repositorio no tiene ningún archivo con el nombre {f}"),
        "it": dict(q_найди="cerca {Ф}.", q_найди2="dove si trova {Ф}?",
                   q_имён="quanti file si chiamano {f}?", q_имён_сейчас="quanti file si chiamano {f} adesso?",
                   a_путь="il percorso {Фр} è {С}", a_имён="il repository ha {N} con il nome {f}",
                   a_нет_имени="il repository non ha nessun file con il nome {f}"),
        "pt": dict(q_найди="procura {Ф}.", q_найди2="onde está {Ф}?",
                   q_имён="quantos ficheiros se chamam {f}?", q_имён_сейчас="quantos ficheiros se chamam {f} agora?",
                   a_путь="o caminho {Фр} é {С}", a_имён="o repositório tem {N} com o nome {f}",
                   a_нет_имени="o repositório não tem nenhum ficheiro com o nome {f}"),
        "nl": dict(q_найди="zoek {Ф}.", q_найди2="waar staat {Ф}?",
                   q_имён="hoeveel bestanden heten {f}?", q_имён_сейчас="hoeveel bestanden heten nu {f}?",
                   a_путь="het pad {Фр} is {С}", a_имён="de repository heeft {N} met de naam {f}",
                   a_нет_имени="de repository heeft geen bestand met de naam {f}"),
        "pl": dict(q_найди="znajdź {Ф}.", q_найди2="gdzie jest {Ф}?",
                   q_имён="ile plików nazywa się {f}?", q_имён_сейчас="ile plików nazywa się teraz {f}?",
                   a_путь="ścieżka {Фр} to {С}", a_имён="repozytorium ma {N} o nazwie {f}",
                   a_нет_имени="repozytorium nie ma pliku o nazwie {f}")}.items():
    РЕЧЬ[_я].update(_речь)
# ГДЕ ЛЕЖИТ И В КАКОЙ ПАПКЕ (27.09, слово ведущего): «locate F» — повелительно глаголом голоса («найди, где лежит F»,
# «finde heraus, wo F liegt», «zoek uit waar F staat»); «which folder holds F?» — ответ называет папку (родителя пути
# хода мира) и путь: «the file chores.md is in the folder home: home/chores.md»; у нескольких записей — их число и пути.
# Немецкий — «welcher Ordner enthält F?»: дательного «welchem» пакет языка зачином не объявил («in welchem Ordner liegt
# cake.md?» самопроверка зовёт незачинным, когда знак имени файла уводит вопрос к английскому)
for _я, (_где, _папка, _ответ) in {
        "en": ("locate {Ф}.", "which folder holds {f}?", "{Ф} is {Дв}"),
        "ru": ("найди, где лежит {Ф}.", "в какой папке {f}?", "{Ф} лежит {Дв}"),
        "de": ("finde heraus, wo {Ф} liegt.", "welcher Ordner enthält {f}?", "{Ф} liegt {Дв}"),
        "fr": ("localise {Ф}.", "dans quel dossier se trouve {f} ?", "{Ф} se trouve {Дв}"),
        "es": ("localiza {Ф}.", "¿en qué carpeta está {f}?", "{Ф} está {Дв}"),
        "it": ("localizza {Ф}.", "in quale cartella si trova {f}?", "{Ф} si trova {Дв}"),
        "pt": ("localiza {Ф}.", "em que pasta está {f}?", "{Ф} está {Дв}"),
        "nl": ("zoek uit waar {Ф} staat.", "in welke map staat {f}?", "{Ф} staat {Дв}"),
        "pl": ("zlokalizuj {Ф}.", "w którym folderze jest {f}?", "{Ф} jest {Дв}")}.items():
    РЕЧЬ[_я].update(q_где_лежит=_где, q_какая_папка=_папка, a_папка=_ответ)
# «найти файл F» инфинитивом голоса — у регистров, какие держат {inf} (28.09, конструкции записи по имени)
for _я, _инф in {"en": "find {Ф}", "ru": "найти {Ф}", "de": "{Ф} suchen", "fr": "chercher {Ф}", "es": "buscar {Ф}",
                 "it": "cercare {Ф}", "pt": "procurar {Ф}", "nl": "{Ф} zoeken", "pl": "znaleźć {Ф}"}.items():
    РЕЧЬ[_я]["q_найди_инф"] = _инф
# «in the repository» — место слова во всём мире
# за ним — имена того же места в живой речи программиста (27.09, наряд (d): repo, project, codebase): одна дверь,
# первое имя каноническое — его говорит организм
РЕПО = {"en": ("in the repository", "in the repo", "in the project", "in the codebase"),
        "ru": ("в репозитории", "в репо", "в проекте", "в кодовой базе"),
        "de": ("im Repository", "im Repo", "im Projekt", "in der Codebasis"),
        "fr": ("dans le dépôt", "dans le repo", "dans le projet", "dans la base de code"),
        "es": ("en el repositorio", "en el repo", "en el proyecto", "en la base de código"),
        "it": ("nel repository", "nel repo", "nel progetto", "nella codebase"),
        "pt": ("no repositório", "no repo", "no projeto", "na base de código"),
        "nl": ("in de repository", "in de repo", "in het project", "in de codebase"),
        "pl": ("w repozytorium", "w repo", "w projekcie", "w bazie kodu")}
РЕЧЬ_РЕПО = {я: места[0] for я, места in РЕПО.items()}
# ВОПРОСЫ О ТОМ ЖЕ АКТЕ И ПОВЕЛИТЕЛЬНОЕ СЛОВО ВЫБОРА (27.09, наряд ведущего (h2)): «do the Python tests pass?» —
# зачином, какой объявил пакет голоса (`asking`): «проходят ли …», «sind … erfolgreich?», «¿se superan …?», «sono
# superati …?», «… são aprovados?», «zijn … geslaagd?» (слово исхода — то, каким дом говорит о прошедших тестах); ряд
# «выбор_в» — слово выбора в винительном («первую», «die erste», «pierwszą»), при нём повелительные формы вопроса о
# строке по выбору: прочитай — голым файлом, покажи, выведи
for _я, _речь in {
        "en": dict(q_тесты_ли="do {Т} pass?",
                   выбор_в=("first", "second", "last"), q_выбор_читай="read the {cv} line {Фр1}.",
                   q_выбор_покажи="show the {cv} line {Фр}.", q_выбор_выведи="display the {cv} line {Фр}."),
        "ru": dict(q_тесты_ли="проходят ли {Т}?",
                   выбор_в=("первую", "вторую", "последнюю"), q_выбор_читай="прочитай {cv} строку {Фр1}.",
                   q_выбор_покажи="покажи {cv} строку {Фр}.", q_выбор_выведи="выведи {cv} строку из {Фр}."),
        "de": dict(q_тесты_ли="sind {Т} erfolgreich?",
                   выбор_в=("erste", "zweite", "letzte"), q_выбор_читай="lies die {cv} Zeile {Фр1}.",
                   q_выбор_покажи="zeig die {cv} Zeile {Фр}.", q_выбор_выведи="zeige die {cv} Zeile {Фр} an."),
        "fr": dict(q_тесты_ли="est-ce que {Т} réussissent ?",
                   выбор_в=("première", "deuxième", "dernière"), q_выбор_читай="lis la {cv} ligne {Фр1}.",
                   q_выбор_покажи="montre la {cv} ligne {Фр}.", q_выбор_выведи="affiche la {cv} ligne {Фр}."),
        "es": dict(q_тесты_ли="¿se superan {Т}?",
                   выбор_в=("primera", "segunda", "última"), q_выбор_читай="lee la {cv} línea {Фр1}.",
                   q_выбор_покажи="muestra la {cv} línea {Фр}.", q_выбор_выведи="visualiza la {cv} línea {Фр}."),
        "it": dict(q_тесты_ли="sono superati {Т}?",
                   выбор_в=("la prima", "la seconda", "l'ultima"), q_выбор_читай="leggi {cv} riga {Фр1}.",
                   q_выбор_покажи="mostra {cv} riga {Фр}.", q_выбор_выведи="visualizza {cv} riga {Фр}."),
        "pt": dict(q_тесты_ли="{Т} são aprovados?",
                   выбор_в=("primeira", "segunda", "última"), q_выбор_читай="lê a {cv} linha {Фр1}.",
                   q_выбор_покажи="mostra a {cv} linha {Фр}.", q_выбор_выведи="apresenta a {cv} linha {Фр}."),
        "nl": dict(q_тесты_ли="zijn {Т} geslaagd?",
                   выбор_в=("eerste", "tweede", "laatste"), q_выбор_читай="lees de {cv} regel {Фр1}.",
                   q_выбор_покажи="toon de {cv} regel {Фр}.", q_выбор_выведи="geef de {cv} regel {Фр} weer."),
        "pl": dict(q_тесты_ли="czy {Т} przechodzą?",
                   выбор_в=("pierwszą", "drugą", "ostatnią"), q_выбор_читай="przeczytaj {cv} linię {Фр1}.",
                   q_выбор_покажи="pokaż {cv} linię {Фр}.", q_выбор_выведи="wyświetl {cv} linię {Фр}.")}.items():
    РЕЧЬ[_я].update(_речь)
# ПРОГОН БЕЗ ТЕСТОВ (28.09, наряд ведущего «исходы прогона»): бегун не нашёл ни одного теста — числа у итога нет, мир его
# не пишет («NO TESTS RAN»)
for _я, _фраза in {"en": "no tests ran", "ru": "не запущено ни одного теста", "de": "es lief kein Test",
                   "fr": "aucun test n'a été exécuté", "es": "no se ejecutó ninguna prueba",
                   "it": "non è stato eseguito nessun test", "pt": "não foi executado nenhum teste",
                   "nl": "er is geen enkele test uitgevoerd", "pl": "nie uruchomiono żadnego testu"}.items():
    РЕЧЬ[_я]["ни_одного"] = _фраза
# ОШИБКА ТЕСТА (слово ведущего 28.09): у unittest упавший тест — провал («failures») или ошибка («errors»); итог называет
# вычтенное словом отказа, как бегун: провал — словом провала голоса (вторая половина `прошли_упали`, та же дверь, что у
# отчёта cargo), ошибку — своим словом, согласным с числом
for _я, _формы in {"en": ("error", "errors"), "ru": ("ошибка", "ошибки", "ошибок"), "de": ("Fehler", "Fehler"),
               "fr": ("erreur", "erreurs"), "es": ("error", "errores"), "it": ("errore", "errori"), "pt": ("erro", "erros"),
               "nl": ("fout", "fouten"), "pl": ("błąd", "błędy", "błędów")}.items():
    РЕЧЬ[_я]["ошибки"] = _формы
РЕГИСТРЫ = ("плоский", "вежливый")
# КОНСТРУКЦИИ ПРОСЬБЫ (28.09, наряд ведущего по классам отложенного ключа H2: «иная конструкция»): косвенный регистр двери
# («we need to …», «нужно …», «il faut …» — дом его прежде не показывал) и два новых — нужда первым лицом («i need to …») и
# желание («i would like to …»); на основах вопросных регистров всякого акта, пара — та же страница плоско
КОНСТРУКЦИИ = ("косвенный", "нужда", "желание")
# СОСТАВНЫЕ СТРАНИЦЫ (наряд 28.09: дальний ярус H2 — конструкция и ещё два хода): нужда и желание × первый синоним ×
# голый путь («i need to remove shopping.txt»)
СОСТАВНЫЕ_РЕГИСТРЫ = ("нужда", "желание")

# ======================================================================================================
# РОДЫ ДОМА
# ======================================================================================================
СОЗДАТЬ = "создать файл по пути"
СОЗДАТЬ_ПАПКА = "создать файл в названной папке"
СОЗДАТЬ_ЕСТЬ = "создать файл, который уже есть"
СОЗДАТЬ_ОТКАЗ = "создать файл — отказ"
УДАЛИТЬ = "удалить файл по пути"
УДАЛИТЬ_ПАПКА = "удалить файл из названной папки"
УДАЛИТЬ_НЕТ = "удалить файл, которого нет"
УДАЛИТЬ_ОТКАЗ = "удалить файл — отказ"
ПЕРЕНОС = "перенести файл в названную папку"
ПЕРЕНОС_НЕТ = "перенести файл, которого нет"
ПЕРЕНОС_ОТКАЗ = "перенести файл — отказ"
ИМЯ = "переименовать файл по пути"
ИМЯ_ЗАНЯТО = "переименовать в имя, занятое в той же папке"
ИМЯ_НЕТ = "переименовать файл, которого нет"
ИМЯ_ОТКАЗ = "переименовать файл — отказ"
ЗАМЕНА = "заменить текст в кавычках"
ЗАМЕНА_СЛОВА = "заменить слово в файле по пути"
ЗАМЕНА_НЕТ = "заменить текст, которого в файле нет"
ЗАМЕНА_ОТКАЗ = "заменить текст — отказ"
ДОПИСАТЬ = "дописать строку в кавычках"
ДОПИСАТЬ_ОТКАЗ = "дописать строку — отказ"
ТЕСТЫ = "прогон тестов по языку проекта"
ТЕСТЫ_ОТКАЗ = "прогон тестов — отказ"
ПЛАН_ЗАМЕНА = "план: заменить, затем прогнать тесты"
ПЛАН_ДОПИСАТЬ = "план: дописать, затем прогнать тесты"
ПЛАН_ПЕРЕНОС = "план: перенести, затем удалить"
ПЛАН_ОТКАЗ = "план из двух актов — отказ"
В_КАКОМ = "в каком файле текст — вопрос"
В_КАКИХ = "в каких файлах слово — вопрос списком"
НИГДЕ = "текста нет ни в одном файле — вопрос"
НА_СТРОКЕ = "на какой строке файла текст — вопрос"
ВЫБОР = "первая, вторая, последняя строка файла — вопрос"
СТРОКА_Н = "строка файла с номером — вопрос"
КЛЮЧ = "значение ключа в файле настроек — вопрос"
О_КЛЮЧЕ = "что файл настроек говорит о ключе — вопрос"
СТРОК = "сколько строк в файле — вопрос"
РАЗ = "сколько раз слово в папке и во всём репозитории — вопрос"
ФАЙЛОВ = "сколько файлов в папке — вопрос"
# ПЛАН С МЕСТОИМЕНИЕМ (25.09, вопрос 4 коллегии; роды ведущего): второй приказ называет объект первого местоимением
МЕСТО_СОЗДАТЬ = "план с местоимением: создать, затем дописать в него"
МЕСТО_ИМЯ = "план с местоимением: переименовать, затем дописать в него"
МЕСТО_ПЕРЕНОС = "план с местоимением: перенести в папку, затем удалить его"
МЕСТО_НАЙТИ = "план с местоимением: найти файл со словом, затем дописать в него"
МЕСТО_ОТКАЗ = "план с местоимением — отказ"
МЕСТО_НЕВОЗМОЖНО = "план с местоимением — первый акт невозможен"
МЕСТО_МНОГО = "план с местоимением — слово в нескольких файлах, второй акт ждёт одного"
МЕСТО_СТРОК = "план с местоимением: акт, затем сколько строк в нём"
# РОДЫ ЖИВЫХ ПРОСЬБ (26.09, третий заказ ведущего: по переписи живых просьб к агенту, не по ключам)
ТРИ_АКТА = "план из трёх актов: акт, дописать туда же, затем сколько строк или прогон"
УСЛОВИЕ_ДОПИСАТЬ = "условный приказ: если файл есть — дописать, иначе создать"
УСЛОВИЕ_УДАЛИТЬ = "условный приказ: если файл есть — удалить"
УСЛОВИЕ_ЗАМЕНА = "условный приказ: если текст в файле есть — заменить"
ВСЕ_КРОМЕ = "все файлы папки, кроме названного"
ДВА_ОБЪЕКТА = "два объекта в одном приказе"
# РОДЫ, КАКИХ ДОМ НЕ ПОКАЗЫВАЛ (26.09, наряд ведущего по переписи): вопрос «сколько тестов проходит» — ответ берёт прогон;
# план «прогони тесты, затем скажи, сколько прошло»; находка файла, затем «сколько в нём строк» — вид МЕСТО_НАЙТИ
ТЕСТЫ_СКОЛЬКО = "сколько тестов проходит — вопрос, ответ берёт прогон"
ПЛАН_ТЕСТЫ_СКОЛЬКО = "план: прогнать тесты, затем сказать, сколько прошло"
# ЗАЧИН ПЕРЕД ВТОРЫМ ВОПРОСОМ ПЛАНА (27.09, наряд ведущего): «…, then tell me what its first line is» — зачин просьбы
# сказать (`toolacts.ЗАЧИН`) перед вопросом, какой дом прежде показывал лишь одиночным; вид зачина — последняя часть
# формы («имя·первая·1»); вопрос «файл» — у двери и суда, в показах — нет (цена названа в показах)
ПЛАН_СКАЖИ = "план: акт, затем зачин просьбы сказать и вопрос о файле, какой двинул акт"
# ВОПРОС О ПРОШЛОМ АКТЕ (27.09, наряд ведущего: контрастная пара к «delete F») — «did you delete the file F?»: мир
# читает файл, акт удаления не идёт; форма — что прочёл мир («есть», «нет»)
ПРОШЛОЕ = "вопрос о прошлом акте: удалил ли ты файл — ответ чтением мира, не актом"
# ПЕРЕЧЕНЬ ФАЙЛОВ ПАПКИ (27.09, наряд ведущего (d), глагол «list»): «list the files in the folder D» — мир называет записи
# места (`list`), ответ — они же словами двери папки
СПИСОК = "перечень файлов папки — вопрос, ответ записями хода мира"
РОДЫ = (СОЗДАТЬ, СОЗДАТЬ_ПАПКА, СОЗДАТЬ_ЕСТЬ, СОЗДАТЬ_ОТКАЗ, УДАЛИТЬ, УДАЛИТЬ_ПАПКА, УДАЛИТЬ_НЕТ, УДАЛИТЬ_ОТКАЗ,
        ПЕРЕНОС, ПЕРЕНОС_НЕТ, ПЕРЕНОС_ОТКАЗ, ИМЯ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ, ИМЯ_ОТКАЗ, ЗАМЕНА, ЗАМЕНА_СЛОВА, ЗАМЕНА_НЕТ,
        ЗАМЕНА_ОТКАЗ, ДОПИСАТЬ, ДОПИСАТЬ_ОТКАЗ, ТЕСТЫ, ТЕСТЫ_ОТКАЗ, ПЛАН_ЗАМЕНА, ПЛАН_ДОПИСАТЬ, ПЛАН_ПЕРЕНОС,
        ПЛАН_ОТКАЗ, В_КАКОМ, В_КАКИХ, НИГДЕ, НА_СТРОКЕ, ВЫБОР, СТРОКА_Н, КЛЮЧ, О_КЛЮЧЕ, СТРОК, РАЗ, ФАЙЛОВ,
        МЕСТО_СОЗДАТЬ, МЕСТО_ИМЯ, МЕСТО_ПЕРЕНОС, МЕСТО_НАЙТИ, МЕСТО_ОТКАЗ, МЕСТО_НЕВОЗМОЖНО, МЕСТО_МНОГО, МЕСТО_СТРОК,
        ТРИ_АКТА, УСЛОВИЕ_ДОПИСАТЬ, УСЛОВИЕ_УДАЛИТЬ, УСЛОВИЕ_ЗАМЕНА, ВСЕ_КРОМЕ, ДВА_ОБЪЕКТА, ТЕСТЫ_СКОЛЬКО,
        ПЛАН_ТЕСТЫ_СКОЛЬКО, ПЛАН_СКАЖИ, ПРОШЛОЕ, СПИСОК)
ВОПРОСЫ = frozenset({В_КАКОМ, В_КАКИХ, НИГДЕ, НА_СТРОКЕ, ВЫБОР, СТРОКА_Н, КЛЮЧ, О_КЛЮЧЕ, СТРОК, РАЗ, ФАЙЛОВ, ПРОШЛОЕ,
                     СПИСОК})
# ВОПРОСЫ О ТОМ ЖЕ АКТЕ, ОТВЕЧЕННЫЕ ЗНАЧЕНИЕМ МИРА (27.09, наряд ведущего (h2), перепись дома: у прогона был лишь
# вопрос «сколько проходит», у находки в одном файле — лишь «на какой строке»): «проходят ли тесты» — предложение
# прогнать, ход мира-процесса, ответ «да» или «нет» по исходу мира; «сколько раз слово в файле» — форма «файл» рода
# РАЗ. «Есть ли файл» — нет: акта с ответом «да / нет» у дома нет (слово ведущего)
ТЕСТЫ_ЛИ = "проходят ли тесты — вопрос, ответ берёт прогон: да или нет"
РОДЫ += (ТЕСТЫ_ЛИ,)
# повелительные формы вопроса о строке по выбору со словом выбора в винительном (ряды «выбор_в» и «q_выбор_…» речи)
ВЫБОР_ПОВЕЛИТЕЛЬНО = ("выбор·читай", "выбор·покажи", "выбор·выведи")
# ЗАПИСЬ ПО ИМЕНИ (27.09, наряд ведущего (c); закон мира М-2075 — чтение `locate <имя>`): «find the file F», «where is
# the file F?» — мир называет всякую запись этого имени во всём дереве; ответ — путь хода мира, у нескольких записей —
# их число и пути, у ни одной — «нет»; «how many files are named F?» — числом записей мира. Роды прибавлены к РОДЫ и
# ВОПРОСЫ, а не вписаны в строки их литералов
ГДЕ_ФАЙЛ = "файл по имени во всём дереве — вопрос, ответ путём хода мира"
ГДЕ_ФАЙЛЫ = "файлов одного имени несколько — ответ их числом и путями"
НЕТ_ФАЙЛА = "файла с этим именем нет ни в одной папке — вопрос"
ФАЙЛОВ_ИМЕНИ = "сколько файлов с этим именем — вопрос"
РОДЫ += (ГДЕ_ФАЙЛ, ГДЕ_ФАЙЛЫ, НЕТ_ФАЙЛА, ФАЙЛОВ_ИМЕНИ)
ВОПРОСЫ |= {ГДЕ_ФАЙЛ, ГДЕ_ФАЙЛЫ, НЕТ_ФАЙЛА, ФАЙЛОВ_ИМЕНИ}
# ИСХОДЫ ПРОГОНА (28.09, наряд ведущего omega-90): приказ прогона одним актом на проекте в том состоянии, какое держит
# мир (правка, какая дала состояние, страницей не названа), — всякий исход мира процесса, какого прогон на объявленном
# проекте не показывал ни у одного бегуна: провал и ошибка unittest, прогон без тестов (unittest «NO TESTS RAN», код 5),
# провал полного прогона крейта. Исход читается из строк отчёта, как у прежних страниц прогона (`исход`). Успеха cargo
# в роде нет: его форма — та же, что у успеха Python («all # tests passed»), место её исхода ядро купило числом перед
# «tests», и страницы успеха cargo дали бы месту второе прочтение (число перед «passed», немое на страницах Python) —
# ядро отказало бы месту, и сказуемый ныне успех стал бы несказуем (долг ядра, слово ведущего 28.09)
ИСХОДЫ = "прогон тестов — исход мира процесса, какого прогон на объявленном проекте не показывал"
РОДЫ += (ИСХОДЫ,)
# ДВА РАЗНЫХ АКТА (28.09, заказ руки joins2 через ведущего omega-90, к М-2090 «у голоса столько связок, сколько их
# свидетельствуют разные пары актов»): план из двух разных актов над разными файлами — «move the file F to the folder
# D, then append the line "x" to the file G»; всякий акт пары дом кладёт и одиночной страницей. Пары — те, каких дом
# планом не показывал; форма — пара актов («перенос+дописать»), союзом «and» — «…·союз» (`СОЮЗОМ`)
ДВА_АКТА = "план из двух разных актов над разными файлами"
РОДЫ += (ДВА_АКТА,)
ПАРЫ_АКТОВ = ("перенос+дописать", "создать+удалить", "дописать+замена", "имя+дописать", "удалить+создать")
# ПРОЧИТАТЬ ФАЙЛ АКТОМ С ХОДОМ МИРА (29.09, находка ведущего omega-90 по переписи и стеклу ядра): «read the file F» с
# подтверждением свод показывал лишь страницами дома `actturn` без хода мира («user: yes. organism: read the file
# notes.md. the file notes.md contains 20 bytes: 20 = 20.»), а ходы «world: read F · files N · bytes B · path F» — лишь
# внутри условных программ; у рамки чтения не было ни одной страницы с ходом мира, род акта не решался, и после «yes»
# ядро отказывало — немел весь дом чтения. Здесь — исполненное чтение строем прочих актов (М-2018: ход мира между «yes» и
# отчётом), отчёт — тот же, что у дома `actturn`; и чтение файла, которого нет, — отказ мира по имени
ЧТЕНИЕ = "прочитать файл — акт, ход мира read и число байт файла"
ЧТЕНИЕ_НЕТ = "прочитать файл, которого нет — отказ мира по имени"
РОДЫ += (ЧТЕНИЕ, ЧТЕНИЕ_НЕТ)
# ВОПРОС О ПРОШЛОМ ПРОГОНЕ (29.09, находка ведущего по переписи: у мира прогона не было ни одного вопроса «did you run
# the X tests?», и механизму неисполненного акта у органа не на чем было купить формы): мир процесса читает счёт запусков
# прогона (`folderworld.счёт_прогонов`, тот же ход, что у отказа прогона), ответ — «да» или «нет» по клетке runs, с именем
# тестов и отчётом запусков. Зачин вопроса — объявленный зачин голоса (суд вопросов `asking`)
ПРОШЛОЕ_ПРОГОН = "вопрос о прошлом прогоне — чтение счёта запусков, ответ «да» или «нет» по клетке runs"
РОДЫ += (ПРОШЛОЕ_ПРОГОН,)
ВОПРОСЫ |= {ПРОШЛОЕ_ПРОГОН}
ПРОГОН_ПРОШЛОЕ = {
    "en": ("did you run {Т}?", "{да} — {Т} have been run", "{нет} — {Т} have not been run"),
    "ru": ("запустил ли ты {Т}?", "{да} — {Т} запускались", "{нет} — {Т} не запускались"),
    "de": ("sind {Т} gestartet worden?", "{да} — {Т} sind gestartet worden", "{нет} — {Т} sind nicht gestartet worden"),
    "fr": ("est-ce que tu as lancé {Т} ?", "{да} — {Т} ont été lancés", "{нет} — {Т} n'ont pas été lancés"),
    "es": ("¿se ejecutaron {Т}?", "{да} — {Т} se ejecutaron", "{нет} — {Т} no se ejecutaron"),
    "it": ("sono stati eseguiti {Т}?", "{да} — {Т} sono stati eseguiti", "{нет} — {Т} non sono stati eseguiti"),
    "pt": ("é verdade que executaste {Т}?", "{да} — {Т} foram executados", "{нет} — {Т} não foram executados"),
    "nl": ("heb je {Т} gestart?", "{да} — {Т} zijn gestart", "{нет} — {Т} zijn niet gestart"),
    "pl": ("czy uruchomiłeś {Т}?", "{да} — {Т} zostały uruchomione", "{нет} — {Т} nie zostały uruchomione"),
}
ОТКАЗЫ = frozenset({СОЗДАТЬ_ОТКАЗ, УДАЛИТЬ_ОТКАЗ, ПЕРЕНОС_ОТКАЗ, ИМЯ_ОТКАЗ, ЗАМЕНА_ОТКАЗ, ДОПИСАТЬ_ОТКАЗ,
                    ТЕСТЫ_ОТКАЗ, ПЛАН_ОТКАЗ, МЕСТО_ОТКАЗ})
# невозможное — акт, какого мир не дал (или второй акт, какому мир не назвал одного места): итог называет отказ по
# имени, а не дыры приказа; рамка его — рамка исполненного того же приказа
НЕВОЗМОЖНЫЕ = frozenset({СОЗДАТЬ_ЕСТЬ, УДАЛИТЬ_НЕТ, ПЕРЕНОС_НЕТ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ, ЗАМЕНА_НЕТ, МЕСТО_НЕВОЗМОЖНО,
                         МЕСТО_МНОГО, ЧТЕНИЕ_НЕТ})
МЕСТО = frozenset({МЕСТО_СОЗДАТЬ, МЕСТО_ИМЯ, МЕСТО_ПЕРЕНОС, МЕСТО_НАЙТИ, МЕСТО_ОТКАЗ, МЕСТО_НЕВОЗМОЖНО, МЕСТО_МНОГО,
                   МЕСТО_СТРОК})
# условный приказ: ветка — ход мира; итог называет дыры проверки и исполненной ветки, дыры другой ветки — нет
УСЛОВНЫЕ = frozenset({УСЛОВИЕ_ДОПИСАТЬ, УСЛОВИЕ_УДАЛИТЬ, УСЛОВИЕ_ЗАМЕНА})
# МНОГОАКТНЫЕ исполненные роды: их каноническая форма получает вежливую просьбу планом (`вежливо`) — пару одного акта
# мира «одна форма = другая минус слова»
МНОГОАКТНЫЕ = frozenset({ПЛАН_ЗАМЕНА, ПЛАН_ДОПИСАТЬ, ПЛАН_ПЕРЕНОС, МЕСТО_СОЗДАТЬ, МЕСТО_ИМЯ, МЕСТО_ПЕРЕНОС, МЕСТО_НАЙТИ,
                         МЕСТО_СТРОК, ТРИ_АКТА, УСЛОВИЕ_ДОПИСАТЬ, УСЛОВИЕ_УДАЛИТЬ, УСЛОВИЕ_ЗАМЕНА, ВСЕ_КРОМЕ, ДВА_ОБЪЕКТА,
                         ПЛАН_ТЕСТЫ_СКОЛЬКО, ПЛАН_СКАЖИ, ДВА_АКТА})


# ======================================================================================================
# МИР: ход и его клетки; прогоны — по коду проекта
# ======================================================================================================
def папка_пути(путь):
    return путь.rsplit("/", 1)[0] if "/" in путь else ""


def имя_пути(путь):
    return путь.rsplit("/", 1)[-1]


def мера(ход_, имя):
    return dict(ход_.меры)[имя]


def поле(ход_, имя):
    """Значения поля строк хода мира по порядку."""
    return [dict(строка)[имя] for строка in ход_.строки]


# ПАДЕНИЯ ПРОГОНОВ объявлены кодом проекта (тест «doubles» ждёт 5 от 2 + 2); самопроверка сверяет их с отчётом бегуна
def тестов(имя_прогона, проект=ПРОЕКТ):
    """Тестов в коде прогона — по коду проекта в его состоянии: тестовые методы Python («def test_»), функции Rust с
    «#[test]» и блоки кода в документации крейта (доктесты)."""
    код = Р.код_прогона(имя_прогона, проект)
    if Р.БЕГУНЫ[имя_прогона] == "unittest":
        return sum(1 for строки in код.values() for с in строки if с.startswith("    def test_"))
    return sum(1 for строки in код.values() for с in строки if с.strip().startswith("#[test]")) + sum(
        1 for строки in код.values() for с in строки if с.strip() == "/// ```") // 2


# ЧТЕНИЕ ОТЧЁТА БЕГУНА (27.09) — числа итога берутся из отчёта так, как их пишет бегун: unittest — «Ran N tests» и
# «OK» или «FAILED (failures=K, errors=E)»; cargo — всякая строка «test result: … P passed; F failed; …» (у полного
# прогона крейта их несколько — тесты модуля, интеграционные, доктесты, — и дом их складывает)
_RAN = re.compile(r"^Ran (\d+) tests? in ")
_FAILED = re.compile(r"^FAILED \((.*)\)$")
# упавшие unittest — провалы и ошибки строки FAILED, каждое своим словом («failures=4, errors=1»); прогон, не нашедший
# ни одного теста, unittest кончает строкой «NO TESTS RAN» и кодом 5
_УПАВШИЕ = re.compile(r"\b(failures|errors)=(\d+)")
_НЕТ_ТЕСТОВ = "NO TESTS RAN"


def упавшие_отчёта(снятое):
    """[(слово, число)] — упавшие строки FAILED отчёта unittest в том порядке, в каком бегун их пишет."""
    return [(м.group(1), int(м.group(2))) for с in снятое["report"] if (ф := _FAILED.match(с))
            for м in _УПАВШИЕ.finditer(ф.group(1))]


def упавшие_словом(язык, слово, x):
    """Упавшие одного рода словом голоса: провал — словом провала двери отчёта («3 failed», «3 упали»), ошибка — своим
    («1 error», «1 ошибка»)."""
    р = РЕЧЬ[язык]
    if слово == "failures":
        return р["прошли_упали"].split(", ", 1)[1].format(F=x, упали=S._счёт(р["упали"], x, язык) if "упали" in р else "")
    return f"{x} {S._счёт(р['ошибки'], x, язык)}"
_ИТОГ_CARGO = re.compile(r"^test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed;")


def строки_итога(снятое):
    """[(прошло, упало)] — по строке итога бегуна: у cargo — всякая «test result», у unittest — одна (прошедших
    unittest не пишет: они — «Ran N» без упавших)."""
    вон = [(int(м.group(1)), int(м.group(2))) for с in снятое["report"] if (м := _ИТОГ_CARGO.match(с))]
    if вон:
        return вон
    всего = next(int(м.group(1)) for с in снятое["report"] if (м := _RAN.match(с)))
    упало = sum(x for _слово, x in упавшие_отчёта(снятое))
    return [(всего - упало, упало)]


# ======================================================================================================
# ФРАЗЫ
# ======================================================================================================
def _р(язык, кто, что):
    return A._реплика(язык, кто, что)


def _ф(язык, строка):
    return T._фр(язык, строка)


def к(язык, текст):
    return T.кавычки(язык, текст)


def _о(язык, фраза, вариант=0):
    """Фраза объекта у двери `toolacts.ОБЪЕКТЫ`; вариант, какого у языка нет, — каноническая."""
    о = T.ОБЪЕКТЫ[язык][фраза]
    return о[вариант] if вариант < len(о) else о[0]


def _текст(язык, текст, падеж="в"):
    """«the word "milk"» для одного слова, «the text "fresh bread"» для нескольких."""
    род = "слово" if len(текст.split()) == 1 else "текст"
    return T.ОБЪЕКТЫ[язык][род][падеж].format(w=к(язык, текст))


class Приказ(str):
    """Приказ повелительным наклонением; `.инф` — тот же приказ инфинитивом (вопросная просьба: «could you create …»,
    «ты можешь создать …», «kannst du die Datei … erstellen»); `.отмена` — приказ меняющим словом («don't …»,
    «pretend to …», `toolacts.ОТМЕНА`), где форма его знает. Склеенный с чем-либо, он — простая строка."""

    def __new__(cls, imp, инф=None, отмена=None):
        вон = str.__new__(cls, imp)
        вон.инф = инф if инф is not None else imp
        вон.отмена = отмена or {}
        return вон


def _с_отменой(язык, акт, приказ_, отчёт_, **п):
    """Приказ с формами меняющих слов «не» и «притворись» (дверь `toolacts.ОТМЕНА`) — у канонических частей акта."""
    return Приказ(приказ_, приказ_.инф, {вид: _ф(язык, T.отмена(язык, вид, акт, приказ_, приказ_.инф, отчёт_, **п))
                                        for вид in ("не", "притворись")})


def _регистр(язык, регистр, imp):
    if регистр in T.ОТМЕНА[язык]:
        return imp.отмена[регистр] + "."
    return _ф(язык, T.РЕЧЬ[язык]["регистры"][регистр].format(imp=imp, inf=getattr(imp, "инф", imp)))


def _предложение(язык, inf, zu):
    return _ф(язык, T.РЕЧЬ[язык]["предложение"].format(inf=inf, zu=zu) + ". " + T._вопрос_предложения(язык))


class _Отказ(str):
    """Итог отказа пользователем: «no confirmation — the act is not performed. <чтение «до»>»; `.хвост` — чтение «до»:
    приказ на потом (`toolacts.ПОТОМ`) меняет лишь причину."""

    def __new__(cls, язык, хвост):
        вон = str.__new__(cls, A.РЕЧЬ[язык]["отказ"] + ". " + хвост)
        вон.хвост = хвост
        return вон


def _отказ(язык, хвост):
    return _Отказ(язык, хвост)


def _мир(язык, мир_):
    """Ход мира репликой: метка у двери хода, содержимое одно на всех языках, конец — точкой."""
    return _р(язык, "мир", мир_ + ".")


def _папка(язык, N):
    return A.РЕЧЬ[язык]["папка"].format(N=N)


def _строк_в(язык, f, N):
    return T._файл_строк(язык, f, N)


def _встречается(язык, текст, М, N):
    """«the text "b" occurs 1 time in the file f» — место фразой двери (файл, папка, репозиторий)."""
    return _ф(язык, T.РЕЧЬ[язык]["встречается"].format(Wи=_текст(язык, текст, "и"), М=М, N=N))


def _в_файле(язык, f):
    return _о(язык, "в_файле").format(f=f)


# АКТ ДВЕРИ ХОДА (создать, удалить): приказ, предложение и отчёт — шаблонами `actturn`, объект — фразой формы
def _акт_хода(язык, акт, Ф_приказа, Ф, f=None):
    """(приказ, предложение, отчёт, инфинитив) акта двери хода; с путём `f` канонической формы приказ знает и формы
    меняющих слов («don't delete the file f», «nie usuwaj pliku f»)."""
    приказ_в, инф_в, отчёт_в = A.ГЛАГОЛЫ[язык][акт]
    р = A.РЕЧЬ[язык]
    приказ_ = Приказ(_ф(язык, р["приказ"].format(V=приказ_в, Ф=Ф_приказа)),
                     _ф(язык, РЕЧЬ[язык]["инф_акта"].format(V=инф_в, Ф=Ф_приказа)))
    отчёт_ = _ф(язык, р["отчёт"].format(V=отчёт_в, Ф=Ф))
    if f is not None:
        приказ_ = _с_отменой(язык, акт, приказ_, отчёт_, Ф=Ф_приказа, Фр=_о(язык, "файла").format(f=f))
    return (приказ_, _ф(язык, р["предложение"].format(V=инф_в, Ф=Ф)), отчёт_,
            _ф(язык, РЕЧЬ[язык]["инф_акта"].format(V=инф_в, Ф=Ф)))


def ф_создать(язык, форма, f=None, n=None, d=None):
    """Фраза объекта приказа «создать»: «the file x», «x», «an empty file x», «a new file x», «… in the folder d»,
    «… in the directory d»."""
    if форма == "каталог":
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "в_каталоге").format(d=d)
    if форма.startswith(("папка", "впереди")):
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "в_папке", int(форма[-1])).format(d=d)
    if форма == "голый":
        return f
    if форма == "артикль":
        return _о(язык, "файл_вин", T.неопр(язык, "файл_вин")).format(f=f)      # «a file x» (наряд (h1))
    if форма in ("пустой", "новый"):
        return РЕЧЬ[язык][форма].format(f=f)
    if форма == "назв":
        return T.НАЗВАННЫЙ[язык]["новый"].format(f=f)
    return A.РЕЧЬ[язык]["файл"].format(f=f)


def ф_удалить(язык, форма, f=None, n=None, d=None):
    if форма == "каталог":
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "из_каталога").format(d=d)
    if форма.startswith(("папка", "впереди")):
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "из_папки", int(форма[-1])).format(d=d)
    if форма == "назв":
        return T.НАЗВАННЫЙ[язык]["вин"].format(f=f)
    return f if форма == "голый" else A.РЕЧЬ[язык]["файл"].format(f=f)


def канон(форма):
    """Каноническая форма той же дыры: «голый», «пустой», «новый», «назв», «синоним» → «канон»; «папка·2» и
    «впереди·0» и «каталог» → «папка·0»."""
    return "папка·0" if форма.startswith(("папка", "впереди", "каталог")) else "канон"


def _ступени(язык, акт, канон_, форма_=None):
    """(приказ, предложение, отчёт, инфинитив плана) акта двери рук: приказ — частями формы поверх канонических,
    предложение и отчёт — каноническими частями."""
    imp, inf_формы = T._ступени(язык, акт, **{**канон_, **(форма_ or {})})[:2]
    _imp, inf, zu, past = T._ступени(язык, акт, **канон_)
    отчёт_ = _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past))
    приказ_ = _с_отменой(язык, акт, Приказ(_ф(язык, imp), _ф(язык, inf_формы)), отчёт_, **{**канон_, **(форма_ or {})})
    return приказ_, _предложение(язык, inf, zu), отчёт_, _ф(язык, inf)


# ПРАВКА СЕМЬИ ПЕРЕФРАЗА поверх канонического приказа: синоним глагола или место впереди (двери `toolacts`)
_ПРОБЕЛЫ = re.compile(r" {2,}")


def _синоним(язык, акт, форма, **п):
    """Приказ формы «синоним» — первым глаголом двери, «синоним·i» — i-м (`toolacts.СИНОНИМЫ`); «страд» —
    страдательным оборотом или долженствованием с объектом впереди (`toolacts.СТРАДАТЕЛЬНЫЙ`, наряд 28.09)."""
    if форма == "страд":
        return Приказ(_ф(язык, T.страдательный(язык, акт, **п)))
    # СОСТАВНАЯ ФОРМА (наряд 28.09): «синоним·голый» — первый синоним с объектами голым именем, как их называет форма
    # «голый» акта; первый синоним несёт и инфинитив голоса (`toolacts.СИНОНИМЫ_ИНФ`) — регистры нужды и желания его держат
    if форма == "синоним·голый":
        п = {**п, **_голые_слоты(язык, акт, п)}
        форма = "синоним"
    i = int(форма.partition("·")[2] or 0)
    if i == 0:
        return Приказ(_ф(язык, T.синоним(язык, акт, 0, **п)), _ф(язык, T.синоним_инф(язык, акт, **п)))
    return Приказ(_ф(язык, T.синоним(язык, акт, i, **п)))


def _голые_слоты(язык, акт, п):
    """Фразы объектов голым именем — те, какими их называет форма «голый» акта (дверь `toolacts.ОБЪЕКТЫ`, вариант 1)."""
    if акт in ("создать", "удалить"):
        return dict(Ф=п["f"])
    if акт == "перенести":
        return dict(Ф=_о(язык, "файл_вин", 1).format(f=п["f"]))
    if акт == "переименовать":
        return dict(Фи=_о(язык, "файл_имени", 1).format(f=п["f"]), Ф=_о(язык, "файл_вин", 1).format(f=п["f"]))
    if акт == "дописать":
        return dict(S=_о(язык, "строку", 1).format(s=п["s"]), К=_о(язык, "в_файл", 1).format(f=п["f"]))
    if акт == "замена":
        return dict(W=п["w"], М=_о(язык, "в_файле", 1).format(f=п["f"]))
    return {}


def синонимы(язык, акт):
    """Формы синонимов акта в голосе: «синоним», «синоним·1», … — по ряду двери."""
    return tuple("синоним" + (f"·{i}" if i else "") for i in range(len(T.СИНОНИМЫ[язык][акт])))


def _впереди(язык, место, без_места):
    """Приказ с местом впереди: место, знак языка, канонический приказ без места (пробелы сведены)."""
    return Приказ(_ф(язык, T.впереди(язык, место, _ПРОБЕЛЫ.sub(" ", без_места).strip())))


def варианты_переноса(язык):
    """Формы приказа переноса: каждое непустое место назначения с каноническим файлом и голое с голым файлом."""
    места = T.ОБЪЕКТЫ[язык]["в_папку"]
    return tuple(f"0·{j}" for j in range(len(места)) if j != 1) + ("1·1",)


def _части_переноса(язык, форма, f, d):
    if форма == "каталог":
        return dict(f=f, d=d), dict(Ф=_о(язык, "файл_вин").format(f=f), Д=_о(язык, "в_каталог").format(d=d))
    vф, vд = (int(x) for x in форма.split("·"))
    return dict(f=f, d=d), dict(Ф=_о(язык, "файл_вин", vф).format(f=f), Д=_о(язык, "в_папку", vд).format(d=d))


def _части_замены(язык, форма, a, b, f):
    """Слово — «the word», несколько слов — «the text»; голая форма — без «the text» и без «the file»; «назв» —
    «in the file called f»."""
    канон_ = dict(w=к(язык, a), v=к(язык, b), f=f, W=_текст(язык, a), Wнет=_текст(язык, a, "нет"))
    if форма == "голый":
        return канон_, dict(W=к(язык, a), М=_о(язык, "в_файле", 1).format(f=f))
    if форма == "назв":
        return канон_, dict(М=_о(язык, "в_файле", 2).format(f=f))
    return канон_, None


def _части_дописать(язык, форма, s, f):
    """Голая форма — без «the line» и «the file»; «назв» — «to the file called f»; «конец» — «to the end of the
    file f»."""
    канон_ = dict(s=к(язык, s), f=f)
    if форма == "голый":
        return канон_, dict(S=_о(язык, "строку", 1).format(s=к(язык, s)), К=_о(язык, "в_файл", 1).format(f=f))
    if форма == "назв":
        return канон_, dict(К=_о(язык, "в_файл", 2).format(f=f))
    if форма == "артикль":
        # «append a line "x" to the file f» — строка с неопределённым артиклем (наряд (h1))
        return канон_, dict(S=_о(язык, "строку", T.неопр(язык, "строку")).format(s=к(язык, s)))
    if форма == "конец":
        return канон_, dict(К=T.В_КОНЕЦ[язык].format(f=f))
    return канон_, None


def _тесты(язык, я):
    return dict(Т=РЕЧЬ[язык]["тесты_языка"].format(Я=я))


def исход(язык, я, снятое):
    """(числа отчёта, исход): «all 8 tests passed» / «4 tests passed, 1 failed» — числа, какие стоят в отчёте бегуна
    («Ran 8 tests», «4 passed; 1 failed»); у отчёта из нескольких строк итога — их сумма леджером: «all 6 tests passed:
    2 + 3 + 1 = 6»; исход — по коду выхода мира, фразой двери `toolacts`."""
    строки_ = строки_итога(снятое)
    прошло, упало = sum(п for п, _у in строки_), sum(у for _п, у in строки_)
    р = РЕЧЬ[язык]
    if прошло + упало == 0:
        # прогон без тестов: числа мир не пишет («Ran 0 tests … NO TESTS RAN») — фраза двери без числа
        числа = р["ни_одного"]
    elif упало == 0:
        числа = р["все_прошли"].format(N=T.тестов(язык, прошло))
    elif not any(_ИТОГ_CARGO.match(с) for с in снятое["report"]):
        # unittest пишет всё и упавшие («Ran 8 tests», «FAILED (failures=3)»): прошедших организм считает сам, вычитая
        # всякое число строки FAILED, как бегун его написал («8 − 4 − 1 = 3» у «failures=4, errors=1»), и называет
        # вычтенное словом отказа («…, 4 failed and 1 error»)
        всего = прошло + упало
        упавшие = упавшие_отчёта(снятое)
        числа = (р["из_прошли"].format(P=прошло, N=T.тестов(язык, всего),
                                       прошли=S._счёт(р["прошли"], прошло, язык) if "прошли" in р else "")
                 + A.РЕЧЬ[язык]["двоеточие"] + f"{всего} − " + " − ".join(str(x) for _слово, x in упавшие)
                 + f" = {прошло}, " + f" {р['и']} ".join(упавшие_словом(язык, слово, x) for слово, x in упавшие))
    else:
        числа = р["прошли_упали"].format(
            P=T.тестов(язык, прошло), F=упало,
            прошли=S._счёт(р["прошли"], прошло, язык) if "прошли" in р else "",
            упали=S._счёт(р["упали"], упало, язык) if "упали" in р else "")
    if len(строки_) > 1:
        числа += A.РЕЧЬ[язык]["двоеточие"] + " + ".join(str(п) for п, _у in строки_) + f" = {прошло}"
    return _ф(язык, числа), _ф(язык, T.РЕЧЬ[язык]["итог"][0 if снятое["exit"] == 0 else 1])


def _слоты_вопроса(язык, вариант, f=None, d=None, k=None, текст=None):
    """Слоты вопроса: вариант 0 — канонический, 1 — голый («F», «"x"»), «назв» — файл по имени при канонических
    прочих словах, «второй» — канонические слоты для второй формы вопроса; у папки — вариант её фразы."""
    п = {}
    файл = 2 if вариант == "назв" else вариант if isinstance(вариант, int) else 0
    # «второй·голый» — вторая форма вопроса голым файлом («where is F?», наряд (c)); прочие слова — канонические
    файл = 1 if вариант == "второй·голый" else файл
    голый = 1 if вариант == 1 else 0
    if f is not None:
        п.update(Ф=_о(язык, "файл_вин", файл).format(f=f), Фр=_о(язык, "файла", файл).format(f=f),
                 М=_о(язык, "в_файле", файл).format(f=f))
    if d is not None:
        п.update(Дв=_о(язык, "в_каталоге" if вариант == "каталог" else "в_папке", файл).format(d=d),
                 Дп=T.ПАПКА_ПОДЛ[язык].format(d=d))
    if k is not None:
        п.update(K=РЕЧЬ[язык]["ключ"][голый].format(k=k), Kо=РЕЧЬ[язык]["ключ_о"][голый].format(k=k))
    if текст is not None:
        if голый:
            п.update(W=к(язык, текст), Wи=к(язык, текст), Wнет=к(язык, текст))
        else:
            п.update(W=_текст(язык, текст), Wи=_текст(язык, текст, "и"), Wнет=_текст(язык, текст, "нет"))
    return п


def _q(язык, ключ, **п):
    return _ф(язык, РЕЧЬ[язык][ключ].format(**п))


def место(язык, текст, f, поз):
    """«the text "x" stands in line 2 of the file f»; где число встало бы перед чужим существительным («в строке 1
    файла») — файл впереди: «в файле f текст «x» стоит в строке 2»."""
    позиция = T.РЕЧЬ[язык]["позиция"][len(поз) - 1].format(Wи=_текст(язык, текст, "и"), a=поз[0], b=поз[-1])
    return _ф(язык, РЕЧЬ[язык]["место"].format(позиция=позиция, Фр=_о(язык, "файла").format(f=f), М=_в_файле(язык, f)))


def список(язык, пути):
    """«a and b», «a, b and c» — союз языка."""
    return пути[0] if len(пути) == 1 else ", ".join(пути[:-1]) + f" {РЕЧЬ[язык]['и']} " + пути[-1]


# ======================================================================================================
# СБОРКИ — части, какие меняются, приходят готовыми (дыры, ход мира строкой, счётные фразы, леджеры).
# Суд подаёт в них метки и получает рамку дома; ход мира и числа он проверяет своим пересчётом.
# ======================================================================================================
def ход(язык, регистр, приказ_, предложение_, да, мир_, итог):
    """Акт: приказ · предложение с вопросом · «да»/«нет» · ход мира · итог организма. Приказ на потом («… later»,
    регистр `toolacts.МЕНЯЮЩИЕ`; «не …», «притворись» — так же): слово меняет акт — организм его не предлагает, мир
    читает «до» (чтение отказа
    пользователем), итог называет акт инфинитивом и отказ с причиной «на потом»; с «да» (рамка суда, дом её не
    пишет) — акт вопреки слову."""
    р = A.РЕЧЬ[язык]
    if not да and регистр in T.МЕНЯЮЩИЕ[язык]:
        отказ_ = приказ_.инф + р["двоеточие"] + T.МЕНЯЮЩИЕ[язык][регистр] + " — " + T._хвост_отказа(язык)
        return " ".join((_р(язык, "польз", _регистр(язык, регистр, приказ_)), _мир(язык, мир_),
                         _р(язык, "орг", _ф(язык, отказ_) + ". " + итог.хвост)))
    return " ".join((_р(язык, "польз", _регистр(язык, регистр, приказ_)), _р(язык, "орг", предложение_),
                     _р(язык, "польз", (р["да"] if да else р["нет"]) + "."), _мир(язык, мир_), _р(язык, "орг", итог)))


def невозможный(язык, регистр, приказ_, мир_, причина):
    """Невозможный акт: приказ · отказ мира по имени · причина организма по имени."""
    return " ".join((_р(язык, "польз", _регистр(язык, регистр, приказ_)), _мир(язык, мир_),
                     _р(язык, "орг", причина + ".")))


def вопрос(язык, вопрос_, мир_, ответ):
    return " ".join((_р(язык, "польз", вопрос_), _мир(язык, мир_),
                     _р(язык, "орг", ответ if ответ.endswith(".") else ответ + ".")))


def сборка_создать(язык, род, форма, регистр, f, n, d, мир_, N=None, L=None):
    приказ_, предложение_, отчёт_, _инф = _акт_хода(язык, "создать", ф_создать(язык, форма, f, n, d),
                                                    ф_создать(язык, канон(форма), f, n, d),
                                                    f if форма == "канон" else None)
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "создать", форма, f=f)
    elif форма.startswith("впереди"):
        приказ_ = _впереди(язык, _о(язык, "в_папке", int(форма[-1])).format(d=d),
                           _акт_хода(язык, "создать", A.РЕЧЬ[язык]["файл"].format(f=n), "")[0])
    if род == СОЗДАТЬ_ЕСТЬ:
        return невозможный(язык, регистр, приказ_, мир_, A.РЕЧЬ[язык]["есть"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=f)))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N) if форма.startswith(("папка", "впереди", "каталог"))
                         else _папка(язык, N), L)
    да = род != СОЗДАТЬ_ОТКАЗ
    return ход(язык, регистр, приказ_, предложение_, да, мир_, (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост))


def сборка_удалить(язык, род, форма, регистр, f, n, d, мир_, N=None, L=None):
    приказ_, предложение_, отчёт_, _инф = _акт_хода(язык, "удалить", ф_удалить(язык, форма, f, n, d),
                                                    ф_удалить(язык, канон(форма), f, n, d),
                                                    f if форма == "канон" else None)
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "удалить", форма, f=f)
    elif форма.startswith("впереди"):
        приказ_ = _впереди(язык, _о(язык, "из_папки", int(форма[-1])).format(d=d),
                           _акт_хода(язык, "удалить", A.РЕЧЬ[язык]["файл"].format(f=n), "")[0])
    if род == УДАЛИТЬ_НЕТ:
        return невозможный(язык, регистр, приказ_, мир_,
                           A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f)))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N) if форма.startswith(("папка", "впереди", "каталог"))
                         else _папка(язык, N), L)
    да = род != УДАЛИТЬ_ОТКАЗ
    return ход(язык, регистр, приказ_, предложение_, да, мир_, (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост))


def сборка_переноса(язык, род, форма, регистр, f, d, мир_, N=None, L=None):
    части_ = _части_переноса(язык, "0·0" if форма.startswith("синоним") or форма in ("впереди", "страд") else форма,
                             f, d)
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "перенести", *части_)
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "перенести", форма, f=f, d=d)
    elif форма == "впереди":
        приказ_ = _впереди(язык, _о(язык, "в_папку").format(d=d), T._ступени(язык, "перенести", f=f, d=d, Д="")[0])
    if род == ПЕРЕНОС_НЕТ:
        return невозможный(язык, регистр, приказ_, мир_,
                           A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f)))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N), L)
    да = род != ПЕРЕНОС_ОТКАЗ
    return ход(язык, регистр, приказ_, предложение_, да, мир_, (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост))


def сборка_имени(язык, род, форма, регистр, f, g, мир_, N=None, L=None):
    приказ_, предложение_, отчёт_, _инф = _ступени(
        язык, "переименовать", dict(f=f, g=g),
        dict(Фи=_о(язык, "файл_имени", {"голый": 1, "назв": 2}.get(форма, 0)).format(f=f)))
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "переименовать", форма, f=f, g=g)
    if род in (ИМЯ_ЗАНЯТО, ИМЯ_НЕТ):
        причина = (A.РЕЧЬ[язык]["есть"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=g)) if род == ИМЯ_ЗАНЯТО
                   else A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f)))
        return невозможный(язык, регистр, приказ_, мир_, причина)
    хвост = T.наблюдение(язык, _папка(язык, N), L)
    да = род != ИМЯ_ОТКАЗ
    return ход(язык, регистр, приказ_, предложение_, да, мир_, (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост))


def сборка_замены(язык, род, форма, регистр, a, b, f, мир_, N=None, L=None):
    части_ = _части_замены(язык, форма, a, b, f)
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "замена", *части_)
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "замена", форма, **части_[0])
    elif форма == "впереди":
        приказ_ = _впереди(язык, _в_файле(язык, f), T._ступени(язык, "замена", **{**части_[0], "М": ""})[0])
    if род == ЗАМЕНА_НЕТ:
        причина = (_ф(язык, T.РЕЧЬ[язык]["нет_слова"].format(**T.слоты(язык, f=f, Wнет=_текст(язык, a, "нет"))))
                   + " — " + T._хвост_отказа(язык))
        return невозможный(язык, регистр, приказ_, мир_, причина)
    if род == ЗАМЕНА_ОТКАЗ:
        return ход(язык, регистр, приказ_, предложение_, False, мир_,
                   _отказ(язык, T.наблюдение(язык, _встречается(язык, a, _в_файле(язык, f), N), L)))
    итог = отчёт_ + ". " + T.наблюдение(язык, _встречается(язык, b, _в_файле(язык, f), N), L)
    return ход(язык, регистр, приказ_, предложение_, True, мир_, итог)


def сборка_дописать(язык, род, форма, регистр, s, f, мир_, N=None, L=None):
    части_ = _части_дописать(язык, форма, s, f)
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "дописать", *части_)
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "дописать", форма, **части_[0])
    elif форма in ("у_конца", "конец·впереди", "добавь_конец"):
        # «в конце файла» одной фразой: внутри приказа, впереди него и с синонимом «add» (дверь `toolacts.КОНЕЦ`)
        шаблон = T.КОНЕЦ[язык][{"у_конца": "у_конца", "конец·впереди": "впереди", "добавь_конец": "добавь"}[форма]]
        приказ_ = Приказ(_ф(язык, шаблон.format(S=_о(язык, "строку").format(s=к(язык, s)), f=f)))
    if форма in ("конец·голый", "добавь_конец·голый"):
        # голый файл после «to the end of» (наряд (h1), дверь `toolacts.КОНЕЦ`): «append "x" to the end of f» — глагол
        # акта и голый литерал; «add the line "x" to the end of f» — синоним «add» и строка канонически
        голый_ = форма == "конец·голый"
        шаблон = T.КОНЕЦ[язык]["у_конца_голый" if голый_ else "добавь_голый"]
        приказ_ = Приказ(_ф(язык, шаблон.format(S=_о(язык, "строку", int(голый_)).format(s=к(язык, s)), f=f)))
    хвост = T.наблюдение(язык, _строк_в(язык, f, N), L)
    да = род != ДОПИСАТЬ_ОТКАЗ
    return ход(язык, регистр, приказ_, предложение_, да, мир_, (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост))


def _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N, L):
    past = T._ступени(язык, "тесты", **_тесты(язык, я))[3]
    return (_ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past)) + ". " + ЧИСЛА + ". " + ИСХОД + ". "
            + T._запуски(язык, N, L))


def сборка_прогона(язык, род, регистр, я, мир_, ЧИСЛА=None, ИСХОД=None, N=None, L=None, форма="язык"):
    imp, inf, zu, past = T._ступени(язык, "тесты", **_тесты(язык, я))
    приказ_, предложение_ = Приказ(_ф(язык, imp), _ф(язык, inf)), _предложение(язык, inf, zu)
    приказ_ = _с_отменой(язык, "тесты", приказ_, _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past)),
                         Я=я, **_тесты(язык, я))
    if форма.startswith("синоним") or форма == "страд":
        приказ_ = _синоним(язык, "тесты", форма, Я=я, **_тесты(язык, я))
    if род == ТЕСТЫ_ОТКАЗ:
        return ход(язык, регистр, приказ_, предложение_, False, мир_, _отказ(язык, T._запуски(язык, N, L)))
    return ход(язык, регистр, приказ_, предложение_, True, мир_, _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N, L))


# ПЛАН ИЗ ДВУХ АКТОВ: приказ и предложение — связкой `toolacts.связать`; после «да» — ход мира и итог каждого акта
def _план(язык, A_, B_):
    приказ_ = _ф(язык, T.связать(язык, "приказ", A_[0], B_[0]))
    предложение_ = _ф(язык, T.связать(язык, "предложение", A_[1], B_[1])) + ". " + T._вопрос_предложения(язык)
    return приказ_, предложение_


# СОЮЗ «AND» МЕЖДУ ДВУМЯ АКТАМИ (27.09, слово ведущего omega-90 к наряду (f)): приказ плана из двух актов союзом —
# «create the file F and add "x" as its only line», «replace … and run the Rust tests»: связка приказа канонического
# шаблона (`toolacts.СВЯЗКА`) → связка «и» двери `toolacts.СВЯЗКА_ВОПРОСА` (у нидерландского «en … daarna» уходит
# «daarna»); предложение организма, ходы мира и итоги — те же, что у канонической страницы.
# СЧЁТ СВЯЗКИ: ядро покупает одну связку на голос (свидетелей больше двух соперниц); в худшем счёте всякий новый «and» —
# соперница связки плана, и страниц с «and» на голос — 16: «найди и скажи» 4, «as its only line» союзом 4 и две пары
# актов `СОЮЗОМ` по 4 — заменить в коде и прогнать, перенести и удалить. Страницы союзом — лишь там, где «и» голоса — не
# связка его канонического плана: у нидерландского «{A} en {B1} daarna {B2}» союз «en» и есть связка плана, и новые
# «en» спорили бы с единственной купленной связкой голоса («as its only line» у него — одной формой «en … daarna»)
СОЮЗОМ = ((ПЛАН_ЗАМЕНА, "код"), (ПЛАН_ПЕРЕНОС, "перенос"))
# СОЮЗОМ ШИРЕ (28.09, заказ руки joins2, к М-2090): свидетели союза — разные пары актов. Пары рода ДВА_АКТА, план «…,
# then let me know how many lines it has» после переименования и переноса и план «…, then tell me what its first line
# is» после дописывания (зачин вида 1) — на тех же четырёх основах. Страниц с «and» на голос — 48 (было 16); новых
# страниц плана связкой голоса — 40 (20 канонических и 20 вежливых)
СОЮЗОМ += ((МЕСТО_СТРОК, "имя"), (МЕСТО_СТРОК, "перенос"), (ПЛАН_СКАЖИ, "дописать·первая·1"),
           *((ДВА_АКТА, пара) for пара in ПАРЫ_АКТОВ))


def _союз(язык):
    """(связка канонического шаблона плана, связка «и» голоса) — часть шаблона между {A} и {B1}."""
    return tuple(re.split(r"\{A\}|\{B1\}", шаблон)[1] for шаблон in (T.СВЯЗКА[язык][0], T.СВЯЗКА_ВОПРОСА[язык][0]))


def союз_иной(язык):
    """«И» голоса — иное слово, чем связка его канонического плана: союзу есть что сменить."""
    тогда_, и_ = _союз(язык)
    return тогда_ != и_


def союзом(язык, стр):
    """Страница плана из двух актов союзом «and»: в первой реплике пользователя связка канонического шаблона сменяется
    связкой «и» (перед той же гласной — благозвучная форма союза, `toolacts.СОЮЗ_ЕВФОНИЯ`); прочее страницы то же."""
    метка = A._реплика(язык, "польз", "")
    приказ_ = реплики(стр, язык)[0][1]
    тогда_, и_ = _союз(язык)
    первый, _, хвост = приказ_.partition(тогда_)
    assert стр.startswith(метка + приказ_) and тогда_ != и_ and хвост and тогда_ not in хвост, стр[:120]
    союз_, перед_гласной = T.СОЮЗ_ЕВФОНИЯ.get(язык, (None, None))
    if и_.strip() == союз_ and хвост.startswith(союз_[-1]):
        и_ = и_.replace(союз_, перед_гласной)
    return метка + первый + и_ + хвост + стр[len(метка + приказ_):]


def вежливо(язык, стр):
    """Страница вежливой просьбой: первая реплика пользователя — приказ плана целиком — в шаблоне регистра «вежливый»
    двери (`toolacts.РЕЧЬ[…]["регистры"]`); шаблон лишь прибавляет слова, прочее страницы то же — пара одного акта мира
    «одна форма = другая минус слова»."""
    метка = A._реплика(язык, "польз", "")
    приказ_ = реплики(стр, язык)[0][1]
    assert стр.startswith(метка + приказ_) and приказ_.endswith("."), стр[:120]
    return метка + _регистр(язык, "вежливый", приказ_[:-1]) + стр[len(метка + приказ_):]


def _приказ_правкой(язык, стр, правка):
    """Страница, где первая реплика пользователя сказана правкой `правка` (язык, текст → текст); прочее страницы то
    же — пара одного хода мира."""
    метка = A._реплика(язык, "польз", "")
    приказ_ = реплики(стр, язык)[0][1]
    правлено = правка(язык, приказ_)
    assert стр.startswith(метка + приказ_) and правлено != приказ_, стр[:120]
    return метка + правлено + стр[len(метка + приказ_):]


def сокращённо(язык, стр):
    """Страница, где пользователь говорит сокращением голоса (`toolacts.СОКРАЩЕНИЯ`): «what's the first line of the file
    F?» вместо «what is …» — пара «полная форма / сокращение» одного хода мира; речь организма — каноническая."""
    return _приказ_правкой(язык, стр, T.сократить)


def в_бэктиках(язык, стр):
    """Страница, где пользователь пишет литерал в обёртке программиста (`toolacts.ЛИТЕРАЛ`): «replace `x` with `y` in
    F» вместо кавычек голоса — пара: та же страница в кавычках голоса; речь организма и ход мира — те же."""
    return _приказ_правкой(язык, стр, T.в_литерале)


def _план_ход(язык, приказ_, предложение_, да, ходы):
    """Приказ · предложение · слово · (ход мира · итог) на каждый акт — или ход чтения и отказ на «нет»."""
    р = A.РЕЧЬ[язык]
    части = [_р(язык, "польз", приказ_ + "."), _р(язык, "орг", предложение_),
             _р(язык, "польз", (р["да"] if да else р["нет"]) + ".")]
    for мир_, итог in ходы:
        части += [_мир(язык, мир_), _р(язык, "орг", итог)]
    return " ".join(части)


def сборка_плана_замены(язык, род, a, b, f, я, мир1, N1, L1, мир2=None, ЧИСЛА=None, ИСХОД=None, N=None, L=None):
    приказ_з, _пр, отчёт_з, инф_з = _ступени(язык, "замена", *_части_замены(язык, "текст", a, b, f))
    imp_т, inf_т, _zu, _past = T._ступени(язык, "тесты", **_тесты(язык, я))
    приказ_, предложение_ = _план(язык, (приказ_з, инф_з), (_ф(язык, imp_т), _ф(язык, inf_т)))
    if род == ПЛАН_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False,
                         [(мир1, _отказ(язык, T.наблюдение(язык, _встречается(язык, a, _в_файле(язык, f), N1), L1)))])
    итог1 = отчёт_з + ". " + T.наблюдение(язык, _встречается(язык, b, _в_файле(язык, f), N1), L1)
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, итог1), (мир2, _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N, L))])


def сборка_плана_дописать(язык, род, s, f, я, мир1, N1, L1, мир2=None, ЧИСЛА=None, ИСХОД=None, N=None, L=None):
    приказ_д, _пр, отчёт_д, инф_д = _ступени(язык, "дописать", *_части_дописать(язык, "канон", s, f))
    imp_т, inf_т, _zu, _past = T._ступени(язык, "тесты", **_тесты(язык, я))
    приказ_, предложение_ = _план(язык, (приказ_д, инф_д), (_ф(язык, imp_т), _ф(язык, inf_т)))
    строки_ = T.наблюдение(язык, _строк_в(язык, f, N1), L1)
    if род == ПЛАН_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False, [(мир1, _отказ(язык, строки_))])
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_д + ". " + строки_), (мир2, _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N, L))])


def сборка_плана_переноса(язык, род, f, d, q, мир1, N1, L1, мир2=None, N2=None, L2=None):
    приказ_п, _пр, отчёт_п, инф_п = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", f, d))
    приказ_у, _пу, отчёт_у, инф_у = _акт_хода(язык, "удалить", A.РЕЧЬ[язык]["файл"].format(f=q),
                                               A.РЕЧЬ[язык]["файл"].format(f=q))
    приказ_, предложение_ = _план(язык, (приказ_п, инф_п), (приказ_у, инф_у))
    папка_ = T.наблюдение(язык, T.папка_с_именем(язык, d, N1), L1)
    if род == ПЛАН_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False, [(мир1, _отказ(язык, папка_))])
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_п + ". " + папка_), (мир2, отчёт_у + ". " + T.наблюдение(язык, _папка(язык, N2), L2))])


# ПЛАН С МЕСТОИМЕНИЕМ (ведущий, 25.09): приказ называет объект второго акта местоимением («… then append the line
# "x" to it»); предложение называет путь, какой определяет сам приказ — создание: созданный файл, переименование:
# новое имя в той же папке, перенос: папка/имя; итог после акта — путь из строки path хода мира (`p`), и мир ходит
# после каждого акта. Первый акт невозможен — мир отказывает по имени, итог называет его отказ, второй акт не идёт.
def _причина_мира(язык, почему, что):
    """Отказ мира по имени словами организма: «the file x is already there», «the file x is not there»."""
    р = A.РЕЧЬ[язык]
    if почему == "already-there":
        return р["есть"].format(Ф=р["файл"].format(f=что))
    return р["пуст"].format(НФ=р["нет_файла"].format(f=что))


def _место_невозможный(язык, приказ_, мир_, почему, что):
    return невозможный(язык, "плоский", приказ_, мир_,
                       _причина_мира(язык, почему, что) + ". " + T.МЕСТОИМЕНИЕ[язык]["нет_второго"])


def _второй_приказ(язык, акт, ссылка=None, **п):
    """Второй приказ плана: местоимением («append … to it») или ссылкой без местоимения («… to this file», «… to the
    same file» — правка той же пары актов)."""
    return T.ссылка(язык, ссылка, акт, **п) if ссылка else T.местоимение(язык, акт, **п)


def _дописать_в_него(язык, s, p, ссылка=None):
    """(второй приказ местоимением или ссылкой, инфинитив с путём, отчёт с путём) дописывания строки."""
    _пр, _пп, отчёт_, инф_ = _ступени(язык, "дописать", *_части_дописать(язык, "канон", s, p))
    return _второй_приказ(язык, "дописать", ссылка, s=к(язык, s)), инф_, отчёт_


def _строки_после(язык, p, N, L):
    return T.наблюдение(язык, _строк_в(язык, p, N), L)


def сборка_места_создать(язык, род, f, s, мир1, N1=None, L1=None, мир2=None, N2=None, L2=None, почему=None, p=None,
                         ссылка=None):
    Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
    приказ_с, _пс, отчёт_с, инф_с = _акт_хода(язык, "создать", Ф, Ф)
    местоимение_, инф_д, отчёт_д = _дописать_в_него(язык, s, f, ссылка)
    приказ_, предложение_ = _план(язык, (приказ_с, инф_с), (местоимение_, инф_д))
    if род == МЕСТО_НЕВОЗМОЖНО:
        return _место_невозможный(язык, приказ_, мир1, почему, p)
    папка_ = T.наблюдение(язык, _папка(язык, N1), L1)
    if род == МЕСТО_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False, [(мир1, _отказ(язык, папка_))])
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_с + ". " + папка_), (мир2, отчёт_д + ". " + _строки_после(язык, f, N2, L2))])


def сборка_места_имени(язык, род, f, g, p, s, мир1, N1=None, L1=None, мир2=None, N2=None, L2=None, почему=None,
                       ссылка=None):
    приказ_и, _пи, отчёт_и, инф_и = _ступени(язык, "переименовать", dict(f=f, g=g))
    местоимение_, инф_д, отчёт_д = _дописать_в_него(язык, s, p, ссылка)
    приказ_, предложение_ = _план(язык, (приказ_и, инф_и), (местоимение_, инф_д))
    if род == МЕСТО_НЕВОЗМОЖНО:
        return _место_невозможный(язык, приказ_, мир1, почему, p)
    папка_ = T.наблюдение(язык, _папка(язык, N1), L1)
    if род == МЕСТО_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False, [(мир1, _отказ(язык, папка_))])
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_и + ". " + папка_), (мир2, отчёт_д + ". " + _строки_после(язык, p, N2, L2))])


def сборка_места_переноса(язык, род, f, d, p, мир1, N1=None, L1=None, мир2=None, N2=None, L2=None, почему=None,
                          ссылка=None):
    приказ_п, _пп, отчёт_п, инф_п = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", f, d))
    Ф = A.РЕЧЬ[язык]["файл"].format(f=p)
    _пу, _ппу, отчёт_у, инф_у = _акт_хода(язык, "удалить", Ф, Ф)
    приказ_, предложение_ = _план(язык, (приказ_п, инф_п), (_второй_приказ(язык, "удалить", ссылка), инф_у))
    if род == МЕСТО_НЕВОЗМОЖНО:
        return _место_невозможный(язык, приказ_, мир1, почему, p)
    папка_ = T.наблюдение(язык, T.папка_с_именем(язык, d, N1), L1)
    if род == МЕСТО_ОТКАЗ:
        return _план_ход(язык, приказ_, предложение_, False, [(мир1, _отказ(язык, папка_))])
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_п + ". " + папка_), (мир2, отчёт_у + ". " + T.наблюдение(язык, _папка(язык, N2), L2))])


def сборка_места_найти(язык, род, w, s, мир1, f=None, поз=None, пути=None, мир2=None, N2=None, L2=None,
                       второй="дописать"):
    """Находка файла со словом, затем дописать в него (или сказать, сколько в нём строк — `второй="строк"`):
    предложение предлагает лишь находку и говорит, что второй акт ждёт одного места; мир назвал одно — второй акт идёт
    туда; несколько — ответ всеми путями и отказ по имени."""
    imp_н, inf_н, zu_н = T.найти(язык, w=к(язык, w))
    if второй == "строк":
        местоимение_, отчёт_д = T.МЕСТОИМЕНИЕ[язык]["строк"][0], None
    else:
        местоимение_, _инф_д, отчёт_д = _дописать_в_него(язык, s, f)
    м = T.МЕСТОИМЕНИЕ[язык]
    приказ_ = _ф(язык, T.связать(язык, "приказ", imp_н, местоимение_))
    предложение_ = _ф(язык, T.РЕЧЬ[язык]["предложение"].format(inf=inf_н, zu=zu_н) + " — " + м["ждёт"] + ". "
                      + T._вопрос_предложения(язык))
    if род == МЕСТО_МНОГО:
        ответ = _q(язык, "в_файлах", С=список(язык, пути), **_слоты_вопроса(язык, 0, текст=w))
        return _план_ход(язык, приказ_, предложение_, True,
                         [(мир1, ответ + ". " + _ф(язык, м["ждёт"] + " — " + T._хвост_отказа(язык)) + ".")])
    строки_ = _строки_после(язык, f, N2, L2)
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, место(язык, w, f, поз) + "."), (мир2, строки_ if отчёт_д is None else отчёт_д + ". " + строки_)])


def сборка_места_строк(язык, план, f, x, p, s, мир1, N1=None, L1=None, мир2=None, N2=None, L2=None, ссылка=None):
    """План: акт над файлом, затем вопрос о несомом месте — «…, then tell me how many lines it has». Предложение
    называет путь, какой определяет приказ (`p`); мир ходит дважды — акт и чтение строк на месте из строки path;
    второй итог — ответ «сколько строк» каноническими словами. Первый акт: переименование, перенос, дописывание."""
    приказ_а, отчёт_а, инф_а, хвост_ = _первый_акт(язык, план, f, s if план == "дописать" else x, N1, L1)
    местоимение_, инф_строк = T.МЕСТОИМЕНИЕ[язык]["строк"]
    if ссылка:
        местоимение_ = T.ССЫЛКА[язык][ссылка]["строк"]
    приказ_, предложение_ = _план(язык, (приказ_а, инф_а), (местоимение_, _ф(язык, инф_строк.format(p=p))))
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_а + ". " + хвост_), (мир2, _строки_после(язык, p, N2, L2))])


def сборка_плана_скажи(язык, план, вопрос_, вид, f, x, p, мир1, N1, L1, мир2, T_=None, w=None, поз=None):
    """План: акт над файлом (переименовать, перенести, дописать — `x`: новое имя, папка, строка), затем зачин просьбы
    сказать вида `вид` и вопрос: «первая» — какая первая строка файла там, куда его положил акт («…, then tell me what
    its first line is»); «файл» — в каком файле слово `w` («…, then let me know which file contains the word "x"»).
    Предложение называет путь, какой определяет приказ (`p`), и слово вопроса; мир ходит дважды — акт и чтение (строки
    на месте из строки path; находка слова во всём репозитории после акта); второй итог — ответ словами вопроса дома:
    текст первой строки хода (`T_`) или путь и строки находки (`поз`)."""
    приказ_а, отчёт_а, инф_а, хвост_ = _первый_акт(язык, план, f, x, N1, L1)
    с = _слоты_вопроса(язык, 0, текст=w) if w is not None else {}
    инф_второго = _ф(язык, T.ВОПРОС_ВТОРОЙ[язык][вопрос_][1].format(p=p, **с))
    приказ_, предложение_ = _план(язык, (приказ_а, инф_а), (T.второй_вопрос(язык, вопрос_, вид, **с), инф_второго))
    if вопрос_ == "первая":
        ответ = _q(язык, "a_выбор", c=РЕЧЬ[язык]["выбор"][0], T=к(язык, T_), **_слоты_вопроса(язык, 0, f=p))
    else:
        ответ = место(язык, w, p, поз)
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_а + ". " + хвост_), (мир2, ответ if ответ.endswith(".") else ответ + ".")])


def сборка_двух_актов(язык, пара, f, x, q, y, мир1, N1, L1, мир2, N2, L2):
    """План из двух разных актов (`ПАРЫ_АКТОВ`): первый над файлом `f` (довод `x` — папка, новое имя, строка, пара
    текстов), второй над другим файлом `q` (довод `y`); приказ и предложение — связкой плана, после «да» — ход мира и
    итог каждого акта, как у акта плана того же рода (`_первый_акт`)."""
    первый, второй = пара.split("+")
    приказ_1, отчёт_1, инф_1, хвост_1 = _первый_акт(язык, первый, f, x, N1, L1)
    приказ_2, отчёт_2, инф_2, хвост_2 = _первый_акт(язык, второй, q, y, N2, L2)
    приказ_, предложение_ = _план(язык, (приказ_1, инф_1), (приказ_2, инф_2))
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_1 + ". " + хвост_1), (мир2, отчёт_2 + ". " + хвост_2)])


# ======================================================================================================
# РОДЫ ЖИВЫХ ПРОСЬБ (третий заказ ведущего, 26.09): план из трёх актов, условный приказ на ходе мира, «все файлы,
# кроме …», два объекта в одном приказе. Мир ходит после каждого акта; числа итога — клетки хода.
# ======================================================================================================
def _слитно(гл_ост):
    """(глагол, остаток) приказа одной строкой: «delete it», «supprime-le»."""
    return " ".join(x for x in гл_ост if x)


def _первый_акт(язык, вариант, f, x, N1, L1):
    """(приказ, отчёт, инфинитив, хвост итога) акта плана: создать, удалить, переименовать, перенести, дописать (`x` —
    строка), заменить (`x` — пара текстов)."""
    if вариант == "создать":
        Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
        приказ_, _п, отчёт_, инф_ = _акт_хода(язык, "создать", Ф, Ф)
        return приказ_, отчёт_, инф_, T.наблюдение(язык, _папка(язык, N1), L1)
    if вариант == "имя":
        приказ_, _п, отчёт_, инф_ = _ступени(язык, "переименовать", dict(f=f, g=x))
        return приказ_, отчёт_, инф_, T.наблюдение(язык, _папка(язык, N1), L1)
    if вариант == "перенос":
        приказ_, _п, отчёт_, инф_ = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", f, x))
        return приказ_, отчёт_, инф_, T.наблюдение(язык, T.папка_с_именем(язык, x, N1), L1)
    if вариант == "дописать":
        приказ_, _п, отчёт_, инф_ = _ступени(язык, "дописать", *_части_дописать(язык, "канон", x, f))
        return приказ_, отчёт_, инф_, _строки_после(язык, f, N1, L1)
    if вариант == "удалить":
        Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
        приказ_, _п, отчёт_, инф_ = _акт_хода(язык, "удалить", Ф, Ф)
        return приказ_, отчёт_, инф_, T.наблюдение(язык, _папка(язык, N1), L1)
    a, b = x
    приказ_, _п, отчёт_, инф_ = _ступени(язык, "замена", *_части_замены(язык, "текст", a, b, f))
    return приказ_, отчёт_, инф_, T.наблюдение(язык, _встречается(язык, b, _в_файле(язык, f), N1), L1)


def сборка_трёх(язык, вариант, f, x, p, s, мир1, N1, L1, мир2, N2, L2, мир3, N3=None, L3=None, я=None, ЧИСЛА=None,
                ИСХОД=None):
    """План из трёх актов: первый акт над файлом; второй дописывает строку туда, куда первый положил объект («it» —
    путь из строки path хода мира); третий — вопрос «сколько строк» о том же месте или прогон тестов. Предложение
    называет путь, какой определяет приказ; мир ходит после каждого акта."""
    приказ_а, отчёт_а, инф_а, хвост_ = _первый_акт(язык, вариант, f, x, N1, L1)
    местоимение_, инф_д, отчёт_д = _дописать_в_него(язык, s, p)
    if вариант == "замена":
        imp_т, inf_т, _zu, _past = T._ступени(язык, "тесты", **_тесты(язык, я))
        третий_, инф_третьего = _ф(язык, imp_т), _ф(язык, inf_т)
        итог3 = _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N3, L3)
    else:
        третий_, инф_строк = T.МЕСТОИМЕНИЕ[язык]["строк"]
        инф_третьего, итог3 = _ф(язык, инф_строк.format(p=p)), _строки_после(язык, p, N3, L3)
    приказ_ = _ф(язык, T.связать3(язык, "приказ", приказ_а, местоимение_, третий_))
    предложение_ = (_ф(язык, T.связать3(язык, "предложение", инф_а, инф_д, инф_третьего)) + ". "
                    + T._вопрос_предложения(язык))
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, отчёт_а + ". " + хвост_), (мир2, отчёт_д + ". " + _строки_после(язык, p, N2, L2)),
                      (мир3, итог3)])


def _условие_приказ(язык, род, форма, f, s=None, a=None, b=None):
    """(приказ, предложение) условного приказа: условие впереди («если») или хвостом после приказа («после»);
    предложение — ветка «да» инфинитивом с хвостом условия и ветка «иначе», где она есть."""
    у, р = T.УСЛОВИЕ[язык], РЕЧЬ[язык]
    Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
    if род == УСЛОВИЕ_ЗАМЕНА:
        imp, inf, zu, _past = T._ступени(язык, "замена", **_части_замены(язык, "текст", a, b, f)[0])
        условие_ = у["содержит_если"].format(f=f, W=_текст(язык, a), Wи=_текст(язык, a, "и"))
        тогда_, после_ = _слитно(T.местоимение(язык, "заменить", v=к(язык, b))), у["после_текст"]
    elif род == УСЛОВИЕ_ДОПИСАТЬ:
        imp, inf, zu, _past = T._ступени(язык, "дописать", s=к(язык, s), f=f)
        условие_, после_ = у["есть_если"].format(f=f), у["после"]
        тогда_ = _слитно(T.местоимение(язык, "дописать", s=к(язык, s)))
    else:
        приказ_в, инф_в, _отчёт_в = A.ГЛАГОЛЫ[язык]["удалить"]
        imp = A.РЕЧЬ[язык]["приказ"].format(V=приказ_в, Ф=Ф)
        inf, zu = р["инф_акта"].format(V=инф_в, Ф=Ф), р["zu_акта"].format(V=инф_в, Ф=Ф)
        условие_, тогда_, после_ = у["есть_если"].format(f=f), _слитно(T.местоимение(язык, "удалить")), у["после"]
    иначе_ = иначе_пр = ""
    if род == УСЛОВИЕ_ДОПИСАТЬ:
        _пв, инф_с, _ов = A.ГЛАГОЛЫ[язык]["создать"]
        иначе_ = у["иначе"].format(И=_слитно(T.местоимение(язык, "создать")))
        иначе_пр = у["иначе_пр"].format(inf=р["инф_акта"].format(V=инф_с, Ф=Ф), zu=р["zu_акта"].format(V=инф_с, Ф=Ф))
    приказ_ = (imp + после_ if форма.startswith("после") else у["если"].format(У=условие_, Т=тогда_)) + иначе_
    предложение_ = (T.РЕЧЬ[язык]["предложение"].format(inf=inf + после_, zu=zu + после_) + иначе_пр + ". "
                    + T._вопрос_предложения(язык))
    return _ф(язык, приказ_), _ф(язык, предложение_)


def сборка_условия(язык, род, форма, f, мир1, мир2=None, N=None, L=None, s=None, a=None, b=None):
    """Условный приказ на ходе мира: мир проверяет условие — чтение файла (read) или находка текста (find), итог
    проверки называет её исход; ветка «да» (и «иначе», где она есть) — акт вторым ходом мира и его итог; ветка без
    акта — условие не выполнено, акт не совершён. Ветка страницы — после «|» формы: её показал мир."""
    у = T.УСЛОВИЕ[язык]
    приказ_, предложение_ = _условие_приказ(язык, род, форма, f, s, a, b)
    if "·сокр" in форма:
        # СОКРАЩЕНИЕ ГОЛОСА (наряд (g)): хвост условия «… if it's there»; предложение организма — каноническое
        приказ_, полный_ = T.сократить(язык, приказ_), приказ_
        assert приказ_ != полный_, полный_
    да = форма.endswith("|да")
    if род == УСЛОВИЕ_ЗАМЕНА:
        проверка_ = (у["содержит"].format(f=f, W=_текст(язык, a), Wи=_текст(язык, a, "и")) if да
                     else T.РЕЧЬ[язык]["нет_слова"].format(**T.слоты(язык, f=f, Wнет=_текст(язык, a, "нет"))))
    else:
        проверка_ = у["есть" if да else "нет"].format(f=f)
    if not да and род != УСЛОВИЕ_ДОПИСАТЬ:
        return _план_ход(язык, приказ_, предложение_, True,
                         [(мир1, _ф(язык, проверка_ + " — " + T.не_выполнено(язык)) + ".")])
    Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
    if род == УСЛОВИЕ_ЗАМЕНА:
        отчёт_ = _ступени(язык, "замена", *_части_замены(язык, "текст", a, b, f))[2]
        итог = отчёт_ + ". " + T.наблюдение(язык, _встречается(язык, b, _в_файле(язык, f), N), L)
    elif род == УСЛОВИЕ_УДАЛИТЬ:
        итог = _акт_хода(язык, "удалить", Ф, Ф)[2] + ". " + T.наблюдение(язык, _папка(язык, N), L)
    elif да:
        отчёт_ = _ступени(язык, "дописать", *_части_дописать(язык, "канон", s, f))[2]
        итог = отчёт_ + ". " + T.наблюдение(язык, _строк_в(язык, f, N), L)
    else:
        итог = _акт_хода(язык, "создать", Ф, Ф)[2] + ". " + T.наблюдение(язык, _папка(язык, N), L)
    return _план_ход(язык, приказ_, предложение_, True, [(мир1, _ф(язык, проверка_) + "."), (мир2, итог)])


def сборка_кроме(язык, акт, форма, d, n, e, мир1, записи, акты):
    """«Все файлы папки, кроме n»: мир читает папку (list), итог называет её записи; затем акт идёт на всякий файл
    папки, кроме названного, и итог каждого акта — клетки его хода. `акты` — [(ход мира, путь, счётная фраза,
    леджер)]; правка «не трогай» — тот же приказ отрицанием."""
    к_ = T.КРОМЕ[язык][акт]
    п = dict(d=d, n=n, e=e)
    приказ_ = _ф(язык, к_["не_трогай" if форма == "не_трогай" else "imp"].format(**п))
    предложение_ = _ф(язык, T.РЕЧЬ[язык]["предложение"].format(inf=к_["inf"].format(**п),
                                                                zu=к_.get("zu", к_["inf"]).format(**п))
                      + ". " + T._вопрос_предложения(язык))
    ходы = [(мир1, _ф(язык, T.ОБЪЕКТЫ[язык]["папка_имя"].format(d=d, N=список(язык, записи))) + ".")]
    for мир_, путь, N, L in акты:
        if акт == "удалить":
            Ф = A.РЕЧЬ[язык]["файл"].format(f=путь)
            итог = _акт_хода(язык, "удалить", Ф, Ф)[2] + ". " + T.наблюдение(язык, T.папка_с_именем(язык, d, N), L)
        else:
            отчёт_ = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", путь, e))[2]
            итог = отчёт_ + ". " + T.наблюдение(язык, T.папка_с_именем(язык, e, N), L)
        ходы.append((мир_, итог))
    return _план_ход(язык, приказ_, предложение_, True, ходы)


def _акт_объекта(язык, акт, f, d=None, s=None):
    """(приказ, отчёт, инфинитив) акта над одним файлом — шаг плана и половина приказа о двух объектах."""
    if акт in ("создать", "удалить"):
        Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
        приказ_, _п, отчёт_, инф_ = _акт_хода(язык, акт, Ф, Ф)
    elif акт == "перенести":
        приказ_, _п, отчёт_, инф_ = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", f, d))
    else:
        приказ_, _п, отчёт_, инф_ = _ступени(язык, "дописать", *_части_дописать(язык, "канон", s, f))
    return приказ_, отчёт_, инф_


def _хвост_объекта(язык, акт, f, d, N, L):
    if акт == "перенести":
        return T.наблюдение(язык, T.папка_с_именем(язык, d, N), L)
    if акт == "дописать":
        return T.наблюдение(язык, _строк_в(язык, f, N), L)
    return T.наблюдение(язык, _папка(язык, N), L)


def сборка_двух(язык, акт, форма, f, q, мир1, N1, L1, мир2, N2, L2, d=None, s=None):
    """Два объекта: «delete the files f and q» (форма «и») — правка плана «delete the file f, then delete the file q»
    (форма «план»): предложение одно — два акта по очереди; мир ходит на каждый объект, итог — клетки хода."""
    (п1, о1, и1), (п2, о2, и2) = (_акт_объекта(язык, акт, x, d, s) for x in (f, q))
    приказ_, предложение_ = _план(язык, (п1, и1), (п2, и2))
    if форма == "и":
        оба = список(язык, [f, q])
        if акт in ("создать", "удалить"):
            приказ_ = _акт_хода(язык, акт, T.ОБЪЕКТЫ[язык]["файлы_вин"].format(С=оба), "")[0]
        elif акт == "перенести":
            приказ_ = _ступени(язык, "перенести", dict(f=f, d=d), dict(Ф=T.ОБЪЕКТЫ[язык]["файлы_вин"].format(С=оба)))[0]
        else:
            приказ_ = _ступени(язык, "дописать", dict(s=к(язык, s), f=f),
                               dict(К=T.ОБЪЕКТЫ[язык]["в_файлы"].format(С=оба)))[0]
        приказ_ = _ф(язык, приказ_)
    return _план_ход(язык, приказ_, предложение_, True,
                     [(мир1, о1 + ". " + _хвост_объекта(язык, акт, f, d, N1, L1)),
                      (мир2, о2 + ". " + _хвост_объекта(язык, акт, q, d, N2, L2))])


def сборка_тестов_сколько(язык, род, я, мир_, ЧИСЛА=None, ИСХОД=None, N=None, L=None, форма="язык"):
    """Вопрос «сколько тестов проходит» (ответ берёт прогон: предложение — прогнать тесты) и план «прогони тесты, затем
    скажи, сколько прошло»: после «да» — ход мира-процесса, итог прогона называет числа отчёта бегуна — сколько прошло.
    Формы плана: «язык» — «…, then let me know how many passed»; «зачин·1» — зачин вида 1 («…, then tell me how many
    passed»); «связка·и» — «… and let me know how many of them passed»; «связка·прямо» — «…; how many of them
    passed?». Предложение организма у всех форм одно — каноническое."""
    imp, inf, zu, _past = T._ступени(язык, "тесты", **_тесты(язык, я))
    if род == ТЕСТЫ_СКОЛЬКО:
        приказ_ = _q(язык, "q_тесты", Я=я, **_тесты(язык, я))
        предложение_ = _предложение(язык, inf, zu)
    else:
        прошло_, инф_прошло = T.МЕСТОИМЕНИЕ[язык]["прошло"]
        приказ_, предложение_ = _план(язык, (_ф(язык, imp), _ф(язык, inf)), (прошло_, _ф(язык, инф_прошло)))
        if форма == "зачин·1":
            приказ_ = _ф(язык, T.связать(язык, "приказ", _ф(язык, imp), T.второй_вопрос(язык, "прошло", 1)))
        elif форма.startswith("связка·"):
            связка = форма.split("·")[1]
            их, прямо_ = T.ВОПРОС_ВТОРОЙ[язык]["их"]
            приказ_ = _ф(язык, T.связать_вопрос(язык, связка, _ф(язык, imp),
                                                 T.зачин(язык, 0, их) if связка == "и" else прямо_))
        приказ_ += "" if приказ_.endswith("?") else "."
    р = A.РЕЧЬ[язык]
    return " ".join((_р(язык, "польз", приказ_), _р(язык, "орг", предложение_), _р(язык, "польз", р["да"] + "."),
                     _мир(язык, мир_), _р(язык, "орг", _итог_прогона(язык, я, ЧИСЛА, ИСХОД, N, L))))


def сборка_прошлого(язык, форма, f, мир_):
    """Вопрос о прошлом акте — «did you delete the file F?»: мир читает файл, акт удаления не идёт; ответ — чтение:
    «the file F exists — it is not deleted» (форма «есть») или «the file F does not exist» («нет»)."""
    _imp, inf, past = A.ГЛАГОЛЫ[язык]["удалить"]
    п = T.ПРОШЛОЕ[язык]
    вопрос_ = _ф(язык, п["вопрос"].format(inf=inf, past=past, Ф=A.РЕЧЬ[язык]["файл"].format(f=f)))
    у = T.УСЛОВИЕ[язык]
    ответ = у["есть"].format(f=f) + " — " + п["не_сделан"].format(past=past) if форма == "есть" else у["нет"].format(f=f)
    return вопрос(язык, вопрос_, мир_, _ф(язык, ответ))


# ЗАЧИН ПЕРЕД ОДИНОЧНЫМ ВОПРОСОМ (27.09, наряд ведущего (e)): вопрос формы «зачин·i» — зачин i-го вида голоса
# (`toolacts.ЗАЧИН`) и косвенный вопрос рода (`toolacts.ВОПРОС_ВТОРОЙ`): «tell me which file contains the word "x"»,
# «скажи, сколько строк в файле F», «sag mir, wie oft das Wort „x“ im Ordner D vorkommt»; ход мира и ответ — те же, что
# у прямого вопроса. Список файлов находки вопрос за зачином спрашивает, как и прямой, одним файлом
КОСВЕННЫЙ = {В_КАКОМ: "файл", В_КАКИХ: "файл", НИГДЕ: "файл", НА_СТРОКЕ: "строка", ВЫБОР: "выбор",
             СТРОКА_Н: "строка_н", КЛЮЧ: "ключ", О_КЛЮЧЕ: "о_ключе", СТРОК: "строк", РАЗ: "раз", ФАЙЛОВ: "файлов"}
# КОНСТРУКЦИИ ЗАПИСИ ПО ИМЕНИ (28.09, долг рода конструкций): зачин перед вопросом о месте файла и о числе записей
КОСВЕННЫЙ.update({ГДЕ_ФАЙЛ: "где", ГДЕ_ФАЙЛЫ: "где", НЕТ_ФАЙЛА: "где", ФАЙЛОВ_ИМЕНИ: "имён"})
# «find the file F» регистрами вопроса и конструкциями: «could you find …?», «i need to find …» (инфинитив — «q_найди_инф»)
НАЙДИ_РЕГИСТРЫ = ("вопросом", "вопросом2", "вопросом3") + КОНСТРУКЦИИ


def _найди_регистром(язык, вариант, f):
    """«find the file F» регистром вопроса или конструкции («could you find the file F?», «i need to find the file
    F»): повеление двери без точки и инфинитив голоса."""
    с = _слоты_вопроса(язык, 0, f=f)
    imp = РЕЧЬ[язык]["q_найди"].format(f=f, **с).rstrip(".").rstrip()
    inf = РЕЧЬ[язык]["q_найди_инф"].format(f=f, **с)
    return _ф(язык, T.РЕЧЬ[язык]["регистры"][вариант.partition("·")[2]].format(imp=imp, inf=inf))


def _зачин_вопроса(язык, род, вариант, **д):
    """Вопрос «зачин·i» на канонических слотах прямого вопроса: у ключа файл — файл настроек, у «сколько раз» место —
    папка или репозиторий, как у прямого."""
    с = _слоты_вопроса(язык, 0, f=д.get("f", д.get("s")), d=д.get("d"), k=д.get("k"), текст=д.get("w"))
    if род == РАЗ:
        с["М"] = РЕЧЬ_РЕПО[язык] if д.get("d") is None else _о(язык, "в_папке").format(d=д["d"])
    вид = int(вариант.partition("·")[2])
    return _ф(язык, " ".join(T.второй_вопрос(язык, КОСВЕННЫЙ[род], вид, **{**д, **с})) + ".")


# НАЙДИ И СКАЖИ, В КАКОМ ФАЙЛЕ (27.09, наряд ведущего (f)): «look for the word "x" and tell me which file it's in» —
# вопрос о файле тем же ходом мира (find) и тем же ответом: глагол поиска голоса (`РЕЧЬ[…]["q_ищи"]`, вид k), связка
# акта и вопроса «и» (`toolacts.СВЯЗКА_ВОПРОСА`), зачин вида z и косвенный вопрос о найденном местоимением
# (`toolacts.ВОПРОС_ВТОРОЙ["файл_оно"]`). Вид — тот, каким сказал ведущий («look for», «tell me»): одна форма, союз
# «and» держит счёт связки плана; лишь там, где «и» голоса — не связка его канонического плана (`союз_иной`)
НАХОДКА = ((1, 1),)


def связки_находки(язык):
    """Формы «связка·k·z» вопроса о файле — по видам `НАХОДКА`, там, где союзу голоса есть место."""
    return tuple(f"связка·{k}·{z}" for k, z in НАХОДКА) if союз_иной(язык) else ()


def _связка_вопроса(язык, вариант, **д):
    k, z = (int(x) for x in вариант.split("·")[1:])
    ищи = РЕЧЬ[язык]["q_ищи"][k].format(**_слоты_вопроса(язык, 0, текст=д.get("w"))).rstrip(".")
    return _ф(язык, T.связать_вопрос(язык, "и", ищи, T.второй_вопрос(язык, "файл_оно", z)) + ".")


def _выбор_повелительно(язык, вариант, **д):
    """Повелительная форма вопроса о строке по выбору — «покажи последнюю строку файла F», «прочитай первую строку F»:
    слово выбора в винительном — ряд «выбор_в» того же места, что слово дыры `c` в ряду «выбор» (суд подаёт его меткой
    `cv`); файл — канонически (`Фр`) или голым (`Фр1`, у «прочитай»)."""
    р = РЕЧЬ[язык]
    cv = д.get("cv") or р["выбор_в"][р["выбор"].index(д["c"])]
    return _q(язык, "q_" + вариант.replace("·", "_"), cv=cv, Фр=_о(язык, "файла").format(f=д["f"]),
              Фр1=_о(язык, "файла", 1).format(f=д["f"]))


def сборка_тестов_ли(язык, я, мир_, ЧИСЛА=None, ИСХОД=None, N=None, L=None, да=True):
    """Вопрос «проходят ли тесты» — «do the Python tests pass?»: предложение — прогнать тесты; после «да» — ход
    мира-процесса; итог — отчёт прогона, где числам предшествует ответ «да» или «нет» — по исходу, какой сказал мир."""
    imp, inf, zu, _past = T._ступени(язык, "тесты", **_тесты(язык, я))
    р = A.РЕЧЬ[язык]
    ответ_ = р["да" if да else "нет"] + р["двоеточие"] + ЧИСЛА
    return " ".join((_р(язык, "польз", _q(язык, "q_тесты_ли", Я=я, **_тесты(язык, я))),
                     _р(язык, "орг", _предложение(язык, inf, zu)), _р(язык, "польз", р["да"] + "."),
                     _мир(язык, мир_), _р(язык, "орг", _итог_прогона(язык, я, ответ_, ИСХОД, N, L))))


def сборка_вопроса(язык, род, вариант, мир_, **д):
    """Вопрос с дырами `д`, ход мира и ответ; найденное (путь, строка, текст, значение, число) приходит в `д`."""
    с = _слоты_вопроса(язык, вариант, f=д.get("f"), d=д.get("d"), k=д.get("k"), текст=д.get("w"))
    с0 = _слоты_вопроса(язык, 0, f=д.get("f"), d=д.get("d"), k=д.get("k"), текст=д.get("w"))

    def q(ключ):
        """Вторая и третья форма вопроса — тот же ключ речи с «2» и «3»."""
        return ключ + {"второй": "2", "третий": "3"}.get(вариант, "") if isinstance(вариант, str) else ключ
    if род in (В_КАКОМ, В_КАКИХ, НИГДЕ):
        вопрос_ = (_q(язык, "q_файлы" if род == В_КАКИХ else q("q_файл"), **с) if not str(вариант).startswith("ищи")
                   else _ф(язык, РЕЧЬ[язык]["q_ищи"][int(вариант.partition("·")[2])].format(**с)))
        if str(вариант).startswith("в_репо·"):
            вопрос_ = _q(язык, "q_файл_репо", Мр=РЕПО[язык][int(вариант.partition("·")[2])], **с)
        if род == НИГДЕ:
            ответ = _q(язык, "нигде", **с0)
        elif род == В_КАКИХ:
            ответ = _q(язык, "в_файлах", С=список(язык, д["пути"]), **с0)
        else:
            ответ = место(язык, д["w"], д["найден"], д["поз"])
    elif род == НА_СТРОКЕ:
        вопрос_, ответ = _q(язык, q("q_строка"), **с), место(язык, д["w"], д["f"], д["поз"])
    elif род == ВЫБОР:
        вопрос_ = _q(язык, {"второй": "q_выбор2", "конец": "q_конец"}.get(вариант, "q_выбор"), c=д["c"], **с)
        ответ = _q(язык, "a_выбор", c=д["c"], T=к(язык, д["T"]), **с0)
    elif род == СТРОКА_Н:
        вопрос_ = _q(язык, {"читай": "q_читай", "покажи": "q_покажи", "выведи": "q_выведи", "дай": "q_дай"}.get(
            вариант, q("q_строка_н")), a=д["a"], **с)
        ответ = _q(язык, "a_строка", a=д["a"], T=к(язык, д["T"]), **с0)
    elif род in (КЛЮЧ, О_КЛЮЧЕ):
        с_s = {**_слоты_вопроса(язык, вариант, f=д["s"], k=д["k"]), "k": д["k"]}
        с0_s = {**_слоты_вопроса(язык, 0, f=д["s"], k=д["k"]), "k": д["k"]}
        if род == КЛЮЧ:
            if str(вариант).startswith("ед·"):
                # единица ключа — «the setting port», «у параметра port»: тот же вопрос о значении
                с_s = {**с_s, "Kо": РЕЧЬ[язык]["ключ_ед"][int(вариант.partition("·")[2])].format(k=д["k"])}
            вопрос_ = _q(язык, {"без_ключа": "q_ключ_бк", "найди": "q_ключ_найди"}.get(вариант, q("q_ключ")), **с_s)
            ответ = _q(язык, "ключ_ответ", v=д["v"], **с0_s)
        else:
            вопрос_ = _q(язык, "q_о_ключе", **с_s)
            ответ = _q(язык, "a_о_ключе", T=к(язык, д["T"]), **с0_s)
    elif род == СТРОК:
        вопрос_ = _q(язык, {"посчитай": "q_посчитай_строки", "число": "q_число_строк"}.get(вариант, q("q_строк")), **с)
        ответ = T.наблюдение(язык, _строк_в(язык, д["f"], д["N"]), д["L"])
    elif род == РАЗ:
        М = РЕЧЬ_РЕПО[язык] if д.get("d") is None else _о(язык, "в_папке").format(d=д["d"])
        if д.get("f") is not None:
            М = _в_файле(язык, д["f"])            # сколько раз слово в одном файле (наряд (h2))
        раз_ = T.ВОПРОС_РАЗ2[язык] if вариант == "второй" else T.РЕЧЬ[язык]["вопрос_раз"]
        # место — именем двери `РЕПО` («in the repo», «in the codebase»); «how many occurrences …?» — единица счёта;
        # ответ называет место канонически
        Мв = РЕПО[язык][int(вариант.partition("·")[2])] if str(вариант).startswith("репо·") else М
        вопрос_ = _ф(язык, (РЕЧЬ[язык]["q_вхождений"] if вариант == "вхождения" else раз_).format(
            Wи=_текст(язык, д["w"], "и"), Wнет=_текст(язык, д["w"], "нет"), М=Мв))
        if str(вариант).startswith("счёт·"):
            # «count the occurrences of the word "x" in the repository» — повелительно, место канонически (наряд (h1))
            вопрос_ = _ф(язык, РЕЧЬ[язык]["q_посчитай_раз"][int(вариант.partition("·")[2])].format(
                Wи=_текст(язык, д["w"], "и"), Wнет=_текст(язык, д["w"], "нет"), М=М))
        ответ = T.наблюдение(язык, _встречается(язык, д["w"], М, д["N"]), д["L"])
    elif род == ФАЙЛОВ:
        ключ_ = ("q_папка2" if вариант in ("второй", "второй·сейчас") else "q_число_файлов" if вариант == "число"
                 else "q_папка")
        вопрос_ = (_ф(язык, РЕЧЬ[язык]["q_посчитай"][int(вариант.partition("·")[2])].format(**с))
                   if str(вариант).startswith("посчитай") else
                   _q(язык, ключ_ + ("_сейчас" if str(вариант).endswith("сейчас") else ""), **с))
        ответ = T.наблюдение(язык, T.папка_с_именем(язык, д["d"], д["N"]), д["L"])
    elif род == СПИСОК:
        вопрос_ = _ф(язык, РЕЧЬ[язык]["q_список"][{"второй": 1, "третий": 2}.get(вариант, 0)].format(**с))
        ответ = T.папка_с_именем(язык, д["d"], список(язык, д["записи"]))
    elif род in (ГДЕ_ФАЙЛ, ГДЕ_ФАЙЛЫ, НЕТ_ФАЙЛА, ФАЙЛОВ_ИМЕНИ):
        # найди — канонически, голым файлом, «с именем»; где — вторая форма; «locate» — глаголом голоса; в какой папке;
        # сколько — вопрос о числе записей
        вопрос_ = _q(язык, {"второй": "q_найди2", "второй·голый": "q_найди2", "по_имени": "q_найди_имя",
                            "сколько": "q_имён", "сколько·сейчас": "q_имён_сейчас", "где_лежит": "q_где_лежит",
                            "какая_папка": "q_какая_папка"}.get(вариант, "q_найди"), f=д["f"], **с)
        if род == ГДЕ_ФАЙЛ and вариант == "какая_папка":
            # одна запись: папка — родитель пути хода мира (`d` страницы), затем сам путь
            ответ = _q(язык, "a_папка", **с0) + A.РЕЧЬ[язык]["двоеточие"] + список(язык, д["пути"])
        elif род == ГДЕ_ФАЙЛ:
            ответ = _q(язык, "a_путь", С=список(язык, д["пути"]), **с0)
        elif род == НЕТ_ФАЙЛА:
            ответ = _q(язык, "a_нет_имени", f=д["f"])
        elif род == ГДЕ_ФАЙЛЫ:
            ответ = _q(язык, "a_имён", N=д["N"], f=д["f"]) + A.РЕЧЬ[язык]["двоеточие"] + список(язык, д["пути"])
        else:
            ответ = T.наблюдение(язык, _q(язык, "a_имён", N=д["N"], f=д["f"]), д["L"])
    else:
        raise ValueError(род)
    if str(вариант).startswith("зачин"):
        вопрос_ = _зачин_вопроса(язык, род, вариант, **д)
    if str(вариант).startswith("найди·"):
        вопрос_ = _найди_регистром(язык, вариант, д["f"])
    if str(вариант).startswith("связка·"):
        вопрос_ = _связка_вопроса(язык, вариант, **д)
    if вариант in ВЫБОР_ПОВЕЛИТЕЛЬНО:
        вопрос_ = _выбор_повелительно(язык, вариант, **д)
    return вопрос(язык, вопрос_, мир_, ответ)


# ======================================================================================================
# СТРАНИЦЫ — обёртки идут в мир, берут его ход и отдают сборке готовые части: числа итога — клетки хода
# ======================================================================================================
def _л(было, сдвиг):
    return A.леджер(было, сдвиг)[0]


def страница_создать(язык, род, форма, регистр, f=None, n=None, d=None):
    путь = f if f is not None else f"{d}/{n}"
    мир_ = Р.папка(язык)
    if род == СОЗДАТЬ_ОТКАЗ:
        _, ход_ = мир_.count(d if форма.startswith("папка") else папка_пути(путь))
        N = мера(ход_, "files")
        return сборка_создать(язык, род, форма, регистр, f, n, d, W.текст(ход_), A.файлов(язык, N), _л(N, 0))
    _, ход_ = мир_.create(путь)
    if род == СОЗДАТЬ_ЕСТЬ:
        return сборка_создать(язык, род, форма, регистр, f, n, d, W.текст(ход_))
    N = мера(ход_, "files")
    return сборка_создать(язык, род, форма, регистр, f, n, d, W.текст(ход_), A.файлов(язык, N), _л(N - 1, 1))


def сборка_прочитать(язык, род, форма, регистр, f, мир_, N=None, L=None):
    """Прочитать файл: приказ («read the file F», голым путём — «read F») · предложение · «да» · ход мира read · отчёт с
    числом байт файла (клетка bytes хода, леджер «B = B» — тот же, что у дома `actturn`); файла нет — отказ мира по
    имени."""
    Ф = A.РЕЧЬ[язык]["файл"].format(f=f)
    приказ_, предложение_, отчёт_, _инф = _акт_хода(язык, "прочитать", f if форма == "голый" else Ф, Ф)
    if род == ЧТЕНИЕ_НЕТ:
        return невозможный(язык, регистр, приказ_, мир_,
                           A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f)))
    return ход(язык, регистр, приказ_, предложение_, True, мир_,
               отчёт_ + ". " + T.наблюдение(язык, A.РЕЧЬ[язык]["в_файле"].format(Ф=Ф, B=N), L))


def страница_прочитать(язык, род, форма, регистр, f):
    _, ход_ = Р.папка(язык).read(f)
    if род == ЧТЕНИЕ_НЕТ:
        return сборка_прочитать(язык, род, форма, регистр, f, W.текст(ход_))
    B = мера(ход_, "bytes")
    return сборка_прочитать(язык, род, форма, регистр, f, W.текст(ход_), A.байтов(язык, B), _л(B, 0))


def сборка_прошлого_прогона(язык, форма, я, мир_, N, L):
    """«did you run the Python tests?» — мир процесса читает счёт запусков; ответ: «yes — the Python tests have been run.
    the world counts 2 runs: 2 = 2.» (форма «был», runs > 0) или «no — … have not been run. … 0 runs: 0 = 0.» («не_был»)."""
    вопрос_т, был, не_был = ПРОГОН_ПРОШЛОЕ[язык]
    р = A.РЕЧЬ[язык]
    ответ = (был if форма == "был" else не_был).format(да=р["да"], нет=р["нет"], **_тесты(язык, я))
    return вопрос(язык, _ф(язык, вопрос_т.format(**_тесты(язык, я))), мир_,
                  _ф(язык, ответ) + ". " + T._запуски(язык, N, L))


def страница_прошлого_прогона(язык, форма, я, было):
    ход_ = W.счёт_прогонов(ИМЕНА_ПРОГОНОВ[я], было)
    assert (форма == "был") == (было > 0), (форма, было)
    return сборка_прошлого_прогона(язык, форма, я, W.текст(ход_), A.запусков(язык, было), _л(было, 0))


def страница_удалить(язык, род, форма, регистр, f=None, n=None, d=None):
    путь = f if f is not None else f"{d}/{n}"
    мир_ = Р.папка(язык)
    if род == УДАЛИТЬ_ОТКАЗ:
        _, ход_ = мир_.count(d if форма.startswith("папка") else папка_пути(путь))
        N = мера(ход_, "files")
        return сборка_удалить(язык, род, форма, регистр, f, n, d, W.текст(ход_), A.файлов(язык, N), _л(N, 0))
    _, ход_ = мир_.delete(путь)
    if род == УДАЛИТЬ_НЕТ:
        return сборка_удалить(язык, род, форма, регистр, f, n, d, W.текст(ход_))
    N = мера(ход_, "files")
    return сборка_удалить(язык, род, форма, регистр, f, n, d, W.текст(ход_), A.файлов(язык, N), _л(N + 1, -1))


def страница_переноса(язык, род, форма, регистр, f, d):
    мир_ = Р.папка(язык)
    if род == ПЕРЕНОС_ОТКАЗ:
        _, ход_ = мир_.count(d)
        N = мера(ход_, "files")
        return сборка_переноса(язык, род, форма, регистр, f, d, W.текст(ход_), A.файлов(язык, N), _л(N, 0))
    _, ход_ = мир_.move(f, d)
    if род == ПЕРЕНОС_НЕТ:
        return сборка_переноса(язык, род, форма, регистр, f, d, W.текст(ход_))
    N = мера(ход_, "files")
    return сборка_переноса(язык, род, форма, регистр, f, d, W.текст(ход_), A.файлов(язык, N), _л(N - 1, 1))


def страница_имени(язык, род, форма, регистр, f, g):
    мир_ = Р.папка(язык)
    if род == ИМЯ_ОТКАЗ:
        _, ход_ = мир_.count(папка_пути(f))
        N = мера(ход_, "files")
        return сборка_имени(язык, род, форма, регистр, f, g, W.текст(ход_), A.файлов(язык, N), _л(N, 0))
    _, ход_ = мир_.move(f, (папка_пути(f) + "/" if папка_пути(f) else "") + g)
    if род in (ИМЯ_ЗАНЯТО, ИМЯ_НЕТ):
        return сборка_имени(язык, род, форма, регистр, f, g, W.текст(ход_))
    N = мера(ход_, "files")
    return сборка_имени(язык, род, форма, регистр, f, g, W.текст(ход_), A.файлов(язык, N), _л(N, 0))


def страница_замены(язык, род, форма, регистр, f, a, b):
    мир_ = Р.папка(язык)
    if род == ЗАМЕНА_ОТКАЗ:
        _, ход_ = мир_.find(f, a)
        k = мера(ход_, "occurrences")
        return сборка_замены(язык, род, форма, регистр, a, b, f, W.текст(ход_), T.раз(язык, k), _л(k, 0))
    _, ход_ = мир_.replace(f, a, b)
    if род == ЗАМЕНА_НЕТ:
        return сборка_замены(язык, род, форма, регистр, a, b, f, W.текст(ход_))
    k = мера(ход_, "occurrences")
    return сборка_замены(язык, род, форма, регистр, a, b, f, W.текст(ход_), T.раз(язык, k), _л(0, k))


def страница_дописать(язык, род, форма, регистр, f, s):
    мир_ = Р.папка(язык)
    if род == ДОПИСАТЬ_ОТКАЗ:
        _, ход_ = мир_.lines(f)
        n = мера(ход_, "lines")
        return сборка_дописать(язык, род, форма, регистр, s, f, W.текст(ход_), T.строк_вин(язык, n), _л(n, 0))
    _, ход_ = мир_.line(f, s)
    n = мера(ход_, "lines")
    return сборка_дописать(язык, род, форма, регистр, s, f, W.текст(ход_), T.строк_вин(язык, n), _л(n - 1, 1))


def _прогон(я, было, мир_=None):
    """Ход прогона: отчёт, снятый с проекта в том состоянии, в каком его держит мир страницы (без мира — объявленный)."""
    имя = ИМЕНА_ПРОГОНОВ[я]
    return W.прогон(имя, Р.снятое(имя, мир_.файлы if мир_ else None), было)


def _прогон_части(язык, я, было, мир_=None):
    """(ход мира строкой, числа отчёта, исход, запусков, леджер запусков) — прогон и его итог."""
    ход_ = _прогон(я, было, мир_)
    числа, исход_ = исход(язык, я, Р.снятое(ИМЕНА_ПРОГОНОВ[я], мир_.файлы if мир_ else None))
    runs = мера(ход_, "runs")
    return W.текст(ход_), числа, исход_, A.запусков(язык, runs), _л(runs - 1, 1)


def страница_прогона(язык, род, регистр, я, было, форма="язык", мир_=None):
    if род == ТЕСТЫ_ОТКАЗ:
        ход_ = W.счёт_прогонов(ИМЕНА_ПРОГОНОВ[я], было)
        return сборка_прогона(язык, род, регистр, я, W.текст(ход_), N=A.запусков(язык, было), L=_л(было, 0))
    return сборка_прогона(язык, род, регистр, я, *_прогон_части(язык, я, было, мир_), форма=форма)


def мир_состояния(язык, правка_):
    """Мир страницы, чей проект — в состоянии после правки (без правки — объявленный): правка идёт актом мира папки ДО
    страницы, и страница её не называет — прогон одним приказом в этом мире."""
    мир_ = Р.папка(язык)
    if правка_ is None:
        return мир_
    акт, путь, доводы = правка_
    return (мир_.replace(путь, *доводы) if акт == "replace" else мир_.line(путь, *доводы))[0]


def форма_исхода(язык, я, снятое):
    """Исход прогона, как его говорит итог, — числа знаком «#»: исход одной формы при разных числах — один исход."""
    return re.sub(r"\d+", "#", ". ".join(исход(язык, я, снятое)))


def исходы_бегуна(я):
    """[правка] — состояния проекта (None — объявленный), на каких прогон `я` кончается исходом, какого прогон на
    объявленном проекте не показывает ни у одного бегуна рода ТЕСТЫ (форма исхода по-английски); исход тех же строк
    итога, тех же упавших и того же кода выхода — однажды."""
    имя = ИМЕНА_ПРОГОНОВ[я]
    показано = {форма_исхода("en", я_, Р.снятое(ИМЕНА_ПРОГОНОВ[я_])) for я_ in (*ЯЗЫКИ_ПРОЕКТА, *КРЕЙТЫ)}
    вон, видено = [], set()
    for правка_ in (None, *ПРАВКИ_ПРОЕКТА, *СОСТОЯНИЯ_ИСХОДОВ):
        if правка_ is not None and not правка_[1].startswith(КОД_ПРОГОНА[имя]):
            continue
        снятое = Р.снятое(имя, Р.проект_после(правка_) if правка_ else None)
        ключ = (снятое["exit"], tuple(строки_итога(снятое)), tuple(упавшие_отчёта(снятое)))
        if форма_исхода("en", я, снятое) in показано or ключ in видено:
            continue
        видено.add(ключ)
        вон.append(правка_)
    return вон


def страница_плана_замены(язык, род, f, a, b, я, было):
    мир_ = Р.папка(язык)
    if род == ПЛАН_ОТКАЗ:
        _, ход_ = мир_.find(f, a)
        k = мера(ход_, "occurrences")
        return сборка_плана_замены(язык, род, a, b, f, я, W.текст(ход_), T.раз(язык, k), _л(k, 0))
    мир2, ход1 = мир_.replace(f, a, b)
    k = мера(ход1, "occurrences")
    return сборка_плана_замены(язык, род, a, b, f, я, W.текст(ход1), T.раз(язык, k), _л(0, k),
                               *_прогон_части(язык, я, было, мир2))


def страница_плана_дописать(язык, род, f, s, я, было):
    мир_ = Р.папка(язык)
    if род == ПЛАН_ОТКАЗ:
        _, ход_ = мир_.lines(f)
        n = мера(ход_, "lines")
        return сборка_плана_дописать(язык, род, s, f, я, W.текст(ход_), T.строк_вин(язык, n), _л(n, 0))
    мир2, ход1 = мир_.line(f, s)
    n = мера(ход1, "lines")
    return сборка_плана_дописать(язык, род, s, f, я, W.текст(ход1), T.строк_вин(язык, n), _л(n - 1, 1),
                                 *_прогон_части(язык, я, было, мир2))


def страница_плана_переноса(язык, род, f, d, q):
    мир_ = Р.папка(язык)
    if род == ПЛАН_ОТКАЗ:
        _, ход_ = мир_.count(d)
        N = мера(ход_, "files")
        return сборка_плана_переноса(язык, род, f, d, q, W.текст(ход_), A.файлов(язык, N), _л(N, 0))
    мир2, ход1 = мир_.move(f, d)
    N1 = мера(ход1, "files")
    _, ход2 = мир2.delete(q)
    N2 = мера(ход2, "files")
    return сборка_плана_переноса(язык, род, f, d, q, W.текст(ход1), A.файлов(язык, N1), _л(N1 - 1, 1),
                                 W.текст(ход2), A.файлов(язык, N2), _л(N2 + 1, -1))


# ПЛАН С МЕСТОИМЕНИЕМ: «it» второго акта — путь, какой строка path хода мира назвала после первого акта
def _место_после(ход_):
    (путь,) = dict.fromkeys(поле(ход_, "path"))
    return путь


def _место_чтение(язык, мир_, папка_):
    """Отказ пользователем: мир читает «до» — счёт папки, какую двинул бы первый акт."""
    _, ход_ = мир_.count(папка_)
    N = мера(ход_, "files")
    return W.текст(ход_), A.файлов(язык, N), _л(N, 0)


def _место_второй(язык, мир2, ход1, второй, s=None):
    """(ход мира второго акта, счётная фраза, леджер) — второй акт идёт на место из строки хода первого."""
    место_ = _место_после(ход1)
    if второй == "строк":
        _, ход2 = мир2.lines(место_)
        n = мера(ход2, "lines")
        return W.текст(ход2), T.строк_вин(язык, n), _л(n, 0)
    if второй == "удалить":
        _, ход2 = мир2.delete(место_)
        N = мера(ход2, "files")
        return W.текст(ход2), A.файлов(язык, N), _л(N + 1, -1)
    _, ход2 = мир2.line(место_, s)
    n = мера(ход2, "lines")
    return W.текст(ход2), T.строк_вин(язык, n), _л(n - 1, 1)


def страница_места_создать(язык, род, f, s, ссылка=None):
    мир_ = Р.папка(язык)
    if род == МЕСТО_ОТКАЗ:
        return сборка_места_создать(язык, род, f, s, *_место_чтение(язык, мир_, папка_пути(f)))
    мир2, ход1 = мир_.create(f)
    if род == МЕСТО_НЕВОЗМОЖНО:
        return сборка_места_создать(язык, род, f, s, W.текст(ход1), почему=ход1.почему, p=ход1.названо())
    N1 = мера(ход1, "files")
    assert _место_после(ход1) == f, (f, W.текст(ход1))
    return сборка_места_создать(язык, род, f, s, W.текст(ход1), A.файлов(язык, N1), _л(N1 - 1, 1),
                                *_место_второй(язык, мир2, ход1, "дописать", s), ссылка=ссылка)


def страница_места_имени(язык, род, f, g, s, ссылка=None):
    мир_ = Р.папка(язык)
    новый = (папка_пути(f) + "/" if папка_пути(f) else "") + g        # путь, какой определяет приказ
    if род == МЕСТО_ОТКАЗ:
        return сборка_места_имени(язык, род, f, g, новый, s, *_место_чтение(язык, мир_, папка_пути(f)))
    мир2, ход1 = мир_.move(f, новый)
    if род == МЕСТО_НЕВОЗМОЖНО:
        return сборка_места_имени(язык, род, f, g, ход1.названо(), s, W.текст(ход1), почему=ход1.почему)
    N1 = мера(ход1, "files")
    assert _место_после(ход1) == новый, (новый, W.текст(ход1))
    return сборка_места_имени(язык, род, f, g, новый, s, W.текст(ход1), A.файлов(язык, N1), _л(N1, 0),
                              *_место_второй(язык, мир2, ход1, "дописать", s), ссылка=ссылка)


def страница_места_переноса(язык, род, f, d, ссылка=None):
    мир_ = Р.папка(язык)
    новый = f"{d}/{имя_пути(f)}"                                     # путь, какой определяет приказ
    if род == МЕСТО_ОТКАЗ:
        return сборка_места_переноса(язык, род, f, d, новый, *_место_чтение(язык, мир_, d))
    мир2, ход1 = мир_.move(f, d)
    if род == МЕСТО_НЕВОЗМОЖНО:
        return сборка_места_переноса(язык, род, f, d, ход1.названо(), W.текст(ход1), почему=ход1.почему)
    N1 = мера(ход1, "files")
    assert _место_после(ход1) == новый, (новый, W.текст(ход1))
    return сборка_места_переноса(язык, род, f, d, новый, W.текст(ход1), A.файлов(язык, N1), _л(N1 - 1, 1),
                                 *_место_второй(язык, мир2, ход1, "удалить"), ссылка=ссылка)


def страница_места_найти(язык, род, w, s, второй="дописать"):
    мир_ = Р.папка(язык)
    _, ход1 = мир_.find(".", w)
    пути = list(dict.fromkeys(поле(ход1, "path")))
    if род == МЕСТО_МНОГО:
        assert len(пути) >= 2, (w, пути)
        return сборка_места_найти(язык, род, w, s, W.текст(ход1), пути=пути, второй=второй)
    (f,) = пути
    return сборка_места_найти(язык, род, w, s, W.текст(ход1), f=f, поз=tuple(поле(ход1, "line")), второй=второй,
                              **dict(zip(("мир2", "N2", "L2"), _место_второй(язык, мир_, ход1, второй, s))))


def _акт_в_мире(язык, мир_, вариант, f, x):
    """(путь, какой определяет приказ, мир после акта, ход акта, счётная фраза, леджер) акта плана на мире `мир_`:
    создать, удалить, переименовать (новое имя `x` в той же папке), перенести в папку `x`, дописать строку `x`,
    заменить (`x` — пара текстов)."""
    if вариант == "создать":
        мир2, ход1 = мир_.create(f)
        return f, мир2, ход1, A.файлов(язык, мера(ход1, "files")), _л(мера(ход1, "files") - 1, 1)
    if вариант == "имя":
        новый = (папка_пути(f) + "/" if папка_пути(f) else "") + x
        мир2, ход1 = мир_.move(f, новый)
        return новый, мир2, ход1, A.файлов(язык, мера(ход1, "files")), _л(мера(ход1, "files"), 0)
    if вариант == "перенос":
        мир2, ход1 = мир_.move(f, x)
        return f"{x}/{имя_пути(f)}", мир2, ход1, A.файлов(язык, мера(ход1, "files")), _л(мера(ход1, "files") - 1, 1)
    if вариант == "дописать":
        мир2, ход1 = мир_.line(f, x)
        n = мера(ход1, "lines")
        return f, мир2, ход1, T.строк_вин(язык, n), _л(n - 1, 1)
    if вариант == "удалить":
        мир2, ход1 = мир_.delete(f)
        return f, мир2, ход1, A.файлов(язык, мера(ход1, "files")), _л(мера(ход1, "files") + 1, -1)
    мир2, ход1 = мир_.replace(f, *x)
    k = мера(ход1, "occurrences")
    return f, мир2, ход1, T.раз(язык, k), _л(0, k)


def страница_места_строк(язык, план, f, x=None, s=None, ссылка=None):
    """Первый акт на мире страницы, затем чтение строк там, куда строка path положила объект."""
    новый, мир2, ход1, N1, L1 = _акт_в_мире(язык, Р.папка(язык), план, f, s if план == "дописать" else x)
    assert _место_после(ход1) == новый, (новый, W.текст(ход1))
    _, ход2 = мир2.lines(новый)
    n2 = мера(ход2, "lines")
    return сборка_места_строк(язык, план, f, x, новый, s, W.текст(ход1), N1, L1, W.текст(ход2), T.строк_вин(язык, n2),
                              _л(n2, 0), ссылка=ссылка)


# РОДЫ ЖИВЫХ ПРОСЬБ: обёртки идут в мир страницы и отдают сборке его ходы
def страница_трёх(язык, вариант, f, x, s, я=None, было=None):
    """Три акта на мире страницы: первый — по дырам; второй и третий — на месте из строки path первого хода."""
    новый, мир2, ход1, N1, L1 = _акт_в_мире(язык, Р.папка(язык), вариант, f, x)
    assert _место_после(ход1) == новый, (новый, W.текст(ход1))
    мир3, ход2 = мир2.line(новый, s)
    n2 = мера(ход2, "lines")
    части = (W.текст(ход1), N1, L1, W.текст(ход2), T.строк_вин(язык, n2), _л(n2 - 1, 1))
    if вариант == "замена":
        ход3, числа, исход_, N3, L3 = _прогон_части(язык, я, было, мир3)
        return сборка_трёх(язык, вариант, f, x, новый, s, *части, ход3, N3, L3, я=я, ЧИСЛА=числа, ИСХОД=исход_)
    _, ход3 = мир3.lines(новый)
    n3 = мера(ход3, "lines")
    return сборка_трёх(язык, вариант, f, x, новый, s, *части, W.текст(ход3), T.строк_вин(язык, n3), _л(n3, 0))


def страница_условия(язык, род, форма, f, s=None, a=None, b=None):
    """Условие проверяет мир страницы; ветка формы («|да», «|нет») — та, какую показал мир, и второй ход — её акт."""
    мир_ = Р.папка(язык)
    if род == УСЛОВИЕ_ЗАМЕНА:
        _, ход1 = мир_.find(f, a)
        да = мера(ход1, "occurrences") > 0
    else:
        _, ход1 = мир_.read(f)
        да = isinstance(ход1, W.Наблюдение)
    assert форма.endswith("|да" if да else "|нет"), (форма, W.текст(ход1))
    if not да and род != УСЛОВИЕ_ДОПИСАТЬ:
        return сборка_условия(язык, род, форма, f, W.текст(ход1), s=s, a=a, b=b)
    if род == УСЛОВИЕ_ЗАМЕНА:
        _, ход2 = мир_.replace(f, a, b)
        k = мера(ход2, "occurrences")
        N, L = T.раз(язык, k), _л(0, k)
    elif род == УСЛОВИЕ_УДАЛИТЬ:
        _, ход2 = мир_.delete(f)
        n = мера(ход2, "files")
        N, L = A.файлов(язык, n), _л(n + 1, -1)
    elif да:
        _, ход2 = мир_.line(f, s)
        n = мера(ход2, "lines")
        N, L = T.строк_вин(язык, n), _л(n - 1, 1)
    else:
        _, ход2 = мир_.create(f)
        n = мера(ход2, "files")
        N, L = A.файлов(язык, n), _л(n - 1, 1)
    return сборка_условия(язык, род, форма, f, W.текст(ход1), W.текст(ход2), N, L, s=s, a=a, b=b)


def страница_кроме(язык, акт, форма, d, n, e=None):
    """Мир читает папку; акт идёт на всякую запись-файл, кроме названной, по порядку записей мира."""
    мир_ = Р.папка(язык)
    _, ход1 = мир_.list(d)
    записи = поле(ход1, "path")
    акты = []
    for запись in записи:
        if запись.endswith("/") or запись == n:
            continue
        путь = f"{d}/{запись}"
        if акт == "удалить":
            мир_, ход_ = мир_.delete(путь)
            m = мера(ход_, "files")
            акты.append((W.текст(ход_), путь, A.файлов(язык, m), _л(m + 1, -1)))
        else:
            мир_, ход_ = мир_.move(путь, e)
            m = мера(ход_, "files")
            акты.append((W.текст(ход_), путь, A.файлов(язык, m), _л(m - 1, 1)))
    assert акты and n in записи, (d, n, записи)
    return сборка_кроме(язык, акт, форма, d, n, e, W.текст(ход1), записи, акты)


def страница_двух(язык, акт, форма, f, q, d=None, s=None):
    """Два акта по очереди на мире страницы: второй — на мире после первого."""
    мир_ = Р.папка(язык)
    части = []
    for x in (f, q):
        if акт == "создать":
            мир_, ход_ = мир_.create(x)
            m = мера(ход_, "files")
            части += [W.текст(ход_), A.файлов(язык, m), _л(m - 1, 1)]
        elif акт == "удалить":
            мир_, ход_ = мир_.delete(x)
            m = мера(ход_, "files")
            части += [W.текст(ход_), A.файлов(язык, m), _л(m + 1, -1)]
        elif акт == "перенести":
            мир_, ход_ = мир_.move(x, d)
            m = мера(ход_, "files")
            части += [W.текст(ход_), A.файлов(язык, m), _л(m - 1, 1)]
        else:
            мир_, ход_ = мир_.line(x, s)
            m = мера(ход_, "lines")
            части += [W.текст(ход_), T.строк_вин(язык, m), _л(m - 1, 1)]
    return сборка_двух(язык, акт, форма, f, q, *части, d=d, s=s)


def страница_тестов_сколько(язык, род, я, было, форма="язык"):
    return сборка_тестов_сколько(язык, род, я, *_прогон_части(язык, я, было), форма=форма)


def страница_плана_скажи(язык, план, вопрос_, вид, f, x, w=None):
    """Первый акт на мире страницы, затем второй ход — чтение строк там, куда строка path положила файл, или находка
    слова `w` во всём репозитории после акта: слово стоит лишь в этом файле, и находка называет его новое место."""
    новый, мир2, ход1, N1, L1 = _акт_в_мире(язык, Р.папка(язык), план, f, x)
    assert _место_после(ход1) == новый, (новый, W.текст(ход1))
    if вопрос_ == "первая":
        _, ход2 = мир2.lines(новый)
        return сборка_плана_скажи(язык, план, вопрос_, вид, f, x, новый, W.текст(ход1), N1, L1, W.текст(ход2),
                                  T_=поле(ход2, "text")[0])
    _, ход2 = мир2.find(".", w)
    assert list(dict.fromkeys(поле(ход2, "path"))) == [новый], (w, W.текст(ход2))
    return сборка_плана_скажи(язык, план, вопрос_, вид, f, x, новый, W.текст(ход1), N1, L1, W.текст(ход2), w=w,
                              поз=tuple(поле(ход2, "line")))


def страница_двух_актов(язык, пара, f, x, q, y):
    """Первый акт пары на мире страницы, второй — на мире после первого."""
    первый, второй = пара.split("+")
    _путь1, мир2, ход1, N1, L1 = _акт_в_мире(язык, Р.папка(язык), первый, f, x)
    _путь2, _мир3, ход2, N2, L2 = _акт_в_мире(язык, мир2, второй, q, y)
    return сборка_двух_актов(язык, пара, f, x, q, y, W.текст(ход1), N1, L1, W.текст(ход2), N2, L2)


def _дыры_двух_актов(язык, пара, f, x, q, y):
    """Дыры плана из двух разных актов: файл и довод первого акта, файл и довод второго."""
    дыры = {"f": f, "q": q}
    for акт, довод in zip(пара.split("+"), (x, y)):
        if акт == "перенос":
            дыры["d"] = довод
        elif акт == "имя":
            дыры["g"] = довод
        elif акт == "дописать":
            дыры["s"] = к(язык, довод)
        elif акт == "замена":
            дыры.update(a=к(язык, довод[0]), b=к(язык, довод[1]))
    return дыры


def страница_прошлого(язык, форма, f):
    """Мир читает файл: есть он — наблюдение, нет — отказ мира по имени; форма страницы — то, что прочёл мир."""
    _, ход_ = Р.папка(язык).read(f)
    assert (форма == "есть") == isinstance(ход_, W.Наблюдение), (f, W.текст(ход_))
    return сборка_прошлого(язык, форма, f, W.текст(ход_))


def страница_тестов_ли(язык, я, было):
    """Прогон объявленного проекта; «да» — исход мира успешен (код выхода 0), «нет» — нет."""
    мир_, числа, исход_, N, L = _прогон_части(язык, я, было)
    return сборка_тестов_ли(язык, я, мир_, числа, исход_, N, L, Р.снятое(ИМЕНА_ПРОГОНОВ[я])["exit"] == 0)


def страница_вопроса(язык, род, вариант, **д):
    """Обёртка вопросов: идёт в мир, берёт ход и отдаёт сборке найденное — клетки хода."""
    мир_ = Р.папка(язык)
    if род in (В_КАКОМ, В_КАКИХ, НИГДЕ):
        _, ход_ = мир_.find(".", д["w"])
        пути = list(dict.fromkeys(поле(ход_, "path")))
        if род == В_КАКОМ:
            (найден,) = пути
            д.update(найден=найден, поз=tuple(поле(ход_, "line")))
        elif род == В_КАКИХ:
            д.update(пути=пути)
    elif род == НА_СТРОКЕ:
        _, ход_ = мир_.find(д["f"], д["w"])
        д.update(поз=tuple(поле(ход_, "line")))
    elif род in (ВЫБОР, СТРОКА_Н):
        _, ход_ = мир_.lines(д["f"])
        i = д.pop("i")
        д.update(T=поле(ход_, "text")[i], a=поле(ход_, "line")[i])
    elif род in (КЛЮЧ, О_КЛЮЧЕ):
        _, ход_ = мир_.find(д["s"], д["k"])
        (строка,) = поле(ход_, "text")
        д.update(v=строка.partition(" = ")[2], T=строка, a=поле(ход_, "line")[0])
    elif род == СТРОК:
        _, ход_ = мир_.lines(д["f"])
        n = мера(ход_, "lines")
        д.update(N=T.строк_вин(язык, n), L=_л(n, 0))
    elif род == РАЗ:
        _, ход_ = мир_.find(д.get("d") or ".", д["w"])
        if д.get("f") is not None:
            _, ход_ = мир_.find(д["f"], д["w"])
        n = мера(ход_, "occurrences")
        д.update(N=T.раз(язык, n), L=_л(n, 0))
    elif род == ФАЙЛОВ:
        _, ход_ = мир_.count(д["d"])
        n = мера(ход_, "files")
        д.update(N=A.файлов(язык, n), L=_л(n, 0))
    elif род == СПИСОК:
        _, ход_ = мир_.list(д["d"])
        д.update(записи=поле(ход_, "path"))
    elif род in (ГДЕ_ФАЙЛ, ГДЕ_ФАЙЛЫ, НЕТ_ФАЙЛА, ФАЙЛОВ_ИМЕНИ):
        _, ход_ = мир_.locate(".", д["f"])
        n = мера(ход_, "entries")
        # род страницы — то, что нашёл мир: одна запись, несколько, ни одной; число — у одной и нескольких
        assert {ГДЕ_ФАЙЛ: n == 1, ГДЕ_ФАЙЛЫ: n > 1, НЕТ_ФАЙЛА: n == 0, ФАЙЛОВ_ИМЕНИ: n > 0}[род], (род, д["f"], n)
        д.update(пути=поле(ход_, "path"), N=A.файлов(язык, n), L=_л(n, 0))
        if n == 1:
            д.update(d=папка_пути(д["пути"][0]))      # «which folder holds F?» — папка записи, родитель её пути
    return сборка_вопроса(язык, род, вариант, W.текст(ход_), **д)


# ======================================================================================================
# ПОКАЗЫ: всякая форма приказа и вопроса — на всяком языке, не меньше четырёх страниц с разными наполнителями
# ======================================================================================================
def единственные_слова(язык):
    """(файл, слово): в каждом текстовом файле первое слово, что стоит во всём мире один раз (подстрокой тоже) и не
    в первой строке — ответ «строка 1» не разводит источники."""
    мир_ = папка(язык)
    вон = []
    for f in ТЕКСТЫ:
        for i, строка in enumerate(мир_.файлы[f][1:], 2):
            for w in строка.split():
                if len(w) >= 4 and мера(мир_.find(".", w)[1], "occurrences") == 1:
                    вон.append((f, w))
                    break
            else:
                continue
            break
    return вон


def _варианты(язык, фраза):
    return range(len(T.ОБЪЕКТЫ[язык][фраза]))


def _кругом(ряд, i, n=4):
    """n членов ряда, начиная с i-го по кругу — у каждой формы свои наполнители."""
    return [ряд[(i + j) % len(ряд)] for j in range(min(n, len(ряд)))]


# НАПОЛНИТЕЛИ ПЛАНА С МЕСТОИМЕНИЕМ — из объявления мира: создают и дописывают в текстовой части репозитория (в папках,
# где лежат тексты); переименовывают файлы в папках — новый путь (папка/имя) не равен ни одному слову приказа, и рынок
# отличит путь из хода мира от пути из приказа
МЕСТО_СОЗДАТЬ_ПУТИ = tuple(f for f in СОЗДАТЬ_ПУТИ if папка_пути(f) in {папка_пути(т) for т in ТЕКСТЫ})
МЕСТО_ИМЕНА = tuple((f, g) for f, g in ИМЕНА if папка_пути(f))
# в созданный файл дописывается строка текстового файла ТОЙ ЖЕ ПАПКИ (по порядку имён; в корне — по одному на файл):
# строка о поездке — в новый файл поездок, о кухне — в кухонный
МЕСТО_СОСЕД = {f: sorted(т for т in ТЕКСТЫ if папка_пути(т) == папка_пути(f))[
    [x for x in МЕСТО_СОЗДАТЬ_ПУТИ if папка_пути(x) == папка_пути(f)].index(f)] for f in МЕСТО_СОЗДАТЬ_ПУТИ}


# НАПОЛНИТЕЛИ ЗАПИСИ ПО ИМЕНИ — из объявления мира: имя файла в папке, какое стоит в мире однажды (путь ответа — не
# слово приказа), и имя, какое стоит в нескольких папках (одно имя в двух крейтах); ни одной записи — `НЕТ_ФАЙЛОВ`
_ИМЁН = collections.Counter(имя_пути(п) for п in ПУТИ)
ОДНО_ИМЯ = tuple(имя_пути(п) for п in ПУТИ if папка_пути(п) and _ИМЁН[имя_пути(п)] == 1)
МНОГО_ИМЁН = tuple(dict.fromkeys(имя_пути(п) for п in ПУТИ if _ИМЁН[имя_пути(п)] > 1))


def _показы():
    вон, перепись = {}, {}

    def положить(стр, язык, род, форма, регистр, дыры):
        if стр not in вон:
            вон[стр] = (язык, род, форма, регистр)
            перепись[стр] = дыры

    п_, в_ = "плоский", "вежливый"
    for язык in ЯЗЫКИ:
        с = СОДЕРЖИМОЕ[язык]
        # СОЗДАТЬ: по пути — «the file», голым путём, «пустой», «новый»; в названной папке — всеми формами места
        for f in СОЗДАТЬ_ПУТИ:
            положить(страница_создать(язык, СОЗДАТЬ, "канон", п_, f=f), язык, СОЗДАТЬ, "канон", п_, {"f": f})
        for i, форма in enumerate(("голый", "пустой", "новый")):
            for f in _кругом(СОЗДАТЬ_ПУТИ, 2 * i):
                положить(страница_создать(язык, СОЗДАТЬ, форма, п_, f=f), язык, СОЗДАТЬ, форма, п_, {"f": f})
        for f in СОЗДАТЬ_ПУТИ[1::2]:
            положить(страница_создать(язык, СОЗДАТЬ, "канон", в_, f=f), язык, СОЗДАТЬ, "канон", в_, {"f": f})
        for v in _варианты(язык, "в_папке"):
            for n, d in (СОЗДАТЬ_В_ПАПКЕ if v == 0 else _кругом(СОЗДАТЬ_В_ПАПКЕ, v)):
                положить(страница_создать(язык, СОЗДАТЬ, f"папка·{v}", п_, n=n, d=d), язык, СОЗДАТЬ_ПАПКА,
                         f"папка·{v}", п_, {"n": n, "d": d})
        for f in ("shopping.txt", "home/chores.md", "kitchen/soup.md"):
            положить(страница_создать(язык, СОЗДАТЬ_ЕСТЬ, "канон", п_, f=f), язык, СОЗДАТЬ_ЕСТЬ, "канон", п_, {"f": f})
        for f in ("home/garden.md", "trips/lake.md"):
            положить(страница_создать(язык, СОЗДАТЬ_ОТКАЗ, "канон", п_, f=f), язык, СОЗДАТЬ_ОТКАЗ, "канон", п_, {"f": f})
        # УДАЛИТЬ
        for f in ТЕКСТЫ:
            положить(страница_удалить(язык, УДАЛИТЬ, "канон", п_, f=f), язык, УДАЛИТЬ, "канон", п_, {"f": f})
        for f in ТЕКСТЫ[:4]:
            положить(страница_удалить(язык, УДАЛИТЬ, "голый", п_, f=f), язык, УДАЛИТЬ, "голый", п_, {"f": f})
        for f in ТЕКСТЫ[4:]:
            положить(страница_удалить(язык, УДАЛИТЬ, "канон", в_, f=f), язык, УДАЛИТЬ, "канон", в_, {"f": f})
        for v in _варианты(язык, "из_папки"):
            for n, d in (УДАЛИТЬ_ИЗ_ПАПКИ if v == 0 else _кругом(УДАЛИТЬ_ИЗ_ПАПКИ, v)):
                положить(страница_удалить(язык, УДАЛИТЬ, f"папка·{v}", п_, n=n, d=d), язык, УДАЛИТЬ_ПАПКА,
                         f"папка·{v}", п_, {"n": n, "d": d})
        for f in НЕТ_ФАЙЛОВ:
            положить(страница_удалить(язык, УДАЛИТЬ_НЕТ, "канон", п_, f=f), язык, УДАЛИТЬ_НЕТ, "канон", п_, {"f": f})
        for f in ("home/repairs.txt", "kitchen/soup.md"):
            положить(страница_удалить(язык, УДАЛИТЬ_ОТКАЗ, "канон", п_, f=f), язык, УДАЛИТЬ_ОТКАЗ, "канон", п_,
                     {"f": f})
        # ПЕРЕНЕСТИ — в папки, какие есть
        формы = варианты_переноса(язык)
        for i, форма in enumerate(формы):
            for f, d in (ПЕРЕНОСЫ if i == 0 else _кругом(ПЕРЕНОСЫ, 2 * i)):
                положить(страница_переноса(язык, ПЕРЕНОС, форма, п_, f, d), язык, ПЕРЕНОС, форма, п_, {"f": f, "d": d})
        for f, d in ПЕРЕНОСЫ[1::2]:
            положить(страница_переноса(язык, ПЕРЕНОС, формы[0], в_, f, d), язык, ПЕРЕНОС, формы[0], в_,
                     {"f": f, "d": d})
        for f, d in zip(НЕТ_ФАЙЛОВ, ("home", "kitchen")):
            положить(страница_переноса(язык, ПЕРЕНОС_НЕТ, формы[0], п_, f, d), язык, ПЕРЕНОС_НЕТ, формы[0], п_,
                     {"f": f, "d": d})
        for f, d in (ПЕРЕНОСЫ[2], ПЕРЕНОСЫ[5]):
            положить(страница_переноса(язык, ПЕРЕНОС_ОТКАЗ, формы[0], п_, f, d), язык, ПЕРЕНОС_ОТКАЗ, формы[0], п_,
                     {"f": f, "d": d})
        # ПЕРЕИМЕНОВАТЬ
        for f, g in ИМЕНА:
            положить(страница_имени(язык, ИМЯ, "канон", п_, f, g), язык, ИМЯ, "канон", п_, {"f": f, "g": g})
        for f, g in ИМЕНА[::2]:
            положить(страница_имени(язык, ИМЯ, "голый", п_, f, g), язык, ИМЯ, "голый", п_, {"f": f, "g": g})
        for f, g in ИМЕНА[1::2]:
            положить(страница_имени(язык, ИМЯ, "канон", в_, f, g), язык, ИМЯ, "канон", в_, {"f": f, "g": g})
        for род, пары in ((ИМЯ_ЗАНЯТО, ИМЕНА_ЗАНЯТЫ), (ИМЯ_НЕТ, ИМЕНА_НЕТ), (ИМЯ_ОТКАЗ, (ИМЕНА[3], ИМЕНА[7]))):
            for f, g in пары:
                положить(страница_имени(язык, род, "канон", п_, f, g), язык, род, "канон", п_, {"f": f, "g": g})
        # ЗАМЕНИТЬ: текст из нескольких слов — «the text» и голым; слово — «the word»
        for i, f in enumerate(ТЕКСТЫ):
            _строки, (a, b), (w, v), _s = с[f]
            дыры = {"a": к(язык, a), "b": к(язык, b), "f": f}
            положить(страница_замены(язык, ЗАМЕНА, "текст", п_, f, a, b), язык, ЗАМЕНА, "текст", п_, дыры)
            форма, регистр = ("голый", п_) if i % 2 == 0 else ("текст", в_)
            положить(страница_замены(язык, ЗАМЕНА, форма, регистр, f, a, b), язык, ЗАМЕНА, форма, регистр, дыры)
            положить(страница_замены(язык, ЗАМЕНА_СЛОВА, "слово", п_, f, w, v), язык, ЗАМЕНА_СЛОВА, "слово", п_,
                     {"a": к(язык, w), "b": к(язык, v), "f": f})
        for f, a in zip((ТЕКСТЫ[0], ТЕКСТЫ[5]), НЕТ_ТЕКСТА[язык]):
            b = с[f][1][1]
            положить(страница_замены(язык, ЗАМЕНА_НЕТ, "текст", п_, f, a, b), язык, ЗАМЕНА_НЕТ, "текст", п_,
                     {"a": к(язык, a), "b": к(язык, b), "f": f})
        for f in (ТЕКСТЫ[2], ТЕКСТЫ[7]):
            a, b = с[f][1]
            положить(страница_замены(язык, ЗАМЕНА_ОТКАЗ, "текст", п_, f, a, b), язык, ЗАМЕНА_ОТКАЗ, "текст", п_,
                     {"a": к(язык, a), "b": к(язык, b), "f": f})
        # ДОПИСАТЬ СТРОКУ — акт строки мира (М-2016)
        for i, f in enumerate(ТЕКСТЫ):
            s = с[f][3]
            положить(страница_дописать(язык, ДОПИСАТЬ, "канон", п_, f, s), язык, ДОПИСАТЬ, "канон", п_,
                     {"s": к(язык, s), "f": f})
            форма, регистр = ("голый", п_) if i % 2 else ("канон", в_)
            положить(страница_дописать(язык, ДОПИСАТЬ, форма, регистр, f, s), язык, ДОПИСАТЬ, форма, регистр,
                     {"s": к(язык, s), "f": f})
        for f in (ТЕКСТЫ[0], ТЕКСТЫ[5]):
            s = с[f][3]
            положить(страница_дописать(язык, ДОПИСАТЬ_ОТКАЗ, "канон", п_, f, s), язык, ДОПИСАТЬ_ОТКАЗ, "канон", п_,
                     {"s": к(язык, s), "f": f})
        # ТЕСТЫ ПО ЯЗЫКУ ПРОЕКТА — отчёт бегуна в ходе мира
        for я in ЯЗЫКИ_ПРОЕКТА:
            for было in ЗАПУСКИ_ДО:
                положить(страница_прогона(язык, ТЕСТЫ, п_, я, было), язык, ТЕСТЫ, "язык", п_, {"Я": я})
            for было in ЗАПУСКИ_ДО[:2]:
                положить(страница_прогона(язык, ТЕСТЫ, в_, я, было), язык, ТЕСТЫ, "язык", в_, {"Я": я})
        for я, было in zip(ЯЗЫКИ_ПРОЕКТА, ЗАПУСКИ_ДО[1:]):
            положить(страница_прогона(язык, ТЕСТЫ_ОТКАЗ, п_, я, было), язык, ТЕСТЫ_ОТКАЗ, "язык", п_, {"Я": я})
        # ПЛАНЫ ИЗ ДВУХ АКТОВ
        языки_проекта = tuple(ЯЗЫКИ_ПРОЕКТА)
        for i, f in enumerate(ТЕКСТЫ):
            a, b = с[f][1]
            я, я2 = языки_проекта[i % 2], языки_проекта[(i + 1) % 2]
            положить(страница_плана_замены(язык, ПЛАН_ЗАМЕНА, f, a, b, я, ЗАПУСКИ_ДО[i % 3]), язык, ПЛАН_ЗАМЕНА,
                     "замена", п_, {"a": к(язык, a), "b": к(язык, b), "f": f, "Я": я})
            положить(страница_плана_дописать(язык, ПЛАН_ДОПИСАТЬ, f, с[f][3], я2, ЗАПУСКИ_ДО[(i + 1) % 3]), язык,
                     ПЛАН_ДОПИСАТЬ, "дописать", п_, {"s": к(язык, с[f][3]), "f": f, "Я": я2})
            f2, d = ПЕРЕНОСЫ[i]
            q = ТЕКСТЫ[(i + 3) % len(ТЕКСТЫ)]
            положить(страница_плана_переноса(язык, ПЛАН_ПЕРЕНОС, f2, d, q), язык, ПЛАН_ПЕРЕНОС, "перенос", п_,
                     {"f": f2, "d": d, "q": q})
        a, b = с[ТЕКСТЫ[1]][1]
        положить(страница_плана_замены(язык, ПЛАН_ОТКАЗ, ТЕКСТЫ[1], a, b, "Rust", 1), язык, ПЛАН_ОТКАЗ, "замена", п_,
                 {"a": к(язык, a), "b": к(язык, b), "f": ТЕКСТЫ[1], "Я": "Rust"})
        положить(страница_плана_дописать(язык, ПЛАН_ОТКАЗ, ТЕКСТЫ[2], с[ТЕКСТЫ[2]][3], "Python", 1), язык, ПЛАН_ОТКАЗ,
                 "дописать", п_, {"s": к(язык, с[ТЕКСТЫ[2]][3]), "f": ТЕКСТЫ[2], "Я": "Python"})
        положить(страница_плана_переноса(язык, ПЛАН_ОТКАЗ, *ПЕРЕНОСЫ[3], ТЕКСТЫ[0]), язык, ПЛАН_ОТКАЗ, "перенос", п_,
                 {"f": ПЕРЕНОСЫ[3][0], "d": ПЕРЕНОСЫ[3][1], "q": ТЕКСТЫ[0]})
        # ПЛАНЫ С МЕСТОИМЕНИЕМ: «it» — объект первого акта; второй акт идёт на путь из строки хода мира
        строки_ = [с[f][3] for f in ТЕКСТЫ]
        for f in МЕСТО_СОЗДАТЬ_ПУТИ:
            s = с[МЕСТО_СОСЕД[f]][3]
            положить(страница_места_создать(язык, МЕСТО_СОЗДАТЬ, f, s), язык, МЕСТО_СОЗДАТЬ, "создать", п_,
                     {"f": f, "s": к(язык, s)})
        for f, s in zip(МЕСТО_СОЗДАТЬ_ПУТИ[2:4], строки_[5:]):
            положить(страница_места_создать(язык, МЕСТО_ОТКАЗ, f, s), язык, МЕСТО_ОТКАЗ, "создать", п_,
                     {"f": f, "s": к(язык, s)})
        for f, s in zip((ТЕКСТЫ[0], ТЕКСТЫ[2], ТЕКСТЫ[6]), строки_[5:]):
            положить(страница_места_создать(язык, МЕСТО_НЕВОЗМОЖНО, f, s), язык, МЕСТО_НЕВОЗМОЖНО, "создать", п_,
                     {"f": f, "s": к(язык, s)})
        for f, g in МЕСТО_ИМЕНА:
            положить(страница_места_имени(язык, МЕСТО_ИМЯ, f, g, с[f][3]), язык, МЕСТО_ИМЯ, "имя", п_,
                     {"f": f, "g": g, "s": к(язык, с[f][3])})
        for f, g in МЕСТО_ИМЕНА[1::3]:
            положить(страница_места_имени(язык, МЕСТО_ОТКАЗ, f, g, с[f][3]), язык, МЕСТО_ОТКАЗ, "имя", п_,
                     {"f": f, "g": g, "s": к(язык, с[f][3])})
        for (f, g), s in zip(ИМЕНА_ЗАНЯТЫ + ИМЕНА_НЕТ, строки_[3:]):
            положить(страница_места_имени(язык, МЕСТО_НЕВОЗМОЖНО, f, g, s), язык, МЕСТО_НЕВОЗМОЖНО, "имя", п_,
                     {"f": f, "g": g, "s": к(язык, s)})
        for f, d in ПЕРЕНОСЫ:
            положить(страница_места_переноса(язык, МЕСТО_ПЕРЕНОС, f, d), язык, МЕСТО_ПЕРЕНОС, "перенос", п_,
                     {"f": f, "d": d})
        for f, d in (ПЕРЕНОСЫ[1], ПЕРЕНОСЫ[6]):
            положить(страница_места_переноса(язык, МЕСТО_ОТКАЗ, f, d), язык, МЕСТО_ОТКАЗ, "перенос", п_,
                     {"f": f, "d": d})
        for f, d in zip(НЕТ_ФАЙЛОВ, ("home", "kitchen")):
            положить(страница_места_переноса(язык, МЕСТО_НЕВОЗМОЖНО, f, d), язык, МЕСТО_НЕВОЗМОЖНО, "перенос", п_,
                     {"f": f, "d": d})
        for f, w in единственные_слова(язык):
            положить(страница_места_найти(язык, МЕСТО_НАЙТИ, w, с[f][3]), язык, МЕСТО_НАЙТИ, "найти", п_,
                     {"w": к(язык, w), "s": к(язык, с[f][3])})
        for w, s in zip(В_ДВУХ[язык] + В_ТРЁХ[язык], строки_[2:]):
            положить(страница_места_найти(язык, МЕСТО_МНОГО, w, s), язык, МЕСТО_МНОГО, "найти", п_,
                     {"w": к(язык, w), "s": к(язык, s)})
        # ВОПРОСЫ
        def вопрос_(род, вариант, форма, дыры, **д):
            положить(страница_вопроса(язык, род, вариант, **д), язык, род, форма, п_, дыры)

        мир_ = папка(язык)
        единственные = единственные_слова(язык)
        for i, f in enumerate(ТЕКСТЫ):
            a = с[f][1][0]
            вопрос_(В_КАКОМ, 0, "текст", {"w": к(язык, a)}, w=a)
            вопрос_(НА_СТРОКЕ, 0, "текст", {"f": f, "w": к(язык, a)}, f=f, w=a)
            if i % 2:
                вопрос_(В_КАКОМ, 1, "голый", {"w": к(язык, a)}, w=a)
            else:
                вопрос_(НА_СТРОКЕ, 1, "голый", {"f": f, "w": к(язык, a)}, f=f, w=a)
            строк_ = len(с[f][0])
            for j, c in enumerate(РЕЧЬ[язык]["выбор"]):
                вопрос_(ВЫБОР, 0, "канон", {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if j == 2 else j))
            c = РЕЧЬ[язык]["выбор"][i % 3]
            вопрос_(ВЫБОР, 1, "голый", {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if i % 3 == 2 else i % 3))
            n = 2 + i % (строк_ - 1)
            вопрос_(СТРОКА_Н, 0, "канон", {"f": f, "a": str(n)}, f=f, i=n - 1)
            if i % 2 == 0:
                вопрос_(СТРОКА_Н, 1, "голый", {"f": f, "a": str(n)}, f=f, i=n - 1)
            вопрос_(СТРОК, 0, "канон", {"f": f}, f=f)
            if i % 2:
                вопрос_(СТРОК, 1, "голый", {"f": f}, f=f)
        for f, w in единственные:
            вопрос_(В_КАКОМ, 0, "слово", {"w": к(язык, w)}, w=w)
            вопрос_(НА_СТРОКЕ, 0, "слово", {"f": f, "w": к(язык, w)}, f=f, w=w)
        for w in В_ДВУХ[язык] + В_ТРЁХ[язык]:
            вопрос_(В_КАКИХ, 0, "слово", {"w": к(язык, w)}, w=w)
        for a in НЕТ_ТЕКСТА[язык]:
            вопрос_(НИГДЕ, 0, "текст", {"w": к(язык, a)}, w=a)
        for w in ДВАЖДЫ[язык]:
            путь = поле(мир_.find(".", w)[1], "path")[0]   # первый файл слова в порядке мира
            вопрос_(НА_СТРОКЕ, 0, "слово", {"f": путь, "w": к(язык, w)}, f=путь, w=w)
            вопрос_(РАЗ, 0, "репо", {"w": к(язык, w)}, w=w)
            вопрос_(РАЗ, 0, "папка", {"w": к(язык, w), "d": папка_пути(путь)}, w=w, d=папка_пути(путь))
        for s, k_ in КЛЮЧИ:
            вопрос_(КЛЮЧ, 0, "канон", {"k": k_, "s": s}, s=s, k=k_)
            вопрос_(КЛЮЧ, 1, "голый", {"k": k_, "s": s}, s=s, k=k_)
            вопрос_(О_КЛЮЧЕ, 0, "канон", {"k": k_, "s": s}, s=s, k=k_)
            вопрос_(О_КЛЮЧЕ, 1, "голый", {"k": k_, "s": s}, s=s, k=k_)
        for f in ("web/main.py", "tests/test_main.py", "tally/src/lib.rs", "server.ini"):
            вопрос_(СТРОК, 0, "канон", {"f": f}, f=f)
        for v in _варианты(язык, "в_папке"):
            for d in (ПАПКИ_СЧЁТА if v == 0 else _кругом(ПАПКИ_СЧЁТА, 2 * v)):
                вопрос_(ФАЙЛОВ, v, f"папка·{v}", {"d": d}, d=d)
        # СЕМЬИ ПЕРЕФРАЗА (заказ ведущего, М-2021): правленая форма стоит на тех же наполнителях, что и каноническая
        # страница, — пара одного акта мира; четыре основы на правку, одна основа служит всем своим правкам
        в2 = ("вопросом", "вопросом2", "вопросом3") + КОНСТРУКЦИИ
        for f in СОЗДАТЬ_ПУТИ[:4]:
            for р in в2:
                положить(страница_создать(язык, СОЗДАТЬ, "канон", р, f=f), язык, СОЗДАТЬ, "канон", р, {"f": f})
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_создать(язык, СОЗДАТЬ, "синоним·голый", р, f=f), язык, СОЗДАТЬ, "синоним·голый", р,
                         {"f": f})
            for форма in ("назв",) + синонимы(язык, "создать") + ("страд",):
                положить(страница_создать(язык, СОЗДАТЬ, форма, п_, f=f), язык, СОЗДАТЬ, форма, п_, {"f": f})
        for n, d in СОЗДАТЬ_В_ПАПКЕ[:4]:
            положить(страница_создать(язык, СОЗДАТЬ, "впереди·0", п_, n=n, d=d), язык, СОЗДАТЬ_ПАПКА, "впереди·0", п_,
                     {"n": n, "d": d})
        for f in ТЕКСТЫ[:4]:
            for р in в2:
                положить(страница_удалить(язык, УДАЛИТЬ, "канон", р, f=f), язык, УДАЛИТЬ, "канон", р, {"f": f})
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_удалить(язык, УДАЛИТЬ, "синоним·голый", р, f=f), язык, УДАЛИТЬ, "синоним·голый", р,
                         {"f": f})
            for форма in ("назв",) + синонимы(язык, "удалить") + ("страд",):
                положить(страница_удалить(язык, УДАЛИТЬ, форма, п_, f=f), язык, УДАЛИТЬ, форма, п_, {"f": f})
        for n, d in УДАЛИТЬ_ИЗ_ПАПКИ[:4]:
            положить(страница_удалить(язык, УДАЛИТЬ, "впереди·0", п_, n=n, d=d), язык, УДАЛИТЬ_ПАПКА, "впереди·0", п_,
                     {"n": n, "d": d})
        for f, d in ПЕРЕНОСЫ[:4]:
            for р in в2:
                положить(страница_переноса(язык, ПЕРЕНОС, "0·0", р, f, d), язык, ПЕРЕНОС, "0·0", р, {"f": f, "d": d})
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_переноса(язык, ПЕРЕНОС, "синоним·голый", р, f, d), язык, ПЕРЕНОС, "синоним·голый", р,
                         {"f": f, "d": d})
            for форма in ("2·0",) + синонимы(язык, "перенести") + ("страд",):
                положить(страница_переноса(язык, ПЕРЕНОС, форма, п_, f, d), язык, ПЕРЕНОС, форма, п_, {"f": f, "d": d})
        for f, g in ИМЕНА[:4]:
            for р in в2:
                положить(страница_имени(язык, ИМЯ, "канон", р, f, g), язык, ИМЯ, "канон", р, {"f": f, "g": g})
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_имени(язык, ИМЯ, "синоним·голый", р, f, g), язык, ИМЯ, "синоним·голый", р,
                         {"f": f, "g": g})
            for форма in ("назв",) + синонимы(язык, "переименовать") + ("страд",):
                положить(страница_имени(язык, ИМЯ, форма, п_, f, g), язык, ИМЯ, форма, п_, {"f": f, "g": g})
        for f in ТЕКСТЫ[:4]:
            s = с[f][3]
            for р in в2:
                положить(страница_дописать(язык, ДОПИСАТЬ, "канон", р, f, s), язык, ДОПИСАТЬ, "канон", р,
                         {"s": к(язык, s), "f": f})
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_дописать(язык, ДОПИСАТЬ, "синоним·голый", р, f, s), язык, ДОПИСАТЬ, "синоним·голый", р,
                         {"s": к(язык, s), "f": f})
            for форма in ("назв", "синоним", "конец") + синонимы(язык, "дописать")[1:] + ("страд",):
                положить(страница_дописать(язык, ДОПИСАТЬ, форма, п_, f, s), язык, ДОПИСАТЬ, форма, п_,
                         {"s": к(язык, s), "f": f})
            a, b = с[f][1]
            дыры = {"a": к(язык, a), "b": к(язык, b), "f": f}
            for р in в2:
                положить(страница_замены(язык, ЗАМЕНА, "текст", р, f, a, b), язык, ЗАМЕНА, "текст", р, дыры)
            for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                положить(страница_замены(язык, ЗАМЕНА, "синоним·голый", р, f, a, b), язык, ЗАМЕНА, "синоним·голый", р, дыры)
            for форма in ("назв", "синоним", "впереди") + синонимы(язык, "замена")[1:] + ("страд",):
                положить(страница_замены(язык, ЗАМЕНА, форма, п_, f, a, b), язык, ЗАМЕНА, форма, п_, дыры)
        for я in ЯЗЫКИ_ПРОЕКТА:
            for было in ЗАПУСКИ_ДО[:2]:
                for р in в2:
                    положить(страница_прогона(язык, ТЕСТЫ, р, я, было), язык, ТЕСТЫ, "язык", р, {"Я": я})
                for р in СОСТАВНЫЕ_РЕГИСТРЫ:
                    положить(страница_прогона(язык, ТЕСТЫ, р, я, было, форма="синоним"), язык, ТЕСТЫ, "синоним", р,
                             {"Я": я})
                for форма in синонимы(язык, "тесты") + ("страд",):
                    положить(страница_прогона(язык, ТЕСТЫ, п_, я, было, форма=форма), язык, ТЕСТЫ, форма, п_, {"Я": я})
        for i, f in enumerate(ТЕКСТЫ[:4]):
            a = с[f][1][0]
            for вариант in ("назв", "второй"):
                вопрос_(НА_СТРОКЕ, вариант, вариант, {"f": f, "w": к(язык, a)}, f=f, w=a)
                n = 2 + i % (len(с[f][0]) - 1)
                вопрос_(СТРОКА_Н, вариант, вариант, {"f": f, "a": str(n)}, f=f, i=n - 1)
            вопрос_(В_КАКОМ, "второй", "второй", {"w": к(язык, a)}, w=a)
            c = РЕЧЬ[язык]["выбор"][i % 3]
            вопрос_(ВЫБОР, "назв", "назв", {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if i % 3 == 2 else i % 3))
        # «сколько строк» правится на основах, какие разводят источники (число строк — не файлы папки и не байты):
        # мера правленой формы та же, что у канонической
        def строк_разведено(f):
            меры = dict(мир_.lines(f)[1].меры)
            return list(меры.values()).count(меры["lines"]) == 1
        for f in [f for f in ТЕКСТЫ if строк_разведено(f)][:4]:
            for вариант in ("назв", "второй", "посчитай"):
                вопрос_(СТРОК, вариант, вариант, {"f": f}, f=f)
        for s, k_ in КЛЮЧИ[:4]:
            for вариант in ("назв", "второй"):
                вопрос_(КЛЮЧ, вариант, вариант, {"k": k_, "s": s}, s=s, k=k_)
        for w in ДВАЖДЫ[язык]:
            путь = поле(мир_.find(".", w)[1], "path")[0]
            вопрос_(РАЗ, "второй", "второй·папка", {"w": к(язык, w), "d": папка_пути(путь)}, w=w, d=папка_пути(путь))
        for d in ПАПКИ_СЧЁТА[:4]:
            вопрос_(ФАЙЛОВ, "второй", "второй", {"d": d}, d=d)
            for j in range(len(РЕЧЬ[язык]["q_посчитай"])):
                вопрос_(ФАЙЛОВ, f"посчитай·{j}", f"посчитай·{j}", {"d": d}, d=d)
        # ВВОДНОЕ «СЕЙЧАС» (перепись пар: у count их было 3–9 на язык, у de, it, pt — 2 группы из 9) — на всякой папке счёта
        for d in ПАПКИ_СЧЁТА:
            for вариант in ("сейчас", "второй·сейчас"):
                вопрос_(ФАЙЛОВ, вариант, вариант, {"d": d}, d=d)
        # СЕМЬИ ШИРЕ И СЕМЬИ КОНСТРУКЦИЙ (второй заказ ведущего): «в конце файла» — внутри, впереди и с «add»; перенос с
        # местом впереди — где язык его так ставит; третья форма вопроса о файле и о строке; «what does the first line
        # say», «what is written at the end», «read / show line N», значение без «ключа», «файл с именем» у вопроса о
        # ключе; план «…, затем скажи, сколько в нём строк»
        for f in ТЕКСТЫ[:4]:
            s = с[f][3]
            for форма in ("у_конца", "конец·впереди", "добавь_конец"):
                if форма == "у_конца" and "у_конца" not in T.КОНЕЦ[язык]:
                    continue
                положить(страница_дописать(язык, ДОПИСАТЬ, форма, п_, f, s), язык, ДОПИСАТЬ, форма, п_,
                         {"s": к(язык, s), "f": f})
        if язык in T.ВПЕРЕДИ_ПЕРЕНОС:
            for f, d in ПЕРЕНОСЫ[:4]:
                положить(страница_переноса(язык, ПЕРЕНОС, "впереди", п_, f, d), язык, ПЕРЕНОС, "впереди", п_,
                         {"f": f, "d": d})
        for i, f in enumerate(ТЕКСТЫ[:4]):
            a = с[f][1][0]
            вопрос_(В_КАКОМ, "третий", "третий", {"w": к(язык, a)}, w=a)
            вопрос_(НА_СТРОКЕ, "третий", "третий", {"f": f, "w": к(язык, a)}, f=f, w=a)
            c = РЕЧЬ[язык]["выбор"][i % 3]
            вопрос_(ВЫБОР, "второй", "второй", {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if i % 3 == 2 else i % 3))
            последний = РЕЧЬ[язык]["выбор"][2]
            # «что написано в конце файла» — конструкция, а не правка пары: слово выбора в вопросе не стоит, дыра — файл
            вопрос_(ВЫБОР, "конец", "в_конце", {"f": f}, f=f, c=последний, i=-1)
            n = 2 + i % (len(с[f][0]) - 1)
            for вариант in ("читай", "покажи", "выведи", "дай"):
                вопрос_(СТРОКА_Н, вариант, вариант, {"f": f, "a": str(n)}, f=f, i=n - 1)
            # ГЛАГОЛЫ ЧТЕНИЙ (наряд (d)): найди текст повелительно — на основах второй формы вопроса о файле
            for j in range(len(РЕЧЬ[язык]["q_ищи"])):
                вопрос_(В_КАКОМ, f"ищи·{j}", f"ищи·{j}", {"w": к(язык, a)}, w=a)
        for s_, k_ in КЛЮЧИ[:4]:
            вопрос_(КЛЮЧ, "без_ключа", "без_ключа", {"k": k_, "s": s_}, s=s_, k=k_)
            вопрос_(О_КЛЮЧЕ, "назв", "назв", {"k": k_, "s": s_}, s=s_, k=k_)
        # план «…, then tell me how many lines it has»: основы, где число строк не совпадает ни с файлами, ни с байтами
        def строк_разводит(путь, мир_после):
            меры = dict(мир_после.lines(путь)[1].меры)
            return list(меры.values()).count(меры["lines"]) == 1
        for план, пары in (("имя", МЕСТО_ИМЕНА), ("перенос", ПЕРЕНОСЫ), ("дописать", [(f, None) for f in ТЕКСТЫ])):
            взято = 0
            for f, x in пары:
                if план == "имя":
                    новый = (папка_пути(f) + "/" if папка_пути(f) else "") + x
                    мир_после = мир_.move(f, новый)[0]
                elif план == "перенос":
                    новый = f"{x}/{имя_пути(f)}"
                    мир_после = мир_.move(f, x)[0]
                else:
                    новый, мир_после = f, мир_.line(f, с[f][3])[0]
                if взято == 4 or not строк_разводит(новый, мир_после):
                    continue
                s = с[f][3] if план == "дописать" else None
                дыры = {"f": f, **({"g": x} if план == "имя" else {"d": x} if план == "перенос" else {"s": к(язык, s)})}
                положить(страница_места_строк(язык, план, f, x, s), язык, МЕСТО_СТРОК, план, п_, дыры)
                взято += 1
        # РОДЫ ЖИВЫХ ПРОСЬБ (третий заказ ведущего): на всякую форму и язык — четыре основы, первые из объявления
        # мира, какие разводят источники (правило дома `_разведено`); ряд основ идёт по кругу папок и файлов
        def четыре(род, форма, ряд, страница, дыры):
            взято = 0
            for x in ряд:
                if взято == 4:
                    break
                стр = страница(x)
                if _разведено(стр, язык, род):
                    положить(стр, язык, род, форма, п_, дыры(x))
                    взято += 1
            assert взято == 4, (язык, род, форма, взято)

        языки_проекта = tuple(ЯЗЫКИ_ПРОЕКТА)
        # ПЛАН ИЗ ТРЁХ АКТОВ: акт, дописать туда, куда его положил мир, затем «сколько строк» или прогон
        for вариант, ряд in (("создать", [(f, None, с[МЕСТО_СОСЕД[f]][3]) for f in МЕСТО_СОЗДАТЬ_ПУТИ]),
                             ("имя", [(f, g, с[f][3]) for f, g in МЕСТО_ИМЕНА]),
                             ("перенос", [(f, d, с[f][3]) for f, d in ПЕРЕНОСЫ]),
                             ("замена", [(f, с[f][1], с[f][3]) for f in ТЕКСТЫ])):
            ряд = [(i, *x) for i, x in enumerate(ряд)]
            четыре(ТРИ_АКТА, вариант, ряд,
                   lambda x, в=вариант: страница_трёх(язык, в, x[1], x[2], x[3], языки_проекта[x[0] % 2],
                                                      ЗАПУСКИ_ДО[x[0] % 3]),
                   lambda x, в=вариант: {"f": x[1], "s": к(язык, x[3]),
                                         **({"g": x[2]} if в == "имя" else {"d": x[2]} if в == "перенос" else
                                            {"a": к(язык, x[2][0]), "b": к(язык, x[2][1]),
                                             "Я": языки_проекта[x[0] % 2]} if в == "замена" else {})})
        # УСЛОВНЫЙ ПРИКАЗ: ветка «да» — на файлах и текстах, какие есть; «нет» — на путях, каких нет, и на тексте
        # чужого файла; условие впереди и после
        есть_ = [(f, с[f][3], *с[f][1]) for f in ТЕКСТЫ]
        нет_ = [(f, с[МЕСТО_СОСЕД[f]][3], None, None) for f in МЕСТО_СОЗДАТЬ_ПУТИ]
        чужие = [(f, с[f][3], с[ТЕКСТЫ[(i + 3) % len(ТЕКСТЫ)]][1][0], с[f][1][1]) for i, f in enumerate(ТЕКСТЫ)]
        for род, ряды in ((УСЛОВИЕ_ДОПИСАТЬ, (("да", есть_), ("нет", нет_))),
                          (УСЛОВИЕ_УДАЛИТЬ, (("да", есть_), ("нет", [(f, None, None, None) for f in СОЗДАТЬ_ПУТИ]))),
                          (УСЛОВИЕ_ЗАМЕНА, (("да", есть_), ("нет", чужие)))):
            for вид in ("если", "после"):
                for ветка, ряд in ряды:
                    форма = f"{вид}|{ветка}"
                    четыре(род, форма, ряд,
                           lambda x, р=род, ф=форма: страница_условия(язык, р, ф, x[0], s=x[1], a=x[2], b=x[3]),
                           lambda x, р=род: {"f": x[0],
                                             **({"s": к(язык, x[1])} if р == УСЛОВИЕ_ДОПИСАТЬ else {}),
                                             **({"a": к(язык, x[2]), "b": к(язык, x[3])} if р == УСЛОВИЕ_ЗАМЕНА
                                                else {})})
        # ВСЕ ФАЙЛЫ ПАПКИ, КРОМЕ НАЗВАННОГО: папки без подпапок в две записи и больше; названный файл идёт по кругу
        # записей, папка назначения переноса — следующая папка ряда
        папки_ = [d for d in ПАПКИ_СЧЁТА if len(поле(мир_.list(d)[1], "path")) >= 2
                  and not any(з.endswith("/") for з in поле(мир_.list(d)[1], "path"))]
        кроме_ = [(d, поле(мир_.list(d)[1], "path")[j % len(поле(мир_.list(d)[1], "path"))], папки_[(i + 1) % len(папки_)])
                  for j in range(3) for i, d in enumerate(папки_)]
        for акт in ("удалить", "перенести"):
            for форма in ("кроме", "не_трогай"):
                четыре(ВСЕ_КРОМЕ, f"{акт}·{форма}", кроме_,
                       lambda x, а=акт, ф=форма: страница_кроме(язык, а, ф, x[0], x[1], x[2] if а == "перенести" else None),
                       lambda x, а=акт: {"d": x[0], "n": x[1], **({"e": x[2]} if а == "перенести" else {})})
        # ДВА ОБЪЕКТА В ОДНОМ ПРИКАЗЕ и его пара — план из двух актов над теми же файлами
        пары_текстов = [(ТЕКСТЫ[i], ТЕКСТЫ[(i + k) % len(ТЕКСТЫ)]) for k in (4, 3, 5) for i in range(len(ТЕКСТЫ))]
        for акт, ряд in (("создать", [(СОЗДАТЬ_ПУТИ[2 * i], СОЗДАТЬ_ПУТИ[2 * i + 1], None) for i in range(4)]),
                         ("удалить", [(f, q, None) for f, q in пары_текстов]),
                         ("перенести", [(f, q, d) for f, q in пары_текстов
                                        for d in [x for x in ("home", "trips", "kitchen")
                                                  if x not in (папка_пути(f), папка_пути(q))][:1]]),
                         ("дописать", [(f, q, с[f][3]) for f, q in пары_текстов])):
            for форма in ("план", "и"):
                четыре(ДВА_ОБЪЕКТА, f"{акт}·{форма}", ряд,
                       lambda x, а=акт, ф=форма: страница_двух(язык, а, ф, x[0], x[1],
                                                                d=x[2] if а == "перенести" else None,
                                                                s=x[2] if а == "дописать" else None),
                       lambda x, а=акт: {"f": x[0], "q": x[1], **({"d": x[2]} if а == "перенести" else
                                                                   {"s": к(язык, x[2])} if а == "дописать" else {})})
        # ССЫЛКА НА ПРОШЛЫЙ ШАГ БЕЗ МЕСТОИМЕНИЯ — правка плана с местоимением на тех же основах
        for ссылка_ in ("этот", "тот_же"):
            for f in МЕСТО_СОЗДАТЬ_ПУТИ[:4]:
                s = с[МЕСТО_СОСЕД[f]][3]
                положить(страница_места_создать(язык, МЕСТО_СОЗДАТЬ, f, s, ссылка_), язык, МЕСТО_СОЗДАТЬ,
                         f"создать·{ссылка_}", п_, {"f": f, "s": к(язык, s)})
            for f, g in МЕСТО_ИМЕНА[:4]:
                положить(страница_места_имени(язык, МЕСТО_ИМЯ, f, g, с[f][3], ссылка_), язык, МЕСТО_ИМЯ,
                         f"имя·{ссылка_}", п_, {"f": f, "g": g, "s": к(язык, с[f][3])})
            for f, d in ПЕРЕНОСЫ[:4]:
                положить(страница_места_переноса(язык, МЕСТО_ПЕРЕНОС, f, d, ссылка_), язык, МЕСТО_ПЕРЕНОС,
                         f"перенос·{ссылка_}", п_, {"f": f, "d": d})
        for стр_, (я_, род_, форма_, р_) in list(вон.items()):
            if я_ == язык and род_ == МЕСТО_СТРОК and "·" not in форма_:
                д_ = перепись[стр_]
                x_ = д_.get("g", д_.get("d"))
                s_ = СОДЕРЖИМОЕ[язык][д_["f"]][3] if форма_ == "дописать" else None
                положить(страница_места_строк(язык, форма_, д_["f"], x_, s_, "этот"), язык, МЕСТО_СТРОК,
                         f"{форма_}·этот", п_, д_)
        # РОДЫ, КАКИХ ДОМ НЕ ПОКАЗЫВАЛ (наряд ведущего по переписи): вопрос «сколько тестов проходит» и план «прогони
        # тесты, затем скажи, сколько прошло» — на всяком языке проекта и всяком числе прогонов «до»; находка файла со
        # словом, затем «сколько в нём строк» — одно место (второй акт идёт) и несколько (второй акт ждёт одного)
        for род_ in (ТЕСТЫ_СКОЛЬКО, ПЛАН_ТЕСТЫ_СКОЛЬКО):
            for я in ЯЗЫКИ_ПРОЕКТА:
                for было in ЗАПУСКИ_ДО:
                    положить(страница_тестов_сколько(язык, род_, я, было), язык, род_, "язык", п_, {"Я": я})
        четыре(МЕСТО_НАЙТИ, "найти·строк", единственные_слова(язык),
               lambda x: страница_места_найти(язык, МЕСТО_НАЙТИ, x[1], None, "строк"), lambda x: {"w": к(язык, x[1])})
        for w in В_ДВУХ[язык] + В_ТРЁХ[язык]:
            положить(страница_места_найти(язык, МЕСТО_МНОГО, w, None, "строк"), язык, МЕСТО_МНОГО, "найти·строк", п_,
                     {"w": к(язык, w)})
        # ЗАЧИН И СВЯЗКА ВТОРОГО ВОПРОСА (27.09, наряд ведущего): план прогона — зачином вида 1, связкой «and» и
        # прямым вопросом за «;» на всяком языке проекта и числе прогонов «до»; план «акт, затем зачин и вопрос» —
        # первая строка там, куда акт положил файл, и файл со словом, какое во всём мире стоит лишь в этом файле
        # (`единственные_слова`: находка называет новое место файла); основы обоих видов зачина — одни
        for форма_ in ("зачин·1", "связка·и", "связка·прямо"):
            for я in ЯЗЫКИ_ПРОЕКТА:
                for было in ЗАПУСКИ_ДО:
                    положить(страница_тестов_сколько(язык, ПЛАН_ТЕСТЫ_СКОЛЬКО, я, было, форма_), язык,
                             ПЛАН_ТЕСТЫ_СКОЛЬКО, форма_, п_, {"Я": я})
        # «ФАЙЛ» («…, then let me know which file contains the word "x"») НЕ ПОКАЗЫВАЕТСЯ — ЦЕНА НАЗВАНА (мера 27.09 на
        # варке ствола с М-2049): хвост после зачина — вопрос, какой рамка ядра укладывает целым, и ядро берёт «, then
        # let me know» соперницей связки; там, где косвенный вопрос равен прямому (en, ru, pl), связка плана теряет
        # кворум — «then» 32 свидетеля против 24, «затем» 32 против 24, «potem» 24 против 24, — и планы этих голосов
        # не режутся. Дверь (`toolacts.ВОПРОС_ВТОРОЙ`), сборка и рамка суда готовы — до слова ведущего
        слово_ = dict(единственные_слова(язык))
        for план, ряд in (("имя", [(f, g, слово_.get(f)) for f, g in МЕСТО_ИМЕНА]),
                          ("перенос", [(f, d, слово_.get(f)) for f, d in ПЕРЕНОСЫ]),
                          ("дописать", [(f, с[f][3], None) for f in ТЕКСТЫ])):
            for второй_ in ("первая",):
                for вид in (0, 1):
                    четыре(ПЛАН_СКАЖИ, f"{план}·{второй_}·{вид}", [x for x in ряд if второй_ == "первая" or x[2]],
                           lambda x, пл=план, в=второй_, вд=вид: страница_плана_скажи(
                               язык, пл, в, вд, x[0], x[1], x[2] if в == "файл" else None),
                           lambda x, пл=план, в=второй_: {
                               "f": x[0], **({"g": x[1]} if пл == "имя" else {"d": x[1]} if пл == "перенос"
                                             else {"s": к(язык, x[1])}),
                               **({"w": к(язык, x[2])} if в == "файл" else {})})
        # МОДИФИКАТОРЫ ПРИКАЗА (27.09, наряд ведущего: контрастные пары «приказ со словом / без слова») — слово, какое
        # акт хранит («now», «just», «right now»: тот же ход мира, что у приказа без слова), и слово, какое его меняет
        # («later», «tomorrow»: организм акта не предлагает, мир читает «до», итог — отказ с причиной); у всякого
        # акта и слова — четыре основы канонической формы, ряд основ сдвинут на слово
        формы_ = варианты_переноса(язык)
        for исп, отк, форма_, ряд, страница, дыры in (
                (СОЗДАТЬ, СОЗДАТЬ_ОТКАЗ, "канон", СОЗДАТЬ_ПУТИ,
                 lambda р_, рг, x: страница_создать(язык, р_, "канон", рг, f=x), lambda x: {"f": x}),
                (УДАЛИТЬ, УДАЛИТЬ_ОТКАЗ, "канон", ТЕКСТЫ,
                 lambda р_, рг, x: страница_удалить(язык, р_, "канон", рг, f=x), lambda x: {"f": x}),
                (ПЕРЕНОС, ПЕРЕНОС_ОТКАЗ, формы_[0], ПЕРЕНОСЫ,
                 lambda р_, рг, x: страница_переноса(язык, р_, формы_[0], рг, *x), lambda x: {"f": x[0], "d": x[1]}),
                (ИМЯ, ИМЯ_ОТКАЗ, "канон", ИМЕНА,
                 lambda р_, рг, x: страница_имени(язык, р_, "канон", рг, *x), lambda x: {"f": x[0], "g": x[1]}),
                (ЗАМЕНА, ЗАМЕНА_ОТКАЗ, "текст", ТЕКСТЫ,
                 lambda р_, рг, x: страница_замены(язык, р_, "текст", рг, x, *с[x][1]),
                 lambda x: {"a": к(язык, с[x][1][0]), "b": к(язык, с[x][1][1]), "f": x}),
                (ДОПИСАТЬ, ДОПИСАТЬ_ОТКАЗ, "канон", ТЕКСТЫ,
                 lambda р_, рг, x: страница_дописать(язык, р_, "канон", рг, x, с[x][3]),
                 lambda x: {"s": к(язык, с[x][3]), "f": x}),
                (ТЕСТЫ, ТЕСТЫ_ОТКАЗ, "язык", [(я, было) for было in ЗАПУСКИ_ДО for я in ЯЗЫКИ_ПРОЕКТА],
                 lambda р_, рг, x: страница_прогона(язык, р_, рг, *x), lambda x: {"Я": x[0]})):
            for i, рг in enumerate(T.ХРАНИТЕЛИ + tuple(T.МЕНЯЮЩИЕ[язык])):
                р_ = исп if рг in T.ХРАНИТЕЛИ else отк
                основы = [x for x in ряд[i:] + ряд[:i]
                          if р_ == отк or _разведено(страница(р_, рг, x), язык, р_)][:4]
                assert len(основы) == 4, (язык, р_, рг, основы)
                for x in основы:
                    положить(страница(р_, рг, x), язык, р_, форма_, рг, дыры(x))
        # ВОПРОС О ПРОШЛОМ АКТЕ — «did you delete the file F?»: мир читает файл, какой есть, и имя, какого нет
        for форма_, ряд in (("есть", _кругом(ТЕКСТЫ, 2)), ("нет", list(НЕТ_ФАЙЛОВ) + list(СОЗДАТЬ_ПУТИ[:2]))):
            for f in ряд:
                положить(страница_прошлого(язык, форма_, f), язык, ПРОШЛОЕ, форма_, п_, {"f": f})
        # ПЛАН «ПРАВКА КОДА, ЗАТЕМ ПРОГОН» (27.09, наряд ведущего: у прогона оба исхода, иное число тестов, иные
        # millis и длина отчёта) — правка проекта одним актом мира (`ПРАВКИ_ПРОЕКТА`), затем прогон тестов того
        # проекта, чей код правка тронула: отчёт снят с проекта в этом состоянии. Второй крейт — полный прогон: у
        # отчёта несколько строк итога, дом их складывает
        for i, (акт, f, доводы) in enumerate(ПРАВКИ_ПРОЕКТА):
            я = next(я_ for я_, имя in ИМЕНА_ПРОГОНОВ.items() if f.startswith(КОД_ПРОГОНА[имя]))
            if акт == "replace":
                a, b = доводы
                положить(страница_плана_замены(язык, ПЛАН_ЗАМЕНА, f, a, b, я, ЗАПУСКИ_ДО[i % 3]), язык, ПЛАН_ЗАМЕНА,
                         "код", п_, {"a": к(язык, a), "b": к(язык, b), "f": f, "Я": я})
            else:
                (s,) = доводы
                положить(страница_плана_дописать(язык, ПЛАН_ДОПИСАТЬ, f, s, я, ЗАПУСКИ_ДО[i % 3]), язык,
                         ПЛАН_ДОПИСАТЬ, "код", п_, {"s": к(язык, s), "f": f, "Я": я})
        for я in КРЕЙТЫ:
            for было in ЗАПУСКИ_ДО:
                положить(страница_прогона(язык, ТЕСТЫ, п_, я, было), язык, ТЕСТЫ, "язык", п_, {"Я": я})
                for род_ in (ТЕСТЫ_СКОЛЬКО, ПЛАН_ТЕСТЫ_СКОЛЬКО):
                    положить(страница_тестов_сколько(язык, род_, я, было), язык, род_, "язык", п_, {"Я": я})
        # СЛОВАРЬ ЖИВЫХ ПРОСЬБ (27.09, наряд ведущего (d)): каталог — у актов папки и её счёта; имена репозитория — у
        # вопросов о всём дереве; единицы ключа и «посмотри значение», вхождения, число файлов и строк; перечень файлов
        # папки. Всякое слово — на четырёх основах своей канонической формы, пара — та же страница канонически
        for n, d in СОЗДАТЬ_В_ПАПКЕ[:4]:
            положить(страница_создать(язык, СОЗДАТЬ, "каталог", п_, n=n, d=d), язык, СОЗДАТЬ_ПАПКА, "каталог", п_,
                     {"n": n, "d": d})
        for n, d in УДАЛИТЬ_ИЗ_ПАПКИ[:4]:
            положить(страница_удалить(язык, УДАЛИТЬ, "каталог", п_, n=n, d=d), язык, УДАЛИТЬ_ПАПКА, "каталог", п_,
                     {"n": n, "d": d})
        for f, d in ПЕРЕНОСЫ[:4]:
            положить(страница_переноса(язык, ПЕРЕНОС, "каталог", п_, f, d), язык, ПЕРЕНОС, "каталог", п_,
                     {"f": f, "d": d})
        for d in ПАПКИ_СЧЁТА[:4]:
            for вариант in ("каталог", "число"):
                вопрос_(ФАЙЛОВ, вариант, вариант, {"d": d}, d=d)
        for f in [f for f in ТЕКСТЫ if строк_разведено(f)][:4]:
            вопрос_(СТРОК, "число", "число", {"f": f}, f=f)
        for f in ТЕКСТЫ[:4]:
            a = с[f][1][0]
            for j in range(1, len(РЕПО[язык])):
                вопрос_(В_КАКОМ, f"в_репо·{j}", f"в_репо·{j}", {"w": к(язык, a)}, w=a)
        for w in ДВАЖДЫ[язык]:
            for вариант in [f"репо·{j}" for j in range(1, len(РЕПО[язык]))] + ["вхождения"]:
                вопрос_(РАЗ, вариант, вариант, {"w": к(язык, w)}, w=w)
        for s_, k_ in КЛЮЧИ[:4]:
            for вариант in [f"ед·{j}" for j in range(len(РЕЧЬ[язык]["ключ_ед"]))] + ["найди"]:
                вопрос_(КЛЮЧ, вариант, вариант, {"k": k_, "s": s_}, s=s_, k=k_)
        for d in ПАПКИ_СЧЁТА:
            for вариант in ("список", "второй", "третий"):
                вопрос_(СПИСОК, вариант, вариант, {"d": d}, d=d)
        # ЗАЧИН ПЕРЕД ОДИНОЧНЫМ ВОПРОСОМ (27.09, наряд ведущего (e)): всякий вид зачина голоса и косвенный вопрос — на
        # основах второй формы вопроса (у «что файл говорит о ключе» второй формы нет — на основах его «назв»); пара —
        # прямой вопрос на тех же дырах
        for вид in range(len(T.ЗАЧИН[язык])):
            з = f"зачин·{вид}"
            for i, f in enumerate(ТЕКСТЫ[:4]):
                a = с[f][1][0]
                c = РЕЧЬ[язык]["выбор"][i % 3]
                n = 2 + i % (len(с[f][0]) - 1)
                вопрос_(В_КАКОМ, з, з, {"w": к(язык, a)}, w=a)
                вопрос_(НА_СТРОКЕ, з, з, {"f": f, "w": к(язык, a)}, f=f, w=a)
                вопрос_(ВЫБОР, з, з, {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if i % 3 == 2 else i % 3))
                вопрос_(СТРОКА_Н, з, з, {"f": f, "a": str(n)}, f=f, i=n - 1)
            for s_, k_ in КЛЮЧИ[:4]:
                вопрос_(КЛЮЧ, з, з, {"k": k_, "s": s_}, s=s_, k=k_)
                вопрос_(О_КЛЮЧЕ, з, з, {"k": k_, "s": s_}, s=s_, k=k_)
            for f in [f for f in ТЕКСТЫ if строк_разведено(f)][:4]:
                вопрос_(СТРОК, з, з, {"f": f}, f=f)
            for w in ДВАЖДЫ[язык]:
                путь = поле(мир_.find(".", w)[1], "path")[0]
                вопрос_(РАЗ, з, з, {"w": к(язык, w), "d": папка_пути(путь)}, w=w, d=папка_пути(путь))
            for d in ПАПКИ_СЧЁТА[:4]:
                вопрос_(ФАЙЛОВ, з, з, {"d": d}, d=d)
        # СОКРАЩЕНИЕ ГОЛОСА (27.09, наряд ведущего (g)): вопрос и хвост условия сокращением голоса («what's the first
        # line of the file F?», «where's the text "x"?», «… if it's there») — на основах той же формы полным словом;
        # голос без сокращений (`toolacts.СОКРАЩЕНИЯ`) форм не получает
        if T.СОКРАЩЕНИЯ.get(язык):
            for i, f in enumerate(ТЕКСТЫ[:4]):
                c, j = РЕЧЬ[язык]["выбор"][i % 3], (-1 if i % 3 == 2 else i % 3)
                n = 2 + i % (len(с[f][0]) - 1)
                for род_, база, форма_, дыры_, д_ in (
                        (ВЫБОР, 0, "сокр", {"f": f, "c": c.split()[-1]}, dict(f=f, c=c, i=j)),
                        (ВЫБОР, "конец", "конец·сокр", {"f": f}, dict(f=f, c=РЕЧЬ[язык]["выбор"][2], i=-1)),
                        (СТРОКА_Н, "второй", "второй·сокр", {"f": f, "a": str(n)}, dict(f=f, i=n - 1)),
                        (В_КАКОМ, "второй", "второй·сокр", {"w": к(язык, с[f][1][0])}, dict(w=с[f][1][0]))):
                    положить(сокращённо(язык, страница_вопроса(язык, род_, база, **д_)), язык, род_, форма_, п_, дыры_)
            for s_, k_ in КЛЮЧИ[:4]:
                for база, форма_ in ((0, "сокр"), ("без_ключа", "без_ключа·сокр")):
                    положить(сокращённо(язык, страница_вопроса(язык, КЛЮЧ, база, s=s_, k=k_)), язык, КЛЮЧ, форма_, п_,
                             {"k": k_, "s": s_})
            for ветка, ряд in (("да", есть_), ("нет", чужие)):
                форма_ = f"после·сокр|{ветка}"
                четыре(УСЛОВИЕ_ЗАМЕНА, форма_, ряд,
                       lambda x, ф=форма_: страница_условия(язык, УСЛОВИЕ_ЗАМЕНА, ф, x[0], a=x[2], b=x[3]),
                       lambda x: {"f": x[0], "a": к(язык, x[2]), "b": к(язык, x[3])})
        # ЛИТЕРАЛ В БЭКТИКАХ (27.09, наряд ведущего (g)): текст приказа и вопроса голым литералом в обёртке программиста
        # («replace `fresh bread` with `rye bread` in shopping.txt», «which file contains `a good book`?») — на основах
        # голой формы: пара — та же страница в кавычках голоса
        for i, f in enumerate(ТЕКСТЫ):
            a, b = с[f][1]
            if i % 2 == 0:
                положить(в_бэктиках(язык, страница_замены(язык, ЗАМЕНА, "голый", п_, f, a, b)), язык, ЗАМЕНА, "бэктик",
                         п_, {"a": к(язык, a), "b": к(язык, b), "f": f})
                положить(в_бэктиках(язык, страница_вопроса(язык, НА_СТРОКЕ, 1, f=f, w=a)), язык, НА_СТРОКЕ, "бэктик",
                         п_, {"f": f, "w": к(язык, a)})
            else:
                положить(в_бэктиках(язык, страница_дописать(язык, ДОПИСАТЬ, "голый", п_, f, с[f][3])), язык, ДОПИСАТЬ,
                         "бэктик", п_, {"s": к(язык, с[f][3]), "f": f})
                положить(в_бэктиках(язык, страница_вопроса(язык, В_КАКОМ, 1, w=a)), язык, В_КАКОМ, "бэктик", п_,
                         {"w": к(язык, a)})
        # ПЛАНЫ ЖИВЫХ ПРОСЬБ ШИРЕ (27.09, наряд ведущего (f)): «…, then tell me its line count» — на основах плана «…,
        # then let me know how many lines it has»; «into it» (глаголом акта и синонимом) — на основах ссылки «этот»;
        # «look for "x" and tell me which file it's in» — на основах второй формы вопроса о файле
        for стр_, (я_, род_, форма_, р_) in list(вон.items()):
            if я_ == язык and род_ == МЕСТО_СТРОК and "·" not in форма_ and р_ == п_:
                д_ = перепись[стр_]
                s_ = СОДЕРЖИМОЕ[язык][д_["f"]][3] if форма_ == "дописать" else None
                положить(страница_места_строк(язык, форма_, д_["f"], д_.get("g", д_.get("d")), s_, "число"), язык,
                         МЕСТО_СТРОК, f"{форма_}·число", п_, д_)
        for вид in [в for в in T.ССЫЛКА[язык] if в.startswith("в_него")]:
            for f in МЕСТО_СОЗДАТЬ_ПУТИ[:4]:
                s = с[МЕСТО_СОСЕД[f]][3]
                положить(страница_места_создать(язык, МЕСТО_СОЗДАТЬ, f, s, вид), язык, МЕСТО_СОЗДАТЬ,
                         f"создать·{вид}", п_, {"f": f, "s": к(язык, s)})
            for f, g in МЕСТО_ИМЕНА[:4]:
                положить(страница_места_имени(язык, МЕСТО_ИМЯ, f, g, с[f][3], вид), язык, МЕСТО_ИМЯ,
                         f"имя·{вид}", п_, {"f": f, "g": g, "s": к(язык, с[f][3])})
        for f in ТЕКСТЫ[:4]:
            a = с[f][1][0]
            for v in связки_находки(язык):
                вопрос_(В_КАКОМ, v, v, {"w": к(язык, a)}, w=a)
        # «AS ITS ONLY LINE» (слово ведущего): строка в новый файл — «…, then add "x" as its only line» и союзом «and»
        for f in МЕСТО_СОЗДАТЬ_ПУТИ[:4]:
            s = с[МЕСТО_СОСЕД[f]][3]
            стр_ = страница_места_создать(язык, МЕСТО_СОЗДАТЬ, f, s, "единственная")
            положить(стр_, язык, МЕСТО_СОЗДАТЬ, "создать·единственная", п_, {"f": f, "s": к(язык, s)})
            if союз_иной(язык):
                положить(союзом(язык, стр_), язык, МЕСТО_СОЗДАТЬ, "создать·единственная·союз", п_,
                         {"f": f, "s": к(язык, s)})
        # ДВА РАЗНЫХ АКТА (заказ руки joins2, к М-2090): всякая пара `ПАРЫ_АКТОВ` — на четырёх основах, какие разводят
        # источники; второй акт — над другим файлом (текст — по кругу от первого, новый файл — по кругу путей создания)
        # на мире после первого; союзом «and» их берёт блок `СОЮЗОМ` ниже
        for пара, ряд in (
                ("перенос+дописать", [(f, d, q, с[q][3]) for (f, d), q in zip(ПЕРЕНОСЫ, _кругом(ТЕКСТЫ, 3, 8))]),
                ("создать+удалить", [(f, None, q, None) for f, q in zip(СОЗДАТЬ_ПУТИ, _кругом(ТЕКСТЫ, 1, 8))]),
                ("дописать+замена", [(f, с[f][3], q, с[q][1]) for f, q in zip(ТЕКСТЫ, _кругом(ТЕКСТЫ, 5, 8))]),
                ("имя+дописать", [(f, g, q, с[q][3]) for (f, g), q in zip(ИМЕНА, _кругом(ТЕКСТЫ, 3, 8))]),
                ("удалить+создать", [(f, None, q, None) for f, q in zip(ТЕКСТЫ, _кругом(СОЗДАТЬ_ПУТИ, 2, 8))])):
            четыре(ДВА_АКТА, пара, ряд, lambda x, п=пара: страница_двух_актов(язык, п, *x),
                   lambda x, п=пара: _дыры_двух_актов(язык, п, *x))
        # СОЮЗ «AND» МЕЖДУ ДВУМЯ АКТАМИ (слово ведущего): четыре основы всякой пары актов `СОЮЗОМ`, какие разводят
        # источники, — та же страница союзом; там, где канон голоса говорит не «и»
        взято = collections.Counter()
        for стр_, (я_, род_, форма_, р_) in list(вон.items()):
            if я_ != язык or р_ != п_ or (род_, форма_) not in СОЮЗОМ or not союз_иной(язык):
                continue
            if взято[(род_, форма_)] == 4 or not _разведено(стр_, язык, род_):
                continue
            положить(союзом(язык, стр_), язык, род_, f"{форма_}·союз", п_, перепись[стр_])
            взято[(род_, форма_)] += 1
        assert not союз_иной(язык) or all(взято[к_] == 4 for к_ in СОЮЗОМ), (язык, взято)
        # НАРЯД (h1), 27.09 — три класса томографа ведущего на четырёх основах канона: неопределённый артикль
        # («create a file plan.md», «append a line "x" to the file F» — где голос артикль знает), конец файла голым
        # именем («append "x" to the end of F», «add the line "x" to the end of F»), счёт вхождений повелительно («count
        # the occurrences of the word "x" in the repository», «… in the folder D»)
        артикль_ = ("артикль",) if T.неопр(язык, "строку") is not None else ()
        for f in (СОЗДАТЬ_ПУТИ[:4] if артикль_ else ()):
            положить(страница_создать(язык, СОЗДАТЬ, "артикль", п_, f=f), язык, СОЗДАТЬ, "артикль", п_, {"f": f})
        for f in ТЕКСТЫ[:4]:
            s = с[f][3]
            for форма_ in артикль_ + ("конец·голый", "добавь_конец·голый"):
                положить(страница_дописать(язык, ДОПИСАТЬ, форма_, п_, f, s), язык, ДОПИСАТЬ, форма_, п_,
                         {"s": к(язык, s), "f": f})
        for w in ДВАЖДЫ[язык]:
            путь = поле(мир_.find(".", w)[1], "path")[0]
            for j in range(len(РЕЧЬ[язык]["q_посчитай_раз"])):
                вопрос_(РАЗ, f"счёт·{j}", f"счёт·{j}", {"w": к(язык, w)}, w=w)
                вопрос_(РАЗ, f"счёт·{j}", f"счёт·{j}·папка", {"w": к(язык, w), "d": папка_пути(путь)}, w=w,
                        d=папка_пути(путь))
        # ВОПРОСЫ О ТОМ ЖЕ АКТЕ (27.09, наряд ведущего (h2)): «do the Python tests pass?» — всякий язык проекта и
        # крейт и число прогонов «до»; «how many times does the word "x" occur in the file F?» — слово, какое стоит в
        # мире дважды, и всякий его файл: четыре основы, какие разводят источники (вхождений не столько, сколько строк
        # или файлов); повелительные формы вопроса о строке по выбору — на основах второй формы вопроса
        for я in (*ЯЗЫКИ_ПРОЕКТА, *КРЕЙТЫ):
            for было in ЗАПУСКИ_ДО:
                положить(страница_тестов_ли(язык, я, было), язык, ТЕСТЫ_ЛИ, "язык", п_, {"Я": я})
        четыре(РАЗ, "файл", [(w, п) for w in ДВАЖДЫ[язык] for п in dict.fromkeys(поле(мир_.find(".", w)[1], "path"))],
               lambda x: страница_вопроса(язык, РАЗ, 0, w=x[0], f=x[1]), lambda x: {"w": к(язык, x[0]), "f": x[1]})
        for вариант in ВЫБОР_ПОВЕЛИТЕЛЬНО:
            for i, f in enumerate(ТЕКСТЫ[:4]):
                c = РЕЧЬ[язык]["выбор"][i % 3]
                вопрос_(ВЫБОР, вариант, вариант, {"f": f, "c": c.split()[-1]}, f=f, c=c, i=(-1 if i % 3 == 2 else i % 3))
        # ЗАПИСЬ ПО ИМЕНИ (27.09, наряд ведущего (c); мир — М-2075 `locate`): «find the file F» и его пары — голым
        # файлом, «с именем», «where is …?» — на всяком имени, какое стоит однажды (четыре основы на форму, по кругу),
        # на именах нескольких записей и на именах, каких нет; «how many files are named F?» и «… now?» — на одной и
        # нескольких записях, у имени, какого нет, ответ — «нет»; «locate F» и «which folder holds F?» — так же
        найди = [(0, "канон"), (1, "голый"), ("назв", "назв"), ("второй", "второй"), ("второй·голый", "второй·голый"),
                 ("где_лежит", "где_лежит"), ("какая_папка", "какая_папка")]
        if РЕЧЬ[язык].get("q_найди_имя"):
            найди.append(("по_имени", "по_имени"))
        for f in ОДНО_ИМЯ:
            вопрос_(ГДЕ_ФАЙЛ, 0, "канон", {"f": f}, f=f)
        for i, (вариант, форма_) in enumerate(найди[1:]):
            for f in _кругом(ОДНО_ИМЯ, 3 * i):
                вопрос_(ГДЕ_ФАЙЛ, вариант, форма_, {"f": f}, f=f)
        for род_, имена_ in ((ГДЕ_ФАЙЛЫ, МНОГО_ИМЁН), (НЕТ_ФАЙЛА, НЕТ_ФАЙЛОВ)):
            for f in имена_:
                for вариант, форма_ in найди:
                    вопрос_(род_, вариант, форма_, {"f": f}, f=f)
        for род_, имена_ in ((ФАЙЛОВ_ИМЕНИ, _кругом(ОДНО_ИМЯ, 5, 6) + list(МНОГО_ИМЁН)), (НЕТ_ФАЙЛА, НЕТ_ФАЙЛОВ)):
            for f in имена_:
                for форма_ in ("сколько", "сколько·сейчас"):
                    вопрос_(род_, форма_, форма_, {"f": f}, f=f)
        # КОНСТРУКЦИИ ЗАПИСИ ПО ИМЕНИ (28.09, долг рода конструкций; М-2075): зачин всякого вида перед косвенным
        # вопросом о месте файла и о числе записей и «find the file F» регистрами вопроса и конструкциями — на четырёх
        # основах одной записи, на именах нескольких записей и на именах, каких нет
        for вид in range(len(T.ЗАЧИН[язык])):
            з = f"зачин·{вид}"
            for f in ОДНО_ИМЯ[:4]:
                вопрос_(ГДЕ_ФАЙЛ, з, з, {"f": f}, f=f)
            for род_, имена_ in ((ГДЕ_ФАЙЛЫ, МНОГО_ИМЁН), (НЕТ_ФАЙЛА, НЕТ_ФАЙЛОВ)):
                for f in имена_:
                    вопрос_(род_, з, з, {"f": f}, f=f)
            for f in _кругом(ОДНО_ИМЯ, 5, 4):
                вопрос_(ФАЙЛОВ_ИМЕНИ, з, з, {"f": f}, f=f)
        for р in НАЙДИ_РЕГИСТРЫ:
            в = f"найди·{р}"
            for f in ОДНО_ИМЯ[:4]:
                вопрос_(ГДЕ_ФАЙЛ, в, в, {"f": f}, f=f)
            for род_, имена_ in ((ГДЕ_ФАЙЛЫ, МНОГО_ИМЁН), (НЕТ_ФАЙЛА, НЕТ_ФАЙЛОВ)):
                for f in имена_:
                    вопрос_(род_, в, в, {"f": f}, f=f)
        # ИСХОДЫ ПРОГОНА (28.09, наряд ведущего omega-90): прогон одним приказом на проекте в состоянии, какое держит
        # мир, — всякий исход, какого прогон на объявленном проекте не показывал; прогонов «до» — всякое число, вежливой
        # просьбой — первое (пара одного акта мира — та же страница плоско)
        for я in ИМЕНА_ПРОГОНОВ:
            for правка_ in исходы_бегуна(я):
                мир_ = мир_состояния(язык, правка_)
                for было in ЗАПУСКИ_ДО:
                    положить(страница_прогона(язык, ИСХОДЫ, п_, я, было, мир_=мир_), язык, ИСХОДЫ, "язык", п_, {"Я": я})
                положить(страница_прогона(язык, ИСХОДЫ, в_, я, ЗАПУСКИ_ДО[0], мир_=мир_), язык, ИСХОДЫ, "язык", в_,
                         {"Я": я})
        # ПРОЧИТАТЬ (29.09): всякий текстовый файл и файлы проекта — канонически; голым путём и вежливой просьбой — по
        # четыре основы; файлы, каких нет, — отказ мира
        for f in ТЕКСТЫ + ("server.ini", "web/main.py", "tests/test_main.py", "tally/src/lib.rs"):
            положить(страница_прочитать(язык, ЧТЕНИЕ, "канон", п_, f), язык, ЧТЕНИЕ, "канон", п_, {"f": f})
        for f in ТЕКСТЫ[:4]:
            положить(страница_прочитать(язык, ЧТЕНИЕ, "голый", п_, f), язык, ЧТЕНИЕ, "голый", п_, {"f": f})
        for f in ТЕКСТЫ[4:]:
            положить(страница_прочитать(язык, ЧТЕНИЕ, "канон", в_, f), язык, ЧТЕНИЕ, "канон", в_, {"f": f})
        for f in НЕТ_ФАЙЛОВ:
            положить(страница_прочитать(язык, ЧТЕНИЕ_НЕТ, "канон", п_, f), язык, ЧТЕНИЕ_НЕТ, "канон", п_, {"f": f})
        # ПРОШЛЫЙ ПРОГОН (29.09): всякий прогон — запускался (запусков «до» по кругу) и не запускался (0)
        for i, я in enumerate(ИМЕНА_ПРОГОНОВ):
            положить(страница_прошлого_прогона(язык, "был", я, ЗАПУСКИ_ДО[i % len(ЗАПУСКИ_ДО)]), язык, ПРОШЛОЕ_ПРОГОН,
                     "был", п_, {"Я": я})
            положить(страница_прошлого_прогона(язык, "не_был", я, 0), язык, ПРОШЛОЕ_ПРОГОН, "не_был", п_, {"Я": я})
        # ВЕЖЛИВАЯ ПРОСЬБА ПЛАНОМ (перепись: у многоактных страниц пар «минус слова» не было): четыре основы всякой
        # канонической формы многоактного рода, какие разводят источники, — та же страница вежливой просьбой
        взято = collections.Counter()
        for стр_, (я_, род_, форма_, р_) in list(вон.items()):
            if я_ != язык or род_ not in МНОГОАКТНЫЕ or р_ != п_ or форма_ in ПЕРЕФРАЗ_ФОРМЫ:
                continue
            if взято[(род_, форма_)] == 4 or not _разведено(стр_, язык, род_):
                continue
            положить(вежливо(язык, стр_), язык, род_, форма_, в_, перепись[стр_])
            взято[(род_, форма_)] += 1
    return вон, перепись


# ======================================================================================================
# САМОПРОВЕРКИ: мир объявлен так, как дом о нём говорит; условия рынка М-2013 и разведение источников держатся
# ======================================================================================================
_НЕ_РЯДУ = re.compile(r'[.?!] +[^\W\d_]+ ?:| · ')     # строка хода мира: без «слово:» после фразы и без « · »
                                                          # (кавычки внутри значения ядро читает до закрывателя, М-2057)


def _самопроверка_мира():
    import frgram  # noqa: PLC0415 — французское сокращение не должно съесть имя пути
    for язык in ЯЗЫКИ:
        мир_ = папка(язык)
        for f in ТЕКСТЫ:
            строки_, (a, b), (w, v), s = СОДЕРЖИМОЕ[язык][f]
            assert 3 <= len(строки_) <= 6, (язык, f)
            _, ход_a = мир_.find(".", a)
            assert list(dict.fromkeys(поле(ход_a, "path"))) == [f] and мера(ход_a, "occurrences") == 1, (язык, f, a)
            assert мера(мир_.find(f, b)[1], "occurrences") == 0 and мера(мир_.find(f, v)[1], "occurrences") == 0, (язык, f)
            # слово замены стоит словом столько же раз, сколько подстрокой: «the word» не лжёт о находке мира
            assert мера(мир_.find(f, w)[1], "occurrences") == sum(с.split().count(w) for с in строки_) > 0, (язык, f, w)
            assert s not in строки_, (язык, f, s)
            for текст in строки_ + (a, b, w, v, s):
                assert not re.search(r"[\d.:?!«»„“”\"]", текст), (язык, f, текст)
        assert all(мера(мир_.find(".", a)[1], "files") == 0 for a in НЕТ_ТЕКСТА[язык]), язык
        for имя_, слова, файлов in (("ДВАЖДЫ", ДВАЖДЫ[язык], None), ("В_ДВУХ", В_ДВУХ[язык], 2),
                                    ("В_ТРЁХ", В_ТРЁХ[язык], 3)):
            for w in слова:
                ход_ = мир_.find(".", w)[1]
                целых = sum(с.split().count(w) for п in ПУТИ for с in мир_.файлы[п])
                assert целых == мера(ход_, "occurrences"), (язык, имя_, w)
                if файлов is None:
                    assert мера(ход_, "occurrences") not in (мера(ход_, "matches"), мера(ход_, "files")), (язык, w)
                else:
                    assert мера(ход_, "files") == файлов, (язык, имя_, w)
    # НЕОПРЕДЕЛЁННЫЙ АРТИКЛЬ (наряд (h1)): вариант с артиклем стоит дальше всякого номера, какой прежние циклы берут по
    # вариантам — у фразы файла номер фразы папки и «назв» (2), у строки — голая (1)
    for я in T.НЕОПР:
        assert T.неопр(я, "файл_вин") >= max(len(T.ОБЪЕКТЫ[я]["в_папке"]), 3) and T.неопр(я, "строку") >= 2, я
    # КОНЕЦ ФАЙЛА ГОЛЫМ ИМЕНЕМ (наряд (h1)): «append "x" to the end of F» говорит глаголом акта двери
    for я in ЯЗЫКИ:
        assert T.КОНЕЦ[я]["у_конца_голый"].split()[0] == T.РЕЧЬ[я]["дописать"][0].split()[0], я
    for f in СОЗДАТЬ_ПУТИ + НЕТ_ФАЙЛОВ:
        assert f not in ПУТИ, f
    # ЗАПИСЬ ПО ИМЕНИ: имя, какого нет, не стоит ни одной записью; имена одной и нескольких записей есть
    assert all(мера(папка("en").locate(".", f)[1], "entries") == 0 for f in НЕТ_ФАЙЛОВ), НЕТ_ФАЙЛОВ
    assert len(ОДНО_ИМЯ) >= 4 and len(МНОГО_ИМЁН) >= 2, (ОДНО_ИМЯ, МНОГО_ИМЁН)
    for n, d in СОЗДАТЬ_В_ПАПКЕ:
        assert f"{d}/{n}" not in ПУТИ, (n, d)
    for n, d in УДАЛИТЬ_ИЗ_ПАПКИ:
        assert f"{d}/{n}" in ПУТИ, (n, d)
    for f, d in ПЕРЕНОСЫ:
        assert f in ПУТИ and папка_пути(f) != d and any(п.startswith(d + "/") for п in ПУТИ), (f, d)
    for f, g in ИМЕНА:
        assert f in ПУТИ and (f"{папка_пути(f)}/{g}".lstrip("/") not in ПУТИ), (f, g)
    for f, g in ИМЕНА_ЗАНЯТЫ:
        assert f in ПУТИ and f"{папка_пути(f)}/{g}".lstrip("/") in ПУТИ, (f, g)
    for s, k_ in КЛЮЧИ:
        строки_ = [с for с in ПРОЕКТ[s] if с.split(" = ")[0] == k_]
        assert len(строки_) == 1 and строки_[0].split(" = ")[1].isdigit(), (s, k_)
    # ИМЕНА ДОМА НЕ ВСТРЕЧАЮТСЯ У СОСЕДЕЙ: суд дома узнаёт свою строку по имени её мира
    свои = set(ПУТИ) | set(СОЗДАТЬ_ПУТИ) | set(НЕТ_ФАЙЛОВ) | {g for _f, g in ИМЕНА + ИМЕНА_НЕТ} | {
        имя_пути(п) for п in ПУТИ}
    чужие = set(A.ФАЙЛЫ) | set(T.ТЕКСТЫ) | set(T.ТЕСТЫ) | set(T.НЕТ_ФАЙЛА) | {
        g for гг in T.НОВЫЕ_ИМЕНА.values() for g in гг}
    assert not свои & чужие, свои & чужие
    for имя in свои | {d for _f, d in ПЕРЕНОСЫ} | set(ПАПКИ_СЧЁТА):
        assert frgram.элизия(f"de {имя}") == f"de {имя}", имя
    # МЕСТОИМЕНИЕ ДЕРЖИТ ГЛАГОЛ АКТА: второй приказ с местоимением говорит тем же глаголом, что акт двери (М-2013, 4 —
    # у акта один глагол на язык); местоимение пристаёт к нему («ajoute-y», «elimínalo») — ударение не в счёт
    import unicodedata  # noqa: PLC0415

    def голый(x):
        return "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c))
    for язык in ЯЗЫКИ:
        м = T.МЕСТОИМЕНИЕ[язык]
        глаголы = dict(дописать=T.РЕЧЬ[язык]["дописать"][0].split()[0], удалить=A.ГЛАГОЛЫ[язык]["удалить"][0],
                       найти=T.РЕЧЬ[язык]["поиск"][0].split()[0], создать=A.ГЛАГОЛЫ[язык]["создать"][0],
                       заменить=T.РЕЧЬ[язык]["замена"][0].split()[0], перенести=T.РЕЧЬ[язык]["перенести"][0].split()[0])
        формы_ = [(м[акт][0], глаголы[акт]) for акт in ("дописать", "удалить", "найти", "создать", "заменить")]
        формы_.append((РЕЧЬ[язык]["q_найди"], глаголы["найти"]))      # «find the file F» — глагол поиска двери
        # ссылка «этот / тот же» и «все, кроме» говорят тем же глаголом, что акт двери
        формы_ += [(T.ССЫЛКА[язык][вид][акт][0], глаголы[акт]) for вид in T.ССЫЛКА[язык]
                   for акт in T.ССЫЛКА[язык][вид] if акт != "строк" and вид not in T.ССЫЛКА_СИНОНИМОМ]
        формы_ += [(T.КРОМЕ[язык][акт][к_], глаголы[акт]) for акт in T.КРОМЕ[язык] for к_ in ("imp", "не_трогай")]
        for форма, глагол in формы_:
            assert голый(форма).startswith(голый(глагол)), (язык, форма, глагол)
        # ССЫЛКА СИНОНИМОМ (слово ведущего к наряду (f)): приказ пользователя вправе сказать второй приказ синонимом акта —
        # глагол акта или первое слово формы из ряда двери синонимов (`toolacts.СИНОНИМЫ`); организм говорит канонически
        for вид in T.ССЫЛКА_СИНОНИМОМ & set(T.ССЫЛКА[язык]):
            for акт, (глагол_, _остаток) in T.ССЫЛКА[язык][вид].items():
                ряд = [глаголы[акт]] + [с.split()[0] for с in T.СИНОНИМЫ[язык][акт]]
                assert any(голый(глагол_).startswith(голый(г)) for г in ряд), (язык, вид, глагол_, ряд)
    # ПРОГОНЫ: отчёт бегуна снят и говорит числа, какие дом объявил кодом проекта; строки отчёта безопасны
    assert sorted(ПРОГОНЫ_СНЯТЫЕ) == sorted(ПРОГОНЫ), \
        f"снятые прогоны {sorted(ПРОГОНЫ_СНЯТЫЕ)} не те, что объявлены ({sorted(ПРОГОНЫ)}): семя {Р.СЕМЯ_ПРОГОНОВ}"
    assert set(ИМЕНА_ПРОГОНОВ.values()) == set(ПРОГОНЫ), (ИМЕНА_ПРОГОНОВ, ПРОГОНЫ)
    # всякий прогон на всяком состоянии проекта: отчёт снят; исход — по коду выхода; тестов в отчёте — столько,
    # сколько их в коде состояния (прогон, упавший раньше доктестов, до них не доходит — не больше)
    for состояние, проект in Р.состояния():
        for имя in ПРОГОНЫ:
            снятое = Р.снятое(имя, проект)
            строки_ = строки_итога(снятое)
            в_отчёте, упало = sum(п + у for п, у in строки_), sum(у for _п, у in строки_)
            # код 0 — ни одного упавшего и хоть один тест; прогон без тестов unittest кончает «NO TESTS RAN» не нулём
            пусто = в_отчёте == 0 and _НЕТ_ТЕСТОВ in снятое["report"]
            assert (упало == 0 and not пусто) == (снятое["exit"] == 0), (имя, состояние, строки_)
            assert в_отчёте == тестов(имя, проект) if упало == 0 else в_отчёте <= тестов(имя, проект), \
                (имя, состояние, в_отчёте, тестов(имя, проект))
            assert снятое["lines"] == len(снятое["report"]), (имя, состояние)
            assert not any(_НЕ_РЯДУ.search(с) for с in снятое["report"]), (имя, состояние)


_самопроверка_мира()


def _слова_органа(текст):
    """Слова, какими приказ режет орган: пробельные слова с обрезанными краевыми знаками."""
    return {с.strip(".,:;?!¿¡") for с in текст.split()}


def реплики(стр, язык):
    """[(роль, текст)] страницы: пользователь, организм, мир — по меткам двери хода."""
    роли = {A._реплика(язык, р, ""): р for р in ("польз", "орг", "мир")}
    образец = re.compile(r"(?:^|(?<=[.?!] ))(" + "|".join(re.escape(м) for м in роли) + ")")
    куски, прежний, роль = [], 0, None
    for м in образец.finditer(стр):
        if роль is not None:
            куски.append((роль, стр[прежний:м.start()].strip()))
        роль, прежний = роли[м.group(1)], м.end()
    куски.append((роль, стр[прежний:].strip()))
    return куски


def клетки(мир_):
    """Клетки хода мира: меры {имя: число}, строки [{поле: значение}], отказ — (почему, что)."""
    куски = мир_.rstrip(".").split(" · ")
    меры, строки_, отказ_ = {}, [], None
    for кусок in куски[1:]:
        имя, _, значение = кусок.partition(" ")
        if имя == "refused":
            отказ_ = значение
        elif имя in ("path", "line", "text"):
            if имя == "path" or not строки_:
                строки_.append({})
            строки_[-1][имя] = значение[1:-1] if имя == "text" else значение
        else:
            меры[имя] = int(значение)
    return меры, строки_, отказ_


_ЧИСЛО = re.compile(r"(?<![\w.])\d+(?!\w|\.\d)")      # число — не часть имени и не дробь («0.000s»)
_ЛЕДЖЕР = re.compile(r"\d+(?: [+−] \d+)* = (\d+)")


def _леджер_отчёта(леджер, в_текстах):
    """Леджер чисел отчёта («2 + 3 + 1 = 6» — сумма строк итога; «8 − 3 = 5» — прошедшие unittest): всякое число
    слева — число строки мира, счёт верен."""
    левая, итог_ = леджер.split(" = ")
    числа = [int(x) for x in re.findall(r"\d+", левая)]
    знаки = re.findall(r" ([+−]) ", левая)
    счёт = числа[0] + sum(x if з == "+" else -x for з, x in zip(знаки, числа[1:]))
    return all(x in в_текстах for x in числа) and счёт == int(итог_)


def источник(стр, язык, дыры):
    """Беды источника: всякое число итога — клетка хода мира перед ним (у леджера — его итог; у суммы строк отчёта —
    её слагаемые), либо дыра приказа; всякий текст в кавычках — дыра приказа или текст строки мира; числа внутри
    кавычек — слова текста, не числа итога."""
    беды = []
    о, з = T.КАВЫЧКИ[язык]
    части = реплики(стр, язык)
    приказ_ = части[0][1]
    for i, (роль, текст) in enumerate(части):
        if роль != "орг" or i == 0 or части[i - 1][0] != "мир":
            continue
        меры, строки_, _отказ = клетки(части[i - 1][1])
        числа_мира = set(меры.values()) | {int(с["line"]) for с in строки_ if "line" in с}
        в_текстах = {int(x) for с in строки_ for x in _ЧИСЛО.findall(с.get("text", ""))}
        вне = re.sub(re.escape(о) + ".+?" + re.escape(з), " ", текст)
        for м in _ЛЕДЖЕР.finditer(вне):
            if int(м.group(1)) not in числа_мира and not _леджер_отчёта(м.group(), в_текстах):
                беды.append(f"итог леджера не клетка мира: {м.group()}")
        без_леджеров = _ЛЕДЖЕР.sub(" ", вне)
        for x in _ЧИСЛО.findall(без_леджеров):
            if int(x) not in числа_мира | в_текстах and x not in _слова_органа(приказ_):
                беды.append(f"число {x} не клетка мира")
        for кусок in re.findall(re.escape(о) + "(.+?)" + re.escape(з), текст):
            if о + кусок + з not in T.в_кавычках(язык, приказ_) and not any(с.get("text") == кусок for с in строки_):
                беды.append(f"текст «{кусок}» ни дыра приказа, ни строка мира")
    return беды


def _разведено(стр, язык, род):
    """Страница разводит источники: число, какое итог взял у мира, не равно ни одной соперничающей клетке. У ответа
    номером строки соперницы — меры хода и единица; у значения ключа — меры и номера строк; у итога леджера — прочие
    меры; числа отчёта бегуна — не меры мира-процесса. Ответ текстом (строка, список файлов) разведён сам."""
    if род in (ВЫБОР, СТРОКА_Н, В_КАКИХ, НИГДЕ):
        return True
    о, з = T.КАВЫЧКИ[язык]
    части = реплики(стр, язык)
    приказ_ = части[0][1]
    for i, (роль, текст) in enumerate(части):
        if роль != "орг" or части[i - 1][0] != "мир":
            continue
        меры, строки_, _отказ = клетки(части[i - 1][1])
        вне = re.sub(re.escape(о) + ".+?" + re.escape(з), " ", текст)
        # сумма строк отчёта бегуна — не леджер меры: её итог не вправе совпасть ни с одной мерой хода
        в_текстах = {int(x) for с in строки_ for x in _ЧИСЛО.findall(с.get("text", ""))}
        отчёта = [м for м in _ЛЕДЖЕР.finditer(вне) if int(м.group(1)) not in меры.values()
                  and _леджер_отчёта(м.group(), в_текстах)]
        if any(int(м.group(1)) in меры.values() for м in отчёта):
            return False
        for м in отчёта:
            вне = вне.replace(м.group(), " ", 1)
        итоги = [int(м.group(1)) for м in _ЛЕДЖЕР.finditer(вне)]
        прочие = [int(x) for x in _ЧИСЛО.findall(_ЛЕДЖЕР.sub(" ", вне))
                  if x not in _слова_органа(приказ_) and int(x) not in итоги]
        if род in (В_КАКОМ, НА_СТРОКЕ):
            if any(x == 1 or x in меры.values() for x in прочие):
                return False
        elif род == КЛЮЧ:
            номера = {int(с["line"]) for с in строки_}
            if any(x in меры.values() or x in номера for x in прочие):
                return False
        else:
            if any(sum(1 for v in меры.values() if v == x) != 1 for x in итоги):
                return False
            if any(x in меры.values() for x in прочие):
                return False
    return True


# РАЗВЕДЕНИЕ ИСХОДА ПО СУДУ РЫНКА (28.09, трасса варки VRO): число, какое итог прогона берёт у отчёта бегуна, рынок исхода
# (М-2055) покупает местом по свидетелям и опровержениям — LAW²: свидетелей не меньше четырёх, LAW×: опровержений не меньше
# половины свидетелей, и клетка отвергнута. Клетка-соперница хода (runs, exit, millis, lines), совпавшая с числом итога на
# многих страницах формы, этот суд прошла бы и стала бы местом: «8 − 1 = 7» у одного упавшего — и exit 1 купил место
# числа упавших (12 страниц против 4). У всякой формы исхода (голос, числа итога знаком #) всякое число итога, какое меняется
# по страницам формы, совпадает с клеткой-соперницей меньше чем на четырёх страницах или расходится с ней хоть на половине
# совпадений. Число, одно на всех страницах формы (единица при счётном слове единственного числа: «1 error», «1 упал»),
# данными не разводится — клетка exit 1 совпадает с ним самой формой; её снимает ядро: М-2085 (клетка конца исхода — не
# его место), М-2084 (чтение, одно на всех страницах, не держит меняющегося места), М-2086 (из заполнимых исходов говорит
# тот, чей отчёт читает больше: «failures=4, errors=1» — форма провала с ошибкой, а не провала); самопроверка их считает
_СОПЕРНИЦЫ_ИСХОДА = ("runs", "exit", "millis", "lines")


def исходы_разведены():
    """Беды разведения чисел исхода прогона с клетками хода — по суду рынка (LAW², LAW×). Исход — предложения итога
    организма после хода «run» между предложением акта и наблюдением запусков (родов прогона одним приказом)."""
    счёт, значения = collections.defaultdict(lambda: [0, 0]), collections.defaultdict(set)
    for стр, (язык, род, _ф, _р) in ПОКАЗЫ.items():
        if род not in (ТЕСТЫ, ИСХОДЫ):
            continue
        части = реплики(стр, язык)
        for i, (роль, текст) in enumerate(части):
            if роль != "орг" or i == 0 or части[i - 1][0] != "мир" or not части[i - 1][1].startswith("run "):
                continue
            меры, _строки, _отказ = клетки(части[i - 1][1])
            исход_ = ". ".join(текст.split(". ")[1:-1])
            форма = (язык, _ЧИСЛО.sub("#", исход_))
            for j, x in enumerate(_ЧИСЛО.findall(исход_)):
                значения[(форма, j)].add(x)
                for имя in _СОПЕРНИЦЫ_ИСХОДА:
                    счёт[(форма, j, имя)][0 if int(x) == меры.get(имя) else 1] += 1
    return [f"число {j} исхода «{форма[1]}» ({форма[0]}) совпало с {имя} на {с} страницах, разошлось на {р}"
            for (форма, j, имя), (с, р) in счёт.items() if с >= 4 and с > 2 * р and len(значения[(форма, j)]) > 1]


def исходы_одним_числом():
    """[(голос, форма, место)] — числа исхода прогона, одни на всех страницах своей формы и равные клетке exit: их место
    данными не разводится — клетку конца исхода снимает ядро (М-2085); самопроверка печатает их счёт."""
    значения, exit_ = collections.defaultdict(set), collections.defaultdict(set)
    for стр, (язык, род, _ф, _р) in ПОКАЗЫ.items():
        if род not in (ТЕСТЫ, ИСХОДЫ):
            continue
        части = реплики(стр, язык)
        for i, (роль, текст) in enumerate(части):
            if роль != "орг" or i == 0 or части[i - 1][0] != "мир" or not части[i - 1][1].startswith("run "):
                continue
            исход_ = ". ".join(текст.split(". ")[1:-1])
            форма = (язык, _ЧИСЛО.sub("#", исход_))
            for j, x in enumerate(_ЧИСЛО.findall(исход_)):
                значения[(форма, j)].add(int(x))
                exit_[(форма, j)].add(клетки(части[i - 1][1])[0].get("exit"))
    return sorted((ф[0], ф[1], j) for (ф, j), в in значения.items() if len(в) == 1 and в == exit_[(ф, j)])


# ФОРМА ПРИКАЗА у отказа и невозможного — форма исполненного того же акта: отказ ложится в её рамку (М-2013, 5)
_ПОРЯДОК = {СОЗДАТЬ_ЕСТЬ: СОЗДАТЬ, СОЗДАТЬ_ОТКАЗ: СОЗДАТЬ, УДАЛИТЬ_НЕТ: УДАЛИТЬ, УДАЛИТЬ_ОТКАЗ: УДАЛИТЬ,
            ПЕРЕНОС_НЕТ: ПЕРЕНОС, ПЕРЕНОС_ОТКАЗ: ПЕРЕНОС, ИМЯ_ЗАНЯТО: ИМЯ, ИМЯ_НЕТ: ИМЯ, ИМЯ_ОТКАЗ: ИМЯ,
            ЗАМЕНА_НЕТ: ЗАМЕНА, ЗАМЕНА_ОТКАЗ: ЗАМЕНА, ДОПИСАТЬ_ОТКАЗ: ДОПИСАТЬ, ТЕСТЫ_ОТКАЗ: ТЕСТЫ, НИГДЕ: В_КАКОМ}
_ПОРЯДОК_ПО_ФОРМЕ = {(ПЛАН_ОТКАЗ, "замена"): ПЛАН_ЗАМЕНА, (ПЛАН_ОТКАЗ, "дописать"): ПЛАН_ДОПИСАТЬ,
                     (ПЛАН_ОТКАЗ, "перенос"): ПЛАН_ПЕРЕНОС, (МЕСТО_МНОГО, "найти"): МЕСТО_НАЙТИ,
                     (МЕСТО_МНОГО, "найти·строк"): МЕСТО_НАЙТИ,
                     **{(род, форма): исп for род in (МЕСТО_ОТКАЗ, МЕСТО_НЕВОЗМОЖНО)
                        for форма, исп in (("создать", МЕСТО_СОЗДАТЬ), ("имя", МЕСТО_ИМЯ), ("перенос", МЕСТО_ПЕРЕНОС))}}


# ЗАПИСЬ ПО ИМЕНИ (наряд (c)): имя нескольких записей и имя, какого нет, — формы той же находки; счёт имени, какого
# нет, — форма счёта
_ПОРЯДОК.update({ГДЕ_ФАЙЛЫ: ГДЕ_ФАЙЛ, НЕТ_ФАЙЛА: ГДЕ_ФАЙЛ})
_ПОРЯДОК.update({ЧТЕНИЕ_НЕТ: ЧТЕНИЕ})
_ПОРЯДОК_ПО_ФОРМЕ.update({(НЕТ_ФАЙЛА, "сколько"): ФАЙЛОВ_ИМЕНИ, (НЕТ_ФАЙЛА, "сколько·сейчас"): ФАЙЛОВ_ИМЕНИ})


def форма_приказа(род, форма):
    """Род, чья форма приказа у страницы: исполненный акт для отказа и невозможного, сам род — для прочих."""
    return _ПОРЯДОК_ПО_ФОРМЕ.get((род, форма), _ПОРЯДОК.get(род, род))


def _взял_мир(язык, знач, части):
    """Дыра взята ходом мира: её значение стоит в ходе (текст — без кавычек страницы). У условного приказа итог
    называет дыры проверки и исполненной ветки; дыру другой ветки мир не брал, и итог её не называет."""
    о, з = T.КАВЫЧКИ[язык]
    голое = знач[len(о):-len(з)] if знач.startswith(о) and знач.endswith(з) else знач
    return any(голое in текст for роль, текст in части if роль == "мир")


def _в_падеже(язык, знач, приказ_):
    """Дыра слова выбора в падеже приказа (наряд (h2)): «покажи последнюю строку файла F» несёт слово ряда «выбор_в»
    того же места в ряду, что слово дыры в ряду «выбор» (его называет итог: «последняя строка файла F гласит …»)."""
    слова_, р = _слова_органа(приказ_), РЕЧЬ[язык]
    return any(в.split()[-1] == знач and в_.split()[-1] in слова_ for в, в_ in zip(р["выбор"], р["выбор_в"]))


def условия_рынка():
    """Условия М-2013 и коллегии по показам: (беды, счёт форм). Итог называет всякую дыру; у всякой формы и языка —
    пара исполненных страниц с разными наполнителями; исполненных больше, чем отказов той же формы; числа и тексты
    итога — клетки хода мира; не меньше четырёх страниц формы разводят источники; слово выбора — не меньше четырёх
    страниц на файлах в две строки и больше."""
    беды = []
    исполненные, отказы, прочие, разведено = {}, {}, {}, {}
    for стр, (язык, род, форма, регистр) in ПОКАЗЫ.items():
        дыры = ПЕРЕПИСЬ[стр]
        части = реплики(стр, язык)
        приказ_ = части[0][1]
        for имя, знач in дыры.items():
            if знач.startswith(T.КАВЫЧКИ[язык][0]):
                # литерал в обёртке программиста — та же дыра, что текст в кавычках голоса (наряд (g))
                if знач not in T.в_кавычках(язык, приказ_):
                    беды.append(f"дыра {имя} не в приказе: {стр[:120]}")
            elif знач not in _слова_органа(приказ_) and not _в_падеже(язык, знач, приказ_):
                беды.append(f"дыра {имя} не слово приказа: {стр[:120]}")
        беды.extend(f"{б}: {стр[:140]}" for б in источник(стр, язык, дыры))
        for роль, текст in части:
            if роль == "мир":
                for с in клетки(текст)[1]:
                    if _НЕ_РЯДУ.search(с.get("text", "")):
                        беды.append(f"строка мира небезопасна: {с.get('text')}")
        ключ = (язык, форма_приказа(род, форма), форма, регистр)
        if род in ОТКАЗЫ:
            отказы.setdefault(ключ, []).append(дыры)
            continue
        if род in НЕВОЗМОЖНЫЕ:
            прочие.setdefault(ключ, []).append(дыры)
            continue
        # итог — всё, что организм сказал после первого хода мира (у плана — отчёты обоих актов)
        первый_мир = next(i for i, (роль, _т) in enumerate(части) if роль == "мир")
        итог = " ".join(текст for роль, текст in части[первый_мир:] if роль == "орг")
        for имя, знач in дыры.items():
            есть = знач in итог if знач.startswith(T.КАВЫЧКИ[язык][0]) else знач in _слова_органа(итог)
            if not есть and not (род in УСЛОВНЫЕ and not _взял_мир(язык, знач, части)):
                беды.append(f"итог не называет дыру {имя}={знач}: {стр[:140]}")
        исполненные.setdefault(ключ, []).append(дыры)
        разведено[ключ] = разведено.get(ключ, 0) + _разведено(стр, язык, род)
    for ключ, члены in исполненные.items():
        if not any(all(x[и] != y[и] for и in x) for i, x in enumerate(члены) for y in члены[i + 1:]):
            беды.append(f"нет пары с разными наполнителями: {ключ} ({len(члены)} стр.)")
        if разведено[ключ] < 4:
            беды.append(f"разводят источники лишь {разведено[ключ]} стр. из {len(члены)}: {ключ}")
    def рамка(ключ):
        """Рамка исполненных для отказа: та же форма того же регистра; у приказа на потом — тот же приказ без слова
        (пара «приказ со словом / без слова»)."""
        return (*ключ[:3], "плоский") if ключ[3] in T.МЕНЯЮЩИЕ[ключ[0]] else ключ
    for ключ in list(отказы) + list(прочие):
        if len(исполненные.get(рамка(ключ), ())) < 2:
            беды.append(f"отказ или невозможное без рамки исполненных: {ключ}")
    for ключ, члены in отказы.items():
        if len(исполненные.get(рамка(ключ), ())) <= len(члены):
            беды.append(f"отказов не меньше исполненных: {ключ}")
    for язык in ЯЗЫКИ:
        # находка в одном месте (второй акт идёт) — чаще, чем в нескольких (второй акт ждёт): отказ ложится в рамку
        # исполненного, как у отказа пользователем (М-2013, 5)
        по_роду = {р: sum(1 for я, род, _ф_, _р_ in ПОКАЗЫ.values() if я == язык and род == р)
                   for р in (МЕСТО_НАЙТИ, МЕСТО_МНОГО)}
        if по_роду[МЕСТО_НАЙТИ] <= по_роду[МЕСТО_МНОГО]:
            беды.append(f"находок в одном месте не больше, чем в нескольких ({язык}): {по_роду}")
        for c in РЕЧЬ[язык]["выбор"]:
            n = sum(1 for стр, (я, род, _ф_, _р_) in ПОКАЗЫ.items()
                    if я == язык and род == ВЫБОР and ПЕРЕПИСЬ[стр].get("c") == c.split()[-1]
                    and len(СОДЕРЖИМОЕ[язык].get(ПЕРЕПИСЬ[стр]["f"], ((),))[0]) >= 2)
            if n < 4:
                беды.append(f"слово выбора «{c}» ({язык}): {n} стр.")
    for акт in ("создать", "удалить"):
        приказ_в, _инф, отчёт_в = A.ГЛАГОЛЫ["en"][акт]
        assert приказ_в != отчёт_в, акт
    for акт in ("замена", "дописать", "переименовать", "перенести", "тесты"):
        imp, _inf, past = T.РЕЧЬ["en"][акт][:3]
        assert imp.split()[0] != past.split()[0], акт
    return беды, len(исполненные)


# СЕМЬИ ПЕРЕФРАЗА: правленая форма → её семья; регистры (вежливый и голый — прежние семьи «please» и «F без the
# file»)
ПЕРЕФРАЗ_ФОРМЫ = {"назв": "назв", "2·0": "назв", "синоним": "синоним", "впереди·0": "впереди", "впереди": "впереди",
                  "конец": "конец", "второй": "второй", "второй·папка": "второй", "голый": "голый",
                  "у_конца": "конец", "конец·впереди": "впереди", "добавь_конец": "синоним", "третий": "второй",
                  "читай": "второй", "покажи": "второй", "без_ключа": "без_ключа",
                  "после|да": "условие_после", "после|нет": "условие_после", "сейчас": "вводное",
                  "второй·сейчас": "вводное", "зачин·1": "зачин", "связка·и": "связка", "связка·прямо": "связка",
                  **{f"{план}·{в}·1": "зачин" for план in ("имя", "перенос", "дописать") for в in ("первая", "файл")},
                  **{f"{акт}·не_трогай": "не_трогай" for акт in ("удалить", "перенести")},
                  **{f"{акт}·и": "и" for акт in ("создать", "удалить", "перенести", "дописать")},
                  **{f"{план}·{с}": "ссылка" for план in ("создать", "имя", "перенос", "дописать")
                     for с in ("этот", "тот_же")}}
# ГЛАГОЛЫ АКТА И ЧТЕНИЙ (наряд (d)): второй и дальние синонимы, повелительные формы чтений — семья «синоним»
ПЕРЕФРАЗ_ФОРМЫ.update({"выведи": "синоним", "дай": "синоним", "посчитай": "синоним",
                       **{f"синоним·{i}": "синоним" for i in range(1, 5)}, **{f"ищи·{i}": "синоним" for i in range(4)},
                       **{f"посчитай·{i}": "синоним" for i in range(2)}})
# СЛОВАРЬ ЖИВЫХ ПРОСЬБ (наряд (d)): имя места, единица, «посмотри значение» — семья «синоним»
ПЕРЕФРАЗ_ФОРМЫ.update({"каталог": "синоним", "число": "синоним", "вхождения": "синоним", "найди": "синоним",
                       **{f"в_репо·{i}": "синоним" for i in range(1, 4)}, **{f"репо·{i}": "синоним" for i in range(1, 4)},
                       **{f"ед·{i}": "синоним" for i in range(3)}})
# ЗАЧИН ПЕРЕД ОДИНОЧНЫМ ВОПРОСОМ (наряд (e)): всякий вид зачина голоса — семья «зачин»
ПЕРЕФРАЗ_ФОРМЫ.update({f"зачин·{i}": "зачин" for i in range(max(len(в) for в in T.ЗАЧИН.values()))})
# СОКРАЩЕНИЕ ГОЛОСА (наряд (g)): вопрос и хвост условия сокращением голоса — семья «сокращение»: правка письма (два
# слова одним), а не второй оборот вопроса; пара — полная форма тех же дыр
ПЕРЕФРАЗ_ФОРМЫ.update({ф: "сокращение" for ф in ("сокр", "конец·сокр", "второй·сокр", "без_ключа·сокр", "после·сокр|да",
                                                 "после·сокр|нет")})
# ЛИТЕРАЛ В БЭКТИКАХ (наряд (g)): голая форма с литералом в обёртке программиста — семья «литерал»
ПЕРЕФРАЗ_ФОРМЫ.update({"бэктик": "литерал"})
# ПЛАНЫ ЖИВЫХ ПРОСЬБ ШИРЕ (наряд (f)): «its line count» — слово единицы (семья «синоним», как «число» вопроса); «into
# it» глаголом акта и синонимом — ссылка на несомый файл (семья «ссылка», слово ведущего); «as its only line» —
# «синоним»; «найди и скажи, в каком файле» и союз «and» между актами — связка (семья «связка»)
ПЕРЕФРАЗ_ФОРМЫ.update({**{f"{план}·число": "синоним" for план in ("имя", "перенос", "дописать")},
                       **{f"{план}·{вид}": "ссылка" for план in ("создать", "имя")
                          for вид in ("в_него", "в_него·1", "в_него·2")},
                       "создать·единственная": "синоним", "создать·единственная·союз": "связка",
                       **{f"{форма}·союз": "связка" for _род, форма in СОЮЗОМ},
                       **{v: "связка" for я in ЯЗЫКИ for v in связки_находки(я)}})
# НАРЯД (h1): артикль — своя семья (слово при объекте, не глагол и не место); конец файла голым именем — семья «конец»,
# с «add» — «синоним», как «добавь_конец»; счёт вхождений повелительно — «синоним»
ПЕРЕФРАЗ_ФОРМЫ.update({"артикль": "артикль", "конец·голый": "конец", "добавь_конец·голый": "синоним",
                       **{f"счёт·{j}{м}": "синоним" for j in range(2) for м in ("", "·папка")}})
# ПОВЕЛИТЕЛЬНОЕ СЛОВО ВЫБОРА (наряд (h2)): повелительные формы вопроса о строке по выбору — семья «второй» (как «read /
# show line N»)
ПЕРЕФРАЗ_ФОРМЫ.update({v: "второй" for v in ВЫБОР_ПОВЕЛИТЕЛЬНО})
# СТРАДАТЕЛЬНЫЙ ОБОРОТ (наряд 28.09, классы H2): приказ без повеления — семья «конструкция»
ПЕРЕФРАЗ_ФОРМЫ.update({"страд": "конструкция", "синоним·голый": "синоним"})
# «find the file F» регистром вопроса или конструкции — семья «конструкция» (долг рода, М-2075)
ПЕРЕФРАЗ_ФОРМЫ.update({f"найди·{р}": "конструкция" for р in НАЙДИ_РЕГИСТРЫ})
# ЗАПИСЬ ПО ИМЕНИ (наряд (c)): «where is F?» голым файлом — семья «голый»; «find the file named F» — «назв»; «… now?»
# — вводное; «locate F» — синоним глагола; «which folder holds F?» — второй оборот вопроса
ПЕРЕФРАЗ_ФОРМЫ.update({"второй·голый": "голый", "по_имени": "назв", "сколько·сейчас": "вводное", "где_лежит": "синоним",
                       "какая_папка": "второй"})
ПЕРЕФРАЗ_РЕГИСТРЫ = frozenset({"вежливый", "вопросом", "вопросом2", "вопросом3", *T.ХРАНИТЕЛИ, *КОНСТРУКЦИИ})
# ПОКАЗЫ строятся после правила разведения источников и таблицы семей правок: основы новых родов отбирает `_разведено`
# дома, каноническую форму многоактного рода — таблица правок
ПОКАЗЫ, ПЕРЕПИСЬ = _показы()


def _ходы_мира(стр, язык):
    return tuple(текст for роль, текст in реплики(стр, язык) if роль == "мир")


def пары_перефраза():
    """(беды, семьи): у всякой правленой страницы есть каноническая пара — те же язык, род и дыры, тот же ход мира
    байт в байт (свидетель правки — пара одного акта мира); семья → виды актов мира, на каких она стоит (рынок правок
    берёт правку при двух видах и больше)."""
    основы = {}
    for стр, (я, род, форма, р) in ПОКАЗЫ.items():
        if форма not in ПЕРЕФРАЗ_ФОРМЫ and р not in ПЕРЕФРАЗ_РЕГИСТРЫ:
            основы.setdefault((я, род, tuple(sorted(ПЕРЕПИСЬ[стр].items()))), set()).add(_ходы_мира(стр, я))
    беды, семьи = [], {}
    for стр, (я, род, форма, р) in ПОКАЗЫ.items():
        семья = р if р in ПЕРЕФРАЗ_РЕГИСТРЫ else ПЕРЕФРАЗ_ФОРМЫ.get(форма)
        if семья is None or род in ОТКАЗЫ or род in НЕВОЗМОЖНЫЕ:
            continue
        ходы = _ходы_мира(стр, я)
        if ходы not in основы.get((я, род, tuple(sorted(ПЕРЕПИСЬ[стр].items()))), ()):
            беды.append(f"правка без пары одного акта мира: {стр[:140]}")
        семьи.setdefault(семья, set()).add(ходы[0].split()[0])
    return беды, семьи


def _самопроверка():
    import asking  # noqa: PLC0415 — дом пары объявляет зачины вопросов
    по_роду = {}
    for стр, (язык, род, _ф_, _р_) in ПОКАЗЫ.items():
        по_роду.setdefault(род, set()).add(язык)
        вопрос_ = реплики(стр, язык)[0][1].rsplit("; ", 1)[-1]     # «act; question?» — вопрос за «;»
        if вопрос_.endswith("?") and asking.зачин_объявлен(вопрос_) is False:
            raise AssertionError(f"незачинный вопрос: {язык} · {вопрос_}")
    пустые = [р for р in РОДЫ if по_роду.get(р) != set(ЯЗЫКИ)]
    assert not пустые, f"род не кован на всех языках: {пустые}"
    беды, форм = условия_рынка()
    for б in беды[:12]:
        print("  М-2013:", б)
    assert not беды, f"условий рынка нарушено {len(беды)}"
    беды = исходы_разведены()
    for б in беды[:12]:
        print("  ИСХОД:", б)
    assert not беды, f"чисел исхода, не разведённых с клетками хода, {len(беды)}"
    стена = исходы_одним_числом()
    print(f"  исход — число, одно на всех страницах формы и равное exit (клетку конца снимает ядро, М-2085): {len(стена)} мест "
          f"в {len({(я, ф) for я, ф, _j in стена})} формах")
    беды, семьи = пары_перефраза()
    for б in беды[:12]:
        print("  ПАРА:", б)
    assert not беды, f"правок без пары одного акта мира {len(беды)}"
    print("  семьи перефраза — виды актов мира: "
          + "; ".join(f"{с} {len(в)} ({', '.join(sorted(в))})" for с, в in sorted(семьи.items())))
    for язык in ("en", "ru", "de"):
        for образец in (ВЫБОР, ТЕСТЫ, ПЛАН_ПЕРЕНОС, МЕСТО_ИМЯ, МЕСТО_МНОГО):
            стр = next(с for с, (я, род, _ф_, р) in ПОКАЗЫ.items() if я == язык and род == образец and р == "плоский")
            print("  ", стр[:600])
    сч = {р: sum(1 for _я, род, _ф_, _р_ in ПОКАЗЫ.values() if род == р) for р in РОДЫ}
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}, форм на языках {форм}): "
          + ", ".join(f"{р} {к_}" for р, к_ in сч.items()))


if __name__ == "__main__":
    _самопроверка()
