#!/usr/bin/env python3
"""ДОМ ПОВЕДЕНЧЕСКИХ ЗАКОНОВ — причина поступка и вопрос о ней.

Заказ владельца (04.09, через holon): «понимать базовые поведенческие и
психологические законы». Не «психология вообще» и не цитаты с полки, а
ПОКАЗЫ своего дома: состояние человека, его следствие, и ВОПРОС о причине,
на который есть ответ.

Шесть родов, названных заказом, и все шесть суть регулярности, а не
приговоры, — потому следствие всюду сравнительное («ошибается ЧАЩЕ», «makes
MORE mistakes»): «усталый ошибается» ложно как закон о человеке, «усталый
ошибается чаще» верно как закон о частоте, и корпус не вправе учить первому.

  усталость → ошибки          потребность → действие
  эмоция → её повод           намерение → поступок
  привычка → повтор           внимание → упущение

ВЫВОД НАД ЗАКОНОМ (04.09) — форма, ради которой дом стоило перечитать. Он держал
ЗАКОН и СЛУЧАЙ порознь, и связи между ними не показывал ни один показ:

    когда человек устал, он ошибается чаще. пётр устал. значит пётр ошибается чаще.

Третья фраза здесь не факт о Петре, а СЛЕДСТВИЕ закона и посылки — modus ponens
над уже объявленным. Стоило это ОДНОЙ СВЯЗКИ на язык: обе части были объявлены
давно, недоставало лишь слова «значит». Так и узнаётся, что род уже готов и ждёт
только имени.

Формы у каждого рода, и третья из первых — главная:
  · ПРАВИЛО   «пётр устал. поэтому пётр ошибается чаще.»
  · ВОПРОС    «… почему пётр ошибается чаще? потому что пётр устал.»
  · ЗАКОН     «когда человек устал, он ошибается чаще.» — обобщение над
    случаями, тот самый акт, который манифест зовёт generalize.

ДОЛГ ЖЕНСКОГО РОДА УПЛАЧЕН (04.09, тем же днём). Дом брал имена одного рода и
говорил об этом прямо: клауза причины несёт ПРИЛАГАТЕЛЬНОЕ («устал», «stanco»,
«cansado», «zmęczony»), оно согласуется с родом подлежащего в шести языках из
девяти, и «Anna è stanco» верно счётом ролей и ложно речью. Уплачено так же,
как было объявлено: ВТОРАЯ ФОРМА КЛАУЗЫ написана там, где язык её меняет, и
НЕ написана там, где не меняет, — и второе объявлено списком
(ЖЕНСКОЕ_НЕ_МЕНЯЕТСЯ), а не умолчанием.

Меняется не только прилагательное: русское и польское ПРОШЕДШЕЕ время
согласуется тоже («смотрел» → «смотрела», «nie zobaczył» → «nie zobaczyła»), и
потому у пятого рода женская форма несёт и причину, и следствие. Угадать это
по одному прилагательному было нельзя — оттого долг и стоял названным, пока не
были прочитаны все шесть клауз всех шести языков.

ПОДЛЕЖАЩЕЕ — ИМЯ, А НЕ МЕСТОИМЕНИЕ: правило d5 от 04.09 («страница,
открытая местоимением, обязана иметь явный референт») соблюдается тем, что
референта здесь нет вовсе — всякая клауза называет человека по имени.

ЧЕТЫРЕ СТРОКИ НА ПАРУ, А НЕ ДВЕ: немецкий и голландский ставят в
придаточном глагол в конец («weil Anna müde ist»), а после «deshalb» —
инверсию («deshalb macht Anna mehr Fehler»), и потому причина объявлена
дважды: как главная клауза и как придаточная. Язык, где формы совпадают,
объявляет их одинаковыми — явно, а не умолчанием.

    python3 tools/behaviorforms.py    # самопроверка с мутантами
"""
УСТАЛОСТЬ, ПОТРЕБНОСТЬ, ЭМОЦИЯ, НАМЕРЕНИЕ, ПРИВЫЧКА, ВНИМАНИЕ = range(6)
РОДЫ = (УСТАЛОСТЬ, ПОТРЕБНОСТЬ, ЭМОЦИЯ, НАМЕРЕНИЕ, ПРИВЫЧКА, ВНИМАНИЕ)

