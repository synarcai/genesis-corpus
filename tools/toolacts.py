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
          "S": ("s", "строку"), "Т": ("t", "тесты_файла"), "Д": ("d", "в_папку"), "Фр": ("f", "файла")}


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


# ЗАЧИН ПРОСЬБЫ СКАЗАТЬ (27.09, наряд ведущего: зачин перед вторым вопросом плана) — одна дверь на всякий вопрос
# вторым приказом: (глагол, остаток) зачина, придаточное вопроса идёт за остатком. Вид 0 — прежний зачин дома («let
# me know», «скажи»), вид 1 — зачин с местоимением после глагола («tell me», «скажи мне») или соседний глагол языка,
# где прежний уже несёт местоимение («avísame», «laat me weten»). Глагол отдельно от остатка — ради связки:
# нидерландское наречие стоит после глагола повеления («… en laat me daarna weten …»).
ЗАЧИН = {
    "en": (("let", "me know"), ("tell", "me")),
    "ru": (("скажи,", ""), ("скажи", "мне,")),
    "de": (("sag", "mir,"), ("gib", "mir Bescheid,")),
    "fr": (("dis-moi", ""), ("fais-moi", "savoir")),
    "es": (("dime", ""), ("avísame", "")),
    "it": (("dimmi", ""), ("fammi", "sapere")),
    "pt": (("diz-me", ""), ("avisa-me", "")),
    "nl": (("vertel me", ""), ("laat me", "weten")),
    "pl": (("powiedz", "mi,"), ("daj", "mi znać,")),
}


def зачин(язык, вид, придаточное):
    """(глагол, остаток) второго приказа — зачин просьбы сказать и придаточное вопроса за ним."""
    глагол, остаток = ЗАЧИН[язык][вид]
    return глагол, (остаток + " " + придаточное).strip()


# ЗАЧИНЫ ОДИНОЧНОГО ВОПРОСА (27.09, наряд ведущего (e): зачин перед одиночным вопросом, а не только перед вторым
# вопросом плана) — свои у голоса: «show me», «report»; «сообщи», «покажи», «подскажи»; «zeig mir», «teil mir mit»;
# «montre-moi», «indique-moi»; «laat me zien», «geef aan» (нидерландская частица — после наречия связки: «… en geef
# daarna aan …»); «pokaż mi», «podaj». Новые виды — в конце ряда: планы берут виды 0 и 1, как прежде
for _я, _в in {"en": (("show", "me"), ("report", "")),
               "ru": (("сообщи,", ""), ("покажи,", ""), ("подскажи,", "")),
               "de": (("zeig", "mir,"), ("teil", "mir mit,")),
               "fr": (("montre-moi", ""), ("indique-moi", "")),
               "es": (("muéstrame", ""), ("indícame", "")),
               "it": (("mostrami", ""), ("indicami", "")),
               "pt": (("mostra-me", ""), ("indica-me", "")),
               "nl": (("laat me", "zien"), ("geef", "aan")),
               "pl": (("pokaż", "mi,"), ("podaj,", ""))}.items():
    ЗАЧИН[_я] += _в
# НУЖДА И ЖЕЛАНИЕ ЗНАТЬ (28.09, наряд ведущего по классам H2: «иная конструкция» — утверждение нужды вместо вопроса):
# «i need to know which file contains …», «мне нужно знать, …», «ich möchte wissen, …» — два вида в конце ряда
for _я, _в in {"en": (("i need to know", ""), ("i would like to know", "")),
               "ru": (("мне нужно знать,", ""), ("я хочу знать,", "")),
               "de": (("ich muss", "wissen,"), ("ich möchte", "wissen,")),
               "fr": (("je dois savoir", ""), ("je voudrais savoir", "")),
               "es": (("necesito saber", ""), ("quiero saber", "")),
               "it": (("ho bisogno di sapere", ""), ("vorrei sapere", "")),
               "pt": (("preciso de saber", ""), ("queria saber", "")),
               "nl": (("ik moet", "weten"), ("ik wil graag", "weten")),
               "pl": (("muszę wiedzieć,", ""), ("chcę wiedzieć,", ""))}.items():
    ЗАЧИН[_я] += _в


