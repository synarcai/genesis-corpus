#!/usr/bin/env python3
"""ДОМ РЕЧЕВОГО ОБИХОДА — первое слово, которым человек начинает разговор.

Заказ владельца (04.09, через holon): владелец пробовал организм живьём и
написал ему «привет». Организм ПРОМОЛЧАЛ — и на «ты не знаешь, что такое
привет?» тоже. Это не изъян дорог: во всём своде (309 132 строки, 135 миров)
приветствий было РОВНО НОЛЬ. Продукт, чьё первое слово нечем ответить, не
имеет первого слова.

Дом объявляет девять языков атаки и пять форм, и все пять суть ПАРЫ показов
того же вида, что и прочие миры корпуса, — не «диалоговый режим», а материал:

  1. ПАРА ОБИХОДА — «привет. здравствуйте.», «спасибо. не за что.». Ответ
     берётся из СВОЕГО списка ответов, а не эхом: рынок обязан купить, что
     на благодарность отвечают иначе, чем благодарят.
  2. ОПРЕДЕЛЕНИЕ ОБИХОДА — «что такое привет? привет — это приветствие.»:
     тот же род, что дом определений, и тот же рынок купит его своим законом.
  3. ИМЯ — «как тебя зовут? меня зовут озарь.» Вопрос идёт ВЕЕРОМ («как
     твоё имя?», «кто ты такой?», «что ты такое?»): человек спрашивает одно
     разными словами, и продукт, знающий одну формулировку, молчит на
     второй — та же немота, ради которой дом и заказан. Имя организма объявлено ОДНОЙ
     строкой (`ИМЯ`), и рядом с ним в той же рамке стоят другие имена: рынок
     обязан купить РАМКУ, а не слово, — тот же закон, каким мир сочленений
     показывает веер в одной позиции.
  4. КТО ТЫ — «кто ты? я организм, который отвечает тем, что может
     обосновать.» Ответ говорит не о величии, а о ГРАНИЦЕ, и потому он
     верен: организм и вправду отвечает только обоснованным.
  5. ВЕЖЛИВОЕ НЕЗНАНИЕ — «что такое кваркозавр? я не знаю, что такое
     кваркозавр.» Это форма ЧЕСТНОГО ответа вместо молчания, и она нужна не
     меньше приветствия: молчание неотличимо от поломки, а «я не знаю»
     говорит о состоянии знания, и его можно проверить.

МАССА ПО ПРАВИЛУ (М-148, LAW² = 9): у всякого вида ≥3 зачина и ≥3 ответа,
то есть ≥9 разных пар на язык; списки объявлены здесь и нигде больше.

    python3 tools/dialogueforms.py    # самопроверка с мутантами
"""
import re

# ИМЯ ОРГАНИЗМА — ОДНОЙ СТРОКОЙ, НО ПИСЬМОМ СВОЕГО ЯЗЫКА. Оно входит в
# показы, и потому названо в одном месте: день, когда организм получит другое
# имя, стоит одной правки. Письмо объявлено, а не выведено: «me llamo озарь»
# есть кириллица посреди испанской фразы — слово, которое не пишет ни один
# язык корпуса, и суд письма назвал бы его ложью по праву.
ИМЯ = "ozar"
ИМЯ_ПИСЬМОМ = {"ru": "озарь"}


def имя_организма(язык):
    return ИМЯ_ПИСЬМОМ.get(язык, ИМЯ)

ПРИВЕТ, ПРОЩАНИЕ, БЛАГОДАРНОСТЬ, ИЗВИНЕНИЕ, СОГЛАСИЕ, ОТКАЗ = (
    "привет", "прощание", "благодарность", "извинение", "согласие", "отказ")
ВИДЫ = (ПРИВЕТ, ПРОЩАНИЕ, БЛАГОДАРНОСТЬ, ИЗВИНЕНИЕ, СОГЛАСИЕ, ОТКАЗ)
# у приветствия и прощания ответ берётся из ТОГО ЖЕ списка (на «привет»
# отвечают «здравствуйте»), у прочих — из своего
ЗЕРКАЛЬНЫЕ = (ПРИВЕТ, ПРОЩАНИЕ)