# пара = (причина главной клаузой, следствие, причина придаточной клаузой,
#         обобщение: «когда <причина>, <следствие>»)
ЯЗЫКИ = {
    "ru": dict(
        имена=("пётр", "иван", "олег", "борис"),
        пары=(
            ("{X} устал", "{X} ошибается чаще", "{X} устал", "человек устал", "он ошибается чаще"),
            ("{X} голоден", "{X} ищет еду", "{X} голоден", "человек голоден", "он ищет еду"),
            ("{X} не знает, что будет", "{X} боится", "{X} не знает, что будет", "человек не знает, что будет", "он боится"),
            ("{X} хочет успеть", "{X} спешит", "{X} хочет успеть", "человек хочет успеть", "он спешит"),
            ("{X} делает это каждый день", "{X} делает это не думая", "{X} делает это каждый день", "человек делает что-то каждый день", "он делает это не думая"),
            ("{X} смотрел в другую сторону", "{X} не увидел знака", "{X} смотрел в другую сторону", "человек смотрит в другую сторону", "он не видит знака"),
        ),
        правило="{п}. поэтому {с}.", вопрос="{п}. поэтому {с}. почему {с}? потому что {пп}.",
        кратко="почему, когда {оп}, {ов}? {осн}.",
        дела_многих=("люди спят", "люди едят", "люди учатся"),
        цели=(("человек спит", "чтобы отдохнуть"), ("человек ест", "чтобы не быть голодным"), ("человек учится", "чтобы уметь больше")), зачем_рамка="зачем {д}? {ц}.",
        вывод="{з} {п}. значит {с}.",
        закон="когда {оп}, {ос}.",
        закон_вопрос="когда {оп}, {ос}. почему {ов}? потому что {оп}.",
        вопросы_многих=(
            'почему люди ошибаются чаще, когда устали?',
            'почему люди ищут еду, когда голодны?',
            'почему люди боятся неизвестного?',
            'почему люди спешат, когда хотят успеть?',
            'почему люди делают не думая то, что делают каждый день?',
            'почему люди не видят знака, когда смотрят в другую сторону?',
        ),
        основания=(
            ('почему человек ошибается чаще, когда устал?', 'потому что усталость ослабляет внимание'),
            ('почему человек ищет еду, когда голоден?', 'потому что тело требует того, чего ему не хватает'),
            ('почему человек боится, когда не знает, что будет?', 'потому что неизвестное нельзя предусмотреть'),
            ('почему человек спешит, когда хочет успеть?', 'потому что времени остаётся меньше, чем нужно'),
            ('почему человек делает не думая то, что делает каждый день?', 'потому что повторение делает действие привычным'),
            ('почему человек не видит знака, когда смотрит в другую сторону?', 'потому что человек видит только то, на что смотрит'),
        ),
    ),
    "en": dict(
        имена=("peter", "ivan", "john", "mark"),
        пары=(
            ("{X} is tired", "{X} makes more mistakes", "{X} is tired", "a person is tired", "that person makes more mistakes"),
            ("{X} is hungry", "{X} looks for food", "{X} is hungry", "a person is hungry", "that person looks for food"),
            ("{X} does not know what will happen", "{X} is afraid", "{X} does not know what will happen", "a person does not know what will happen", "that person is afraid"),
            ("{X} wants to be in time", "{X} hurries", "{X} wants to be in time", "a person wants to be in time", "that person hurries"),
            ("{X} does it every day", "{X} does it without thinking", "{X} does it every day", "a person does something every day", "that person does it without thinking"),
            ("{X} looked the other way", "{X} did not see the sign", "{X} looked the other way", "a person looks the other way", "that person does not see the sign"),
        ),
        # АНГЛИЙСКИЙ ВОПРОС ТРЕБУЕТ ВСПОМОГАТЕЛЬНОГО ГЛАГОЛА, и потому следствие
        # объявлено дважды: «peter makes more mistakes» → «does peter make more
        # mistakes». Язык, где утверждение и вопрос совпадают, второго объявления
        # не имеет — это сказано отсутствием ключа, а не умолчанием кода.
        вопр_след=("does {X} make more mistakes", "does {X} look for food", "is {X} afraid",
                   "does {X} hurry", "does {X} do it without thinking", "did {X} not see the sign"),
        правило="{п}. therefore {с}.", вопрос="{п}. therefore {с}. why {в}? because {пп}.",
        кратко="why, when {оп}, {ов}? {осн}.",
        дела_многих=("do people sleep", "do people eat", "do people study"),
        цели=(("does a person sleep", "in order to rest"), ("does a person eat", "in order not to be hungry"), ("does a person study", "in order to be able to do more")), зачем_рамка="why {д}? {ц}.",
        вывод="{з} {п}. so {с}.",
        закон="when {оп}, {ос}.",
        закон_вопрос="when {оп}, {ос}. why {ов}? because {оп}.",
        вопросы_многих=(
            'why do people make more mistakes when they are tired?',
            'why do people look for food when they are hungry?',
            'why do people fear the unknown?',
            'why do people hurry when they want to be in time?',
            'why do people do without thinking what they do every day?',
            'why do people not see the sign when they look the other way?',
        ),
        основания=(
            ('why does a person make more mistakes when tired?', 'because tiredness weakens attention'),
            ('why does a person look for food when hungry?', 'because the body asks for what it lacks'),
            ('why is a person afraid when they do not know what will happen?', 'because the unknown cannot be foreseen'),
            ('why does a person hurry when they want to be in time?', 'because less time is left than is needed'),
            ('why does a person do without thinking what they do every day?', 'because repetition makes an action a habit'),
            ('why does a person not see the sign when looking the other way?', 'because a person sees only what they look at'),
        ),
        # английский вопрос и здесь требует вспомогательного глагола
        общ_вопрос=("does that person make more mistakes", "does that person look for food",
                    "is that person afraid", "does that person hurry",
                    "does that person do it without thinking", "does that person not see the sign"),
    ),
    "de": dict(
        имена=("Paul", "Jonas", "Max", "Felix"),
        пары=(
            ("{X} ist müde", "macht {X} mehr Fehler", "{X} müde ist", "ein Mensch müde ist", "macht er mehr Fehler"),
            ("{X} ist hungrig", "sucht {X} Essen", "{X} hungrig ist", "ein Mensch hungrig ist", "sucht er Essen"),
            ("{X} weiß nicht, was kommt", "hat {X} Angst", "{X} nicht weiß, was kommt", "ein Mensch nicht weiß, was kommt", "hat er Angst"),
            ("{X} will rechtzeitig kommen", "beeilt {X} sich", "{X} rechtzeitig kommen will", "ein Mensch rechtzeitig kommen will", "beeilt er sich"),
            ("{X} macht es jeden Tag", "macht {X} es ohne nachzudenken", "{X} es jeden Tag macht", "ein Mensch etwas jeden Tag macht", "macht er es ohne nachzudenken"),
            ("{X} hat weggeschaut", "hat {X} das Zeichen nicht gesehen", "{X} weggeschaut hat", "ein Mensch wegschaut", "sieht er das Zeichen nicht"),
        ),
        правило="{п}. deshalb {с}.", вопрос="{п}. deshalb {с}. warum {с}? weil {пп}.",
        дела_многих=("schlafen Menschen", "essen Menschen", "lernen Menschen"),
        цели=(("schläft ein Mensch", "um sich auszuruhen"), ("isst ein Mensch", "um nicht hungrig zu sein"), ("lernt ein Mensch", "um mehr zu können")), зачем_рамка="wozu {д}? {ц}.",
        вывод="{з} {п}. also {с}.",
        закон="wenn {оп}, {ос}.",
        закон_вопрос="wenn {оп}, {ос}. warum {ов}? weil {оп}.",
        вопросы_многих=(
            'warum machen Menschen mehr Fehler, wenn sie müde sind?',
            'warum suchen Menschen Essen, wenn sie hungrig sind?',
            'warum fürchten Menschen das Unbekannte?',
            'warum beeilen sich Menschen, wenn sie rechtzeitig kommen wollen?',
            'warum machen Menschen ohne nachzudenken, was sie jeden Tag machen?',
            'warum sehen Menschen das Zeichen nicht, wenn sie wegschauen?',
        ),
        основания=(
            ('warum macht ein Mensch mehr Fehler, wenn er müde ist?', 'weil Müdigkeit die Aufmerksamkeit schwächt'),
            ('warum sucht ein Mensch Essen, wenn er hungrig ist?', 'weil der Körper verlangt, was ihm fehlt'),
            ('warum hat ein Mensch Angst, wenn er nicht weiß, was kommt?', 'weil man das Unbekannte nicht vorhersehen kann'),
            ('warum beeilt sich ein Mensch, wenn er rechtzeitig kommen will?', 'weil weniger Zeit bleibt als nötig ist'),
            ('warum macht ein Mensch ohne nachzudenken, was er jeden Tag macht?', 'weil Wiederholung eine Handlung zur Gewohnheit macht'),
            ('warum sieht ein Mensch das Zeichen nicht, wenn er wegschaut?', 'weil ein Mensch nur sieht, wohin er schaut'),
        ),
    ),
    "fr": dict(
        имена=("Paul", "Louis", "Jules", "Hugo"),
        пары=(
            ("{X} est fatigué", "{X} fait plus d'erreurs", "{X} est fatigué", "une personne est fatiguée", "elle fait plus d'erreurs"),
            ("{X} a faim", "{X} cherche à manger", "{X} a faim", "une personne a faim", "elle cherche à manger"),
            ("{X} ne sait pas ce qui va arriver", "{X} a peur", "{X} ne sait pas ce qui va arriver", "une personne ne sait pas ce qui va arriver", "elle a peur"),
            ("{X} veut arriver à temps", "{X} se dépêche", "{X} veut arriver à temps", "une personne veut arriver à temps", "elle se dépêche"),
            ("{X} le fait chaque jour", "{X} le fait sans réfléchir", "{X} le fait chaque jour", "une personne fait quelque chose chaque jour", "elle le fait sans réfléchir"),
            ("{X} regardait ailleurs", "{X} n'a pas vu le signe", "{X} regardait ailleurs", "une personne regarde ailleurs", "elle ne voit pas le signe"),
        ),
        правило="{п}. donc {с}.", вопрос="{п}. donc {с}. pourquoi {с} ? parce que {пп}.",
        кратко="pourquoi, quand {оп}, {ов} ? {осн}.",
        дела_многих=("les gens dorment", "les gens mangent", "les gens apprennent"),
        цели=(("une personne dort", "pour se reposer"), ("une personne mange", "pour ne pas avoir faim"), ("une personne apprend", "pour savoir faire plus")), зачем_рамка="pourquoi {д} ? {ц}.",
        вывод="{з} {п}. donc {с}.",
        закон="quand {оп}, {ос}.",
        закон_вопрос="quand {оп}, {ос}. pourquoi {ов} ? parce que {оп}.",
        вопросы_многих=(
            "pourquoi les gens font-ils plus d'erreurs quand ils sont fatigués ?",
            'pourquoi les gens cherchent-ils à manger quand ils ont faim ?',
            "pourquoi les gens craignent-ils l'inconnu ?",
            'pourquoi les gens se dépêchent-ils quand ils veulent arriver à temps ?',
            "pourquoi les gens font-ils sans réfléchir ce qu'ils font chaque jour ?",
            'pourquoi les gens ne voient-ils pas le signe quand ils regardent ailleurs ?',
        ),
        основания=(
            ("pourquoi une personne fait-elle plus d'erreurs quand elle est fatiguée ?", "parce que la fatigue affaiblit l'attention"),
            ('pourquoi une personne cherche-t-elle à manger quand elle a faim ?', 'parce que le corps demande ce qui lui manque'),
            ('pourquoi une personne a-t-elle peur quand elle ne sait pas ce qui va arriver ?', "parce qu'on ne peut pas prévoir l'inconnu"),
            ('pourquoi une personne se dépêche-t-elle quand elle veut arriver à temps ?', "parce qu'il reste moins de temps qu'il n'en faut"),
            ("pourquoi une personne fait-elle sans réfléchir ce qu'elle fait chaque jour ?", 'parce que la répétition rend un geste habituel'),
            ('pourquoi une personne ne voit-elle pas le signe quand elle regarde ailleurs ?', "parce qu'une personne ne voit que ce qu'elle regarde"),
        ),
    ),
    "es": dict(
        имена=("Pablo", "Luis", "Diego", "Carlos"),
        пары=(
            ("{X} está cansado", "{X} comete más errores", "{X} está cansado", "una persona está cansada", "comete más errores"),
            ("{X} tiene hambre", "{X} busca comida", "{X} tiene hambre", "una persona tiene hambre", "busca comida"),
            ("{X} no sabe qué va a pasar", "{X} tiene miedo", "{X} no sabe qué va a pasar", "una persona no sabe qué va a pasar", "tiene miedo"),
            ("{X} quiere llegar a tiempo", "{X} se apresura", "{X} quiere llegar a tiempo", "una persona quiere llegar a tiempo", "se apresura"),
            ("{X} lo hace cada día", "{X} lo hace sin pensar", "{X} lo hace cada día", "una persona hace algo cada día", "lo hace sin pensar"),
            ("{X} miraba hacia otro lado", "{X} no vio la señal", "{X} miraba hacia otro lado", "una persona mira hacia otro lado", "no ve la señal"),
        ),
        правило="{п}. por eso {с}.", вопрос="{п}. por eso {с}. ¿por qué {с}? porque {пп}.",
        кратко="¿por qué, cuando {оп}, {ов}? {осн}.",
        дела_многих=("la gente duerme", "la gente come", "la gente estudia"),
        цели=(("una persona duerme", "para descansar"), ("una persona come", "para no tener hambre"), ("una persona estudia", "para saber hacer más")), зачем_рамка="¿por qué {д}? {ц}.",
        вывод="{з} {п}. así que {с}.",
        закон="cuando {оп}, {ос}.",
        закон_вопрос="cuando {оп}, {ос}. ¿por qué {ов}? porque {оп}.",
        вопросы_многих=(
            '¿por qué la gente comete más errores cuando está cansada?',
            '¿por qué la gente busca comida cuando tiene hambre?',
            '¿por qué la gente teme lo desconocido?',
            '¿por qué la gente se apresura cuando quiere llegar a tiempo?',
            '¿por qué la gente hace sin pensar lo que hace cada día?',
            '¿por qué la gente no ve la señal cuando mira hacia otro lado?',
        ),
        основания=(
            ('¿por qué una persona comete más errores cuando está cansada?', 'porque el cansancio debilita la atención'),
            ('¿por qué una persona busca comida cuando tiene hambre?', 'porque el cuerpo pide lo que le falta'),
            ('¿por qué una persona tiene miedo cuando no sabe qué va a pasar?', 'porque lo desconocido no se puede prever'),
            ('¿por qué una persona se apresura cuando quiere llegar a tiempo?', 'porque queda menos tiempo del que hace falta'),
            ('¿por qué una persona hace sin pensar lo que hace cada día?', 'porque la repetición convierte una acción en costumbre'),
            ('¿por qué una persona no ve la señal cuando mira hacia otro lado?', 'porque una persona sólo ve aquello que mira'),
        ),
    ),
    "it": dict(
        имена=("Marco", "Luca", "Paolo", "Matteo"),
        пары=(
            ("{X} è stanco", "{X} fa più errori", "{X} è stanco", "una persona è stanca", "fa più errori"),
            ("{X} ha fame", "{X} cerca del cibo", "{X} ha fame", "una persona ha fame", "cerca del cibo"),
            ("{X} non sa che cosa succederà", "{X} ha paura", "{X} non sa che cosa succederà", "una persona non sa che cosa succederà", "ha paura"),
            ("{X} vuole arrivare in tempo", "{X} si affretta", "{X} vuole arrivare in tempo", "una persona vuole arrivare in tempo", "si affretta"),
            ("{X} lo fa ogni giorno", "{X} lo fa senza pensare", "{X} lo fa ogni giorno", "una persona fa qualcosa ogni giorno", "lo fa senza pensare"),
            ("{X} guardava dall'altra parte", "{X} non ha visto il segnale", "{X} guardava dall'altra parte", "una persona guarda dall'altra parte", "non vede il segnale"),
        ),
        правило="{п}. perciò {с}.", вопрос="{п}. perciò {с}. perché {с}? perché {пп}.",
        кратко="perché, quando {оп}, {ов}? {осн}.",
        дела_многих=("le persone dormono", "le persone mangiano", "le persone studiano"),
        цели=(("una persona dorme", "per riposare"), ("una persona mangia", "per non avere fame"), ("una persona studia", "per saper fare di più")), зачем_рамка="perché {д}? {ц}.",
        вывод="{з} {п}. quindi {с}.",
        закон="quando {оп}, {ос}.",
        закон_вопрос="quando {оп}, {ос}. perché {ов}? perché {оп}.",
        вопросы_многих=(
            'perché le persone fanno più errori quando sono stanche?',
            'perché le persone cercano del cibo quando hanno fame?',
            "perché le persone temono l'ignoto?",
            'perché le persone si affrettano quando vogliono arrivare in tempo?',
            'perché le persone fanno senza pensare ciò che fanno ogni giorno?',
            "perché le persone non vedono il segnale quando guardano dall'altra parte?",
        ),
        основания=(
            ('perché una persona fa più errori quando è stanca?', "perché la stanchezza indebolisce l'attenzione"),
            ('perché una persona cerca del cibo quando ha fame?', 'perché il corpo chiede ciò che gli manca'),
            ('perché una persona ha paura quando non sa che cosa succederà?', "perché l'ignoto non si può prevedere"),
            ('perché una persona si affretta quando vuole arrivare in tempo?', 'perché resta meno tempo di quanto serve'),
            ('perché una persona fa senza pensare ciò che fa ogni giorno?', 'perché la ripetizione rende un gesto abituale'),
            ("perché una persona non vede il segnale quando guarda dall'altra parte?", 'perché una persona vede solo ciò che guarda'),
        ),
    ),
    "pt": dict(
        имена=("Pedro", "Tiago", "Rui", "João"),
        пары=(
            ("{X} está cansado", "{X} comete mais erros", "{X} está cansado", "uma pessoa está cansada", "comete mais erros"),
            ("{X} tem fome", "{X} procura comida", "{X} tem fome", "uma pessoa tem fome", "procura comida"),
            ("{X} não sabe o que vai acontecer", "{X} tem medo", "{X} não sabe o que vai acontecer", "uma pessoa não sabe o que vai acontecer", "tem medo"),
            ("{X} quer chegar a tempo", "{X} apressa-se", "{X} quer chegar a tempo", "uma pessoa quer chegar a tempo", "apressa-se"),
            ("{X} fá-lo todos os dias", "{X} fá-lo sem pensar", "{X} fá-lo todos os dias", "uma pessoa faz algo todos os dias", "fá-lo sem pensar"),
            ("{X} olhava para o outro lado", "{X} não viu o sinal", "{X} olhava para o outro lado", "uma pessoa olha para o outro lado", "não vê o sinal"),
        ),
        # португальский вопрос ставит «é que» между вопросным словом и клаузой
        правило="{п}. por isso {с}.", вопрос="{п}. por isso {с}. porque é que {в}? porque {пп}.",
        кратко="porque é que, quando {оп}, {ов}? {осн}.",
        дела_многих=("as pessoas dormem", "as pessoas comem", "as pessoas estudam"),
        цели=(("uma pessoa dorme", "para descansar"), ("uma pessoa come", "para não ter fome"), ("uma pessoa estuda", "para saber fazer mais")), зачем_рамка="porque é que {д}? {ц}.",
        вывод="{з} {п}. portanto {с}.",
        закон="quando {оп}, {ос}.",
        закон_вопрос="quando {оп}, {ос}. porque é que {ов}? porque {оп}.",
        вопросы_многих=(
            'porque é que as pessoas cometem mais erros quando estão cansadas?',
            'porque é que as pessoas procuram comida quando têm fome?',
            'porque é que as pessoas temem o desconhecido?',
            'porque é que as pessoas se apressam quando querem chegar a tempo?',
            'porque é que as pessoas fazem sem pensar o que fazem todos os dias?',
            'porque é que as pessoas não veem o sinal quando olham para o outro lado?',
        ),
        основания=(
            ('porque é que uma pessoa comete mais erros quando está cansada?', 'porque o cansaço enfraquece a atenção'),
            ('porque é que uma pessoa procura comida quando tem fome?', 'porque o corpo pede o que lhe falta'),
            ('porque é que uma pessoa tem medo quando não sabe o que vai acontecer?', 'porque o desconhecido não se pode prever'),
            ('porque é que uma pessoa se apressa quando quer chegar a tempo?', 'porque resta menos tempo do que é preciso'),
            ('porque é que uma pessoa faz sem pensar o que faz todos os dias?', 'porque a repetição torna um gesto habitual'),
            ('porque é que uma pessoa não vê o sinal quando olha para o outro lado?', 'porque uma pessoa só vê aquilo para onde olha'),
        ),
    ),
    "nl": dict(
        имена=("Piet", "Jan", "Max", "Tim"),
        пары=(
            ("{X} is moe", "maakt {X} meer fouten", "{X} moe is", "een mens moe is", "maakt hij meer fouten"),
            ("{X} heeft honger", "zoekt {X} eten", "{X} honger heeft", "een mens honger heeft", "zoekt hij eten"),
            ("{X} weet niet wat er komt", "is {X} bang", "{X} niet weet wat er komt", "een mens niet weet wat er komt", "is hij bang"),
            ("{X} wil op tijd komen", "haast {X} zich", "{X} op tijd wil komen", "een mens op tijd wil komen", "haast hij zich"),
            ("{X} doet het elke dag", "doet {X} het zonder na te denken", "{X} het elke dag doet", "een mens iets elke dag doet", "doet hij het zonder na te denken"),
            ("{X} keek de andere kant op", "heeft {X} het teken niet gezien", "{X} de andere kant op keek", "een mens de andere kant op kijkt", "ziet hij het teken niet"),
        ),
        правило="{п}. daarom {с}.", вопрос="{п}. daarom {с}. waarom {с}? omdat {пп}.",
        дела_многих=("slapen mensen", "eten mensen", "leren mensen"),
        цели=(("slaapt een mens", "om uit te rusten"), ("eet een mens", "om geen honger te hebben"), ("leert een mens", "om meer te kunnen")), зачем_рамка="waarom {д}? {ц}.",
        вывод="{з} {п}. dus {с}.",
        закон="als {оп}, {ос}.",
        закон_вопрос="als {оп}, {ос}. waarom {ов}? omdat {оп}.",
        вопросы_многих=(
            'waarom maken mensen meer fouten als ze moe zijn?',
            'waarom zoeken mensen eten als ze honger hebben?',
            'waarom vrezen mensen het onbekende?',
            'waarom haasten mensen zich als ze op tijd willen komen?',
            'waarom doen mensen zonder na te denken wat ze elke dag doen?',
            'waarom zien mensen het teken niet als ze de andere kant op kijken?',
        ),
        основания=(
            ('waarom maakt een mens meer fouten als hij moe is?', 'omdat vermoeidheid de aandacht verzwakt'),
            ('waarom zoekt een mens eten als hij honger heeft?', 'omdat het lichaam vraagt wat het mist'),
            ('waarom is een mens bang als hij niet weet wat er komt?', 'omdat het onbekende niet te voorzien is'),
            ('waarom haast een mens zich als hij op tijd wil komen?', 'omdat er minder tijd over is dan nodig is'),
            ('waarom doet een mens zonder na te denken wat hij elke dag doet?', 'omdat herhaling een handeling tot gewoonte maakt'),
            ('waarom ziet een mens het teken niet als hij de andere kant op kijkt?', 'omdat een mens alleen ziet waar hij naar kijkt'),
        ),
    ),
    "pl": dict(
        имена=("Piotr", "Jan", "Marek", "Adam"),
        пары=(
            ("{X} jest zmęczony", "{X} popełnia więcej błędów", "{X} jest zmęczony", "człowiek jest zmęczony", "popełnia więcej błędów"),
            ("{X} jest głodny", "{X} szuka jedzenia", "{X} jest głodny", "człowiek jest głodny", "szuka jedzenia"),
            ("{X} nie wie, co będzie", "{X} się boi", "{X} nie wie, co będzie", "człowiek nie wie, co będzie", "boi się"),
            ("{X} chce zdążyć", "{X} się spieszy", "{X} chce zdążyć", "człowiek chce zdążyć", "spieszy się"),
            ("{X} robi to codziennie", "{X} robi to bez namysłu", "{X} robi to codziennie", "człowiek robi coś codziennie", "robi to bez namysłu"),
            ("{X} patrzył w inną stronę", "{X} nie zobaczył znaku", "{X} patrzył w inną stronę", "człowiek patrzy w inną stronę", "nie widzi znaku"),
        ),
        правило="{п}. dlatego {с}.", вопрос="{п}. dlatego {с}. dlaczego {с}? ponieważ {пп}.",
        кратко="dlaczego, kiedy {оп}, {ов}? {осн}.",
        дела_многих=("ludzie śpią", "ludzie jedzą", "ludzie się uczą"),
        цели=(("człowiek śpi", "żeby odpocząć"), ("człowiek je", "żeby nie być głodnym"), ("człowiek się uczy", "żeby umieć więcej")), зачем_рамка="dlaczego {д}? {ц}.",
        вывод="{з} {п}. więc {с}.",
        закон="kiedy {оп}, {ос}.",
        закон_вопрос="kiedy {оп}, {ос}. dlaczego {ов}? ponieważ {оп}.",
        вопросы_многих=(
            'dlaczego ludzie popełniają więcej błędów, kiedy są zmęczeni?',
            'dlaczego ludzie szukają jedzenia, kiedy są głodni?',
            'dlaczego ludzie boją się nieznanego?',
            'dlaczego ludzie się spieszą, kiedy chcą zdążyć?',
            'dlaczego ludzie robią bez namysłu to, co robią codziennie?',
            'dlaczego ludzie nie widzą znaku, kiedy patrzą w inną stronę?',
        ),
        основания=(
            ('dlaczego człowiek popełnia więcej błędów, kiedy jest zmęczony?', 'bo zmęczenie osłabia uwagę'),
            ('dlaczego człowiek szuka jedzenia, kiedy jest głodny?', 'bo ciało domaga się tego, czego mu brakuje'),
            ('dlaczego człowiek boi się, kiedy nie wie, co będzie?', 'bo nieznanego nie można przewidzieć'),
            ('dlaczego człowiek się spieszy, kiedy chce zdążyć?', 'bo zostaje mniej czasu, niż potrzeba'),
            ('dlaczego człowiek robi bez namysłu to, co robi codziennie?', 'bo powtarzanie czyni czynność nawykiem'),
            ('dlaczego człowiek nie widzi znaku, kiedy patrzy w inną stronę?', 'bo człowiek widzi tylko to, na co patrzy'),
        ),
    ),
}
ФОРМЫ = ("правило", "вопрос", "закон", "закон_вопрос", "кратко", "основание", "основание_многих", "зачем", "зачем_многих", "вывод")

