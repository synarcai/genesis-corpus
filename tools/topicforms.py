#!/usr/bin/env python3
"""ДОМ БЫТОВЫХ ТЕМ — то, о чём человек спрашивает первым делом.

Заказ владельца (04.09, через holon, п.4): восемь тем беседы — погода, время
и календарь, еда, дорога, работа, счёт денег в быту, здоровье, семья. Полоса
БЕСЕДА-100 меряет этот род немым на 16 из 20, и причина у неё названа:
`SUBJ-UNKNOWN` — читатель не знает СУБЪЕКТА вопроса. «Что такое дождь?»
требует, чтобы дождь был определён в своде, а его там нет.

Две формы, и обе проверяемы своим способом:

  ОПРЕДЕЛЕНИЕ  «что такое дождь? дождь — это вода, которая падает из облаков.»
               судится объявленной таблицей: определение стоит в доме, и
               строка той же рамки с ЧУЖИМ определением — ложь;
  СЧЁТ         «в неделе 7 дней. сколько дней в неделе? 7 дней.» и
               «в сутках 24 часа, в часе 60 минут. сколько минут в сутках?
               1440 минут: 24 × 60 = 1440.» — судится пересчётом.

ЯЗЫКИ РАЗДЕЛЕНЫ ПО ПРИРОДЕ ФОРМЫ, и это не лень, а закон объявления. Счёт
календаря держат ВСЕ ДЕВЯТЬ языков атаки: в нём работают числа, а слов нужно
ровно два на единицу («день/дней»). Определения держат ПЯТЬ (ru, en, de, fr,
es): всякое определение есть предложение, которое надо написать верно, а не
перевести на глаз, и язык, чьи определения ещё не объявлены, их не пишет.
Это названный долг — четыре языка ждут своей волны, а не молчат по недосмотру.

    python3 tools/topicforms.py    # самопроверка с мутантами
"""
ТЕМЫ = ("погода", "время", "еда", "дорога", "работа", "деньги", "здоровье", "семья", "поведение")