# ПЛАН С МЕСТОИМЕНИЕМ (25.09, вопрос 4 коллегии «ответ мира»; ведущий: роды дома актов `toolrepo`): второй приказ
# называет объект первого местоимением — «create the file X, then append the line "…" to it». Формы приказа —
# (глагол, остаток) для связки: местоимение стоит там, где его ставит язык, и глагол тот же, что у акта двери
# (французское, испанское, итальянское, португальское местоимение пристаёт к глаголу: «ajoute-y», «añádele»).
# Предложение местоимения не повторяет: оно называет путь, какой определяет приказ. «найти» — приказ находки файла
# со словом (глагол поиска двери); «ждёт» — второй акт ждёт одного места, «нет_второго» — первый акт не совершён.
# «строк» — вопрос о несомом месте вторым приказом; английская форма — соседняя: у первой пробы длиннейший общий ряд
# с ключом AGENT-K вышел 8 слов (> 6, мера счётом genesis_key_overlap), у этой — 5.
МЕСТОИМЕНИЕ = {
    "en": dict(дописать=("append", "{S} to it"), удалить=("delete", "it"),
               строк=(зачин("en", 0, "how many lines it has"), "tell how many lines the file {p} has"),
               найти=("find the file that contains {W}", "find the file that contains {W}"),
               ждёт="the second act waits for one file", нет_второго="the second act is not performed either"),
    "ru": dict(дописать=("допиши", "в него {S}"), удалить=("удали", "его"),
               строк=(зачин("ru", 0, "сколько в нём строк"), "сказать, сколько строк в файле {p}"),
               найти=("найди файл, в котором есть {Wи}", "найти файл, в котором есть {Wи}"),
               ждёт="второй акт ждёт одного файла", нет_второго="второй акт тоже не совершён"),
    "de": dict(дописать=("ergänze", "sie um {S}"), удалить=("lösche", "sie"),
               строк=(зачин("de", 0, "wie viele Zeilen sie hat"), "sagen, wie viele Zeilen die Datei {p} hat"),
               найти=("suche die Datei, die {W} enthält", "die Datei suchen, die {W} enthält",
                      "die Datei zu suchen, die {W} enthält"),
               ждёт="die zweite Handlung wartet auf eine Datei",
               нет_второго="die zweite Handlung wird auch nicht ausgeführt"),
    "fr": dict(дописать=("ajoute-y", "{S}"), удалить=("supprime-le", ""),
               строк=(зачин("fr", 0, "combien de lignes il contient"), "dire combien de lignes contient le fichier {p}"),
               найти=("cherche le fichier qui contient {W}", "chercher le fichier qui contient {W}"),
               ждёт="le deuxième acte attend un seul fichier", нет_второго="le deuxième acte n'est pas exécuté non plus"),
    "es": dict(дописать=("añádele", "{S}"), удалить=("elimínalo", ""),
               строк=(зачин("es", 0, "cuántas líneas tiene"), "decir cuántas líneas tiene el archivo {p}"),
               найти=("busca el archivo que contiene {W}", "buscar el archivo que contiene {W}"),
               ждёт="el segundo acto espera un solo archivo", нет_второго="el segundo acto tampoco se realiza"),
    "it": dict(дописать=("aggiungici", "{S}"), удалить=("eliminalo", ""),
               строк=(зачин("it", 0, "quante righe ha"), "dire quante righe ha il file {p}"),
               найти=("cerca il file che contiene {W}", "cercare il file che contiene {W}"),
               ждёт="il secondo atto aspetta un solo file", нет_второго="neanche il secondo atto viene eseguito"),
    "pt": dict(дописать=("acrescenta-lhe", "{S}"), удалить=("elimina-o", ""),
               строк=(зачин("pt", 0, "quantas linhas tem"), "dizer quantas linhas tem o ficheiro {p}"),
               найти=("procura o ficheiro que contém {W}", "procurar o ficheiro que contém {W}"),
               ждёт="o segundo ato espera um só ficheiro", нет_второго="o segundo ato também não é realizado"),
    "nl": dict(дописать=("zet", "{S} er onderaan"), удалить=("verwijder het", ""),
               строк=(зачин("nl", 0, "hoeveel regels het heeft"), "zeggen hoeveel regels het bestand {p} heeft"),
               найти=("zoek het bestand dat {W} bevat", "het bestand zoeken dat {W} bevat",
                      "het bestand te zoeken dat {W} bevat"),
               ждёт="de tweede handeling wacht op één bestand",
               нет_второго="de tweede handeling wordt ook niet uitgevoerd"),
    "pl": dict(дописать=("dopisz", "do niego {S}"), удалить=("usuń", "go"),
               строк=(зачин("pl", 0, "ile ma linii"), "powiedzieć, ile linii ma plik {p}"),
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


# СЕМЬИ ПЕРЕФРАЗА ПРИКАЗА (25.09, заказ ведущего под рынок правок М-2021): одна правка формы на паре страниц одного
# акта мира. Предложение и отчёт организма говорят каноническими словами; правится лишь приказ пользователя.
#
# СИНОНИМ ГЛАГОЛА — второй глагол того же акта, только в приказе (условие М-2013, 4: у акта один глагол на язык в
# речи организма). Слоты — те же, что у шаблона акта; где синоним требует иного падежа объекта, стоит слот этого
# падежа («benenne {Ф} in {g} um» — винительный, «przemianuj {Ф} na {g}»).
# ГЛАГОЛЫ АКТА В КАЖДОМ ГОЛОСЕ СВОИ (27.09, наряд ведущего (d)): у всякого акта — ряд синонимов, первый — прежний;
# слово или оборот голоса, а не перевод английского («get rid of», «избавься от файла», «débarrasse-toi du fichier»,
# «pozbądź się pliku» — у оборота с родительным слот {Фр}; «use Y instead of X» — голыми литералами в кавычках:
# «используй «y» вместо «x»», «usa «y» en lugar de «x»» — артикль не сливается с предлогом)
СИНОНИМЫ = {
    "en": dict(создать=("make {Ф}", "set up {Ф}", "start a new file {f}"),
               удалить=("remove {Ф}", "erase {Ф}", "get rid of {Ф}"),
               перенести=("transfer {Ф} {Д}", "shift {Ф} {Д}", "put {Ф} into the folder {d}"),
               переименовать=("change the name of {Фи} to {g}", "give {Фи} the new name {g}"),
               дописать=("add {S} {К}", "put {S} {М}", "write {S} {К}", "attach {S} {К}"),
               замена=("change {W} to {v} {М}", "swap {W} for {v} {М}", "use {v} instead of {w} {М}",
                       "switch {W} to {v} {М}"),
               тесты=("execute {Т}", "launch {Т}", "kick off {Т}")),
    "ru": dict(создать=("заведи {Ф}", "сделай {Ф}", "сформируй {Ф}"),
               удалить=("сотри {Ф}", "убери {Ф}", "избавься от {Фр}"),
               перенести=("перемести {Ф} {Д}", "переложи {Ф} {Д}", "отправь {Ф} {Д}"),
               переименовать=("переназови {Фи} в {g}", "смени имя {Фр} на {g}"),
               дописать=("добавь {S} {К}", "впиши {S} {К}", "запиши {S} {К}"),
               замена=("поменяй {W} на {v} {М}", "смени {W} на {v} {М}", "используй {v} вместо {w} {М}"),
               тесты=("прогони {Т}", "выполни {Т}", "проведи {Т}")),
    "de": dict(создать=("lege {Ф} an", "erzeuge {Ф}", "richte {Ф} ein"),
               удалить=("entferne {Ф}", "wirf {Ф} weg", "beseitige {Ф}"),
               перенести=("verlege {Ф} {Д}", "schieb {Ф} {Д}", "leg {Ф} {Д}"),
               переименовать=("benenne {Ф} in {g} um", "nenne {Ф} in {g} um"),
               дописать=("erweitere {К} um {S}", "hänge {S} an {К} an", "schreib {S} in {К}", "füge {S} in {К} ein"),
               замена=("tausche {W} {М} gegen {v}", "ändere {W} {М} in {v}", "wechsle {W} {М} gegen {v}",
                       "nimm {v} statt {w} {М}"),
               тесты=("führe {Т} aus", "lass {Т} laufen", "wirf {Т} an")),
    "fr": dict(создать=("génère {Ф}", "prépare {Ф}", "démarre un nouveau fichier {f}"),
               удалить=("efface {Ф}", "retire {Ф}", "débarrasse-toi {Фр}"),
               перенести=("transfère {Ф} {Д}", "range {Ф} {Д}", "mets {Ф} {Д}"),
               переименовать=("rebaptise {Фи} en {g}", "donne {К} le nom {g}"),
               дописать=("rajoute {S} {К}", "écris {S} {М}", "mets {S} {М}", "joins {S} {К}"),
               замена=("change {W} en {v} {М}", "échange {W} contre {v} {М}", "transforme {W} en {v} {М}",
                       "mets {v} à la place de {w} {М}"),
               тесты=("exécute {Т}", "démarre {Т}", "fais tourner {Т}")),
    "es": dict(создать=("genera {Ф}", "prepara {Ф}", "empieza un archivo nuevo {f}"),
               удалить=("borra {Ф}", "quita {Ф}", "deshazte {Фр}"),
               перенести=("traslada {Ф} {Д}", "pasa {Ф} {Д}", "lleva {Ф} {Д}"),
               переименовать=("rebautiza {Фи} como {g}", "cambia el nombre {Фр} a {g}"),
               дописать=("agrega {S} {К}", "escribe {S} {М}", "pon {S} {М}", "adjunta {S} {К}"),
               замена=("cambia {W} por {v} {М}", "sustituye {W} por {v} {М}", "usa {v} en lugar de {w} {М}"),
               тесты=("corre {Т}", "lanza {Т}", "arranca {Т}")),
    "it": dict(создать=("genera {Ф}", "prepara {Ф}", "inizia un nuovo file {f}"),
               удалить=("cancella {Ф}", "rimuovi {Ф}", "sbarazzati {Фр}"),
               перенести=("trasferisci {Ф} {Д}", "porta {Ф} {Д}", "metti {Ф} {Д}"),
               переименовать=("ribattezza {Фи} in {g}", "cambia il nome {Фр} in {g}"),
               дописать=("accoda {S} {К}", "scrivi {S} {М}", "metti {S} {М}", "allega {S} {К}"),
               замена=("cambia {W} con {v} {М}", "scambia {W} con {v} {М}", "rimpiazza {W} con {v} {М}",
                       "usa {v} al posto di {w} {М}"),
               тесты=("lancia {Т}", "avvia {Т}", "fai girare {Т}")),
    "pt": dict(создать=("gera {Ф}", "prepara {Ф}", "começa um novo ficheiro {f}"),
               удалить=("apaga {Ф}", "remove {Ф}", "livra-te {Фр}"),
               перенести=("passa {Ф} {Д}", "leva {Ф} {Д}", "transfere {Ф} {Д}"),
               переименовать=("rebatiza {Фи} para {g}", "muda o nome {Фр} para {g}"),
               дописать=("adiciona {S} {К}", "escreve {S} {М}", "põe {S} {М}", "anexa {S} {К}"),
               замена=("troca {W} por {v} {М}", "muda {W} para {v} {М}", "altera {W} para {v} {М}",
                       "usa {v} em vez de {w} {М}"),
               тесты=("corre {Т}", "lança {Т}", "arranca {Т}")),
    "nl": dict(создать=("maak {Ф}", "zet {Ф} klaar", "begin een nieuw bestand {f}"),
               удалить=("wis {Ф}", "haal {Ф} weg", "gooi {Ф} weg"),
               перенести=("breng {Ф} {Д}", "schuif {Ф} {Д}", "stuur {Ф} {Д}"),
               переименовать=("wijzig de naam van {Фи} naar {g}", "geef {Фи} de naam {g}"),
               дописать=("plaats {S} {К}", "schrijf {S} {М}", "voeg {S} toe aan {Фи}"),
               замена=("verander {W} {М} in {v}", "wijzig {W} {М} in {v}", "gebruik {v} in plaats van {w} {М}"),
               тесты=("draai {Т}", "voer {Т} uit", "laat {Т} lopen")),
    "pl": dict(создать=("stwórz {Ф}", "zrób {Ф}", "przygotuj {Ф}", "zacznij nowy plik {f}"),
               удалить=("skasuj {Ф}", "wyrzuć {Ф}", "pozbądź się {Фр}"),
               перенести=("przesuń {Ф} {Д}", "przełóż {Ф} {Д}", "wrzuć {Ф} {Д}"),
               переименовать=("przemianuj {Ф} na {g}", "przechrzcij {Ф} na {g}"),
               дописать=("dodaj {S} {К}", "wpisz {S} {К}", "zapisz {S} {М}", "dołącz {S} {К}"),
               замена=("podmień {W} na {v} {М}", "zmień {W} na {v} {М}", "użyj {v} zamiast {w} {М}"),
               тесты=("odpal {Т}", "puść {Т}", "wykonaj {Т}")),
}


# НАБОР И ПРОГОН ТЕСТОВ — единицы прогона в живой речи (наряд (d): «test suite», «test run»): те же синонимы акта
# прогона, объект — язык проекта {Я}
for _я, _ещё in {"en": ("run the {Я} test suite", "start a test run for {Я}"),
                 "ru": ("запусти набор тестов {Я}", "начни прогон тестов {Я}"),
                 "de": ("starte die Testsuite für {Я}", "starte einen Testlauf für {Я}"),
                 "fr": ("lance la suite de tests {Я}", "démarre une exécution des tests {Я}"),
                 "es": ("ejecuta la batería de pruebas de {Я}", "inicia una ejecución de las pruebas de {Я}"),
                 "it": ("esegui la suite di test {Я}", "avvia un'esecuzione dei test {Я}"),
                 "pt": ("executa a bateria de testes de {Я}", "inicia uma execução dos testes de {Я}"),
                 "nl": ("start de testsuite voor {Я}", "start een testrun voor {Я}"),
                 "pl": ("uruchom zestaw testów {Я}", "zacznij przebieg testów {Я}")}.items():
    СИНОНИМЫ[_я]["тесты"] += _ещё


# КОНСТРУКЦИИ ОДНОГО АКТА (27.09, наряд ведущего (f)): порядок доводов и место — «from "x" to "y"» у замены (объект —
# текст в файле, доводы — голыми литералами в кавычках), «over to» у переноса (где голос говорит это одним глаголом —
# «перекинь», «przerzuć», «bascule»), «on its own line» у дописывания («отдельной строкой», «als eigene Zeile»)
for _я, _ещё in {
        "en": dict(замена=("change the text {М} from {w} to {v}",), перенести=("move {Ф} over to the folder {d}",),
                   дописать=("add {s} on its own line {К}",)),
        "ru": dict(замена=("поменяй текст {М} с {w} на {v}",), перенести=("перекинь {Ф} {Д}",),
                   дописать=("допиши {s} отдельной строкой {К}",)),
        "de": dict(замена=("ändere den Text {М} von {w} zu {v}",), перенести=("schieb {Ф} rüber {Д}",),
                   дописать=("füge {s} als eigene Zeile in {К} ein",)),
        "fr": dict(замена=("change le texte {М} de {w} en {v}",), перенести=("bascule {Ф} {Д}",),
                   дописать=("ajoute {s} sur une ligne à part {К}",)),
        "es": dict(замена=("cambia el texto {М} de {w} a {v}",), перенести=("manda {Ф} {Д}",),
                   дописать=("añade {s} en una línea aparte {К}",)),
        "it": dict(замена=("cambia il testo {М} da {w} a {v}",), перенести=("manda {Ф} {Д}",),
                   дописать=("aggiungi {s} su una riga a parte {К}",)),
        "pt": dict(замена=("muda o texto {М} de {w} para {v}",), перенести=("manda {Ф} {Д}",),
                   дописать=("acrescenta {s} numa linha à parte {К}",)),
        "nl": dict(замена=("verander de tekst {М} van {w} naar {v}",), перенести=("zet {Ф} over {Д}",),
                   дописать=("zet {s} op een eigen regel {К}",)),
        "pl": dict(замена=("zmień tekst {М} z {w} na {v}",), перенести=("przerzuć {Ф} {Д}",),
                   дописать=("dopisz {s} w osobnej linii {К}",))}.items():
    for _акт, _формы in _ещё.items():
        СИНОНИМЫ[_я][_акт] += _формы


def синоним(язык, акт, i=0, **п):
    """Приказ акта i-м вторым глаголом: «make the file x», «set up the file x», «add the line "y" to the file x»."""
    return СИНОНИМЫ[язык][акт][i].format(**слоты(язык, **п))


# СТРАДАТЕЛЬНЫЙ ОБОРОТ И ДОЛЖЕНСТВОВАНИЕ С ОБЪЕКТОМ ВПЕРЕДИ (28.09, наряд ведущего по классам отложенного ключа H2:
# «иная конструкция») — приказ без повеления: акт назван тем, что с объектом должно стать. Шаблон на акт и голос, слоты —
# двери: «the file F should be deleted», «файл F нужно удалить», «plik F trzeba usunąć». Где род или падеж объекта менялся
# бы с наполнителем (de «den Text», it «la parola» / «il testo», pt «a palavra» / «o texto» у замены), голос говорит
# безличное долженствование с объектом в падеже двери: «man muss …», «si deve sostituire …», «tem de se substituir …»
СТРАДАТЕЛЬНЫЙ = {
    "en": dict(создать="{Ф} should be created", удалить="{Ф} should be deleted", перенести="{Ф} should be moved {Д}",
               переименовать="{Фи} should be renamed to {g}", дописать="{S} should be appended {К}",
               замена="{W} {М} should be replaced with {v}", тесты="{Т} should be run"),
    "ru": dict(создать="{Ф} нужно создать", удалить="{Ф} нужно удалить", перенести="{Ф} нужно перенести {Д}",
               переименовать="{Фи} нужно переименовать в {g}", дописать="{S} нужно дописать {К}",
               замена="{W} {М} нужно заменить на {v}", тесты="{Т} нужно запустить"),
    "de": dict(создать="{Ф} muss erstellt werden", удалить="{Ф} muss gelöscht werden",
               перенести="{Ф} muss {Д} verschoben werden", переименовать="{Ф} muss in {g} umbenannt werden",
               дописать="{К} muss um {S} ergänzt werden", замена="man muss {W} {М} durch {v} ersetzen",
               тесты="{Т} müssen gestartet werden"),
    "fr": dict(создать="{Ф} doit être créé", удалить="{Ф} doit être supprimé", перенести="{Ф} doit être déplacé {Д}",
               переименовать="{Фи} doit être renommé en {g}", дописать="{S} doit être ajoutée {К}",
               замена="{W} {М} doit être remplacé par {v}", тесты="{Т} doivent être lancés"),
    "es": dict(создать="{Ф} debe crearse", удалить="{Ф} debe eliminarse", перенести="{Ф} debe moverse {Д}",
               переименовать="{Фи} debe renombrarse como {g}", дописать="{S} debe añadirse {К}",
               замена="{W} {М} debe reemplazarse por {v}", тесты="{Т} deben ejecutarse"),
    "it": dict(создать="{Ф} va creato", удалить="{Ф} va eliminato", перенести="{Ф} va spostato {Д}",
               переименовать="{Фи} va rinominato in {g}", дописать="{S} va aggiunta {К}",
               замена="si deve sostituire {W} con {v} {М}", тесты="{Т} vanno eseguiti"),
    "pt": dict(создать="{Ф} tem de ser criado", удалить="{Ф} tem de ser eliminado",
               перенести="{Ф} tem de ser movido {Д}", переименовать="{Фи} tem de ser renomeado para {g}",
               дописать="{S} tem de ser acrescentada {К}", замена="tem de se substituir {W} por {v} {М}",
               тесты="{Т} têm de ser executados"),
    "nl": dict(создать="{Ф} moet gecreëerd worden", удалить="{Ф} moet verwijderd worden",
               перенести="{Ф} moet {Д} verplaatst worden", переименовать="{Фи} moet naar {g} hernoemd worden",
               дописать="{S} moet {К} gezet worden", замена="{W} {М} moet door {v} vervangen worden",
               тесты="{Т} moeten gestart worden"),
    "pl": dict(создать="{Ф} trzeba utworzyć", удалить="{Ф} trzeba usunąć", перенести="{Ф} trzeba przenieść {Д}",
               переименовать="nazwę {Фи} trzeba zmienić na {g}", дописать="{S} trzeba dopisać {К}",
               замена="{W} {М} trzeba zamienić na {v}", тесты="{Т} trzeba uruchomić"),
}


# СИНОНИМ В ИНФИНИТИВЕ (28.09, наряд ведущего: составные страницы «конструкция × синоним × голый путь») — первый синоним
# всякого акта (`СИНОНИМЫ`) неопределённой формой голоса: регистры нужды и желания держат {inf}
СИНОНИМЫ_ИНФ = {
    "en": dict(создать="make {Ф}", удалить="remove {Ф}", перенести="transfer {Ф} {Д}",
               переименовать="change the name of {Фи} to {g}", дописать="add {S} {К}", замена="change {W} to {v} {М}",
               тесты="execute {Т}"),
    "ru": dict(создать="завести {Ф}", удалить="стереть {Ф}", перенести="переместить {Ф} {Д}",
               переименовать="переназвать {Фи} в {g}", дописать="добавить {S} {К}", замена="поменять {W} на {v} {М}",
               тесты="прогнать {Т}"),
    "de": dict(создать="{Ф} anlegen", удалить="{Ф} entfernen", перенести="{Ф} {Д} verlegen",
               переименовать="{Ф} in {g} umbenennen", дописать="{К} um {S} erweitern",
               замена="{W} {М} gegen {v} tauschen", тесты="{Т} ausführen"),
    "fr": dict(создать="générer {Ф}", удалить="effacer {Ф}", перенести="transférer {Ф} {Д}",
               переименовать="rebaptiser {Фи} en {g}", дописать="rajouter {S} {К}", замена="changer {W} en {v} {М}",
               тесты="exécuter {Т}"),
    "es": dict(создать="generar {Ф}", удалить="borrar {Ф}", перенести="trasladar {Ф} {Д}",
               переименовать="rebautizar {Фи} como {g}", дописать="agregar {S} {К}", замена="cambiar {W} por {v} {М}",
               тесты="correr {Т}"),
    "it": dict(создать="generare {Ф}", удалить="cancellare {Ф}", перенести="trasferire {Ф} {Д}",
               переименовать="ribattezzare {Фи} in {g}", дописать="accodare {S} {К}",
               замена="cambiare {W} con {v} {М}", тесты="lanciare {Т}"),
    "pt": dict(создать="gerar {Ф}", удалить="apagar {Ф}", перенести="passar {Ф} {Д}",
               переименовать="rebatizar {Фи} para {g}", дописать="adicionar {S} {К}", замена="trocar {W} por {v} {М}",
               тесты="correr {Т}"),
    "nl": dict(создать="{Ф} maken", удалить="{Ф} wissen", перенести="{Ф} {Д} brengen",
               переименовать="de naam van {Фи} naar {g} wijzigen", дописать="{S} {К} plaatsen",
               замена="{W} {М} in {v} veranderen", тесты="{Т} draaien"),
    "pl": dict(создать="stworzyć {Ф}", удалить="skasować {Ф}", перенести="przesunąć {Ф} {Д}",
               переименовать="przemianować {Ф} na {g}", дописать="dodać {S} {К}", замена="podmienić {W} na {v} {М}",
               тесты="odpalić {Т}"),
}


def синоним_инф(язык, акт, **п):
    """Первый синоним акта неопределённой формой (`СИНОНИМЫ_ИНФ`) — для регистров, какие держат {inf}."""
    return СИНОНИМЫ_ИНФ[язык][акт].format(**слоты(язык, **п))


def страдательный(язык, акт, **п):
    """Приказ акта страдательным оборотом или долженствованием с объектом впереди (`СТРАДАТЕЛЬНЫЙ`)."""
    return СТРАДАТЕЛЬНЫЙ[язык][акт].format(**слоты(язык, **п))


# ЖЕЛАНИЕ И НУЖДА С ОБЪЕКТОМ ВПЕРЕДИ И СТРАДАТЕЛЬНЫМ ПРИЧАСТИЕМ (28.09, наряд ведущего (б), ход «иная конструкция»):
# «i want the file F deleted», «я хочу, чтобы файл F был удалён», «ich möchte, dass die Datei F gelöscht wird» — на
# шести актах правки. Причастие согласуется с объектом: строка — своим словом класса в именительном там, где слот двери
# винительный («строка {s}», «linia {s}»); у замены — пара (текст, слово), где голос различает их род (ru, pl, es, it,
# pt), у de — слово класса в именительном («der Text», «das Wort»)
СТРАД_ЖЕЛАНИЕ = {
    "en": {вид: dict(создать=f"{з} {{Ф}} created", удалить=f"{з} {{Ф}} deleted", перенести=f"{з} {{Ф}} moved {{Д}}",
                     переименовать=f"{з} {{Фи}} renamed to {{g}}", дописать=f"{з} {{S}} appended {{К}}",
                     замена=(f"{з} {{W}} {{М}} replaced with {{v}}",) * 2)
           for вид, з in (("желание", "i want"), ("нужда", "i need"))},
    "ru": {вид: dict(создать=f"{з} {{Ф}} был создан", удалить=f"{з} {{Ф}} был удалён",
                     перенести=f"{з} {{Ф}} был перенесён {{Д}}", переименовать=f"{з} {{Фи}} был переименован в {{g}}",
                     дописать=f"{з} строка {{s}} была дописана {{К}}",
                     замена=(f"{з} {{W}} {{М}} был заменён на {{v}}", f"{з} {{W}} {{М}} было заменено на {{v}}"))
           for вид, з in (("желание", "я хочу, чтобы"), ("нужда", "мне нужно, чтобы"))},
    "de": {вид: dict(создать=f"{з} {{Ф}} erstellt wird", удалить=f"{з} {{Ф}} gelöscht wird",
                     перенести=f"{з} {{Ф}} {{Д}} verschoben wird", переименовать=f"{з} {{Ф}} in {{g}} umbenannt wird",
                     дописать=f"{з} {{К}} um {{S}} ergänzt wird",
                     замена=(f"{з} der Text {{w}} {{М}} durch {{v}} ersetzt wird",
                             f"{з} das Wort {{w}} {{М}} durch {{v}} ersetzt wird"))
           for вид, з in (("желание", "ich möchte, dass"), ("нужда", "es ist nötig, dass"))},
    "fr": {вид: dict(создать=f"{з} {{Ф}} soit créé", удалить=f"{з} {{Ф}} soit supprimé",
                     перенести=f"{з} {{Ф}} soit déplacé {{Д}}", переименовать=f"{з} {{Фи}} soit renommé en {{g}}",
                     дописать=f"{з} {{S}} soit ajoutée {{К}}", замена=(f"{з} {{W}} {{М}} soit remplacé par {{v}}",) * 2)
           for вид, з in (("желание", "je veux que"), ("нужда", "il faut que"))},
    "es": {вид: dict(создать=f"{з} {{Ф}} sea creado", удалить=f"{з} {{Ф}} sea eliminado",
                     перенести=f"{з} {{Ф}} sea movido {{Д}}", переименовать=f"{з} {{Фи}} sea renombrado como {{g}}",
                     дописать=f"{з} {{S}} sea añadida {{К}}",
                     замена=(f"{з} {{W}} {{М}} sea reemplazado por {{v}}",
                             f"{з} {{W}} {{М}} sea reemplazada por {{v}}"))
           for вид, з in (("желание", "quiero que"), ("нужда", "necesito que"))},
    "it": {вид: dict(создать=f"{з} {{Ф}} sia creato", удалить=f"{з} {{Ф}} sia eliminato",
                     перенести=f"{з} {{Ф}} sia spostato {{Д}}", переименовать=f"{з} {{Фи}} sia rinominato in {{g}}",
                     дописать=f"{з} {{S}} sia aggiunta {{К}}",
                     замена=(f"{з} {{W}} {{М}} sia sostituito con {{v}}", f"{з} {{W}} {{М}} sia sostituita con {{v}}"))
           for вид, з in (("желание", "voglio che"), ("нужда", "ho bisogno che"))},
    "pt": {вид: dict(создать=f"{з} {{Ф}} seja criado", удалить=f"{з} {{Ф}} seja eliminado",
                     перенести=f"{з} {{Ф}} seja movido {{Д}}", переименовать=f"{з} {{Фи}} seja renomeado para {{g}}",
                     дописать=f"{з} {{S}} seja acrescentada {{К}}",
                     замена=(f"{з} {{W}} {{М}} seja substituído por {{v}}",
                             f"{з} {{W}} {{М}} seja substituída por {{v}}"))
           for вид, з in (("желание", "quero que"), ("нужда", "preciso que"))},
    "nl": {вид: dict(создать=f"{з} {{Ф}} gecreëerd wordt", удалить=f"{з} {{Ф}} verwijderd wordt",
                     перенести=f"{з} {{Ф}} {{Д}} verplaatst wordt",
                     переименовать=f"{з} {{Фи}} naar {{g}} hernoemd wordt", дописать=f"{з} {{S}} {{К}} gezet wordt",
                     замена=(f"{з} {{W}} {{М}} door {{v}} vervangen wordt",) * 2)
           for вид, з in (("желание", "ik wil dat"), ("нужда", "het is nodig dat"))},
    "pl": {вид: dict(создать=f"{з} {{Ф}} został utworzony", удалить=f"{з} {{Ф}} został usunięty",
                     перенести=f"{з} {{Ф}} został przeniesiony {{Д}}",
                     переименовать=f"{з} nazwa {{Фи}} została zmieniona na {{g}}",
                     дописать=f"{з} linia {{s}} została dopisana {{К}}",
                     замена=(f"{з} {{W}} {{М}} został zamieniony na {{v}}",
                             f"{з} {{W}} {{М}} zostało zamienione na {{v}}"))
           for вид, з in (("желание", "chcę, żeby"), ("нужда", "potrzebuję, żeby"))},
}


def страд_желание(язык, вид, акт, **п):
    """Приказ желанием или нуждой с объектом впереди и страдательным причастием (`СТРАД_ЖЕЛАНИЕ`); у замены — шаблон
    слова, когда слот {W} назван фразой слова (одно слово), иначе — текста."""
    шаблон = СТРАД_ЖЕЛАНИЕ[язык][вид][акт]
    if isinstance(шаблон, tuple):
        слово = "W" in п and п["W"] == ОБЪЕКТЫ[язык]["слово"]["в"].format(w=п.get("w"))
        шаблон = шаблон[1 if слово else 0]
    return шаблон.format(**слоты(язык, **п))


# ФАЙЛ ПО ИМЕНИ — «a file called F», «файл с именем F»: третья форма фраз файла (после канонической и голой), в
# падеже шаблона. «новый» — у создания (неопределённый артикль), прочие — у файла, какой есть.
НАЗВАННЫЙ = {
    "en": dict(вин="the file called {f}", имени="the file called {f}", в_файл="to the file called {f}",
               в_файле="in the file called {f}", файла="of the file called {f}", новый="a file called {f}"),
    "ru": dict(вин="файл с именем {f}", имени="файл с именем {f}", в_файл="в файл с именем {f}",
               в_файле="в файле с именем {f}", файла="файла с именем {f}", новый="файл с именем {f}"),
    "de": dict(вин="die Datei namens {f}", имени="der Datei namens {f}", в_файл="die Datei namens {f}",
               в_файле="in der Datei namens {f}", файла="der Datei namens {f}", новый="eine Datei namens {f}"),
    "fr": dict(вин="le fichier nommé {f}", имени="le fichier nommé {f}", в_файл="au fichier nommé {f}",
               в_файле="dans le fichier nommé {f}", файла="du fichier nommé {f}", новый="un fichier nommé {f}"),
    "es": dict(вин="el archivo llamado {f}", имени="el archivo llamado {f}", в_файл="al archivo llamado {f}",
               в_файле="en el archivo llamado {f}", файла="del archivo llamado {f}", новый="un archivo llamado {f}"),
    "it": dict(вин="il file chiamato {f}", имени="il file chiamato {f}", в_файл="al file chiamato {f}",
               в_файле="nel file chiamato {f}", файла="del file chiamato {f}", новый="un file chiamato {f}"),
    "pt": dict(вин="o ficheiro chamado {f}", имени="o ficheiro chamado {f}", в_файл="ao ficheiro chamado {f}",
               в_файле="no ficheiro chamado {f}", файла="do ficheiro chamado {f}", новый="um ficheiro chamado {f}"),
    "nl": dict(вин="het bestand met de naam {f}", имени="het bestand met de naam {f}",
               в_файл="onderaan het bestand met de naam {f}", в_файле="in het bestand met de naam {f}",
               файла="van het bestand met de naam {f}", новый="een bestand met de naam {f}"),
    "pl": dict(вин="plik o nazwie {f}", имени="pliku o nazwie {f}", в_файл="do pliku o nazwie {f}",
               в_файле="w pliku o nazwie {f}", файла="pliku o nazwie {f}", новый="plik o nazwie {f}"),
}
for _я, _о in ОБЪЕКТЫ.items():
    _н = НАЗВАННЫЙ[_я]
    _о["файл_вин"] = _о["файл_вин"] + (_н["вин"],)
    for _фраза in ("файл_имени", "в_файл", "в_файле", "файла"):
        _о[_фраза] = _о[_фраза] + (_н[_фраза.replace("файл_имени", "имени")],)
# КАТАЛОГ — второе имя папки в живой речи программиста (27.09, наряд ведущего (d), места: «directory», «каталог»,
# «Verzeichnis», «répertoire», «directorio», «diretório», «katalog»): фразы места той же двери объектов, в падежах
# фраз папки; прежние ряды фраз папки не тронуты — формы и основы показов стоят на их номерах
for _я, (_в, _на, _из) in {"en": ("in the directory {d}", "to the directory {d}", "from the directory {d}"),
                          "ru": ("в каталоге {d}", "в каталог {d}", "из каталога {d}"),
                          "de": ("im Verzeichnis {d}", "in das Verzeichnis {d}", "aus dem Verzeichnis {d}"),
                          "fr": ("dans le répertoire {d}", "dans le répertoire {d}", "du répertoire {d}"),
                          "es": ("en el directorio {d}", "al directorio {d}", "del directorio {d}"),
                          "it": ("nella directory {d}", "nella directory {d}", "dalla directory {d}"),
                          "pt": ("no diretório {d}", "para o diretório {d}", "do diretório {d}"),
                          "nl": ("in de directory {d}", "naar de directory {d}", "uit de directory {d}"),
                          "pl": ("w katalogu {d}", "do katalogu {d}", "z katalogu {d}")}.items():
    ОБЪЕКТЫ[_я].update(в_каталоге=(_в,), в_каталог=(_на,), из_каталога=(_из,))
# СЛОВО КЛАССА ФАЙЛА ВТОРЫМ ИМЕНЕМ (28.09, наряд ведущего (б), ход «синоним»): «документ» — у всякого акта над файлом
# и вопроса о файле те же пять фраз, что у файла (винительный, родительный, «в файле», «в файл», имя при
# переименовании), в падеже шаблона двери; брат «каталога» у папки
for _я, _фразы in {
        "en": ("the document {f}", "of the document {f}", "in the document {f}", "to the document {f}",
               "the document {f}"),
        "ru": ("документ {f}", "документа {f}", "в документе {f}", "в документ {f}", "документ {f}"),
        "de": ("das Dokument {f}", "des Dokuments {f}", "im Dokument {f}", "das Dokument {f}", "dem Dokument {f}"),
        "fr": ("le document {f}", "du document {f}", "dans le document {f}", "au document {f}", "le document {f}"),
        "es": ("el documento {f}", "del documento {f}", "en el documento {f}", "al documento {f}", "el documento {f}"),
        "it": ("il documento {f}", "del documento {f}", "nel documento {f}", "al documento {f}", "il documento {f}"),
        "pt": ("o documento {f}", "do documento {f}", "no documento {f}", "ao documento {f}", "o documento {f}"),
        "nl": ("het document {f}", "van het document {f}", "in het document {f}", "onderaan het document {f}",
               "het document {f}"),
        "pl": ("dokument {f}", "dokumentu {f}", "w dokumencie {f}", "do dokumentu {f}", "dokumentu {f}")}.items():
    ОБЪЕКТЫ[_я].update(zip(("документ_вин", "документа", "в_документе", "в_документ", "документ_имени"),
                           ((x,) for x in _фразы)))
# «в конец файла» — место дописываемой строки (голландское каноническое «onderaan» уже есть «внизу»: здесь — «в
# конец»); папка подлежащим — вторая форма вопроса о числе файлов («how many files does the folder D contain»)
В_КОНЕЦ = {"en": "to the end of the file {f}", "ru": "в конец файла {f}", "de": "die Datei {f} am Ende",
           "fr": "à la fin du fichier {f}", "es": "al final del archivo {f}", "it": "alla fine del file {f}",
           "pt": "ao fim do ficheiro {f}", "nl": "aan het eind van het bestand {f}", "pl": "na końcu pliku {f}"}
ПАПКА_ПОДЛ = {"en": "the folder {d}", "ru": "папка {d}", "de": "der Ordner {d}", "fr": "le dossier {d}",
              "es": "la carpeta {d}", "it": "la cartella {d}", "pt": "a pasta {d}", "nl": "de map {d}",
              "pl": "folder {d}"}
# ЧАСТЬ МЕСТА ВПЕРЕДИ — «in the file F, replace …», «в файле F замени …»: место приказа, вынесенное перед глаголом,
# и знак между ними (запятая там, где язык её ставит). Шаблон остаётся тем же: место вырезается из него, а не пишется
# вторым шаблоном
ВПЕРЕДИ_ЗНАК = {"en": ", ", "ru": " ", "de": " ", "fr": ", ", "es": ", ", "it": ", ", "pt": ", ", "nl": ", ",
                "pl": " "}
# «сколько раз» второй формой — одна правка вопросного оборота
ВОПРОС_РАЗ2 = {"en": "how often does {Wи} occur {М}?", "ru": "как часто {Wи} встречается {М}?",
               "de": "wie viele Male kommt {Wи} {М} vor?", "fr": "combien de fois trouve-t-on {Wи} {М} ?",
               "es": "¿cuántas veces está {Wи} {М}?", "it": "quante volte appare {Wи} {М}?",
               "pt": "quantas vezes surge {Wи} {М}?", "nl": "hoeveel keer komt {Wи} voor {М}?",
               "pl": "ile razy pojawia się {Wи} {М}?"}
# ГЛАГОЛЫ ВХОЖДЕНИЯ (28.09, наряд ведущего (б), ход «синоним»): «сколько раз» иным глаголом вхождения — тот же вопросный
# оборот; глагол второй формы (`ВОПРОС_РАЗ2`) здесь не повторяется
ГЛАГОЛЫ_ВХОЖДЕНИЯ = {
    "en": ("how many times does {Wи} appear {М}?", "how many times does {Wи} show up {М}?"),
    "ru": ("сколько раз {Wи} появляется {М}?", "сколько раз {Wи} попадается {М}?"),
    "de": ("wie oft erscheint {Wи} {М}?", "wie oft taucht {Wи} {М} auf?"),
    "fr": ("combien de fois {Wи} figure-t-il {М} ?", "combien de fois voit-on {Wи} {М} ?"),
    "es": ("¿cuántas veces sale {Wи} {М}?", "¿cuántas veces figura {Wи} {М}?"),
    "it": ("quante volte ricorre {Wи} {М}?", "quante volte si trova {Wи} {М}?"),
    "pt": ("quantas vezes consta {Wи} {М}?", "quantas vezes se encontra {Wи} {М}?"),
    "nl": ("hoe vaak verschijnt {Wи} {М}?", "hoe vaak staat {Wи} {М}?"),
    "pl": ("ile razy {Wи} znajduje się {М}?", "ile razy {Wи} jest {М}?"),
}


# КОНЕЦ ФАЙЛА — место дописываемой строки «в конце файла», одной фразой и в приказе, и впереди него: «append … at the
# end of the file F» ↔ «at the end of the file F, append …»; «добавь» — синоним глагола на той же фразе. `у_конца` —
# приказ, где фраза «в конце» стоит внутри (у английского — «at» вместо «to», у русского — перед строкой, у немецкого —
# при строке-дополнении); языки, у каких каноническое «конец» уже есть «в конце», его не заводят.
КОНЕЦ = {
    "en": dict(место="at the end of the file {f}",
               впереди="at the end of the file {f}, append {S}", у_конца="append {S} at the end of the file {f}",
               добавь="add {S} at the end of the file {f}"),
    "ru": dict(место="в конец файла {f}",
               впереди="в конец файла {f} допиши {S}", у_конца="допиши в конец файла {f} {S}",
               добавь="добавь в конец файла {f} {S}"),
    "de": dict(место="am Ende der Datei {f}",
               впереди="am Ende der Datei {f} ergänze {S}", у_конца="ergänze {S} am Ende der Datei {f}",
               добавь="füge {S} am Ende der Datei {f} hinzu"),
    "fr": dict(место="à la fin du fichier {f}",
               впереди="à la fin du fichier {f}, ajoute {S}", добавь="rajoute {S} à la fin du fichier {f}"),
    "es": dict(место="al final del archivo {f}",
               впереди="al final del archivo {f}, añade {S}", добавь="agrega {S} al final del archivo {f}"),
    "it": dict(место="alla fine del file {f}",
               впереди="alla fine del file {f}, aggiungi {S}", добавь="accoda {S} alla fine del file {f}"),
    "pt": dict(место="ao fim do ficheiro {f}",
               впереди="ao fim do ficheiro {f}, acrescenta {S}", добавь="adiciona {S} ao fim do ficheiro {f}"),
    "nl": dict(место="aan het eind van het bestand {f}",
               впереди="aan het eind van het bestand {f}, zet {S}",
               добавь="plaats {S} aan het eind van het bestand {f}"),
    "pl": dict(место="na końcu pliku {f}",
               впереди="na końcu pliku {f} dopisz {S}", добавь="dodaj {S} na końcu pliku {f}"),
}
# ПЕРЕНОС С МЕСТОМ ВПЕРЕДИ — лишь там, где язык ставит место назначения перед повелением естественно («в папку D
# перенеси файл X», «in den Ordner D verschiebe …», «do folderu D przenieś …»); прочие этой формы не заводят
ВПЕРЕДИ_ПЕРЕНОС = frozenset({"ru", "de", "pl"})
# СЧЁТ С МЕСТОМ ВПЕРЕДИ (28.09, наряд ведущего (б), ход «порядок»): «в файле F сколько раз встречается слово "x"?» —
# там, где голос выносит место перед вопросным словом естественно (знак — `ВПЕРЕДИ_ЗНАК`); у de и nl вопрос держит
# глагол вторым, и место перед вопросным словом неестественно — этой формы они не заводят
ВПЕРЕДИ_ВОПРОС = frozenset({"en", "ru", "fr", "es", "it", "pt", "pl"})


def впереди(язык, место, приказ_без_места):
    """Приказ с местом впереди: «in the file F, replace …» — место, знак языка, приказ без места."""
    return место + ВПЕРЕДИ_ЗНАК[язык] + приказ_без_места


# РОДЫ ЖИВЫХ ПРОСЬБ (26.09, третий заказ ведущего — по переписи живых просьб к агенту, не по ключам): план из трёх
# актов, условный приказ на ходе мира, «все файлы, кроме …», два объекта в одном приказе, ссылка на прошлый шаг без
# местоимения. Речь организма — канонические слова актов; иначе сказан лишь приказ пользователя.
#
# ПЛАН ИЗ ТРЁХ АКТОВ — связка трёх: {B1}/{C1} — глагол, {B2}/{C2} — остаток (местоимение там, где его ставит язык;
# нидерландское наречие — после глагола повеления, как у связки двух)
СВЯЗКА3 = {
    "en": ("{A}, then {B1} {B2}, then {C1} {C2}", "i propose three acts: {A}, then {B}, then {C}"),
    "ru": ("{A}, затем {B1} {B2}, затем {C1} {C2}", "предлагаю три акта: {A}, затем {B}, затем {C}"),
    "de": ("{A}, dann {B1} {B2}, dann {C1} {C2}", "ich schlage drei Handlungen vor: {A}, dann {B}, dann {C}"),
    "fr": ("{A}, puis {B1} {B2}, puis {C1} {C2}", "je propose trois actes : {A}, puis {B}, puis {C}"),
    "es": ("{A}, luego {B1} {B2}, luego {C1} {C2}", "propongo tres actos: {A}, luego {B}, luego {C}"),
    "it": ("{A}, poi {B1} {B2}, poi {C1} {C2}", "propongo tre atti: {A}, poi {B}, poi {C}"),
    "pt": ("{A}, depois {B1} {B2}, depois {C1} {C2}", "proponho três atos: {A}, depois {B}, depois {C}"),
    "nl": ("{A}, {B1} dan {B2} en {C1} daarna {C2}", "ik stel drie handelingen voor: {A}, dan {B} en daarna {C}"),
    "pl": ("{A}, potem {B1} {B2}, potem {C1} {C2}", "proponuję trzy akty: {A}, potem {B}, potem {C}"),
}


def связать3(язык, ступень, A, B, C):
    """Приказ или тело предложения плана из трёх актов; второй и третий приказ — как у `связать`."""
    приказ_, предложение_ = СВЯЗКА3[язык]
    if ступень == "приказ":
        (B1, B2), (C1, C2) = (x if isinstance(x, tuple) else x.split(" ", 1) for x in (B, C))
        return re.sub(r" +(?=[ ,])", "", приказ_.format(A=A, B1=B1, B2=B2, C1=C1, C2=C2)).rstrip()
    return предложение_.format(A=A, B=B, C=C)


# МЕСТОИМЕНИЕ ВЕТКИ УСЛОВИЯ — «create it», «replace it with …» (объект — файл условия или текст условия); глагол тот
# же, что у акта двери
for _я, _м in {"en": dict(создать=("create", "it"), заменить=("replace", "it with {v}")),
               "ru": dict(создать=("создай", "его"), заменить=("замени", "его на {v}")),
               "de": dict(создать=("erstelle", "sie"), заменить=("ersetze", "ihn durch {v}")),
               "fr": dict(создать=("crée-le", ""), заменить=("remplace-le", "par {v}")),
               "es": dict(создать=("créalo", ""), заменить=("reemplázalo", "por {v}")),
               "it": dict(создать=("crealo", ""), заменить=("sostituiscilo", "con {v}")),
               "pt": dict(создать=("cria-o", ""), заменить=("substitui-o", "por {v}")),
               "nl": dict(создать=("creëer het", ""), заменить=("vervang", "hem door {v}")),
               "pl": dict(создать=("utwórz", "go"), заменить=("zamień", "go na {v}"))}.items():
    МЕСТОИМЕНИЕ[_я].update(_м)

# ВОПРОС ВТОРЫМ ПРИКАЗОМ ПЛАНА — придаточное за зачином и инфинитив предложения (организм говорит путём, какой
# определяет приказ, — `{p}`, и словом вопроса — `{W}`): «прошло» — «run the tests, then let me know how many
# passed», число прошедших берёт отчёт бегуна в ходе мира-процесса; «первая» — «…, then tell me what its first line
# is», «файл» — «…, then let me know which file contains the word "x"» (27.09, наряд ведущего: зачин перед вторым
# вопросом плана). «их» — вопрос о прогоне с местоимением тестов: придаточное за связкой «and» и прямой вопрос за
# «;» — «run the Rust tests; how many of them passed?». Без местоимения обе связки с этим вопросом суть просьбы ключа
# AGENT-K целиком («… and tell me how many passed», «…; how many passed?» — мера счётом genesis_key_overlap, 27.09);
# «tell me how many lines it has» — общий ряд с ключом 8 слов, и зачин вида 1 перед «строк» не ставится.
ВОПРОС_ВТОРОЙ = {
    "en": dict(прошло=("how many passed", "tell how many of them passed"),
               их=("how many of them passed", "how many of them passed?"),
               первая=("what its first line is", "tell what the first line of the file {p} is"),
               файл=("which file contains {W}", "tell which file contains {W}")),
    "ru": dict(прошло=("сколько прошло", "сказать, сколько прошло"),
               их=("сколько из них прошло", "сколько из них прошло?"),
               первая=("какая первая строка в нём", "сказать, какая первая строка в файле {p}"),
               файл=("в каком файле есть {Wи}", "сказать, в каком файле есть {Wи}")),
    "de": dict(прошло=("wie viele bestanden haben", "sagen, wie viele bestanden haben"),
               их=("wie viele davon bestanden haben", "wie viele davon haben bestanden?"),
               первая=("was in ihrer ersten Zeile steht", "sagen, was in der ersten Zeile der Datei {p} steht"),
               файл=("welche Datei {W} enthält", "sagen, welche Datei {W} enthält")),
    "fr": dict(прошло=("combien ont réussi", "dire combien ont réussi"),
               их=("combien d'entre eux ont réussi", "combien d'entre eux ont réussi ?"),
               первая=("quelle est sa première ligne", "dire quelle est la première ligne du fichier {p}"),
               файл=("quel fichier contient {W}", "dire quel fichier contient {W}")),
    "es": dict(прошло=("cuántas pasaron", "decir cuántas pasaron"),
               их=("cuántas de ellas pasaron", "¿cuántas de ellas pasaron?"),
               первая=("cuál es su primera línea", "decir cuál es la primera línea del archivo {p}"),
               файл=("qué archivo contiene {W}", "decir qué archivo contiene {W}")),
    "it": dict(прошло=("quanti sono passati", "dire quanti sono passati"),
               их=("quanti ne sono passati", "quanti ne sono passati?"),
               первая=("qual è la sua prima riga", "dire qual è la prima riga del file {p}"),
               файл=("quale file contiene {W}", "dire quale file contiene {W}")),
    "pt": dict(прошло=("quantos passaram", "dizer quantos passaram"),
               их=("quantos deles passaram", "quantos deles passaram?"),
               первая=("qual é a primeira linha dele", "dizer qual é a primeira linha do ficheiro {p}"),
               файл=("que ficheiro contém {W}", "dizer que ficheiro contém {W}")),
    "nl": dict(прошло=("hoeveel er geslaagd zijn", "zeggen hoeveel er geslaagd zijn"),
               их=("hoeveel ervan geslaagd zijn", "hoeveel ervan zijn geslaagd?"),
               первая=("wat de eerste regel ervan is", "zeggen wat de eerste regel van het bestand {p} is"),
               файл=("welk bestand {W} bevat", "zeggen welk bestand {W} bevat")),
    "pl": dict(прошло=("ile przeszło", "powiedzieć, ile przeszło"),
               их=("ile z nich przeszło", "ile z nich przeszło?"),
               первая=("jaka jest jego pierwsza linia", "powiedzieć, jaka jest pierwsza linia pliku {p}"),
               файл=("który plik zawiera {W}", "powiedzieć, który plik zawiera {W}")),
}
for _я, _в in ВОПРОС_ВТОРОЙ.items():
    МЕСТОИМЕНИЕ[_я]["прошло"] = (зачин(_я, 0, _в["прошло"][0]), _в["прошло"][1])

# ОДИНОЧНЫЙ ВОПРОС ЗА ЗАЧИНОМ (27.09, наряд ведущего (e)) — косвенный вопрос всякого одиночного вопроса дома
# `toolrepo` той же дверью, что второй вопрос плана («файл» — прежний): «tell me which line of the file F contains the
# text "x"», «скажи, сколько строк в файле F», «sag mir, was in Zeile 2 der Datei F steht» — у de и nl глагол
# косвенного в конце, у en вопрос без инверсии и без «do». Слоты — канонические слоты прямого вопроса дома: файл назван
# ({Фр}, {М}, {Ф}), а не местоимением, как у второго вопроса плана; инфинитив предложения — «сказать» голоса, как у
# «файл», и то же придаточное
for _я, _к in {
        "en": dict(строка="which line {Фр} contains {W}", выбор="what the {c} line {Фр} is",
                   строка_н="what line {a} {Фр} says", ключ="what value {K} has {М}", о_ключе="what {Ф} says about {k}",
                   строк="how many lines {Ф} has", раз="how many times {Wи} occurs {М}",
                   файлов="how many files there are {Дв}"),
        "ru": dict(строка="в какой строке {Фр} стоит {Wи}", выбор="какая {c} строка {Фр}",
                   строка_н="что написано {М} в строке {a}", ключ="какое значение {Kо} {М}",
                   о_ключе="что {Ф} говорит о {k}", строк="сколько строк {М}", раз="сколько раз {Wи} встречается {М}",
                   файлов="сколько файлов {Дв}"),
        "de": dict(строка="in welcher Zeile {Фр} {Wи} steht", выбор="was in der {c} Zeile {Фр} steht",
                   строка_н="was in Zeile {a} {Фр} steht", ключ="welchen Wert {Kо} {М} hat",
                   о_ключе="was {Ф} über {k} sagt", строк="wie viele Zeilen {Ф} hat", раз="wie oft {Wи} {М} vorkommt",
                   файлов="wie viele Dateien {Дв} sind"),
        "fr": dict(строка="à quelle ligne {Фр} se trouve {Wи}", выбор="quelle est la {c} ligne {Фр}",
                   строка_н="ce que dit la ligne {a} {Фр}", ключ="quelle est la valeur {Kо} {М}",
                   о_ключе="ce que dit {Ф} sur {k}", строк="combien de lignes contient {Ф}",
                   раз="combien de fois {Wи} apparaît {М}", файлов="combien de fichiers il y a {Дв}"),
        "es": dict(строка="en qué línea {Фр} está {Wи}", выбор="cuál es la {c} línea {Фр}",
                   строка_н="qué dice la línea {a} {Фр}", ключ="cuál es el valor {Kо} {М}",
                   о_ключе="qué dice {Ф} sobre {k}", строк="cuántas líneas tiene {Ф}",
                   раз="cuántas veces aparece {Wи} {М}", файлов="cuántos archivos hay {Дв}"),
        "it": dict(строка="in quale riga {Фр} si trova {Wи}", выбор="qual è {c} riga {Фр}",
                   строка_н="cosa dice la riga {a} {Фр}", ключ="qual è il valore {Kо} {М}", о_ключе="cosa dice {Ф} su {k}",
                   строк="quante righe ha {Ф}", раз="quante volte compare {Wи} {М}", файлов="quanti file ci sono {Дв}"),
        "pt": dict(строка="em que linha {Фр} está {Wи}", выбор="qual é a {c} linha {Фр}",
                   строка_н="o que diz a linha {a} {Фр}", ключ="qual é o valor {Kо} {М}",
                   о_ключе="o que diz {Ф} sobre {k}", строк="quantas linhas tem {Ф}",
                   раз="quantas vezes aparece {Wи} {М}", файлов="quantos ficheiros há {Дв}"),
        "nl": dict(строка="in welke regel {Фр} {Wи} staat", выбор="wat de {c} regel {Фр} is",
                   строка_н="wat er in regel {a} {Фр} staat", ключ="wat de waarde {Kо} {М} is",
                   о_ключе="wat {Ф} over {k} zegt", строк="hoeveel regels {Ф} heeft", раз="hoe vaak {Wи} {М} voorkomt",
                   файлов="hoeveel bestanden er {Дв} zitten"),
        "pl": dict(строка="w której linii {Фр} jest {Wи}", выбор="jaka jest {c} linia {Фр}",
                   строка_н="co jest {М} w linii {a}", ключ="jaka jest wartość {Kо} {М}", о_ключе="co {Ф} mówi o {k}",
                   строк="ile linii ma {Ф}", раз="ile razy {Wи} występuje {М}", файлов="ile plików jest {Дв}")}.items():
    _сказать, _, _хвост = ВОПРОС_ВТОРОЙ[_я]["файл"][1].rpartition(ВОПРОС_ВТОРОЙ[_я]["файл"][0])
    assert _сказать and not _хвост, (_я, ВОПРОС_ВТОРОЙ[_я]["файл"])
    ВОПРОС_ВТОРОЙ[_я].update({_в: (_п, _сказать + _п) for _в, _п in _к.items()})

# НАЙДЕННОЕ МЕСТОИМЕНИЕМ (27.09, наряд ведущего (f)) — косвенный вопрос о файле, где стоит найденное, с местоимением на
# месте текста: «look for the word "x" and tell me which file it's in» («it's» — лишь у en: так говорит голос); «в каком
# это файле», «in welcher Datei das steht», «in welk bestand dat staat» — «это», «das», «dat» без рода слова и текста;
# инфинитив предложения — «сказать» голоса, как у «файл»
for _я, _п in {"en": "which file it's in", "ru": "в каком это файле", "de": "in welcher Datei das steht",
               "fr": "dans quel fichier il est", "es": "en qué archivo está", "it": "in quale file è",
               "pt": "em que ficheiro está", "nl": "in welk bestand dat staat", "pl": "w którym pliku jest"}.items():
    _сказать, _, _хвост = ВОПРОС_ВТОРОЙ[_я]["файл"][1].rpartition(ВОПРОС_ВТОРОЙ[_я]["файл"][0])
    assert _сказать and not _хвост, (_я, ВОПРОС_ВТОРОЙ[_я]["файл"])
    ВОПРОС_ВТОРОЙ[_я]["файл_оно"] = (_п, _сказать + _п)
# СОЮЗ ПЕРЕД ТОЙ ЖЕ ГЛАСНОЙ (27.09, наряд ведущего (f), союз «and» между актами): итальянское «e» перед словом на «e»
# — «ed» («… ed esegui i test Python», «… ed elimina il file …»)
СОЮЗ_ЕВФОНИЯ = {"it": ("e", "ed")}

# СВЯЗКА АКТА И ВОПРОСА (27.09, наряд ведущего: связки шире «, then let me know») — «{A} and {B1} {B2}»: второй
# приказ — зачин и придаточное; «{A}; {Q}»: второй — прямой вопрос. Предложение организма — связкой плана `СВЯЗКА`.
СВЯЗКА_ВОПРОСА = {
    "en": ("{A} and {B1} {B2}", "{A}; {Q}"), "ru": ("{A} и {B1} {B2}", "{A}; {Q}"),
    "de": ("{A} und {B1} {B2}", "{A}; {Q}"), "fr": ("{A} et {B1} {B2}", "{A} ; {Q}"),
    "es": ("{A} y {B1} {B2}", "{A}; {Q}"), "it": ("{A} e {B1} {B2}", "{A}; {Q}"),
    "pt": ("{A} e {B1} {B2}", "{A}; {Q}"), "nl": ("{A} en {B1} {B2}", "{A}; {Q}"),
    "pl": ("{A} i {B1} {B2}", "{A}; {Q}"),
}


# КОСВЕННЫЙ ВОПРОС О ЗАПИСИ ПО ИМЕНИ (28.09, долг рода конструкций; М-2075): где лежит файл и сколько файлов носят имя —
# за зачином всякого вида («i need to know where the file F is», «tell me how many files are named F»)
for _я, _в in {"en": dict(где=("where {Ф} is", "tell where {Ф} is"),
                          имён=("how many files are named {f}", "tell how many files are named {f}")),
               "ru": dict(где=("где лежит {Ф}", "сказать, где лежит {Ф}"),
                          имён=("сколько файлов с именем {f}", "сказать, сколько файлов с именем {f}")),
               "de": dict(где=("wo {Ф} liegt", "sagen, wo {Ф} liegt"),
                          имён=("wie viele Dateien {f} heißen", "sagen, wie viele Dateien {f} heißen")),
               "fr": dict(где=("où se trouve {Ф}", "dire où se trouve {Ф}"),
                          имён=("combien de fichiers s'appellent {f}", "dire combien de fichiers s'appellent {f}")),
               "es": dict(где=("dónde está {Ф}", "decir dónde está {Ф}"),
                          имён=("cuántos archivos se llaman {f}", "decir cuántos archivos se llaman {f}")),
               "it": dict(где=("dove si trova {Ф}", "dire dove si trova {Ф}"),
                          имён=("quanti file si chiamano {f}", "dire quanti file si chiamano {f}")),
               "pt": dict(где=("onde está {Ф}", "dizer onde está {Ф}"),
                          имён=("quantos ficheiros se chamam {f}", "dizer quantos ficheiros se chamam {f}")),
               "nl": dict(где=("waar {Ф} staat", "zeggen waar {Ф} staat"),
                          имён=("hoeveel bestanden {f} heten", "zeggen hoeveel bestanden {f} heten")),
               "pl": dict(где=("gdzie jest {Ф}", "powiedzieć, gdzie jest {Ф}"),
                          имён=("ile plików nazywa się {f}", "powiedzieć, ile plików nazywa się {f}"))}.items():
    ВОПРОС_ВТОРОЙ[_я].update(_в)


def второй_вопрос(язык, вопрос_, вид, **п):
    """(глагол, остаток) второго приказа: зачин вида `вид` и придаточное вопроса `вопрос_` со слотами."""
    return зачин(язык, вид, ВОПРОС_ВТОРОЙ[язык][вопрос_][0].format(**слоты(язык, **п)))


def связать_вопрос(язык, связка, A, B):
    """Приказ «акт и вопрос»: `связка` «и» — B есть (глагол, остаток) зачина с придаточным; «прямо» — B есть прямой
    вопрос, приказ кончается его знаком."""
    и_, прямо_ = СВЯЗКА_ВОПРОСА[язык]
    if связка == "и":
        return и_.format(A=A, B1=B[0], B2=B[1]).rstrip()
    return прямо_.format(A=A, Q=B)

# ССЫЛКА НА ПРОШЛЫЙ ШАГ — второй приказ плана иначе, чем каноническим «it» двери МЕСТОИМЕНИЕ: (глагол, остаток) той же
# связки. «этот», «тот_же» — без местоимения («this file», «the same file» на месте «it»); «строк» — лишь «этот»: «how
# many lines the same file has» язык не говорит. Виды шире — с местоимением и синонимом акта («its line count», «into
# it», «as its only line») — ниже, у `ССЫЛКА_СИНОНИМОМ` (27.09, наряд (f))
ССЫЛКА = {
    "en": dict(этот=dict(дописать=("append", "{S} to this file"), удалить=("delete", "this file"),
                         строк=зачин("en", 0, "how many lines this file has")),
               тот_же=dict(дописать=("append", "{S} to the same file"), удалить=("delete", "the same file"))),
    "ru": dict(этот=dict(дописать=("допиши", "в этот файл {S}"), удалить=("удали", "этот файл"),
                         строк=зачин("ru", 0, "сколько строк в этом файле")),
               тот_же=dict(дописать=("допиши", "в тот же файл {S}"), удалить=("удали", "тот же файл"))),
    "de": dict(этот=dict(дописать=("ergänze", "diese Datei um {S}"), удалить=("lösche", "diese Datei"),
                         строк=зачин("de", 0, "wie viele Zeilen diese Datei hat")),
               тот_же=dict(дописать=("ergänze", "dieselbe Datei um {S}"), удалить=("lösche", "dieselbe Datei"))),
    "fr": dict(этот=dict(дописать=("ajoute", "{S} à ce fichier"), удалить=("supprime", "ce fichier"),
                         строк=зачин("fr", 0, "combien de lignes contient ce fichier")),
               тот_же=dict(дописать=("ajoute", "{S} au même fichier"), удалить=("supprime", "le même fichier"))),
    "es": dict(этот=dict(дописать=("añade", "{S} a este archivo"), удалить=("elimina", "este archivo"),
                         строк=зачин("es", 0, "cuántas líneas tiene este archivo")),
               тот_же=dict(дописать=("añade", "{S} al mismo archivo"), удалить=("elimina", "el mismo archivo"))),
    "it": dict(этот=dict(дописать=("aggiungi", "{S} a questo file"), удалить=("elimina", "questo file"),
                         строк=зачин("it", 0, "quante righe ha questo file")),
               тот_же=dict(дописать=("aggiungi", "{S} allo stesso file"), удалить=("elimina", "lo stesso file"))),
    "pt": dict(этот=dict(дописать=("acrescenta", "{S} a este ficheiro"), удалить=("elimina", "este ficheiro"),
                         строк=зачин("pt", 0, "quantas linhas tem este ficheiro")),
               тот_же=dict(дописать=("acrescenta", "{S} ao mesmo ficheiro"),
                           удалить=("elimina", "o mesmo ficheiro"))),
    "nl": dict(этот=dict(дописать=("zet", "{S} onderaan dit bestand"), удалить=("verwijder", "dit bestand"),
                         строк=зачин("nl", 0, "hoeveel regels dit bestand heeft")),
               тот_же=dict(дописать=("zet", "{S} onderaan hetzelfde bestand"),
                           удалить=("verwijder", "hetzelfde bestand"))),
    "pl": dict(этот=dict(дописать=("dopisz", "do tego pliku {S}"), удалить=("usuń", "ten plik"),
                         строк=зачин("pl", 0, "ile linii ma ten plik")),
               тот_же=dict(дописать=("dopisz", "do tego samego pliku {S}"), удалить=("usuń", "ten sam plik"))),
}


# ВИДЫ ССЫЛКИ ШИРЕ (27.09, наряд ведущего (f), планы) — второй приказ плана иначе, чем каноническим «it» двери
# МЕСТОИМЕНИЕ; новые виды — в конце ряда (прежние циклы берут «этот» и «тот_же» по имени); предложение и отчёт организма
# — канонические. «число» — число строк несомого файла словом единицы голоса, зачином двери: «tell me its line count»,
# «сообщи, каково число строк в нём», «dis-moi son nombre de lignes». «в_него» — «into it» глаголом акта там, где канон
# голоса — не место («añade … en él», «acrescenta … nele», «zet … erin»; у ru, fr, it, pl канон уже место — «допиши в
# него», «ajoute-y», «aggiungici», «dopisz do niego»). «в_него·i» — «into it» синонимом акта там, где глаголом акта
# голос его не говорит (слово ведущего): «put / write … into it», «schreib … hinein», «füge … ein» — глагол из ряда
# двери синонимов (`СИНОНИМЫ`). «единственная» — строка в новый файл: «add "x" as its only line», «допиши в него «x»
# единственной строкой», «schreib „x“ als einzige Zeile hinein»
for _я, _в in {
        "en": {"число": dict(строк=зачин("en", 1, "its line count")),
               "в_него·1": dict(дописать=("put", "{S} into it")), "в_него·2": dict(дописать=("write", "{S} into it")),
               "единственная": dict(дописать=("add", "{s} as its only line"))},
        "ru": {"число": dict(строк=зачин("ru", 2, "каково число строк в нём")),
               "единственная": dict(дописать=("допиши", "в него {s} единственной строкой"))},
        "de": {"число": dict(строк=зачин("de", 0, "wie hoch ihre Zeilenzahl ist")),
               "в_него·1": dict(дописать=("schreib", "{S} hinein")), "в_него·2": dict(дописать=("füge", "{S} ein")),
               "единственная": dict(дописать=("schreib", "{s} als einzige Zeile hinein"))},
        "fr": {"число": dict(строк=зачин("fr", 0, "son nombre de lignes")),
               "единственная": dict(дописать=("ajoute", "{s} comme seule ligne"))},
        "es": {"число": dict(строк=зачин("es", 0, "su número de líneas")), "в_него": dict(дописать=("añade", "{S} en él")),
               "единственная": dict(дописать=("añade", "{s} como única línea"))},
        "it": {"число": dict(строк=зачин("it", 0, "il suo numero di righe")),
               "единственная": dict(дописать=("aggiungi", "{s} come unica riga"))},
        "pt": {"число": dict(строк=зачин("pt", 0, "o número de linhas dele")),
               "в_него": dict(дописать=("acrescenta", "{S} nele")),
               "единственная": dict(дописать=("acrescenta", "{s} como única linha"))},
        "nl": {"число": dict(строк=зачин("nl", 0, "het aantal regels ervan")), "в_него": dict(дописать=("zet", "{S} erin")),
               "единственная": dict(дописать=("zet", "{s} erin als enige regel"))},
        "pl": {"число": dict(строк=зачин("pl", 0, "jaka jest liczba jego linii")),
               "единственная": dict(дописать=("dopisz", "do niego {s} jako jedyną linię"))}}.items():
    ССЫЛКА[_я].update(_в)
# виды ссылки, какие приказ пользователя вправе сказать синонимом акта: самопроверка дома сверяет их глагол с глаголом
# акта или с рядом двери синонимов, прочих — с глаголом акта
ССЫЛКА_СИНОНИМОМ = frozenset({"в_него·1", "в_него·2", "единственная"})


def ссылка(язык, вид, акт, **п):
    """(глагол, остаток) второго приказа со ссылкой «этот» или «тот же» на месте местоимения."""
    глагол, остаток = ССЫЛКА[язык][вид][акт]
    return глагол, остаток.format(**слоты(язык, **п))


# УСЛОВНЫЙ ПРИКАЗ НА ХОДЕ МИРА — «if the file F exists, append … to it, otherwise create it»: условие проверяет мир
# (чтение файла, находка текста), и ветка — ход мира. `если` — условие впереди (`есть_если`, `содержит_если` —
# придаточным: немецкий и нидерландский ставят глагол в конец, португальский — будущее сослагательное); `после` и
# `после_текст` — хвост условия после приказа; `есть`, `нет`, `содержит` — итог проверки; `иначе` — ветка «иначе» в
# приказе, `иначе_пр` — в предложении (инфинитивом; немецкий и нидерландский — zu/te-формой). Не выполнено — хвост
# условия у двери хода (`actturn.РЕЧЬ_УСЛОВИЯ`).
УСЛОВИЕ = {
    "en": dict(если="if {У}, {Т}", иначе=", otherwise {И}", иначе_пр=", otherwise to {inf}", после=" if it exists",
               после_текст=" if it is there", есть_если="the file {f} exists", есть="the file {f} exists",
               нет="the file {f} does not exist", содержит_если="the file {f} contains {W}",
               содержит="the file {f} contains {W}"),
    "ru": dict(если="если {У}, {Т}", иначе=", иначе {И}", иначе_пр=", иначе {inf}", после=", если он есть",
               после_текст=", если он там есть", есть_если="файл {f} есть", есть="файл {f} есть", нет="файла {f} нет",
               содержит_если="в файле {f} есть {Wи}", содержит="в файле {f} есть {Wи}"),
    "de": dict(если="wenn {У}, {Т}", иначе=", sonst {И}", иначе_пр=", sonst {zu}", после=", wenn sie existiert",
               после_текст=", wenn er dort steht", есть_если="die Datei {f} existiert", есть="die Datei {f} existiert",
               нет="die Datei {f} existiert nicht", содержит_если="die Datei {f} {W} enthält",
               содержит="die Datei {f} enthält {W}"),
    "fr": dict(если="si {У}, {Т}", иначе=", sinon {И}", иначе_пр=", sinon de {inf}", после=" s'il existe",
               после_текст=" s'il y figure", есть_если="le fichier {f} existe", есть="le fichier {f} existe",
               нет="le fichier {f} n'existe pas", содержит_если="le fichier {f} contient {W}",
               содержит="le fichier {f} contient {W}"),
    "es": dict(если="si {У}, {Т}", иначе=", si no, {И}", иначе_пр=", si no, {inf}", после=" si existe",
               после_текст=" si aparece", есть_если="el archivo {f} existe", есть="el archivo {f} existe",
               нет="el archivo {f} no existe", содержит_если="el archivo {f} contiene {W}",
               содержит="el archivo {f} contiene {W}"),
    "it": dict(если="se {У}, {Т}", иначе=", altrimenti {И}", иначе_пр=", altrimenti di {inf}", после=" se esiste",
               после_текст=" se c'è", есть_если="il file {f} esiste", есть="il file {f} esiste",
               нет="il file {f} non esiste", содержит_если="il file {f} contiene {W}",
               содержит="il file {f} contiene {W}"),
    "pt": dict(если="se {У}, {Т}", иначе=", senão {И}", иначе_пр=", senão {inf}", после=" se existir",
               после_текст=" se lá estiver", есть_если="o ficheiro {f} existir", есть="o ficheiro {f} existe",
               нет="o ficheiro {f} não existe", содержит_если="o ficheiro {f} contiver {W}",
               содержит="o ficheiro {f} contém {W}"),
    "nl": dict(если="als {У}, {Т}", иначе=", anders {И}", иначе_пр=", anders {zu}", после=" als het bestaat",
               после_текст=" als die erin staat", есть_если="het bestand {f} bestaat", есть="het bestand {f} bestaat",
               нет="het bestand {f} bestaat niet", содержит_если="het bestand {f} {W} bevat",
               содержит="het bestand {f} bevat {W}"),
    "pl": dict(если="jeśli {У}, {Т}", иначе=", w przeciwnym razie {И}", иначе_пр=", w przeciwnym razie {inf}",
               после=", jeśli istnieje", после_текст=", jeśli tam jest", есть_если="plik {f} istnieje",
               есть="plik {f} istnieje", нет="plik {f} nie istnieje", содержит_если="plik {f} zawiera {W}",
               содержит="plik {f} zawiera {W}"),
}


def не_выполнено(язык):
    """«the condition is not met, the act is not performed» — хвост условия у двери хода `actturn`."""
    return A.РЕЧЬ_УСЛОВИЯ[язык]["не_выполнено"].split(" — ", 1)[1]


# ВСЕ ФАЙЛЫ ПАПКИ, КРОМЕ НАЗВАННОГО — «delete all files in the folder D except N» и правка отрицанием «…, but don't
# touch N»: приказ, инфинитив предложения (zu/te-форма — у немецкого и нидерландского) и приказ с «не трогай». Глагол
# — тот же, что у акта двери; {e} — папка, куда переносят
КРОМЕ = {
    "en": dict(удалить=dict(imp="delete all files in the folder {d} except {n}",
                            inf="delete all files in the folder {d} except {n}",
                            не_трогай="delete all files in the folder {d}, but don't touch {n}"),
               перенести=dict(imp="move all files from the folder {d} to the folder {e} except {n}",
                              inf="move all files from the folder {d} to the folder {e} except {n}",
                              не_трогай="move all files from the folder {d} to the folder {e}, but don't touch {n}")),
    "ru": dict(удалить=dict(imp="удали все файлы в папке {d}, кроме {n}", inf="удалить все файлы в папке {d}, кроме {n}",
                            не_трогай="удали все файлы в папке {d}, но не трогай {n}"),
               перенести=dict(imp="перенеси все файлы из папки {d} в папку {e}, кроме {n}",
                              inf="перенести все файлы из папки {d} в папку {e}, кроме {n}",
                              не_трогай="перенеси все файлы из папки {d} в папку {e}, но не трогай {n}")),
    "de": dict(удалить=dict(imp="lösche alle Dateien im Ordner {d} außer {n}",
                            inf="alle Dateien im Ordner {d} außer {n} löschen",
                            zu="alle Dateien im Ordner {d} außer {n} zu löschen",
                            не_трогай="lösche alle Dateien im Ordner {d}, aber rühr {n} nicht an"),
               перенести=dict(imp="verschiebe alle Dateien außer {n} aus dem Ordner {d} in den Ordner {e}",
                              inf="alle Dateien außer {n} aus dem Ordner {d} in den Ordner {e} verschieben",
                              zu="alle Dateien außer {n} aus dem Ordner {d} in den Ordner {e} zu verschieben",
                              не_трогай="verschiebe alle Dateien aus dem Ordner {d} in den Ordner {e}, aber rühr {n} "
                                        "nicht an")),
    "fr": dict(удалить=dict(imp="supprime tous les fichiers du dossier {d} sauf {n}",
                            inf="supprimer tous les fichiers du dossier {d} sauf {n}",
                            не_трогай="supprime tous les fichiers du dossier {d}, mais ne touche pas à {n}"),
               перенести=dict(imp="déplace tous les fichiers du dossier {d} dans le dossier {e} sauf {n}",
                              inf="déplacer tous les fichiers du dossier {d} dans le dossier {e} sauf {n}",
                              не_трогай="déplace tous les fichiers du dossier {d} dans le dossier {e}, mais ne touche "
                                        "pas à {n}")),
    "es": dict(удалить=dict(imp="elimina todos los archivos de la carpeta {d} excepto {n}",
                            inf="eliminar todos los archivos de la carpeta {d} excepto {n}",
                            не_трогай="elimina todos los archivos de la carpeta {d}, pero no toques {n}"),
               перенести=dict(imp="mueve todos los archivos de la carpeta {d} a la carpeta {e} excepto {n}",
                              inf="mover todos los archivos de la carpeta {d} a la carpeta {e} excepto {n}",
                              не_трогай="mueve todos los archivos de la carpeta {d} a la carpeta {e}, pero no toques "
                                        "{n}")),
    "it": dict(удалить=dict(imp="elimina tutti i file della cartella {d} tranne {n}",
                            inf="eliminare tutti i file della cartella {d} tranne {n}",
                            не_трогай="elimina tutti i file della cartella {d}, ma non toccare {n}"),
               перенести=dict(imp="sposta tutti i file della cartella {d} nella cartella {e} tranne {n}",
                              inf="spostare tutti i file della cartella {d} nella cartella {e} tranne {n}",
                              не_трогай="sposta tutti i file della cartella {d} nella cartella {e}, ma non toccare "
                                        "{n}")),
    "pt": dict(удалить=dict(imp="elimina todos os ficheiros da pasta {d} exceto {n}",
                            inf="eliminar todos os ficheiros da pasta {d} exceto {n}",
                            не_трогай="elimina todos os ficheiros da pasta {d}, mas não toques em {n}"),
               перенести=dict(imp="move todos os ficheiros da pasta {d} para a pasta {e} exceto {n}",
                              inf="mover todos os ficheiros da pasta {d} para a pasta {e} exceto {n}",
                              не_трогай="move todos os ficheiros da pasta {d} para a pasta {e}, mas não toques em "
                                        "{n}")),
    "nl": dict(удалить=dict(imp="verwijder alle bestanden in de map {d} behalve {n}",
                            inf="alle bestanden in de map {d} behalve {n} verwijderen",
                            zu="alle bestanden in de map {d} behalve {n} te verwijderen",
                            не_трогай="verwijder alle bestanden in de map {d}, maar laat {n} staan"),
               перенести=dict(imp="verplaats alle bestanden uit de map {d} naar de map {e} behalve {n}",
                              inf="alle bestanden uit de map {d} behalve {n} naar de map {e} verplaatsen",
                              zu="alle bestanden uit de map {d} behalve {n} naar de map {e} te verplaatsen",
                              не_трогай="verplaats alle bestanden uit de map {d} naar de map {e}, maar laat {n} "
                                        "staan")),
    "pl": dict(удалить=dict(imp="usuń wszystkie pliki z folderu {d} oprócz {n}",
                            inf="usunąć wszystkie pliki z folderu {d} oprócz {n}",
                            не_трогай="usuń wszystkie pliki z folderu {d}, ale nie ruszaj {n}"),
               перенести=dict(imp="przenieś wszystkie pliki z folderu {d} do folderu {e} oprócz {n}",
                              inf="przenieść wszystkie pliki z folderu {d} do folderu {e} oprócz {n}",
                              не_трогай="przenieś wszystkie pliki z folderu {d} do folderu {e}, ale nie ruszaj {n}")),
}

# ДВА ОБЪЕКТА В ОДНОМ ПРИКАЗЕ — «delete the files f and q», «append … to the files f and q»: фраза объекта во
# множественном числе в падеже шаблона акта ({С} — перечень с союзом языка)
for _я, (_вин, _в) in {"en": ("the files {С}", "to the files {С}"), "ru": ("файлы {С}", "в файлы {С}"),
                       "de": ("die Dateien {С}", "die Dateien {С}"), "fr": ("les fichiers {С}", "aux fichiers {С}"),
                       "es": ("los archivos {С}", "a los archivos {С}"), "it": ("i file {С}", "ai file {С}"),
                       "pt": ("os ficheiros {С}", "aos ficheiros {С}"),
                       "nl": ("de bestanden {С}", "onderaan de bestanden {С}"),
                       "pl": ("pliki {С}", "do plików {С}")}.items():
    ОБЪЕКТЫ[_я].update(файлы_вин=_вин, в_файлы=_в)


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
                      вопросом="could you {inf}?", вопросом2="can you {inf}?", вопросом3="would you {inf}?"),
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
                      вопросом="ты можешь {inf}?", вопросом2="ты сможешь {inf}?", вопросом3="а можешь {inf}?"),
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
                      вопросом="kannst du {inf}?", вопросом2="kannst du bitte {inf}?",
                      вопросом3="kannst du mal {inf}?"),
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
                      вопросом="peux-tu {inf} ?", вопросом2="tu peux {inf} ?", вопросом3="est-ce que tu peux {inf} ?"),
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
                      вопросом="¿puedes {inf}?", вопросом2="¿quieres {inf}?", вопросом3="¿puedes por favor {inf}?"),
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
                      вопросом="puoi {inf}?", вопросом2="puoi per favore {inf}?", вопросом3="puoi gentilmente {inf}?"),
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
                      вопросом="podes {inf}?", вопросом2="queres {inf}?", вопросом3="podes por favor {inf}?"),
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
                      вопросом="kun je {inf}?", вопросом2="wil je {inf}?", вопросом3="kan je {inf}?"),
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
                      вопросом="czy możesz {inf}?", вопросом2="czy mógłbyś {inf}?",
                      вопросом3="czy możesz proszę {inf}?"),
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
# МОДИФИКАТОРЫ ПРИКАЗА (27.09, наряд ведущего: контрастные пары «приказ со словом / без слова» на ходах мира) —
# регистры, какие лишь прибавляют слово к повелению. Хранители акта — «сейчас», «просто», «прямо_сейчас»: тот же
# ход мира, что у приказа без слова. Меняющие — «позже», «завтра» (здесь), «не», «притворись» (`ОТМЕНА`): акт сейчас
# не идёт; причина отказа — `МЕНЯЮЩИЕ`.
МОДИФИКАТОРЫ = {
    "en": dict(сейчас="{imp} now.", просто="just {imp}.", прямо_сейчас="{imp} right now.", позже="{imp} later.",
               завтра="{imp} tomorrow."),
    "ru": dict(сейчас="{imp} сейчас.", просто="просто {imp}.", прямо_сейчас="{imp} прямо сейчас.",
               позже="{imp} позже.", завтра="{imp} завтра."),
    "de": dict(сейчас="{imp} jetzt.", просто="{imp} einfach.", прямо_сейчас="{imp} sofort.", позже="{imp} später.",
               завтра="{imp} morgen."),
    "fr": dict(сейчас="{imp} maintenant.", просто="{imp}, tout simplement.", прямо_сейчас="{imp} tout de suite.",
               позже="{imp} plus tard.", завтра="{imp} demain."),
    "es": dict(сейчас="{imp} ahora.", просто="simplemente {imp}.", прямо_сейчас="{imp} ahora mismo.",
               позже="{imp} más tarde.", завтра="{imp} mañana."),
    "it": dict(сейчас="{imp} adesso.", просто="{imp} e basta.", прямо_сейчас="{imp} subito.",
               позже="{imp} più tardi.", завтра="{imp} domani."),
    "pt": dict(сейчас="{imp} agora.", просто="simplesmente {imp}.", прямо_сейчас="{imp} agora mesmo.",
               позже="{imp} mais tarde.", завтра="{imp} amanhã."),
    "nl": dict(сейчас="{imp} nu.", просто="{imp} gewoon.", прямо_сейчас="{imp} meteen.", позже="{imp} later.",
               завтра="{imp} morgen."),
    "pl": dict(сейчас="{imp} teraz.", просто="po prostu {imp}.", прямо_сейчас="{imp} od razu.",
               позже="{imp} później.", завтра="{imp} jutro."),
}
for _я, _м in МОДИФИКАТОРЫ.items():
    РЕЧЬ[_я]["регистры"].update(_м)