for _яз, _я in ЯЗЫКИ.items():
    assert len(_я["пары"]) == len(РОДЫ), (_яз, len(_я["пары"]))
    assert len(_я["имена"]) >= 4, _яз
    for _п in _я["пары"]:
        assert len(_п) == 5, (_яз, _п)
    assert "вопр_след" not in _я or len(_я["вопр_след"]) == len(РОДЫ), _яз
    assert "общ_вопрос" not in _я or len(_я["общ_вопрос"]) == len(РОДЫ), _яз
    assert len(_я["основания"]) == len(РОДЫ), _яз
    assert len(_я["вопросы_многих"]) == len(РОДЫ), _яз
    assert len(_я["дела_многих"]) == len(_я["цели"]), _яз
    for _в in _я["вопросы_многих"]:
        assert _в.rstrip().endswith("?"), (_яз, _в)
    for _в, _о in _я["основания"]:
        assert _в.rstrip().endswith(("?", "؟")) and _о and not _о.endswith("."), (_яз, _в)



# ЖЕНСКИЙ РОД — УПЛАТА НАЗВАННОГО ДОЛГА (04.09). Дом брал имена ОДНОГО рода и
# говорил об этом прямо: клауза причины несёт прилагательное, оно согласуется с
# родом подлежащего в шести языках из девяти, и «Anna è stanco» верно счётом
# ролей и ложно речью. Долг уплачен так же, как объявлен: ВТОРАЯ ФОРМА КЛАУЗЫ
# написана там, где язык её меняет, и НЕ написана там, где не меняет, —
# и второе объявлено списком, а не умолчанием.
#
# Меняется не только прилагательное: русское и польское ПРОШЕДШЕЕ время
# согласуется тоже («смотрел» → «смотрела», «nie zobaczył» → «nie zobaczyła»),
# и потому у пятого рода женская форма несёт и причину, и следствие.
ЖЕНСКОЕ_НЕ_МЕНЯЕТСЯ = frozenset({"en", "de", "nl"})
ИМЕНА_Ж = {
    "ru": ["анна", "мария", "ольга", "вера"],
    "en": ["anna", "mary", "kate", "jane"],
    "de": ["Anna", "Maria", "Eva", "Lena"],
    "fr": ["Anne", "Marie", "Julie", "Claire"],
    "es": ["Ana", "María", "Lucía", "Elena"],
    "it": ["Anna", "Maria", "Giulia", "Chiara"],
    "pt": ["Ana", "Maria", "Rita", "Sofia"],
    "nl": ["Anna", "Maria", "Eva", "Lotte"],
    "pl": ["Anna", "Maria", "Ewa", "Zofia"],
}
ЖЕНСКОЕ = {
    "ru": {
        0: ["{X} устала", "{X} ошибается чаще", "{X} устала"],
        1: ["{X} голодна", "{X} ищет еду", "{X} голодна"],
        5: ["{X} смотрела в другую сторону", "{X} не увидела знака", "{X} смотрела в другую сторону"],
    },
    "pl": {
        0: ["{X} jest zmęczona", "{X} popełnia więcej błędów", "{X} jest zmęczona"],
        1: ["{X} jest głodna", "{X} szuka jedzenia", "{X} jest głodna"],
        5: ["{X} patrzyła w inną stronę", "{X} nie zobaczyła znaku", "{X} patrzyła w inną stronę"],
    },
    "it": {
        0: ["{X} è stanca", "{X} fa più errori", "{X} è stanca"],
    },
    "es": {
        0: ["{X} está cansada", "{X} comete más errores", "{X} está cansada"],
    },
    "pt": {
        0: ["{X} está cansada", "{X} comete mais erros", "{X} está cansada"],
    },
    "fr": {
        0: ["{X} est fatiguée", "{X} fait plus d'erreurs", "{X} est fatiguée"],
    },
}