# --- ОПРЕДЕЛЕНИЯ: {тема: ((термин, определение), …)} ---
ОПРЕДЕЛЕНИЯ = {
    "ru": {
        "погода": (("дождь", "вода, которая падает из облаков"), ("снег", "вода, которая замёрзла и падает из облаков"),
                   ("ветер", "воздух, который движется"), ("туман", "облако, которое лежит на земле"), ("погода", "то, каков воздух сегодня: тепло или холодно, сухо или дождливо"), ("гроза", "дождь с громом и молнией")),
        "время": (("неделя", "семь дней подряд"), ("год", "двенадцать месяцев подряд"),
                  ("час", "шестьдесят минут"), ("сутки", "двадцать четыре часа"), ("месяц", "часть года, около тридцати дней")),
        "еда": (("хлеб", "еда, которую пекут из муки"), ("суп", "горячая еда, которую едят ложкой"),
                ("завтрак", "еда, которую едят утром"), ("вода", "то, что пьют, когда хотят пить"), ("обед", "еда, которую едят днём")),
        "дорога": (("улица", "дорога между домами"), ("автобус", "машина, которая возит людей"),
                   ("пешеход", "человек, который идёт пешком"), ("мост", "дорога над водой"), ("дорога", "путь, по которому едут и идут"), ("поезд", "машина, которая едет по рельсам")),
        "работа": (("врач", "человек, который лечит больных"), ("учитель", "человек, который учит других"),
                   ("пекарь", "человек, который печёт хлеб"), ("водитель", "человек, который водит машину"), ("работа", "дело, которое человек делает, чтобы жить")),
        "деньги": (("цена", "сколько денег стоит вещь"), ("сдача", "деньги, которые возвращают покупателю"),
                   ("покупка", "вещь, которую купили"), ("кошелёк", "то, в чём носят деньги"), ("деньги", "то, чем платят за вещи"), ("магазин", "дом, где покупают вещи")),
        "здоровье": (("болезнь", "состояние, когда тело работает плохо"), ("сон", "отдых, в котором человек не бодрствует"),
                     ("лекарство", "то, что помогает больному"), ("больница", "дом, где лечат людей"), ("здоровье", "состояние, когда тело работает хорошо"), ("боль", "то, что человек чувствует, когда телу плохо")),
        "семья": (("родители", "мать и отец"), ("брат", "сын тех же родителей"),
                  ("сестра", "дочь тех же родителей"), ("семья", "люди, которые живут вместе и родня друг другу"), ("мать", "женщина, у которой есть ребёнок"), ("отец", "мужчина, у которого есть ребёнок")),
        "поведение": (("привычка", "действие, которое человек повторяет не думая"), ("внимание", "то, чем человек выбирает, что замечать"),
                      ("намерение", "то, что человек собирается сделать"), ("потребность", "то, чего человеку не хватает"),
                      ("эмоция", "состояние, которое меняет поведение"), ("усталость", "состояние, в котором человек работает хуже"), ("страх", "чувство, которое приходит при опасности или неизвестности"), ("память", "то, чем человек хранит прошлое")),
    },
    "en": {
        "погода": (("rain", "water that falls from the clouds"), ("snow", "water that has frozen and falls from the clouds"),
                   ("wind", "air that moves"), ("fog", "a cloud that lies on the ground"), ("the weather", "what the air is like today: warm or cold, dry or rainy"), ("a thunderstorm", "rain with thunder and lightning")),
        "время": (("a week", "seven days in a row"), ("a year", "twelve months in a row"),
                  ("an hour", "sixty minutes"), ("a day", "twenty four hours"), ("a month", "a part of a year, about thirty days")),
        "еда": (("bread", "food that is baked from flour"), ("soup", "hot food that is eaten with a spoon"),
                ("breakfast", "the food that is eaten in the morning"), ("water", "what people drink when they are thirsty"), ("lunch", "the food that is eaten in the middle of the day")),
        "дорога": (("a street", "a road between houses"), ("a bus", "a vehicle that carries people"),
                   ("a pedestrian", "a person who goes on foot"), ("a bridge", "a road over water"), ("a road", "a way along which people drive and walk"), ("a train", "a vehicle that runs on rails")),
        "работа": (("a doctor", "a person who treats the sick"), ("a teacher", "a person who teaches others"),
                   ("a baker", "a person who bakes bread"), ("a driver", "a person who drives a car"), ("work", "what a person does in order to live")),
        "деньги": (("a price", "how much money a thing costs"), ("change", "the money that is given back to the buyer"),
                   ("a purchase", "a thing that has been bought"), ("a wallet", "what people carry money in"), ("money", "what people pay for things with"), ("a shop", "a house where things are bought")),
        "здоровье": (("an illness", "a state in which the body works badly"), ("sleep", "the rest in which a person is not awake"),
                     ("a medicine", "what helps the sick"), ("a hospital", "a house where people are treated"), ("health", "the state in which the body works well"), ("pain", "what a person feels when the body is unwell")),
        "семья": (("parents", "a mother and a father"), ("a brother", "a son of the same parents"),
                  ("a sister", "a daughter of the same parents"), ("a family", "people who live together and are kin to each other"), ("a mother", "a woman who has a child"), ("a father", "a man who has a child")),
        "поведение": (("a habit", "an action that a person repeats without thinking"), ("attention", "what a person chooses with what to notice"),
                      ("an intention", "what a person is going to do"), ("a need", "what a person lacks"),
                      ("an emotion", "a state that changes behaviour"), ("tiredness", "a state in which a person works worse"), ("fear", "the feeling that comes with danger or the unknown"), ("memory", "what a person keeps the past with")),
    },
    "de": {
        "погода": (("Regen", "Wasser, das aus den Wolken fällt"), ("Schnee", "Wasser, das gefroren ist und aus den Wolken fällt"),
                   ("Wind", "Luft, die sich bewegt"), ("Nebel", "eine Wolke, die auf dem Boden liegt"), ("das Wetter", "wie die Luft heute ist: warm oder kalt, trocken oder regnerisch"), ("ein Gewitter", "Regen mit Donner und Blitz")),
        "время": (("eine Woche", "sieben Tage hintereinander"), ("ein Jahr", "zwölf Monate hintereinander"),
                  ("eine Stunde", "sechzig Minuten"), ("ein Tag", "vierundzwanzig Stunden"), ("ein Monat", "ein Teil des Jahres, etwa dreißig Tage")),
        "еда": (("Brot", "Essen, das aus Mehl gebacken wird"), ("Suppe", "warmes Essen, das man mit dem Löffel isst"),
                ("Frühstück", "das Essen, das man am Morgen isst"), ("Wasser", "das, was man trinkt, wenn man Durst hat"), ("Mittagessen", "das Essen, das man mittags isst")),
        "дорога": (("eine Straße", "ein Weg zwischen den Häusern"), ("ein Bus", "ein Fahrzeug, das Menschen befördert"),
                   ("ein Fußgänger", "ein Mensch, der zu Fuß geht"), ("eine Brücke", "ein Weg über das Wasser"), ("ein Weg", "eine Strecke, auf der man fährt und geht"), ("ein Zug", "ein Fahrzeug, das auf Schienen fährt")),
        "работа": (("ein Arzt", "ein Mensch, der Kranke behandelt"), ("ein Lehrer", "ein Mensch, der andere unterrichtet"),
                   ("ein Bäcker", "ein Mensch, der Brot backt"), ("ein Fahrer", "ein Mensch, der ein Auto fährt"), ("Arbeit", "das, was ein Mensch tut, um zu leben")),
        "деньги": (("ein Preis", "wie viel Geld eine Sache kostet"), ("Wechselgeld", "das Geld, das man dem Käufer zurückgibt"),
                   ("ein Einkauf", "eine Sache, die gekauft wurde"), ("eine Geldbörse", "das, worin man Geld trägt"), ("Geld", "das, womit man für Sachen bezahlt"), ("ein Geschäft", "ein Haus, in dem man Sachen kauft")),
        "здоровье": (("eine Krankheit", "ein Zustand, in dem der Körper schlecht arbeitet"), ("Schlaf", "die Ruhe, in der ein Mensch nicht wach ist"),
                     ("ein Medikament", "das, was dem Kranken hilft"), ("ein Krankenhaus", "ein Haus, in dem Menschen behandelt werden"), ("Gesundheit", "der Zustand, in dem der Körper gut arbeitet"), ("Schmerz", "das, was ein Mensch fühlt, wenn es dem Körper schlecht geht")),
        "семья": (("Eltern", "eine Mutter und ein Vater"), ("ein Bruder", "ein Sohn derselben Eltern"),
                  ("eine Schwester", "eine Tochter derselben Eltern"), ("eine Familie", "Menschen, die zusammen leben und miteinander verwandt sind"), ("eine Mutter", "eine Frau, die ein Kind hat"), ("ein Vater", "ein Mann, der ein Kind hat")),
        "поведение": (("eine Gewohnheit", "eine Handlung, die ein Mensch ohne nachzudenken wiederholt"), ("Aufmerksamkeit", "das, womit ein Mensch wählt, was er bemerkt"),
                      ("eine Absicht", "das, was ein Mensch tun will"), ("ein Bedürfnis", "das, was einem Menschen fehlt"),
                      ("ein Gefühl", "ein Zustand, der das Verhalten ändert"), ("Müdigkeit", "ein Zustand, in dem ein Mensch schlechter arbeitet"), ("Angst", "das Gefühl, das bei Gefahr oder Unbekanntem kommt"), ("Gedächtnis", "das, womit ein Mensch die Vergangenheit bewahrt")),
    },
    "fr": {
        "погода": (("la pluie", "de l'eau qui tombe des nuages"), ("la neige", "de l'eau gelée qui tombe des nuages"),
                   ("le vent", "de l'air qui bouge"), ("le brouillard", "un nuage qui repose sur le sol"), ("le temps", "ce qu'est l'air aujourd'hui : chaud ou froid, sec ou pluvieux"), ("un orage", "de la pluie avec du tonnerre et des éclairs")),
        "время": (("une semaine", "sept jours de suite"), ("une année", "douze mois de suite"),
                  ("une heure", "soixante minutes"), ("un jour", "vingt-quatre heures"), ("un mois", "une partie de l'année, environ trente jours")),
        "еда": (("le pain", "un aliment que l'on cuit avec de la farine"), ("la soupe", "un plat chaud que l'on mange à la cuillère"),
                ("le petit-déjeuner", "le repas que l'on prend le matin"), ("l'eau", "ce que l'on boit quand on a soif"), ("le déjeuner", "le repas que l'on prend au milieu du jour")),
        "дорога": (("une rue", "une route entre les maisons"), ("un bus", "un véhicule qui transporte des personnes"),
                   ("un piéton", "une personne qui va à pied"), ("un pont", "une route au-dessus de l'eau"), ("une route", "un chemin sur lequel on roule et on marche"), ("un train", "un véhicule qui roule sur des rails")),
        "работа": (("un médecin", "une personne qui soigne les malades"), ("un enseignant", "une personne qui instruit les autres"),
                   ("un boulanger", "une personne qui fait le pain"), ("un conducteur", "une personne qui conduit une voiture"), ("le travail", "ce qu'une personne fait pour vivre")),
        "деньги": (("un prix", "combien d'argent coûte une chose"), ("la monnaie", "l'argent que l'on rend à l'acheteur"),
                   ("un achat", "une chose que l'on a achetée"), ("un porte-monnaie", "ce dans quoi on porte l'argent"), ("l'argent", "ce avec quoi on paie les choses"), ("un magasin", "une maison où l'on achète des choses")),
        "здоровье": (("une maladie", "un état dans lequel le corps fonctionne mal"), ("le sommeil", "le repos pendant lequel on n'est pas éveillé"),
                     ("un médicament", "ce qui aide le malade"), ("un hôpital", "une maison où l'on soigne les gens"), ("la santé", "l'état dans lequel le corps fonctionne bien"), ("la douleur", "ce qu'une personne ressent quand le corps va mal")),
        "семья": (("les parents", "une mère et un père"), ("un frère", "un fils des mêmes parents"),
                  ("une sœur", "une fille des mêmes parents"), ("une famille", "des personnes qui vivent ensemble et sont parentes"), ("une mère", "une femme qui a un enfant"), ("un père", "un homme qui a un enfant")),
        "поведение": (("une habitude", "une action qu'une personne répète sans réfléchir"), ("l'attention", "ce par quoi une personne choisit ce qu'elle remarque"),
                      ("une intention", "ce qu'une personne va faire"), ("un besoin", "ce qui manque à une personne"),
                      ("une émotion", "un état qui change le comportement"), ("la fatigue", "un état dans lequel une personne travaille moins bien"), ("la peur", "le sentiment qui vient avec le danger ou l'inconnu"), ("la mémoire", "ce avec quoi une personne garde le passé")),
    },
    "es": {
        "погода": (("la lluvia", "agua que cae de las nubes"), ("la nieve", "agua congelada que cae de las nubes"),
                   ("el viento", "aire que se mueve"), ("la niebla", "una nube que está sobre el suelo"), ("el tiempo", "cómo está el aire hoy: cálido o frío, seco o lluvioso"), ("una tormenta", "lluvia con truenos y relámpagos")),
        "время": (("una semana", "siete días seguidos"), ("un año", "doce meses seguidos"),
                  ("una hora", "sesenta minutos"), ("un día", "veinticuatro horas"), ("un mes", "una parte del año, unos treinta días")),
        "еда": (("el pan", "comida que se hornea con harina"), ("la sopa", "comida caliente que se come con cuchara"),
                ("el desayuno", "la comida que se toma por la mañana"), ("el agua", "lo que se bebe cuando se tiene sed"), ("el almuerzo", "la comida que se toma a mediodía")),
        "дорога": (("una calle", "un camino entre las casas"), ("un autobús", "un vehículo que lleva personas"),
                   ("un peatón", "una persona que va a pie"), ("un puente", "un camino sobre el agua"), ("un camino", "una vía por la que se conduce y se anda"), ("un tren", "un vehículo que va sobre raíles")),
        "работа": (("un médico", "una persona que cura a los enfermos"), ("un maestro", "una persona que enseña a otros"),
                   ("un panadero", "una persona que hace el pan"), ("un conductor", "una persona que conduce un coche"), ("el trabajo", "lo que una persona hace para vivir")),
        "деньги": (("un precio", "cuánto dinero cuesta una cosa"), ("el cambio", "el dinero que se devuelve al comprador"),
                   ("una compra", "una cosa que se ha comprado"), ("una cartera", "aquello en lo que se lleva el dinero"), ("el dinero", "aquello con lo que se paga por las cosas"), ("una tienda", "una casa donde se compran cosas")),
        "здоровье": (("una enfermedad", "un estado en el que el cuerpo funciona mal"), ("el sueño", "el descanso en el que no se está despierto"),
                     ("un medicamento", "lo que ayuda al enfermo"), ("un hospital", "una casa donde se cura a las personas"), ("la salud", "el estado en el que el cuerpo funciona bien"), ("el dolor", "lo que una persona siente cuando el cuerpo está mal")),
        "семья": (("los padres", "una madre y un padre"), ("un hermano", "un hijo de los mismos padres"),
                  ("una hermana", "una hija de los mismos padres"), ("una familia", "personas que viven juntas y son parientes"), ("una madre", "una mujer que tiene un hijo"), ("un padre", "un hombre que tiene un hijo")),
        "поведение": (("un hábito", "una acción que una persona repite sin pensar"), ("la atención", "aquello con lo que una persona elige qué notar"),
                      ("una intención", "lo que una persona va a hacer"), ("una necesidad", "lo que le falta a una persona"),
                      ("una emoción", "un estado que cambia la conducta"), ("el cansancio", "un estado en el que una persona trabaja peor"), ("el miedo", "el sentimiento que llega con el peligro o lo desconocido"), ("la memoria", "aquello con lo que una persona guarda el pasado")),
    },
    "it": {
        "погода": (("la pioggia", "acqua che cade dalle nuvole"), ("la neve", "acqua gelata che cade dalle nuvole"),
                   ("il vento", "aria che si muove"), ("la nebbia", "una nuvola che sta sul terreno"),
                   ("il tempo", "com'è l'aria oggi: caldo o freddo, secco o piovoso"), ("un temporale", "pioggia con tuoni e lampi")),
        "время": (("una settimana", "sette giorni di seguito"), ("un anno", "dodici mesi di seguito"),
                  ("un'ora", "sessanta minuti"), ("un giorno", "ventiquattro ore"),
                  ("un mese", "una parte dell'anno, circa trenta giorni")),
        "еда": (("il pane", "cibo che si cuoce con la farina"), ("la zuppa", "cibo caldo che si mangia col cucchiaio"),
                ("la colazione", "il pasto che si fa la mattina"), ("l'acqua", "ciò che si beve quando si ha sete"),
                ("il pranzo", "il pasto che si fa a metà giornata")),
        "дорога": (("una via", "una strada tra le case"), ("un autobus", "un veicolo che porta le persone"),
                   ("un pedone", "una persona che va a piedi"), ("un ponte", "una strada sopra l'acqua"),
                   ("una strada", "un percorso su cui si guida e si cammina"), ("un treno", "un veicolo che va sui binari")),
        "работа": (("un medico", "una persona che cura i malati"), ("un insegnante", "una persona che insegna agli altri"),
                   ("un panettiere", "una persona che fa il pane"), ("un autista", "una persona che guida un'auto"),
                   ("il lavoro", "ciò che una persona fa per vivere")),
        "деньги": (("un prezzo", "quanto denaro costa una cosa"), ("il resto", "il denaro che si rende a chi compra"),
                   ("un acquisto", "una cosa che è stata comprata"), ("un portafoglio", "ciò in cui si porta il denaro"),
                   ("il denaro", "ciò con cui si paga per le cose"), ("un negozio", "una casa dove si comprano le cose")),
        "здоровье": (("una malattia", "uno stato in cui il corpo funziona male"), ("il sonno", "il riposo in cui non si è svegli"),
                     ("una medicina", "ciò che aiuta il malato"), ("un ospedale", "una casa dove si curano le persone"),
                     ("la salute", "lo stato in cui il corpo funziona bene"), ("il dolore", "ciò che una persona sente quando il corpo sta male")),
        "семья": (("i genitori", "una madre e un padre"), ("un fratello", "un figlio degli stessi genitori"),
                  ("una sorella", "una figlia degli stessi genitori"), ("una famiglia", "persone che vivono insieme e sono parenti"),
                  ("una madre", "una donna che ha un figlio"), ("un padre", "un uomo che ha un figlio")),
        "поведение": (("un'abitudine", "un'azione che una persona ripete senza pensare"), ("l'attenzione", "ciò con cui una persona sceglie che cosa notare"),
                      ("un'intenzione", "ciò che una persona sta per fare"), ("un bisogno", "ciò che manca a una persona"),
                      ("un'emozione", "uno stato che cambia il comportamento"), ("la stanchezza", "uno stato in cui una persona lavora peggio"),
                      ("la paura", "il sentimento che viene col pericolo o con l'ignoto"), ("la memoria", "ciò con cui una persona conserva il passato")),
    },
    "pt": {
        "погода": (("a chuva", "água que cai das nuvens"), ("a neve", "água gelada que cai das nuvens"),
                   ("o vento", "ar que se move"), ("o nevoeiro", "uma nuvem que está sobre o chão"),
                   ("o tempo", "como está o ar hoje: quente ou frio, seco ou chuvoso"), ("uma trovoada", "chuva com trovões e relâmpagos")),
        "время": (("uma semana", "sete dias seguidos"), ("um ano", "doze meses seguidos"),
                  ("uma hora", "sessenta minutos"), ("um dia", "vinte e quatro horas"),
                  ("um mês", "uma parte do ano, cerca de trinta dias")),
        "еда": (("o pão", "comida que se coze com farinha"), ("a sopa", "comida quente que se come com colher"),
                ("o pequeno-almoço", "a refeição que se toma de manhã"), ("a água", "o que se bebe quando se tem sede"),
                ("o almoço", "a refeição que se toma a meio do dia")),
        "дорога": (("uma rua", "um caminho entre as casas"), ("um autocarro", "um veículo que leva pessoas"),
                   ("um peão", "uma pessoa que anda a pé"), ("uma ponte", "um caminho por cima da água"),
                   ("uma estrada", "um caminho por onde se conduz e se anda"), ("um comboio", "um veículo que anda sobre carris")),
        "работа": (("um médico", "uma pessoa que trata os doentes"), ("um professor", "uma pessoa que ensina os outros"),
                   ("um padeiro", "uma pessoa que faz o pão"), ("um condutor", "uma pessoa que conduz um carro"),
                   ("o trabalho", "aquilo que uma pessoa faz para viver")),
        "деньги": (("um preço", "quanto dinheiro custa uma coisa"), ("o troco", "o dinheiro que se devolve a quem compra"),
                   ("uma compra", "uma coisa que foi comprada"), ("uma carteira", "aquilo em que se leva o dinheiro"),
                   ("o dinheiro", "aquilo com que se paga as coisas"), ("uma loja", "uma casa onde se compram coisas")),
        "здоровье": (("uma doença", "um estado em que o corpo funciona mal"), ("o sono", "o descanso em que não se está acordado"),
                     ("um medicamento", "aquilo que ajuda o doente"), ("um hospital", "uma casa onde se tratam as pessoas"),
                     ("a saúde", "o estado em que o corpo funciona bem"), ("a dor", "o que uma pessoa sente quando o corpo está mal")),
        "семья": (("os pais", "uma mãe e um pai"), ("um irmão", "um filho dos mesmos pais"),
                  ("uma irmã", "uma filha dos mesmos pais"), ("uma família", "pessoas que vivem juntas e são parentes"),
                  ("uma mãe", "uma mulher que tem um filho"), ("um pai", "um homem que tem um filho")),
        "поведение": (("um hábito", "uma ação que uma pessoa repete sem pensar"), ("a atenção", "aquilo com que uma pessoa escolhe o que notar"),
                      ("uma intenção", "aquilo que uma pessoa vai fazer"), ("uma necessidade", "aquilo que falta a uma pessoa"),
                      ("uma emoção", "um estado que muda o comportamento"), ("o cansaço", "um estado em que uma pessoa trabalha pior"),
                      ("o medo", "o sentimento que vem com o perigo ou com o desconhecido"), ("a memória", "aquilo com que uma pessoa guarda o passado")),
    },
    "nl": {
        "погода": (("de regen", "water dat uit de wolken valt"), ("de sneeuw", "bevroren water dat uit de wolken valt"),
                   ("de wind", "lucht die beweegt"), ("de mist", "een wolk die op de grond ligt"),
                   ("het weer", "hoe de lucht vandaag is: warm of koud, droog of regenachtig"), ("een onweer", "regen met donder en bliksem")),
        "время": (("een week", "zeven dagen achter elkaar"), ("een jaar", "twaalf maanden achter elkaar"),
                  ("een uur", "zestig minuten"), ("een dag", "vierentwintig uren"),
                  ("een maand", "een deel van het jaar, ongeveer dertig dagen")),
        "еда": (("het brood", "eten dat van meel gebakken wordt"), ("de soep", "warm eten dat men met een lepel eet"),
                ("het ontbijt", "het eten dat men in de ochtend eet"), ("het water", "wat men drinkt als men dorst heeft"),
                ("de lunch", "het eten dat men midden op de dag eet")),
        "дорога": (("een straat", "een weg tussen de huizen"), ("een bus", "een voertuig dat mensen vervoert"),
                   ("een voetganger", "een mens die te voet gaat"), ("een brug", "een weg over het water"),
                   ("een weg", "een baan waarover men rijdt en loopt"), ("een trein", "een voertuig dat op rails rijdt")),
        "работа": (("een arts", "een mens die zieken behandelt"), ("een leraar", "een mens die anderen onderwijst"),
                   ("een bakker", "een mens die brood bakt"), ("een chauffeur", "een mens die een auto bestuurt"),
                   ("het werk", "dat wat een mens doet om te leven")),
        "деньги": (("een prijs", "hoeveel geld een ding kost"), ("het wisselgeld", "het geld dat men aan de koper teruggeeft"),
                   ("een aankoop", "een ding dat gekocht is"), ("een portemonnee", "dat waarin men geld draagt"),
                   ("het geld", "dat waarmee men voor dingen betaalt"), ("een winkel", "een huis waar men dingen koopt")),
        "здоровье": (("een ziekte", "een toestand waarin het lichaam slecht werkt"), ("de slaap", "de rust waarin een mens niet wakker is"),
                     ("een geneesmiddel", "dat wat de zieke helpt"), ("een ziekenhuis", "een huis waar mensen behandeld worden"),
                     ("de gezondheid", "de toestand waarin het lichaam goed werkt"), ("de pijn", "wat een mens voelt als het lichaam slecht is")),
        "семья": (("de ouders", "een moeder en een vader"), ("een broer", "een zoon van dezelfde ouders"),
                  ("een zus", "een dochter van dezelfde ouders"), ("een gezin", "mensen die samen leven en familie van elkaar zijn"),
                  ("een moeder", "een vrouw die een kind heeft"), ("een vader", "een man die een kind heeft")),
        "поведение": (("een gewoonte", "een handeling die een mens zonder nadenken herhaalt"), ("de aandacht", "dat waarmee een mens kiest wat hij opmerkt"),
                      ("een voornemen", "dat wat een mens gaat doen"), ("een behoefte", "dat wat een mens mist"),
                      ("een gevoel", "een toestand die het gedrag verandert"), ("de moeheid", "een toestand waarin een mens slechter werkt"),
                      ("de angst", "het gevoel dat komt bij gevaar of bij het onbekende"), ("het geheugen", "dat waarmee een mens het verleden bewaart")),
    },
    "pl": {
        "погода": (("deszcz", "woda, która pada z chmur"), ("śnieg", "zamarznięta woda, która pada z chmur"),
                   ("wiatr", "powietrze, które się porusza"), ("mgła", "chmura, która leży na ziemi"),
                   ("pogoda", "jakie jest dziś powietrze: ciepło czy zimno, sucho czy deszczowo"), ("burza", "deszcz z grzmotami i błyskawicami")),
        "время": (("tydzień", "siedem dni po sobie"), ("rok", "dwanaście miesięcy po sobie"),
                  ("godzina", "sześćdziesiąt minut"), ("doba", "dwadzieścia cztery godziny"),
                  ("miesiąc", "część roku, około trzydziestu dni")),
        "еда": (("chleb", "jedzenie, które piecze się z mąki"), ("zupa", "gorące jedzenie, które je się łyżką"),
                ("śniadanie", "jedzenie, które je się rano"), ("woda", "to, co się pije, gdy chce się pić"),
                ("obiad", "jedzenie, które je się w środku dnia")),
        "дорога": (("ulica", "droga między domami"), ("autobus", "pojazd, który wozi ludzi"),
                   ("pieszy", "człowiek, który idzie na piechotę"), ("most", "droga nad wodą"),
                   ("droga", "szlak, po którym się jeździ i chodzi"), ("pociąg", "pojazd, który jedzie po szynach")),
        "работа": (("lekarz", "człowiek, który leczy chorych"), ("nauczyciel", "człowiek, który uczy innych"),
                   ("piekarz", "człowiek, który piecze chleb"), ("kierowca", "człowiek, który prowadzi samochód"),
                   ("praca", "to, co człowiek robi, żeby żyć")),
        "деньги": (("cena", "ile pieniędzy kosztuje rzecz"), ("reszta", "pieniądze, które oddaje się kupującemu"),
                   ("zakup", "rzecz, która została kupiona"), ("portfel", "to, w czym nosi się pieniądze"),
                   ("pieniądze", "to, czym płaci się za rzeczy"), ("sklep", "dom, w którym kupuje się rzeczy")),
        "здоровье": (("choroba", "stan, w którym ciało źle pracuje"), ("sen", "odpoczynek, w którym człowiek nie czuwa"),
                     ("lekarstwo", "to, co pomaga choremu"), ("szpital", "dom, w którym leczy się ludzi"),
                     ("zdrowie", "stan, w którym ciało dobrze pracuje"), ("ból", "to, co człowiek czuje, gdy ciału jest źle")),
        "семья": (("rodzice", "matka i ojciec"), ("brat", "syn tych samych rodziców"),
                  ("siostra", "córka tych samych rodziców"), ("rodzina", "ludzie, którzy mieszkają razem i są sobie krewni"),
                  ("matka", "kobieta, która ma dziecko"), ("ojciec", "mężczyzna, który ma dziecko")),
        "поведение": (("nawyk", "czynność, którą człowiek powtarza bez namysłu"), ("uwaga", "to, czym człowiek wybiera, co zauważyć"),
                      ("zamiar", "to, co człowiek zamierza zrobić"), ("potrzeba", "to, czego człowiekowi brakuje"),
                      ("emocja", "stan, który zmienia zachowanie"), ("zmęczenie", "stan, w którym człowiek gorzej pracuje"),
                      ("strach", "uczucie, które przychodzi przy niebezpieczeństwie lub przy nieznanym"), ("pamięć", "to, czym człowiek przechowuje przeszłość")),
    },
}
# рамка определения и вопроса о нём
РАМКИ = {
    "ru": ("{т} — это {о}.", "что такое {т}? {т} — это {о}."),
    "en": ("{т} is {о}.", "what is {т}? {т} is {о}."),
    "de": ("{т} ist {о}.", "was ist {т}? {т} ist {о}."),
    "fr": ("{т}, c'est {о}.", "qu'est-ce que {т} ? {т}, c'est {о}."),
    "es": ("{т} es {о}.", "¿qué es {т}? {т} es {о}."),
    "it": ("{т} è {о}.", "che cos'è {т}? {т} è {о}."),
    "pt": ("{т} é {о}.", "o que é {т}? {т} é {о}."),
    "nl": ("{т} is {о}.", "wat is {т}? {т} is {о}."),
    "pl": ("{т} to {о}.", "co to jest {т}? {т} to {о}."),
}

