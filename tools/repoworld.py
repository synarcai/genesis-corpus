#!/usr/bin/env python3
"""МИР РЕПОЗИТОРИЯ дома `toolrepo` — объявление, общее дому, суду и прибору съёмки прогонов (25.09).

Репозиторий: восемь текстовых файлов с содержимым на языке страницы и файлы проекта (код Python и двух крейтов Rust,
настройки, тесты) — одни на всех языках. Мир-процесс держит четыре прогона (`ПРОГОНЫ`; четвёртый — пакет без тестов),
проект — свои состояния после правки одним актом (`ПРАВКИ_ПРОЕКТА`, `СОСТОЯНИЯ_ИСХОДОВ`); настоящий вывод всякого прогона
на всяком состоянии снят прибором
`toolrepo_capture.py` в семя `tools/seeds/toolrepo_runs.json`. Имена мира нарочно не совпадают с песочницей ключа
агента.

Здесь только объявление и мир папки над ним (`папка(язык)` — дверь `folderworld`); речь и страницы — у дома.
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actturn as A  # noqa: E402 — языки свода
import folderworld as W  # noqa: E402 — мир папки: семантика ядра

ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# МИР: репозиторий — восемь текстовых файлов с содержимым на языке страницы и десять файлов проекта
# ======================================================================================================
ТЕКСТЫ = ("shopping.txt", "journal.md", "home/chores.md", "home/repairs.txt", "trips/sea.md", "trips/city.md",
          "kitchen/soup.md", "kitchen/cake.md")
# ПРОЕКТ: код, настройки и тесты — одни на всех языках (язык страницы — не язык кода)
ПРОЕКТ = {
    "server.ini": ("port = 8080", "delay = 45", "workers = 4"),
    "web/main.py": ("from helpers import greet", "print(greet())"),
    "web/helpers.py": ("def greet(name='world'):", "    return 'hello ' + name.lower()"),
    "web/site.ini": ("retries = 5", "limit = 500", "level = 2"),
    "tests/test_main.py": ("import unittest", "from web.helpers import greet", "class GreetTests(unittest.TestCase):",
                           "    def test_default(self):", "        self.assertEqual(greet(), 'hello world')",
                           "    def test_name(self):", "        self.assertEqual(greet('bo'), 'hello bo')",
                           "    def test_empty(self):", "        self.assertEqual(greet(''), 'hello ')",
                           "    def test_lower(self):", "        self.assertEqual(greet('BO'), 'hello bo')"),
    "tests/test_helpers.py": ("import unittest", "from web.helpers import greet", "class HelperTests(unittest.TestCase):",
                              "    def test_type(self):", "        self.assertIsInstance(greet(), str)",
                              "    def test_start(self):", "        self.assertTrue(greet().startswith('hello'))",
                              "    def test_length(self):", "        self.assertEqual(len(greet()), 11)",
                              "    def test_space(self):", "        self.assertIn(' ', greet())"),
    "tally/Cargo.toml": ("[package]", "name = 'tally'", "edition = '2021'"),
    "tally/src/lib.rs": ("pub fn add(a: i32, b: i32) -> i32 {", "    a + b", "}", "pub fn shout(s: &str) -> String {",
                         "    s.to_uppercase()", "}"),
    "tally/tests/checks.rs": ("use tally::add;", "#[test]", "fn adds() { assert_eq!(add(2, 3), 5); }", "#[test]",
                              "fn zero() { assert_eq!(add(0, 0), 0); }", "#[test]",
                              "fn negative() { assert_eq!(add(-1, 1), 0); }", "#[test]",
                              "fn twice() { assert_eq!(add(4, 4), 8); }", "#[test]",
                              "fn doubles() { assert_eq!(add(2, 2), 5); }"),
    # ВТОРОЙ КРЕЙТ (27.09, слово ведущего: доктесты — отдельным крейтом, прежние страницы байт в байт) — полный прогон
    # крейта печатает несколько строк «test result»: тесты модуля lib, интеграционные, доктест
    "gauge/Cargo.toml": ("[package]", "name = 'gauge'", "edition = '2021'"),
    "gauge/src/lib.rs": ("/// ```", "/// assert_eq!(gauge::half(8), 4);", "/// ```", "pub fn half(n: u32) -> u32 {",
                         "    n / 2", "}", "#[cfg(test)]", "mod unit {", "    #[test]",
                         "    fn halves() { assert_eq!(super::half(6), 3); }", "    #[test]",
                         "    fn nought() { assert_eq!(super::half(0), 0); }", "}"),
    "gauge/tests/checks.rs": ("use gauge::half;", "#[test]", "fn even() { assert_eq!(half(10), 5); }", "#[test]",
                              "fn odd() { assert_eq!(half(7), 3); }", "#[test]",
                              "fn one() { assert_eq!(half(1), 0); }"),
}
# ПРОГОНЫ МИРА-ПРОЦЕССА: имя прогона → команда, какую мир держит сам (речь выбирает акт по имени, команда — данные
# мира). Вывод прогона — НАСТОЯЩИЙ вывод бегуна: снят один раз прибором `toolrepo_capture.py` в семя прогонов.
ПРОГОНЫ = {"python": "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_main tests.test_helpers",
           "rust": "CARGO_TARGET_DIR=.ozar/target cargo test -q --manifest-path tally/Cargo.toml --test checks",
           "gauge": "CARGO_TARGET_DIR=.ozar/target cargo test -q --manifest-path gauge/Cargo.toml",
           # ПРОГОН БЕЗ ТЕСТОВ (28.09, наряд ведущего «исходы прогона»): пакет web ищет тесты в своей папке — их там
           # нет, и unittest кончает прогон «NO TESTS RAN» с кодом 5; прогон — данные мира, файлов мира он не прибавляет
           "web": "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web"}
# КОД ПРОГОНА — файлы проекта, какие прогон читает (по началу пути): отпечаток состояния — у каждого прогона свой
КОД_ПРОГОНА = {"python": ("web/", "tests/"), "rust": ("tally/",), "gauge": ("gauge/",), "web": ("web/",)}
# БЕГУН ПРОГОНА — чей отчёт прогон печатает: число тестов в коде и чтение отчёта — по бегуну
БЕГУНЫ = {"python": "unittest", "rust": "cargo", "gauge": "cargo", "web": "unittest"}
# язык проекта в речи дома → имя прогона мира; крейт и пакет, названные в речи своим именем, → имя прогона
ЯЗЫКИ_ПРОЕКТА = {"Python": "python", "Rust": "rust"}
КРЕЙТЫ = {"Gauge": "gauge"}
ПАКЕТЫ = {"Web": "web"}
ИМЕНА_ПРОГОНОВ = {**ЯЗЫКИ_ПРОЕКТА, **КРЕЙТЫ, **ПАКЕТЫ}
# СОСТОЯНИЯ ПРОЕКТА (27.09, наряд ведущего: у прогона оба исхода, иное число тестов, иные millis и длина отчёта) —
# правка кода или теста ОДНИМ актом мира над объявленным проектом: (акт, путь, доводы) — замена текста или строка в
# конце файла. Прогон после правки печатает отчёт бегуна, снятый прибором с проекта в этом состоянии; снятое ищется
# по отпечатку файлов проекта, какие мир держит после правки (`снятое`).
ПРАВКИ_ПРОЕКТА = (
    ("replace", "tally/tests/checks.rs", ("add(2, 2), 5", "add(2, 2), 4")),          # rust чинится: все 5 проходят
    ("replace", "tally/tests/checks.rs", ("add(0, 0), 0", "add(0, 0), 1")),          # rust: 3 проходят, 2 падают
    ("line", "tally/tests/checks.rs", ("#[test] fn ones() { assert_eq!(add(1, 1), 2); }",)),  # rust: тестов 6
    ("replace", "tests/test_helpers.py", ("test_space", "check_space")),             # python: тестов 7
    ("replace", "tally/src/lib.rs", ("i32", "i64")),                                 # rust: исход тот же
    ("replace", "tests/test_main.py", ("test_empty", "check_empty")),                # python: тестов 7
    ("replace", "gauge/src/lib.rs", ("u32", "u64")),                                 # gauge: исход тот же
    ("replace", "gauge/tests/checks.rs", ("half(7), 3", "half(7), 4")),              # gauge: падает, доктест не идёт
    ("line", "gauge/tests/checks.rs", ("#[test] fn four() { assert_eq!(half(4), 2); }",)),    # gauge: тестов 7
    ("line", "tally/tests/checks.rs", ("#[test] fn wrong() { assert_eq!(add(1, 1), 3); }",)),  # rust: 4 и 2 падают
    ("line", "gauge/tests/checks.rs", ("#[test] fn nine() { assert_eq!(half(9), 5); }",)),    # gauge: падает
    ("replace", "tests/test_main.py", ("test_lower", "check_lower")),                # python: тестов 7
    ("replace", "tests/test_helpers.py", ("test_type", "check_type")),               # python: тестов 7
    # ПАДЕНИЕ PYTHON (слово ведущего 27.09: строка трассы — кавычки как есть, путь от дома мира, М-2057 + М-2069;
    # в свод — с поездом T112, сел 1fbf0f99a): отчёт unittest о падении снят миром процесса с домом (`ozar_process <мир>
    # <дом>`)
    ("replace", "web/helpers.py", ("lower", "upper")),                               # python: 3 из 8 падают
    ("replace", "tests/test_main.py", ("hello world", "hello there")),               # python: 1 из 8 падает
)
# ИСХОДЫ ПРОГОНА (28.09, наряд ведущего omega-90): состояния, на каких прогон кончается исходом, какого дом прежде не
# показывал, — ошибка теста (unittest «errors»), провал вместе с ошибкой, провал девятого теста. Правка одна, как у
# `ПРАВКИ_ПРОЕКТА`, но страницы её не называют: это мир, в каком прогон идёт одним приказом (род дома «исходы»)
СОСТОЯНИЯ_ИСХОДОВ = (
    ("replace", "tests/test_main.py", ("greet('bo')", "greet(5)")),                  # python: 1 из 8 — ошибка
    ("replace", "web/helpers.py", ("name.lower()", "name.lower()[0]")),              # python: 4 падают, 1 — ошибка
    ("line", "tests/test_main.py", ("    def test_upper(self): self.assertEqual(greet('Al'), 'hello Al')",)),
)                                                                                    # python: тестов 9, 1 падает
НАСТРОЙКИ = tuple(ф for ф in ПРОЕКТ if ф.endswith(".ini"))
ПУТИ = ТЕКСТЫ + tuple(ПРОЕКТ)
ЗАПУСКИ_ДО = (1, 2, 5)          # запусков мира до прогона: после — 2, 3, 6; ни одно не равно числу отчёта

# АКТЫ НАД МИРОМ — пути и имена; всякое имя вне мира объявлено как новое или как отсутствующее
СОЗДАТЬ_ПУТИ = ("plan.md", "memo.txt", "home/garden.md", "trips/lake.md", "kitchen/salad.md", "web/config.py",
                "tests/test_net.py", "tally/src/net.rs")
СОЗДАТЬ_В_ПАПКЕ = (("garden.md", "home"), ("lake.md", "trips"), ("salad.md", "kitchen"), ("config.py", "web"),
                   ("test_net.py", "tests"), ("net.rs", "tally/src"))
УДАЛИТЬ_ИЗ_ПАПКИ = (("chores.md", "home"), ("city.md", "trips"), ("cake.md", "kitchen"), ("helpers.py", "web"),
                    ("test_helpers.py", "tests"), ("checks.rs", "tally/tests"))
# ПЕРЕНОС — лишь в папки, какие есть: счёт «до» мир читает (папки, которой нет, счёт — отказ по имени)
ПЕРЕНОСЫ = (("shopping.txt", "home"), ("journal.md", "trips"), ("home/chores.md", "kitchen"),
            ("home/repairs.txt", "trips"), ("trips/sea.md", "home"), ("trips/city.md", "kitchen"),
            ("kitchen/soup.md", "home"), ("kitchen/cake.md", "trips"))
ИМЕНА = (("shopping.txt", "groceries.txt"), ("journal.md", "diary.md"), ("home/chores.md", "tasks.md"),
         ("home/repairs.txt", "fixes.txt"), ("trips/sea.md", "beach.md"), ("trips/city.md", "town.md"),
         ("kitchen/soup.md", "broth.md"), ("kitchen/cake.md", "pie.md"))
ИМЕНА_ЗАНЯТЫ = (("home/chores.md", "repairs.txt"), ("trips/sea.md", "city.md"), ("kitchen/cake.md", "soup.md"))
НЕТ_ФАЙЛОВ = ("budget.md", "recipes.txt")
ИМЕНА_НЕТ = (("budget.md", "costs.md"), ("recipes.txt", "menu.txt"))
КЛЮЧИ = (("server.ini", "port"), ("web/site.ini", "retries"), ("server.ini", "delay"), ("web/site.ini", "limit"),
         ("server.ini", "workers"), ("web/site.ini", "level"))
ПАПКИ_СЧЁТА = ("home", "trips", "kitchen", "web", "tests", "tally/src", "tally/tests")

# (строки файла; текст для замены и чем заменить; слово для замены и чем заменить; строка для дописывания)
СОДЕРЖИМОЕ = {
    "en": {
        "shopping.txt": (("get eggs", "get fresh bread", "pay the phone bill"), ("fresh bread", "rye bread"),
                         ("eggs", "rice"), "get green apples"),
        "journal.md": (("a long walk by the river", "read a good book", "slept well", "met an old friend"),
                       ("a good book", "the morning paper"), ("walk", "swim"), "wrote a letter home"),
        "home/chores.md": (("water the plants", "take out the trash", "clean the windows", "walk the dog", "sort the socks pair by pair"),
                           ("the trash", "the recycling"), ("plants", "flowers"), "sweep the floor"),
        "home/repairs.txt": (("fix the kitchen tap", "paint the front door", "fix the lamp", "check the tap again and again"),
                             ("the front door", "the garden fence"), ("lamp", "clock"), "oil the gate"),
        "trips/sea.md": (("book the hotel", "pack the swimsuit", "get sun cream", "swim side by side"), ("sun cream", "a beach towel"),
                         ("hotel", "cabin"), "check the weather"),
        "trips/city.md": (("visit the old museum", "book a table for dinner", "walk along the river",
                           "take the night train"), ("the night train", "the early bus"), ("museum", "castle"),
                          "get a city map"),
        "kitchen/soup.md": (("boil the water", "cut the carrots", "stir in salt and pepper", "stir and stir again"),
                            ("salt and pepper", "fresh herbs"), ("carrots", "potatoes"), "serve it hot"),
        "kitchen/cake.md": (("mix the flour and the butter", "heat the oven", "let the cake cool"),
                            ("heat the oven", "grease the pan"), ("flour", "sugar"), "decorate the cake")},
    "ru": {
        "shopping.txt": (("купить молоко", "купить свежий хлеб", "оплатить счёт за телефон"),
                         ("свежий хлеб", "ржаной хлеб"), ("молоко", "сок"), "купить зелёные яблоки"),
        "journal.md": (("долгая прогулка у реки", "читал хорошую книгу", "хорошо выспался", "встретил старого друга"),
                       ("хорошую книгу", "утреннюю газету"), ("прогулка", "поездка"), "написал письмо домой"),
        "home/chores.md": (("полить цветы", "вынести мусор", "помыть окна", "купить стиральный порошок", "всё помыть и всё убрать"), ("вынести мусор", "сдать бутылки"),
                           ("цветы", "кактусы"), "подмести пол"),
        "home/repairs.txt": (("починить кран на кухне", "покрасить входную дверь", "починить лампу", "проверить кран снова и снова"),
                             ("входную дверь", "садовый забор"), ("лампу", "полку"), "смазать калитку"),
        "trips/sea.md": (("забронировать гостиницу", "уложить купальник", "купить крем от солнца", "плыть бок о бок", "проехать вдоль реки к морю"),
                         ("крем от солнца", "пляжное полотенце"), ("гостиницу", "домик"), "узнать погоду"),
        "trips/city.md": (("сходить в старый музей", "заказать столик на ужин", "погулять вдоль реки",
                           "сесть на ночной поезд"), ("ночной поезд", "утренний автобус"), ("музей", "замок"),
                          "купить карту города"),
        "kitchen/soup.md": (("вскипятить воду", "нарезать морковь", "добавить соль и перец", "пробовать и снова пробовать"),
                            ("соль и перец", "свежую зелень"), ("морковь", "картошку"), "подать горячим"),
        "kitchen/cake.md": (("смешать муку и молоко", "разогреть духовку", "дать пирогу остыть"),
                            ("разогреть духовку", "смазать форму"), ("муку", "сахар"), "украсить пирог")},
    "de": {
        "shopping.txt": (("Milch kaufen", "frisches Brot kaufen", "die Handyrechnung bezahlen"),
                         ("frisches Brot", "dunkles Brot"), ("Milch", "Saft"), "grüne Äpfel kaufen"),
        "journal.md": (("ein langer Spaziergang am Fluss", "ein gutes Buch gelesen", "gut geschlafen",
                        "einen alten Freund getroffen"), ("ein gutes Buch", "die Morgenzeitung"),
                       ("Spaziergang", "Ausflug"), "einen Brief nach Hause geschrieben"),
        "home/chores.md": (("die Pflanzen gießen", "den Müll rausbringen", "die Fenster putzen", "Waschpulver kaufen", "Stück für Stück aufräumen"),
                           ("den Müll", "das Altpapier"), ("Pflanzen", "Blumen"), "den Boden fegen"),
        "home/repairs.txt": (("den Wasserhahn in der Küche reparieren", "die Haustür streichen", "die Lampe reparieren", "den Hahn immer und immer wieder prüfen"),
                             ("die Haustür", "den Gartenzaun"), ("Lampe", "Uhr"), "das Tor ölen"),
        "trips/sea.md": (("das Hotel buchen", "den Badeanzug einpacken", "Sonnencreme kaufen", "Seite an Seite schwimmen", "am Fluss zum Meer fahren"),
                         ("Sonnencreme kaufen", "ein Strandtuch einpacken"), ("Hotel", "Zimmer"), "das Wetter prüfen"),
        "trips/city.md": (("das alte Museum besuchen", "einen Tisch zum Abendessen reservieren",
                           "am Fluss entlang spazieren", "den Nachtzug nehmen"), ("den Nachtzug", "den Frühbus"),
                          ("Museum", "Schloss"), "einen Stadtplan kaufen"),
        "kitchen/soup.md": (("das Wasser kochen", "die Karotten schneiden", "Salz und Pfeffer dazugeben", "probieren und wieder probieren"),
                            ("Salz und Pfeffer", "frische Kräuter"), ("Karotten", "Kartoffeln"), "heiß servieren"),
        "kitchen/cake.md": (("Mehl und Milch verrühren", "den Ofen vorheizen", "den Kuchen abkühlen lassen"),
                            ("den Ofen vorheizen", "die Form einfetten"), ("Mehl", "Zucker"), "den Kuchen verzieren")},
    "fr": {
        "shopping.txt": (("acheter du lait", "acheter du pain frais", "payer la facture du téléphone"),
                         ("du pain frais", "du pain de seigle"), ("lait", "jus"), "acheter des pommes vertes"),
        "journal.md": (("une longue promenade au bord de la rivière", "lu un bon livre", "bien dormi",
                        "revu un vieil ami"), ("un bon livre", "le journal du matin"), ("promenade", "balade"),
                       "écrit une lettre aux parents"),
        "home/chores.md": (("arroser les plantes", "sortir la poubelle", "laver les fenêtres", "acheter de la lessive", "ranger pièce par pièce"),
                           ("la poubelle", "le recyclage"), ("plantes", "fleurs"), "balayer le sol"),
        "home/repairs.txt": (("réparer le robinet de la cuisine", "peindre la porte bleue", "réparer la lampe", "vérifier le robinet encore et encore"),
                             ("la porte bleue", "la clôture du jardin"), ("lampe", "pendule"), "huiler le portail"),
        "trips/sea.md": (("réserver la chambre", "emporter le maillot de bain", "acheter de la crème solaire", "nager côte à côte", "suivre la rivière vers la mer"),
                         ("de la crème solaire", "une serviette de plage"), ("chambre", "cabane"),
                         "regarder la météo"),
        "trips/city.md": (("visiter le vieux musée", "réserver une table pour le dîner", "marcher le long de la rivière",
                           "prendre le train de nuit"), ("le train de nuit", "le bus du matin"),
                          ("musée", "château"), "acheter un plan de la ville"),
        "kitchen/soup.md": (("chauffer le bouillon", "couper les carottes", "ajouter le sel et le poivre", "goûter et goûter encore"),
                            ("le sel et le poivre", "des herbes fraîches"), ("carottes", "poireaux"),
                            "servir bien chaud"),
        "kitchen/cake.md": (("mélanger la farine et le lait", "préchauffer le four", "laisser refroidir le gâteau"),
                            ("préchauffer le four", "beurrer le moule"), ("farine", "sucre"), "décorer le gâteau")},
    "es": {
        "shopping.txt": (("comprar leche", "comprar pan fresco", "pagar la factura del teléfono"),
                         ("pan fresco", "pan de centeno"), ("leche", "zumo"), "comprar manzanas verdes"),
        "journal.md": (("un largo paseo junto al río", "leí un buen libro", "dormí bien", "vi a un viejo amigo"),
                       ("un buen libro", "el periódico de la mañana"), ("paseo", "viaje"),
                       "escribí una carta a casa"),
        "home/chores.md": (("regar las plantas", "sacar la basura", "limpiar las ventanas", "comprar detergente", "ordenar poco a poco"),
                           ("la basura", "el reciclaje"), ("plantas", "flores"), "barrer el suelo"),
        "home/repairs.txt": (("arreglar el grifo de la cocina", "pintar la puerta de entrada", "arreglar la lámpara", "revisar el tejado paso a paso"),
                             ("la puerta de entrada", "la valla del jardín"), ("lámpara", "estantería"),
                             "engrasar la verja"),
        "trips/sea.md": (("reservar el hotel", "meter el bañador", "comprar crema solar", "nadar lado a lado", "bajar por el río hasta el mar"),
                         ("crema solar", "una toalla de playa"), ("hotel", "apartamento"), "mirar el tiempo"),
        "trips/city.md": (("visitar el viejo museo", "reservar una mesa para cenar", "caminar junto al río",
                           "tomar el tren nocturno"), ("el tren nocturno", "el autobús de la mañana"),
                          ("museo", "castillo"), "comprar un plano de la ciudad"),
        "kitchen/soup.md": (("hervir el agua", "cortar las zanahorias", "añadir sal y pimienta", "remover y remover otra vez"),
                            ("sal y pimienta", "hierbas frescas"), ("zanahorias", "patatas"), "servir bien caliente"),
        "kitchen/cake.md": (("mezclar la harina y la leche", "calentar el horno", "dejar enfriar el pastel"),
                            ("calentar el horno", "engrasar el molde"), ("harina", "azúcar"), "decorar el pastel")},
    "it": {
        "shopping.txt": (("comprare il latte", "comprare il pane fresco", "pagare la bolletta del telefono"),
                         ("il pane fresco", "il pane di segale"), ("latte", "succo"), "comprare le mele verdi"),
        "journal.md": (("una lunga passeggiata lungo il fiume", "letto un buon libro", "dormito bene",
                        "rivisto un vecchio amico"), ("un buon libro", "il giornale del mattino"),
                       ("passeggiata", "gita"), "scritto una lettera a casa"),
        "home/chores.md": (("annaffiare le piante", "portare fuori la spazzatura", "lavare le finestre", "comprare il detersivo", "sistemare poco a poco"),
                           ("la spazzatura", "la carta"), ("piante", "rose"), "spazzare il pavimento"),
        "home/repairs.txt": (("riparare il rubinetto della cucina", "dipingere la porta di casa", "riparare la lampada", "controllare il rubinetto passo dopo passo"),
                             ("la porta di casa", "il recinto del giardino"), ("lampada", "mensola"),
                             "oliare il cancello"),
        "trips/sea.md": (("prenotare la stanza", "mettere in valigia il costume", "comprare la crema solare", "nuotare fianco a fianco", "scendere lungo il fiume fino al mare"),
                         ("la crema solare", "un telo da spiaggia"), ("stanza", "cabina"), "guardare il meteo"),
        "trips/city.md": (("visitare il vecchio museo", "prenotare un tavolo per cena", "camminare lungo il fiume",
                           "prendere il treno di notte"), ("il treno di notte", "il pullman del mattino"),
                          ("museo", "castello"), "comprare una mappa della città"),
        "kitchen/soup.md": (("scaldare il brodo", "tagliare le carote", "aggiungere sale e pepe", "mescolare e mescolare ancora"),
                            ("sale e pepe", "erbe fresche"), ("carote", "patate"), "servire ben caldo"),
        "kitchen/cake.md": (("mescolare la farina e il latte", "accendere il forno", "lasciar raffreddare la torta"),
                            ("accendere il forno", "imburrare lo stampo"), ("farina", "zucchero"), "decorare la torta")},
    "pt": {
        "shopping.txt": (("comprar leite", "comprar pão fresco", "pagar a conta do telefone"),
                         ("pão fresco", "pão de centeio"), ("leite", "sumo"), "comprar maçãs verdes"),
        "journal.md": (("um longo passeio junto ao rio", "li um bom livro", "dormi bem", "encontrei um velho amigo"),
                       ("um bom livro", "o jornal da manhã"), ("passeio", "percurso"), "escrevi uma carta para casa"),
        "home/chores.md": (("regar as plantas", "levar o lixo", "lavar as janelas", "comprar detergente", "arrumar pouco a pouco"), ("o lixo", "a reciclagem"),
                           ("plantas", "flores"), "varrer o chão"),
        "home/repairs.txt": (("arranjar a torneira da cozinha", "pintar a porta da entrada", "arranjar o candeeiro", "arranjar tudo passo a passo"),
                             ("a porta da entrada", "a vedação do jardim"), ("candeeiro", "relógio"),
                             "olear o portão"),
        "trips/sea.md": (("reservar o hotel", "levar o fato de banho", "comprar protetor solar", "nadar lado a lado", "descer o rio até ao mar"),
                         ("protetor solar", "uma toalha de praia"), ("hotel", "apartamento"),
                         "ver a previsão do tempo"),
        "trips/city.md": (("visitar o velho museu", "reservar uma mesa para o jantar", "caminhar junto ao rio",
                           "apanhar o comboio da noite"), ("o comboio da noite", "o autocarro da manhã"),
                          ("museu", "castelo"), "comprar um mapa da cidade"),
        "kitchen/soup.md": (("ferver a água", "cortar as cenouras", "juntar sal e pimenta", "mexer e mexer outra vez"),
                            ("sal e pimenta", "ervas frescas"), ("cenouras", "batatas"), "servir bem quente"),
        "kitchen/cake.md": (("misturar a farinha e o leite", "aquecer o forno", "deixar arrefecer o bolo"),
                            ("aquecer o forno", "untar a forma"), ("farinha", "açúcar"), "decorar o bolo")},
    "nl": {
        "shopping.txt": (("melk kopen", "vers brood kopen", "de telefoonrekening betalen"), ("vers brood", "roggebrood"),
                         ("melk", "sap"), "groene appels kopen"),
        "journal.md": (("een lange wandeling langs de rivier", "een goed boek gelezen", "goed geslapen",
                        "een oude vriend gezien"), ("een goed boek", "de ochtendkrant"), ("wandeling", "fietstocht"),
                       "een brief naar huis geschreven"),
        "home/chores.md": (("de planten water geven", "het afval buiten zetten", "de ramen lappen", "waspoeder kopen", "de sokken paar voor paar sorteren"),
                           ("het afval", "het oud papier"), ("planten", "bloemen"), "de vloer vegen"),
        "home/repairs.txt": (("de keukenkraan repareren", "de voordeur verven", "de lamp repareren", "alles stap voor stap nakijken"),
                             ("de voordeur", "het tuinhek"), ("lamp", "klok"), "de poort smeren"),
        "trips/sea.md": (("het hotel boeken", "het badpak inpakken", "zonnebrand kopen", "zij aan zij zwemmen", "langs de rivier naar zee rijden"),
                         ("zonnebrand kopen", "een strandlaken inpakken"), ("hotel", "huisje"), "het weer bekijken"),
        "trips/city.md": (("het oude museum bezoeken", "een tafel voor het diner reserveren", "langs de rivier lopen",
                           "de nachttrein nemen"), ("de nachttrein", "de vroege bus"), ("museum", "kasteel"),
                          "een stadsplattegrond kopen"),
        "kitchen/soup.md": (("het water koken", "de wortels snijden", "zout en peper toevoegen", "roeren en nog eens roeren"),
                            ("zout en peper", "verse kruiden"), ("wortels", "aardappels"), "heet opdienen"),
        "kitchen/cake.md": (("de bloem en de melk mengen", "de oven voorverwarmen", "de taart laten afkoelen"),
                            ("de oven voorverwarmen", "de vorm invetten"), ("bloem", "suiker"), "de taart versieren")},
    "pl": {
        "shopping.txt": (("kupić mleko", "kupić świeży chleb", "zapłacić rachunek za telefon"),
                         ("świeży chleb", "chleb żytni"), ("mleko", "sok"), "kupić zielone jabłka"),
        "journal.md": (("długi spacer nad rzeką", "przeczytałem dobrą książkę", "dobrze spałem",
                        "spotkałem starego przyjaciela"), ("dobrą książkę", "poranną gazetę"), ("spacer", "rejs"),
                       "napisałem list do domu"),
        "home/chores.md": (("podlać kwiaty", "wynieść śmieci", "umyć okna", "kupić proszek do prania", "sprzątać dzień w dzień"), ("wynieść śmieci", "oddać butelki"),
                           ("kwiaty", "zioła"), "zamieść podłogę"),
        "home/repairs.txt": (("naprawić kran w kuchni", "pomalować drzwi wejściowe", "naprawić lampę", "sprawdzać kran ciągle i ciągle", "zarezerwować fachowca"),
                             ("drzwi wejściowe", "płot w ogrodzie"), ("lampę", "półkę"), "naoliwić furtkę"),
        "trips/sea.md": (("zarezerwować hotel", "spakować kostium kąpielowy", "kupić krem z filtrem", "płynąć ramię w ramię", "przejść się po plaży"),
                         ("krem z filtrem", "ręcznik plażowy"), ("hotel", "domek"), "sprawdzić pogodę"),
        "trips/city.md": (("zwiedzić stare muzeum", "zarezerwować stolik na kolację", "przejść się wzdłuż rzeki",
                           "wsiąść do nocnego pociągu"), ("nocnego pociągu", "porannego autobusu"),
                          ("muzeum", "zamek"), "kupić mapę miasta"),
        "kitchen/soup.md": (("zagotować wodę", "pokroić marchewkę", "dodać sól i pieprz", "próbować i znowu próbować"), ("sól i pieprz", "świeże zioła"),
                            ("marchewkę", "cebulę"), "podać na gorąco"),
        "kitchen/cake.md": (("wymieszać mąkę i mleko", "nagrzać piekarnik", "ostudzić ciasto"),
                            ("nagrzać piekarnik", "wysmarować formę"), ("mąkę", "cukier"), "udekorować ciasto")},
}
# текст, какого нет ни в одном файле
НЕТ_ТЕКСТА = {"en": ("call the dentist", "order coffee beans"), "ru": ("позвонить зубному врачу", "купить кофе в зёрнах"),
              "de": ("den Zahnarzt anrufen", "Kaffeebohnen kaufen"), "fr": ("appeler le dentiste", "acheter du café en grains"),
              "es": ("llamar al dentista", "comprar café en grano"), "it": ("chiamare il dentista", "comprare il caffè in grani"),
              "pt": ("ligar ao dentista", "comprar café em grão"), "nl": ("de tandarts bellen", "koffiebonen kopen"),
              "pl": ("zadzwonić do dentysty", "kupić kawę ziarnistą")}
# СЛОВА ВОПРОСОВ ПО РЕПОЗИТОРИЮ — каждое словом и подстрокой стоит одинаково (находка мира — подстрока):
#   ДВАЖДЫ — слово стоит дважды в одной строке: вхождений больше совпавших строк (закон E: occurrences ≠ matches);
#   В_ДВУХ, В_ТРЁХ — слово стоит в двух и в трёх файлах: ответ списком «a and b», «a, b and c»
ДВАЖДЫ = {"en": ("pair", "again", "side", "stir"), "ru": ("всё", "снова", "бок", "пробовать"),
          "de": ("Stück", "immer", "Seite", "probieren"), "fr": ("pièce", "encore", "côte", "goûter"),
          "es": ("poco", "paso", "lado", "remover"), "it": ("poco", "passo", "fianco", "mescolare"),
          "pt": ("pouco", "passo", "lado", "mexer"), "nl": ("paar", "stap", "zij", "roeren"),
          "pl": ("dzień", "ciągle", "ramię", "próbować")}
В_ДВУХ = {"en": ("get", "river"), "ru": ("молоко", "вдоль"), "de": ("Milch", "wieder"), "fr": ("lait", "réserver"),
          "es": ("leche", "junto"), "it": ("latte", "vecchio"), "pt": ("leite", "junto"), "nl": ("melk", "oude"),
          "pl": ("mleko", "przejść")}
В_ТРЁХ = {"en": ("walk", "book"), "ru": ("купить", "реки"), "de": ("kaufen", "Fluss"), "fr": ("acheter", "rivière"),
          "es": ("comprar", "río"), "it": ("comprare", "fiume"), "pt": ("comprar", "rio"), "nl": ("kopen", "rivier"),
          "pl": ("kupić", "zarezerwować")}

def файлы(язык):
    """Файлы репозитория на языке страницы: путь → строки."""
    return {путь: (СОДЕРЖИМОЕ[язык][путь][0] if путь in ТЕКСТЫ else ПРОЕКТ[путь]) for путь in ПУТИ}


def папка(язык):
    """Мир папки над репозиторием языка — ход мира на странице печатается им."""
    return W.Папка(файлы(язык))


def проект_после(правка):
    """Файлы проекта после правки — актом мира папки над объявленным проектом (путь → строки)."""
    акт, путь, доводы = правка
    мир_ = W.Папка(dict(ПРОЕКТ))
    мир2, ход_ = мир_.replace(путь, *доводы) if акт == "replace" else мир_.line(путь, *доводы)
    assert isinstance(ход_, W.Наблюдение), (правка, W.текст(ход_))
    return {п: мир2.файлы[п] for п in ПРОЕКТ}


def состояния():
    """[(имя, файлы проекта)] — объявленный проект и всякое его состояние после правки."""
    return [("база", dict(ПРОЕКТ))] + [(" ".join((акт, путь) + доводы), проект_после((акт, путь, доводы)))
                                       for акт, путь, доводы in ПРАВКИ_ПРОЕКТА + СОСТОЯНИЯ_ИСХОДОВ]


def код_прогона(имя, проект):
    """Файлы проекта, какие читает прогон `имя` (путь → строки)."""
    return {п: tuple(с) for п, с in проект.items() if п.startswith(КОД_ПРОГОНА[имя])}


def отпечаток(имя, проект):
    """Отпечаток состояния для прогона: его код и его команда. Снятое верно, пока отпечаток тот же, что при съёмке."""
    return hashlib.sha256(json.dumps([sorted(код_прогона(имя, проект).items()), ПРОГОНЫ[имя]],
                                     ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


# СЕМЯ ПРОГОНОВ лежит в `tools/seeds/` (М-126): это сырьё генератора, какого сборка не выводит, — бегун идёт однажды,
# а двор воспроизводимости зеркалит семена вместе с домами. Семени нет лишь до первой съёмки. Семя: имя прогона →
# отпечаток состояния проекта → снятое.
СЕМЯ_ПРОГОНОВ = pathlib.Path(__file__).resolve().parent / "seeds" / "toolrepo_runs.json"
ПРОГОНЫ_СНЯТЫЕ = json.loads(СЕМЯ_ПРОГОНОВ.read_text(encoding="utf-8")) if СЕМЯ_ПРОГОНОВ.exists() else {}


def снятое(имя, файлы=None):
    """Снятый отчёт прогона `имя` с проекта в том состоянии, в каком его держит мир (`файлы` — все файлы мира; без
    них — объявленный проект)."""
    return ПРОГОНЫ_СНЯТЫЕ[имя][отпечаток(имя, ПРОЕКТ if файлы is None else файлы)]