ЯЗЫКИ = {
    "ru": dict(
        зачины={ПРИВЕТ: ("привет", "здравствуйте", "доброе утро", "добрый день", "добрый вечер"),
                ПРОЩАНИЕ: ("пока", "до свидания", "до встречи", "всего доброго"),
                БЛАГОДАРНОСТЬ: ("спасибо", "большое спасибо", "благодарю"),
                ИЗВИНЕНИЕ: ("извините", "простите", "прошу прощения"),
                СОГЛАСИЕ: ("ответь, пожалуйста", "помоги, пожалуйста", "скажи, пожалуйста"),
                ОТКАЗ: ("нет", "к сожалению, нет", "не могу")},
        ответы={БЛАГОДАРНОСТЬ: ("пожалуйста", "не за что", "рад помочь"),
                ИЗВИНЕНИЕ: ("ничего страшного", "всё в порядке", "не беспокойтесь"),
                СОГЛАСИЕ: ("да", "конечно", "хорошо")},
        виды={ПРИВЕТ: "приветствие", ПРОЩАНИЕ: "прощание", БЛАГОДАРНОСТЬ: "благодарность",
              ИЗВИНЕНИЕ: "извинение", СОГЛАСИЕ: "просьба", ОТКАЗ: "отказ"},
        определение="что такое {с}? {с} — это {в}.",
        имя_воп=("как тебя зовут?", "как твоё имя?"), имя_отв="меня зовут {и}.",
        кто_воп=("кто ты?", "кто ты такой?", "что ты такое?"), кто_отв="я организм, который отвечает тем, что может обосновать.",
        незнание="что такое {н}? я не знаю, что такое {н}.",
        имена=(ИМЯ_ПИСЬМОМ["ru"], "анна", "пётр", "вера"),
        небылицы=("кваркозавр", "флюмбер", "зитоплекс"),
    ),
    "en": dict(
        зачины={ПРИВЕТ: ("hello", "hi", "good morning", "good afternoon", "good evening"),
                ПРОЩАНИЕ: ("goodbye", "bye", "see you", "farewell"),
                БЛАГОДАРНОСТЬ: ("thank you", "thanks", "thank you very much"),
                ИЗВИНЕНИЕ: ("sorry", "excuse me", "i am sorry"),
                СОГЛАСИЕ: ("answer, please", "help me, please", "tell me, please"),
                ОТКАЗ: ("no", "unfortunately not", "i cannot")},
        ответы={БЛАГОДАРНОСТЬ: ("you are welcome", "not at all", "glad to help"),
                ИЗВИНЕНИЕ: ("it is all right", "no problem", "do not worry"),
                СОГЛАСИЕ: ("yes", "of course", "all right")},
        виды={ПРИВЕТ: "a greeting", ПРОЩАНИЕ: "a farewell", БЛАГОДАРНОСТЬ: "a word of gratitude",
              ИЗВИНЕНИЕ: "an apology", СОГЛАСИЕ: "a request", ОТКАЗ: "a refusal"},
        определение="what is {с}? {с} is {в}.",
        имя_воп=("what is your name?", "how are you called?"), имя_отв="my name is {и}.",
        кто_воп=("who are you?", "what are you?", "tell me who you are."), кто_отв="i am an organism that answers only with what it can justify.",
        незнание="what is {н}? i do not know what {н} is.",
        имена=(ИМЯ, "ann", "peter", "vera"),
        небылицы=("quarkosaur", "flumber", "zitoplex"),
    ),
    "de": dict(
        зачины={ПРИВЕТ: ("hallo", "guten Morgen", "guten Tag", "guten Abend", "grüß dich"),
                ПРОЩАНИЕ: ("tschüss", "auf Wiedersehen", "bis bald", "leb wohl"),
                БЛАГОДАРНОСТЬ: ("danke", "vielen Dank", "danke schön"),
                ИЗВИНЕНИЕ: ("entschuldigung", "es tut mir leid", "verzeihung"),
                СОГЛАСИЕ: ("antworte bitte", "hilf mir bitte", "sag mir bitte"),
                ОТКАЗ: ("nein", "leider nicht", "ich kann nicht")},
        ответы={БЛАГОДАРНОСТЬ: ("bitte", "gern geschehen", "nichts zu danken"),
                ИЗВИНЕНИЕ: ("kein Problem", "schon gut", "mach dir nichts daraus"),
                СОГЛАСИЕ: ("ja", "natürlich", "in Ordnung")},
        виды={ПРИВЕТ: "eine Begrüßung", ПРОЩАНИЕ: "eine Verabschiedung", БЛАГОДАРНОСТЬ: "ein Dank",
              ИЗВИНЕНИЕ: "eine Entschuldigung", СОГЛАСИЕ: "eine Bitte", ОТКАЗ: "eine Ablehnung"},
        определение="was ist {с}? {с} ist {в}.",
        имя_воп=("wie heißt du?", "wie ist dein Name?"), имя_отв="ich heiße {и}.",
        кто_воп=("wer bist du?", "was bist du?", "sag mir, wer du bist."), кто_отв="ich bin ein Organismus, der nur mit dem antwortet, was er begründen kann.",
        незнание="was ist {н}? ich weiß nicht, was {н} ist.",
        имена=(ИМЯ, "Anna", "Paul", "Lena"),
        небылицы=("Quarkosaurus", "Flumber", "Zitoplex"),
    ),
    "fr": dict(
        зачины={ПРИВЕТ: ("bonjour", "salut", "bonsoir", "coucou"),
                ПРОЩАНИЕ: ("au revoir", "à bientôt", "à plus tard", "adieu"),
                БЛАГОДАРНОСТЬ: ("merci", "merci beaucoup", "je te remercie"),
                ИЗВИНЕНИЕ: ("pardon", "excusez-moi", "je suis désolé"),
                СОГЛАСИЕ: ("réponds, s'il te plaît", "aide-moi, s'il te plaît", "dis-moi, s'il te plaît"),
                ОТКАЗ: ("non", "malheureusement non", "je ne peux pas")},
        ответы={БЛАГОДАРНОСТЬ: ("de rien", "je t'en prie", "avec plaisir"),
                ИЗВИНЕНИЕ: ("ce n'est rien", "pas de problème", "ne t'inquiète pas"),
                СОГЛАСИЕ: ("oui", "bien sûr", "d'accord")},
        виды={ПРИВЕТ: "une salutation", ПРОЩАНИЕ: "un adieu", БЛАГОДАРНОСТЬ: "un remerciement",
              ИЗВИНЕНИЕ: "une excuse", СОГЛАСИЕ: "une demande", ОТКАЗ: "un refus"},
        определение="qu'est-ce que {с} ? {с} est {в}.",
        имя_воп=("comment t'appelles-tu ?", "quel est ton nom ?"), имя_отв="je m'appelle {и}.",
        кто_воп=("qui es-tu ?", "qu'est-ce que tu es ?", "dis-moi qui tu es."), кто_отв="je suis un organisme qui ne répond que par ce qu'il peut justifier.",
        незнание="qu'est-ce que {н} ? je ne sais pas ce qu'est {н}.",
        имена=(ИМЯ, "Anne", "Paul", "Marie"),
        небылицы=("quarkosaure", "flumbère", "zitoplexe"),
    ),
    "es": dict(
        зачины={ПРИВЕТ: ("hola", "buenos días", "buenas tardes", "buenas noches"),
                ПРОЩАНИЕ: ("adiós", "hasta luego", "hasta pronto", "nos vemos"),
                БЛАГОДАРНОСТЬ: ("gracias", "muchas gracias", "te lo agradezco"),
                ИЗВИНЕНИЕ: ("perdón", "disculpe", "lo siento"),
                СОГЛАСИЕ: ("responde, por favor", "ayúdame, por favor", "dime, por favor"),
                ОТКАЗ: ("no", "lamentablemente no", "no puedo")},
        ответы={БЛАГОДАРНОСТЬ: ("de nada", "no hay de qué", "con gusto"),
                ИЗВИНЕНИЕ: ("no pasa nada", "no hay problema", "no te preocupes"),
                СОГЛАСИЕ: ("sí", "claro", "de acuerdo")},
        виды={ПРИВЕТ: "un saludo", ПРОЩАНИЕ: "una despedida", БЛАГОДАРНОСТЬ: "un agradecimiento",
              ИЗВИНЕНИЕ: "una disculpa", СОГЛАСИЕ: "una petición", ОТКАЗ: "un rechazo"},
        определение="¿qué es {с}? {с} es {в}.",
        имя_воп=("¿cómo te llamas?", "¿cuál es tu nombre?"), имя_отв="me llamo {и}.",
        кто_воп=("¿quién eres?", "¿qué eres?", "dime quién eres."), кто_отв="soy un organismo que solo responde con lo que puede justificar.",
        незнание="¿qué es {н}? no sé qué es {н}.",
        имена=(ИМЯ, "Ana", "Pablo", "Marta"),
        небылицы=("cuarcosaurio", "flumbero", "zitoplex"),
    ),
    "it": dict(
        зачины={ПРИВЕТ: ("ciao", "buongiorno", "buonasera", "salve"),
                ПРОЩАНИЕ: ("arrivederci", "a presto", "a dopo", "addio"),
                БЛАГОДАРНОСТЬ: ("grazie", "grazie mille", "ti ringrazio"),
                ИЗВИНЕНИЕ: ("scusa", "mi dispiace", "chiedo scusa"),
                СОГЛАСИЕ: ("rispondi, per favore", "aiutami, per favore", "dimmi, per favore"),
                ОТКАЗ: ("no", "purtroppo no", "non posso")},
        ответы={БЛАГОДАРНОСТЬ: ("prego", "di niente", "con piacere"),
                ИЗВИНЕНИЕ: ("non fa niente", "nessun problema", "non preoccuparti"),
                СОГЛАСИЕ: ("sì", "certo", "va bene")},
        виды={ПРИВЕТ: "un saluto", ПРОЩАНИЕ: "un congedo", БЛАГОДАРНОСТЬ: "un ringraziamento",
              ИЗВИНЕНИЕ: "una scusa", СОГЛАСИЕ: "una richiesta", ОТКАЗ: "un rifiuto"},
        определение="che cos'è {с}? {с} è {в}.",
        имя_воп=("come ti chiami?", "qual è il tuo nome?"), имя_отв="mi chiamo {и}.",
        кто_воп=("chi sei?", "che cosa sei?", "dimmi chi sei."), кто_отв="sono un organismo che risponde solo con ciò che può giustificare.",
        незнание="che cos'è {н}? non so che cos'è {н}.",
        имена=(ИМЯ, "Anna", "Marco", "Giulia"),
        небылицы=("quarcosauro", "flumbero", "zitoplesso"),
    ),
    "pt": dict(
        зачины={ПРИВЕТ: ("olá", "bom dia", "boa tarde", "boa noite"),
                ПРОЩАНИЕ: ("adeus", "até logo", "até breve", "tchau"),
                БЛАГОДАРНОСТЬ: ("obrigado", "muito obrigado", "agradeço"),
                ИЗВИНЕНИЕ: ("desculpe", "perdão", "lamento"),
                СОГЛАСИЕ: ("responde, por favor", "ajuda-me, por favor", "diz-me, por favor"),
                ОТКАЗ: ("não", "infelizmente não", "não posso")},
        ответы={БЛАГОДАРНОСТЬ: ("de nada", "não há de quê", "com prazer"),
                ИЗВИНЕНИЕ: ("não faz mal", "sem problema", "não te preocupes"),
                СОГЛАСИЕ: ("sim", "claro", "está bem")},
        виды={ПРИВЕТ: "uma saudação", ПРОЩАНИЕ: "uma despedida", БЛАГОДАРНОСТЬ: "um agradecimento",
              ИЗВИНЕНИЕ: "um pedido de desculpa", СОГЛАСИЕ: "um pedido", ОТКАЗ: "uma recusa"},
        определение="o que é {с}? {с} é {в}.",
        имя_воп=("como te chamas?", "qual é o teu nome?"), имя_отв="chamo-me {и}.",
        кто_воп=("quem és tu?", "o que és tu?", "diz-me quem és."), кто_отв="sou um organismo que só responde com o que pode justificar.",
        незнание="o que é {н}? não sei o que é {н}.",
        имена=(ИМЯ, "Ana", "Pedro", "Maria"),
        небылицы=("quarcossauro", "flumbero", "zitoplexo"),
    ),
    "nl": dict(
        зачины={ПРИВЕТ: ("hallo", "goedemorgen", "goedemiddag", "goedenavond", "hoi"),
                ПРОЩАНИЕ: ("dag", "tot ziens", "tot straks", "vaarwel"),
                БЛАГОДАРНОСТЬ: ("dank je", "bedankt", "dank u wel"),
                ИЗВИНЕНИЕ: ("sorry", "pardon", "het spijt me"),
                СОГЛАСИЕ: ("antwoord alsjeblieft", "help me alsjeblieft", "zeg het me alsjeblieft"),
                ОТКАЗ: ("nee", "helaas niet", "ik kan niet")},
        ответы={БЛАГОДАРНОСТЬ: ("graag gedaan", "geen dank", "met plezier"),
                ИЗВИНЕНИЕ: ("geeft niet", "geen probleem", "maak je geen zorgen"),
                СОГЛАСИЕ: ("ja", "natuurlijk", "goed")},
        виды={ПРИВЕТ: "een begroeting", ПРОЩАНИЕ: "een afscheid", БЛАГОДАРНОСТЬ: "een dank",
              ИЗВИНЕНИЕ: "een verontschuldiging", СОГЛАСИЕ: "een verzoek", ОТКАЗ: "een weigering"},
        определение="wat is {с}? {с} is {в}.",
        имя_воп=("hoe heet je?", "wat is je naam?"), имя_отв="ik heet {и}.",
        кто_воп=("wie ben je?", "wat ben je?", "zeg me wie je bent."), кто_отв="ik ben een organisme dat alleen antwoordt met wat het kan onderbouwen.",
        незнание="wat is {н}? ik weet niet wat {н} is.",
        имена=(ИМЯ, "Anna", "Piet", "Lena"),
        небылицы=("quarkosaurus", "flumber", "zitoplex"),
    ),
    "pl": dict(
        зачины={ПРИВЕТ: ("cześć", "dzień dobry", "dobry wieczór", "witam"),
                ПРОЩАНИЕ: ("do widzenia", "pa", "do zobaczenia", "żegnaj"),
                БЛАГОДАРНОСТЬ: ("dziękuję", "dzięki", "bardzo dziękuję"),
                ИЗВИНЕНИЕ: ("przepraszam", "wybacz", "bardzo przepraszam"),
                СОГЛАСИЕ: ("odpowiedz, proszę", "pomóż mi, proszę", "powiedz mi, proszę"),
                ОТКАЗ: ("nie", "niestety nie", "nie mogę")},
        ответы={БЛАГОДАРНОСТЬ: ("proszę", "nie ma za co", "cała przyjemność po mojej stronie"),
                ИЗВИНЕНИЕ: ("nic się nie stało", "nie ma problemu", "nie martw się"),
                СОГЛАСИЕ: ("tak", "oczywiście", "dobrze")},
        виды={ПРИВЕТ: "powitanie", ПРОЩАНИЕ: "pożegnanie", БЛАГОДАРНОСТЬ: "podziękowanie",
              ИЗВИНЕНИЕ: "przeprosiny", СОГЛАСИЕ: "prośba", ОТКАЗ: "odmowa"},
        определение="co to jest {с}? {с} to {в}.",
        имя_воп=("jak masz na imię?", "jak się nazywasz?"), имя_отв="mam na imię {и}.",
        кто_воп=("kim jesteś?", "czym jesteś?", "powiedz mi, kim jesteś."), кто_отв="jestem organizmem, który odpowiada tylko tym, co potrafi uzasadnić.",
        незнание="co to jest {н}? nie wiem, co to jest {н}.",
        имена=(ИМЯ, "Anna", "Piotr", "Zofia"),
        небылицы=("kwarkozaur", "flumber", "zitopleks"),
    ),
}
ФОРМЫ = ("пара", "определение", "имя", "кто", "незнание")

