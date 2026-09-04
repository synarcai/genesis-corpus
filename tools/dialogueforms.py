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
        зачины={ПРИВЕТ: ("привет", "здравствуй", "доброе утро", "добрый день", "добрый вечер"),
                ПРОЩАНИЕ: ("пока", "до свидания", "до встречи", "всего доброго"),
                БЛАГОДАРНОСТЬ: ("спасибо", "большое спасибо", "благодарю"),
                ИЗВИНЕНИЕ: ("извини", "прости", "прошу прощения"),
                СОГЛАСИЕ: ("ответь, пожалуйста", "помоги, пожалуйста", "скажи, пожалуйста"),
                ОТКАЗ: ("нет", "к сожалению, нет", "не могу")},
        ответы={БЛАГОДАРНОСТЬ: ("пожалуйста", "не за что", "рад помочь"),
                ИЗВИНЕНИЕ: ("ничего страшного", "всё в порядке", "не беспокойся"),
                СОГЛАСИЕ: ("да", "конечно", "хорошо")},
        виды={ПРИВЕТ: "приветствие", ПРОЩАНИЕ: "прощание", БЛАГОДАРНОСТЬ: "благодарность",
              ИЗВИНЕНИЕ: "извинение", СОГЛАСИЕ: "просьба", ОТКАЗ: "отказ"},
        определение="что такое {с}? {с} — это {в}.",
        имя_воп=("как тебя зовут?", "как твоё имя?"), имя_отв="меня зовут {и}.",
        кто_воп=("кто ты?", "кто ты такой?", "что ты такое?"), кто_отв="я организм, который отвечает тем, что может обосновать.",
        незнание="что такое {н}? я не знаю, что такое {н}.",
        малый=((("как дела?", "как ты?", "как поживаешь?"),
                ("я отвечаю тем, что могу обосновать.", "хорошо: я отвечаю и проверяю ответы.", "как всегда: отвечаю на то, что могу обосновать.")),
               (("что нового?", "какие новости?", "есть что-нибудь новое?"),
                ("я узнаю новое из того, что мне показывают.", "новое приходит ко мне с показами.", "нового ровно столько, сколько мне показали.")),
               (("чем занимаешься?", "что ты делаешь?", "чем ты занят?"),
                ("я отвечаю на вопросы и проверяю ответы.", "отвечаю и проверяю, из чего вышел ответ.", "я разбираю вопрос и ищу, чем его обосновать.")),
               (("что ты умеешь?", "что ты можешь?", "на что ты способен?"),
                ("я умею отвечать на вопрос и показывать, из чего вышел ответ.", "я могу ответить и показать основание ответа.", "я умею одно: отвечать тем, что могу обосновать."))),
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
        малый=((("how are you?", "how are you doing?", "how is it going?"),
                ("i answer with what i can justify.", "well: i answer and check the answers.", "as always: i answer what i can justify.")),
               (("what is new?", "any news?", "anything new?"),
                ("i learn what is new from what is shown to me.", "the new comes to me with the shows.", "exactly as much is new as i have been shown.")),
               (("what are you doing?", "what are you up to?", "what are you busy with?"),
                ("i answer questions and check the answers.", "i answer and check what the answer came from.", "i take a question apart and look for its ground.")),
               (("what can you do?", "what are you able to do?", "what are you good at?"),
                ("i can answer a question and show what the answer came from.", "i can answer and show the ground of the answer.", "i can do one thing: answer with what i can justify."))),
        имена=(ИМЯ, "ann", "peter", "vera"),
        небылицы=("quarkosaur", "flumber", "zitoplex", "a quarkosaur", "a flumber", "a zitoplex"),
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
        малый=((("wie geht es dir?", "wie geht's?", "wie läuft es?"),
                ("ich antworte mit dem, was ich begründen kann.", "gut: ich antworte und prüfe die Antworten.", "wie immer: ich antworte auf das, was ich begründen kann.")),
               (("was gibt es Neues?", "gibt es Neuigkeiten?", "etwas Neues?"),
                ("ich erfahre Neues aus dem, was mir gezeigt wird.", "das Neue kommt mit den Beispielen zu mir.", "neu ist genau so viel, wie man mir gezeigt hat.")),
               (("was machst du?", "womit bist du beschäftigt?", "was tust du gerade?"),
                ("ich beantworte Fragen und prüfe die Antworten.", "ich antworte und prüfe, woraus die Antwort kam.", "ich zerlege die Frage und suche ihren Grund.")),
               (("was kannst du?", "wozu bist du fähig?", "was kannst du gut?"),
                ("ich kann eine Frage beantworten und zeigen, woraus die Antwort kam.", "ich kann antworten und den Grund der Antwort zeigen.", "ich kann eines: mit dem antworten, was ich begründen kann."))),
        имена=(ИМЯ, "Anna", "Paul", "Lena"),
        небылицы=("Quarkosaurus", "Flumber", "Zitoplex", "ein Quarkosaurier", "ein Flumber", "ein Zitoplex"),
    ),
    "fr": dict(
        зачины={ПРИВЕТ: ("bonjour", "salut", "bonsoir", "coucou"),
                ПРОЩАНИЕ: ("au revoir", "à bientôt", "à plus tard", "adieu"),
                БЛАГОДАРНОСТЬ: ("merci", "merci beaucoup", "je te remercie"),
                ИЗВИНЕНИЕ: ("pardon", "excuse-moi", "je suis désolé"),
                СОГЛАСИЕ: ("réponds, s'il te plaît", "aide-moi, s'il te plaît", "dis-moi, s'il te plaît"),
                ОТКАЗ: ("non", "malheureusement non", "je ne peux pas")},
        ответы={БЛАГОДАРНОСТЬ: ("de rien", "je t'en prie", "avec plaisir"),
                ИЗВИНЕНИЕ: ("ce n'est rien", "pas de problème", "ne t'inquiète pas"),
                СОГЛАСИЕ: ("oui", "bien sûr", "d'accord")},
        виды={ПРИВЕТ: "une salutation", ПРОЩАНИЕ: "un adieu", БЛАГОДАРНОСТЬ: "un remerciement",
              ИЗВИНЕНИЕ: "une excuse", СОГЛАСИЕ: "une demande", ОТКАЗ: "un refus"},
        определение="qu'est-ce {ЧТО}{с} ? {с} est {в}.",
        имя_воп=("comment t'appelles-tu ?", "quel est ton nom ?"), имя_отв="je m'appelle {и}.",
        кто_воп=("qui es-tu ?", "qu'est-ce que tu es ?", "dis-moi qui tu es."), кто_отв="je suis un organisme qui ne répond que par ce qu'il peut justifier.",
        незнание="qu'est-ce {ЧТО}{н} ? je ne sais pas ce qu'est {н}.",
        малый=((("comment vas-tu ?", "ça va ?", "comment ça va ?"),
                ("je réponds par ce que je peux justifier.", "bien : je réponds et je vérifie les réponses.", "comme toujours : je réponds à ce que je peux justifier.")),
               (("quoi de neuf ?", "des nouvelles ?", "rien de nouveau ?"),
                ("j'apprends le nouveau à partir de ce qu'on me montre.", "le nouveau me vient avec les exemples.", "il y a de nouveau exactement ce qu'on m'a montré.")),
               (("que fais-tu ?", "qu'est-ce que tu fais ?", "tu fais quoi ?"),
                ("je réponds aux questions et je vérifie les réponses.", "je réponds et je vérifie d'où vient la réponse.", "je décompose la question et je cherche son fondement.")),
               (("que sais-tu faire ?", "qu'est-ce que tu sais faire ?", "de quoi es-tu capable ?"),
                ("je sais répondre à une question et montrer d'où vient la réponse.", "je sais répondre et montrer le fondement de la réponse.", "je sais une chose : répondre par ce que je peux justifier."))),
        имена=(ИМЯ, "Anne", "Paul", "Marie"),
        небылицы=("quarkosaure", "flumbère", "zitoplexe", "un quarkosaure", "un flumbère", "un zitoplexe"),
    ),
    "es": dict(
        зачины={ПРИВЕТ: ("hola", "buenos días", "buenas tardes", "buenas noches"),
                ПРОЩАНИЕ: ("adiós", "hasta luego", "hasta pronto", "nos vemos"),
                БЛАГОДАРНОСТЬ: ("gracias", "muchas gracias", "te lo agradezco"),
                ИЗВИНЕНИЕ: ("perdón", "disculpa", "lo siento"),
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
        малый=((("¿cómo estás?", "¿qué tal?", "¿cómo te va?"),
                ("respondo con lo que puedo justificar.", "bien: respondo y compruebo las respuestas.", "como siempre: respondo a lo que puedo justificar.")),
               (("¿qué hay de nuevo?", "¿alguna novedad?", "¿algo nuevo?"),
                ("aprendo lo nuevo de lo que se me muestra.", "lo nuevo me llega con los ejemplos.", "hay de nuevo exactamente lo que se me ha mostrado.")),
               (("¿qué haces?", "¿en qué andas?", "¿qué estás haciendo?"),
                ("respondo preguntas y compruebo las respuestas.", "respondo y compruebo de dónde vino la respuesta.", "desarmo la pregunta y busco su fundamento.")),
               (("¿qué sabes hacer?", "¿qué puedes hacer?", "¿de qué eres capaz?"),
                ("sé responder a una pregunta y mostrar de dónde vino la respuesta.", "sé responder y mostrar el fundamento de la respuesta.", "sé una cosa: responder con lo que puedo justificar."))),
        имена=(ИМЯ, "Ana", "Pablo", "Marta"),
        небылицы=("cuarcosaurio", "flumbero", "zitoplex", "un cuarcosaurio", "un flumbero", "un zitoplex"),
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
        малый=((("come stai?", "come va?", "tutto bene?"),
                ("rispondo con ciò che posso giustificare.", "bene: rispondo e controllo le risposte.", "come sempre: rispondo a ciò che posso giustificare.")),
               (("che c'è di nuovo?", "novità?", "niente di nuovo?"),
                ("imparo il nuovo da ciò che mi viene mostrato.", "il nuovo mi arriva con gli esempi.", "di nuovo c'è esattamente quello che mi è stato mostrato.")),
               (("che cosa fai?", "che stai facendo?", "di che cosa ti occupi?"),
                ("rispondo alle domande e controllo le risposte.", "rispondo e controllo da dove viene la risposta.", "scompongo la domanda e cerco il suo fondamento.")),
               (("che cosa sai fare?", "che cosa puoi fare?", "di che cosa sei capace?"),
                ("so rispondere a una domanda e mostrare da dove viene la risposta.", "so rispondere e mostrare il fondamento della risposta.", "so una cosa: rispondere con ciò che posso giustificare."))),
        имена=(ИМЯ, "Anna", "Marco", "Giulia"),
        небылицы=("quarcosauro", "flumbero", "zitoplesso", "un quarcosauro", "un flumbero", "un zitoplesso"),
    ),
    "pt": dict(
        зачины={ПРИВЕТ: ("olá", "bom dia", "boa tarde", "boa noite"),
                ПРОЩАНИЕ: ("adeus", "até logo", "até breve", "tchau"),
                БЛАГОДАРНОСТЬ: ("obrigado", "muito obrigado", "agradeço"),
                ИЗВИНЕНИЕ: ("desculpa", "perdão", "lamento"),
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
        малый=((("como estás?", "tudo bem?", "como vais?"),
                ("respondo com aquilo que posso justificar.", "bem: respondo e verifico as respostas.", "como sempre: respondo ao que posso justificar.")),
               (("o que há de novo?", "alguma novidade?", "algo de novo?"),
                ("aprendo o novo a partir do que me é mostrado.", "o novo chega-me com os exemplos.", "de novo há exatamente o que me foi mostrado.")),
               (("o que fazes?", "o que estás a fazer?", "em que andas?"),
                ("respondo a perguntas e verifico as respostas.", "respondo e verifico de onde veio a resposta.", "desmonto a pergunta e procuro o seu fundamento.")),
               (("o que sabes fazer?", "o que consegues fazer?", "de que és capaz?"),
                ("sei responder a uma pergunta e mostrar de onde veio a resposta.", "sei responder e mostrar o fundamento da resposta.", "sei uma coisa: responder com aquilo que posso justificar."))),
        имена=(ИМЯ, "Ana", "Pedro", "Maria"),
        небылицы=("quarcossauro", "flumbero", "zitoplexo", "um quarcossauro", "um flumbero", "um zitoplexo"),
    ),
    "nl": dict(
        зачины={ПРИВЕТ: ("hallo", "goedemorgen", "goedemiddag", "goedenavond", "hoi"),
                ПРОЩАНИЕ: ("dag", "tot ziens", "tot straks", "vaarwel"),
                БЛАГОДАРНОСТЬ: ("dank je", "bedankt", "dank je wel"),
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
        малый=((("hoe gaat het?", "hoe is het?", "alles goed?"),
                ("ik antwoord met wat ik kan onderbouwen.", "goed: ik antwoord en controleer de antwoorden.", "zoals altijd: ik antwoord op wat ik kan onderbouwen.")),
               (("wat is er nieuw?", "nog nieuws?", "iets nieuws?"),
                ("ik leer het nieuwe uit wat mij getoond wordt.", "het nieuwe komt met de voorbeelden naar mij.", "nieuw is precies zoveel als mij getoond is.")),
               (("wat doe je?", "waar ben je mee bezig?", "wat ben je aan het doen?"),
                ("ik beantwoord vragen en controleer de antwoorden.", "ik antwoord en controleer waar het antwoord vandaan komt.", "ik haal de vraag uit elkaar en zoek haar grond.")),
               (("wat kun je?", "waartoe ben je in staat?", "waar ben je goed in?"),
                ("ik kan een vraag beantwoorden en tonen waar het antwoord vandaan komt.", "ik kan antwoorden en de grond van het antwoord tonen.", "ik kan één ding: antwoorden met wat ik kan onderbouwen."))),
        имена=(ИМЯ, "Anna", "Piet", "Lena"),
        небылицы=("quarkosaurus", "flumber", "zitoplex", "een quarkosaurus", "een flumber", "een zitoplex"),
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
        определение2="czym jest {с}? {с} to {в}.",
        имя_воп=("jak masz na imię?", "jak się nazywasz?"), имя_отв="mam na imię {и}.",
        кто_воп=("kim jesteś?", "czym jesteś?", "powiedz mi, kim jesteś."), кто_отв="jestem organizmem, który odpowiada tylko tym, co potrafi uzasadnić.",
        незнание="co to jest {н}? nie wiem, co to jest {н}.",
        малый=((("jak się masz?", "co słychać?", "jak leci?"),
                ("odpowiadam tym, co potrafię uzasadnić.", "dobrze: odpowiadam i sprawdzam odpowiedzi.", "jak zawsze: odpowiadam na to, co potrafię uzasadnić.")),
               (("co nowego?", "jakieś nowości?", "coś nowego?"),
                ("uczę się nowego z tego, co mi pokazano.", "nowe przychodzi do mnie z przykładami.", "nowego jest dokładnie tyle, ile mi pokazano.")),
               (("co robisz?", "czym się zajmujesz?", "co teraz robisz?"),
                ("odpowiadam na pytania i sprawdzam odpowiedzi.", "odpowiadam i sprawdzam, z czego wyszła odpowiedź.", "rozkładam pytanie i szukam jego podstawy.")),
               (("co potrafisz?", "co umiesz?", "do czego jesteś zdolny?"),
                ("potrafię odpowiedzieć na pytanie i pokazać, z czego wyszła odpowiedź.", "potrafię odpowiedzieć i pokazać podstawę odpowiedzi.", "potrafię jedno: odpowiadać tym, co potrafię uzasadnić."))),
        имена=(ИМЯ, "Anna", "Piotr", "Zofia"),
        небылицы=("kwarkozaur", "flumber", "zitopleks"),
    ),
}

# --- ВЕЖЛИВОЕ ОБРАЩЕНИЕ ---
#
# Замер 04.09 по всему своду: «ты» 92 строки, «вы» НОЛЬ; «du» 220, «Sie» ноль;
# «tu» 117, «vous» ноль; «usted» ноль, «Lei» ноль. Дом обихода — тот, которым
# человек начинает разговор, — обращался на «ты» ко всякому. Это не пустая
# клетка: это форма, которой корпус учил бы УВЕРЕННО И НЕВЕРНО, а по-русски,
# по-немецки, по-французски, по-испански, по-итальянски и по-польски «ты» в
# лицо незнакомому есть не оттенок, а грубость.
#
# ВЕЖЛИВАЯ РАМКА ЕСТЬ НЕФОРМАЛЬНАЯ С ОБЪЯВЛЕННОЙ ЗАМЕНОЙ, А НЕ ВТОРАЯ РУКОПИСЬ.
# Объявляется ровно словарь замен; всё прочее — рамки, ответы, виды, имена —
# берётся у неформального дома неизменным. Пара строк, различающихся ровно
# обращением, есть тот показ, из которого рынок покупает закон регистра
# анти-унификацией: общее уходит в рамку, различие остаётся дырой.
#
# ЗАМЕНА ИДЁТ УЗЛОМ, А НЕ СЛОВОМ (04.09, спор с holon). Польский вежливый
# ставит вместо второго лица СУЩЕСТВИТЕЛЬНОЕ третьего («czy się zgadzasz» →
# «czy pan się zgadza»), и глагол идёт за подлежащим, а не за регистром;
# немецкий делает то же третьим лицом множественного. Потому объявляется
# ЦЕЛАЯ СТРОКА в обеих одеждах, а не местоимение с поправкой: строка есть узел
# со всем, что от него зависит, и подмена местоимения сломалась бы на первом
# же языке, где меняется лицо, падеж или род.
#
# АНГЛИЙСКИЙ ПИШЕТ ОДНУ ФОРМУ, И ЭТО ОБЪЯВЛЕНО (М-279). «You» служит обоим
# регистрам, вежливый показ совпал бы с неформальным слово в слово, и корпус
# понёс бы двойника ради ровной решётки. Словарь замен английского ПУСТ, и
# пустота эта названа домом, а не выведена прибором из молчания.
ВЕЖЛИВО = {
    "ru": {"как ты?": "как вы?", "как поживаешь?": "как поживаете?", "что ты делаешь?": "что вы делаете?", "чем ты занят?": "чем вы заняты?", "что ты можешь?": "что вы можете?", "на что ты способен?": "на что вы способны?", "здравствуй": "здравствуйте", "извини": "извините", "прости": "простите",
           "не беспокойся": "не беспокойтесь", "как тебя зовут?": "как вас зовут?", "как твоё имя?": "как ваше имя?",
           "кто ты?": "кто вы?", "кто ты такой?": "кто вы такой?",
           "что ты такое?": "что вы такое?", "как дела?": "как ваши дела?",
           "чем занимаешься?": "чем вы занимаетесь?", "что ты умеешь?": "что вы умеете?",
           "ответь, пожалуйста": "ответьте, пожалуйста",
           "помоги, пожалуйста": "помогите, пожалуйста",
           "скажи, пожалуйста": "скажите, пожалуйста"},
    "en": {},
    "de": {"wie geht's?": "wie geht es Ihnen?", "womit bist du beschäftigt?": "womit sind Sie beschäftigt?", "was tust du gerade?": "was tun Sie gerade?", "wozu bist du fähig?": "wozu sind Sie fähig?", "was kannst du gut?": "was können Sie gut?", "wie heißt du?": "wie heißen Sie?", "wie ist dein Name?": "wie ist Ihr Name?",
           "wer bist du?": "wer sind Sie?", "was bist du?": "was sind Sie?",
           "sag mir, wer du bist.": "sagen Sie mir, wer Sie sind.",
           "wie geht es dir?": "wie geht es Ihnen?", "was machst du?": "was machen Sie?",
           "was kannst du?": "was können Sie?", "antworte bitte": "antworten Sie bitte",
           "hilf mir bitte": "helfen Sie mir bitte", "sag mir bitte": "sagen Sie mir bitte",
           "mach dir nichts daraus": "machen Sie sich nichts daraus"},
    "fr": {"ça va ?": "vous allez bien ?", "comment ça va ?": "comment allez-vous ?", "qu'est-ce que tu fais ?": "qu'est-ce que vous faites ?", "tu fais quoi ?": "vous faites quoi ?", "qu'est-ce que tu sais faire ?": "qu'est-ce que vous savez faire ?", "de quoi es-tu capable ?": "de quoi êtes-vous capable ?", "excuse-moi": "excusez-moi", "comment t'appelles-tu ?": "comment vous appelez-vous ?",
           "quel est ton nom ?": "quel est votre nom ?",
           "qui es-tu ?": "qui êtes-vous ?", "qu'est-ce que tu es ?": "qu'est-ce que vous êtes ?",
           "dis-moi qui tu es.": "dites-moi qui vous êtes.",
           "comment vas-tu ?": "comment allez-vous ?", "que fais-tu ?": "que faites-vous ?",
           "que sais-tu faire ?": "que savez-vous faire ?",
           "réponds, s'il te plaît": "répondez, s'il vous plaît",
           "aide-moi, s'il te plaît": "aidez-moi, s'il vous plaît",
           "dis-moi, s'il te plaît": "dites-moi, s'il vous plaît",
           "je te remercie": "je vous remercie", "ne t'inquiète pas": "ne vous inquiétez pas",
           "je t'en prie": "je vous en prie"},
    "es": {"¿cómo te va?": "¿cómo le va?", "¿en qué andas?": "¿en qué anda usted?", "¿qué estás haciendo?": "¿qué está haciendo usted?", "¿qué puedes hacer?": "¿qué puede hacer usted?", "¿de qué eres capaz?": "¿de qué es capaz usted?", "disculpa": "disculpe", "¿cómo te llamas?": "¿cómo se llama usted?", "¿cuál es tu nombre?": "¿cuál es su nombre?",
           "¿quién eres?": "¿quién es usted?", "¿qué eres?": "¿qué es usted?",
           "dime quién eres.": "dígame quién es usted.", "¿cómo estás?": "¿cómo está usted?",
           "¿qué haces?": "¿qué hace usted?", "¿qué sabes hacer?": "¿qué sabe usted hacer?",
           "responde, por favor": "responda, por favor", "ayúdame, por favor": "ayúdeme, por favor",
           "dime, por favor": "dígame, por favor", "no te preocupes": "no se preocupe",
           "te lo agradezco": "se lo agradezco"},
    "it": {"che stai facendo?": "che sta facendo?", "di che cosa ti occupi?": "di che cosa si occupa?", "che cosa puoi fare?": "che cosa può fare?", "di che cosa sei capace?": "di che cosa è capace?", "scusa": "scusi", "come ti chiami?": "come si chiama?", "qual è il tuo nome?": "qual è il suo nome?",
           "chi sei?": "chi è Lei?", "che cosa sei?": "che cosa è Lei?",
           "dimmi chi sei.": "mi dica chi è Lei.", "come stai?": "come sta?",
           "che cosa fai?": "che cosa fa?", "che cosa sai fare?": "che cosa sa fare?",
           "rispondi, per favore": "risponda, per favore",
           "aiutami, per favore": "mi aiuti, per favore", "dimmi, per favore": "mi dica, per favore",
           "non preoccuparti": "non si preoccupi", "ti ringrazio": "la ringrazio"},
    "pt": {"como vais?": "como vai?", "o que estás a fazer?": "o que está a fazer?", "em que andas?": "em que anda?", "o que consegues fazer?": "o que consegue fazer?", "de que és capaz?": "de que é capaz?", "desculpa": "desculpe", "como te chamas?": "como se chama?", "qual é o teu nome?": "qual é o seu nome?",
           "quem és tu?": "quem é o senhor?", "o que és tu?": "o que é o senhor?",
           "diz-me quem és.": "diga-me quem é.", "como estás?": "como está?",
           "o que fazes?": "o que faz?", "o que sabes fazer?": "o que sabe fazer?",
           "responde, por favor": "responda, por favor", "ajuda-me, por favor": "ajude-me, por favor",
           "diz-me, por favor": "diga-me, por favor", "não te preocupes": "não se preocupe"},
    "nl": {"hoe is het?": "hoe is het met u?", "waar ben je mee bezig?": "waar bent u mee bezig?", "wat ben je aan het doen?": "wat bent u aan het doen?", "waartoe ben je in staat?": "waartoe bent u in staat?", "waar ben je goed in?": "waar bent u goed in?", "dank je wel": "dank u wel", "hoe heet je?": "hoe heet u?", "wat is je naam?": "wat is uw naam?",
           "wie ben je?": "wie bent u?", "wat ben je?": "wat bent u?",
           "zeg me wie je bent.": "zegt u mij wie u bent.",
           "hoe gaat het?": "hoe gaat het met u?", "wat doe je?": "wat doet u?",
           "wat kun je?": "wat kunt u?", "antwoord alsjeblieft": "antwoordt u alstublieft",
           "help me alsjeblieft": "helpt u mij alstublieft",
           "zeg het me alsjeblieft": "zegt u het mij alstublieft",
           "maak je geen zorgen": "maakt u zich geen zorgen", "dank je": "dank u"},
    "pl": {"czym się zajmujesz?": "czym się pan zajmuje?", "co teraz robisz?": "co pan teraz robi?", "co umiesz?": "co pan umie?", "do czego jesteś zdolny?": "do czego pan jest zdolny?", "jak masz na imię?": "jak pan ma na imię?", "jak się nazywasz?": "jak się pan nazywa?",
           "kim jesteś?": "kim pan jest?", "czym jesteś?": "czym pan jest?",
           "powiedz mi, kim jesteś.": "proszę mi powiedzieć, kim pan jest.",
           "jak się masz?": "jak się pan ma?", "co robisz?": "co pan robi?",
           "co potrafisz?": "co pan potrafi?", "odpowiedz, proszę": "proszę odpowiedzieć",
           "pomóż mi, proszę": "proszę mi pomóc", "powiedz mi, proszę": "proszę mi powiedzieć",
           "nie martw się": "proszę się nie martwić", "wybacz": "proszę wybaczyć"},
}


def _переодеть(значение, таблица):
    """Тот же дом в другом обращении — замена ведётся по объявленным строкам.

    Обход общий, а не по полям: всякая строка дома проходит через словарь, и
    новое поле, дописанное завтра, оденется само. Строки, замены не имеющей,
    остаются как есть, — и форма, не изменившаяся ни в одной строке, показа не
    получает (см. `_все_показы`): двойник в корпусе хуже пустой клетки.
    """
    if isinstance(значение, str):
        return таблица.get(значение, значение)
    if isinstance(значение, tuple):
        return tuple(_переодеть(x, таблица) for x in значение)
    if isinstance(значение, dict):
        return {k: _переодеть(v, таблица) for k, v in значение.items()}
    return значение


ЯЗЫКИ_ВЫ = {яз: _переодеть(я, ВЕЖЛИВО[яз]) for яз, я in ЯЗЫКИ.items()}
for _яз, _т in ВЕЖЛИВО.items():
    assert _яз in ЯЗЫКИ, _яз
    _все = repr(ЯЗЫКИ[_яз])
    for _из in _т:
        assert repr(_из)[1:-1] in _все, (_яз, _из, "замена объявлена строке, которой в доме нет")
    assert (ЯЗЫКИ_ВЫ[_яз] != ЯЗЫКИ[_яз]) == bool(_т), (_яз, "словарь замен и дело разошлись")

ФОРМЫ = ("пара", "определение", "имя", "кто", "незнание", "малый")
ФОРМЫ_ВЫ = ("пара", "имя", "кто", "малый")
# английский различия не имеет — дыра объявлена домом, а не выведена прибором
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {ф + "_вы": frozenset(я for я, т in ВЕЖЛИВО.items() if not т)
                        for ф in ФОРМЫ_ВЫ}

# МАССА ПО ПРАВИЛУ: у всякого вида с парой ≥3 зачина и ≥3 ответа
for _яз, _я in ЯЗЫКИ.items():
    for _в in ВИДЫ:
        _зач = _я["зачины"][_в]
        _отв = _зач if _в in ЗЕРКАЛЬНЫЕ else _я["ответы"].get(_в, ())
        if _отв:
            assert len(_зач) >= 3 and len(_отв) >= 3, (_яз, _в, len(_зач), len(_отв))
    assert set(_я["виды"]) == set(ВИДЫ), (_яз, "вид объявлен не всякому роду")
    for _в, _о in _я["малый"]:
        assert len(_в) >= 3 and len(_о) >= 3, (_яз, _в[0], "малый разговор ниже LAW²")


# СТЯЖЕНИЕ ПЕРЕД ГЛАСНОЙ — правило языка, объявленное, а не угаданное:
# французское «que» перед гласной становится «qu'» («qu'est-ce qu'un
# quarkosaure ?», не «que un»). Язык, не объявивший гласных, стяжения не
# знает и получает своё слово целиком.
ГЛАСНЫЕ = {"fr": "aeiouâàéèêëîïôöûüh"}


def _стяжение(язык, слово):
    if язык not in ГЛАСНЫЕ:
        return ""
    return "qu'" if слово and слово[0].lower() in ГЛАСНЫЕ[язык] else "que "


def ответы(язык, вид, вы=False):
    я = (ЯЗЫКИ_ВЫ if вы else ЯЗЫКИ)[язык]
    return я["зачины"][вид] if вид in ЗЕРКАЛЬНЫЕ else я["ответы"].get(вид, ())


def страница(язык, форма, вид=None, i=0, j=0, вы=False):
    я = (ЯЗЫКИ_ВЫ if вы else ЯЗЫКИ)[язык]
    if форма == "пара":
        зач, отв = я["зачины"][вид], ответы(язык, вид, вы)
        return f"{зач[i % len(зач)]}. {отв[j % len(отв)]}."
    if форма == "определение":
        зач = я["зачины"][вид]
        с = зач[i % len(зач)]
        return я["определение"].format(с=с, в=я["виды"][вид], ЧТО=_стяжение(язык, с))
    if форма == "имя":
        имена, вопросы = я["имена"], я["имя_воп"]
        return f"{вопросы[j % len(вопросы)]} {я['имя_отв'].format(и=имена[i % len(имена)])}"
    if форма == "кто":
        вопросы = я["кто_воп"]
        return f"{вопросы[i % len(вопросы)]} {я['кто_отв']}"
    if форма == "малый":
        # МАЛЫЙ РАЗГОВОР БЕЗ ЧИСЛА (04.09, слово holon). Форма «сейчас я знаю
        # N форм» была бы ЛОЖЬЮ при первом же росте свода, и суд её не поймал
        # бы: арифметика в ней верна. Величина состояния приходит из органа во
        # время ответа, а корпус показывает рамку без величины — и потому она
        # остаётся истинной при всяком размере свода.
        # ВЕЕР: тема × поверхность вопроса × ответ. Перепись голов нашла 59
        # одиночных голов в этом доме — «что нового?» стояло ОДНОЙ строкой на
        # язык, и по LAW² = 9 такая голова не покупается вовсе. Три поверхности
        # на три ответа дают ровно девять: число выведено из закона покупки, а
        # не взято. Ответы — о границе знания, без величин (см. выше).
        темы = я["малый"]
        воп_список, отв_список = темы[i % len(темы)]
        return f"{воп_список[j % len(воп_список)]} {отв_список[(i // len(темы)) % len(отв_список)]}"
    небылицы = я["небылицы"]
    н = небылицы[i % len(небылицы)]
    return я["незнание"].format(н=н, ЧТО=_стяжение(язык, н))


# --- сторона суда: строка судится ПЕРЕПИСЫВАНИЕМ ---
def _показ_вы(вон, язык, форма, *, вид=None, i=0, j=0):
    """Вежливый показ пишется, лишь если он ОТЛИЧАЕТСЯ от неформального.

    Строка, совпавшая с неформальной, есть двойник, а не второй регистр: язык,
    у которого различия нет (английский) или у которого эта именно строка
    обращения не содержит, не получает ни одной лишней страницы.
    """
    вежливая = страница(язык, форма, вид, i, j, вы=True)
    if вежливая != страница(язык, форма, вид, i, j):
        вон[вежливая] = (язык, форма + "_вы")


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for вид in ВИДЫ:
            зач = я["зачины"][вид]
            отв = ответы(язык, вид)
            for i in range(len(зач)):
                вон[страница(язык, "определение", вид, i)] = (язык, "определение")
                # ВТОРАЯ РАМКА ВОПРОСА, ГДЕ ЯЗЫК ЕЁ ИМЕЕТ: польский спрашивает
                # «co to jest X?» и «czym jest X?» равно часто, и продукт,
                # знающий одну, молчит на второй
                if "определение2" in я:
                    вон[я["определение2"].format(с=зач[i], в=я["виды"][вид],
                                                 ЧТО=_стяжение(язык, зач[i]))] = (язык, "определение")
                for j in range(len(отв)):
                    вон[страница(язык, "пара", вид, i, j)] = (язык, "пара")
                    _показ_вы(вон, язык, "пара", вид=вид, i=i, j=j)
        for i in range(len(я["имена"])):
            for j in range(len(я["имя_воп"])):
                вон[страница(язык, "имя", i=i, j=j)] = (язык, "имя")
                _показ_вы(вон, язык, "имя", i=i, j=j)
        for i in range(len(я["кто_воп"])):
            вон[страница(язык, "кто", i=i)] = (язык, "кто")
            _показ_вы(вон, язык, "кто", i=i)
        for i in range(len(я["небылицы"])):
            вон[страница(язык, "незнание", i=i)] = (язык, "незнание")
        for i in range(len(я["малый"]) * 3):
            for j in range(3):
                вон[страница(язык, "малый", i=i, j=j)] = (язык, "малый")
                _показ_вы(вон, язык, "малый", i=i, j=j)
    return вон


ПОКАЗЫ = _все_показы()
# РАМКИ БЕЗ СЛОВ — для суда о ЧУЖОМ слове в объявленной рамке: строка, севшая
# в рамку дома, но с незнакомым словом, есть ЛОЖЬ, а не молчание.
#
# РАМКА ДОМА ШИРЕ ЕГО ПРЕДМЕТА, И ЭТО ЛОВУШКА (04.09). «что такое X?» есть
# рамка ВСЕГО КОРПУСА, а не дома обихода: ею спрашивают о дожде, о числе, о
# роде — обо всём. Дом, объявивший эту рамку своей, назвал ложью 128 честных
# определений соседнего мира тем в тот же час, как они появились. Потому суд
# рамки СМОТРИТ НА СЛОВО: он берётся судить лишь тогда, когда предмет вопроса
# есть слово ЭТОГО дома («привет», «спасибо»); о дожде дом молчит, ибо о дожде
# он ничего не объявлял. Тот же род, что М-172: молчание «не моё дело»
# законно ровно там, где предмет и вправду не объявлен домом.
# ДЫРА НЕ ПЕРЕХОДИТ ГРАНИЦЫ ПРЕДЛОЖЕНИЯ. Дыра «(.+?)» проглатывала точку, и
# суд читал удвоенный показ как один: «что такое привет? привет — это
# приветствие. что такое привет? …» ловилось им как ложь (прибор ЛОВУШКИ
# НАЧАЛА, 10 проб из 40). Слово, о котором спрашивают, и вид, которым отвечают,
# суть ОДНА клауза каждое — «[^.?!]+» говорит это прямо.
_РАМКИ = tuple((язык, re.compile("^" + re.escape(ш).replace(r"\{с\}", "([^.?!]+)")
                                 .replace(r"\{в\}", "([^.?!]+)").replace(r"\{н\}", "([^.?!]+)")
                                 .replace(r"\{и\}", "([^.?!]+)").replace(r"\{ЧТО\}", "(?:qu'|que )") + "$"))
               for дом in (ЯЗЫКИ, ЯЗЫКИ_ВЫ) for язык, я in дом.items()
               for ш in (я["определение"], я["незнание"]) + ((я["определение2"],) if "определение2" in я else ())
               + tuple(f"{в} {я['имя_отв']}" for в in я["имя_воп"]))
_СВОИ_СЛОВА = {язык: {с for дом in (ЯЗЫКИ, ЯЗЫКИ_ВЫ) for вид in ВИДЫ for с in дом[язык]["зачины"][вид]}
               | set(я["небылицы"]) | set(я["имена"])
               for язык, я in ЯЗЫКИ.items()}


def судить(строка):
    """(судимо, истинно): показ дома истинен; строка, севшая в объявленную
    рамку с чужим словом, — ложна; всё прочее дому не подсудно."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for язык, р in _РАМКИ:
        м = р.match(с)
        if м and any(г in _СВОИ_СЛОВА[язык] for г in м.groups()):
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
        битое = я["определение"].format(с=я["зачины"][ПРИВЕТ][0], в=я["виды"][ПРОЩАНИЕ],
                                        ЧТО=_стяжение(язык, я["зачины"][ПРИВЕТ][0]))
        судимо, истинно = судить(битое)
        assert судимо and not истинно, (язык, битое)
        мутанты += 1
        # МУТАНТ: ответ не своего вида («спасибо. до свидания.») дому не подсуден,
        # но и показом не зовётся — пара объявлена своими списками
        чужая = f"{я['зачины'][БЛАГОДАРНОСТЬ][0]}. {я['зачины'][ПРОЩАНИЕ][0]}."
        assert чужая not in ПОКАЗЫ, (язык, чужая)
        мутанты += 1
        # ВЕЖЛИВЫЙ ПОКАЗ ИСТИНЕН ТАМ, ГДЕ ОБЪЯВЛЕН, и не пишется, где замены нет
        for форма in ФОРМЫ_ВЫ:
            вид = ПРИВЕТ if форма == "пара" else None
            вежливая = страница(язык, форма, вид, вы=True)
            есть = вежливая != страница(язык, форма, вид)
            assert есть == (ПОКАЗЫ.get(вежливая) == (язык, форма + "_вы")) or not ВЕЖЛИВО[язык], \
                (язык, форма, вежливая)
        # МУТАНТ: незнание о ЗНАКОМОМ слове — ложь («что такое привет? я не знаю…»)
        битое2 = я["незнание"].format(н=я["зачины"][ПРИВЕТ][0],
                                      ЧТО=_стяжение(язык, я["зачины"][ПРИВЕТ][0]))
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