ХРАНИТЕЛИ = ("сейчас", "просто", "прямо_сейчас")
# СЛОВО, КАКОЕ АКТ МЕНЯЕТ, — причина отказа словами «{причина} — {хвост отказа}»: организм акта не предлагает, мир
# читает «до» (то же чтение, что у отказа пользователем), итог называет акт и то, что не сдвинулось
МЕНЯЮЩИЕ = {
    "en": dict(позже="the order is for later", завтра="the order is for tomorrow", не="the order says not to",
               притворись="the order asks only to pretend"),
    "ru": dict(позже="приказ на потом", завтра="приказ на завтра", не="приказ это запрещает",
               притворись="приказ просит лишь притвориться"),
    "de": dict(позже="der Auftrag ist für später", завтра="der Auftrag ist für morgen", не="der Auftrag verbietet es",
               притворись="der Auftrag verlangt nur, so zu tun"),
    "fr": dict(позже="l'ordre est pour plus tard", завтра="l'ordre est pour demain", не="l'ordre l'interdit",
               притворись="l'ordre demande seulement de faire semblant"),
    "es": dict(позже="la orden es para más tarde", завтра="la orden es para mañana", не="la orden lo prohíbe",
               притворись="la orden pide solo fingir"),
    "it": dict(позже="l'ordine è per più tardi", завтра="l'ordine è per domani", не="l'ordine lo vieta",
               притворись="l'ordine chiede solo di fingere"),
    "pt": dict(позже="a ordem é para mais tarde", завтра="a ordem é para amanhã", не="a ordem proíbe-o",
               притворись="a ordem pede só para fingir"),
    "nl": dict(позже="de opdracht is voor later", завтра="de opdracht is voor morgen", не="de opdracht verbiedt het",
               притворись="de opdracht vraagt alleen om te doen alsof"),
    "pl": dict(позже="polecenie jest na później", завтра="polecenie jest na jutro", не="polecenie tego zabrania",
               притворись="polecenie każe tylko udawać"),
}
# ПРИКАЗ «НЕ …» И «ПРИТВОРИСЬ» (27.09, наряд ведущего: блок C) — форма приказа меняющего слова. Строка — над формами
# самого приказа: {imp} — повеление, {V} и {R} — его глагол и остаток, {inf} — инфинитив, {past} — отчёт без
# вспомогательного глагола («die Datei X gelöscht», «удалил файл X»), {past2} — он же вторым лицом (польское «-łem» →
# «-łeś»). Словарь — по актам, слотами двери: где язык при отрицании меняет глагол (вид, сослагательное) или падеж
# объекта («nie usuwaj pliku X») и где место отрицания — внутри приказа («verschiebe die Datei X nicht in den Ordner»).
ОТМЕНА = {
    "en": dict(не="don't {imp}", притворись="pretend to {inf}"),
    "ru": dict(не=dict(создать="не создавай {Ф}", удалить="не удаляй {Ф}", перенести="не переноси {Ф} {Д}",
                       переименовать="не переименовывай {Фи} в {g}", замена="не заменяй {W} на {v} {М}",
                       дописать="не дописывай {S} {К}", тесты="не запускай {Т}"),
               притворись="притворись, что {past}"),
    "de": dict(не=dict(создать="erstelle {Ф} nicht", удалить="lösche {Ф} nicht", перенести="verschiebe {Ф} nicht {Д}",
                       переименовать="gib {Фи} nicht den Namen {g}", замена="ersetze {W} {М} nicht durch {v}",
                       дописать="ergänze {К} nicht um {S}", тесты="starte {Т} nicht"),
               притворись="tu so, als hättest du {past}"),
    "fr": dict(не="ne {V} pas {R}", притворись="fais semblant de {inf}"),
    "es": dict(не=dict(создать="no crees {Ф}", удалить="no elimines {Ф}", перенести="no muevas {Ф} {Д}",
                       переименовать="no renombres {Фи} como {g}", замена="no reemplaces {W} por {v} {М}",
                       дописать="no añadas {S} {К}", тесты="no ejecutes {Т}"),
               притворись="finge {inf}"),
    "it": dict(не="non {inf}", притворись="fai finta di {inf}"),
    "pt": dict(не=dict(создать="não cries {Ф}", удалить="não elimines {Ф}", перенести="não movas {Ф} {Д}",
                       переименовать="não renomeies {Фи} para {g}", замена="não substituas {W} por {v} {М}",
                       дописать="não acrescentes {S} {К}", тесты="não executes {Т}"),
               притворись="finge {inf}"),
    "nl": dict(не=dict(создать="creëer {Ф} niet", удалить="verwijder {Ф} niet", перенести="verplaats {Ф} niet {Д}",
                       переименовать="hernoem {Фи} niet naar {g}", замена="vervang {W} {М} niet door {v}",
                       дописать="zet {S} niet {К}", тесты="start {Т} niet"),
               притворись="doe alsof je {past} hebt"),
    "pl": dict(не=dict(создать="nie twórz {Фр}", удалить="nie usuwaj {Фр}", перенести="nie przenoś {Фр} {Д}",
                       переименовать="nie zmieniaj nazwy {Фи} na {g}", замена="nie zamieniaj {Wнет} na {v} {М}",
                       дописать="nie dopisuj linii {s} {К}", тесты="nie uruchamiaj testów {Я}"),
               притворись="udawaj, że {past2}"),
}


