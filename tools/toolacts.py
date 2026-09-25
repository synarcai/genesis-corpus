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
import plgram  # noqa: E402 — польский винительный при единице («zawiera 1 linię»)
import rugram  # noqa: E402 — русские формы «раз» и «строка» при числе и винительный при числе
import svampforms as S  # noqa: E402 — счётная ячейка пакета

ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# МИР: папка из шести файлов — три текстовых и три тестовых; содержимое текстовых — на языке страницы
# ======================================================================================================
ТЕКСТЫ = ("notes.md", "todo.txt", "manual.md")
# ТЕСТЫ: файл → (тестов, падает) — исход прогона объявлен миром и один при всяком прогоне
ТЕСТЫ = {"test_notes.py": (5, 1), "test_todo.py": (6, 0), "test_manual.py": (4, 2)}
ПАПКА = len(ТЕКСТЫ) + len(ТЕСТЫ)
ВЫПУСКИ_ДО = (0, 1, 3)          # запусков мира до прогона — леджер запусков (дверь `actturn`)
АРХИВ = "archive"               # папка переноса — имя мира, как имена файлов
АРХИВ_ДО = (0, 1, 2)            # файлов в папке archive до переноса — по файлу
НОВЫЕ_ИМЕНА = {"notes.md": ("shopping.md", "list.md"), "todo.txt": ("tasks.txt", "plan.txt"),
               "manual.md": ("about.md", "info.md")}
ЗАНЯТОЕ = {"notes.md": "todo.txt", "todo.txt": "manual.md", "manual.md": "notes.md"}
НЕТ_ФАЙЛА = ("sketch.md", "final.md")   # файла sketch.md в мире нет; final.md — имя, в которое его зовут

