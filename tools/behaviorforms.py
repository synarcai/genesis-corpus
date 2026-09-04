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

Три формы у каждого рода, и третья — главная:
  · ПРАВИЛО   «пётр устал. поэтому пётр ошибается чаще.»
  · ВОПРОС    «… почему пётр ошибается чаще? потому что пётр устал.»
  · ЗАКОН     «когда человек устал, он ошибается чаще.» — обобщение над
    случаями, тот самый акт, который манифест зовёт generalize.

ИМЕНА ЗДЕСЬ ОДНОГО РОДА, И ЭТО НАЗВАННЫЙ ДОЛГ, А НЕ НЕДОСМОТР. Клауза
причины несёт ПРИЛАГАТЕЛЬНОЕ («устал», «stanco», «cansado», «zmęczony»), и
оно согласуется с родом подлежащего в шести языках из девяти: «Anna è
stanco» верно счётом ролей и ложно речью. Вторая, женская форма клаузы
объявляется так же, как объявлена мужская, — и будет объявлена; до тех пор
дом берёт имена одного рода, ибо угадывать окончание он не вправе (тот же
закон, по которому дом страниц действия НЕ ПИШЕТ страницу, если падеж вещи
не объявлен).

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
        кратко="почему, когда {оп}, {ов}? потому что {оп}.",
        цели=(("человек спит", "чтобы отдохнуть"), ("человек ест", "чтобы не быть голодным"), ("человек учится", "чтобы уметь больше")), зачем_рамка="зачем {д}? {ц}.",
        закон="когда {оп}, {ос}.",
        закон_вопрос="когда {оп}, {ос}. почему {ов}? потому что {оп}.",
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
        кратко="why, when {оп}, {ов}? because {оп}.",
        цели=(("does a person sleep", "in order to rest"), ("does a person eat", "in order not to be hungry"), ("does a person study", "in order to be able to do more")), зачем_рамка="why {д}? {ц}.",
        закон="when {оп}, {ос}.",
        закон_вопрос="when {оп}, {ос}. why {ов}? because {оп}.",
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
        кратко="warum {ов}, wenn {оп}? weil {оп}.",
        цели=(("schläft ein Mensch", "um sich auszuruhen"), ("isst ein Mensch", "um nicht hungrig zu sein"), ("lernt ein Mensch", "um mehr zu können")), зачем_рамка="wozu {д}? {ц}.",
        закон="wenn {оп}, {ос}.",
        закон_вопрос="wenn {оп}, {ос}. warum {ов}? weil {оп}.",
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
        кратко="pourquoi, quand {оп}, {ов} ? parce que {оп}.",
        цели=(("une personne dort", "pour se reposer"), ("une personne mange", "pour ne pas avoir faim"), ("une personne apprend", "pour savoir faire plus")), зачем_рамка="pourquoi {д} ? {ц}.",
        закон="quand {оп}, {ос}.",
        закон_вопрос="quand {оп}, {ос}. pourquoi {ов} ? parce que {оп}.",
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
        кратко="¿por qué, cuando {оп}, {ов}? porque {оп}.",
        цели=(("una persona duerme", "para descansar"), ("una persona come", "para no tener hambre"), ("una persona estudia", "para saber hacer más")), зачем_рамка="¿por qué {д}? {ц}.",
        закон="cuando {оп}, {ос}.",
        закон_вопрос="cuando {оп}, {ос}. ¿por qué {ов}? porque {оп}.",
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
        кратко="perché, quando {оп}, {ов}? perché {оп}.",
        цели=(("una persona dorme", "per riposare"), ("una persona mangia", "per non avere fame"), ("una persona studia", "per saper fare di più")), зачем_рамка="perché {д}? {ц}.",
        закон="quando {оп}, {ос}.",
        закон_вопрос="quando {оп}, {ос}. perché {ов}? perché {оп}.",
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
        кратко="porque é que, quando {оп}, {ов}? porque {оп}.",
        цели=(("uma pessoa dorme", "para descansar"), ("uma pessoa come", "para não ter fome"), ("uma pessoa estuda", "para saber fazer mais")), зачем_рамка="porque é que {д}? {ц}.",
        закон="quando {оп}, {ос}.",
        закон_вопрос="quando {оп}, {ос}. porque é que {ов}? porque {оп}.",
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
        кратко="waarom {ов} als {оп}? omdat {оп}.",
        цели=(("slaapt een mens", "om uit te rusten"), ("eet een mens", "om geen honger te hebben"), ("leert een mens", "om meer te kunnen")), зачем_рамка="waarom {д}? {ц}.",
        закон="als {оп}, {ос}.",
        закон_вопрос="als {оп}, {ос}. waarom {ов}? omdat {оп}.",
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
        кратко="dlaczego, kiedy {оп}, {ов}? ponieważ {оп}.",
        цели=(("człowiek śpi", "żeby odpocząć"), ("człowiek je", "żeby nie być głodnym"), ("człowiek się uczy", "żeby umieć więcej")), зачем_рамка="dlaczego {д}? {ц}.",
        закон="kiedy {оп}, {ос}.",
        закон_вопрос="kiedy {оп}, {ос}. dlaczego {ов}? ponieważ {оп}.",
    ),
}
ФОРМЫ = ("правило", "вопрос", "закон", "закон_вопрос", "кратко", "зачем")

