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

ПОВОДЫ, А НЕ РОДЫ (13.09). Шесть видов поведения звались здесь `РОДЫ` — и слово это в корпусе
занято: `РОДЫ` есть объявление РОДОВ ПОКАЗА, имён, под которыми лежат страницы дома. Указатель
родов прочёл `(0, 1, 2, 3, 4, 5)` как шесть родов, названных цифрами, и напечатал у каждого
«страниц 0», пока 1 635 живых страниц лежали вне всякого рода. Дом не лгал: он говорил о своём.

    СЛОВО, ЗАНЯТОЕ КОРПУСОМ, НЕЛЬЗЯ БРАТЬ ДЛЯ СВОЕЙ ОСИ — даже когда оно к ней подходит.
    Столкновение это тихо: дом работает, суд зелен, и лишь общий указатель печатает вздор
    и не жалуется, ибо ноль страниц у рода есть для него законный ответ.

Шесть видов поведения зовутся теперь `ПОВОДЫ`, а роды показа дом объявляет в `ФОРМЫ` — их
одиннадцать, и все они названы страницами.

    python3 tools/behaviorforms.py    # самопроверка с мутантами
"""
УСТАЛОСТЬ, ПОТРЕБНОСТЬ, ЭМОЦИЯ, НАМЕРЕНИЕ, ПРИВЫЧКА, ВНИМАНИЕ = range(6)
# ЧУВСТВА И УМ (25.09, дом 3 наряда ведущего по слову владельца — «поведение и ум», «обыденные темы»): свод знал
# ОДНО чувство — страх неизвестного (24 английские строки из 1 797 страниц дома) — и ни одного закона ума. Шесть
# новых поводов стоят ЗДЕСЬ, в той же двери закона «причина → следствие», а не рядом: дом отклика берёт закон у
# дома поведения слово в слово, и второй дом законов о человеке был бы второй дверью.
РАДОСТЬ, ГРУСТЬ, ГНЕВ, СКУКА, ПАМЯТЬ, СОН = range(6, 12)
ПОВОДЫ = (УСТАЛОСТЬ, ПОТРЕБНОСТЬ, ЭМОЦИЯ, НАМЕРЕНИЕ, ПРИВЫЧКА, ВНИМАНИЕ, РАДОСТЬ, ГРУСТЬ, ГНЕВ, СКУКА, ПАМЯТЬ, СОН)

# пара = (причина главной клаузой, следствие, причина придаточной клаузой,
#         обобщение: «когда <причина>, <следствие>»)
import pathlib as _pathlib  # noqa: E402
import asking  # noqa: E402 — дом пары: объявленные вопросные слова
import sys as _sys  # noqa: E402
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import frgram as _fr  # французская элизия: закон над готовой страницей
import closedworld as _зк  # noqa: E402 — закон замкнутого мира: род прошедшего

ЯЗЫКИ = {
    "ru": dict(
        имена=("Пётр", "Иван", "Олег", "Борис"),   # имя лица — с заглавной, как в пакете (05.09)
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
# ОБЪЯВЛЕННЫЙ ПРОПУСК: «кратко» не пишется по-немецки и по-голландски, ибо их
# порядок ставит местоимение перед именем (М-175). Прибор щербатости читает это
# объявление и щербатостью дыру не зовёт.
# ======================================================================================================
# ЧУВСТВА И УМ — шесть поводов (25.09). Всякое следствие, как и у прежних шести, СРАВНИТЕЛЬНОЕ или названное
# чувство при названной причине («получил подарок → радуется», «мало спал → устаёт быстрее»), а основание —
# знание о человеке одним уровнем ниже, объявленное целой фразой («потому что сон восстанавливает силы»). Мнения
# («грусть проходит быстрее, когда её называют») здесь нет: закон проверяем соседом, мнение — ничем (holon, 04.09).
# Прежний литерал ЯЗЫКИ не тронут: новые поводы дописываются блоком, и прежние страницы остаются байт в байт.
# ======================================================================================================
_ЧУВСТВА_И_УМ = {
    "ru": dict(
        пары=(("{X} получил подарок", "{X} радуется", "{X} получил подарок", "человек получает подарок", "он радуется"),
              ("{X} потерял дорогую ему вещь", "{X} грустит", "{X} потерял дорогую ему вещь",
               "человек теряет дорогую ему вещь", "он грустит"),
              ("{X} получил несправедливое замечание", "{X} злится", "{X} получил несправедливое замечание",
               "человек получает несправедливое замечание", "он злится"),
              ("{X} сидит без дела", "{X} скучает", "{X} сидит без дела", "человек сидит без дела", "он скучает"),
              ("{X} много раз повторил слова", "{X} помнит их лучше", "{X} много раз повторил слова",
               "человек много раз повторяет слова", "он помнит их лучше"),
              ("{X} мало спал", "{X} устаёт быстрее", "{X} мало спал", "человек мало спит", "он устаёт быстрее")),
        основания=(("почему человек радуется, когда получает подарок?", "потому что подарок показывает, что о нём помнят"),
                   ("почему человек грустит, когда теряет дорогую ему вещь?", "потому что ему не хватает того, что было дорого"),
                   ("почему человек злится, когда получает несправедливое замечание?",
                    "потому что человек ждёт, что с ним поступят справедливо"),
                   ("почему человек скучает, когда сидит без дела?", "потому что время без занятия тянется долго"),
                   ("почему человек помнит слова лучше, когда много раз их повторяет?", "потому что повторение укрепляет память"),
                   ("почему человек устаёт быстрее, когда мало спит?", "потому что сон восстанавливает силы")),
        вопросы_многих=("почему люди радуются подаркам?", "почему люди грустят, когда теряют дорогие им вещи?",
                        "почему люди злятся на несправедливые замечания?", "почему люди скучают без дела?",
                        "почему люди лучше помнят то, что повторяют?", "почему люди устают быстрее, когда мало спят?")),
    "en": dict(
        пары=(("{X} got a gift", "{X} is glad", "{X} got a gift", "a person gets a gift", "that person is glad"),
              ("{X} lost something dear", "{X} is sad", "{X} lost something dear", "a person loses something dear",
               "that person is sad"),
              ("{X} got an unfair remark", "{X} is angry", "{X} got an unfair remark", "a person gets an unfair remark",
               "that person is angry"),
              ("{X} has nothing to do", "{X} is bored", "{X} has nothing to do", "a person has nothing to do",
               "that person is bored"),
              ("{X} repeated the words many times", "{X} remembers them better", "{X} repeated the words many times",
               "a person repeats words many times", "that person remembers them better"),
              ("{X} slept little", "{X} gets tired faster", "{X} slept little", "a person sleeps little",
               "that person gets tired faster")),
        вопр_след=("is {X} glad", "is {X} sad", "is {X} angry", "is {X} bored", "does {X} remember them better",
                   "does {X} get tired faster"),
        общ_вопрос=("is that person glad", "is that person sad", "is that person angry", "is that person bored",
                    "does that person remember them better", "does that person get tired faster"),
        основания=(("why is a person glad when they get a gift?", "because a gift shows that someone remembers them"),
                   ("why is a person sad when they lose something dear?", "because they miss what was dear to them"),
                   ("why is a person angry when they get an unfair remark?", "because a person expects to be treated fairly"),
                   ("why is a person bored when they have nothing to do?", "because time without an occupation seems long"),
                   ("why does a person remember words better when they repeat them many times?",
                    "because repetition strengthens memory"),
                   ("why does a person get tired faster when they sleep little?", "because sleep restores strength")),
        вопросы_многих=("why are people glad to get gifts?", "why are people sad when they lose something dear?",
                        "why do people get angry at unfair remarks?", "why are people bored when they have nothing to do?",
                        "why do people remember better what they repeat?",
                        "why do people get tired faster when they sleep little?")),
    "de": dict(
        пары=(("{X} hat ein Geschenk bekommen", "freut sich {X}", "{X} ein Geschenk bekommen hat",
               "ein Mensch ein Geschenk bekommt", "freut er sich"),
              ("{X} hat etwas Liebes verloren", "ist {X} traurig", "{X} etwas Liebes verloren hat",
               "ein Mensch etwas Liebes verliert", "ist er traurig"),
              ("{X} hat eine ungerechte Bemerkung bekommen", "ärgert sich {X}", "{X} eine ungerechte Bemerkung bekommen hat",
               "ein Mensch eine ungerechte Bemerkung bekommt", "ärgert er sich"),
              ("{X} hat nichts zu tun", "langweilt sich {X}", "{X} nichts zu tun hat", "ein Mensch nichts zu tun hat",
               "langweilt er sich"),
              ("{X} hat die Wörter oft wiederholt", "merkt {X} sie sich besser", "{X} die Wörter oft wiederholt hat",
               "ein Mensch Wörter oft wiederholt", "merkt er sie sich besser"),
              ("{X} hat wenig geschlafen", "wird {X} schneller müde", "{X} wenig geschlafen hat", "ein Mensch wenig schläft",
               "wird er schneller müde")),
        основания=(("warum freut sich ein Mensch, wenn er ein Geschenk bekommt?", "weil ein Geschenk zeigt, dass jemand an ihn denkt"),
                   ("warum ist ein Mensch traurig, wenn er etwas Liebes verliert?", "weil ihm fehlt, was ihm lieb war"),
                   ("warum ärgert sich ein Mensch, wenn er eine ungerechte Bemerkung bekommt?",
                    "weil ein Mensch erwartet, gerecht behandelt zu werden"),
                   ("warum langweilt sich ein Mensch, wenn er nichts zu tun hat?", "weil Zeit ohne Beschäftigung lang wird"),
                   ("warum merkt sich ein Mensch Wörter besser, wenn er sie oft wiederholt?",
                    "weil Wiederholung das Gedächtnis stärkt"),
                   ("warum wird ein Mensch schneller müde, wenn er wenig schläft?", "weil Schlaf die Kräfte wiederherstellt")),
        вопросы_многих=("warum freuen sich Menschen über Geschenke?", "warum sind Menschen traurig, wenn sie etwas Liebes verlieren?",
                        "warum ärgern sich Menschen über ungerechte Bemerkungen?",
                        "warum langweilen sich Menschen, wenn sie nichts zu tun haben?",
                        "warum merken sich Menschen besser, was sie wiederholen?",
                        "warum werden Menschen schneller müde, wenn sie wenig schlafen?")),
    "fr": dict(
        пары=(("{X} a reçu un cadeau", "{X} est content", "{X} a reçu un cadeau", "une personne reçoit un cadeau",
               "elle est contente"),
              ("{X} a perdu une chose chère", "{X} est triste", "{X} a perdu une chose chère",
               "une personne perd une chose chère", "elle est triste"),
              ("{X} a reçu une remarque injuste", "{X} est en colère", "{X} a reçu une remarque injuste",
               "une personne reçoit une remarque injuste", "elle est en colère"),
              ("{X} n'a rien à faire", "{X} s'ennuie", "{X} n'a rien à faire", "une personne n'a rien à faire",
               "elle s'ennuie"),
              ("{X} a répété les mots plusieurs fois", "{X} les retient mieux", "{X} a répété les mots plusieurs fois",
               "une personne répète des mots plusieurs fois", "elle les retient mieux"),
              ("{X} a peu dormi", "{X} se fatigue plus vite", "{X} a peu dormi", "une personne dort peu",
               "elle se fatigue plus vite")),
        основания=(("pourquoi une personne est-elle contente quand elle reçoit un cadeau ?",
                    "parce qu'un cadeau montre que quelqu'un pense à elle"),
                   ("pourquoi une personne est-elle triste quand elle perd une chose chère ?",
                    "parce que ce qui lui était cher lui manque"),
                   ("pourquoi une personne est-elle en colère quand elle reçoit une remarque injuste ?",
                    "parce qu'une personne attend d'être traitée avec justice"),
                   ("pourquoi une personne s'ennuie-t-elle quand elle n'a rien à faire ?",
                    "parce que le temps sans occupation paraît long"),
                   ("pourquoi une personne retient-elle mieux les mots quand elle les répète plusieurs fois ?",
                    "parce que la répétition renforce la mémoire"),
                   ("pourquoi une personne se fatigue-t-elle plus vite quand elle dort peu ?", "parce que le sommeil rend les forces")),
        вопросы_многих=("pourquoi les gens sont-ils contents de recevoir des cadeaux ?",
                        "pourquoi les gens sont-ils tristes quand ils perdent une chose chère ?",
                        "pourquoi les gens se fâchent-ils contre les remarques injustes ?",
                        "pourquoi les gens s'ennuient-ils quand ils n'ont rien à faire ?",
                        "pourquoi les gens retiennent-ils mieux ce qu'ils répètent ?",
                        "pourquoi les gens se fatiguent-ils plus vite quand ils dorment peu ?")),
    "es": dict(
        пары=(("{X} recibió un regalo", "{X} está contento", "{X} recibió un regalo", "una persona recibe un regalo",
               "está contenta"),
              ("{X} perdió algo querido", "{X} está triste", "{X} perdió algo querido", "una persona pierde algo querido",
               "está triste"),
              ("{X} recibió un comentario injusto", "{X} está enfadado", "{X} recibió un comentario injusto",
               "una persona recibe un comentario injusto", "está enfadada"),
              ("{X} no tiene nada que hacer", "{X} se aburre", "{X} no tiene nada que hacer",
               "una persona no tiene nada que hacer", "se aburre"),
              ("{X} repitió las palabras muchas veces", "{X} las recuerda mejor", "{X} repitió las palabras muchas veces",
               "una persona repite palabras muchas veces", "las recuerda mejor"),
              ("{X} durmió poco", "{X} se cansa antes", "{X} durmió poco", "una persona duerme poco", "se cansa antes")),
        основания=(("¿por qué una persona está contenta cuando recibe un regalo?",
                    "porque un regalo muestra que alguien piensa en ella"),
                   ("¿por qué una persona está triste cuando pierde algo querido?", "porque echa de menos lo que le era querido"),
                   ("¿por qué una persona está enfadada cuando recibe un comentario injusto?",
                    "porque una persona espera que la traten con justicia"),
                   ("¿por qué una persona se aburre cuando no tiene nada que hacer?", "porque el tiempo sin ocupación parece largo"),
                   ("¿por qué una persona recuerda mejor las palabras cuando las repite muchas veces?",
                    "porque la repetición refuerza la memoria"),
                   ("¿por qué una persona se cansa antes cuando duerme poco?", "porque el sueño repone las fuerzas")),
        вопросы_многих=("¿por qué la gente se alegra de recibir regalos?", "¿por qué la gente está triste cuando pierde algo querido?",
                        "¿por qué la gente se enfada ante los comentarios injustos?",
                        "¿por qué la gente se aburre cuando no tiene nada que hacer?",
                        "¿por qué la gente recuerda mejor lo que repite?", "¿por qué la gente se cansa antes cuando duerme poco?")),
    "it": dict(
        пары=(("{X} ha ricevuto un regalo", "{X} è contento", "{X} ha ricevuto un regalo", "una persona riceve un regalo",
               "è contenta"),
              ("{X} ha perso una cosa cara", "{X} è triste", "{X} ha perso una cosa cara", "una persona perde una cosa cara",
               "è triste"),
              ("{X} ha ricevuto un rimprovero ingiusto", "{X} è arrabbiato", "{X} ha ricevuto un rimprovero ingiusto",
               "una persona riceve un rimprovero ingiusto", "è arrabbiata"),
              ("{X} non ha niente da fare", "{X} si annoia", "{X} non ha niente da fare",
               "una persona non ha niente da fare", "si annoia"),
              ("{X} ha ripetuto le parole molte volte", "{X} le ricorda meglio", "{X} ha ripetuto le parole molte volte",
               "una persona ripete parole molte volte", "le ricorda meglio"),
              ("{X} ha dormito poco", "{X} si stanca prima", "{X} ha dormito poco", "una persona dorme poco", "si stanca prima")),
        основания=(("perché una persona è contenta quando riceve un regalo?", "perché un regalo mostra che qualcuno pensa a lei"),
                   ("perché una persona è triste quando perde una cosa cara?", "perché le manca ciò che le era caro"),
                   ("perché una persona è arrabbiata quando riceve un rimprovero ingiusto?",
                    "perché una persona si aspetta di essere trattata con giustizia"),
                   ("perché una persona si annoia quando non ha niente da fare?", "perché il tempo senza occupazione sembra lungo"),
                   ("perché una persona ricorda meglio le parole quando le ripete molte volte?",
                    "perché la ripetizione rafforza la memoria"),
                   ("perché una persona si stanca prima quando dorme poco?", "perché il sonno ridà le forze")),
        вопросы_многих=("perché le persone sono contente di ricevere regali?",
                        "perché le persone sono tristi quando perdono una cosa cara?",
                        "perché le persone si arrabbiano per i rimproveri ingiusti?",
                        "perché le persone si annoiano quando non hanno niente da fare?",
                        "perché le persone ricordano meglio ciò che ripetono?",
                        "perché le persone si stancano prima quando dormono poco?")),
    "pt": dict(
        пары=(("{X} recebeu um presente", "{X} está contente", "{X} recebeu um presente", "uma pessoa recebe um presente",
               "está contente"),
              ("{X} perdeu uma coisa querida", "{X} está triste", "{X} perdeu uma coisa querida",
               "uma pessoa perde uma coisa querida", "está triste"),
              ("{X} recebeu um comentário injusto", "{X} está zangado", "{X} recebeu um comentário injusto",
               "uma pessoa recebe um comentário injusto", "está zangada"),
              ("{X} não tem nada para fazer", "{X} aborrece-se", "{X} não tem nada para fazer",
               "uma pessoa não tem nada para fazer", "aborrece-se"),
              ("{X} repetiu as palavras muitas vezes", "{X} lembra-se melhor delas", "{X} repetiu as palavras muitas vezes",
               "uma pessoa repete palavras muitas vezes", "lembra-se melhor delas"),
              ("{X} dormiu pouco", "{X} cansa-se mais depressa", "{X} dormiu pouco", "uma pessoa dorme pouco",
               "cansa-se mais depressa")),
        основания=(("porque é que uma pessoa está contente quando recebe um presente?",
                    "porque um presente mostra que alguém pensa nela"),
                   ("porque é que uma pessoa está triste quando perde uma coisa querida?",
                    "porque sente falta do que lhe era querido"),
                   ("porque é que uma pessoa está zangada quando recebe um comentário injusto?",
                    "porque uma pessoa espera ser tratada com justiça"),
                   ("porque é que uma pessoa se aborrece quando não tem nada para fazer?",
                    "porque o tempo sem ocupação parece longo"),
                   ("porque é que uma pessoa se lembra melhor das palavras quando as repete muitas vezes?",
                    "porque a repetição reforça a memória"),
                   ("porque é que uma pessoa se cansa mais depressa quando dorme pouco?", "porque o sono repõe as forças")),
        вопросы_многих=("porque é que as pessoas ficam contentes com presentes?",
                        "porque é que as pessoas ficam tristes quando perdem uma coisa querida?",
                        "porque é que as pessoas se zangam com comentários injustos?",
                        "porque é que as pessoas se aborrecem quando não têm nada para fazer?",
                        "porque é que as pessoas se lembram melhor do que repetem?",
                        "porque é que as pessoas se cansam mais depressa quando dormem pouco?")),
    "nl": dict(
        пары=(("{X} heeft een cadeau gekregen", "is {X} blij", "{X} een cadeau heeft gekregen", "een mens een cadeau krijgt",
               "is hij blij"),
              ("{X} is iets dierbaars kwijtgeraakt", "is {X} verdrietig", "{X} iets dierbaars is kwijtgeraakt",
               "een mens iets dierbaars kwijtraakt", "is hij verdrietig"),
              ("{X} heeft een onterechte opmerking gekregen", "is {X} boos", "{X} een onterechte opmerking heeft gekregen",
               "een mens een onterechte opmerking krijgt", "is hij boos"),
              ("{X} heeft niets te doen", "verveelt {X} zich", "{X} niets te doen heeft", "een mens niets te doen heeft",
               "verveelt hij zich"),
              ("{X} heeft de woorden vaak herhaald", "onthoudt {X} ze beter", "{X} de woorden vaak heeft herhaald",
               "een mens woorden vaak herhaalt", "onthoudt hij ze beter"),
              ("{X} heeft weinig geslapen", "wordt {X} sneller moe", "{X} weinig heeft geslapen", "een mens weinig slaapt",
               "wordt hij sneller moe")),
        основания=(("waarom is een mens blij als hij een cadeau krijgt?", "omdat een cadeau laat zien dat iemand aan hem denkt"),
                   ("waarom is een mens verdrietig als hij iets dierbaars kwijtraakt?", "omdat hij mist wat hem dierbaar was"),
                   ("waarom is een mens boos als hij een onterechte opmerking krijgt?",
                    "omdat een mens verwacht eerlijk behandeld te worden"),
                   ("waarom verveelt een mens zich als hij niets te doen heeft?", "omdat tijd zonder bezigheid lang lijkt"),
                   ("waarom onthoudt een mens woorden beter als hij ze vaak herhaalt?", "omdat herhaling het geheugen versterkt"),
                   ("waarom wordt een mens sneller moe als hij weinig slaapt?", "omdat slaap de krachten herstelt")),
        вопросы_многих=("waarom zijn mensen blij met cadeaus?", "waarom zijn mensen verdrietig als ze iets dierbaars kwijtraken?",
                        "waarom worden mensen boos om onterechte opmerkingen?",
                        "waarom vervelen mensen zich als ze niets te doen hebben?",
                        "waarom onthouden mensen beter wat ze herhalen?", "waarom worden mensen sneller moe als ze weinig slapen?")),
    "pl": dict(
        пары=(("{X} dostał prezent", "{X} się cieszy", "{X} dostał prezent", "człowiek dostaje prezent", "cieszy się"),
              ("{X} stracił coś bliskiego", "{X} jest smutny", "{X} stracił coś bliskiego", "człowiek traci coś bliskiego",
               "jest smutny"),
              ("{X} dostał niesprawiedliwą uwagę", "{X} się złości", "{X} dostał niesprawiedliwą uwagę",
               "człowiek dostaje niesprawiedliwą uwagę", "złości się"),
              ("{X} nie ma nic do roboty", "{X} się nudzi", "{X} nie ma nic do roboty", "człowiek nie ma nic do roboty",
               "nudzi się"),
              ("{X} wiele razy powtórzył słowa", "{X} lepiej je pamięta", "{X} wiele razy powtórzył słowa",
               "człowiek wiele razy powtarza słowa", "lepiej je pamięta"),
              ("{X} mało spał", "{X} szybciej się męczy", "{X} mało spał", "człowiek mało śpi", "szybciej się męczy")),
        основания=(("dlaczego człowiek cieszy się, kiedy dostaje prezent?", "bo prezent pokazuje, że ktoś o nim pamięta"),
                   ("dlaczego człowiek jest smutny, kiedy traci coś bliskiego?", "bo brakuje mu tego, co było mu bliskie"),
                   ("dlaczego człowiek złości się, kiedy dostaje niesprawiedliwą uwagę?",
                    "bo człowiek oczekuje, że zostanie potraktowany sprawiedliwie"),
                   ("dlaczego człowiek nudzi się, kiedy nie ma nic do roboty?", "bo czas bez zajęcia wydaje się długi"),
                   ("dlaczego człowiek lepiej pamięta słowa, kiedy wiele razy je powtarza?", "bo powtarzanie wzmacnia pamięć"),
                   ("dlaczego człowiek szybciej się męczy, kiedy mało śpi?", "bo sen przywraca siły")),
        вопросы_многих=("dlaczego ludzie cieszą się z prezentów?", "dlaczego ludzie są smutni, kiedy tracą coś bliskiego?",
                        "dlaczego ludzie złoszczą się na niesprawiedliwe uwagi?",
                        "dlaczego ludzie nudzą się, kiedy nie mają nic do roboty?",
                        "dlaczego ludzie lepiej pamiętają to, co powtarzają?",
                        "dlaczego ludzie szybciej się męczą, kiedy mało śpią?")),
}
for _яз, _добавка in _ЧУВСТВА_И_УМ.items():
    for _ключ, _ряд in _добавка.items():
        assert len(_ряд) == len(ПОВОДЫ) - 6, (_яз, _ключ)
        ЯЗЫКИ[_яз][_ключ] = tuple(ЯЗЫКИ[_яз][_ключ]) + tuple(_ряд)
assert set(_ЧУВСТВА_И_УМ) == set(ЯЗЫКИ), "новые поводы обязаны стоять на всех девяти языках"

ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {"кратко": frozenset({"de", "nl"})}

# ВЕЕР ВОПРОСА О ПРИЧИНЕ (22.09, заказ руки agent по полосе беседы). Дом показывал причинный
# вопрос ОДИН раз на язык в каждой поверхности, и это ниже закона повтора: «почему люди боятся
# неизвестного?» — один показ, «зачем человек спит» — один. Человек спрашивает то же ИНАЧЕ, и
# продукт, знающий одну формулировку, молчит на второй.
#
#     ПОВЕРХНОСТЬ ВОПРОСА МЕНЯЕТСЯ, А ПРИЧИНА НЕТ — и веер показывает ровно это.
#
# ВЕЕР НЕ СОЧИНЯЕТ ЗНАНИЯ: основание остаётся объявленное. Меняются ПОРЯДОК («утверждение
# впереди, вопрос голой головой») и ГЛУБИНА ОТВЕТА (основание одно — и основание, за которым
# стои́т сам закон).
#
# ВТОРАЯ ВОПРОСНАЯ ГОЛОВА ОТВЕРГНУТА СУДОМ ПИСЬМА, И ОТВЕРГНУТА ПО ПРАВУ. Первая редакция веера
# спрашивала «отчего…», «aus welchem Grund…», «per quale motivo…» — и ворота не пустили 32
# страницы: вопрос обязан открываться ОБЪЯВЛЕННЫМ вопросным словом (`asking`), а эти головы
# многословны и открываются предлогом. Односложная замена есть у русского («отчего»), немецкого
# («wieso»), польского («czemu») — и НЕТ у английского и французского.
#
#     ВЫРОВНЕННЫЙ ПО ЯЗЫКАМ ДОМ НЕ ЧИНИТСЯ ПРИБАВКОЙ ТРЁМ ЯЗЫКАМ ИЗ ДЕВЯТИ: чиня перекос
#     родов, наживёшь перекос языков.
#
# Долг назван: вторые головы ждут объявления в ПАКЕТАХ (`ask_words`) — там, где займ вопросных
# слов и погашается, — и дописывать их надо на всех девяти разом.
ГОЛАЯ_ГОЛОВА = {"ru": "почему?", "en": "why?", "de": "warum?", "fr": "pourquoi ?",
                "es": "¿por qué?", "it": "perché?", "pt": "porquê?", "nl": "waarom?",
                "pl": "dlaczego?"}
# СТРАЖ СВЕРЯЕТ ГОЛОВУ С ОБЪЯВЛЕНИЕМ ДОМА ПАРЫ, А НЕ С ПОВЕДЕНИЕМ ЕГО РАЗБОРА. Голая голова
# кончается вопросным словом языка: восемь из девяти суть само слово («почему», «warum»,
# «porquê»), испанская — предлог при объявленном слове («¿por qué»), и дом пары принимает её
# тем же правилом, каким принимает «на сколько…». Слово берётся ПОСЛЕДНИМ: им голова и кончается.
for _яз, _гол in ГОЛАЯ_ГОЛОВА.items():
    _слово = _гол.strip("?¿ ").lower().split()[-1]
    assert _слово in asking.ЗАЧИНЫ, (_яз, _гол, "вопросное слово головы не объявлено домом пары")

ФОРМЫ = ("правило", "вопрос", "закон", "закон_вопрос", "кратко", "основание", "основание_многих", "зачем", "зачем_многих", "зачем_многих_утв", "вывод", "веер_причины")

for _яз, _я in ЯЗЫКИ.items():
    assert len(_я["пары"]) == len(ПОВОДЫ), (_яз, len(_я["пары"]))
    assert len(_я["имена"]) >= 4, _яз
    for _п in _я["пары"]:
        assert len(_п) == 5, (_яз, _п)
    assert "вопр_след" not in _я or len(_я["вопр_след"]) == len(ПОВОДЫ), _яз
    assert "общ_вопрос" not in _я or len(_я["общ_вопрос"]) == len(ПОВОДЫ), _яз
    assert len(_я["основания"]) == len(ПОВОДЫ), _яз
    assert len(_я["вопросы_многих"]) == len(ПОВОДЫ), _яз
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
    "ru": ["Анна", "Мария", "Ольга", "Вера"],
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

# ЖЕНСКИЕ ФОРМЫ НОВЫХ ПОВОДОВ — лишь там, где язык их меняет (прошедшее у ru и pl, прилагательное у fr, es, it, pt)
ЖЕНСКОЕ["ru"].update({
    РАДОСТЬ: ["{X} получила подарок", "{X} радуется", "{X} получила подарок"],
    ГРУСТЬ: ["{X} потеряла дорогую ей вещь", "{X} грустит", "{X} потеряла дорогую ей вещь"],
    ГНЕВ: ["{X} получила несправедливое замечание", "{X} злится", "{X} получила несправедливое замечание"],
    ПАМЯТЬ: ["{X} много раз повторила слова", "{X} помнит их лучше", "{X} много раз повторила слова"],
    СОН: ["{X} мало спала", "{X} устаёт быстрее", "{X} мало спала"],
})
ЖЕНСКОЕ["pl"].update({
    РАДОСТЬ: ["{X} dostała prezent", "{X} się cieszy", "{X} dostała prezent"],
    ГРУСТЬ: ["{X} straciła coś bliskiego", "{X} jest smutna", "{X} straciła coś bliskiego"],
    ГНЕВ: ["{X} dostała niesprawiedliwą uwagę", "{X} się złości", "{X} dostała niesprawiedliwą uwagę"],
    ПАМЯТЬ: ["{X} wiele razy powtórzyła słowa", "{X} lepiej je pamięta", "{X} wiele razy powtórzyła słowa"],
    СОН: ["{X} mało spała", "{X} szybciej się męczy", "{X} mało spała"],
})
ЖЕНСКОЕ["fr"].update({РАДОСТЬ: ["{X} a reçu un cadeau", "{X} est contente", "{X} a reçu un cadeau"]})
ЖЕНСКОЕ["es"].update({РАДОСТЬ: ["{X} recibió un regalo", "{X} está contenta", "{X} recibió un regalo"],
                      ГНЕВ: ["{X} recibió un comentario injusto", "{X} está enfadada", "{X} recibió un comentario injusto"]})
ЖЕНСКОЕ["it"].update({РАДОСТЬ: ["{X} ha ricevuto un regalo", "{X} è contenta", "{X} ha ricevuto un regalo"],
                      ГНЕВ: ["{X} ha ricevuto un rimprovero ingiusto", "{X} è arrabbiata",
                             "{X} ha ricevuto un rimprovero ingiusto"]})
ЖЕНСКОЕ["pt"].update({ГНЕВ: ["{X} recebeu um comentário injusto", "{X} está zangada", "{X} recebeu um comentário injusto"]})

for _яз in ЯЗЫКИ:
    assert len(ИМЕНА_Ж[_яз]) == len(ЯЗЫКИ[_яз]["имена"]), _яз
    assert (_яз in ЖЕНСКОЕ_НЕ_МЕНЯЕТСЯ) != (_яз in ЖЕНСКОЕ), _яз
    for _род, _тройка in ЖЕНСКОЕ.get(_яз, {}).items():
        assert 0 <= _род < len(ПОВОДЫ) and len(_тройка) == 3, (_яз, _род)
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
    if форма == "веер_причины":
        # ДВЕ ПОВЕРХНОСТИ, ЗАКОННЫЕ ВО ВСЕХ ДЕВЯТИ ЯЗЫКАХ: утверждение впереди с голой головой
        # вопроса, и объявленный вопрос с основанием, за которым стои́т сам закон.
        вопрос, основание = я["основания"][род]
        общ_п, общ_с = я["пары"][род][3], я["пары"][род][4]
        закон = я["закон"].format(оп=общ_п, ос=общ_с)
        многих = я["вопросы_многих"][род]
        веер = (f"{закон} {ГОЛАЯ_ГОЛОВА[язык]} {основание}.",
                f"{вопрос} {основание}: {закон}",
                f"{многих} {основание}: {закон}")
        return веер[i % len(веер)]
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



# ПОВЕСТВОВАТЕЛЬНОЕ ДЕЛО МНОГИХ — ТРЁМ ЯЗЫКАМ ОТДЕЛЬНО, ШЕСТИ ХВАТАЕТ СВОЕГО (09.09, ночь).
#
# Прибор [СЛОВО ОДНАЖДЫ] держал семьдесят три слова этого дома, и все они — ГЛАГОЛЫ, стоящие
# ровно в одном показе: «pourquoi les gens apprennent ?» — единственная строка свода со словом
# «apprennent». Лекарство есть то самое «утверждение + вопрос», какое прибор и называет
# рецептом: глагол показывается дважды в одной строке.
#
# ПОЛЕ `дела_многих` ДЛЯ ЭТОГО НЕ ГОДИТСЯ У ТРЁХ ЯЗЫКОВ, и это видно, а не угадано: у
# англичанина там «do people sleep», у немца «schlafen Menschen», у нидерландца «slapen
# mensen» — формы, писанные ДЛЯ ВОПРОСА, с инверсией. Поставить их повествованием значило бы
# написать «do people sleep. why do people sleep?» — грамматический вздор.
#
#     ФОРМА, ОБЪЯВЛЕННАЯ ДЛЯ ОДНОГО МЕСТА, НЕ ГОДИТСЯ ДЛЯ ДРУГОГО ЛИШЬ ОТТОГО, ЧТО СЛОВА В НЕЙ
#     ТЕ ЖЕ. Шесть языков объявили дело многих повествованием и годятся как есть; трое —
#     вопросом, и им объявлено отдельное поле.
ДЕЛА_МНОГИХ_УТВ = {
    "en": ("people sleep", "people eat", "people study"),
    "de": ("Menschen schlafen", "Menschen essen", "Menschen lernen"),
    "nl": ("mensen slapen", "mensen eten", "mensen leren"),
}


def дело_многих_утв(язык, i):
    """Повествовательное дело многих: своё поле у трёх языков, общее у шести."""
    ряд = ДЕЛА_МНОГИХ_УТВ.get(язык) or ЯЗЫКИ[язык]["дела_многих"]
    return ряд[i % len(ряд)]


def цель_многих_утв(язык, i):
    """«люди учатся. зачем люди учатся? чтобы уметь больше.» — глагол показан дважды."""
    я = ЯЗЫКИ[язык]
    return f"{дело_многих_утв(язык, i)}. {цель_многих(язык, i)}"


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for род in ПОВОДЫ:
            вон[страница(язык, "закон", род)] = (язык, "закон")
            вон[страница(язык, "закон_вопрос", род)] = (язык, "закон_вопрос")
            вон[страница(язык, "основание", род)] = (язык, "основание")
            вон[страница(язык, "основание_многих", род)] = (язык, "основание_многих")
            for i in range(3):
                вон[страница(язык, "веер_причины", род, i)] = (язык, "веер_причины")
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
            вон[цель_многих_утв(язык, i)] = (язык, "зачем_многих_утв")
    return вон


# ФРАНЦУЗСКАЯ ЭЛИЗИЯ ДЕЛАЕТСЯ НАД ГОТОВОЙ СТРАНИЦЕЙ (09.09). Дом собирает страницу во
# МНОГИХ местах, и набор показов есть ЕДИНСТВЕННОЕ место, через которое проходит всякая.
#
#     ЗАКОН, КАСАЮЩИЙСЯ ВСЯКОЙ СТРАНИЦЫ, ЗОВЁТСЯ ТАМ, ГДЕ ВСЯКАЯ СТРАНИЦА ПРОХОДИТ.
ПОКАЗЫ = {(_fr.элизия(с) if (v[0] if isinstance(v, tuple) else v) == "fr" else с): v
          for с, v in _все_показы().items()}


# РОД ПРОШЕДШЕГО СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ (08.09).
#
# Дом писал прошедшее по роду верно — и МОЛЧАЛ о подмене: «Пётр устала» не совпадает с его
# рамкой вовсе, и суд говорил «не моя» вместо «ложь». Тридцать проб из тридцати.
#
#     ФОРМА, ОТЛИЧАЮЩАЯСЯ ОТ ПОКАЗА ОДНОЙ БУКВОЙ РОДА, ЕСТЬ ЭТОТ ЖЕ ПОКАЗ ИСПОРЧЕННЫЙ.
#
# ЛИЦА У ДОМА СВОИ, И РОД ИХ ОБЪЯВЛЕН ЗДЕСЬ ЖЕ: мужские имена стоя́т в `ЯЗЫКИ[язык]["имена"]`,
# женские — в `ИМЕНА_Ж`. Закон берётся у замкнутого мира, читающий язык — у `rugram`.
_РОДЫ_ЛИЦ = {и: "m" for и in ЯЗЫКИ["ru"]["имена"]}
_РОДЫ_ЛИЦ.update({и: "f" for и in ИМЕНА_Ж["ru"]})


# РЯДЫ ДОМА — ЧАСТИ, СТОЯЩИЕ В ЕГО РАМКАХ НА ОДНОМ МЕСТЕ (21.09): лица, и все пять колонок
# объявленной пары — причина, следствие, дело, краткая причина, краткое следствие. Дыра
# «{X}» из них убирается: на её месте стои́т лицо, и оно есть свой ряд.
def _ряды():
    вон = []
    for я in ЯЗЫКИ.values():
        вон.append(tuple(я.get("имена") or ()))
        пары = я.get("пары") or ()
        ширина = max((len(п) for п in пары), default=0)
        for i in range(ширина):
            клетки = {п[i] for п in пары
                      if len(п) > i and isinstance(п[i], str) and п[i]}
            вон.append(tuple({к.replace("{X}", "").strip() for к in клетки if к.strip()}))
    return tuple(р for р in вон if len(р) > 1)


РЯДЫ = _ряды()

# ДОМ ОБЪЯВЛЯЕТ СЕБЯ СУДЯЩИМ ОБЪЯВЛЕНИЕМ: «когда человек устал, он ошибается чаще» неоткуда
# вывести, кроме как из объявленной пары причина↔следствие, и набор показов ЕСТЬ это
# объявление. Объявление проверяется прибором дважды: принимается лишь от СТРАЖА и лишь у
# того, кому нечего вычислять.
СУДИТ_ОБЪЯВЛЕНИЕМ = True


def судить(строка):
    """(судимо, истинно): показ дома истинен. Строка, севшая в рамку рода, но
    сцепившая ЧУЖУЮ причину с этим следствием, — ложь: причина объявлена."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for язык, я in ЯЗЫКИ.items():
        for род in ПОВОДЫ:
            причина, следствие, _, _, _ = я["пары"][род]
            for i in range(len(я["имена"])):
                X = я["имена"][i % len(я["имена"])]
                хвост = следствие.format(X=X)
                # та же рамка, то же следствие, но причина иная — ложь
                if хвост in с and any(с.startswith(я["пары"][д][0].format(X=X)) for д in ПОВОДЫ if д != род):
                    return True, False
    # РОД ПРОШЕДШЕГО: «Пётр устала» есть показ этого дома с испорченным родом, а не чужая строка
    if _зк.ложь_по_роду(с, ПОКАЗЫ, _РОДЫ_ЛИЦ):
        return True, False
    # ПЯТЫЙ БРАТ ЗАМКНУТОГО МИРА (21.09): строка, становящаяся показом при замене ОДНОГО
    # члена объявленного ряда, есть показ ЭТОГО дома с испорченной частью.
    #
    # Закон сцепки выше ловит одно: чужую ПРИЧИНУ при своём следствии, и ловит лишь там,
    # где следствие стои́т дословно. Подмена внутри следствия («ошибается чаще» →
    # «засыпает»), подмена лица, подмена слова в законе — всё это проходило мимо, и дом
    # МОЛЧАЛ о собственной порче.
    #
    #     ЗАКОН, СТЕРЕГУЩИЙ ОДНО МЕСТО СТРАНИЦЫ, СТЕРЕЖЁТ ОДНО МЕСТО, А НЕ СТРАНИЦУ.
    if _зк.ложь_по_ряду(с, ПОКАЗЫ, РЯДЫ):
        return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        for форма in ФОРМЫ:
            с = цель_многих_утв(язык, 0) if форма == "зачем_многих_утв" else цель_многих(язык, 0) if форма == "зачем_многих" else цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
            if с is None:
                continue
            # ПРОВЕРКА ИДЁТ ТЕМ ЖЕ ПУТЁМ, ЧТО И ДЕЛО (09.09). Показы мира проходят элизию
            # (`ПОКАЗЫ` строится через `_fr.элизия`), а самопроверка звала рамку НАПРЯМУЮ — и
            # французское «parce que une personne» падало у неё, живя в мире как «parce qu'une».
            #
            #     ПРОВЕРКА, ИДУЩАЯ ИНЫМ ПУТЁМ, ЧЕМ ДЕЛО, ПРОВЕРЯЕТ НЕ ДЕЛО. Дом был красен и
            #     молчал об этом, ибо самопроверки домов набор не гоняет.
            if язык == "fr":
                с = _fr.элизия(с)
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
            печать = цель_многих_утв(язык, 0) if форма == "зачем_многих_утв" else цель_многих(язык, 0) if форма == "зачем_многих" else цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
            if печать is None:
                continue
            print("  ", печать[:104])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, поводов {len(ПОВОДЫ)}, родов {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