def отмена(язык, вид, акт, imp, inf, отчёт_, **п):
    """Приказ меняющего слова `вид` («не», «притворись») для акта `акт`: из форм самого приказа (повеление, инфинитив,
    отчёт) или шаблоном акта со слотами двери (`п` — части приказа)."""
    шаблон = ОТМЕНА[язык][вид]
    if isinstance(шаблон, dict):
        return шаблон[акт].format(**слоты(язык, **п))
    вспом = РЕЧЬ[язык]["отчёт"].split("{past}")[0]
    past = отчёт_[len(вспом):] if отчёт_.startswith(вспом) else отчёт_
    глагол, _, остаток = past.partition(" ")
    V, _, R = imp.partition(" ")
    return шаблон.format(imp=imp, inf=inf, past=past, V=V, R=R,
                         past2=(глагол[:-3] + "łeś" if глагол.endswith("łem") else глагол) + " " + остаток)
# ВОПРОС О ПРОШЛОМ АКТЕ (27.09, наряд ведущего: «did you delete F?» — пара к «delete F») — ответ читает мир (есть ли
# файл), акт удаления не идёт. Глагол — у двери хода (`actturn.ГЛАГОЛЫ`: {inf} и {past}); где его формы второго лица
# дверь не несёт, форма стоит словом шаблона («eliminaste», «usunąłeś», «удалён»). Где пакет языка зачина прошедшего
# времени не объявил («hast du», «as-tu», «¿has», «hai»), вопрос спрашивает о состоянии файла зачином, какой пакет
# объявил: «ist … gelöscht?», «est-ce que tu as …», «¿está eliminado …?», «è stato eliminato …?».
ПРОШЛОЕ = {
    "en": dict(вопрос="did you {inf} {Ф}?", не_сделан="it is not {past}"),
    "ru": dict(вопрос="{past} ли ты {Ф}?", не_сделан="он не удалён"),
    "de": dict(вопрос="ist {Ф} {past}?", не_сделан="sie ist nicht {past}"),
    "fr": dict(вопрос="est-ce que tu as {past} {Ф} ?", не_сделан="il n'est pas {past}"),
    "es": dict(вопрос="¿está {past} {Ф}?", не_сделан="no está {past}"),
    "it": dict(вопрос="è stato {past} {Ф}?", не_сделан="non è stato {past}"),
    "pt": dict(вопрос="eliminaste {Ф}?", не_сделан="não foi eliminado"),
    "nl": dict(вопрос="heb je {Ф} {past}?", не_сделан="het is niet {past}"),
    "pl": dict(вопрос="czy usunąłeś {Ф}?", не_сделан="nie jest usunięty"),
}
# СОКРАЩЕНИЕ ГОЛОСА (27.09, наряд ведущего (g)) — пары (полное, сокращённое), где голос в живой просьбе сливает два
# слова апострофом: английское «what's», «where's», «it's» («what's the first line of the file F?», «… if it's
# there»). Отрицание «don't …» — не сокращение формы, а меняющее слово (дверь `ОТМЕНА`). Прочие голоса ряда не имеют:
# русский и польский апострофа не знают; французская и итальянская элизия («qu'est-ce», «c'è», «l'ultima») — норма
# письма без полной пары, «qual è» пишется без апострофа; испанское и португальское слияние («del», «do», «dá-me») —
# тоже норма; немецкое «gibt's» сливает «es», какого в формах дома нет; нидерландское «wat's» и итальянское «cos'è» —
# разговорные, и пакеты языков зачином их не объявили
СОКРАЩЕНИЯ = {"en": (("what is", "what's"), ("where is", "where's"), ("it is", "it's"))}


