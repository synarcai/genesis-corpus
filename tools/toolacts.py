#!/usr/bin/env python3
"""ДОМ АКТОВ ИНСТРУМЕНТОВ — руки агента: найти, заменить, дописать, переименовать, перенести, прогнать
тесты, план из нескольких актов (25.09, наряд ведущего по слову владельца: ozar — промышленная
альтернатива Claude Code / Gemini / Qwen на своей архитектуре; свод — школа этого продукта).

Дом `actturn` показал ход тела в мире: приказ, предложение с вопросом, слово пользователя, отчёт с
ПЕРЕСЧЁТОМ леджера — над папкой и байтами файла (создать, удалить, прочитать, дописать) и над запусками
объявленных процессов. Продукту нужны руки шире: найти слово или строки в файле, заменить текст,
дописать ПОКАЗАННУЮ строку (орган ядра `ozar-core/src/act.rs` отказывает дописыванию, «чьего содержимого
дом ещё не показал»), переименовать и перенести, прогнать тесты и прочесть исход (прошло сколько из
скольких, успех или ошибка), план из нескольких актов («найди, затем замени, затем проверь»; «прогони
тесты и выпускай, лишь если прошли все») — на девяти языках, с приказами разной вежливости и
косвенности.

ОДНА ДВЕРЬ НА ПОНЯТИЕ: протокол хода — у `actturn`, и дом берёт его оттуда, а не пишет вторую копию:
роли реплик, пару «да/нет», отказ «подтверждения нет — акт не совершён», вопрос предложения
(«is that confirmed?» — по нему рынок `buy_act_frames` пулит слова подтверждения, М-504), фразу папки и
её счётное слово, фразы «уже есть» и «нет», запуски мира (`РЕЧЬ_ЗАПУСКА`), леджер `леджер(было, сдвиг)`.
Здесь объявлено только новое: акты, их три ступени, фразы новых леджеров и сам мир.

ВСЯКОЕ ЧИСЛО — МИРА (М-500): мир объявлен ЗДЕСЬ — три текстовых файла с содержимым на каждом языке,
три файла тестов с числом тестов и падений, папка `archive`, — и всякое число отчёта ВЫЧИСЛЕНО из него:
сколько раз слово стоит в файле (по словам строки), в каких строках, сколько строк после дописанной,
сколько файлов после переноса, сколько тестов прошло. Имена файлов одни на всех языках нарочно (как
a.txt у `actturn`): дом учит АКТУ, а не именованию.

ФОРМА — ТА, ЧТО ПОКУПАЕТ РЫНОК АКТОВ: страница — одна строка реплик двух меток; ход в четыре реплики
(приказ без числа · предложение, чья последняя фраза спрашивает · одно слово · отчёт, последняя фраза
которого — наблюдение с числами «было ± шаг = стало»); невозможный акт — две реплики (приказ · отказ мира
с наблюдением); вопрос — вопрос и наблюдение. Леджер последней фразы движется у одного акта всегда одинаково:
замена растит счёт нового слова, дописывание — строки файла, перенос — файлы папки archive, прогон тестов —
запуски мира; исход прогона (сколько прошло, успех или ошибка) сказан фразой ПЕРЕД наблюдением.

ЧЕТЫРЕ РЕГИСТРА ПРИКАЗА: прямой («замени …»), вежливый («пожалуйста, замени …»), косвенный («нужно
заменить …» — нужда без повеления), вопросом («ты можешь заменить …?»). Предложение тела называет акт
одинаково при всех четырёх: косвенный приказ толкуется предложением, и «да» подтверждает названное.

ЧЕГО ДОМ НЕ МЕРИТ, НАЗВАНО: рынок актов покупает ОДНУ дыру объекта, а у замены их три (слово, замена,
файл), у переименования две; приказ вопросом рынок актов не читает приказом (порядок `!order.asks`); план
есть рамка одного приказа, а не цепь актов. Это долг читателя, названный ведущему переписью форм, а не
причина писать продукт уже, чем он есть.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actturn as A  # noqa: E402 — дверь хода: роли, да/нет, отказ, вопрос предложения, папка, запуски, леджер
import frgram  # noqa: E402 — французская элизия после подстановки («je propose d'ajouter»)
import rugram  # noqa: E402 — русская форма «раз» при числе
import svampforms as S  # noqa: E402 — счётная ячейка пакета

ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# МИР: папка из шести файлов — три текстовых и три тестовых; содержимое текстовых — на языке страницы
# ======================================================================================================
ТЕКСТЫ = ("notes.md", "todo.txt", "readme.md")
# ТЕСТЫ: файл → (тестов, падает) — исход прогона объявлен миром и один при всяком прогоне
ТЕСТЫ = {"test_notes.py": (5, 1), "test_todo.py": (6, 0), "test_readme.py": (4, 2)}
ПАПКА = len(ТЕКСТЫ) + len(ТЕСТЫ)
ВЫПУСКИ_ДО = (0, 1, 3)          # запусков мира до прогона — леджер запусков (дверь `actturn`)
АРХИВ_ДО = (0, 1, 2)            # файлов в папке archive до переноса — по файлу
НОВЫЕ_ИМЕНА = {"notes.md": ("shopping.md", "list.md"), "todo.txt": ("tasks.txt", "plan.txt"),
               "readme.md": ("about.md", "info.md")}
ЗАНЯТОЕ = {"notes.md": "todo.txt", "todo.txt": "readme.md", "readme.md": "notes.md"}
НЕТ_ФАЙЛА = ("draft.md", "final.md")    # файла draft.md в мире нет; final.md — имя, в которое его зовут

# (строки файла; искомые: дважды, однажды, ни разу; три замены; слово, которого нет, и чем его заменить;
#  две строки для дописывания)
СОДЕРЖИМОЕ = {
    "en": {"notes.md": (("buy milk", "call the bank", "buy bread and milk"), ("milk", "bank", "tea"),
                        (("milk", "juice"), ("bank", "shop"), ("bread", "milk")), ("tea", "coffee"),
                        ("buy eggs", "call the school")),
           "todo.txt": (("fix the lamp", "water the plants", "fix the door"), ("fix", "plants", "paint"),
                        (("fix", "check"), ("lamp", "clock"), ("door", "lamp")), ("paint", "glue"),
                        ("clean the room", "fix the tap")),
           "readme.md": (("the tool reads files", "the tool counts words", "the report lists files"),
                         ("files", "words", "code"), (("files", "pages"), ("words", "names"), ("report", "tool")),
                         ("code", "text"), ("the tool finds words", "the report counts pages"))},
    "ru": {"notes.md": (("купить молоко", "позвонить в банк", "купить хлеб и молоко"), ("молоко", "банк", "чай"),
                        (("молоко", "сок"), ("банк", "магазин"), ("хлеб", "молоко")), ("чай", "кофе"),
                        ("купить яйца", "позвонить в школу")),
           "todo.txt": (("починить лампу", "полить цветы", "починить дверь"), ("починить", "цветы", "краску"),
                        (("починить", "проверить"), ("лампу", "полку"), ("дверь", "лампу")), ("краску", "клей"),
                        ("убрать комнату", "починить кран")),
           "readme.md": (("программа читает файлы", "программа считает слова", "отчёт перечисляет файлы"),
                         ("файлы", "слова", "код"), (("файлы", "страницы"), ("слова", "имена"),
                                                    ("отчёт", "программа")),
                         ("код", "текст"), ("программа ищет слова", "отчёт считает страницы"))},
    "de": {"notes.md": (("Milch kaufen", "die Bank anrufen", "Brot und Milch kaufen"), ("Milch", "Bank", "Tee"),
                        (("Milch", "Saft"), ("Bank", "Post"), ("Brot", "Milch")), ("Tee", "Kaffee"),
                        ("Eier kaufen", "die Schule anrufen")),
           "todo.txt": (("die Lampe reparieren", "die Pflanzen gießen", "die Tür reparieren"),
                        ("reparieren", "Pflanzen", "Farbe"),
                        (("reparieren", "prüfen"), ("Lampe", "Uhr"), ("Tür", "Lampe")), ("Farbe", "Leim"),
                        ("das Zimmer aufräumen", "den Hahn reparieren")),
           "readme.md": (("das Programm liest Dateien", "das Programm zählt Wörter", "der Bericht listet Dateien"),
                         ("Dateien", "Wörter", "Code"), (("Dateien", "Seiten"), ("Bericht", "Katalog"),
                                                        ("Wörter", "Dateien")),
                         ("Code", "Text"), ("das Programm sucht Wörter", "der Bericht zählt Seiten"))},
    "fr": {"notes.md": (("acheter du lait", "appeler la banque", "acheter du pain et du lait"),
                        ("lait", "banque", "thé"), (("lait", "jus"), ("banque", "poste"), ("pain", "lait")),
                        ("thé", "café"), ("acheter des œufs", "appeler la mairie")),
           "todo.txt": (("réparer la lampe", "arroser les plantes", "réparer la porte"),
                        ("réparer", "plantes", "peinture"),
                        (("réparer", "vérifier"), ("lampe", "fenêtre"), ("porte", "lampe")), ("peinture", "colle"),
                        ("ranger la chambre", "réparer le robinet")),
           "readme.md": (("le programme lit les fichiers", "le programme compte les mots",
                          "le rapport liste les fichiers"),
                         ("fichiers", "mots", "code"), (("fichiers", "pages"), ("mots", "noms"),
                                                       ("rapport", "programme")),
                         ("code", "texte"), ("le programme cherche les mots", "le rapport compte les pages"))},
    "es": {"notes.md": (("comprar leche", "llamar al banco", "comprar pan y leche"), ("leche", "banco", "té"),
                        (("leche", "zumo"), ("banco", "médico"), ("pan", "leche")), ("té", "café"),
                        ("comprar huevos", "llamar a la escuela")),
           "todo.txt": (("arreglar la lámpara", "regar las plantas", "arreglar la puerta"),
                        ("arreglar", "plantas", "pintura"),
                        (("arreglar", "revisar"), ("lámpara", "ventana"), ("puerta", "lámpara")),
                        ("pintura", "cola"), ("ordenar la habitación", "arreglar el grifo")),
           "readme.md": (("el programa lee archivos", "el programa cuenta palabras", "el informe lista archivos"),
                         ("archivos", "palabras", "código"), (("archivos", "textos"), ("palabras", "frases"),
                                                             ("informe", "programa")),
                         ("código", "texto"), ("el programa busca palabras", "el informe cuenta textos"))},
    "it": {"notes.md": (("comprare il latte", "chiamare la banca", "comprare il pane e il latte"),
                        ("latte", "banca", "tè"), (("latte", "succo"), ("banca", "scuola"), ("pane", "latte")),
                        ("tè", "caffè"), ("comprare le uova", "chiamare il medico")),
           "todo.txt": (("riparare la lampada", "annaffiare le piante", "riparare la porta"),
                        ("riparare", "piante", "vernice"),
                        (("riparare", "controllare"), ("lampada", "finestra"), ("porta", "lampada")),
                        ("vernice", "colla"), ("pulire la stanza", "riparare il rubinetto")),
           "readme.md": (("il programma legge i documenti", "il programma conta le parole",
                          "il rapporto elenca i documenti"),
                         ("documenti", "parole", "codice"), (("documenti", "testi"), ("parole", "frasi"),
                                                            ("rapporto", "programma")),
                         ("codice", "testo"), ("il programma cerca le parole", "il rapporto conta i testi"))},
    "pt": {"notes.md": (("comprar leite", "ligar ao banco", "comprar pão e leite"), ("leite", "banco", "chá"),
                        (("leite", "sumo"), ("banco", "médico"), ("pão", "leite")), ("chá", "café"),
                        ("comprar ovos", "ligar à escola")),
           "todo.txt": (("arranjar a lâmpada", "regar as plantas", "arranjar a porta"),
                        ("arranjar", "plantas", "tinta"),
                        (("arranjar", "verificar"), ("lâmpada", "janela"), ("porta", "lâmpada")), ("tinta", "cola"),
                        ("arrumar o quarto", "arranjar a torneira")),
           "readme.md": (("o programa lê ficheiros", "o programa conta palavras", "o relatório lista ficheiros"),
                         ("ficheiros", "palavras", "código"), (("ficheiros", "textos"), ("palavras", "frases"),
                                                              ("relatório", "programa")),
                         ("código", "texto"), ("o programa procura palavras", "o relatório conta textos"))},
    "nl": {"notes.md": (("melk kopen", "de bank bellen", "brood en melk kopen"), ("melk", "bank", "thee"),
                        (("melk", "sap"), ("bank", "dokter"), ("brood", "melk")), ("thee", "koffie"),
                        ("eieren kopen", "de school bellen")),
           "todo.txt": (("de lamp repareren", "de planten water geven", "de deur repareren"),
                        ("repareren", "planten", "verf"),
                        (("repareren", "controleren"), ("lamp", "klok"), ("deur", "lamp")), ("verf", "lijm"),
                        ("de kamer opruimen", "de kraan repareren")),
           "readme.md": (("het programma leest bestanden", "het programma telt woorden", "het rapport toont bestanden"),
                         ("bestanden", "woorden", "code"), (("bestanden", "teksten"), ("woorden", "namen"),
                                                           ("rapport", "programma")),
                         ("code", "tekst"), ("het programma zoekt woorden", "het rapport telt teksten"))},
    "pl": {"notes.md": (("kupić mleko", "zadzwonić do banku", "kupić chleb i mleko"), ("mleko", "banku", "herbata"),
                        (("mleko", "sok"), ("banku", "sklepu"), ("chleb", "mleko")), ("herbata", "kawa"),
                        ("kupić jajka", "zadzwonić do szkoły")),
           "todo.txt": (("naprawić lampę", "podlać rośliny", "naprawić drzwi"), ("naprawić", "rośliny", "farba"),
                        (("naprawić", "sprawdzić"), ("lampę", "półkę"), ("drzwi", "lampę")), ("farba", "klej"),
                        ("posprzątać pokój", "naprawić kran")),
           "readme.md": (("program czyta pliki", "program liczy słowa", "raport wymienia pliki"),
                         ("pliki", "słowa", "kod"), (("pliki", "strony"), ("słowa", "imiona"), ("raport", "program")),
                         ("kod", "tekst"), ("program szuka słów", "raport liczy strony"))},
}

# ======================================================================================================
# РЕЧЬ: три ступени акта (приказ, инфинитив предложения, отчёт), фразы новых леджеров, регистры приказа
# ======================================================================================================
КАВЫЧКИ = {"ru": ("«", "»"), "en": ('"', '"'), "de": ("„", "“"), "fr": ("« ", " »"), "es": ("«", "»"),
           "it": ("«", "»"), "pt": ("«", "»"), "nl": ('"', '"'), "pl": ("„", "”")}
РАЗ = {"en": ("time", "times"), "de": ("Mal", "Mal"), "fr": ("fois", "fois"), "es": ("vez", "veces"),
       "it": ("volta", "volte"), "pt": ("vez", "vezes"), "nl": ("keer", "keer"), "pl": ("raz", "razy", "razy")}
СТРОК = {"ru": ("строка", "строки", "строк"), "en": ("line", "lines"), "de": ("Zeile", "Zeilen"),
         "fr": ("ligne", "lignes"), "es": ("línea", "líneas"), "it": ("riga", "righe"), "pt": ("linha", "linhas"),
         "nl": ("regel", "regels"), "pl": ("linia", "linie", "linii")}
ТЕСТ = {"ru": ("тест", "теста", "тестов"), "en": ("test", "tests"), "de": ("Test", "Tests"), "fr": ("test", "tests"),
        "es": ("prueba", "pruebas"), "it": ("test", "test"), "pt": ("teste", "testes"), "nl": ("test", "tests"),
        "pl": ("test", "testy", "testów")}
# СОГЛАСИЕ ИСХОДА С ЧИСЛОМ ПРОШЕДШИХ — ячейкой пакета, как счётное слово («1 test sur 5 réussi»)
ПРОШЛО = {"ru": ("пройден", "пройдено", "пройдено"), "fr": ("réussi", "réussis"), "es": ("superada", "superadas"),
          "it": ("superato", "superati"), "pt": ("passou", "passaram")}

# акт → (приказ, инфинитив, отчёт) — у de и nl инфинитив с глаголом в конце и «zu/te»-форма предложения
АКТЫ = ("поиск", "строки", "замена", "дописать", "переименовать", "перенести", "тесты")
РЕЧЬ = {
    "en": dict(
        поиск=("find the word {w} in the file {f}", "find the word {w} in the file {f}",
               "searched for the word {w} in the file {f}"),
        строки=("find the lines with the word {w} in the file {f}", "find the lines with the word {w} in the file {f}",
                "searched for the lines with the word {w} in the file {f}"),
        замена=("replace the word {w} with {v} in the file {f}", "replace the word {w} with {v} in the file {f}",
                "replaced the word {w} with {v} in the file {f}"),
        дописать=("append the line {s} to the file {f}", "append the line {s} to the file {f}",
                  "appended the line {s} to the file {f}"),
        переименовать=("rename the file {f} to {g}", "rename the file {f} to {g}", "renamed the file {f} to {g}"),
        перенести=("move the file {f} to the folder archive", "move the file {f} to the folder archive",
                   "moved the file {f} to the folder archive"),
        тесты=("run the tests in the file {t}", "run the tests in the file {t}", "ran the tests in the file {t}"),
        предложение="i propose to {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="please {imp}.", косвенный="we need to {inf}.",
                      вопросом="could you {inf}?"),
        встречается="the word {w} occurs {N} in the file {f}",
        вопрос_раз="how many times does the word {w} occur in the file {f}?",
        строк_со_словом="the file {f} has {N} with the word {w}",
        позиция=("the word {w} stands in line {a}", "the word {w} stands in lines {a} and {b}"),
        нет_слова="the word {w} is not in the file {f}",
        архив="the folder archive contains {N}",
        проверил="checked the file {f}",
        итог=("the run ended successfully", "the run ended with an error"),
        выпуск=("all tests passed — the release is published", "not all tests passed — the release is not published"),
        план_замены=("find the word {w} in the file {f}, then replace it with {v}, then check the file",
                     "i propose three acts: find the word {w} in the file {f}, replace it with {v}, "
                     "check the file {f}"),
        план_тестов=("run the tests in the file {t}, then publish the release if all tests pass",
                     "i propose two acts: run the tests in the file {t}, then publish the release "
                     "if all tests pass")),
    "ru": dict(
        поиск=("найди слово {w} в файле {f}", "найти слово {w} в файле {f}", "искал слово {w} в файле {f}"),
        строки=("найди строки со словом {w} в файле {f}", "найти строки со словом {w} в файле {f}",
                "искал строки со словом {w} в файле {f}"),
        замена=("замени слово {w} на {v} в файле {f}", "заменить слово {w} на {v} в файле {f}",
                "заменил слово {w} на {v} в файле {f}"),
        дописать=("допиши строку {s} в файл {f}", "дописать строку {s} в файл {f}", "дописал строку {s} в файл {f}"),
        переименовать=("переименуй файл {f} в {g}", "переименовать файл {f} в {g}", "переименовал файл {f} в {g}"),
        перенести=("перенеси файл {f} в папку archive", "перенести файл {f} в папку archive",
                   "перенёс файл {f} в папку archive"),
        тесты=("запусти тесты из файла {t}", "запустить тесты из файла {t}", "запустил тесты из файла {t}"),
        предложение="предлагаю {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="пожалуйста, {imp}.", косвенный="нужно {inf}.",
                      вопросом="ты можешь {inf}?"),
        встречается="в файле {f} слово {w} встречается {N}",
        вопрос_раз="сколько раз слово {w} встречается в файле {f}?",
        строк_со_словом="в файле {f} {N} со словом {w}",
        позиция=("слово {w} стоит в строке {a}", "слово {w} стоит в строках {a} и {b}"),
        нет_слова="слова {w} нет в файле {f}",
        архив="папка archive содержит {N}",
        проверил="проверил файл {f}",
        итог=("запуск завершился успешно", "запуск завершился ошибкой"),
        выпуск=("все тесты пройдены — релиз выпущен", "не все тесты пройдены — релиз не выпущен"),
        план_замены=("найди слово {w} в файле {f}, затем замени его на {v}, затем проверь файл",
                     "предлагаю три акта: найти слово {w} в файле {f}, заменить его на {v}, проверить файл {f}"),
        план_тестов=("запусти тесты из файла {t}, затем выпусти релиз, если все тесты пройдут",
                     "предлагаю два акта: запустить тесты из файла {t}, затем выпустить релиз, "
                     "если все тесты пройдут")),
    "de": dict(
        поиск=("suche das Wort {w} in der Datei {f}", "das Wort {w} in der Datei {f} suchen",
               "das Wort {w} in der Datei {f} gesucht", "das Wort {w} in der Datei {f} zu suchen"),
        строки=("suche die Zeilen mit dem Wort {w} in der Datei {f}",
                "die Zeilen mit dem Wort {w} in der Datei {f} suchen",
                "die Zeilen mit dem Wort {w} in der Datei {f} gesucht",
                "die Zeilen mit dem Wort {w} in der Datei {f} zu suchen"),
        замена=("ersetze das Wort {w} in der Datei {f} durch {v}", "das Wort {w} in der Datei {f} durch {v} ersetzen",
                "das Wort {w} in der Datei {f} durch {v} ersetzt",
                "das Wort {w} in der Datei {f} durch {v} zu ersetzen"),
        дописать=("ergänze die Datei {f} um die Zeile {s}", "die Datei {f} um die Zeile {s} ergänzen",
                  "die Datei {f} um die Zeile {s} ergänzt", "die Datei {f} um die Zeile {s} zu ergänzen"),
        переименовать=("gib der Datei {f} den Namen {g}", "der Datei {f} den Namen {g} geben",
                       "der Datei {f} den Namen {g} gegeben", "der Datei {f} den Namen {g} zu geben"),
        перенести=("verschiebe die Datei {f} in den Ordner archive", "die Datei {f} in den Ordner archive verschieben",
                   "die Datei {f} in den Ordner archive verschoben",
                   "die Datei {f} in den Ordner archive zu verschieben"),
        тесты=("starte die Tests aus der Datei {t}", "die Tests aus der Datei {t} starten",
               "die Tests aus der Datei {t} gestartet", "die Tests aus der Datei {t} zu starten"),
        предложение="ich schlage vor, {zu}", отчёт="ich habe {past}",
        регистры=dict(плоский="{imp}.", вежливый="bitte {imp}.", косвенный="man sollte {inf}.",
                      вопросом="kannst du {inf}?"),
        встречается="das Wort {w} kommt in der Datei {f} {N} vor",
        вопрос_раз="wie oft kommt das Wort {w} in der Datei {f} vor?",
        строк_со_словом="die Datei {f} hat {N} mit dem Wort {w}",
        позиция=("das Wort {w} steht in Zeile {a}", "das Wort {w} steht in den Zeilen {a} und {b}"),
        нет_слова="das Wort {w} steht nicht in der Datei {f}",
        архив="der Ordner archive enthält {N}",
        проверил="ich habe die Datei {f} geprüft",
        итог=("der Lauf endete erfolgreich", "der Lauf endete mit einem Fehler"),
        выпуск=("alle Tests bestanden — das Release ist veröffentlicht",
                "nicht alle Tests bestanden — das Release wird nicht veröffentlicht"),
        план_замены=("suche das Wort {w} in der Datei {f}, dann ersetze es durch {v}, dann prüfe die Datei",
                     "ich schlage drei Handlungen vor: das Wort {w} in der Datei {f} suchen, es durch {v} ersetzen, "
                     "die Datei {f} prüfen"),
        план_тестов=("starte die Tests aus der Datei {t}, dann veröffentliche das Release, wenn alle Tests bestehen",
                     "ich schlage zwei Handlungen vor: die Tests aus der Datei {t} starten, dann das Release "
                     "veröffentlichen, wenn alle Tests bestehen")),
    "fr": dict(
        поиск=("cherche le mot {w} dans le fichier {f}", "chercher le mot {w} dans le fichier {f}",
               "cherché le mot {w} dans le fichier {f}"),
        строки=("cherche les lignes avec le mot {w} dans le fichier {f}",
                "chercher les lignes avec le mot {w} dans le fichier {f}",
                "cherché les lignes avec le mot {w} dans le fichier {f}"),
        замена=("remplace le mot {w} par {v} dans le fichier {f}", "remplacer le mot {w} par {v} dans le fichier {f}",
                "remplacé le mot {w} par {v} dans le fichier {f}"),
        дописать=("ajoute la ligne {s} au fichier {f}", "ajouter la ligne {s} au fichier {f}",
                  "ajouté la ligne {s} au fichier {f}"),
        переименовать=("renomme le fichier {f} en {g}", "renommer le fichier {f} en {g}",
                       "renommé le fichier {f} en {g}"),
        перенести=("déplace le fichier {f} dans le dossier archive", "déplacer le fichier {f} dans le dossier archive",
                   "déplacé le fichier {f} dans le dossier archive"),
        тесты=("lance les tests du fichier {t}", "lancer les tests du fichier {t}", "lancé les tests du fichier {t}"),
        предложение="je propose de {inf}", отчёт="j'ai {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, s'il te plaît.", косвенный="il faut {inf}.",
                      вопросом="peux-tu {inf} ?"),
        встречается="le mot {w} apparaît {N} dans le fichier {f}",
        вопрос_раз="combien de fois le mot {w} apparaît-il dans le fichier {f} ?",
        строк_со_словом="le fichier {f} a {N} avec le mot {w}",
        позиция=("le mot {w} se trouve à la ligne {a}", "le mot {w} se trouve aux lignes {a} et {b}"),
        нет_слова="le mot {w} n'est pas dans le fichier {f}",
        архив="le dossier archive contient {N}",
        проверил="j'ai vérifié le fichier {f}",
        итог=("l'exécution s'est terminée avec succès", "l'exécution s'est terminée par une erreur"),
        выпуск=("tous les tests ont réussi — la version est publiée",
                "certains tests ont échoué — la version n'est pas publiée"),
        план_замены=("cherche le mot {w} dans le fichier {f}, puis remplace-le par {v}, puis vérifie le fichier",
                     "je propose trois actes : chercher le mot {w} dans le fichier {f}, le remplacer par {v}, "
                     "vérifier le fichier {f}"),
        план_тестов=("lance les tests du fichier {t}, puis publie la version si tous les tests réussissent",
                     "je propose deux actes : lancer les tests du fichier {t}, puis publier la version "
                     "si tous les tests réussissent")),
    "es": dict(
        поиск=("busca la palabra {w} en el archivo {f}", "buscar la palabra {w} en el archivo {f}",
               "buscado la palabra {w} en el archivo {f}"),
        строки=("busca las líneas con la palabra {w} en el archivo {f}",
                "buscar las líneas con la palabra {w} en el archivo {f}",
                "buscado las líneas con la palabra {w} en el archivo {f}"),
        замена=("reemplaza la palabra {w} por {v} en el archivo {f}",
                "reemplazar la palabra {w} por {v} en el archivo {f}",
                "reemplazado la palabra {w} por {v} en el archivo {f}"),
        дописать=("añade la línea {s} al archivo {f}", "añadir la línea {s} al archivo {f}",
                  "añadido la línea {s} al archivo {f}"),
        переименовать=("renombra el archivo {f} como {g}", "renombrar el archivo {f} como {g}",
                       "renombrado el archivo {f} como {g}"),
        перенести=("mueve el archivo {f} a la carpeta archive", "mover el archivo {f} a la carpeta archive",
                   "movido el archivo {f} a la carpeta archive"),
        тесты=("ejecuta las pruebas del archivo {t}", "ejecutar las pruebas del archivo {t}",
               "ejecutado las pruebas del archivo {t}"),
        предложение="propongo {inf}", отчёт="he {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, por favor.", косвенный="hay que {inf}.",
                      вопросом="¿puedes {inf}?"),
        встречается="la palabra {w} aparece {N} en el archivo {f}",
        вопрос_раз="¿cuántas veces aparece la palabra {w} en el archivo {f}?",
        строк_со_словом="el archivo {f} tiene {N} con la palabra {w}",
        позиция=("la palabra {w} está en la línea {a}", "la palabra {w} está en las líneas {a} y {b}"),
        нет_слова="la palabra {w} no está en el archivo {f}",
        архив="la carpeta archive contiene {N}",
        проверил="he revisado el archivo {f}",
        итог=("la ejecución terminó con éxito", "la ejecución terminó con un error"),
        выпуск=("todas las pruebas pasaron — la versión está publicada",
                "algunas pruebas fallaron — la versión no se publica"),
        план_замены=("busca la palabra {w} en el archivo {f}, luego reemplázala por {v}, luego revisa el archivo",
                     "propongo tres actos: buscar la palabra {w} en el archivo {f}, reemplazarla por {v}, "
                     "revisar el archivo {f}"),
        план_тестов=("ejecuta las pruebas del archivo {t}, luego publica la versión si todas las pruebas pasan",
                     "propongo dos actos: ejecutar las pruebas del archivo {t}, luego publicar la versión "
                     "si todas las pruebas pasan")),
    "it": dict(
        поиск=("cerca la parola {w} nel file {f}", "cercare la parola {w} nel file {f}",
               "cercato la parola {w} nel file {f}"),
        строки=("cerca le righe con la parola {w} nel file {f}", "cercare le righe con la parola {w} nel file {f}",
                "cercato le righe con la parola {w} nel file {f}"),
        замена=("sostituisci la parola {w} con {v} nel file {f}", "sostituire la parola {w} con {v} nel file {f}",
                "sostituito la parola {w} con {v} nel file {f}"),
        дописать=("aggiungi la riga {s} al file {f}", "aggiungere la riga {s} al file {f}",
                  "aggiunto la riga {s} al file {f}"),
        переименовать=("rinomina il file {f} in {g}", "rinominare il file {f} in {g}", "rinominato il file {f} in {g}"),
        перенести=("sposta il file {f} nella cartella archive", "spostare il file {f} nella cartella archive",
                   "spostato il file {f} nella cartella archive"),
        тесты=("esegui i test del file {t}", "eseguire i test del file {t}", "eseguito i test del file {t}"),
        предложение="propongo di {inf}", отчёт="ho {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, per favore.", косвенный="bisogna {inf}.",
                      вопросом="puoi {inf}?"),
        встречается="la parola {w} compare {N} nel file {f}",
        вопрос_раз="quante volte compare la parola {w} nel file {f}?",
        строк_со_словом="il file {f} ha {N} con la parola {w}",
        позиция=("la parola {w} si trova alla riga {a}", "la parola {w} si trova alle righe {a} e {b}"),
        нет_слова="la parola {w} non è nel file {f}",
        архив="la cartella archive contiene {N}",
        проверил="ho controllato il file {f}",
        итог=("l'esecuzione è terminata con successo", "l'esecuzione è terminata con un errore"),
        выпуск=("tutti i test sono passati — la versione è pubblicata",
                "alcuni test sono falliti — la versione non viene pubblicata"),
        план_замены=("cerca la parola {w} nel file {f}, poi sostituiscila con {v}, poi controlla il file",
                     "propongo tre atti: cercare la parola {w} nel file {f}, sostituirla con {v}, "
                     "controllare il file {f}"),
        план_тестов=("esegui i test del file {t}, poi pubblica la versione se tutti i test passano",
                     "propongo due atti: eseguire i test del file {t}, poi pubblicare la versione "
                     "se tutti i test passano")),
    "pt": dict(
        поиск=("procura a palavra {w} no ficheiro {f}", "procurar a palavra {w} no ficheiro {f}",
               "procurei a palavra {w} no ficheiro {f}"),
        строки=("procura as linhas com a palavra {w} no ficheiro {f}",
                "procurar as linhas com a palavra {w} no ficheiro {f}",
                "procurei as linhas com a palavra {w} no ficheiro {f}"),
        замена=("substitui a palavra {w} por {v} no ficheiro {f}", "substituir a palavra {w} por {v} no ficheiro {f}",
                "substituí a palavra {w} por {v} no ficheiro {f}"),
        дописать=("acrescenta a linha {s} ao ficheiro {f}", "acrescentar a linha {s} ao ficheiro {f}",
                  "acrescentei a linha {s} ao ficheiro {f}"),
        переименовать=("renomeia o ficheiro {f} para {g}", "renomear o ficheiro {f} para {g}",
                       "renomeei o ficheiro {f} para {g}"),
        перенести=("move o ficheiro {f} para a pasta archive", "mover o ficheiro {f} para a pasta archive",
                   "movi o ficheiro {f} para a pasta archive"),
        тесты=("executa os testes do ficheiro {t}", "executar os testes do ficheiro {t}",
               "executei os testes do ficheiro {t}"),
        предложение="proponho {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, por favor.", косвенный="é preciso {inf}.",
                      вопросом="podes {inf}?"),
        встречается="a palavra {w} aparece {N} no ficheiro {f}",
        вопрос_раз="quantas vezes aparece a palavra {w} no ficheiro {f}?",
        строк_со_словом="o ficheiro {f} tem {N} com a palavra {w}",
        позиция=("a palavra {w} está na linha {a}", "a palavra {w} está nas linhas {a} e {b}"),
        нет_слова="a palavra {w} não está no ficheiro {f}",
        архив="a pasta archive contém {N}",
        проверил="verifiquei o ficheiro {f}",
        итог=("a execução terminou com sucesso", "a execução terminou com um erro"),
        выпуск=("todos os testes passaram — a versão está publicada",
                "alguns testes falharam — a versão não é publicada"),
        план_замены=("procura a palavra {w} no ficheiro {f}, depois substitui-a por {v}, depois verifica o ficheiro",
                     "proponho três atos: procurar a palavra {w} no ficheiro {f}, substituí-la por {v}, "
                     "verificar o ficheiro {f}"),
        план_тестов=("executa os testes do ficheiro {t}, depois publica a versão se todos os testes passarem",
                     "proponho dois atos: executar os testes do ficheiro {t}, depois publicar a versão "
                     "se todos os testes passarem")),
    "nl": dict(
        поиск=("zoek het woord {w} in het bestand {f}", "het woord {w} in het bestand {f} zoeken",
               "het woord {w} in het bestand {f} gezocht", "het woord {w} in het bestand {f} te zoeken"),
        строки=("zoek de regels met het woord {w} in het bestand {f}",
                "de regels met het woord {w} in het bestand {f} zoeken",
                "de regels met het woord {w} in het bestand {f} gezocht",
                "de regels met het woord {w} in het bestand {f} te zoeken"),
        замена=("vervang het woord {w} in het bestand {f} door {v}",
                "het woord {w} in het bestand {f} door {v} vervangen",
                "het woord {w} in het bestand {f} door {v} vervangen",
                "het woord {w} in het bestand {f} door {v} te vervangen"),
        дописать=("zet de regel {s} onderaan het bestand {f}", "de regel {s} onderaan het bestand {f} zetten",
                  "de regel {s} onderaan het bestand {f} gezet", "de regel {s} onderaan het bestand {f} te zetten"),
        переименовать=("hernoem het bestand {f} naar {g}", "het bestand {f} naar {g} hernoemen",
                       "het bestand {f} naar {g} hernoemd", "het bestand {f} naar {g} te hernoemen"),
        перенести=("verplaats het bestand {f} naar de map archive", "het bestand {f} naar de map archive verplaatsen",
                   "het bestand {f} naar de map archive verplaatst",
                   "het bestand {f} naar de map archive te verplaatsen"),
        тесты=("start de tests uit het bestand {t}", "de tests uit het bestand {t} starten",
               "de tests uit het bestand {t} gestart", "de tests uit het bestand {t} te starten"),
        предложение="ik stel voor {zu}", отчёт="ik heb {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, alsjeblieft.", косвенный="we moeten {inf}.",
                      вопросом="kun je {inf}?"),
        встречается="het woord {w} komt {N} voor in het bestand {f}",
        вопрос_раз="hoe vaak komt het woord {w} voor in het bestand {f}?",
        строк_со_словом="het bestand {f} heeft {N} met het woord {w}",
        позиция=("het woord {w} staat in regel {a}", "het woord {w} staat in de regels {a} en {b}"),
        нет_слова="het woord {w} staat niet in het bestand {f}",
        архив="de map archive bevat {N}",
        проверил="ik heb het bestand {f} gecontroleerd",
        итог=("de run eindigde succesvol", "de run eindigde met een fout"),
        выпуск=("alle tests geslaagd — de release is gepubliceerd",
                "niet alle tests geslaagd — de release wordt niet gepubliceerd"),
        план_замены=("zoek het woord {w} in het bestand {f}, vervang het dan door {v} en controleer daarna het bestand",
                     "ik stel drie handelingen voor: het woord {w} in het bestand {f} zoeken, het door {v} "
                     "vervangen, het bestand {f} controleren"),
        план_тестов=("start de tests uit het bestand {t} en publiceer daarna de release als alle tests slagen",
                     "ik stel twee handelingen voor: de tests uit het bestand {t} starten en daarna de release "
                     "publiceren als alle tests slagen")),
    "pl": dict(
        поиск=("znajdź słowo {w} w pliku {f}", "znaleźć słowo {w} w pliku {f}", "szukałem słowa {w} w pliku {f}"),
        строки=("znajdź linie ze słowem {w} w pliku {f}", "znaleźć linie ze słowem {w} w pliku {f}",
                "szukałem linii ze słowem {w} w pliku {f}"),
        замена=("zamień słowo {w} na {v} w pliku {f}", "zamienić słowo {w} na {v} w pliku {f}",
                "zamieniłem słowo {w} na {v} w pliku {f}"),
        дописать=("dopisz linię {s} do pliku {f}", "dopisać linię {s} do pliku {f}",
                  "dopisałem linię {s} do pliku {f}"),
        переименовать=("zmień nazwę pliku {f} na {g}", "zmienić nazwę pliku {f} na {g}",
                       "zmieniłem nazwę pliku {f} na {g}"),
        перенести=("przenieś plik {f} do folderu archive", "przenieść plik {f} do folderu archive",
                   "przeniosłem plik {f} do folderu archive"),
        тесты=("uruchom testy z pliku {t}", "uruchomić testy z pliku {t}", "uruchomiłem testy z pliku {t}"),
        предложение="proponuję {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="proszę, {imp}.", косвенный="trzeba {inf}.",
                      вопросом="czy możesz {inf}?"),
        встречается="słowo {w} występuje {N} w pliku {f}",
        вопрос_раз="ile razy słowo {w} występuje w pliku {f}?",
        строк_со_словом="plik {f} ma {N} ze słowem {w}",
        позиция=("słowo {w} jest w linii {a}", "słowo {w} jest w liniach {a} i {b}"),
        нет_слова="słowa {w} nie ma w pliku {f}",
        архив="folder archive zawiera {N}",
        проверил="sprawdziłem plik {f}",
        итог=("uruchomienie zakończyło się sukcesem", "uruchomienie zakończyło się błędem"),
        выпуск=("wszystkie testy przeszły — wydanie jest opublikowane",
                "nie wszystkie testy przeszły — wydanie nie zostaje opublikowane"),
        план_замены=("znajdź słowo {w} w pliku {f}, potem zamień je na {v}, potem sprawdź plik",
                     "proponuję trzy akty: znaleźć słowo {w} w pliku {f}, zamienić je na {v}, sprawdzić plik {f}"),
        план_тестов=("uruchom testy z pliku {t}, potem opublikuj wydanie, jeśli wszystkie testy przejdą",
                     "proponuję dwa akty: uruchomić testy z pliku {t}, potem opublikować wydanie, "
                     "jeśli wszystkie testy przejdą")),
}
РЕГИСТРЫ = ("плоский", "вежливый", "косвенный", "вопросом")

# ======================================================================================================
# РОДЫ ДОМА
# ======================================================================================================
ПОИСК = "поиск слова в файле"
ПОИСК_ОТКАЗ = "поиск слова — отказ"
ПОИСК_ВОПРОС = "сколько раз слово в файле — вопрос без акта"
СТРОКИ = "поиск строк со словом"
ЗАМЕНА = "замена слова"
ЗАМЕНА_ОТКАЗ = "замена слова — отказ"
ЗАМЕНА_НЕЧЕГО = "замена слова, которого в файле нет"
ДОПИСАТЬ = "дописать показанную строку"
ДОПИСАТЬ_ОТКАЗ = "дописать строку — отказ"
ДОПИСАТЬ_НЕТ = "дописать строку в файл, которого нет"
ИМЯ = "переименовать файл"
ИМЯ_ЗАНЯТО = "переименовать в занятое имя"
ИМЯ_НЕТ = "переименовать файл, которого нет"
ПЕРЕНОС = "перенести файл в папку archive"
ПРОГОН = "прогон тестов с исходом"
ПРОГОН_ОТКАЗ = "прогон тестов — отказ"
ПЛАН_ЗАМЕНЫ = "план: найти, заменить, проверить"
ПЛАН_ЗАМЕНЫ_ОТКАЗ = "план замены — отказ"
ПЛАН_ВЫПУСКА = "план: тесты, затем выпуск лишь при всех прошедших"
РОДЫ = (ПОИСК, ПОИСК_ОТКАЗ, ПОИСК_ВОПРОС, СТРОКИ, ЗАМЕНА, ЗАМЕНА_ОТКАЗ, ЗАМЕНА_НЕЧЕГО, ДОПИСАТЬ, ДОПИСАТЬ_ОТКАЗ,
        ДОПИСАТЬ_НЕТ, ИМЯ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ, ПЕРЕНОС, ПРОГОН, ПРОГОН_ОТКАЗ, ПЛАН_ЗАМЕНЫ, ПЛАН_ЗАМЕНЫ_ОТКАЗ,
        ПЛАН_ВЫПУСКА)
# роды, чей приказ пишется во всех четырёх регистрах; прочие — прямым
С_РЕГИСТРАМИ = frozenset({ПОИСК, СТРОКИ, ЗАМЕНА, ЗАМЕНА_НЕЧЕГО, ДОПИСАТЬ, ДОПИСАТЬ_НЕТ, ИМЯ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ,
                          ПЕРЕНОС, ПРОГОН})


# ======================================================================================================
# ФОРМЫ ПРИ ЧИСЛЕ И ФРАЗЫ
# ======================================================================================================
def раз(язык, n):
    """«2 times», «2 раза», «1 vez» — русское «раз» у двери `rugram`, прочие — ячейкой пакета."""
    if язык == "ru":
        return f"{n} {rugram.форма('раз', n)}"
    return f"{n} {S._счёт(РАЗ[язык], n, язык)}"


def строк(язык, n):
    return f"{n} {S._счёт(СТРОК[язык], n, язык)}"


def тестов(язык, n):
    return f"{n} {S._счёт(ТЕСТ[язык], n, язык)}"


def прошло(язык, p, т):
    """Фраза «прошло P из T» — с согласием слова исхода по ячейке пакета там, где оно есть."""
    if язык == "en":
        return f"{p} of {тестов(язык, т)} passed"
    if язык == "ru":
        return f"{S._счёт(ПРОШЛО['ru'], p, 'ru')} {тестов(язык, p)} из {т}"
    if язык == "de":
        return f"{p} von {тестов(язык, т)} bestanden"
    if язык == "fr":
        return f"{тестов(язык, p)} sur {т} {S._счёт(ПРОШЛО['fr'], p, 'fr')}"
    if язык == "es":
        return f"{p} de {тестов(язык, т)} {S._счёт(ПРОШЛО['es'], p, 'es')}"
    if язык == "it":
        return f"{тестов(язык, p)} su {т} {S._счёт(ПРОШЛО['it'], p, 'it')}"
    if язык == "pt":
        return f"{p} de {тестов(язык, т)} {S._счёт(ПРОШЛО['pt'], p, 'pt')}"
    if язык == "nl":
        return f"{p} van de {тестов(язык, т)} geslaagd"
    return f"zaliczono {p} z {т} testów"


def кавычки(язык, текст):
    о, з = КАВЫЧКИ[язык]
    return f"{о}{текст}{з}"


def _р(язык, кто, что):
    return A._реплика(язык, кто, что)


def _вопрос_предложения(язык):
    """«is that confirmed?» — вопрос предложения у двери `actturn`: по нему рынок пулит «да» и «нет»."""
    return A.РЕЧЬ[язык]["предложение"].rsplit(". ", 1)[1]


def _хвост_отказа(язык):
    """«the act is not performed» — хвост отказа у двери `actturn`."""
    return A.РЕЧЬ[язык]["отказ"].split(" — ", 1)[1]


def _фр(язык, строка):
    return frgram.элизия(строка) if язык == "fr" else строка


def _ступени(язык, акт, **п):
    """(приказ, инфинитив, zu-инфинитив, отчёт) акта с подставленными объектами."""
    формы = РЕЧЬ[язык][акт]
    imp, inf, past = (ф.format(**п) for ф in формы[:3])
    zu = формы[3].format(**п) if len(формы) > 3 else inf
    return imp, inf, zu, past


def приказ(язык, регистр, акт, **п):
    imp, inf, _zu, _past = _ступени(язык, акт, **п)
    return _фр(язык, РЕЧЬ[язык]["регистры"][регистр].format(imp=imp, inf=inf))


def предложение(язык, акт, **п):
    _imp, inf, zu, _past = _ступени(язык, акт, **п)
    return _фр(язык, РЕЧЬ[язык]["предложение"].format(inf=inf, zu=zu) + ". " + _вопрос_предложения(язык))


def отчёт(язык, акт, **п):
    _imp, _inf, _zu, past = _ступени(язык, акт, **п)
    return _фр(язык, РЕЧЬ[язык]["отчёт"].format(past=past))


def _с(язык, фраза, **п):
    return _фр(язык, РЕЧЬ[язык][фраза].format(**п))


def наблюдение(язык, фраза, счёт):
    """«<фраза>: <леджер>.» — наблюдение мира с пересчётом (двоеточие — пакетное, у двери `actturn`)."""
    return фраза + A.РЕЧЬ[язык]["двоеточие"] + счёт + "."


# ======================================================================================================
# СТРАНИЦЫ — всякое число вычислено из мира; части, какие меняются, приходят готовыми строками
# ======================================================================================================
def ход(язык, приказ_, предложение_, да, отчёт_):
    """Ход в четыре реплики: приказ · предложение с вопросом · слово · отчёт с наблюдением."""
    р = A.РЕЧЬ[язык]
    слово = р["да"] if да else р["нет"]
    return " ".join((_р(язык, "польз", приказ_), _р(язык, "орг", предложение_), _р(язык, "польз", слово + "."),
                     _р(язык, "орг", отчёт_)))


def невозможный(язык, приказ_, причина, наблюдение_):
    """Невозможный акт — две реплики: приказ · отказ мира по имени и его наблюдение (форма рынка, М-504)."""
    return " ".join((_р(язык, "польз", приказ_), _р(язык, "орг", причина + ". " + наблюдение_)))


def вопрос_и_наблюдение(язык, вопрос, наблюдение_):
    return " ".join((_р(язык, "польз", вопрос), _р(язык, "орг", наблюдение_)))


def слова(строка):
    return строка.split()


def встреч(язык, файл, слово):
    return sum(слова(с).count(слово) for с in СОДЕРЖИМОЕ[язык][файл][0])


def строки_со_словом(язык, файл, слово):
    return [i + 1 for i, с in enumerate(СОДЕРЖИМОЕ[язык][файл][0]) if слово in слова(с)]


def _встречается(язык, w, f, N):
    """«the word "milk" occurs 2 times in the file notes.md» — N приходит готовой счётной фразой."""
    return _с(язык, "встречается", w=кавычки(язык, w), f=f, N=N)


def _файл_строк(язык, f, N):
    return A.РЕЧЬ[язык]["в_файле"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=f), B=N)


def _папка(язык, N):
    return A.РЕЧЬ[язык]["папка"].format(N=N)


def _запуски(язык, N, L):
    return наблюдение(язык, A.РЕЧЬ_ЗАПУСКА[язык]["мир"].format(N=N), L)


# СБОРКА СТРАНИЦ: части, какие меняются, приходят ГОТОВЫМИ строками (слово, файл, счётная фраза, леджер), и
# сборка не считает ничего. Мир считает обёртка ниже, суд — сам: он подаёт в ту же сборку свои метки и
# получает рамку дома, а числа сверяет со своим пересчётом мира (дом не судит себя своим счётом).
def сборка_поиска(язык, род, регистр, w, f, N, L):
    п = dict(w=кавычки(язык, w), f=f)
    хвост = наблюдение(язык, _встречается(язык, w, f, N), L)
    if род == ПОИСК_ВОПРОС:
        return вопрос_и_наблюдение(язык, _с(язык, "вопрос_раз", **п), хвост)
    да = род == ПОИСК
    итог = (отчёт(язык, "поиск", **п) + ". " + хвост) if да else (A.РЕЧЬ[язык]["отказ"] + ". " + хвост)
    return ход(язык, приказ(язык, регистр, "поиск", **п), предложение(язык, "поиск", **п), да, итог)


def сборка_строк(язык, регистр, w, f, поз, N, L):
    п = dict(w=кавычки(язык, w), f=f)
    части = [отчёт(язык, "строки", **п) + "."]
    if поз:
        части.append(_фр(язык, РЕЧЬ[язык]["позиция"][len(поз) - 1].format(w=п["w"], a=поз[0], b=поз[-1])) + ".")
    части.append(наблюдение(язык, _с(язык, "строк_со_словом", f=f, w=п["w"], N=N), L))
    return ход(язык, приказ(язык, регистр, "строки", **п), предложение(язык, "строки", **п), True, " ".join(части))


def сборка_замены(язык, род, регистр, w, v, f, N0, L0, N1=None, L1=None):
    п = dict(w=кавычки(язык, w), v=кавычки(язык, v), f=f)
    старое = наблюдение(язык, _встречается(язык, w, f, N0), L0)
    if род == ЗАМЕНА_НЕЧЕГО:
        причина = _с(язык, "нет_слова", w=п["w"], f=f) + " — " + _хвост_отказа(язык)
        return невозможный(язык, приказ(язык, регистр, "замена", **п), причина, старое)
    if род == ЗАМЕНА_ОТКАЗ:
        итог = A.РЕЧЬ[язык]["отказ"] + ". " + старое
        return ход(язык, приказ(язык, регистр, "замена", **п), предложение(язык, "замена", **п), False, итог)
    итог = (отчёт(язык, "замена", **п) + ". " + старое + " "
            + наблюдение(язык, _встречается(язык, v, f, N1), L1))
    return ход(язык, приказ(язык, регистр, "замена", **п), предложение(язык, "замена", **п), True, итог)


def сборка_дописать(язык, род, регистр, s, f, N, L):
    п = dict(s=кавычки(язык, s), f=f)
    if род == ДОПИСАТЬ_НЕТ:
        причина = A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
        return невозможный(язык, приказ(язык, регистр, "дописать", **п), причина,
                           наблюдение(язык, _папка(язык, N), L))
    да = род == ДОПИСАТЬ
    хвост = наблюдение(язык, _файл_строк(язык, f, N), L)
    итог = (отчёт(язык, "дописать", **п) + ". " + хвост) if да else (A.РЕЧЬ[язык]["отказ"] + ". " + хвост)
    return ход(язык, приказ(язык, регистр, "дописать", **п), предложение(язык, "дописать", **п), да, итог)


def сборка_имени(язык, род, регистр, f, g, N, L):
    п = dict(f=f, g=g)
    папка = наблюдение(язык, _папка(язык, N), L)
    if род == ИМЯ_ЗАНЯТО:
        причина = A.РЕЧЬ[язык]["есть"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=g))
        return невозможный(язык, приказ(язык, регистр, "переименовать", **п), причина, папка)
    if род == ИМЯ_НЕТ:
        причина = A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
        return невозможный(язык, приказ(язык, регистр, "переименовать", **п), причина, папка)
    итог = отчёт(язык, "переименовать", **п) + ". " + папка
    return ход(язык, приказ(язык, регистр, "переименовать", **п), предложение(язык, "переименовать", **п), True,
               итог)


def сборка_переноса(язык, регистр, f, N0, L0, N1, L1):
    п = dict(f=f)
    итог = (отчёт(язык, "перенести", **п) + ". " + наблюдение(язык, _папка(язык, N0), L0) + " "
            + наблюдение(язык, _с(язык, "архив", N=N1), L1))
    return ход(язык, приказ(язык, регистр, "перенести", **п), предложение(язык, "перенести", **п), True, итог)


def сборка_прогона(язык, род, регистр, t, П, L0, исход, N, L):
    п = dict(t=t)
    if род == ПРОГОН_ОТКАЗ:
        итог = A.РЕЧЬ[язык]["отказ"] + ". " + _запуски(язык, N, L)
        return ход(язык, приказ(язык, регистр, "тесты", **п), предложение(язык, "тесты", **п), False, итог)
    итог = (отчёт(язык, "тесты", **п) + ". " + наблюдение(язык, П, L0) + " " + исход + ". "
            + _запуски(язык, N, L))
    return ход(язык, приказ(язык, регистр, "тесты", **п), предложение(язык, "тесты", **п), True, итог)


def _план(язык, ключ, **п):
    приказ_, предложение_ = (_фр(язык, х.format(**п)) for х in РЕЧЬ[язык][ключ])
    return приказ_ + ".", предложение_ + ". " + _вопрос_предложения(язык)


def сборка_плана_замены(язык, род, w, v, f, Nk, L=None, N0=None, N1=None, L1=None):
    п = dict(w=кавычки(язык, w), v=кавычки(язык, v), f=f)
    приказ_, предложение_ = _план(язык, "план_замены", **п)
    if род == ПЛАН_ЗАМЕНЫ_ОТКАЗ:
        итог = A.РЕЧЬ[язык]["отказ"] + ". " + наблюдение(язык, _встречается(язык, w, f, Nk), L)
        return ход(язык, приказ_, предложение_, False, итог)
    итог = " ".join((
        _встречается(язык, w, f, Nk) + ".",
        отчёт(язык, "замена", **п) + ".",
        _с(язык, "проверил", f=f) + A.РЕЧЬ[язык]["двоеточие"] + _встречается(язык, w, f, N0) + ".",
        наблюдение(язык, _встречается(язык, v, f, N1), L1)))
    return ход(язык, приказ_, предложение_, True, итог)


def сборка_плана_выпуска(язык, t, П, L0, выпуск, N, L):
    приказ_, предложение_ = _план(язык, "план_тестов", t=t)
    итог = (отчёт(язык, "тесты", t=t) + ". " + наблюдение(язык, П, L0) + " " + выпуск + ". "
            + _запуски(язык, N, L))
    return ход(язык, приказ_, предложение_, True, итог)


# МИР СЧИТАЕТ: обёртки берут числа у объявленного мира и отдают сборке готовые части
def _л(было, сдвиг):
    return A.леджер(было, сдвиг)


def страница_поиска(язык, род, регистр, f, w):
    k = встреч(язык, f, w)
    return сборка_поиска(язык, род, регистр, w, f, раз(язык, k), _л(k, 0)[0])


def страница_строк(язык, регистр, f, w):
    поз = строки_со_словом(язык, f, w)
    return сборка_строк(язык, регистр, w, f, tuple(str(x) for x in поз), строк(язык, len(поз)), _л(len(поз), 0)[0])


def страница_замены(язык, род, регистр, f, w, v):
    k, a = встреч(язык, f, w), встреч(язык, f, v)
    if род == ЗАМЕНА_НЕЧЕГО:
        return сборка_замены(язык, род, регистр, w, v, f, раз(язык, 0), _л(0, 0)[0])
    if род == ЗАМЕНА_ОТКАЗ:
        return сборка_замены(язык, род, регистр, w, v, f, раз(язык, k), _л(k, 0)[0])
    return сборка_замены(язык, род, регистр, w, v, f, раз(язык, 0), _л(k, -k)[0], раз(язык, a + k), _л(a, k)[0])


def страница_дописать(язык, род, регистр, f, s):
    if род == ДОПИСАТЬ_НЕТ:
        return сборка_дописать(язык, род, регистр, s, f, A.файлов(язык, ПАПКА), _л(ПАПКА, 0)[0])
    n = len(СОДЕРЖИМОЕ[язык][f][0])
    счёт, стало = _л(n, 1 if род == ДОПИСАТЬ else 0)
    return сборка_дописать(язык, род, регистр, s, f, строк(язык, стало), счёт)


def страница_имени(язык, род, регистр, f, g):
    return сборка_имени(язык, род, регистр, f, g, A.файлов(язык, ПАПКА), _л(ПАПКА, 0)[0])


def страница_переноса(язык, регистр, f, c):
    счёт_п, стало_п = _л(ПАПКА, -1)
    счёт_а, стало_а = _л(c, 1)
    return сборка_переноса(язык, регистр, f, A.файлов(язык, стало_п), счёт_п, A.файлов(язык, стало_а), счёт_а)


def исход_прогона(язык, t, фраза):
    """(фраза «прошло P из T», леджер «T − F = P», исход по-объявленному) — из объявления мира."""
    т, падает = ТЕСТЫ[t]
    return прошло(язык, т - падает, т), _л(т, -падает)[0], _фр(язык, РЕЧЬ[язык][фраза][0 if падает == 0 else 1])


def страница_прогона(язык, род, регистр, t, было):
    счёт, стало = _л(было, 0 if род == ПРОГОН_ОТКАЗ else 1)
    П, L0, исход = исход_прогона(язык, t, "итог")
    return сборка_прогона(язык, род, регистр, t, П, L0, исход, A.запусков(язык, стало), счёт)


def страница_плана_замены(язык, род, f, w, v):
    k, a = встреч(язык, f, w), встреч(язык, f, v)
    if род == ПЛАН_ЗАМЕНЫ_ОТКАЗ:
        return сборка_плана_замены(язык, род, w, v, f, раз(язык, k), _л(k, 0)[0])
    return сборка_плана_замены(язык, род, w, v, f, раз(язык, k), None, раз(язык, 0), раз(язык, a + k), _л(a, k)[0])


def страница_плана_выпуска(язык, t, было):
    счёт, стало = _л(было, 1)
    П, L0, выпуск = исход_прогона(язык, t, "выпуск")
    return сборка_плана_выпуска(язык, t, П, L0, выпуск, A.запусков(язык, стало), счёт)


# ======================================================================================================
# ПОКАЗЫ
# ======================================================================================================
def _регистры(род):
    return РЕГИСТРЫ if род in С_РЕГИСТРАМИ else РЕГИСТРЫ[:1]


def _показы():
    вон = {}

    def положить(стр, язык, род, регистр):
        вон.setdefault(стр, (язык, род, регистр))

    for язык in ЯЗЫКИ:
        for i, f in enumerate(ТЕКСТЫ):
            строки_, искомые, замены, нет_слова, новые = СОДЕРЖИМОЕ[язык][f]
            for w in искомые:
                for р in _регистры(ПОИСК):
                    положить(страница_поиска(язык, ПОИСК, р, f, w), язык, ПОИСК, р)
                    положить(страница_строк(язык, р, f, w), язык, СТРОКИ, р)
                положить(страница_поиска(язык, ПОИСК_ВОПРОС, "плоский", f, w), язык, ПОИСК_ВОПРОС, "плоский")
            for w in искомые[:2]:
                положить(страница_поиска(язык, ПОИСК_ОТКАЗ, "плоский", f, w), язык, ПОИСК_ОТКАЗ, "плоский")
            for w, v in замены:
                for р in _регистры(ЗАМЕНА):
                    положить(страница_замены(язык, ЗАМЕНА, р, f, w, v), язык, ЗАМЕНА, р)
                положить(страница_замены(язык, ЗАМЕНА_ОТКАЗ, "плоский", f, w, v), язык, ЗАМЕНА_ОТКАЗ, "плоский")
                положить(страница_плана_замены(язык, ПЛАН_ЗАМЕНЫ, f, w, v), язык, ПЛАН_ЗАМЕНЫ, "плоский")
            положить(страница_плана_замены(язык, ПЛАН_ЗАМЕНЫ_ОТКАЗ, f, *замены[0]), язык, ПЛАН_ЗАМЕНЫ_ОТКАЗ,
                     "плоский")
            for р in _регистры(ЗАМЕНА_НЕЧЕГО):
                положить(страница_замены(язык, ЗАМЕНА_НЕЧЕГО, р, f, *нет_слова), язык, ЗАМЕНА_НЕЧЕГО, р)
            for s in новые:
                for р in _регистры(ДОПИСАТЬ):
                    положить(страница_дописать(язык, ДОПИСАТЬ, р, f, s), язык, ДОПИСАТЬ, р)
                положить(страница_дописать(язык, ДОПИСАТЬ_ОТКАЗ, "плоский", f, s), язык, ДОПИСАТЬ_ОТКАЗ, "плоский")
            for g in НОВЫЕ_ИМЕНА[f]:
                for р in _регистры(ИМЯ):
                    положить(страница_имени(язык, ИМЯ, р, f, g), язык, ИМЯ, р)
            for р in _регистры(ИМЯ_ЗАНЯТО):
                положить(страница_имени(язык, ИМЯ_ЗАНЯТО, р, f, ЗАНЯТОЕ[f]), язык, ИМЯ_ЗАНЯТО, р)
                положить(страница_переноса(язык, р, f, АРХИВ_ДО[i]), язык, ПЕРЕНОС, р)
        for р in _регистры(ДОПИСАТЬ_НЕТ):
            for s in СОДЕРЖИМОЕ[язык][ТЕКСТЫ[0]][4]:
                положить(страница_дописать(язык, ДОПИСАТЬ_НЕТ, р, НЕТ_ФАЙЛА[0], s), язык, ДОПИСАТЬ_НЕТ, р)
            положить(страница_имени(язык, ИМЯ_НЕТ, р, *НЕТ_ФАЙЛА), язык, ИМЯ_НЕТ, р)
        for t in ТЕСТЫ:
            for было in ВЫПУСКИ_ДО:
                for р in _регистры(ПРОГОН):
                    положить(страница_прогона(язык, ПРОГОН, р, t, было), язык, ПРОГОН, р)
                положить(страница_плана_выпуска(язык, t, было), язык, ПЛАН_ВЫПУСКА, "плоский")
            for было in ВЫПУСКИ_ДО[:2]:
                положить(страница_прогона(язык, ПРОГОН_ОТКАЗ, "плоский", t, было), язык, ПРОГОН_ОТКАЗ, "плоский")
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_мира():
    """Мир объявлен так, как дом о нём говорит: искомые стоят 2, 1 и 0 раз, заменяемое есть, «нечего» — нет."""
    for язык in ЯЗЫКИ:
        for f in ТЕКСТЫ:
            строки_, искомые, замены, нет_слова, новые = СОДЕРЖИМОЕ[язык][f]
            assert len(строки_) == 3, (язык, f)
            assert [встреч(язык, f, w) for w in искомые] == [2, 1, 0], (язык, f, искомые)
            assert [len(строки_со_словом(язык, f, w)) for w in искомые] == [2, 1, 0], (язык, f)
            assert all(встреч(язык, f, w) > 0 for w, _v in замены), (язык, f, замены)
            assert встреч(язык, f, нет_слова[0]) == 0, (язык, f, нет_слова)
            assert all(not any(ch.isdigit() for ch in s) for s in строки_ + новые), (язык, f)
    assert НЕТ_ФАЙЛА[0] not in ТЕКСТЫ and НЕТ_ФАЙЛА[0] not in ТЕСТЫ
    assert all(g not in ТЕКСТЫ and g not in ТЕСТЫ for гг in НОВЫЕ_ИМЕНА.values() for g in гг)
    assert all(ЗАНЯТОЕ[f] in ТЕКСТЫ and ЗАНЯТОЕ[f] != f for f in ТЕКСТЫ)


_самопроверка_мира()


def _самопроверка():
    """Всякий род кован на всяком языке; всякий вопрос предложения и приказ вопросом начат объявленным зачином."""
    import asking  # noqa: PLC0415 — дом пары объявляет зачины вопросов
    по_роду = {}
    for стр, (язык, род, _р) in ПОКАЗЫ.items():
        по_роду.setdefault(род, set()).add(язык)
        for фраза in re.split(r"(?<=[.?!])\s+", стр):
            вопрос = re.sub(r"^[^\s:]+ ?: ", "", фраза.strip())
            if вопрос.endswith("?") and asking.зачин_объявлен(вопрос) is False:
                raise AssertionError(f"незачинный вопрос: {язык} · {вопрос}")
    пустые = [р for р in РОДЫ if по_роду.get(р) != set(ЯЗЫКИ)]
    assert not пустые, f"род не кован на всех языках: {пустые}"
    for язык in ("ru", "en", "de", "fr", "pl"):
        for стр, (я, род, р) in ПОКАЗЫ.items():
            if я == язык and род in (ЗАМЕНА, ПРОГОН) and р == "плоский":
                print("  ", стр)
                break
    сч = {р: sum(1 for _я, род, _р in ПОКАЗЫ.values() if род == р) for р in РОДЫ}
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}): "
          + ", ".join(f"{р} {к}" for р, к in сч.items()))


if __name__ == "__main__":
    _самопроверка()