for _яз in ЯЗЫКИ:
    assert len(ИМЕНА_Ж[_яз]) == len(ЯЗЫКИ[_яз]["имена"]), _яз
    assert (_яз in ЖЕНСКОЕ_НЕ_МЕНЯЕТСЯ) != (_яз in ЖЕНСКОЕ), _яз
    for _род, _тройка in ЖЕНСКОЕ.get(_яз, {}).items():
        assert 0 <= _род < len(РОДЫ) and len(_тройка) == 3, (_яз, _род)
        assert _тройка != ЯЗЫКИ[_яз]["пары"][_род][:3], (_яз, _род)


def пара_ж(язык, род):
    """Пара рода в ЖЕНСКОМ: где язык меняет форму — своя, где нет — та же."""
    своё = ЖЕНСКОЕ.get(язык, {}).get(род)
    старое = ЯЗЫКИ[язык]["пары"][род]
    return (tuple(своё) + tuple(старое[3:])) if своё else старое


def страница(язык, форма, род, i=0, женское=False):
    я = ЯЗЫКИ[язык]
    причина, следствие, придаточная, общ_п, общ_с = (пара_ж(язык, род) if женское
                                                     else я["пары"][род])
    if форма == "закон":
        return я["закон"].format(оп=общ_п, ос=общ_с)
    if форма == "вывод":
        # MODUS PONENS НАД УЖЕ ОБЪЯВЛЕННЫМ ЗАКОНОМ (04.09). Дом держал ЗАКОН
        # («когда человек устал, он ошибается чаще») и СЛУЧАЙ («пётр устал.
        # поэтому пётр ошибается чаще») порознь, и связи между ними не показывал
        # ни один показ. Здесь они сведены: закон, случай его посылки и ВЫВОД —
        # и вывод этот не факт о Петре, а следствие закона и посылки.
        # Стоило это одной связки на язык: обе части были объявлены давно, а
        # недоставало лишь слова «значит». Так и узнаётся, что род уже готов.
        X = (ИМЕНА_Ж[язык] if женское else я["имена"])[i % len(я["имена"])]
        закон = я["закон"].format(оп=общ_п, ос=общ_с).rstrip(".")
        return я["вывод"].format(з=закон + ".", п=причина.format(X=X), с=следствие.format(X=X))
    if форма == "основание":
        # ОСНОВАНИЕ ЗАКОНА — причина ОДНИМ УРОВНЕМ НИЖЕ, и без неё дом отвечал
        # кругом. Форма «кратко» спрашивала «почему, когда человек устал, он
        # ошибается чаще?» и отвечала «потому что человек устал» — то есть
        # повторяла условие, стоящее в самом вопросе. Части истинны, а ответ
        # пуст: круг есть ложь ФОРМЫ при истинных частях, и корпус не вправе
        # учить ему (М-182).
        #
        # Основание не выводится из пары и не может быть выведено: «усталость
        # ослабляет внимание» — знание о человеке, а не следствие объявленного.
        # Потому оно ОБЪЯВЛЕНО вместе со своим вопросом, целой фразой на язык:
        # вопрос о законе стоит в естественном порядке («почему человек
        # ошибается чаще, когда устал?»), какого не даст ни одна перестановка
        # объявленных кусков, а связка причины входит в само основание — так
        # французское «parce qu'on» и польское «bo» встают без склейки в коде.
        вопрос, основание = я["основания"][род]
        return f"{вопрос} {основание}."
    if форма == "основание_многих":
        # ТОТ ЖЕ ЗАКОН, СПРОШЕННЫЙ О МНОГИХ. Обобщённое единственное («человек
        # боится») и обобщённое множественное («люди боятся») суть два регистра
        # одного закона, и человек спрашивает вторым не реже первого. Ответ у
        # обоих ОДИН — то самое основание: так дом показывает, что поверхность
        # вопроса меняется, а причина нет, и это первый признак, по которому
        # рынок отличает форму от строки.
        return f'{я["вопросы_многих"][род]} {я["основания"][род][1]}.'
    if форма == "кратко":
        if "кратко" not in я:
            return None
        # ВОПРОС ОДНИМ ПРЕДЛОЖЕНИЕМ, БЕЗ ПРЕДШЕСТВУЮЩЕГО ЗАКОНА: так спрашивает
        # человек («почему человек ошибается, когда устал?»), и до этой формы
        # весь род требовал, чтобы закон стоял перед вопросом.
        общ_в = (я.get("общ_вопрос") or ())
        return я["кратко"].format(оп=общ_п, ос=общ_с, ов=(общ_в[род] if общ_в else общ_с),
                                  осн=я["основания"][род][1])
    if форма == "закон_вопрос":
        # ВОПРОС НАД ОБОБЩЕНИЕМ: человек спрашивает о ЧЕЛОВЕКЕ, а не об имени
        # («почему человек ошибается, когда устал?»), и до этой формы весь род
        # отвечал только про названного Петра. Ответ — та же причина, что и в
        # частном случае: закон и его случай говорят одно.
        общ_в = (я.get("общ_вопрос") or ())
        return я["закон_вопрос"].format(оп=общ_п, ос=общ_с, ов=(общ_в[род] if общ_в else общ_с))
    X = (ИМЕНА_Ж[язык] if женское else я["имена"])[i % len(я["имена"])]
    вопр = (я.get("вопр_след") or ())
    поля = dict(п=причина.format(X=X), с=следствие.format(X=X), пп=придаточная.format(X=X),
                в=(вопр[род] if вопр else следствие).format(X=X))
    return я[форма].format(**поля)