def сократить(язык, текст):
    """Текст сокращением голоса: всякое полное двери вне кавычек — его сокращение («what is the value …» → «what's the
    value …»); голос без ряда — тот же текст."""
    о, з = КАВЫЧКИ[язык]
    куски = re.split("(" + re.escape(о) + ".+?" + re.escape(з) + ")", текст)
    for полное, сокращённое in СОКРАЩЕНИЯ.get(язык, ()):
        куски = [кусок if i % 2 else re.sub(r"\b" + re.escape(полное) + r"\b", сокращённое, кусок)
                 for i, кусок in enumerate(куски)]
    return "".join(куски)


# ЛИТЕРАЛ В ОБЁРТКЕ ПРОГРАММИСТА (27.09, наряд ведущего (g)) — голый литерал в бэктиках вместо кавычек голоса
# («replace `fresh bread` with `rye bread` in shopping.txt»): обёртка одна на всех голосах — письмо программиста, а не
# языка. Речь организма — каноническая (кавычки голоса), мир печатает литерал своими ASCII-кавычками. Литерал в
# обёртке — та же дыра, что текст в кавычках голоса: одно правило условий рынка и источника (`в_кавычках`). Ядру ствола
# бэктик — не обёртка: `markets::buy_wraps` покупает пару знаков лишь там, где поздняя реплика страницы повторяет
# отрезок с его знаками, а организм и мир говорят кавычками
ЛИТЕРАЛ = ("`", "`")