for _яз, _я in ЯЗЫКИ.items():
    assert len(_я["пары"]) == len(РОДЫ), (_яз, len(_я["пары"]))
    assert len(_я["имена"]) >= 4, _яз
    for _п in _я["пары"]:
        assert len(_п) == 5, (_яз, _п)
    assert "вопр_след" not in _я or len(_я["вопр_след"]) == len(РОДЫ), _яз
    assert "общ_вопрос" not in _я or len(_я["общ_вопрос"]) == len(РОДЫ), _яз


def страница(язык, форма, род, i=0):
    я = ЯЗЫКИ[язык]
    причина, следствие, придаточная, общ_п, общ_с = я["пары"][род]
    if форма == "закон":
        return я["закон"].format(оп=общ_п, ос=общ_с)
    if форма == "кратко":
        # ВОПРОС ОДНИМ ПРЕДЛОЖЕНИЕМ, БЕЗ ПРЕДШЕСТВУЮЩЕГО ЗАКОНА: так спрашивает
        # человек («почему человек ошибается, когда устал?»), и до этой формы
        # весь род требовал, чтобы закон стоял перед вопросом.
        общ_в = (я.get("общ_вопрос") or ())
        return я["кратко"].format(оп=общ_п, ос=общ_с, ов=(общ_в[род] if общ_в else общ_с))
    if форма == "закон_вопрос":
        # ВОПРОС НАД ОБОБЩЕНИЕМ: человек спрашивает о ЧЕЛОВЕКЕ, а не об имени
        # («почему человек ошибается, когда устал?»), и до этой формы весь род
        # отвечал только про названного Петра. Ответ — та же причина, что и в
        # частном случае: закон и его случай говорят одно.
        общ_в = (я.get("общ_вопрос") or ())
        return я["закон_вопрос"].format(оп=общ_п, ос=общ_с, ов=(общ_в[род] if общ_в else общ_с))
    X = я["имена"][i % len(я["имена"])]
    вопр = (я.get("вопр_след") or ())
    поля = dict(п=причина.format(X=X), с=следствие.format(X=X), пп=придаточная.format(X=X),
                в=(вопр[род] if вопр else следствие).format(X=X))
    return я[форма].format(**поля)


def цель(язык, i):
    """«зачем человек спит? чтобы отдохнуть.» — цель поступка, объявленная парой."""
    я = ЯЗЫКИ[язык]
    д, ц = я["цели"][i % len(я["цели"])]
    return я["зачем_рамка"].format(д=д, ц=ц)


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for род in РОДЫ:
            вон[страница(язык, "закон", род)] = (язык, "закон")
            вон[страница(язык, "закон_вопрос", род)] = (язык, "закон_вопрос")
            вон[страница(язык, "кратко", род)] = (язык, "кратко")
            for i in range(len(я["имена"])):
                for форма in ("правило", "вопрос"):
                    вон[страница(язык, форма, род, i)] = (язык, форма)
        for i in range(len(я["цели"])):
            вон[цель(язык, i)] = (язык, "зачем")
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
            с = цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
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
            печать = цель(язык, 0) if форма == "зачем" else страница(язык, форма, УСТАЛОСТЬ)
            print("  ", печать[:104])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