def цель(язык, i):
    """«зачем человек спит? чтобы отдохнуть.» — цель поступка, объявленная парой."""
    я = ЯЗЫКИ[язык]
    д, ц = я["цели"][i % len(я["цели"])]
    return я["зачем_рамка"].format(д=д, ц=ц)


def цель_многих(язык, i):
    """«зачем люди спят? чтобы отдохнуть.» — тот же вопрос о цели, спрошенный о
    многих. ЦЕЛЬ ОДНА, а лицо вопроса второе: меняется только дело, и потому
    объявлено только оно (тот же закон, что у основания многих)."""
    я = ЯЗЫКИ[язык]
    _, ц = я["цели"][i % len(я["цели"])]
    return я["зачем_рамка"].format(д=я["дела_многих"][i % len(я["дела_многих"])], ц=ц)


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for род in РОДЫ:
            вон[страница(язык, "закон", род)] = (язык, "закон")
            вон[страница(язык, "закон_вопрос", род)] = (язык, "закон_вопрос")
            вон[страница(язык, "основание", род)] = (язык, "основание")
            вон[страница(язык, "основание_многих", род)] = (язык, "основание_многих")
            с = страница(язык, "кратко", род)
            if с:
                вон[с] = (язык, "кратко")
            for ж in (False, True):
                for i in range(len(я["имена"])):
                    вон[страница(язык, "вывод", род, i, ж)] = (язык, "вывод")
                for i in range(len(я["имена"])):
                    for форма in ("правило", "вопрос"):
                        вон[страница(язык, форма, род, i, ж)] = (язык, форма)
        for i in range(len(я["цели"])):
            вон[цель(язык, i)] = (язык, "зачем")
            вон[цель_многих(язык, i)] = (язык, "зачем_многих")
    return вон