def в_литерале(язык, текст):
    """Текст, где литерал в кавычках голоса обёрнут бэктиками: «replace "x" with "y"» → «replace `x` with `y`»."""
    о, з = КАВЫЧКИ[язык]
    return re.sub(re.escape(о) + "(.+?)" + re.escape(з), lambda м: ЛИТЕРАЛ[0] + м.group(1) + ЛИТЕРАЛ[1], текст)


def в_кавычках(язык, текст):
    """Текст, где литерал в обёртке программиста прочтён кавычками голоса — та же дыра, как бы её ни обернул приказ."""
    return re.sub(re.escape(ЛИТЕРАЛ[0]) + "(.+?)" + re.escape(ЛИТЕРАЛ[1]), lambda м: кавычки(язык, м.group(1)), текст)


# НЕОПРЕДЕЛЁННЫЙ АРТИКЛЬ (27.09, наряд ведущего (h1)): «append a line "x" to the file F», «create a file plan.md» —
# фраза строки и файла с неопределённым артиклем, вариантом в конце ряда той же двери `ОБЪЕКТЫ`. Прежние формы стоят на
# своих номерах, и циклы по вариантам до этого номера не доходят: вопросы берут фразу файла по номеру фразы папки (до
# 2) и «назв» (2), приказы — голую строку (1). Русский и польский артикля не знают — ряда у них нет
НЕОПР = {"en": dict(строку="a line {s}", файл_вин="a file {f}"),
         "de": dict(строку="eine Zeile {s}", файл_вин="eine Datei {f}"),
         "fr": dict(строку="une ligne {s}", файл_вин="un fichier {f}"),
         "es": dict(строку="una línea {s}", файл_вин="un archivo {f}"),
         "it": dict(строку="una riga {s}", файл_вин="un file {f}"),
         "pt": dict(строку="uma linha {s}", файл_вин="um ficheiro {f}"),
         "nl": dict(строку="een regel {s}", файл_вин="een bestand {f}")}