# МАССА ПО ПРАВИЛУ: у всякого вида с парой ≥3 зачина и ≥3 ответа
for _яз, _я in ЯЗЫКИ.items():
    for _в in ВИДЫ:
        _зач = _я["зачины"][_в]
        _отв = _зач if _в in ЗЕРКАЛЬНЫЕ else _я["ответы"].get(_в, ())
        if _отв:
            assert len(_зач) >= 3 and len(_отв) >= 3, (_яз, _в, len(_зач), len(_отв))
    assert set(_я["виды"]) == set(ВИДЫ), (_яз, "вид объявлен не всякому роду")


def ответы(язык, вид):
    я = ЯЗЫКИ[язык]
    return я["зачины"][вид] if вид in ЗЕРКАЛЬНЫЕ else я["ответы"].get(вид, ())


def страница(язык, форма, вид=None, i=0, j=0):
    я = ЯЗЫКИ[язык]
    if форма == "пара":
        зач, отв = я["зачины"][вид], ответы(язык, вид)
        return f"{зач[i % len(зач)]}. {отв[j % len(отв)]}."
    if форма == "определение":
        зач = я["зачины"][вид]
        return я["определение"].format(с=зач[i % len(зач)], в=я["виды"][вид])
    if форма == "имя":
        имена, вопросы = я["имена"], я["имя_воп"]
        return f"{вопросы[j % len(вопросы)]} {я['имя_отв'].format(и=имена[i % len(имена)])}"
    if форма == "кто":
        вопросы = я["кто_воп"]
        return f"{вопросы[i % len(вопросы)]} {я['кто_отв']}"
    небылицы = я["небылицы"]
    return я["незнание"].format(н=небылицы[i % len(небылицы)])