ПОКАЗЫ = _все_показы()


def судить(строка):
    """(судимо, истинно): показ дома истинен. Строка, севшая в рамку рода, но
    сцепившая ЧУЖУЮ причину с этим следствием, — ложь: причина объявлена."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for язык, я in ЯЗЫКИ.items():
        for род in РОДЫ:
            причина, следствие, _, _, _ = я["пары"][род]
            for i in range(len(я["имена"])):
                X = я["имена"][i % len(я["имена"])]
                хвост = следствие.format(X=X)
                # та же рамка, то же следствие, но причина иная — ложь
                if хвост in с and any(с.startswith(я["пары"][д][0].format(X=X)) for д in РОДЫ if д != род):
                    return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        for форма in ФОРМЫ:
            с = цель_многих(язык, 0) if форма == "зачем_многих" else цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
            if с is None:
                continue
            судимо, истинно = судить(с)
            assert судимо and истинно, (язык, форма, с)
        # МУТАНТ: чужая причина при этом следствии
        чужая = я["правило"].format(п=я["пары"][ПОТРЕБНОСТЬ][0].format(X=я["имена"][0]),
                                    с=я["пары"][УСТАЛОСТЬ][1].format(X=я["имена"][0]))
        судимо, истинно = судить(чужая)
        assert судимо and not истинно, (язык, чужая)
        мутанты += 1
    for язык in ("ru", "en", "de"):
        for форма in ФОРМЫ:
            печать = цель_многих(язык, 0) if форма == "зачем_многих" else цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
            if печать is None:
                continue
            print("  ", печать[:104])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