for _я, _арт in НЕОПР.items():
    for _фраза, _шаблон in _арт.items():
        ОБЪЕКТЫ[_я][_фраза] = ОБЪЕКТЫ[_я][_фраза] + (_шаблон,)


def неопр(язык, фраза):
    """Номер варианта с неопределённым артиклем в ряду фразы двери `ОБЪЕКТЫ`; None — голос артикля не знает."""
    return ОБЪЕКТЫ[язык][фраза].index(НЕОПР[язык][фраза]) if язык in НЕОПР else None


# КОНЕЦ ФАЙЛА ГОЛЫМ ИМЕНЕМ (27.09, наряд ведущего (h1)): «append "x" to the end of F» — глагол акта двери, голый
# литерал и голый файл после «to the end of» (`у_конца_голый`; немецкое «ergänze „x“ am Ende von F» — «ergänzen» с
# винительным, как живая речь его говорит); «add the line "x" to the end of F» — синоним «add» на той же фразе
# (`добавь_голый`). У дома — «to the end of the file F» (`В_КОНЕЦ`) и «at the end of the file F»
for _я, (_у_конца, _добавь) in {
        "en": ("append {S} to the end of {f}", "add {S} to the end of {f}"),
        "ru": ("допиши {S} в конец {f}", "добавь {S} в конец {f}"),
        "de": ("ergänze {S} am Ende von {f}", "füge {S} am Ende von {f} hinzu"),
        "fr": ("ajoute {S} à la fin de {f}", "rajoute {S} à la fin de {f}"),
        "es": ("añade {S} al final de {f}", "agrega {S} al final de {f}"),
        "it": ("aggiungi {S} alla fine di {f}", "accoda {S} alla fine di {f}"),
        "pt": ("acrescenta {S} ao fim de {f}", "adiciona {S} ao fim de {f}"),
        "nl": ("zet {S} aan het eind van {f}", "plaats {S} aan het eind van {f}"),
        "pl": ("dopisz {S} na końcu {f}", "dodaj {S} na końcu {f}")}.items():
    КОНЕЦ[_я].update(у_конца_голый=_у_конца, добавь_голый=_добавь)