# --- сторона суда: строка судится ПЕРЕПИСЫВАНИЕМ ---
def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for вид in ВИДЫ:
            зач = я["зачины"][вид]
            отв = ответы(язык, вид)
            for i in range(len(зач)):
                вон[страница(язык, "определение", вид, i)] = (язык, "определение")
                for j in range(len(отв)):
                    вон[страница(язык, "пара", вид, i, j)] = (язык, "пара")
        for i in range(len(я["имена"])):
            for j in range(len(я["имя_воп"])):
                вон[страница(язык, "имя", i=i, j=j)] = (язык, "имя")
        for i in range(len(я["кто_воп"])):
            вон[страница(язык, "кто", i=i)] = (язык, "кто")
        for i in range(len(я["небылицы"])):
            вон[страница(язык, "незнание", i=i)] = (язык, "незнание")
    return вон


ПОКАЗЫ = _все_показы()
# РАМКИ БЕЗ СЛОВ — для суда о ЧУЖОМ слове в объявленной рамке: строка, севшая
# в рамку дома, но с незнакомым словом, есть ЛОЖЬ, а не молчание.
_РАМКИ = tuple(re.compile("^" + re.escape(ш).replace(r"\{с\}", "(.+?)")
                          .replace(r"\{в\}", "(.+?)").replace(r"\{н\}", "(.+?)")
                          .replace(r"\{и\}", "(.+?)") + "$")
               for я in ЯЗЫКИ.values()
               for ш in (я["определение"], я["незнание"])
               + tuple(f"{в} {я['имя_отв']}" for в in я["имя_воп"]))