# --- СЧЁТ КАЛЕНДАРЯ: девять языков, ибо работают числа, а слов нужно два ---
# (единица большая, единица малая, сколько малых в большой)
КАЛЕНДАРЬ = ((("неделе", "неделя"), ("дней", "день"), 7), (("годе", "год"), ("месяцев", "месяц"), 12),
             (("сутках", "сутки"), ("часов", "час"), 24), (("часе", "час"), ("минут", "минута"), 60),
             (("минуте", "минута"), ("секунд", "секунда"), 60))
СЧЁТ = {
    "ru": dict(в="в {б} {n} {м}.", воп="в {б} {n} {м}. сколько {мв} в {б}? {n} {м}.",
               воп2="в {б} {n} {м}. сколько всего {мв} в {б}? {n} {м}.",
               пары=((("неделе", "дней", "дней"), 7), (("году", "месяцев", "месяцев"), 12),
                     (("сутках", "часа", "часов"), 24),
                     (("часе", "минут", "минут"), 60), (("минуте", "секунд", "секунд"), 60))),
    "en": dict(в="there are {n} {м} in {б}.", воп="there are {n} {м} in {б}. how many {мв} are there in {б}? {n} {м}.",
               воп2="there are {n} {м} in {б}. how many {мв} are in {б}? {n} {м}.",
               пары=((("a week", "days", "days"), 7), (("a year", "months", "months"), 12), (("a day", "hours", "hours"), 24),
                     (("an hour", "minutes", "minutes"), 60), (("a minute", "seconds", "seconds"), 60))),
    "de": dict(в="{б} hat {n} {м}.", воп="{б} hat {n} {м}. wie viele {мв} hat {б}? {n} {м}.",
               пары=((("eine Woche", "Tage", "Tage"), 7), (("ein Jahr", "Monate", "Monate"), 12), (("ein Tag", "Stunden", "Stunden"), 24),
                     (("eine Stunde", "Minuten", "Minuten"), 60), (("eine Minute", "Sekunden", "Sekunden"), 60))),
    "fr": dict(в="{б} a {n} {м}.", воп="{б} a {n} {м}. combien de {мв} a {б} ? {n} {м}.",
               пары=((("une semaine", "jours", "jours"), 7), (("une année", "mois", "mois"), 12), (("un jour", "heures", "heures"), 24),
                     (("une heure", "minutes", "minutes"), 60), (("une minute", "secondes", "secondes"), 60))),
    "es": dict(в="{б} tiene {n} {м}.", воп="{б} tiene {n} {м}. ¿cuántos {мв} tiene {б}? {n} {м}.",
               пары=((("una semana", "días", "días"), 7), (("un año", "meses", "meses"), 12), (("un día", "horas", "horas"), 24),
                     (("una hora", "minutos", "minutos"), 60), (("un minuto", "segundos", "segundos"), 60))),
    "it": dict(в="{б} ha {n} {м}.", воп="{б} ha {n} {м}. quanti {мв} ha {б}? {n} {м}.",
               пары=((("una settimana", "giorni", "giorni"), 7), (("un anno", "mesi", "mesi"), 12), (("un giorno", "ore", "ore"), 24),
                     (("un'ora", "minuti", "minuti"), 60), (("un minuto", "secondi", "secondi"), 60))),
    "pt": dict(в="{б} tem {n} {м}.", воп="{б} tem {n} {м}. quantos {мв} tem {б}? {n} {м}.",
               пары=((("uma semana", "dias", "dias"), 7), (("um ano", "meses", "meses"), 12), (("um dia", "horas", "horas"), 24),
                     (("uma hora", "minutos", "minutos"), 60), (("um minuto", "segundos", "segundos"), 60))),
    "nl": dict(в="{б} heeft {n} {м}.", воп="{б} heeft {n} {м}. hoeveel {мв} heeft {б}? {n} {м}.",
               пары=((("een week", "dagen", "dagen"), 7), (("een jaar", "maanden", "maanden"), 12), (("een dag", "uren", "uren"), 24),
                     (("een uur", "minuten", "minuten"), 60), (("een minuut", "seconden", "seconden"), 60))),
    "pl": dict(в="{б} ma {n} {м}.", воп="{б} ma {n} {м}. ile {мв} ma {б}? {n} {м}.",
               пары=((("tydzień", "dni", "dni"), 7), (("rok", "miesięcy", "miesięcy"), 12),
                     (("doba", "godziny", "godzin"), 24),
                     (("godzina", "minut", "minut"), 60), (("minuta", "sekund", "sekund"), 60))),
}
# ЦЕПЬ КАЛЕНДАРЯ: две единицы через третью, и кузница показывает оба шага
ЦЕПИ = ((2, 3), (3, 4))   # индексы пар: сутки→часы→минуты, часы→минуты→секунды
ЦЕПЬ_РАМКА = {
    "ru": "в {б1} {n1} {м1}, в {б2} {n2} {м2}. сколько {мв2} в {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "en": "there are {n1} {м1} in {б1}, and {n2} {м2} in {б2}. how many {мв2} are there in {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "de": "{б1} hat {n1} {м1}, {б2} hat {n2} {м2}. wie viele {мв2} hat {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "fr": "{б1} a {n1} {м1}, {б2} a {n2} {м2}. combien de {мв2} a {б1} ? {r} {м2} : {n1} × {n2} = {r}.",
    "es": "{б1} tiene {n1} {м1}, {б2} tiene {n2} {м2}. ¿cuántos {мв2} tiene {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "it": "{б1} ha {n1} {м1}, {б2} ha {n2} {м2}. quanti {мв2} ha {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "pt": "{б1} tem {n1} {м1}, {б2} tem {n2} {м2}. quantos {мв2} tem {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "nl": "{б1} heeft {n1} {м1}, {б2} heeft {n2} {м2}. hoeveel {мв2} heeft {б1}? {r} {м2}: {n1} × {n2} = {r}.",
    "pl": "{б1} ma {n1} {м1}, {б2} ma {n2} {м2}. ile {мв2} ma {б1}? {r} {м2}: {n1} × {n2} = {r}.",
}


def _показы():
    вон = {}
    for язык, темы in ОПРЕДЕЛЕНИЯ.items():
        утв, воп = РАМКИ[язык]
        for тема, пары in темы.items():
            for т, о in пары:
                вон[утв.format(т=т, о=о)] = (язык, "определение")
                вон[воп.format(т=т, о=о)] = (язык, "вопрос_определения")
    for язык, с in СЧЁТ.items():
        for (б, м, мв), n in с["пары"]:
            вон[с["в"].format(б=б, м=м, мв=мв, n=n)] = (язык, "счёт")
            вон[с["воп"].format(б=б, м=м, мв=мв, n=n)] = (язык, "вопрос_счёта")
            if "воп2" in с:   # вторая вопросная рамка там, где язык её имеет
                вон[с["воп2"].format(б=б, м=м, мв=мв, n=n)] = (язык, "вопрос_счёта")
        for i, j in ЦЕПИ:
            (б1, м1, мв1), n1 = с["пары"][i]
            (б2, м2, мв2), n2 = с["пары"][j]
            вон[ЦЕПЬ_РАМКА[язык].format(б1=б1, м1=м1, мв1=мв1, n1=n1,
                                        б2=б2, м2=м2, мв2=мв2, n2=n2, r=n1 * n2)] = (язык, "цепь_счёта")
    return вон


ПОКАЗЫ = _показы()
ФОРМЫ = ("определение", "вопрос_определения", "счёт", "вопрос_счёта", "цепь_счёта")
ЯЗЫКИ = СЧЁТ   # девять языков: счёт держат все, определения — пять


def судить(строка):
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    # рамка определения с ЧУЖИМ определением — ложь, а не молчание
    for язык, (утв, воп) in РАМКИ.items():
        for тема, пары in ОПРЕДЕЛЕНИЯ[язык].items():
            for т, _ in пары:
                for ш in (утв, воп):
                    начало = ш.split("{о}")[0].format(т=т, о="")
                    if начало and с.startswith(начало):
                        return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык in ОПРЕДЕЛЕНИЯ:
        утв, воп = РАМКИ[язык]
        т, о = ОПРЕДЕЛЕНИЯ[язык]["погода"][0]
        _, чужое = ОПРЕДЕЛЕНИЯ[язык]["еда"][0]
        assert судить(воп.format(т=т, о=о)) == (True, True), язык
        assert судить(воп.format(т=т, о=чужое)) == (True, False), (язык, чужое)
        мутанты += 1
    for язык in СЧЁТ:
        (б, м, мв), n = СЧЁТ[язык]["пары"][0]
        с = СЧЁТ[язык]["воп"].format(б=б, м=м, мв=мв, n=n)
        assert судить(с) == (True, True), (язык, с)
    for язык in ("ru", "en", "de"):
        утв, воп = РАМКИ[язык]
        print("  ", воп.format(*(), **dict(zip(("т", "о"), ОПРЕДЕЛЕНИЯ[язык]["погода"][0])))[:112])
        (б, м, мв), n = СЧЁТ[язык]["пары"][2]
        print("  ", СЧЁТ[язык]["воп"].format(б=б, м=м, мв=мв, n=n)[:112])
    i, j = ЦЕПИ[0]
    (б1, м1, мв1), n1 = СЧЁТ["ru"]["пары"][i]
    (б2, м2, мв2), n2 = СЧЁТ["ru"]["пары"][j]
    print("  ", ЦЕПЬ_РАМКА["ru"].format(б1=б1, м1=м1, мв1=мв1, n1=n1, б2=б2, м2=м2, мв2=мв2, n2=n2, r=n1 * n2))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (тем {len(ТЕМЫ)}, языков счёта {len(СЧЁТ)}, языков определений {len(ОПРЕДЕЛЕНИЯ)})")


if __name__ == "__main__":
    _самопроверка()
