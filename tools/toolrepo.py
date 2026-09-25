#!/usr/bin/env python3
"""ДОМ АКТОВ В РЕПОЗИТОРИИ — руки агента, вторая ступень (25.09, мера ведущего и условия рынка М-2013).

Дом `toolacts` научил ход тела над плоской папкой из шести файлов. Мера ведущего (ядро М-2008, ключ агента на
песочном репозитории: 2 из 50) назвала, чем школа ещё нема: приказ сказан не формой дома («an empty file», без
«the file», «into» вместо «to»), имя файла — литерал рамки (по три имени на род), пути с папкой нет, вопросов о
репозитории нет. Этот дом — те же руки в РЕПОЗИТОРИИ С ПАПКАМИ: создать (с «пустой», «новый», в названной папке),
удалить, перенести в папку, переименовать, заменить и дописать ТЕКСТ В КАВЫЧКАХ из нескольких слов, прогнать
тесты по языку проекта («6 из 7 прошли»), план из двух актов «сделай A, затем B» — и вопросы-поиски: в каком
файле текст, на какой строке, первая и последняя строка, значение ключа в файле настроек, сколько строк, сколько
раз слово во всём репозитории, сколько файлов в папке, где лежит файл.

УСЛОВИЯ РЫНКА (ведущий, М-2013), и как дом их держит:
  1. дыра учится парой: две страницы одного языка, одна форма приказа, разные наполнители — и ИТОГ страницы
     (отчёт, ход «уже есть / нет», ответ) называет каждое слово места дословно. Потому отчёт и ответ называют
     ВСЕ дыры приказа канонической фразой (объект, новое имя, текст, папку, старое и новое), а на всякую форму и
     язык дом пишет не меньше двух страниц с разными наполнителями на всех местах; самопроверка это считает;
  2. текст в кавычках — одна дыра; кавычки приказа и отчёта одни (дверь `toolacts.КАВЫЧКИ`);
  3. путь с папкой («home/chores.md») — одно слово органа: имена путей латиницей без пробелов, а имена, перед
     которыми французское «de» сократилось бы («d'app/…»), не заводятся вовсе — дыра имени иначе не совпала бы
     с отчётом;
  4. английский глагол не совпадает с формой отчёта (create/created, move/moved, run/ran), и у акта один глагол
     на язык — синонимы с тождественными ходами рынок слил бы в дыру;
  5. отказ пользователя ложится в рамку исполненных — исполненных страниц всякой формы больше, чем отказов.

ОДНА ДВЕРЬ НА ПОНЯТИЕ: протокол хода (роли, «да/нет», отказ, вопрос предложения, «уже есть», «нет», леджер,
счётные слова файлов и запусков) — у `actturn`; глаголы создать и удалить — `actturn.ГЛАГОЛЫ`; шаблоны актов
замены, дописывания, переименования, переноса и прогона, фразы объектов в падеже шаблона (`ОБЪЕКТЫ`: слово и
текст, файл, строка, тесты файла, папка), связка плана из двух актов, исход прогона и «прошло P из T» — у
`toolacts`. Здесь объявлены мир, формы вопросов, фраза репозитория и формы приказа «создать пустой / новый».

ВСЯКОЕ ЧИСЛО — МИРА: репозиторий объявлен здесь — восемнадцать файлов, текстовые с содержимым на языке
страницы, код, настройки и тесты — одни на всех языках; число тестов файла — число его тестовых функций, падения
объявлены (и у Python проверены исполнением в самопроверке), значение ключа — строка «ключ = значение» файла
настроек. Всякое число отчёта и ответа вычислено из объявления; суд (courts/toolrepo_court.py) считает сам.

ЧЕГО ДОМ НЕ МЕРИТ, НАЗВАНО: ход «уже есть / нет» у приказа о двух объектах называет лишь тот, какого нет
(«the file X is not there»), — такие страницы ложатся в рамку исполненных, а не учат её; содержимое кода дом не
показывает (он лишь считает строки и тесты); вложенная папка с подпапками («tally») в вопросах о числе файлов не
спрашивается — «сколько файлов» в ней двусмысленно.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actturn as A  # noqa: E402 — дверь хода: роли, да/нет, отказ, «уже есть», «нет», леджер, глаголы, запуски
import toolacts as T  # noqa: E402 — дверь рук: шаблоны актов, фразы объектов, кавычки, исход прогона, связка плана

ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# МИР: репозиторий — восемь текстовых файлов с содержимым на языке страницы и десять файлов проекта
# ======================================================================================================
ТЕКСТЫ = ("shopping.txt", "journal.md", "home/chores.md", "home/repairs.txt", "trips/sea.md", "trips/city.md",
          "kitchen/soup.md", "kitchen/cake.md")
# ПРОЕКТ: код, настройки и тесты — одни на всех языках (язык страницы — не язык кода)
ПРОЕКТ = {
    "server.ini": ("port = 8080", "timeout = 45", "workers = 4"),
    "web/main.py": ("from helpers import greet", "print(greet())"),
    "web/helpers.py": ("def greet(name='world'):", "    return 'hello ' + name.lower()"),
    "web/site.ini": ("retries = 5", "limit = 500", "level = 2"),
    "tests/test_main.py": ("from web.helpers import greet", "def test_greet():", "    assert greet() == 'hello world'",
                           "def test_name():", "    assert greet('bo') == 'hello bo'", "def test_empty():",
                           "    assert greet('') == 'hello '", "def test_upper():",
                           "    assert greet('BO') == 'hello BO'"),
    "tests/test_helpers.py": ("from web.helpers import greet", "def test_type():", "    assert isinstance(greet(), str)",
                            "def test_start():", "    assert greet().startswith('hello')", "def test_len():",
                            "    assert len(greet()) == 11"),
    "tally/Cargo.toml": ("[package]", "name = 'tally'", "edition = '2021'"),
    "tally/src/lib.rs": ("pub fn add(a: i32, b: i32) -> i32 {", "    a + b", "}", "pub fn shout(s: &str) -> String {",
                         "    s.to_uppercase()", "}"),
    "tally/tests/math.rs": ("use tally::add;", "#[test]", "fn adds() { assert_eq!(add(2, 3), 5); }", "#[test]",
                            "fn zero() { assert_eq!(add(0, 0), 0); }", "#[test]",
                            "fn negative() { assert_eq!(add(-1, 1), 0); }"),
    "tally/tests/text.rs": ("use tally::shout;", "#[test]", "fn shouts() { assert_eq!(shout(\"hi\"), \"HI\"); }",
                            "#[test]", "fn empty() { assert_eq!(shout(\"\"), \"\"); }"),
}
# ТЕСТЫ: язык проекта → (расширение файла тестов, начало строки, открывающей тест); падения — исход прогона
ЯЗЫКИ_ПРОЕКТА = {"Python": (".py", "def test_"), "Rust": (".rs", "#[test]")}
ПАДАЮТ = {"tests/test_main.py": ("test_upper",)}
ФАЙЛЫ_ТЕСТОВ = tuple(ф for ф in ПРОЕКТ if ф.split("/")[-1].startswith("test_") or "/tests/" in ф)
НАСТРОЙКИ = tuple(ф for ф in ПРОЕКТ if ф.endswith(".ini"))
ПУТИ = ТЕКСТЫ + tuple(ПРОЕКТ)
ЗАПУСКИ_ДО = (0, 1, 3)          # запусков мира до прогона — леджер запусков (дверь `actturn`)

# АКТЫ НАД МИРОМ — пути и имена; всякое имя вне мира объявлено как новое или как отсутствующее
СОЗДАТЬ_ПУТИ = ("plan.md", "memo.txt", "home/garden.md", "trips/lake.md", "kitchen/salad.md", "web/config.py",
                "tests/test_net.py", "tally/src/net.rs")
СОЗДАТЬ_В_ПАПКЕ = (("garden.md", "home"), ("lake.md", "trips"), ("salad.md", "kitchen"), ("config.py", "web"),
                   ("test_net.py", "tests"), ("net.rs", "tally/src"))
УДАЛИТЬ_ИЗ_ПАПКИ = (("chores.md", "home"), ("city.md", "trips"), ("cake.md", "kitchen"), ("helpers.py", "web"),
                    ("test_helpers.py", "tests"), ("text.rs", "tally/tests"))
ПЕРЕНОСЫ = (("shopping.txt", "home"), ("journal.md", "backup"), ("home/chores.md", "kitchen"),
            ("home/repairs.txt", "backup"), ("trips/sea.md", "done"), ("trips/city.md", "home"),
            ("kitchen/soup.md", "done"), ("kitchen/cake.md", "trips"))
ИМЕНА = (("shopping.txt", "groceries.txt"), ("journal.md", "diary.md"), ("home/chores.md", "tasks.md"),
         ("home/repairs.txt", "fixes.txt"), ("trips/sea.md", "beach.md"), ("trips/city.md", "town.md"),
         ("kitchen/soup.md", "broth.md"), ("kitchen/cake.md", "pie.md"))
ИМЕНА_ЗАНЯТЫ = (("home/chores.md", "repairs.txt"), ("trips/sea.md", "city.md"), ("kitchen/cake.md", "soup.md"))
НЕТ_ФАЙЛОВ = ("budget.md", "recipes.txt")
ИМЕНА_НЕТ = (("budget.md", "costs.md"), ("recipes.txt", "menu.txt"))
КЛЮЧИ = (("server.ini", "port"), ("web/site.ini", "retries"), ("server.ini", "timeout"), ("web/site.ini", "limit"),
         ("server.ini", "workers"), ("web/site.ini", "level"))
ПАПКИ_СЧЁТА = ("home", "trips", "kitchen", "web", "tests", "tally/src", "tally/tests")

# (строки файла; текст для замены и чем заменить; слово для замены и чем заменить; строка для дописывания)
СОДЕРЖИМОЕ = {
    "en": {
        "shopping.txt": (("get eggs", "get fresh bread", "pay the phone bill"), ("fresh bread", "rye bread"),
                         ("eggs", "rice"), "get green apples"),
        "journal.md": (("a long walk by the river", "read a good book", "slept well", "met an old friend"),
                       ("a good book", "the morning paper"), ("walk", "swim"), "wrote a letter home"),
        "home/chores.md": (("water the plants", "take out the trash", "clean the windows"),
                           ("the trash", "the recycling"), ("plants", "flowers"), "sweep the floor"),
        "home/repairs.txt": (("fix the kitchen tap", "paint the front door", "fix the lamp"),
                             ("the front door", "the garden fence"), ("lamp", "clock"), "oil the gate"),
        "trips/sea.md": (("book the hotel", "pack the swimsuit", "get sun cream"), ("sun cream", "a beach towel"),
                         ("hotel", "cabin"), "check the weather"),
        "trips/city.md": (("visit the old museum", "book a table for dinner", "walk along the river",
                           "take the night train"), ("the night train", "the early bus"), ("museum", "castle"),
                          "get a city map"),
        "kitchen/soup.md": (("boil the water", "cut the carrots", "stir in salt and pepper"),
                            ("salt and pepper", "fresh herbs"), ("carrots", "potatoes"), "serve it hot"),
        "kitchen/cake.md": (("mix the flour and the butter", "heat the oven", "let the cake cool"),
                            ("heat the oven", "grease the pan"), ("flour", "sugar"), "decorate the cake")},
    "ru": {
        "shopping.txt": (("купить молоко", "купить свежий хлеб", "оплатить счёт за телефон"),
                         ("свежий хлеб", "ржаной хлеб"), ("молоко", "сок"), "купить зелёные яблоки"),
        "journal.md": (("долгая прогулка у реки", "читал хорошую книгу", "хорошо выспался", "встретил старого друга"),
                       ("хорошую книгу", "утреннюю газету"), ("прогулка", "поездка"), "написал письмо домой"),
        "home/chores.md": (("полить цветы", "вынести мусор", "помыть окна"), ("вынести мусор", "сдать бутылки"),
                           ("цветы", "кактусы"), "подмести пол"),
        "home/repairs.txt": (("починить кран на кухне", "покрасить входную дверь", "починить лампу"),
                             ("входную дверь", "садовый забор"), ("лампу", "полку"), "смазать калитку"),
        "trips/sea.md": (("забронировать гостиницу", "уложить купальник", "купить крем от солнца"),
                         ("крем от солнца", "пляжное полотенце"), ("гостиницу", "домик"), "узнать погоду"),
        "trips/city.md": (("сходить в старый музей", "заказать столик на ужин", "погулять вдоль реки",
                           "сесть на ночной поезд"), ("ночной поезд", "утренний автобус"), ("музей", "замок"),
                          "купить карту города"),
        "kitchen/soup.md": (("вскипятить воду", "нарезать морковь", "добавить соль и перец"),
                            ("соль и перец", "свежую зелень"), ("морковь", "картошку"), "подать горячим"),
        "kitchen/cake.md": (("смешать муку и молоко", "разогреть духовку", "дать пирогу остыть"),
                            ("разогреть духовку", "смазать форму"), ("муку", "сахар"), "украсить пирог")},
    "de": {
        "shopping.txt": (("Milch kaufen", "frisches Brot kaufen", "die Handyrechnung bezahlen"),
                         ("frisches Brot", "dunkles Brot"), ("Milch", "Saft"), "grüne Äpfel kaufen"),
        "journal.md": (("ein langer Spaziergang am Fluss", "ein gutes Buch gelesen", "gut geschlafen",
                        "einen alten Freund getroffen"), ("ein gutes Buch", "die Morgenzeitung"),
                       ("Spaziergang", "Ausflug"), "einen Brief nach Hause geschrieben"),
        "home/chores.md": (("die Pflanzen gießen", "den Müll rausbringen", "die Fenster putzen"),
                           ("den Müll", "das Altpapier"), ("Pflanzen", "Blumen"), "den Boden fegen"),
        "home/repairs.txt": (("den Wasserhahn in der Küche reparieren", "die Haustür streichen", "die Lampe reparieren"),
                             ("die Haustür", "den Gartenzaun"), ("Lampe", "Uhr"), "das Tor ölen"),
        "trips/sea.md": (("das Hotel buchen", "den Badeanzug einpacken", "Sonnencreme kaufen"),
                         ("Sonnencreme kaufen", "ein Strandtuch einpacken"), ("Hotel", "Zimmer"), "das Wetter prüfen"),
        "trips/city.md": (("das alte Museum besuchen", "einen Tisch zum Abendessen reservieren",
                           "am Fluss entlang spazieren", "den Nachtzug nehmen"), ("den Nachtzug", "den Frühbus"),
                          ("Museum", "Schloss"), "einen Stadtplan kaufen"),
        "kitchen/soup.md": (("das Wasser kochen", "die Karotten schneiden", "Salz und Pfeffer dazugeben"),
                            ("Salz und Pfeffer", "frische Kräuter"), ("Karotten", "Kartoffeln"), "heiß servieren"),
        "kitchen/cake.md": (("Mehl und Milch verrühren", "den Ofen vorheizen", "den Kuchen abkühlen lassen"),
                            ("den Ofen vorheizen", "die Form einfetten"), ("Mehl", "Zucker"), "den Kuchen verzieren")},
    "fr": {
        "shopping.txt": (("acheter du lait", "acheter du pain frais", "payer la facture du téléphone"),
                         ("du pain frais", "du pain de seigle"), ("lait", "jus"), "acheter des pommes vertes"),
        "journal.md": (("une longue promenade au bord de la rivière", "lu un bon livre", "bien dormi",
                        "revu un vieil ami"), ("un bon livre", "le journal du matin"), ("promenade", "balade"),
                       "écrit une lettre aux parents"),
        "home/chores.md": (("arroser les plantes", "sortir la poubelle", "laver les fenêtres"),
                           ("la poubelle", "le recyclage"), ("plantes", "fleurs"), "balayer le sol"),
        "home/repairs.txt": (("réparer le robinet de la cuisine", "peindre la porte bleue", "réparer la lampe"),
                             ("la porte bleue", "la clôture du jardin"), ("lampe", "pendule"), "huiler le portail"),
        "trips/sea.md": (("réserver la chambre", "emporter le maillot de bain", "acheter de la crème solaire"),
                         ("de la crème solaire", "une serviette de plage"), ("chambre", "cabane"),
                         "regarder la météo"),
        "trips/city.md": (("visiter le vieux musée", "réserver une table pour le dîner", "marcher le long de la rivière",
                           "prendre le train de nuit"), ("le train de nuit", "le bus du matin"),
                          ("musée", "château"), "acheter un plan de la ville"),
        "kitchen/soup.md": (("chauffer le bouillon", "couper les carottes", "ajouter le sel et le poivre"),
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
        "home/chores.md": (("regar las plantas", "sacar la basura", "limpiar las ventanas"),
                           ("la basura", "el reciclaje"), ("plantas", "flores"), "barrer el suelo"),
        "home/repairs.txt": (("arreglar el grifo de la cocina", "pintar la puerta de entrada", "arreglar la lámpara"),
                             ("la puerta de entrada", "la valla del jardín"), ("lámpara", "estantería"),
                             "engrasar la verja"),
        "trips/sea.md": (("reservar el hotel", "meter el bañador", "comprar crema solar"),
                         ("crema solar", "una toalla de playa"), ("hotel", "apartamento"), "mirar el tiempo"),
        "trips/city.md": (("visitar el viejo museo", "reservar una mesa para cenar", "caminar junto al río",
                           "tomar el tren nocturno"), ("el tren nocturno", "el autobús de la mañana"),
                          ("museo", "castillo"), "comprar un plano de la ciudad"),
        "kitchen/soup.md": (("hervir el agua", "cortar las zanahorias", "añadir sal y pimienta"),
                            ("sal y pimienta", "hierbas frescas"), ("zanahorias", "patatas"), "servir bien caliente"),
        "kitchen/cake.md": (("mezclar la harina y la leche", "calentar el horno", "dejar enfriar el pastel"),
                            ("calentar el horno", "engrasar el molde"), ("harina", "azúcar"), "decorar el pastel")},
    "it": {
        "shopping.txt": (("comprare il latte", "comprare il pane fresco", "pagare la bolletta del telefono"),
                         ("il pane fresco", "il pane di segale"), ("latte", "succo"), "comprare le mele verdi"),
        "journal.md": (("una lunga passeggiata lungo il fiume", "letto un buon libro", "dormito bene",
                        "rivisto un vecchio amico"), ("un buon libro", "il giornale del mattino"),
                       ("passeggiata", "gita"), "scritto una lettera a casa"),
        "home/chores.md": (("annaffiare le piante", "portare fuori la spazzatura", "lavare le finestre"),
                           ("la spazzatura", "la carta"), ("piante", "rose"), "spazzare il pavimento"),
        "home/repairs.txt": (("riparare il rubinetto della cucina", "dipingere la porta di casa", "riparare la lampada"),
                             ("la porta di casa", "il recinto del giardino"), ("lampada", "mensola"),
                             "oliare il cancello"),
        "trips/sea.md": (("prenotare la stanza", "mettere in valigia il costume", "comprare la crema solare"),
                         ("la crema solare", "un telo da spiaggia"), ("stanza", "cabina"), "guardare il meteo"),
        "trips/city.md": (("visitare il vecchio museo", "prenotare un tavolo per cena", "camminare lungo il fiume",
                           "prendere il treno di notte"), ("il treno di notte", "il pullman del mattino"),
                          ("museo", "castello"), "comprare una mappa della città"),
        "kitchen/soup.md": (("scaldare il brodo", "tagliare le carote", "aggiungere sale e pepe"),
                            ("sale e pepe", "erbe fresche"), ("carote", "patate"), "servire ben caldo"),
        "kitchen/cake.md": (("mescolare la farina e il latte", "accendere il forno", "lasciar raffreddare la torta"),
                            ("accendere il forno", "imburrare lo stampo"), ("farina", "zucchero"), "decorare la torta")},
    "pt": {
        "shopping.txt": (("comprar leite", "comprar pão fresco", "pagar a conta do telefone"),
                         ("pão fresco", "pão de centeio"), ("leite", "sumo"), "comprar maçãs verdes"),
        "journal.md": (("um longo passeio junto ao rio", "li um bom livro", "dormi bem", "encontrei um velho amigo"),
                       ("um bom livro", "o jornal da manhã"), ("passeio", "percurso"), "escrevi uma carta para casa"),
        "home/chores.md": (("regar as plantas", "levar o lixo", "lavar as janelas"), ("o lixo", "a reciclagem"),
                           ("plantas", "flores"), "varrer o chão"),
        "home/repairs.txt": (("arranjar a torneira da cozinha", "pintar a porta da entrada", "arranjar o candeeiro"),
                             ("a porta da entrada", "a vedação do jardim"), ("candeeiro", "relógio"),
                             "olear o portão"),
        "trips/sea.md": (("reservar o hotel", "levar o fato de banho", "comprar protetor solar"),
                         ("protetor solar", "uma toalha de praia"), ("hotel", "apartamento"),
                         "ver a previsão do tempo"),
        "trips/city.md": (("visitar o velho museu", "reservar uma mesa para o jantar", "caminhar junto ao rio",
                           "apanhar o comboio da noite"), ("o comboio da noite", "o autocarro da manhã"),
                          ("museu", "castelo"), "comprar um mapa da cidade"),
        "kitchen/soup.md": (("ferver a água", "cortar as cenouras", "juntar sal e pimenta"),
                            ("sal e pimenta", "ervas frescas"), ("cenouras", "batatas"), "servir bem quente"),
        "kitchen/cake.md": (("misturar a farinha e o leite", "aquecer o forno", "deixar arrefecer o bolo"),
                            ("aquecer o forno", "untar a forma"), ("farinha", "açúcar"), "decorar o bolo")},
    "nl": {
        "shopping.txt": (("melk kopen", "vers brood kopen", "de telefoonrekening betalen"), ("vers brood", "roggebrood"),
                         ("melk", "sap"), "groene appels kopen"),
        "journal.md": (("een lange wandeling langs de rivier", "een goed boek gelezen", "goed geslapen",
                        "een oude vriend gezien"), ("een goed boek", "de ochtendkrant"), ("wandeling", "fietstocht"),
                       "een brief naar huis geschreven"),
        "home/chores.md": (("de planten water geven", "het afval buiten zetten", "de ramen lappen"),
                           ("het afval", "het oud papier"), ("planten", "bloemen"), "de vloer vegen"),
        "home/repairs.txt": (("de keukenkraan repareren", "de voordeur verven", "de lamp repareren"),
                             ("de voordeur", "het tuinhek"), ("lamp", "klok"), "de poort smeren"),
        "trips/sea.md": (("het hotel boeken", "het badpak inpakken", "zonnebrand kopen"),
                         ("zonnebrand kopen", "een strandlaken inpakken"), ("hotel", "huisje"), "het weer bekijken"),
        "trips/city.md": (("het oude museum bezoeken", "een tafel voor het diner reserveren", "langs de rivier lopen",
                           "de nachttrein nemen"), ("de nachttrein", "de vroege bus"), ("museum", "kasteel"),
                          "een stadsplattegrond kopen"),
        "kitchen/soup.md": (("het water koken", "de wortels snijden", "zout en peper toevoegen"),
                            ("zout en peper", "verse kruiden"), ("wortels", "aardappels"), "heet opdienen"),
        "kitchen/cake.md": (("de bloem en de melk mengen", "de oven voorverwarmen", "de taart laten afkoelen"),
                            ("de oven voorverwarmen", "de vorm invetten"), ("bloem", "suiker"), "de taart versieren")},
    "pl": {
        "shopping.txt": (("kupić mleko", "kupić świeży chleb", "zapłacić rachunek za telefon"),
                         ("świeży chleb", "chleb żytni"), ("mleko", "sok"), "kupić zielone jabłka"),
        "journal.md": (("długi spacer nad rzeką", "przeczytałem dobrą książkę", "dobrze spałem",
                        "spotkałem starego przyjaciela"), ("dobrą książkę", "poranną gazetę"), ("spacer", "rejs"),
                       "napisałem list do domu"),
        "home/chores.md": (("podlać kwiaty", "wynieść śmieci", "umyć okna"), ("wynieść śmieci", "oddać butelki"),
                           ("kwiaty", "zioła"), "zamieść podłogę"),
        "home/repairs.txt": (("naprawić kran w kuchni", "pomalować drzwi wejściowe", "naprawić lampę"),
                             ("drzwi wejściowe", "płot w ogrodzie"), ("lampę", "półkę"), "naoliwić furtkę"),
        "trips/sea.md": (("zarezerwować hotel", "spakować kostium kąpielowy", "kupić krem z filtrem"),
                         ("krem z filtrem", "ręcznik plażowy"), ("hotel", "domek"), "sprawdzić pogodę"),
        "trips/city.md": (("zwiedzić stare muzeum", "zarezerwować stolik na kolację", "przejść się wzdłuż rzeki",
                           "wsiąść do nocnego pociągu"), ("nocnego pociągu", "porannego autobusu"),
                          ("muzeum", "zamek"), "kupić mapę miasta"),
        "kitchen/soup.md": (("zagotować wodę", "pokroić marchewkę", "dodać sól i pieprz"), ("sól i pieprz", "świeże zioła"),
                            ("marchewkę", "cebulę"), "podać na gorąco"),
        "kitchen/cake.md": (("wymieszać mąkę i mleko", "nagrzać piekarnik", "ostudzić ciasto"),
                            ("nagrzać piekarnik", "wysmarować formę"), ("mąkę", "cukier"), "udekorować ciasto")},
}
# текст, какого нет ни в одном файле; слова, какие спрашиваются по всему репозиторию
НЕТ_ТЕКСТА = {"en": ("call the dentist", "order coffee beans"), "ru": ("позвонить зубному врачу", "купить кофе в зёрнах"),
              "de": ("den Zahnarzt anrufen", "Kaffeebohnen kaufen"), "fr": ("appeler le dentiste", "acheter du café en grains"),
              "es": ("llamar al dentista", "comprar café en grano"), "it": ("chiamare il dentista", "comprare il caffè in grani"),
              "pt": ("ligar ao dentista", "comprar café em grão"), "nl": ("de tandarts bellen", "koffiebonen kopen"),
              "pl": ("zadzwonić do dentysty", "kupić kawę ziarnistą")}
СЛОВА_РЕПО = {"en": ("get", "book", "river", "fix"), "ru": ("купить", "молоко", "реки", "починить"),
              "de": ("kaufen", "Milch", "Fluss", "reparieren"), "fr": ("acheter", "lait", "rivière", "réparer"),
              "es": ("comprar", "leche", "río", "arreglar"), "it": ("comprare", "latte", "fiume", "riparare"),
              "pt": ("comprar", "leite", "rio", "arranjar"), "nl": ("kopen", "melk", "rivier", "repareren"),
              "pl": ("kupić", "mleko", "zarezerwować", "naprawić")}

# ======================================================================================================
# РЕЧЬ: фраза репозитория, формы «создать пустой / новый», инфинитив акта двери хода, вопросы и ответы
# ======================================================================================================
# слоты вопросов: {Ф} файл, {Фр} «файла», {М} «в файле», {Дв} «в папке» — формы у двери `toolacts.ОБЪЕКТЫ`;
# {Р} «в репозитории», {K}/{Kо} ключ, {W}/{Wи}/{Wнет} текст, {НФ} «файла» отрицания у двери хода
РЕЧЬ = {
    "en": dict(репо="the repository contains {N}", в_репо="in the repository", место="{позиция} {Фр}", инф_акта="{V} {Ф}",
               пустой="an empty file {f}", новый="a new file {f}", тесты_языка="the {Я} tests",
               q_файл="which file contains {W}?", нигде="no file contains {W}",
               q_строка="on which line {Фр} is {Wи}?", q_первая="what is the first line {Фр}?",
               q_последняя="what is the last line {Фр}?", читается="line {a} {Фр} reads {T}",
               ключ=("the key {k}", "{k}"), ключ_о=("of the key {k}", "of {k}"),
               q_ключ="what is the value {Kо} {М}?", ключ_ответ="{K} {М} has the value {v}",
               q_строк="how many lines are {М}?", q_папка="how many files are {Дв}?",
               q_где="where is {Ф}?", где_ответ="{Ф} is {Дв}", нет_в_репо="{Ф} is not {Р}"),
    "ru": dict(репо="репозиторий содержит {N}", в_репо="в репозитории", место="{М} {позиция}", инф_акта="{V} {Ф}",
               пустой="пустой файл {f}", новый="новый файл {f}", тесты_языка="тесты {Я}",
               q_файл="в каком файле есть {Wи}?", нигде="{Wнет} нет ни в одном файле",
               q_строка="в какой строке {Фр} стоит {Wи}?", q_первая="какая первая строка {Фр}?",
               q_последняя="какая последняя строка {Фр}?", читается="{М} в строке {a} написано {T}",
               ключ=("ключ {k}", "{k}"), ключ_о=("у ключа {k}", "у {k}"),
               q_ключ="какое значение {Kо} {М}?", ключ_ответ="{Kо} {М} значение {v}",
               q_строк="сколько строк {М}?", q_папка="сколько файлов {Дв}?",
               q_где="где лежит {Ф}?", где_ответ="{Ф} лежит {Дв}", нет_в_репо="{НФ} нет {Р}"),
    "de": dict(репо="das Repository enthält {N}", в_репо="im Repository", место="{позиция} {Фр}", инф_акта="{Ф} {V}",
               пустой="eine leere Datei {f}", новый="eine neue Datei {f}", тесты_языка="die Tests für {Я}",
               q_файл="welche Datei enthält {W}?", нигде="keine Datei enthält {W}",
               q_строка="in welcher Zeile {Фр} steht {Wи}?", q_первая="was steht in der ersten Zeile {Фр}?",
               q_последняя="was steht in der letzten Zeile {Фр}?", читается="in Zeile {a} {Фр} steht {T}",
               ключ=("der Schlüssel {k}", "{k}"), ключ_о=("der Schlüssel {k}", "{k}"),
               q_ключ="welchen Wert hat {Kо} {М}?", ключ_ответ="{K} {М} hat den Wert {v}",
               q_строк="wie viele Zeilen hat {Ф}?", q_папка="wie viele Dateien sind {Дв}?",
               q_где="wo liegt {Ф}?", где_ответ="{Ф} liegt {Дв}", нет_в_репо="{Ф} gibt es {Р} nicht"),
    "fr": dict(репо="le dépôt contient {N}", в_репо="dans le dépôt", место="{позиция} {Фр}", инф_акта="{V} {Ф}",
               пустой="un fichier vide {f}", новый="un nouveau fichier {f}", тесты_языка="les tests {Я}",
               q_файл="quel fichier contient {W} ?", нигде="aucun fichier ne contient {W}",
               q_строка="à quelle ligne {Фр} se trouve {Wи} ?", q_первая="quelle est la première ligne {Фр} ?",
               q_последняя="quelle est la dernière ligne {Фр} ?", читается="la ligne {a} {Фр} contient {T}",
               ключ=("la clé {k}", "{k}"), ключ_о=("de la clé {k}", "de {k}"),
               q_ключ="quelle est la valeur {Kо} {М} ?", ключ_ответ="{K} {М} a la valeur {v}",
               q_строк="combien de lignes contient {Ф} ?", q_папка="combien de fichiers y a-t-il {Дв} ?",
               q_где="où se trouve {Ф} ?", где_ответ="{Ф} se trouve {Дв}", нет_в_репо="{Ф} n'est pas {Р}"),
    "es": dict(репо="el repositorio contiene {N}", в_репо="en el repositorio", место="{позиция} {Фр}", инф_акта="{V} {Ф}",
               пустой="un archivo vacío {f}", новый="un archivo nuevo {f}", тесты_языка="las pruebas de {Я}",
               q_файл="¿qué archivo contiene {W}?", нигде="ningún archivo contiene {W}",
               q_строка="¿en qué línea {Фр} está {Wи}?", q_первая="¿cuál es la primera línea {Фр}?",
               q_последняя="¿cuál es la última línea {Фр}?", читается="la línea {a} {Фр} dice {T}",
               ключ=("la clave {k}", "{k}"), ключ_о=("de la clave {k}", "de {k}"),
               q_ключ="¿cuál es el valor {Kо} {М}?", ключ_ответ="{K} {М} tiene el valor {v}",
               q_строк="¿cuántas líneas tiene {Ф}?", q_папка="¿cuántos archivos hay {Дв}?",
               q_где="¿dónde está {Ф}?", где_ответ="{Ф} está {Дв}", нет_в_репо="{Ф} no está {Р}"),
    "it": dict(репо="il repository contiene {N}", в_репо="nel repository", место="{позиция} {Фр}", инф_акта="{V} {Ф}",
               пустой="un file vuoto {f}", новый="un nuovo file {f}", тесты_языка="i test {Я}",
               q_файл="quale file contiene {W}?", нигде="nessun file contiene {W}",
               q_строка="in quale riga {Фр} si trova {Wи}?", q_первая="qual è la prima riga {Фр}?",
               q_последняя="qual è l'ultima riga {Фр}?", читается="la riga {a} {Фр} dice {T}",
               ключ=("la chiave {k}", "{k}"), ключ_о=("della chiave {k}", "di {k}"),
               q_ключ="qual è il valore {Kо} {М}?", ключ_ответ="{K} {М} ha il valore {v}",
               q_строк="quante righe ha {Ф}?", q_папка="quanti file ci sono {Дв}?",
               q_где="dove si trova {Ф}?", где_ответ="{Ф} si trova {Дв}", нет_в_репо="{Ф} non è {Р}"),
    "pt": dict(репо="o repositório contém {N}", в_репо="no repositório", место="{позиция} {Фр}", инф_акта="{V} {Ф}",
               пустой="um ficheiro vazio {f}", новый="um novo ficheiro {f}", тесты_языка="os testes de {Я}",
               q_файл="que ficheiro contém {W}?", нигде="nenhum ficheiro contém {W}",
               q_строка="em que linha {Фр} está {Wи}?", q_первая="qual é a primeira linha {Фр}?",
               q_последняя="qual é a última linha {Фр}?", читается="a linha {a} {Фр} diz {T}",
               ключ=("a chave {k}", "{k}"), ключ_о=("da chave {k}", "de {k}"),
               q_ключ="qual é o valor {Kо} {М}?", ключ_ответ="{K} {М} tem o valor {v}",
               q_строк="quantas linhas tem {Ф}?", q_папка="quantos ficheiros há {Дв}?",
               q_где="onde está {Ф}?", где_ответ="{Ф} está {Дв}", нет_в_репо="{Ф} não está {Р}"),
    "nl": dict(репо="de repository bevat {N}", в_репо="in de repository", место="{позиция} {Фр}", инф_акта="{Ф} {V}",
               пустой="een leeg bestand {f}", новый="een nieuw bestand {f}", тесты_языка="de tests voor {Я}",
               q_файл="welk bestand bevat {W}?", нигде="geen bestand bevat {W}",
               q_строка="in welke regel {Фр} staat {Wи}?", q_первая="wat is de eerste regel {Фр}?",
               q_последняя="wat is de laatste regel {Фр}?", читается="regel {a} {Фр} luidt {T}",
               ключ=("de sleutel {k}", "{k}"), ключ_о=("van de sleutel {k}", "van {k}"),
               q_ключ="wat is de waarde {Kо} {М}?", ключ_ответ="{K} {М} heeft de waarde {v}",
               q_строк="hoeveel regels heeft {Ф}?", q_папка="hoeveel bestanden zitten er {Дв}?",
               q_где="waar staat {Ф}?", где_ответ="{Ф} staat {Дв}", нет_в_репо="{Ф} staat niet {Р}"),
    "pl": dict(репо="repozytorium zawiera {N}", в_репо="w repozytorium", место="{М} {позиция}", инф_акта="{V} {Ф}",
               пустой="pusty plik {f}", новый="nowy plik {f}", тесты_языка="testy {Я}",
               q_файл="który plik zawiera {W}?", нигде="żaden plik nie zawiera {Wнет}",
               q_строка="w której linii {Фр} jest {Wи}?", q_первая="jaka jest pierwsza linia {Фр}?",
               q_последняя="jaka jest ostatnia linia {Фр}?", читается="{М} linia {a} brzmi {T}",
               ключ=("klucz {k}", "{k}"), ключ_о=("klucza {k}", "{k}"),
               q_ключ="jaka jest wartość {Kо} {М}?", ключ_ответ="{K} {М} ma wartość {v}",
               q_строк="ile linii ma {Ф}?", q_папка="ile plików jest {Дв}?",
               q_где="gdzie jest {Ф}?", где_ответ="{Ф} jest {Дв}", нет_в_репо="{НФ} nie ma {Р}"),
}
РЕГИСТРЫ = ("плоский", "вежливый")

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
ДОПИСАТЬ_НЕТ = "дописать строку в файл, которого нет"
ДОПИСАТЬ_ОТКАЗ = "дописать строку — отказ"
ТЕСТЫ_ЯЗЫКА = "прогон тестов по языку проекта"
ТЕСТЫ_ФАЙЛА = "прогон тестов файла по пути"
ТЕСТЫ_ОТКАЗ = "прогон тестов — отказ"
ПЛАН_ЗАМЕНА = "план: заменить, затем прогнать тесты"
ПЛАН_ДОПИСАТЬ = "план: дописать, затем прогнать тесты"
ПЛАН_ПЕРЕНОС = "план: перенести, затем удалить"
ПЛАН_ОТКАЗ = "план из двух актов — отказ"
В_КАКОМ = "в каком файле текст — вопрос"
НИГДЕ = "текста нет ни в одном файле — вопрос"
НА_СТРОКЕ = "на какой строке файла текст — вопрос"
ПЕРВАЯ = "первая строка файла — вопрос"
ПОСЛЕДНЯЯ = "последняя строка файла — вопрос"
КЛЮЧ = "значение ключа в файле настроек — вопрос"
СТРОК = "сколько строк в файле — вопрос"
РАЗ_В_РЕПО = "сколько раз слово во всём репозитории — вопрос"
ФАЙЛОВ = "сколько файлов в папке — вопрос"
ГДЕ = "где лежит файл — вопрос"
ГДЕ_НЕТ = "файла нет в репозитории — вопрос"
РОДЫ = (СОЗДАТЬ, СОЗДАТЬ_ПАПКА, СОЗДАТЬ_ЕСТЬ, СОЗДАТЬ_ОТКАЗ, УДАЛИТЬ, УДАЛИТЬ_ПАПКА, УДАЛИТЬ_НЕТ, УДАЛИТЬ_ОТКАЗ,
        ПЕРЕНОС, ПЕРЕНОС_НЕТ, ПЕРЕНОС_ОТКАЗ, ИМЯ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ, ИМЯ_ОТКАЗ, ЗАМЕНА, ЗАМЕНА_СЛОВА, ЗАМЕНА_НЕТ,
        ЗАМЕНА_ОТКАЗ, ДОПИСАТЬ, ДОПИСАТЬ_НЕТ, ДОПИСАТЬ_ОТКАЗ, ТЕСТЫ_ЯЗЫКА, ТЕСТЫ_ФАЙЛА, ТЕСТЫ_ОТКАЗ, ПЛАН_ЗАМЕНА,
        ПЛАН_ДОПИСАТЬ, ПЛАН_ПЕРЕНОС, ПЛАН_ОТКАЗ, В_КАКОМ, НИГДЕ, НА_СТРОКЕ, ПЕРВАЯ, ПОСЛЕДНЯЯ, КЛЮЧ, СТРОК,
        РАЗ_В_РЕПО, ФАЙЛОВ, ГДЕ, ГДЕ_НЕТ)
ВОПРОСЫ = frozenset({В_КАКОМ, НИГДЕ, НА_СТРОКЕ, ПЕРВАЯ, ПОСЛЕДНЯЯ, КЛЮЧ, СТРОК, РАЗ_В_РЕПО, ФАЙЛОВ, ГДЕ, ГДЕ_НЕТ})
ОТКАЗЫ = frozenset({СОЗДАТЬ_ОТКАЗ, УДАЛИТЬ_ОТКАЗ, ПЕРЕНОС_ОТКАЗ, ИМЯ_ОТКАЗ, ЗАМЕНА_ОТКАЗ, ДОПИСАТЬ_ОТКАЗ,
                    ТЕСТЫ_ОТКАЗ, ПЛАН_ОТКАЗ})
НЕВОЗМОЖНЫЕ = frozenset({СОЗДАТЬ_ЕСТЬ, УДАЛИТЬ_НЕТ, ПЕРЕНОС_НЕТ, ИМЯ_ЗАНЯТО, ИМЯ_НЕТ, ЗАМЕНА_НЕТ, ДОПИСАТЬ_НЕТ})


# ======================================================================================================
# МИР СЧИТАЕТ
# ======================================================================================================
def строки_файла(язык, путь):
    """Строки файла: текстовые — на языке страницы, проекта — одни на всех; вне мира — None."""
    if путь in ТЕКСТЫ:
        return СОДЕРЖИМОЕ[язык][путь][0]
    return ПРОЕКТ.get(путь)


def папка_пути(путь):
    return путь.rsplit("/", 1)[0] if "/" in путь else ""


def имя_пути(путь):
    return путь.rsplit("/", 1)[-1]


def файлов_в_папке(папка):
    """Файлы, лежащие прямо в папке (не в её подпапках) — «сколько файлов в папке home»."""
    return sum(1 for п in ПУТИ if папка_пути(п) == папка)


def вхождений(строка, текст):
    """Сколько раз текст стоит в строке ЦЕЛЫМИ словами (текст из нескольких слов — подряд)."""
    с, т = строка.split(), текст.split()
    return sum(1 for i in range(len(с) - len(т) + 1) if с[i:i + len(т)] == т)


def в_файле(язык, путь, текст):
    return sum(вхождений(с, текст) for с in строки_файла(язык, путь))


def строки_с(язык, путь, текст):
    return [i + 1 for i, с in enumerate(строки_файла(язык, путь)) if вхождений(с, текст)]


def файлы_с(язык, текст):
    return [п for п in ПУТИ if в_файле(язык, п, текст)]


def значение_ключа(путь, ключ):
    for строка in ПРОЕКТ[путь]:
        к, _, з = строка.partition(" = ")
        if к == ключ:
            return з
    return None


def тестов(путь):
    _расширение, начало = next(в for в in ЯЗЫКИ_ПРОЕКТА.values() if путь.endswith(в[0]))
    return sum(1 for с in ПРОЕКТ[путь] if с.startswith(начало))


def тесты_языка(язык_проекта):
    """(тестов, падает) по всем файлам тестов языка проекта."""
    расширение = ЯЗЫКИ_ПРОЕКТА[язык_проекта][0]
    файлы = [ф for ф in ФАЙЛЫ_ТЕСТОВ if ф.endswith(расширение)]
    return sum(тестов(ф) for ф in файлы), sum(len(ПАДАЮТ.get(ф, ())) for ф in файлы)


def тесты_файла(путь):
    return тестов(путь), len(ПАДАЮТ.get(путь, ()))


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


def репо(язык, N):
    """«the repository contains 19 files» — N приходит готовой счётной фразой."""
    return РЕЧЬ[язык]["репо"].format(N=N)


def _ход(язык, приказ_, предложение_, да, итог):
    return T.ход(язык, приказ_, предложение_, да, итог)


def _регистр(язык, регистр, imp):
    return _ф(язык, T.РЕЧЬ[язык]["регистры"][регистр].format(imp=imp, inf=imp))


def _предложение(язык, inf, zu):
    return _ф(язык, T.РЕЧЬ[язык]["предложение"].format(inf=inf, zu=zu) + ". " + T._вопрос_предложения(язык))


def _отказ(язык, хвост):
    return A.РЕЧЬ[язык]["отказ"] + ". " + хвост


# АКТ ДВЕРИ ХОДА (создать, удалить): приказ, предложение и отчёт — шаблонами `actturn`, объект — фразой формы
def _акт_хода(язык, акт, Ф_приказа, Ф):
    приказ_в, инф_в, отчёт_в = A.ГЛАГОЛЫ[язык][акт]
    р = A.РЕЧЬ[язык]
    return (_ф(язык, р["приказ"].format(V=приказ_в, Ф=Ф_приказа)), _ф(язык, р["предложение"].format(V=инф_в, Ф=Ф)),
            _ф(язык, р["отчёт"].format(V=отчёт_в, Ф=Ф)), _ф(язык, РЕЧЬ[язык]["инф_акта"].format(V=инф_в, Ф=Ф)))


def ф_создать(язык, форма, f=None, n=None, d=None):
    """Фраза объекта приказа «создать»: «the file x», «x», «an empty file x», «a new file x», «… in the folder d»."""
    if форма.startswith("папка"):
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "в_папке", int(форма[-1])).format(d=d)
    if форма == "голый":
        return f
    if форма in ("пустой", "новый"):
        return РЕЧЬ[язык][форма].format(f=f)
    return A.РЕЧЬ[язык]["файл"].format(f=f)


def ф_удалить(язык, форма, f=None, n=None, d=None):
    if форма.startswith("папка"):
        return A.РЕЧЬ[язык]["файл"].format(f=n) + " " + _о(язык, "из_папки", int(форма[-1])).format(d=d)
    return f if форма == "голый" else A.РЕЧЬ[язык]["файл"].format(f=f)


def канон(форма):
    """Каноническая форма той же дыры: «голый», «пустой», «новый» → «канон»; «папка·2» → «папка·0»."""
    return "папка·0" if форма.startswith("папка") else "канон"


# ======================================================================================================
# СБОРКИ — части, какие меняются, приходят готовыми (значения дыр, счётные фразы, леджеры); сборка не считает.
# Суд подаёт в них свои метки и получает рамку дома; числа он сверяет своим пересчётом мира.
# ======================================================================================================
def сборка_создать(язык, род, форма, регистр, f, n, d, N, L):
    приказ_, предложение_, отчёт_, _инф = _акт_хода(язык, "создать", ф_создать(язык, форма, f, n, d),
                                                    ф_создать(язык, канон(форма), f, n, d))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N) if форма.startswith("папка") else репо(язык, N), L)
    if род == СОЗДАТЬ_ЕСТЬ:
        причина = A.РЕЧЬ[язык]["есть"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=f))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина, хвост)
    да = род != СОЗДАТЬ_ОТКАЗ
    итог = (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, да, итог)


def сборка_удалить(язык, род, форма, регистр, f, n, d, N, L):
    приказ_, предложение_, отчёт_, _инф = _акт_хода(язык, "удалить", ф_удалить(язык, форма, f, n, d),
                                                    ф_удалить(язык, канон(форма), f, n, d))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N) if форма.startswith("папка") else репо(язык, N), L)
    if род == УДАЛИТЬ_НЕТ:
        причина = A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина, хвост)
    да = род != УДАЛИТЬ_ОТКАЗ
    итог = (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, да, итог)


def _ступени(язык, акт, канон_, форма_=None):
    """(приказ, предложение, отчёт, инфинитив плана) акта двери рук: приказ — частями формы (`форма_` поверх
    канонических), предложение и отчёт — каноническими частями `канон_`."""
    imp = T._ступени(язык, акт, **{**канон_, **(форма_ or {})})[0]
    _imp, inf, zu, past = T._ступени(язык, акт, **канон_)
    return (_ф(язык, imp), _предложение(язык, inf, zu), _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past)), _ф(язык, inf))


def варианты_переноса(язык):
    """Формы приказа переноса: каждое непустое место назначения с каноническим файлом и голое с голым файлом."""
    места = T.ОБЪЕКТЫ[язык]["в_папку"]
    return tuple(f"{0}·{j}" for j in range(len(места)) if j != 1) + ("1·1",)


def _части_переноса(язык, форма, f, d):
    vф, vд = (int(x) for x in форма.split("·"))
    return dict(f=f, d=d), dict(Ф=_о(язык, "файл_вин", vф).format(f=f), Д=_о(язык, "в_папку", vд).format(d=d))


def сборка_переноса(язык, род, форма, регистр, f, d, N, L):
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "перенести", *_части_переноса(язык, форма, f, d))
    хвост = T.наблюдение(язык, T.папка_с_именем(язык, d, N), L)
    if род == ПЕРЕНОС_НЕТ:
        причина = A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина, хвост)
    да = род != ПЕРЕНОС_ОТКАЗ
    итог = (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, да, итог)


def сборка_имени(язык, род, форма, регистр, f, g, N, L):
    приказ_, предложение_, отчёт_, _инф = _ступени(
        язык, "переименовать", dict(f=f, g=g), dict(Фи=_о(язык, "файл_имени", 1 if форма == "голый" else 0).format(f=f)))
    хвост = T.наблюдение(язык, репо(язык, N), L)
    if род in (ИМЯ_ЗАНЯТО, ИМЯ_НЕТ):
        причина = (A.РЕЧЬ[язык]["есть"].format(Ф=A.РЕЧЬ[язык]["файл"].format(f=g)) if род == ИМЯ_ЗАНЯТО
                   else A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f)))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина, хвост)
    да = род != ИМЯ_ОТКАЗ
    итог = (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, да, итог)


def _части_замены(язык, форма, a, b, f):
    """Слово — «the word», несколько слов — «the text»; голая форма — без «the text» и без «the file»."""
    канон_ = dict(w=к(язык, a), v=к(язык, b), f=f, W=_текст(язык, a))
    return канон_, (dict(W=к(язык, a), М=_о(язык, "в_файле", 1).format(f=f)) if форма == "голый" else None)


def _встречается(язык, текст, f, N):
    return _ф(язык, T.РЕЧЬ[язык]["встречается"].format(**T.слоты(язык, f=f, N=N, Wи=_текст(язык, текст, "и"))))


def сборка_замены(язык, род, форма, регистр, a, b, f, N0, L0, N1=None, L1=None):
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "замена", *_части_замены(язык, форма, a, b, f))
    старое = T.наблюдение(язык, _встречается(язык, a, f, N0), L0)
    if род == ЗАМЕНА_НЕТ:
        причина = (_ф(язык, T.РЕЧЬ[язык]["нет_слова"].format(**T.слоты(язык, f=f, Wнет=_текст(язык, a, "нет"))))
                   + " — " + T._хвост_отказа(язык))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина, старое)
    if род == ЗАМЕНА_ОТКАЗ:
        return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, False, _отказ(язык, старое))
    итог = отчёт_ + ". " + старое + " " + T.наблюдение(язык, _встречается(язык, b, f, N1), L1)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, True, итог)


def _части_дописать(язык, форма, s, f):
    канон_ = dict(s=к(язык, s), f=f)
    if форма != "голый":
        return канон_, None
    return канон_, dict(S=_о(язык, "строку", 1).format(s=к(язык, s)), К=_о(язык, "в_файл", 1).format(f=f))


def _строк_в(язык, f, N):
    return T._файл_строк(язык, f, N)


def сборка_дописать(язык, род, форма, регистр, s, f, N, L):
    приказ_, предложение_, отчёт_, _инф = _ступени(язык, "дописать", *_части_дописать(язык, форма, s, f))
    if род == ДОПИСАТЬ_НЕТ:
        причина = A.РЕЧЬ[язык]["пуст"].format(НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
        return T.невозможный(язык, _регистр(язык, регистр, приказ_), причина,
                             T.наблюдение(язык, репо(язык, N), L))
    хвост = T.наблюдение(язык, _строк_в(язык, f, N), L)
    да = род != ДОПИСАТЬ_ОТКАЗ
    итог = (отчёт_ + ". " + хвост) if да else _отказ(язык, хвост)
    return _ход(язык, _регистр(язык, регистр, приказ_), предложение_, да, итог)


def _части_тестов(язык, форма, t=None, я=None):
    if форма == "язык":
        return dict(Т=РЕЧЬ[язык]["тесты_языка"].format(Я=я))
    return dict(t=t, Т=_о(язык, "тесты_файла", 1 if форма == "голый" else 0).format(t=t))


def _канон_тестов(язык, форма, t=None, я=None):
    return _части_тестов(язык, "канон" if форма == "голый" else форма, t, я)


def _исход(язык, П, L0, итог):
    return T.наблюдение(язык, П, L0) + " " + итог + "."


def сборка_прогона(язык, род, форма, регистр, t, я, П, L0, ИСХОД, N, L):
    imp = T._ступени(язык, "тесты", **_части_тестов(язык, форма, t, я))[0]
    _imp, inf, zu, past = T._ступени(язык, "тесты", **_канон_тестов(язык, форма, t, я))
    приказ_ = _регистр(язык, регистр, _ф(язык, imp))
    предложение_ = _предложение(язык, inf, zu)
    запуски = T._запуски(язык, N, L)
    if род == ТЕСТЫ_ОТКАЗ:
        return _ход(язык, приказ_, предложение_, False, _отказ(язык, запуски))
    итог = _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past)) + ". " + _исход(язык, П, L0, ИСХОД) + " " + запуски
    return _ход(язык, приказ_, предложение_, True, итог)


# ПЛАН ИЗ ДВУХ АКТОВ: приказ и предложение — связкой `toolacts.связать`, отчёт — отчёты обоих актов по порядку
def _план(язык, A_, B_):
    """A_, B_ — (приказ, инфинитив) актов; вон — (приказ плана, предложение плана)."""
    приказ_ = _ф(язык, T.связать(язык, "приказ", A_[0], B_[0])) + "."
    предложение_ = _ф(язык, T.связать(язык, "предложение", A_[1], B_[1])) + ". " + T._вопрос_предложения(язык)
    return приказ_, предложение_


def сборка_плана_замены(язык, род, a, b, f, я, N0, L0, N1=None, L1=None, П=None, Lп=None, ИСХОД=None, N=None,
                        L=None):
    приказ_з, _пр, отчёт_з, инф_з = _ступени(язык, "замена", *_части_замены(язык, "канон", a, b, f))
    imp_т, inf_т, _zu, past_т = T._ступени(язык, "тесты", Т=РЕЧЬ[язык]["тесты_языка"].format(Я=я))
    приказ_, предложение_ = _план(язык, (приказ_з, инф_з), (_ф(язык, imp_т), _ф(язык, inf_т)))
    старое = T.наблюдение(язык, _встречается(язык, a, f, N0), L0)
    if род == ПЛАН_ОТКАЗ:
        return _ход(язык, приказ_, предложение_, False, _отказ(язык, старое))
    итог = " ".join((отчёт_з + ".", старое, T.наблюдение(язык, _встречается(язык, b, f, N1), L1),
                     _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past_т)) + ".", _исход(язык, П, Lп, ИСХОД),
                     T._запуски(язык, N, L)))
    return _ход(язык, приказ_, предложение_, True, итог)


def сборка_плана_дописать(язык, род, s, f, я, N0, L0, П=None, Lп=None, ИСХОД=None, N=None, L=None):
    приказ_д, _пр, отчёт_д, инф_д = _ступени(язык, "дописать", *_части_дописать(язык, "канон", s, f))
    imp_т, inf_т, _zu, past_т = T._ступени(язык, "тесты", Т=РЕЧЬ[язык]["тесты_языка"].format(Я=я))
    приказ_, предложение_ = _план(язык, (приказ_д, инф_д), (_ф(язык, imp_т), _ф(язык, inf_т)))
    строки_ = T.наблюдение(язык, _строк_в(язык, f, N0), L0)
    if род == ПЛАН_ОТКАЗ:
        return _ход(язык, приказ_, предложение_, False, _отказ(язык, строки_))
    итог = " ".join((отчёт_д + ".", строки_, _ф(язык, T.РЕЧЬ[язык]["отчёт"].format(past=past_т)) + ".",
                     _исход(язык, П, Lп, ИСХОД), T._запуски(язык, N, L)))
    return _ход(язык, приказ_, предложение_, True, итог)


def сборка_плана_переноса(язык, род, f, d, q, N0, L0, N1=None, L1=None):
    приказ_п, _пр, отчёт_п, инф_п = _ступени(язык, "перенести", *_части_переноса(язык, "0·0", f, d))
    приказ_у, _пу, отчёт_у, инф_у = _акт_хода(язык, "удалить", A.РЕЧЬ[язык]["файл"].format(f=q),
                                               A.РЕЧЬ[язык]["файл"].format(f=q))
    приказ_, предложение_ = _план(язык, (приказ_п, инф_п), (приказ_у, инф_у))
    папка = T.наблюдение(язык, T.папка_с_именем(язык, d, N0), L0)
    if род == ПЛАН_ОТКАЗ:
        return _ход(язык, приказ_, предложение_, False, _отказ(язык, папка))
    итог = " ".join((отчёт_п + ".", папка, отчёт_у + ".", T.наблюдение(язык, репо(язык, N1), L1)))
    return _ход(язык, приказ_, предложение_, True, итог)


# ВОПРОСЫ: вопрос и ответ одной фразой; ответ называет всякую дыру вопроса канонической фразой
def _слоты_вопроса(язык, вариант, f=None, d=None, k=None, текст=None):
    п = {}
    if f is not None:
        п.update(Ф=_о(язык, "файл_вин", вариант).format(f=f), Фр=_о(язык, "файла", вариант).format(f=f),
                 М=_о(язык, "в_файле", вариант).format(f=f), НФ=A.РЕЧЬ[язык]["нет_файла"].format(f=f))
    if d is not None:
        п.update(Дв=_о(язык, "в_папке", вариант).format(d=d))
    if k is not None:
        п.update(K=РЕЧЬ[язык]["ключ"][min(вариант, 1)].format(k=k), Kо=РЕЧЬ[язык]["ключ_о"][min(вариант, 1)].format(k=k))
    if текст is not None:
        if вариант:
            п.update(W=к(язык, текст), Wи=к(язык, текст), Wнет=к(язык, текст))
        else:
            п.update(W=_текст(язык, текст), Wи=_текст(язык, текст, "и"), Wнет=_текст(язык, текст, "нет"))
    п["Р"] = РЕЧЬ[язык]["в_репо"]
    return п


def _q(язык, ключ, **п):
    return _ф(язык, РЕЧЬ[язык][ключ].format(**п))


def _место(язык, текст, f, поз):
    """«the text "x" stands in line 2 of the file f» — позиция у двери `toolacts`, файл — родительным после неё;
    где число встало бы перед существительным, какого оно не считает («в строке 1 файла» читается «1 файла»), —
    файл впереди: «в файле f текст «x» стоит в строке 2»."""
    позиция = T.РЕЧЬ[язык]["позиция"][len(поз) - 1].format(Wи=_текст(язык, текст, "и"), a=поз[0], b=поз[-1])
    return _ф(язык, РЕЧЬ[язык]["место"].format(позиция=позиция, Фр=_о(язык, "файла").format(f=f),
                                               М=_о(язык, "в_файле").format(f=f)))


def сборка_вопроса(язык, род, вариант, **д):
    """Вопрос рода с дырами `д` и ответ; числа и найденное (путь, строка, значение) приходят готовыми в `д`."""
    с = _слоты_вопроса(язык, вариант, f=д.get("f"), d=д.get("d"), k=д.get("k"), текст=д.get("w"))
    с0 = _слоты_вопроса(язык, 0, f=д.get("найден", д.get("f")), d=д.get("папка", д.get("d")), k=д.get("k"),
                        текст=д.get("w"))
    if род in (В_КАКОМ, НИГДЕ):
        вопрос = _q(язык, "q_файл", **с)
        ответ = _q(язык, "нигде", **с0) if род == НИГДЕ else _место(язык, д["w"], д["найден"], д["поз"])
    elif род == НА_СТРОКЕ:
        вопрос, ответ = _q(язык, "q_строка", **с), _место(язык, д["w"], д["f"], д["поз"])
    elif род in (ПЕРВАЯ, ПОСЛЕДНЯЯ):
        вопрос = _q(язык, "q_первая" if род == ПЕРВАЯ else "q_последняя", **с)
        ответ = _q(язык, "читается", a=д["a"], T=к(язык, д["T"]), **с0)
    elif род == КЛЮЧ:
        вопрос = _q(язык, "q_ключ", **{**с, "М": _о(язык, "в_файле", вариант).format(f=д["s"])})
        ответ = _q(язык, "ключ_ответ", v=д["v"], **{**с0, "М": _о(язык, "в_файле").format(f=д["s"])})
    elif род == СТРОК:
        вопрос = _q(язык, "q_строк", **с)
        ответ = T.наблюдение(язык, _строк_в(язык, д["f"], д["N"]), д["L"])
    elif род == РАЗ_В_РЕПО:
        вопрос = _ф(язык, T.РЕЧЬ[язык]["вопрос_раз"].format(Wи=_текст(язык, д["w"], "и"), М=РЕЧЬ[язык]["в_репо"]))
        ответ = T.наблюдение(язык, _ф(язык, T.РЕЧЬ[язык]["встречается"].format(
            Wи=_текст(язык, д["w"], "и"), М=РЕЧЬ[язык]["в_репо"], N=д["N"])), д["L"])
    elif род == ФАЙЛОВ:
        вопрос = _q(язык, "q_папка", **с)
        ответ = T.наблюдение(язык, T.папка_с_именем(язык, д["d"], д["N"]), д["L"])
    elif род in (ГДЕ, ГДЕ_НЕТ):
        с = _слоты_вопроса(язык, вариант, f=д["n"])
        вопрос = _q(язык, "q_где", **с)
        с0 = _слоты_вопроса(язык, 0, f=д["n"], d=д.get("папка"))
        ответ = _q(язык, "где_ответ" if род == ГДЕ else "нет_в_репо", **с0)
    else:
        raise ValueError(род)
    if not ответ.endswith("."):
        ответ += "."
    return T.вопрос_и_наблюдение(язык, вопрос, ответ)


# ======================================================================================================
# СТРАНИЦЫ — обёртки считают мир и отдают сборке готовые части
# ======================================================================================================
def _л(было, сдвиг):
    return A.леджер(было, сдвиг)


def страница_создать(язык, род, форма, регистр, f=None, n=None, d=None):
    if форма.startswith("папка"):
        было = файлов_в_папке(d)
    else:
        было = len(ПУТИ)
    счёт, стало = _л(было, 1 if род == СОЗДАТЬ else 0)
    return сборка_создать(язык, род, форма, регистр, f, n, d, A.файлов(язык, стало), счёт)


def страница_удалить(язык, род, форма, регистр, f=None, n=None, d=None):
    было = файлов_в_папке(d) if форма.startswith("папка") else len(ПУТИ)
    счёт, стало = _л(было, -1 if род == УДАЛИТЬ else 0)
    return сборка_удалить(язык, род, форма, регистр, f, n, d, A.файлов(язык, стало), счёт)


def страница_переноса(язык, род, форма, регистр, f, d):
    было = файлов_в_папке(d)
    счёт, стало = _л(было, 1 if род == ПЕРЕНОС else 0)
    return сборка_переноса(язык, род, форма, регистр, f, d, A.файлов(язык, стало), счёт)


def страница_имени(язык, род, форма, регистр, f, g):
    счёт, стало = _л(len(ПУТИ), 0)
    return сборка_имени(язык, род, форма, регистр, f, g, A.файлов(язык, стало), счёт)


def страница_замены(язык, род, форма, регистр, f, a, b):
    k, x = в_файле(язык, f, a), в_файле(язык, f, b)
    if род == ЗАМЕНА_НЕТ:
        return сборка_замены(язык, род, форма, регистр, a, b, f, T.раз(язык, 0), _л(0, 0)[0])
    if род == ЗАМЕНА_ОТКАЗ:
        return сборка_замены(язык, род, форма, регистр, a, b, f, T.раз(язык, k), _л(k, 0)[0])
    return сборка_замены(язык, род, форма, регистр, a, b, f, T.раз(язык, 0), _л(k, -k)[0], T.раз(язык, x + k),
                         _л(x, k)[0])


def страница_дописать(язык, род, форма, регистр, f, s):
    if род == ДОПИСАТЬ_НЕТ:
        счёт, стало = _л(len(ПУТИ), 0)
        return сборка_дописать(язык, род, форма, регистр, s, f, A.файлов(язык, стало), счёт)
    счёт, стало = _л(len(строки_файла(язык, f)), 1 if род == ДОПИСАТЬ else 0)
    return сборка_дописать(язык, род, форма, регистр, s, f, T.строк(язык, стало), счёт)


def исход(язык, всего, падает, фраза="итог"):
    """(«6 of 7 tests passed», «7 − 1 = 6», исход) — из объявления мира, фразами двери `toolacts`."""
    return (T.прошло(язык, всего - падает, всего), _л(всего, -падает)[0],
            _ф(язык, T.РЕЧЬ[язык][фраза][0 if падает == 0 else 1]))


def страница_прогона(язык, род, форма, регистр, было, t=None, я=None):
    всего, падает = тесты_языка(я) if форма == "язык" else тесты_файла(t)
    П, L0, ИСХОД = исход(язык, всего, падает)
    счёт, стало = _л(было, 0 if род == ТЕСТЫ_ОТКАЗ else 1)
    return сборка_прогона(язык, род, форма, регистр, t, я, П, L0, ИСХОД, A.запусков(язык, стало), счёт)


def страница_плана_замены(язык, род, f, a, b, я, было):
    k, x = в_файле(язык, f, a), в_файле(язык, f, b)
    if род == ПЛАН_ОТКАЗ:
        return сборка_плана_замены(язык, род, a, b, f, я, T.раз(язык, k), _л(k, 0)[0])
    П, Lп, ИСХОД = исход(язык, *тесты_языка(я))
    счёт, стало = _л(было, 1)
    return сборка_плана_замены(язык, род, a, b, f, я, T.раз(язык, 0), _л(k, -k)[0], T.раз(язык, x + k), _л(x, k)[0],
                               П, Lп, ИСХОД, A.запусков(язык, стало), счёт)


def страница_плана_дописать(язык, род, f, s, я, было):
    n = len(строки_файла(язык, f))
    счёт0, стало0 = _л(n, 0 if род == ПЛАН_ОТКАЗ else 1)
    if род == ПЛАН_ОТКАЗ:
        return сборка_плана_дописать(язык, род, s, f, я, T.строк(язык, стало0), счёт0)
    П, Lп, ИСХОД = исход(язык, *тесты_языка(я))
    счёт, стало = _л(было, 1)
    return сборка_плана_дописать(язык, род, s, f, я, T.строк(язык, стало0), счёт0, П, Lп, ИСХОД,
                                 A.запусков(язык, стало), счёт)


def страница_плана_переноса(язык, род, f, d, q):
    было = файлов_в_папке(d)
    счёт0, стало0 = _л(было, 0 if род == ПЛАН_ОТКАЗ else 1)
    if род == ПЛАН_ОТКАЗ:
        return сборка_плана_переноса(язык, род, f, d, q, A.файлов(язык, стало0), счёт0)
    счёт1, стало1 = _л(len(ПУТИ), -1)
    return сборка_плана_переноса(язык, род, f, d, q, A.файлов(язык, стало0), счёт0, A.файлов(язык, стало1), счёт1)


def страница_вопроса(язык, род, вариант, **д):
    """Обёртка вопросов: находит в мире путь, строку, значение, число — и подаёт сборке."""
    if род == В_КАКОМ:
        (найден,) = файлы_с(язык, д["w"])
        д.update(найден=найден, поз=строки_с(язык, найден, д["w"]))
    elif род == НИГДЕ:
        assert not файлы_с(язык, д["w"]), (язык, д)
    elif род == НА_СТРОКЕ:
        д.update(поз=строки_с(язык, д["f"], д["w"]))
    elif род in (ПЕРВАЯ, ПОСЛЕДНЯЯ):
        строки_ = строки_файла(язык, д["f"])
        i = 0 if род == ПЕРВАЯ else len(строки_) - 1
        д.update(a=i + 1, T=строки_[i])
    elif род == КЛЮЧ:
        д.update(v=значение_ключа(д["s"], д["k"]))
    elif род == СТРОК:
        n = len(строки_файла(язык, д["f"]))
        д.update(N=T.строк(язык, n), L=_л(n, 0)[0])
    elif род == РАЗ_В_РЕПО:
        по_файлам = [в_файле(язык, п, д["w"]) for п in ПУТИ if в_файле(язык, п, д["w"])]
        д.update(N=T.раз(язык, sum(по_файлам)), L=цепь(по_файлам))
    elif род == ФАЙЛОВ:
        n = файлов_в_папке(д["d"])
        д.update(N=A.файлов(язык, n), L=_л(n, 0)[0])
    elif род == ГДЕ:
        (путь,) = [п for п in ПУТИ if имя_пути(п) == д["n"]]
        д.update(папка=папка_пути(путь))
    return сборка_вопроса(язык, род, вариант, **д)


def цепь(слагаемые):
    """«1 + 2 = 3» — счёт по файлам в порядке путей; одно слагаемое — «2 = 2», как у равенства леджера."""
    return " + ".join(str(x) for x in слагаемые) + f" = {sum(слагаемые)}"


# ======================================================================================================
# ПОКАЗЫ: всякая форма приказа и вопроса — на всяком языке, не меньше двух страниц с разными наполнителями
# ======================================================================================================
def _варианты_папки(язык, фраза):
    return range(len(T.ОБЪЕКТЫ[язык][фраза]))


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
        for форма, срез in (("голый", slice(0, 4)), ("пустой", slice(2, 6)), ("новый", slice(4, 8))):
            for f in СОЗДАТЬ_ПУТИ[срез]:
                положить(страница_создать(язык, СОЗДАТЬ, форма, п_, f=f), язык, СОЗДАТЬ, форма, п_, {"f": f})
        for f in СОЗДАТЬ_ПУТИ[1::2]:
            положить(страница_создать(язык, СОЗДАТЬ, "канон", в_, f=f), язык, СОЗДАТЬ, "канон", в_, {"f": f})
        for v in _варианты_папки(язык, "в_папке"):
            пары = СОЗДАТЬ_В_ПАПКЕ if v == 0 else СОЗДАТЬ_В_ПАПКЕ[v - 1::2]
            for n, d in пары:
                положить(страница_создать(язык, СОЗДАТЬ, f"папка·{v}", п_, n=n, d=d), язык, СОЗДАТЬ_ПАПКА,
                         f"папка·{v}", п_, {"n": n, "d": d})
        for f in ("shopping.txt", "home/chores.md", "kitchen/soup.md"):
            положить(страница_создать(язык, СОЗДАТЬ_ЕСТЬ, "канон", п_, f=f), язык, СОЗДАТЬ_ЕСТЬ, "канон", п_, {"f": f})
        for f in СОЗДАТЬ_ПУТИ[0::3][:2]:
            положить(страница_создать(язык, СОЗДАТЬ_ОТКАЗ, "канон", п_, f=f), язык, СОЗДАТЬ_ОТКАЗ, "канон", п_, {"f": f})
        # УДАЛИТЬ
        for f in ТЕКСТЫ:
            положить(страница_удалить(язык, УДАЛИТЬ, "канон", п_, f=f), язык, УДАЛИТЬ, "канон", п_, {"f": f})
        for f in ТЕКСТЫ[:4]:
            положить(страница_удалить(язык, УДАЛИТЬ, "голый", п_, f=f), язык, УДАЛИТЬ, "голый", п_, {"f": f})
        for f in ТЕКСТЫ[4:]:
            положить(страница_удалить(язык, УДАЛИТЬ, "канон", в_, f=f), язык, УДАЛИТЬ, "канон", в_, {"f": f})
        for v in _варианты_папки(язык, "из_папки"):
            for n, d in (УДАЛИТЬ_ИЗ_ПАПКИ if v == 0 else УДАЛИТЬ_ИЗ_ПАПКИ[1::2]):
                положить(страница_удалить(язык, УДАЛИТЬ, f"папка·{v}", п_, n=n, d=d), язык, УДАЛИТЬ_ПАПКА,
                         f"папка·{v}", п_, {"n": n, "d": d})
        for f in НЕТ_ФАЙЛОВ:
            положить(страница_удалить(язык, УДАЛИТЬ_НЕТ, "канон", п_, f=f), язык, УДАЛИТЬ_НЕТ, "канон", п_, {"f": f})
        for f in (ТЕКСТЫ[1], ТЕКСТЫ[6]):
            положить(страница_удалить(язык, УДАЛИТЬ_ОТКАЗ, "канон", п_, f=f), язык, УДАЛИТЬ_ОТКАЗ, "канон", п_,
                     {"f": f})
        # ПЕРЕНЕСТИ: каноническая форма — все пары, прочие — по четыре пары со сдвигом
        формы = варианты_переноса(язык)
        for i, форма in enumerate(формы):
            пары = ПЕРЕНОСЫ if i == 0 else [ПЕРЕНОСЫ[(i + 2 * j) % len(ПЕРЕНОСЫ)] for j in range(4)]
            for f, d in пары:
                положить(страница_переноса(язык, ПЕРЕНОС, форма, п_, f, d), язык, ПЕРЕНОС, форма, п_,
                         {"f": f, "d": d})
        for f, d in ПЕРЕНОСЫ[1::2]:
            положить(страница_переноса(язык, ПЕРЕНОС, формы[0], в_, f, d), язык, ПЕРЕНОС, формы[0], в_, {"f": f, "d": d})
        for f, d in zip(НЕТ_ФАЙЛОВ, ("backup", "kitchen")):
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
        for род, пары in ((ИМЯ_ЗАНЯТО, ИМЕНА_ЗАНЯТЫ), (ИМЯ_НЕТ, ИМЕНА_НЕТ), (ИМЯ_ОТКАЗ, (ИМЕНА[3], ИМЕНА[6]))):
            for f, g in пары:
                положить(страница_имени(язык, род, "канон", п_, f, g), язык, род, "канон", п_, {"f": f, "g": g})
        # ЗАМЕНИТЬ: текст из нескольких слов — «the text» и голым; слово — «the word»
        for i, f in enumerate(ТЕКСТЫ):
            _строки, (a, b), (w, v), _s = с[f]
            дыры = {"a": к(язык, a), "b": к(язык, b), "f": f}
            положить(страница_замены(язык, ЗАМЕНА, "текст", п_, f, a, b), язык, ЗАМЕНА, "текст", п_, дыры)
            if i % 2 == 0:
                положить(страница_замены(язык, ЗАМЕНА, "голый", п_, f, a, b), язык, ЗАМЕНА, "голый", п_, дыры)
            else:
                положить(страница_замены(язык, ЗАМЕНА, "текст", в_, f, a, b), язык, ЗАМЕНА, "текст", в_, дыры)
            положить(страница_замены(язык, ЗАМЕНА_СЛОВА, "слово", п_, f, w, v), язык, ЗАМЕНА_СЛОВА, "слово", п_,
                     {"a": к(язык, w), "b": к(язык, v), "f": f})
        for i, (f, a) in enumerate(zip((ТЕКСТЫ[0], ТЕКСТЫ[5]), НЕТ_ТЕКСТА[язык])):
            b = с[f][1][1]
            положить(страница_замены(язык, ЗАМЕНА_НЕТ, "текст", п_, f, a, b), язык, ЗАМЕНА_НЕТ, "текст", п_,
                     {"a": к(язык, a), "b": к(язык, b), "f": f})
        for f in (ТЕКСТЫ[2], ТЕКСТЫ[7]):
            a, b = с[f][1]
            положить(страница_замены(язык, ЗАМЕНА_ОТКАЗ, "текст", п_, f, a, b), язык, ЗАМЕНА_ОТКАЗ, "текст", п_,
                     {"a": к(язык, a), "b": к(язык, b), "f": f})
        # ДОПИСАТЬ
        for i, f in enumerate(ТЕКСТЫ):
            s = с[f][3]
            положить(страница_дописать(язык, ДОПИСАТЬ, "канон", п_, f, s), язык, ДОПИСАТЬ, "канон", п_,
                     {"s": к(язык, s), "f": f})
            форма, регистр = ("голый", п_) if i % 2 else ("канон", в_)
            положить(страница_дописать(язык, ДОПИСАТЬ, форма, регистр, f, s), язык, ДОПИСАТЬ, форма, регистр,
                     {"s": к(язык, s), "f": f})
        for f, из in zip(НЕТ_ФАЙЛОВ, (ТЕКСТЫ[3], ТЕКСТЫ[4])):
            s = с[из][3]
            положить(страница_дописать(язык, ДОПИСАТЬ_НЕТ, "канон", п_, f, s), язык, ДОПИСАТЬ_НЕТ, "канон", п_,
                     {"s": к(язык, s), "f": f})
        for f in (ТЕКСТЫ[0], ТЕКСТЫ[5]):
            s = с[f][3]
            положить(страница_дописать(язык, ДОПИСАТЬ_ОТКАЗ, "канон", п_, f, s), язык, ДОПИСАТЬ_ОТКАЗ, "канон", п_,
                     {"s": к(язык, s), "f": f})
        # ТЕСТЫ: по языку проекта и по файлу тестов
        for я in ЯЗЫКИ_ПРОЕКТА:
            for было in ЗАПУСКИ_ДО:
                положить(страница_прогона(язык, ТЕСТЫ_ЯЗЫКА, "язык", п_, было, я=я), язык, ТЕСТЫ_ЯЗЫКА, "язык", п_,
                         {"Я": я})
            положить(страница_прогона(язык, ТЕСТЫ_ЯЗЫКА, "язык", в_, ЗАПУСКИ_ДО[1], я=я), язык, ТЕСТЫ_ЯЗЫКА, "язык",
                     в_, {"Я": я})
        for i, t in enumerate(ФАЙЛЫ_ТЕСТОВ):
            for было in ЗАПУСКИ_ДО[:2]:
                положить(страница_прогона(язык, ТЕСТЫ_ФАЙЛА, "канон", п_, было, t=t), язык, ТЕСТЫ_ФАЙЛА, "канон", п_,
                         {"t": t})
            положить(страница_прогона(язык, ТЕСТЫ_ФАЙЛА, "голый", п_, ЗАПУСКИ_ДО[i % 3], t=t), язык, ТЕСТЫ_ФАЙЛА,
                     "голый", п_, {"t": t})
        положить(страница_прогона(язык, ТЕСТЫ_ОТКАЗ, "язык", п_, 1, я="Python"), язык, ТЕСТЫ_ОТКАЗ, "язык", п_,
                 {"Я": "Python"})
        положить(страница_прогона(язык, ТЕСТЫ_ОТКАЗ, "канон", п_, 0, t=ФАЙЛЫ_ТЕСТОВ[1]), язык, ТЕСТЫ_ОТКАЗ, "канон",
                 п_, {"t": ФАЙЛЫ_ТЕСТОВ[1]})
        # ПЛАНЫ ИЗ ДВУХ АКТОВ
        языки_проекта = tuple(ЯЗЫКИ_ПРОЕКТА)
        for i, f in enumerate(ТЕКСТЫ):
            a, b = с[f][1]
            я = языки_проекта[i % 2]
            было = ЗАПУСКИ_ДО[i % 3]
            положить(страница_плана_замены(язык, ПЛАН_ЗАМЕНА, f, a, b, я, было), язык, ПЛАН_ЗАМЕНА, "замена", п_,
                     {"a": к(язык, a), "b": к(язык, b), "f": f, "Я": я})
            я2 = языки_проекта[(i + 1) % 2]
            положить(страница_плана_дописать(язык, ПЛАН_ДОПИСАТЬ, f, с[f][3], я2, ЗАПУСКИ_ДО[(i + 1) % 3]), язык,
                     ПЛАН_ДОПИСАТЬ, "дописать", п_, {"s": к(язык, с[f][3]), "f": f, "Я": я2})
            f2, d = ПЕРЕНОСЫ[i]
            q = ТЕКСТЫ[(i + 3) % len(ТЕКСТЫ)]
            положить(страница_плана_переноса(язык, ПЛАН_ПЕРЕНОС, f2, d, q), язык, ПЛАН_ПЕРЕНОС, "перенос", п_,
                     {"f": f2, "d": d, "q": q})
        a, b = с[ТЕКСТЫ[1]][1]
        положить(страница_плана_замены(язык, ПЛАН_ОТКАЗ, ТЕКСТЫ[1], a, b, "Rust", 0), язык, ПЛАН_ОТКАЗ, "замена", п_,
                 {"a": к(язык, a), "b": к(язык, b), "f": ТЕКСТЫ[1], "Я": "Rust"})
        положить(страница_плана_дописать(язык, ПЛАН_ОТКАЗ, ТЕКСТЫ[2], с[ТЕКСТЫ[2]][3], "Python", 0), язык, ПЛАН_ОТКАЗ,
                 "дописать", п_, {"s": к(язык, с[ТЕКСТЫ[2]][3]), "f": ТЕКСТЫ[2], "Я": "Python"})
        положить(страница_плана_переноса(язык, ПЛАН_ОТКАЗ, *ПЕРЕНОСЫ[3], ТЕКСТЫ[0]), язык, ПЛАН_ОТКАЗ, "перенос", п_,
                 {"f": ПЕРЕНОСЫ[3][0], "d": ПЕРЕНОСЫ[3][1], "q": ТЕКСТЫ[0]})
        # ВОПРОСЫ
        def вопрос(род, вариант, форма, дыры, **д):
            положить(страница_вопроса(язык, род, вариант, **д), язык, род, форма, п_, дыры)

        def форма_текста(текст, вариант):
            return "голый" if вариант else ("слово" if len(текст.split()) == 1 else "текст")

        уникальные_слова = [с[f][2][0] for f in ТЕКСТЫ if len(файлы_с(язык, с[f][2][0])) == 1]
        for i, f in enumerate(ТЕКСТЫ):
            a = с[f][1][0]
            вопрос(В_КАКОМ, 0, "текст", {"w": к(язык, a)}, w=a)
            if i % 2:
                вопрос(В_КАКОМ, 1, "голый", {"w": к(язык, a)}, w=a)
            вопрос(НА_СТРОКЕ, 0, "текст", {"f": f, "w": к(язык, a)}, f=f, w=a)
            if i % 2 == 0:
                вопрос(НА_СТРОКЕ, 1, "голый", {"f": f, "w": к(язык, a)}, f=f, w=a)
            вопрос(ПЕРВАЯ, 0, "канон", {"f": f}, f=f)
            вопрос(ПОСЛЕДНЯЯ, 0, "канон", {"f": f}, f=f)
            if i % 2:
                вопрос(ПЕРВАЯ, 1, "голый", {"f": f}, f=f)
            else:
                вопрос(ПОСЛЕДНЯЯ, 1, "голый", {"f": f}, f=f)
            вопрос(СТРОК, 0, "канон", {"f": f}, f=f)
        for w in уникальные_слова:
            вопрос(В_КАКОМ, 0, "слово", {"w": к(язык, w)}, w=w)
        for w in СЛОВА_РЕПО[язык]:
            первый = файлы_с(язык, w)[0]
            вопрос(НА_СТРОКЕ, 0, "слово", {"f": первый, "w": к(язык, w)}, f=первый, w=w)
            вопрос(РАЗ_В_РЕПО, 0, "слово", {"w": к(язык, w)}, w=w)
        for a in НЕТ_ТЕКСТА[язык]:
            вопрос(НИГДЕ, 0, форма_текста(a, 0), {"w": к(язык, a)}, w=a)
        for i, (s, k_) in enumerate(КЛЮЧИ):
            вопрос(КЛЮЧ, 0, "канон", {"k": k_, "s": s}, s=s, k=k_)
            вопрос(КЛЮЧ, 1, "голый", {"k": k_, "s": s}, s=s, k=k_)
        for f in ("web/main.py", "tests/test_main.py", "tally/src/lib.rs", "server.ini"):
            вопрос(СТРОК, 0, "канон", {"f": f}, f=f)
        for f in ТЕКСТЫ[1::2]:
            вопрос(СТРОК, 1, "голый", {"f": f}, f=f)
        for v in _варианты_папки(язык, "в_папке"):
            for d in (ПАПКИ_СЧЁТА if v == 0 else ПАПКИ_СЧЁТА[v - 1::2]):
                вопрос(ФАЙЛОВ, v, f"папка·{v}", {"d": d}, d=d)
        имена = [имя_пути(п) for п in ПУТИ if "/" in п]
        for i, n in enumerate(имена):
            вопрос(ГДЕ, 0, "канон", {"n": n}, n=n)
            if i % 3 == 0:
                вопрос(ГДЕ, 1, "голый", {"n": n}, n=n)
        for n in НЕТ_ФАЙЛОВ:
            вопрос(ГДЕ_НЕТ, 0, "канон", {"n": n}, n=n)
    return вон, перепись


ПОКАЗЫ, ПЕРЕПИСЬ = _показы()


# ======================================================================================================
# САМОПРОВЕРКИ: мир объявлен так, как дом о нём говорит; условия рынка М-2013 держатся на всяком языке
# ======================================================================================================
def _самопроверка_мира():
    import frgram  # noqa: PLC0415 — французское сокращение не должно съесть имя пути
    for язык in ЯЗЫКИ:
        for f in ТЕКСТЫ:
            строки_, (a, b), (w, v), s = СОДЕРЖИМОЕ[язык][f]
            assert 3 <= len(строки_) <= 4, (язык, f)
            assert файлы_с(язык, a) == [f] and в_файле(язык, f, a) == 1, (язык, f, a)
            assert в_файле(язык, f, b) == 0 and в_файле(язык, f, w) > 0 and в_файле(язык, f, v) == 0, (язык, f)
            assert s not in строки_, (язык, f, s)
            for текст in строки_ + (a, b, w, v, s):
                assert not re.search(r"[\d.:?!«»„“”\"]", текст), (язык, f, текст)
        assert all(not файлы_с(язык, a) for a in НЕТ_ТЕКСТА[язык]), язык
        for w in СЛОВА_РЕПО[язык]:
            assert файлы_с(язык, w) and len(строки_с(язык, файлы_с(язык, w)[0], w)) <= 2, (язык, w)
    for f in СОЗДАТЬ_ПУТИ + НЕТ_ФАЙЛОВ:
        assert f not in ПУТИ, f
    for n, d in СОЗДАТЬ_В_ПАПКЕ:
        assert f"{d}/{n}" not in ПУТИ and файлов_в_папке(d), (n, d)
    for n, d in УДАЛИТЬ_ИЗ_ПАПКИ:
        assert f"{d}/{n}" in ПУТИ, (n, d)
    for f, g in ИМЕНА:
        assert f in ПУТИ and (f"{папка_пути(f)}/{g}".lstrip("/") not in ПУТИ), (f, g)
    for f, g in ИМЕНА_ЗАНЯТЫ:
        assert f in ПУТИ and f"{папка_пути(f)}/{g}".lstrip("/") in ПУТИ, (f, g)
    for f, _g in ИМЕНА_НЕТ:
        assert f not in ПУТИ, f
    for f, d in ПЕРЕНОСЫ:
        assert f in ПУТИ and папка_пути(f) != d, (f, d)
    имена = [имя_пути(п) for п in ПУТИ if "/" in п]
    assert len(имена) == len(set(имена)), имена
    for s, k_ in КЛЮЧИ:
        assert значение_ключа(s, k_) is not None and значение_ключа(s, k_).isdigit(), (s, k_)
    # ИМЕНА ДОМА НЕ ВСТРЕЧАЮТСЯ У СОСЕДЕЙ: суд дома узнаёт свою строку по имени её мира
    свои = set(ПУТИ) | set(СОЗДАТЬ_ПУТИ) | set(НЕТ_ФАЙЛОВ) | {g for _f, g in ИМЕНА + ИМЕНА_НЕТ} | set(имена)
    чужие = set(A.ФАЙЛЫ) | set(T.ТЕКСТЫ) | set(T.ТЕСТЫ) | set(T.НЕТ_ФАЙЛА) | {
        g for гг in T.НОВЫЕ_ИМЕНА.values() for g in гг}
    assert not свои & чужие, свои & чужие
    # французское «de» перед именем не сокращается («d'app/…» разорвал бы дыру имени)
    for имя in свои | {d for _f, d in ПЕРЕНОСЫ} | set(ПАПКИ_СЧЁТА):
        assert frgram.элизия(f"de {имя}") == f"de {имя}", имя
    # исход тестов Python объявлен и ПРОВЕРЕН исполнением: падают ровно объявленные
    код = {}
    exec("\n".join(ПРОЕКТ["web/helpers.py"]), код)  # noqa: S102 — свой код мира, без ввода извне
    for ф in ФАЙЛЫ_ТЕСТОВ:
        if not ф.endswith(".py"):
            continue
        пространство = {"greet": код["greet"]}
        exec("\n".join(с for с in ПРОЕКТ[ф] if not с.startswith("from ")), пространство)  # noqa: S102
        упали = []
        for имя, функция in пространство.items():
            if имя.startswith("test_"):
                try:
                    функция()
                except AssertionError:
                    упали.append(имя)
        assert tuple(упали) == ПАДАЮТ.get(ф, ()), (ф, упали)


_самопроверка_мира()


def _слова_органа(текст):
    """Слова, какими приказ режет орган: пробельные слова с обрезанными краевыми знаками."""
    return {с.strip(".,:;?!¿¡") for с in текст.split()}


def _итог(стр, язык):
    """Итог страницы — последняя реплика организма (отчёт, ход «нет / уже есть», ответ)."""
    return стр.rsplit(A._реплика(язык, "орг", ""), 1)[1]


def _приказ(стр, язык):
    return стр.split(A._реплика(язык, "орг", ""), 1)[0]


# ФОРМА ПРИКАЗА у отказа и невозможного — форма исполненного того же акта: отказ ложится в её рамку (М-2013, 5)
_ПОРЯДОК = {СОЗДАТЬ_ЕСТЬ: СОЗДАТЬ, СОЗДАТЬ_ОТКАЗ: СОЗДАТЬ, УДАЛИТЬ_НЕТ: УДАЛИТЬ, УДАЛИТЬ_ОТКАЗ: УДАЛИТЬ,
            ПЕРЕНОС_НЕТ: ПЕРЕНОС, ПЕРЕНОС_ОТКАЗ: ПЕРЕНОС, ИМЯ_ЗАНЯТО: ИМЯ, ИМЯ_НЕТ: ИМЯ, ИМЯ_ОТКАЗ: ИМЯ,
            ЗАМЕНА_НЕТ: ЗАМЕНА, ЗАМЕНА_ОТКАЗ: ЗАМЕНА, ДОПИСАТЬ_НЕТ: ДОПИСАТЬ, ДОПИСАТЬ_ОТКАЗ: ДОПИСАТЬ,
            НИГДЕ: В_КАКОМ, ГДЕ_НЕТ: ГДЕ}
_ПОРЯДОК_ПО_ФОРМЕ = {(ТЕСТЫ_ОТКАЗ, "язык"): ТЕСТЫ_ЯЗЫКА, (ТЕСТЫ_ОТКАЗ, "канон"): ТЕСТЫ_ФАЙЛА,
                     (ПЛАН_ОТКАЗ, "замена"): ПЛАН_ЗАМЕНА, (ПЛАН_ОТКАЗ, "дописать"): ПЛАН_ДОПИСАТЬ,
                     (ПЛАН_ОТКАЗ, "перенос"): ПЛАН_ПЕРЕНОС}


def форма_приказа(род, форма):
    """Род, чья форма приказа у страницы: исполненный акт для отказа и невозможного, сам род — для прочих."""
    return _ПОРЯДОК_ПО_ФОРМЕ.get((род, форма), _ПОРЯДОК.get(род, род))


def условия_рынка():
    """Условия М-2013 по показам: (беды, счёт форм). Итог называет всякую дыру; у всякой формы приказа и языка —
    пара исполненных страниц с разными наполнителями на всех местах; исполненных больше, чем отказов той же формы."""
    беды = []
    исполненные, отказы, прочие = {}, {}, {}
    for стр, (язык, род, форма, регистр) in ПОКАЗЫ.items():
        дыры = ПЕРЕПИСЬ[стр]
        приказ_ = _приказ(стр, язык)
        for имя, знач in дыры.items():
            if знач.startswith(T.КАВЫЧКИ[язык][0]):
                if знач not in приказ_:
                    беды.append(f"дыра {имя} не в приказе: {стр[:120]}")
            elif знач not in _слова_органа(приказ_):
                беды.append(f"дыра {имя} не слово приказа: {стр[:120]}")
        ключ = (язык, форма_приказа(род, форма), форма, регистр)
        if род in ОТКАЗЫ:
            отказы.setdefault(ключ, []).append(дыры)
            continue
        if род in НЕВОЗМОЖНЫЕ:
            прочие.setdefault(ключ, []).append(дыры)
            continue
        итог = _итог(стр, язык)
        for имя, знач in дыры.items():
            есть = знач in итог if знач.startswith(T.КАВЫЧКИ[язык][0]) else знач in _слова_органа(итог)
            if not есть:
                беды.append(f"итог не называет дыру {имя}={знач}: {стр[:140]}")
        исполненные.setdefault(ключ, []).append(дыры)
    for ключ, члены in исполненные.items():
        if not any(all(x[и] != y[и] for и in x) for i, x in enumerate(члены) for y in члены[i + 1:]):
            беды.append(f"нет пары с разными наполнителями: {ключ} ({len(члены)} стр.)")
    for ключ in list(отказы) + list(прочие):
        if len(исполненные.get(ключ, ())) < 2:
            беды.append(f"отказ или невозможное без рамки исполненных: {ключ}")
    for ключ, члены in отказы.items():
        if len(исполненные.get(ключ, ())) <= len(члены):
            беды.append(f"отказов не меньше исполненных: {ключ}")
    # английский глагол приказа не равен форме отчёта — у всякого акта дома
    for акт in ("создать", "удалить"):
        приказ_в, _инф, отчёт_в = A.ГЛАГОЛЫ["en"][акт]
        assert приказ_в != отчёт_в, акт
    for акт in ("замена", "дописать", "переименовать", "перенести", "тесты"):
        imp, _inf, past = T.РЕЧЬ["en"][акт][:3]
        assert imp.split()[0] != past.split()[0], акт
    return беды, len(исполненные)


def _самопроверка():
    import asking  # noqa: PLC0415 — дом пары объявляет зачины вопросов
    по_роду = {}
    for стр, (язык, род, _ф_, _р_) in ПОКАЗЫ.items():
        по_роду.setdefault(род, set()).add(язык)
        for фраза in re.split(r"(?<=[.?!])\s+", стр):
            вопрос = re.sub(r"^[^\s:]+ ?: ", "", фраза.strip())
            if вопрос.endswith("?") and asking.зачин_объявлен(вопрос) is False:
                raise AssertionError(f"незачинный вопрос: {язык} · {вопрос}")
    пустые = [р for р in РОДЫ if по_роду.get(р) != set(ЯЗЫКИ)]
    assert not пустые, f"род не кован на всех языках: {пустые}"
    беды, форм = условия_рынка()
    for б in беды[:12]:
        print("  М-2013:", б)
    assert not беды, f"условий рынка нарушено {len(беды)}"
    for язык in ("en", "ru", "de", "fr", "nl"):
        for стр, (я, род, форма, р) in ПОКАЗЫ.items():
            if я == язык and род in (ЗАМЕНА, ПЕРЕНОС, КЛЮЧ, ПЛАН_ЗАМЕНА) and форма in ("текст", "0·0", "канон", "замена"):
                print("  ", стр)
    сч = {р: sum(1 for _я, род, _ф_, _р_ in ПОКАЗЫ.values() if род == р) for р in РОДЫ}
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}, форм на языках {форм}): "
          + ", ".join(f"{р} {к_}" for р, к_ in сч.items()))


if __name__ == "__main__":
    _самопроверка()
