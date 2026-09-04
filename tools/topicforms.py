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
                   ("ветер", "воздух, который движется"), ("туман", "облако, которое лежит на земле")),
        "время": (("неделя", "семь дней подряд"), ("год", "двенадцать месяцев подряд"),
                  ("час", "шестьдесят минут"), ("сутки", "двадцать четыре часа")),
        "еда": (("хлеб", "еда, которую пекут из муки"), ("суп", "горячая еда, которую едят ложкой"),
                ("завтрак", "еда, которую едят утром"), ("вода", "то, что пьют, когда хотят пить")),
        "дорога": (("улица", "дорога между домами"), ("автобус", "машина, которая возит людей"),
                   ("пешеход", "человек, который идёт пешком"), ("мост", "дорога над водой")),
        "работа": (("врач", "человек, который лечит больных"), ("учитель", "человек, который учит других"),
                   ("пекарь", "человек, который печёт хлеб"), ("водитель", "человек, который водит машину")),
        "деньги": (("цена", "сколько денег стоит вещь"), ("сдача", "деньги, которые возвращают покупателю"),
                   ("покупка", "вещь, которую купили"), ("кошелёк", "то, в чём носят деньги")),
        "здоровье": (("болезнь", "состояние, когда тело работает плохо"), ("сон", "отдых, в котором человек не бодрствует"),
                     ("лекарство", "то, что помогает больному"), ("больница", "дом, где лечат людей")),
        "семья": (("родители", "мать и отец"), ("брат", "сын тех же родителей"),
                  ("сестра", "дочь тех же родителей"), ("семья", "люди, которые живут вместе и родня друг другу")),
        "поведение": (("привычка", "действие, которое человек повторяет не думая"), ("внимание", "то, чем человек выбирает, что замечать"),
                      ("намерение", "то, что человек собирается сделать"), ("потребность", "то, чего человеку не хватает"),
                      ("эмоция", "состояние, которое меняет поведение"), ("усталость", "состояние, в котором человек работает хуже")),
    },
    "en": {
        "погода": (("rain", "water that falls from the clouds"), ("snow", "water that has frozen and falls from the clouds"),
                   ("wind", "air that moves"), ("fog", "a cloud that lies on the ground")),
        "время": (("a week", "seven days in a row"), ("a year", "twelve months in a row"),
                  ("an hour", "sixty minutes"), ("a day", "twenty four hours")),
        "еда": (("bread", "food that is baked from flour"), ("soup", "hot food that is eaten with a spoon"),
                ("breakfast", "the food that is eaten in the morning"), ("water", "what people drink when they are thirsty")),
        "дорога": (("a street", "a road between houses"), ("a bus", "a vehicle that carries people"),
                   ("a pedestrian", "a person who goes on foot"), ("a bridge", "a road over water")),
        "работа": (("a doctor", "a person who treats the sick"), ("a teacher", "a person who teaches others"),
                   ("a baker", "a person who bakes bread"), ("a driver", "a person who drives a car")),
        "деньги": (("a price", "how much money a thing costs"), ("change", "the money that is given back to the buyer"),
                   ("a purchase", "a thing that has been bought"), ("a wallet", "what people carry money in")),
        "здоровье": (("an illness", "a state in which the body works badly"), ("sleep", "the rest in which a person is not awake"),
                     ("a medicine", "what helps the sick"), ("a hospital", "a house where people are treated")),
        "семья": (("parents", "a mother and a father"), ("a brother", "a son of the same parents"),
                  ("a sister", "a daughter of the same parents"), ("a family", "people who live together and are kin to each other")),
        "поведение": (("a habit", "an action that a person repeats without thinking"), ("attention", "what a person chooses with what to notice"),
                      ("an intention", "what a person is going to do"), ("a need", "what a person lacks"),
                      ("an emotion", "a state that changes behaviour"), ("tiredness", "a state in which a person works worse")),
    },
    "de": {
        "погода": (("Regen", "Wasser, das aus den Wolken fällt"), ("Schnee", "Wasser, das gefroren ist und aus den Wolken fällt"),
                   ("Wind", "Luft, die sich bewegt"), ("Nebel", "eine Wolke, die auf dem Boden liegt")),
        "время": (("eine Woche", "sieben Tage hintereinander"), ("ein Jahr", "zwölf Monate hintereinander"),
                  ("eine Stunde", "sechzig Minuten"), ("ein Tag", "vierundzwanzig Stunden")),
        "еда": (("Brot", "Essen, das aus Mehl gebacken wird"), ("Suppe", "warmes Essen, das man mit dem Löffel isst"),
                ("Frühstück", "das Essen, das man am Morgen isst"), ("Wasser", "das, was man trinkt, wenn man Durst hat")),
        "дорога": (("eine Straße", "ein Weg zwischen den Häusern"), ("ein Bus", "ein Fahrzeug, das Menschen befördert"),
                   ("ein Fußgänger", "ein Mensch, der zu Fuß geht"), ("eine Brücke", "ein Weg über das Wasser")),
        "работа": (("ein Arzt", "ein Mensch, der Kranke behandelt"), ("ein Lehrer", "ein Mensch, der andere unterrichtet"),
                   ("ein Bäcker", "ein Mensch, der Brot backt"), ("ein Fahrer", "ein Mensch, der ein Auto fährt")),
        "деньги": (("ein Preis", "wie viel Geld eine Sache kostet"), ("Wechselgeld", "das Geld, das man dem Käufer zurückgibt"),
                   ("ein Einkauf", "eine Sache, die gekauft wurde"), ("eine Geldbörse", "das, worin man Geld trägt")),
        "здоровье": (("eine Krankheit", "ein Zustand, in dem der Körper schlecht arbeitet"), ("Schlaf", "die Ruhe, in der ein Mensch nicht wach ist"),
                     ("ein Medikament", "das, was dem Kranken hilft"), ("ein Krankenhaus", "ein Haus, in dem Menschen behandelt werden")),
        "семья": (("Eltern", "eine Mutter und ein Vater"), ("ein Bruder", "ein Sohn derselben Eltern"),
                  ("eine Schwester", "eine Tochter derselben Eltern"), ("eine Familie", "Menschen, die zusammen leben und miteinander verwandt sind")),
        "поведение": (("eine Gewohnheit", "eine Handlung, die ein Mensch ohne nachzudenken wiederholt"), ("Aufmerksamkeit", "das, womit ein Mensch wählt, was er bemerkt"),
                      ("eine Absicht", "das, was ein Mensch tun will"), ("ein Bedürfnis", "das, was einem Menschen fehlt"),
                      ("ein Gefühl", "ein Zustand, der das Verhalten ändert"), ("Müdigkeit", "ein Zustand, in dem ein Mensch schlechter arbeitet")),
    },
    "fr": {
        "погода": (("la pluie", "de l'eau qui tombe des nuages"), ("la neige", "de l'eau gelée qui tombe des nuages"),
                   ("le vent", "de l'air qui bouge"), ("le brouillard", "un nuage qui repose sur le sol")),
        "время": (("une semaine", "sept jours de suite"), ("une année", "douze mois de suite"),
                  ("une heure", "soixante minutes"), ("un jour", "vingt-quatre heures")),
        "еда": (("le pain", "un aliment que l'on cuit avec de la farine"), ("la soupe", "un plat chaud que l'on mange à la cuillère"),
                ("le petit-déjeuner", "le repas que l'on prend le matin"), ("l'eau", "ce que l'on boit quand on a soif")),
        "дорога": (("une rue", "une route entre les maisons"), ("un bus", "un véhicule qui transporte des personnes"),
                   ("un piéton", "une personne qui va à pied"), ("un pont", "une route au-dessus de l'eau")),
        "работа": (("un médecin", "une personne qui soigne les malades"), ("un enseignant", "une personne qui instruit les autres"),
                   ("un boulanger", "une personne qui fait le pain"), ("un conducteur", "une personne qui conduit une voiture")),
        "деньги": (("un prix", "combien d'argent coûte une chose"), ("la monnaie", "l'argent que l'on rend à l'acheteur"),
                   ("un achat", "une chose que l'on a achetée"), ("un porte-monnaie", "ce dans quoi on porte l'argent")),
        "здоровье": (("une maladie", "un état dans lequel le corps fonctionne mal"), ("le sommeil", "le repos pendant lequel on n'est pas éveillé"),
                     ("un médicament", "ce qui aide le malade"), ("un hôpital", "une maison où l'on soigne les gens")),
        "семья": (("les parents", "une mère et un père"), ("un frère", "un fils des mêmes parents"),
                  ("une sœur", "une fille des mêmes parents"), ("une famille", "des personnes qui vivent ensemble et sont parentes")),
        "поведение": (("une habitude", "une action qu'une personne répète sans réfléchir"), ("l'attention", "ce par quoi une personne choisit ce qu'elle remarque"),
                      ("une intention", "ce qu'une personne va faire"), ("un besoin", "ce qui manque à une personne"),
                      ("une émotion", "un état qui change le comportement"), ("la fatigue", "un état dans lequel une personne travaille moins bien")),
    },
    "es": {
        "погода": (("la lluvia", "agua que cae de las nubes"), ("la nieve", "agua congelada que cae de las nubes"),
                   ("el viento", "aire que se mueve"), ("la niebla", "una nube que está sobre el suelo")),
        "время": (("una semana", "siete días seguidos"), ("un año", "doce meses seguidos"),
                  ("una hora", "sesenta minutos"), ("un día", "veinticuatro horas")),
        "еда": (("el pan", "comida que se hornea con harina"), ("la sopa", "comida caliente que se come con cuchara"),
                ("el desayuno", "la comida que se toma por la mañana"), ("el agua", "lo que se bebe cuando se tiene sed")),
        "дорога": (("una calle", "un camino entre las casas"), ("un autobús", "un vehículo que lleva personas"),
                   ("un peatón", "una persona que va a pie"), ("un puente", "un camino sobre el agua")),
        "работа": (("un médico", "una persona que cura a los enfermos"), ("un maestro", "una persona que enseña a otros"),
                   ("un panadero", "una persona que hace el pan"), ("un conductor", "una persona que conduce un coche")),
        "деньги": (("un precio", "cuánto dinero cuesta una cosa"), ("el cambio", "el dinero que se devuelve al comprador"),
                   ("una compra", "una cosa que se ha comprado"), ("una cartera", "aquello en lo que se lleva el dinero")),
        "здоровье": (("una enfermedad", "un estado en el que el cuerpo funciona mal"), ("el sueño", "el descanso en el que no se está despierto"),
                     ("un medicamento", "lo que ayuda al enfermo"), ("un hospital", "una casa donde se cura a las personas")),
        "семья": (("los padres", "una madre y un padre"), ("un hermano", "un hijo de los mismos padres"),
                  ("una hermana", "una hija de los mismos padres"), ("una familia", "personas que viven juntas y son parientes")),
        "поведение": (("un hábito", "una acción que una persona repite sin pensar"), ("la atención", "aquello con lo que una persona elige qué notar"),
                      ("una intención", "lo que una persona va a hacer"), ("una necesidad", "lo que le falta a una persona"),
                      ("una emoción", "un estado que cambia la conducta"), ("el cansancio", "un estado en el que una persona trabaja peor")),
    },
}
# рамка определения и вопроса о нём
РАМКИ = {
    "ru": ("{т} — это {о}.", "что такое {т}? {т} — это {о}."),
    "en": ("{т} is {о}.", "what is {т}? {т} is {о}."),
    "de": ("{т} ist {о}.", "was ist {т}? {т} ist {о}."),
    "fr": ("{т}, c'est {о}.", "qu'est-ce que {т} ? {т}, c'est {о}."),
    "es": ("{т} es {о}.", "¿qué es {т}? {т} es {о}."),
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