def судить(строка):
    """(судимо, истинно): показ дома истинен; строка, севшая в объявленную
    рамку с чужим словом, — ложна; всё прочее дому не подсудно."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    if any(р.match(с) for р in _РАМКИ):
        return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        for форма in ФОРМЫ:
            вид = ПРИВЕТ if форма in ("пара", "определение") else None
            с = страница(язык, форма, вид)
            судимо, истинно = судить(с)
            assert судимо and истинно, (язык, форма, с)
        # МУТАНТ: определение, назвавшее ЧУЖОЙ вид, обязано быть ложью
        битое = я["определение"].format(с=я["зачины"][ПРИВЕТ][0], в=я["виды"][ПРОЩАНИЕ])
        судимо, истинно = судить(битое)
        assert судимо and not истинно, (язык, битое)
        мутанты += 1
        # МУТАНТ: ответ не своего вида («спасибо. до свидания.») дому не подсуден,
        # но и показом не зовётся — пара объявлена своими списками
        чужая = f"{я['зачины'][БЛАГОДАРНОСТЬ][0]}. {я['зачины'][ПРОЩАНИЕ][0]}."
        assert чужая not in ПОКАЗЫ, (язык, чужая)
        мутанты += 1
        # МУТАНТ: незнание о ЗНАКОМОМ слове — ложь («что такое привет? я не знаю…»)
        битое2 = я["незнание"].format(н=я["зачины"][ПРИВЕТ][0])
        судимо, истинно = судить(битое2)
        assert судимо and not истинно, (язык, битое2)
        мутанты += 1
    for язык in ("ru", "en", "de"):
        print("  ", страница(язык, "пара", ПРИВЕТ, 0, 1))
        print("  ", страница(язык, "определение", БЛАГОДАРНОСТЬ, 0))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, видов {len(ВИДЫ)})")


if __name__ == "__main__":
    _самопроверка()