# (строки файла; искомые: дважды, однажды, ни разу; три замены; слово, которого нет, и чем его заменить;
#  две строки для дописывания)
СОДЕРЖИМОЕ = {
    "en": {"notes.md": (("get cheese", "call the bank", "get bread and cheese"), ("cheese", "bank", "tea"),
                        (("cheese", "butter"), ("bank", "shop"), ("bread", "cheese")), ("tea", "coffee"),
                        ("get eggs", "call the school")),
           "todo.txt": (("fix the lamp", "water the plants", "fix the door"), ("fix", "plants", "paint"),
                        (("fix", "check"), ("lamp", "clock"), ("door", "lamp")), ("paint", "glue"),
                        ("clean the room", "fix the tap")),
           "manual.md": (("the tool reads pages", "the tool counts words", "the report lists pages"),
                         ("pages", "words", "code"), (("pages", "notes"), ("words", "names"), ("report", "tool")),
                         ("code", "data"), ("the tool finds words", "the report counts notes"))},
    "ru": {"notes.md": (("купить молоко", "позвонить в банк", "купить хлеб и молоко"), ("молоко", "банк", "чай"),
                        (("молоко", "сок"), ("банк", "магазин"), ("хлеб", "молоко")), ("чай", "кофе"),
                        ("купить яйца", "позвонить в школу")),
           "todo.txt": (("починить лампу", "полить цветы", "починить дверь"), ("починить", "цветы", "краску"),
                        (("починить", "проверить"), ("лампу", "полку"), ("дверь", "лампу")), ("краску", "клей"),
                        ("убрать комнату", "починить кран")),
           "manual.md": (("программа читает файлы", "программа считает слова", "отчёт перечисляет файлы"),
                         ("файлы", "слова", "код"), (("файлы", "страницы"), ("слова", "имена"),
                                                    ("отчёт", "программа")),
                         ("код", "шрифт"), ("программа ищет слова", "отчёт считает страницы"))},
    "de": {"notes.md": (("Milch kaufen", "die Bank anrufen", "Brot und Milch kaufen"), ("Milch", "Bank", "Tee"),
                        (("Milch", "Saft"), ("Bank", "Post"), ("Brot", "Milch")), ("Tee", "Kaffee"),
                        ("Eier kaufen", "die Schule anrufen")),
           "todo.txt": (("die Lampe reparieren", "die Pflanzen gießen", "die Tür reparieren"),
                        ("reparieren", "Pflanzen", "Farbe"),
                        (("reparieren", "prüfen"), ("Lampe", "Uhr"), ("Tür", "Lampe")), ("Farbe", "Leim"),
                        ("das Zimmer aufräumen", "den Hahn reparieren")),
           "manual.md": (("das Programm liest Dateien", "das Programm zählt Wörter", "der Bericht listet Dateien"),
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
           "manual.md": (("le programme lit les fichiers", "le programme compte les mots",
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
           "manual.md": (("el programa lee archivos", "el programa cuenta palabras", "el informe lista archivos"),
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
           "manual.md": (("il programma legge i documenti", "il programma conta le parole",
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
           "manual.md": (("o programa lê ficheiros", "o programa conta palavras", "o relatório lista ficheiros"),
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
           "manual.md": (("het programma leest bestanden", "het programma telt woorden", "het rapport toont bestanden"),
                         ("bestanden", "woorden", "code"), (("bestanden", "teksten"), ("woorden", "namen"),
                                                           ("rapport", "programma")),
                         ("code", "tekst"), ("het programma zoekt woorden", "het rapport telt teksten"))},
    "pl": {"notes.md": (("kupić mleko", "zadzwonić do banku", "kupić chleb i mleko"), ("mleko", "banku", "herbata"),
                        (("mleko", "sok"), ("banku", "sklepu"), ("chleb", "mleko")), ("herbata", "kawa"),
                        ("kupić jajka", "zadzwonić do szkoły")),
           "todo.txt": (("naprawić lampę", "podlać rośliny", "naprawić drzwi"), ("naprawić", "rośliny", "farba"),
                        (("naprawić", "sprawdzić"), ("lampę", "półkę"), ("drzwi", "lampę")), ("farba", "klej"),
                        ("posprzątać pokój", "naprawić kran")),
           "manual.md": (("program czyta pliki", "program liczy słowa", "raport wymienia pliki"),
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
# русская тройка строки — у двери `rugram` (там же её винительный при числе), как и «раз»
СТРОК = {"en": ("line", "lines"), "de": ("Zeile", "Zeilen"),
         "fr": ("ligne", "lignes"), "es": ("línea", "líneas"), "it": ("riga", "righe"), "pt": ("linha", "linhas"),
         "nl": ("regel", "regels"), "pl": ("linia", "linie", "linii")}
ТЕСТ = {"ru": ("тест", "теста", "тестов"), "en": ("test", "tests"), "de": ("Test", "Tests"), "fr": ("test", "tests"),
        "es": ("prueba", "pruebas"), "it": ("test", "test"), "pt": ("teste", "testes"), "nl": ("test", "tests"),
        "pl": ("test", "testy", "testów")}
# СОГЛАСИЕ ИСХОДА С ЧИСЛОМ ПРОШЕДШИХ — ячейкой пакета, как счётное слово («1 test sur 5 réussi»)
ПРОШЛО = {"ru": ("пройден", "пройдено", "пройдено"), "fr": ("réussi", "réussis"), "es": ("superada", "superadas"),
          "it": ("superato", "superati"), "pt": ("passou", "passaram")}

# ФРАЗЫ ОБЪЕКТОВ — ОДНА ДВЕРЬ (25.09, дом актов v2 `toolrepo`): слово и текст в кавычках, файл, строка, тесты
# файла, папка — В ПАДЕЖЕ, КАКОГО ПРОСИТ ШАБЛОН АКТА. Шаблон акта держит слот (`{W}`, `{М}`, `{Ф}`…), а не
# готовое «the word {w} … in the file {f}»: так приказ можно сказать и без «the file», и с «the text» вместо
# «the word», а предложение и отчёт — одной канонической фразой. Первая фраза кортежа — каноническая (ею
# говорят предложение и отчёт), прочие — формы приказа («to {d}», «into the {d} folder»). Файл в винительном —
# у двери хода `actturn`; падеж «нет» — тот, какого просит отрицание («слова {w} нет», «das Wort {w} steht
# nicht», «słowa {w} nie ma»).
ОБЪЕКТЫ = {
    "en": dict(слово=dict(в="the word {w}", и="the word {w}", нет="the word {w}"),
               текст=dict(в="the text {w}", и="the text {w}", нет="the text {w}"),
               в_файле=("in the file {f}", "in {f}"), в_файл=("to the file {f}", "to {f}"),
               файл_имени=("the file {f}", "{f}"), файла=("of the file {f}", "of {f}"),
               строку=("the line {s}", "{s}"), тесты_файла=("the tests in the file {t}", "the tests in {t}"),
               в_папку=("to the folder {d}", "to {d}", "into the folder {d}", "into the {d} folder",
                        "to the {d} folder"),
               в_папке=("in the folder {d}", "in {d}", "in the {d} folder"),
               из_папки=("from the folder {d}", "from the {d} folder"),
               папка_имя="the folder {d} contains {N}"),
    "ru": dict(слово=dict(в="слово {w}", и="слово {w}", нет="слова {w}"),
               текст=dict(в="текст {w}", и="текст {w}", нет="текста {w}"),
               в_файле=("в файле {f}", "в {f}"), в_файл=("в файл {f}", "в {f}"),
               файл_имени=("файл {f}", "{f}"), файла=("файла {f}", "{f}"),
               строку=("строку {s}", "{s}"), тесты_файла=("тесты из файла {t}", "тесты из {t}"),
               в_папку=("в папку {d}", "в {d}"), в_папке=("в папке {d}", "в {d}"), из_папки=("из папки {d}",),
               папка_имя="папка {d} содержит {N}"),
    "de": dict(слово=dict(в="das Wort {w}", и="das Wort {w}", нет="das Wort {w}"),
               текст=dict(в="den Text {w}", и="der Text {w}", нет="der Text {w}"),
               в_файле=("in der Datei {f}", "in {f}"), в_файл=("die Datei {f}", "{f}"),
               файл_имени=("der Datei {f}", "{f}"), файла=("der Datei {f}", "von {f}"),
               строку=("die Zeile {s}", "{s}"), тесты_файла=("die Tests aus der Datei {t}", "die Tests aus {t}"),
               в_папку=("in den Ordner {d}", "nach {d}"), в_папке=("im Ordner {d}", "in {d}"),
               из_папки=("aus dem Ordner {d}",), папка_имя="der Ordner {d} enthält {N}"),
    "fr": dict(слово=dict(в="le mot {w}", и="le mot {w}", нет="le mot {w}"),
               текст=dict(в="le texte {w}", и="le texte {w}", нет="le texte {w}"),
               в_файле=("dans le fichier {f}", "dans {f}"), в_файл=("au fichier {f}", "à {f}"),
               файл_имени=("le fichier {f}", "{f}"), файла=("du fichier {f}", "de {f}"),
               строку=("la ligne {s}", "{s}"), тесты_файла=("les tests du fichier {t}", "les tests de {t}"),
               в_папку=("dans le dossier {d}", "dans {d}", "vers le dossier {d}"),
               в_папке=("dans le dossier {d}", "dans {d}"), из_папки=("du dossier {d}",),
               папка_имя="le dossier {d} contient {N}"),
    "es": dict(слово=dict(в="la palabra {w}", и="la palabra {w}", нет="la palabra {w}"),
               текст=dict(в="el texto {w}", и="el texto {w}", нет="el texto {w}"),
               в_файле=("en el archivo {f}", "en {f}"), в_файл=("al archivo {f}", "a {f}"),
               файл_имени=("el archivo {f}", "{f}"), файла=("del archivo {f}", "de {f}"),
               строку=("la línea {s}", "{s}"), тесты_файла=("las pruebas del archivo {t}", "las pruebas de {t}"),
               в_папку=("a la carpeta {d}", "a {d}"), в_папке=("en la carpeta {d}", "en {d}"),
               из_папки=("de la carpeta {d}",), папка_имя="la carpeta {d} contiene {N}"),
    "it": dict(слово=dict(в="la parola {w}", и="la parola {w}", нет="la parola {w}"),
               текст=dict(в="il testo {w}", и="il testo {w}", нет="il testo {w}"),
               в_файле=("nel file {f}", "in {f}"), в_файл=("al file {f}", "a {f}"),
               файл_имени=("il file {f}", "{f}"), файла=("del file {f}", "di {f}"),
               строку=("la riga {s}", "{s}"), тесты_файла=("i test del file {t}", "i test di {t}"),
               в_папку=("nella cartella {d}", "in {d}"), в_папке=("nella cartella {d}", "in {d}"),
               из_папки=("dalla cartella {d}",), папка_имя="la cartella {d} contiene {N}"),
    "pt": dict(слово=dict(в="a palavra {w}", и="a palavra {w}", нет="a palavra {w}"),
               текст=dict(в="o texto {w}", и="o texto {w}", нет="o texto {w}"),
               в_файле=("no ficheiro {f}", "em {f}"), в_файл=("ao ficheiro {f}", "a {f}"),
               файл_имени=("o ficheiro {f}", "{f}"), файла=("do ficheiro {f}", "de {f}"),
               строку=("a linha {s}", "{s}"), тесты_файла=("os testes do ficheiro {t}", "os testes de {t}"),
               в_папку=("para a pasta {d}", "para {d}"), в_папке=("na pasta {d}", "em {d}"),
               из_папки=("da pasta {d}",), папка_имя="a pasta {d} contém {N}"),
    "nl": dict(слово=dict(в="het woord {w}", и="het woord {w}", нет="het woord {w}"),
               текст=dict(в="de tekst {w}", и="de tekst {w}", нет="de tekst {w}"),
               в_файле=("in het bestand {f}", "in {f}"), в_файл=("onderaan het bestand {f}", "onderaan {f}"),
               файл_имени=("het bestand {f}", "{f}"), файла=("van het bestand {f}", "van {f}"),
               строку=("de regel {s}", "{s}"), тесты_файла=("de tests uit het bestand {t}", "de tests uit {t}"),
               в_папку=("naar de map {d}", "naar {d}"), в_папке=("in de map {d}", "in {d}"),
               из_папки=("uit de map {d}",), папка_имя="de map {d} bevat {N}"),
    "pl": dict(слово=dict(в="słowo {w}", и="słowo {w}", нет="słowa {w}"),
               текст=dict(в="tekst {w}", и="tekst {w}", нет="tekstu {w}"),
               в_файле=("w pliku {f}", "w {f}"), в_файл=("do pliku {f}", "do {f}"),
               файл_имени=("pliku {f}", "{f}"), файла=("pliku {f}", "{f}"),
               строку=("linię {s}", "{s}"), тесты_файла=("testy z pliku {t}", "testy z {t}"),
               в_папку=("do folderu {d}", "do {d}"), в_папке=("w folderze {d}", "w {d}"),
               из_папки=("z folderu {d}",), папка_имя="folder {d} zawiera {N}"),
}
for _я, _о in ОБЪЕКТЫ.items():
    # файл в винительном — фраза двери хода: «the file {f}», «файл {f}», «die Datei {f}»
    _о["файл_вин"] = (A.РЕЧЬ[_я]["файл"], "{f}")
# СЛОТ ШАБЛОНА → (имя части, фраза двери[, падеж]): слот, какого не подали готовым, строится из части
# канонической фразой — так прежние вызовы («w=…, f=…») говорят прежние строки байт в байт
_СЛОТЫ = {"W": ("w", "слово", "в"), "Wи": ("w", "слово", "и"), "Wнет": ("w", "слово", "нет"),
          "М": ("f", "в_файле"), "К": ("f", "в_файл"), "Ф": ("f", "файл_вин"), "Фи": ("f", "файл_имени"),
          "S": ("s", "строку"), "Т": ("t", "тесты_файла"), "Д": ("d", "в_папку")}


def слоты(язык, **п):
    """Части приказа с фразами объектов: поданная готовой фраза (форма приказа) остаётся, прочие — канонические."""
    о = ОБЪЕКТЫ[язык]
    вон = dict(п)
    for слот, (часть, фраза, *падеж) in _СЛОТЫ.items():
        if слот in вон or часть not in п:
            continue
        шаблон = о[фраза][падеж[0]] if падеж else о[фраза][0]
        вон[слот] = шаблон.format(**{часть: п[часть]})
    return вон


# ПЛАН ИЗ ДВУХ АКТОВ — связка приказа и предложения: «{A}, then {B}», «i propose two acts: {A}, then {B}». {B1} —
# глагол второго приказа, {B2} — остаток: нидерландское наречие стоит ПОСЛЕ глагола повеления («… en publiceer
# daarna de release»), и шаблон говорит это сам, без ветки языка в коде
СВЯЗКА = {
    "en": ("{A}, then {B1} {B2}", "i propose two acts: {A}, then {B}"),
    "ru": ("{A}, затем {B1} {B2}", "предлагаю два акта: {A}, затем {B}"),
    "de": ("{A}, dann {B1} {B2}", "ich schlage zwei Handlungen vor: {A}, dann {B}"),
    "fr": ("{A}, puis {B1} {B2}", "je propose deux actes : {A}, puis {B}"),
    "es": ("{A}, luego {B1} {B2}", "propongo dos actos: {A}, luego {B}"),
    "it": ("{A}, poi {B1} {B2}", "propongo due atti: {A}, poi {B}"),
    "pt": ("{A}, depois {B1} {B2}", "proponho dois atos: {A}, depois {B}"),
    "nl": ("{A} en {B1} daarna {B2}", "ik stel twee handelingen voor: {A} en daarna {B}"),
    "pl": ("{A}, potem {B1} {B2}", "proponuję dwa akty: {A}, potem {B}"),
}


def связать(язык, ступень, A, B):
    """Приказ («приказ») или тело предложения («предложение») плана из двух актов. Второй приказ режется по первому
    пробелу — или приходит разрезанным (глагол, остаток), когда глагол держит при себе местоимение («verwijder het»)."""
    приказ_, предложение_ = СВЯЗКА[язык]
    if ступень == "приказ":
        B1, B2 = B if isinstance(B, tuple) else B.split(" ", 1)
        return приказ_.format(A=A, B1=B1, B2=B2).rstrip()
    return предложение_.format(A=A, B=B)


# ПЛАН С МЕСТОИМЕНИЕМ (25.09, вопрос 4 коллегии «ответ мира»; ведущий: роды дома актов `toolrepo`): второй приказ
# называет объект первого местоимением — «create the file X, then append the line "…" to it». Формы приказа —
# (глагол, остаток) для связки: местоимение стоит там, где его ставит язык, и глагол тот же, что у акта двери
# (французское, испанское, итальянское, португальское местоимение пристаёт к глаголу: «ajoute-y», «añádele»).
# Предложение местоимения не повторяет: оно называет путь, какой определяет приказ. «найти» — приказ находки файла
# со словом (глагол поиска двери); «ждёт» — второй акт ждёт одного места, «нет_второго» — первый акт не совершён.
МЕСТОИМЕНИЕ = {
    "en": dict(дописать=("append", "{S} to it"), удалить=("delete", "it"),
               найти=("find the file that contains {W}", "find the file that contains {W}"),
               ждёт="the second act waits for one file", нет_второго="the second act is not performed either"),
    "ru": dict(дописать=("допиши", "в него {S}"), удалить=("удали", "его"),
               найти=("найди файл, в котором есть {Wи}", "найти файл, в котором есть {Wи}"),
               ждёт="второй акт ждёт одного файла", нет_второго="второй акт тоже не совершён"),
    "de": dict(дописать=("ergänze", "sie um {S}"), удалить=("lösche", "sie"),
               найти=("suche die Datei, die {W} enthält", "die Datei suchen, die {W} enthält",
                      "die Datei zu suchen, die {W} enthält"),
               ждёт="die zweite Handlung wartet auf eine Datei",
               нет_второго="die zweite Handlung wird auch nicht ausgeführt"),
    "fr": dict(дописать=("ajoute-y", "{S}"), удалить=("supprime-le", ""),
               найти=("cherche le fichier qui contient {W}", "chercher le fichier qui contient {W}"),
               ждёт="le deuxième acte attend un seul fichier", нет_второго="le deuxième acte n'est pas exécuté non plus"),
    "es": dict(дописать=("añádele", "{S}"), удалить=("elimínalo", ""),
               найти=("busca el archivo que contiene {W}", "buscar el archivo que contiene {W}"),
               ждёт="el segundo acto espera un solo archivo", нет_второго="el segundo acto tampoco se realiza"),
    "it": dict(дописать=("aggiungici", "{S}"), удалить=("eliminalo", ""),
               найти=("cerca il file che contiene {W}", "cercare il file che contiene {W}"),
               ждёт="il secondo atto aspetta un solo file", нет_второго="neanche il secondo atto viene eseguito"),
    "pt": dict(дописать=("acrescenta-lhe", "{S}"), удалить=("elimina-o", ""),
               найти=("procura o ficheiro que contém {W}", "procurar o ficheiro que contém {W}"),
               ждёт="o segundo ato espera um só ficheiro", нет_второго="o segundo ato também não é realizado"),
    "nl": dict(дописать=("zet", "{S} er onderaan"), удалить=("verwijder het", ""),
               найти=("zoek het bestand dat {W} bevat", "het bestand zoeken dat {W} bevat",
                      "het bestand te zoeken dat {W} bevat"),
               ждёт="de tweede handeling wacht op één bestand",
               нет_второго="de tweede handeling wordt ook niet uitgevoerd"),
    "pl": dict(дописать=("dopisz", "do niego {S}"), удалить=("usuń", "go"),
               найти=("znajdź plik, który zawiera {W}", "znaleźć plik, który zawiera {W}"),
               ждёт="drugi akt czeka na jeden plik", нет_второго="drugi akt też nie zostaje wykonany"),
}


def местоимение(язык, акт, **п):
    """(глагол, остаток) второго приказа с местоимением на месте объекта — для связки плана."""
    глагол, остаток = МЕСТОИМЕНИЕ[язык][акт]
    return глагол, остаток.format(**слоты(язык, **п))


def найти(язык, **п):
    """(приказ, инфинитив, zu-инфинитив) находки файла со словом: «find the file that contains the word "x"»."""
    формы = [ф.format(**слоты(язык, **п)) for ф in МЕСТОИМЕНИЕ[язык]["найти"]]
    return формы[0], формы[1], формы[2] if len(формы) > 2 else формы[1]


# акт → (приказ, инфинитив, отчёт) — у de и nl инфинитив с глаголом в конце и «zu/te»-форма предложения
АКТЫ = ("поиск", "строки", "замена", "дописать", "переименовать", "перенести", "тесты")
РЕЧЬ = {
    "en": dict(
        поиск=("find the word {w} in the file {f}", "find the word {w} in the file {f}",
               "searched for the word {w} in the file {f}"),
        строки=("find the lines with the word {w} in the file {f}", "find the lines with the word {w} in the file {f}",
                "searched for the lines with the word {w} in the file {f}"),
        замена=("replace {W} with {v} {М}", "replace {W} with {v} {М}", "replaced {W} with {v} {М}"),
        дописать=("append {S} {К}", "append {S} {К}", "appended {S} {К}"),
        переименовать=("rename {Фи} to {g}", "rename {Фи} to {g}", "renamed {Фи} to {g}"),
        перенести=("move {Ф} {Д}", "move {Ф} {Д}", "moved {Ф} {Д}"),
        тесты=("run {Т}", "run {Т}", "ran {Т}"),
        предложение="i propose to {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="please {imp}.", косвенный="we need to {inf}.",
                      вопросом="could you {inf}?"),
        встречается="{Wи} occurs {N} {М}",
        вопрос_раз="how many times does {Wи} occur {М}?",
        строк_со_словом="the file {f} has {N} with the word {w}",
        позиция=("{Wи} stands in line {a}", "{Wи} stands in lines {a} and {b}"),
        нет_слова="{Wнет} is not {М}",
        проверил="checked the file {f}",
        итог=("the run ended successfully", "the run ended with an error"),
        выпуск=("all tests passed — the release is published", "not all tests passed — the release is not published"),
        план_замены=("find the word {w} in the file {f}, then replace it with {v}, then check the file",
                     "i propose three acts: find the word {w} in the file {f}, replace it with {v}, "
                     "check the file {f}"),
        выпуск_акт=("publish the release if all tests pass", "publish the release if all tests pass")),
    "ru": dict(
        поиск=("найди слово {w} в файле {f}", "найти слово {w} в файле {f}", "искал слово {w} в файле {f}"),
        строки=("найди строки со словом {w} в файле {f}", "найти строки со словом {w} в файле {f}",
                "искал строки со словом {w} в файле {f}"),
        замена=("замени {W} на {v} {М}", "заменить {W} на {v} {М}", "заменил {W} на {v} {М}"),
        дописать=("допиши {S} {К}", "дописать {S} {К}", "дописал {S} {К}"),
        переименовать=("переименуй {Фи} в {g}", "переименовать {Фи} в {g}", "переименовал {Фи} в {g}"),
        перенести=("перенеси {Ф} {Д}", "перенести {Ф} {Д}", "перенёс {Ф} {Д}"),
        тесты=("запусти {Т}", "запустить {Т}", "запустил {Т}"),
        предложение="предлагаю {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="пожалуйста, {imp}.", косвенный="нужно {inf}.",
                      вопросом="ты можешь {inf}?"),
        встречается="{М} {Wи} встречается {N}",
        вопрос_раз="сколько раз {Wи} встречается {М}?",
        строк_со_словом="в файле {f} {N} со словом {w}",
        позиция=("{Wи} стоит в строке {a}", "{Wи} стоит в строках {a} и {b}"),
        нет_слова="{Wнет} нет {М}",
        проверил="проверил файл {f}",
        итог=("запуск завершился успешно", "запуск завершился ошибкой"),
        выпуск=("все тесты пройдены — релиз выпущен", "не все тесты пройдены — релиз не выпущен"),
        план_замены=("найди слово {w} в файле {f}, затем замени его на {v}, затем проверь файл",
                     "предлагаю три акта: найти слово {w} в файле {f}, заменить его на {v}, проверить файл {f}"),
        выпуск_акт=("выпусти релиз, если все тесты пройдут", "выпустить релиз, если все тесты пройдут")),
    "de": dict(
        поиск=("suche das Wort {w} in der Datei {f}", "das Wort {w} in der Datei {f} suchen",
               "das Wort {w} in der Datei {f} gesucht", "das Wort {w} in der Datei {f} zu suchen"),
        строки=("suche die Zeilen mit dem Wort {w} in der Datei {f}",
                "die Zeilen mit dem Wort {w} in der Datei {f} suchen",
                "die Zeilen mit dem Wort {w} in der Datei {f} gesucht",
                "die Zeilen mit dem Wort {w} in der Datei {f} zu suchen"),
        замена=("ersetze {W} {М} durch {v}", "{W} {М} durch {v} ersetzen", "{W} {М} durch {v} ersetzt",
                "{W} {М} durch {v} zu ersetzen"),
        дописать=("ergänze {К} um {S}", "{К} um {S} ergänzen", "{К} um {S} ergänzt", "{К} um {S} zu ergänzen"),
        переименовать=("gib {Фи} den Namen {g}", "{Фи} den Namen {g} geben", "{Фи} den Namen {g} gegeben",
                       "{Фи} den Namen {g} zu geben"),
        перенести=("verschiebe {Ф} {Д}", "{Ф} {Д} verschieben", "{Ф} {Д} verschoben", "{Ф} {Д} zu verschieben"),
        тесты=("starte {Т}", "{Т} starten", "{Т} gestartet", "{Т} zu starten"),
        предложение="ich schlage vor, {zu}", отчёт="ich habe {past}",
        регистры=dict(плоский="{imp}.", вежливый="bitte {imp}.", косвенный="man sollte {inf}.",
                      вопросом="kannst du {inf}?"),
        встречается="{Wи} kommt {М} {N} vor",
        вопрос_раз="wie oft kommt {Wи} {М} vor?",
        строк_со_словом="die Datei {f} hat {N} mit dem Wort {w}",
        позиция=("{Wи} steht in Zeile {a}", "{Wи} steht in den Zeilen {a} und {b}"),
        нет_слова="{Wнет} steht nicht {М}",
        проверил="ich habe die Datei {f} geprüft",
        итог=("der Lauf endete erfolgreich", "der Lauf endete mit einem Fehler"),
        выпуск=("alle Tests bestanden — das Release ist veröffentlicht",
                "nicht alle Tests bestanden — das Release wird nicht veröffentlicht"),
        план_замены=("suche das Wort {w} in der Datei {f}, dann ersetze es durch {v}, dann prüfe die Datei",
                     "ich schlage drei Handlungen vor: das Wort {w} in der Datei {f} suchen, es durch {v} ersetzen, "
                     "die Datei {f} prüfen"),
        выпуск_акт=("veröffentliche das Release, wenn alle Tests bestehen",
                    "das Release veröffentlichen, wenn alle Tests bestehen")),
    "fr": dict(
        поиск=("cherche le mot {w} dans le fichier {f}", "chercher le mot {w} dans le fichier {f}",
               "cherché le mot {w} dans le fichier {f}"),
        строки=("cherche les lignes avec le mot {w} dans le fichier {f}",
                "chercher les lignes avec le mot {w} dans le fichier {f}",
                "cherché les lignes avec le mot {w} dans le fichier {f}"),
        замена=("remplace {W} par {v} {М}", "remplacer {W} par {v} {М}", "remplacé {W} par {v} {М}"),
        дописать=("ajoute {S} {К}", "ajouter {S} {К}", "ajouté {S} {К}"),
        переименовать=("renomme {Фи} en {g}", "renommer {Фи} en {g}", "renommé {Фи} en {g}"),
        перенести=("déplace {Ф} {Д}", "déplacer {Ф} {Д}", "déplacé {Ф} {Д}"),
        тесты=("lance {Т}", "lancer {Т}", "lancé {Т}"),
        предложение="je propose de {inf}", отчёт="j'ai {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, s'il te plaît.", косвенный="il faut {inf}.",
                      вопросом="peux-tu {inf} ?"),
        встречается="{Wи} apparaît {N} {М}",
        вопрос_раз="combien de fois {Wи} apparaît-il {М} ?",
        строк_со_словом="le fichier {f} a {N} avec le mot {w}",
        позиция=("{Wи} se trouve à la ligne {a}", "{Wи} se trouve aux lignes {a} et {b}"),
        нет_слова="{Wнет} n'est pas {М}",
        проверил="j'ai vérifié le fichier {f}",
        итог=("l'exécution s'est terminée avec succès", "l'exécution s'est terminée par une erreur"),
        выпуск=("tous les tests ont réussi — la version est publiée",
                "certains tests ont échoué — la version n'est pas publiée"),
        план_замены=("cherche le mot {w} dans le fichier {f}, puis remplace-le par {v}, puis vérifie le fichier",
                     "je propose trois actes : chercher le mot {w} dans le fichier {f}, le remplacer par {v}, "
                     "vérifier le fichier {f}"),
        выпуск_акт=("publie la version si tous les tests réussissent",
                    "publier la version si tous les tests réussissent")),
    "es": dict(
        поиск=("busca la palabra {w} en el archivo {f}", "buscar la palabra {w} en el archivo {f}",
               "buscado la palabra {w} en el archivo {f}"),
        строки=("busca las líneas con la palabra {w} en el archivo {f}",
                "buscar las líneas con la palabra {w} en el archivo {f}",
                "buscado las líneas con la palabra {w} en el archivo {f}"),
        замена=("reemplaza {W} por {v} {М}", "reemplazar {W} por {v} {М}", "reemplazado {W} por {v} {М}"),
        дописать=("añade {S} {К}", "añadir {S} {К}", "añadido {S} {К}"),
        переименовать=("renombra {Фи} como {g}", "renombrar {Фи} como {g}", "renombrado {Фи} como {g}"),
        перенести=("mueve {Ф} {Д}", "mover {Ф} {Д}", "movido {Ф} {Д}"),
        тесты=("ejecuta {Т}", "ejecutar {Т}", "ejecutado {Т}"),
        предложение="propongo {inf}", отчёт="he {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, por favor.", косвенный="hay que {inf}.",
                      вопросом="¿puedes {inf}?"),
        встречается="{Wи} aparece {N} {М}",
        вопрос_раз="¿cuántas veces aparece {Wи} {М}?",
        строк_со_словом="el archivo {f} tiene {N} con la palabra {w}",
        позиция=("{Wи} está en la línea {a}", "{Wи} está en las líneas {a} y {b}"),
        нет_слова="{Wнет} no está {М}",
        проверил="he revisado el archivo {f}",
        итог=("la ejecución terminó con éxito", "la ejecución terminó con un error"),
        выпуск=("todas las pruebas pasaron — la versión está publicada",
                "algunas pruebas fallaron — la versión no se publica"),
        план_замены=("busca la palabra {w} en el archivo {f}, luego reemplázala por {v}, luego revisa el archivo",
                     "propongo tres actos: buscar la palabra {w} en el archivo {f}, reemplazarla por {v}, "
                     "revisar el archivo {f}"),
        выпуск_акт=("publica la versión si todas las pruebas pasan", "publicar la versión si todas las pruebas pasan")),
    "it": dict(
        поиск=("cerca la parola {w} nel file {f}", "cercare la parola {w} nel file {f}",
               "cercato la parola {w} nel file {f}"),
        строки=("cerca le righe con la parola {w} nel file {f}", "cercare le righe con la parola {w} nel file {f}",
                "cercato le righe con la parola {w} nel file {f}"),
        замена=("sostituisci {W} con {v} {М}", "sostituire {W} con {v} {М}", "sostituito {W} con {v} {М}"),
        дописать=("aggiungi {S} {К}", "aggiungere {S} {К}", "aggiunto {S} {К}"),
        переименовать=("rinomina {Фи} in {g}", "rinominare {Фи} in {g}", "rinominato {Фи} in {g}"),
        перенести=("sposta {Ф} {Д}", "spostare {Ф} {Д}", "spostato {Ф} {Д}"),
        тесты=("esegui {Т}", "eseguire {Т}", "eseguito {Т}"),
        предложение="propongo di {inf}", отчёт="ho {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, per favore.", косвенный="bisogna {inf}.",
                      вопросом="puoi {inf}?"),
        встречается="{Wи} compare {N} {М}",
        вопрос_раз="quante volte compare {Wи} {М}?",
        строк_со_словом="il file {f} ha {N} con la parola {w}",
        позиция=("{Wи} si trova alla riga {a}", "{Wи} si trova alle righe {a} e {b}"),
        нет_слова="{Wнет} non è {М}",
        проверил="ho controllato il file {f}",
        итог=("l'esecuzione è terminata con successo", "l'esecuzione è terminata con un errore"),
        выпуск=("tutti i test sono passati — la versione è pubblicata",
                "alcuni test sono falliti — la versione non viene pubblicata"),
        план_замены=("cerca la parola {w} nel file {f}, poi sostituiscila con {v}, poi controlla il file",
                     "propongo tre atti: cercare la parola {w} nel file {f}, sostituirla con {v}, "
                     "controllare il file {f}"),
        выпуск_акт=("pubblica la versione se tutti i test passano", "pubblicare la versione se tutti i test passano")),
    "pt": dict(
        поиск=("procura a palavra {w} no ficheiro {f}", "procurar a palavra {w} no ficheiro {f}",
               "procurei a palavra {w} no ficheiro {f}"),
        строки=("procura as linhas com a palavra {w} no ficheiro {f}",
                "procurar as linhas com a palavra {w} no ficheiro {f}",
                "procurei as linhas com a palavra {w} no ficheiro {f}"),
        замена=("substitui {W} por {v} {М}", "substituir {W} por {v} {М}", "substituí {W} por {v} {М}"),
        дописать=("acrescenta {S} {К}", "acrescentar {S} {К}", "acrescentei {S} {К}"),
        переименовать=("renomeia {Фи} para {g}", "renomear {Фи} para {g}", "renomeei {Фи} para {g}"),
        перенести=("move {Ф} {Д}", "mover {Ф} {Д}", "movi {Ф} {Д}"),
        тесты=("executa {Т}", "executar {Т}", "executei {Т}"),
        предложение="proponho {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, por favor.", косвенный="é preciso {inf}.",
                      вопросом="podes {inf}?"),
        встречается="{Wи} aparece {N} {М}",
        вопрос_раз="quantas vezes aparece {Wи} {М}?",
        строк_со_словом="o ficheiro {f} tem {N} com a palavra {w}",
        позиция=("{Wи} está na linha {a}", "{Wи} está nas linhas {a} e {b}"),
        нет_слова="{Wнет} não está {М}",
        проверил="verifiquei o ficheiro {f}",
        итог=("a execução terminou com sucesso", "a execução terminou com um erro"),
        выпуск=("todos os testes passaram — a versão está publicada",
                "alguns testes falharam — a versão não é publicada"),
        план_замены=("procura a palavra {w} no ficheiro {f}, depois substitui-a por {v}, depois verifica o ficheiro",
                     "proponho três atos: procurar a palavra {w} no ficheiro {f}, substituí-la por {v}, "
                     "verificar o ficheiro {f}"),
        выпуск_акт=("publica a versão se todos os testes passarem", "publicar a versão se todos os testes passarem")),
    "nl": dict(
        поиск=("zoek het woord {w} in het bestand {f}", "het woord {w} in het bestand {f} zoeken",
               "het woord {w} in het bestand {f} gezocht", "het woord {w} in het bestand {f} te zoeken"),
        строки=("zoek de regels met het woord {w} in het bestand {f}",
                "de regels met het woord {w} in het bestand {f} zoeken",
                "de regels met het woord {w} in het bestand {f} gezocht",
                "de regels met het woord {w} in het bestand {f} te zoeken"),
        замена=("vervang {W} {М} door {v}", "{W} {М} door {v} vervangen", "{W} {М} door {v} vervangen",
                "{W} {М} door {v} te vervangen"),
        дописать=("zet {S} {К}", "{S} {К} zetten", "{S} {К} gezet", "{S} {К} te zetten"),
        переименовать=("hernoem {Фи} naar {g}", "{Фи} naar {g} hernoemen", "{Фи} naar {g} hernoemd",
                       "{Фи} naar {g} te hernoemen"),
        перенести=("verplaats {Ф} {Д}", "{Ф} {Д} verplaatsen", "{Ф} {Д} verplaatst", "{Ф} {Д} te verplaatsen"),
        тесты=("start {Т}", "{Т} starten", "{Т} gestart", "{Т} te starten"),
        предложение="ik stel voor {zu}", отчёт="ik heb {past}",
        регистры=dict(плоский="{imp}.", вежливый="{imp}, alsjeblieft.", косвенный="we moeten {inf}.",
                      вопросом="kun je {inf}?"),
        встречается="{Wи} komt {N} voor {М}",
        вопрос_раз="hoe vaak komt {Wи} voor {М}?",
        строк_со_словом="het bestand {f} heeft {N} met het woord {w}",
        позиция=("{Wи} staat in regel {a}", "{Wи} staat in de regels {a} en {b}"),
        нет_слова="{Wнет} staat niet {М}",
        проверил="ik heb het bestand {f} gecontroleerd",
        итог=("de run eindigde succesvol", "de run eindigde met een fout"),
        выпуск=("alle tests geslaagd — de release is gepubliceerd",
                "niet alle tests geslaagd — de release wordt niet gepubliceerd"),
        план_замены=("zoek het woord {w} in het bestand {f}, vervang het dan door {v} en controleer daarna het bestand",
                     "ik stel drie handelingen voor: het woord {w} in het bestand {f} zoeken, het door {v} "
                     "vervangen, het bestand {f} controleren"),
        выпуск_акт=("publiceer de release als alle tests slagen", "de release publiceren als alle tests slagen")),
    "pl": dict(
        поиск=("znajdź słowo {w} w pliku {f}", "znaleźć słowo {w} w pliku {f}", "szukałem słowa {w} w pliku {f}"),
        строки=("znajdź linie ze słowem {w} w pliku {f}", "znaleźć linie ze słowem {w} w pliku {f}",
                "szukałem linii ze słowem {w} w pliku {f}"),
        замена=("zamień {W} na {v} {М}", "zamienić {W} na {v} {М}", "zamieniłem {W} na {v} {М}"),
        дописать=("dopisz {S} {К}", "dopisać {S} {К}", "dopisałem {S} {К}"),
        переименовать=("zmień nazwę {Фи} na {g}", "zmienić nazwę {Фи} na {g}", "zmieniłem nazwę {Фи} na {g}"),
        перенести=("przenieś {Ф} {Д}", "przenieść {Ф} {Д}", "przeniosłem {Ф} {Д}"),
        тесты=("uruchom {Т}", "uruchomić {Т}", "uruchomiłem {Т}"),
        предложение="proponuję {inf}", отчёт="{past}",
        регистры=dict(плоский="{imp}.", вежливый="proszę, {imp}.", косвенный="trzeba {inf}.",
                      вопросом="czy możesz {inf}?"),
        встречается="{Wи} występuje {N} {М}",
        вопрос_раз="ile razy {Wи} występuje {М}?",
        строк_со_словом="plik {f} ma {N} ze słowem {w}",
        позиция=("{Wи} jest w linii {a}", "{Wи} jest w liniach {a} i {b}"),
        нет_слова="{Wнет} nie ma {М}",
        проверил="sprawdziłem plik {f}",
        итог=("uruchomienie zakończyło się sukcesem", "uruchomienie zakończyło się błędem"),
        выпуск=("wszystkie testy przeszły — wydanie jest opublikowane",
                "nie wszystkie testy przeszły — wydanie nie zostaje opublikowane"),
        план_замены=("znajdź słowo {w} w pliku {f}, potem zamień je na {v}, potem sprawdź plik",
                     "proponuję trzy akty: znaleźć słowo {w} w pliku {f}, zamienić je na {v}, sprawdzić plik {f}"),
        выпуск_акт=("opublikuj wydanie, jeśli wszystkie testy przejdą",
                    "opublikować wydanie, jeśli wszystkie testy przejdą")),
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
    """«3 lines», «1 строка» — счётная форма строки (именительный: «в файле 1 строка со словом …»)."""
    if язык == "ru":
        return f"{n} {rugram.форма('строка', n)}"
    return f"{n} {S._счёт(СТРОК[язык], n, язык)}"


def строк_вин(язык, n):
    """Счёт строк дополнением переходного глагола — «файл содержит 1 строку», «plik zawiera 1 linię»: падеж берётся
    у дверей падежа при числе (`rugram.винительный_при_числе`, объявленный `plgram.ВИНИТЕЛЬНЫЙ_ЕД` — у польского
    он виден лишь при ровно единице); у прочих языков винительный равен счётной форме."""
    if язык == "ru":
        return f"{n} {rugram.винительный_при_числе('строка', n)}"
    if язык == "pl" and n == 1:
        return f"{n} {plgram.винительный_ед(СТРОК['pl'][0])}"
    return строк(язык, n)


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
    п = слоты(язык, **п)
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
    return _фр(язык, РЕЧЬ[язык][фраза].format(**слоты(язык, **п)))


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
    """«the word "cheese" occurs 2 times in the file notes.md» — N приходит готовой счётной фразой."""
    return _с(язык, "встречается", w=кавычки(язык, w), f=f, N=N)


def _файл_строк(язык, f, N):
    return A.РЕЧЬ[язык]["в_файле"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=f), B=N)


def _папка(язык, N):
    return A.РЕЧЬ[язык]["папка"].format(N=N)


def папка_с_именем(язык, d, N):
    """«the folder archive contains 1 file» — папка, названная миром (у `actturn` папка одна и без имени)."""
    return ОБЪЕКТЫ[язык]["папка_имя"].format(d=d, N=N)


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
        части.append(_фр(язык, РЕЧЬ[язык]["позиция"][len(поз) - 1].format(**слоты(язык, w=п["w"]), a=поз[0],
                                                                           b=поз[-1])) + ".")
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
    п = dict(f=f, d=АРХИВ)
    итог = (отчёт(язык, "перенести", **п) + ". " + наблюдение(язык, _папка(язык, N0), L0) + " "
            + наблюдение(язык, папка_с_именем(язык, АРХИВ, N1), L1))
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
    imp, inf, _zu, _past = _ступени(язык, "тесты", t=t)
    выпуск_imp, выпуск_inf = РЕЧЬ[язык]["выпуск_акт"]
    приказ_ = _фр(язык, связать(язык, "приказ", imp, выпуск_imp)) + "."
    предложение_ = _фр(язык, связать(язык, "предложение", inf, выпуск_inf)) + ". " + _вопрос_предложения(язык)
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
    return сборка_дописать(язык, род, регистр, s, f, строк_вин(язык, стало), счёт)


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