# КОНСТРУКЦИИ ПРОСЬБЫ (28.09, наряд ведущего по классам отложенного ключа H2: «иная конструкция» — косвенная просьба,
# желание) — нужда первым лицом и желание: «i need to {inf}», «i would like to {inf}»; инфинитив акта двери, предложение
# организма — каноническое. Без апострофа («I'd» — ухо ядра рвёт слово на апострофе, у fr «j'ai besoin» тоже) и без
# придаточного со спряжением («хочу, чтобы ты удалил …»): регистр держит лишь {imp} и {inf}
for _я, _р in {"en": dict(нужда="i need to {inf}.", желание="i would like to {inf}."),
               "ru": dict(нужда="мне нужно {inf}.", желание="я хочу {inf}."),
               "de": dict(нужда="ich muss {inf}.", желание="ich möchte {inf}."),
               "fr": dict(нужда="je dois {inf}.", желание="je voudrais {inf}."),
               "es": dict(нужда="necesito {inf}.", желание="quiero {inf}."),
               "it": dict(нужда="ho bisogno di {inf}.", желание="vorrei {inf}."),
               "pt": dict(нужда="preciso de {inf}.", желание="queria {inf}."),
               "nl": dict(нужда="ik moet {inf}.", желание="ik wil graag {inf}."),
               "pl": dict(нужда="muszę {inf}.", желание="chcę {inf}.")}.items():
    РЕЧЬ[_я]["регистры"].update(_р)
# МОДАЛЬНОЕ «НАДО» (28.09, наряд ведущего (б), ход «иная конструкция»): безличная нужда — «надо удалить файл F» и пары
# голосов, отличные от «косвенного» регистра («нужно», «we need to», «man sollte», «il faut», «hay que», «bisogna», «é
# preciso», «we moeten», «trzeba»)
for _я, _р in {"en": "we have to {inf}.", "ru": "надо {inf}.", "de": "man muss {inf}.", "fr": "on doit {inf}.",
               "es": "hace falta {inf}.", "it": "occorre {inf}.", "pt": "é necessário {inf}.", "nl": "men moet {inf}.",
               "pl": "należy {inf}."}.items():
    РЕЧЬ[_я]["регистры"]["надо"] = _р
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
