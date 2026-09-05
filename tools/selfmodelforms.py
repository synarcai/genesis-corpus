#!/usr/bin/env python3
"""THE HOUSE OF THE SELF-MODEL — predict yourself, then check by the fact (05.09).

Д-2 of the collegium's revision: the organism has a Γ-heart, a growth ledger and a
self-description, but no φ as an OPERATION — it does not PREDICT itself and check. The cure
named there is the φ-organ: predict before answering, check by the FACT, iterate. This house
is the corpus side of that organ, and it shows the whole cycle on one page:

    A PREDICTION, THEN THE ANSWER, THEN THE VERDICT ON THE PREDICTION. «there are 5 files in
    the folder. the first act creates 3 files. i think i will answer 8. how many files are in
    the folder? 8: 5 + 3 = 8. the prediction came true.» — and beside it the page where the
    prediction was wrong, which says so and names both numbers.

    THE SIZE OF THE ERROR IS A NUMBER, NOT A FEELING. «by how much was I wrong? by 1: 9 − 8 =
    1.» A self-model that cannot measure its own error cannot shrink it.

    THE ORGANISM PREDICTS ITS OWN SILENCE TOO. «there are files in the folder. how many is not
    said. i think i will not answer. how many files are in the folder? i do not know: how many
    files are in the folder is not said. the prediction came true.» Knowing that one will not
    know is the sharpest thing a self-model can get right, and the refusal is the pair house's
    own word of not-knowing, derived from it, never declared twice.

    AND THE GUARD STANDS ON THE PAGE ITSELF. «i thought 9, and the answer is 8. what is true?
    8: 5 + 3 = 8. my thought does not change the fact.» This is Campbell's shield written into
    the corpus: a self-estimate may be measured, it may be wrong, and it NEVER enters the
    court of truth. The judge enforces exactly that — the answer is recomputed from the
    ledger, and a page whose answer follows its prediction instead is a lie however
    beautifully the prediction was worded.

WHAT IS BORROWED: nine languages, the things and places and the copula from the house of the
tool, the act and the ledger from the house of the episode, the word of not-knowing from the
house of the pair (through the house of the order, which already derives it), the openers from
the house of the pair. Declared here: the words of predicting, of a prediction come true and
failed, the size of an error, the bare plural of a thing whose count is not said, and the
sentence of the guard.

WHAT IS NOT MEASURED, NAMED: whether the prediction was REASONABLE, whether the error shrinks
over time (that is the growth ledger's, not a page's), and any prediction about another actor
— this house is about the one who answers.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import episodeforms as E  # noqa: E402 — the act of a tape and its ledger
import opforms as O  # noqa: E402 — the pair house's word of not-knowing, already derived there
import svampforms as S  # noqa: E402 — the count cell of a pack
import toolforms as T  # noqa: E402 — things of acts, their places, the copula of a place

ЯЗЫКИ = T.ЯЗЫКИ
НАЧАЛА = (4, 5, 6, 7, 8, 9, 10, 12)
ШАГИ = (2, 3, 5, 6)
СДВИГИ = (1, 2)          # на сколько предсказание расходится с ответом

# ГОЛЫЙ МНОЖЕСТВЕННЫЙ ВЕЩИ — для истории, где число НЕ названо: «в папке есть файлы».
# Счётная форма («файлов») числа требует, а его-то и нет.
ПЛЮРАЛЬ = {
    "ru": ("файлы", "записи", "сообщения"), "en": ("files", "records", "messages"),
    "de": ("Dateien", "Einträge", "Nachrichten"), "fr": ("des fichiers", "des enregistrements", "des messages"),
    "es": ("archivos", "registros", "mensajes"), "it": ("file", "voci", "messaggi"),
    "pt": ("ficheiros", "registos", "mensagens"), "nl": ("bestanden", "records", "berichten"),
    "pl": ("pliki", "wpisy", "wiadomości"),
}
РЕЧЬ = {
    "ru": dict(думаю="я думаю, что отвечу {p}.", не_отвечу="я думаю, что не отвечу.",
               вопрос="сколько {Тмн} {М}?", вопрос_ошибка="на сколько я ошибся?",
               вопрос_верно="что верно?",
               сбылось="предсказание сбылось.",
               не_сбылось="предсказание не сбылось: я думал {p}, а ответ {v}.",
               ошибка="на {e}", думал="я думал {p}, а ответ {v}.",
               не_меняет="моя мысль факта не меняет",
               есть_вещи="{М} есть {ПЛ}.", не_сказано="сколько их, не сказано.",
               основание="сколько {Тмн} {М}, не сказано",
               двоеточие=": ", вопрос_знак="?"),
    "en": dict(думаю="i think i will answer {p}.", не_отвечу="i think i will not answer.",
               вопрос="how many {Тмн} are {М}?", вопрос_ошибка="by how much was i wrong?",
               вопрос_верно="what is true?",
               сбылось="the prediction came true.",
               не_сбылось="the prediction did not come true: i thought {p}, and the answer is {v}.",
               ошибка="by {e}", думал="i thought {p}, and the answer is {v}.",
               не_меняет="my thought does not change the fact",
               есть_вещи="there are {ПЛ} {М}.", не_сказано="how many is not said.",
               основание="how many {Тмн} are {М} is not said",
               двоеточие=": ", вопрос_знак="?"),
    "de": dict(думаю="ich denke, ich werde {p} antworten.", не_отвечу="ich denke, ich werde nicht antworten.",
               вопрос="wie viele {Тмн} sind {М}?", вопрос_ошибка="wie viel war mein Fehler?",
               вопрос_верно="was ist wahr?",
               сбылось="die Vorhersage traf zu.",
               не_сбылось="die Vorhersage traf nicht zu: ich dachte {p}, und die Antwort ist {v}.",
               ошибка="{e}", думал="ich dachte {p}, und die Antwort ist {v}.",
               не_меняет="mein Gedanke ändert die Tatsache nicht",
               есть_вещи="{М} sind {ПЛ}.", не_сказано="wie viele, ist nicht gesagt.",
               основание="wie viele {Тмн} {М} sind, ist nicht gesagt",
               двоеточие=": ", вопрос_знак="?"),
    "fr": dict(думаю="je pense que je répondrai {p}.", не_отвечу="je pense que je ne répondrai pas.",
               вопрос="combien de {Тмн} y a-t-il {М} ?", вопрос_ошибка="de combien me suis-je trompé ?",
               вопрос_верно="qu'est-ce qui est vrai ?",
               сбылось="la prédiction s'est réalisée.",
               не_сбылось="la prédiction ne s'est pas réalisée : je pensais {p}, et la réponse est {v}.",
               ошибка="de {e}", думал="je pensais {p}, et la réponse est {v}.",
               не_меняет="ma pensée ne change pas le fait",
               есть_вещи="il y a {ПЛ} {М}.", не_сказано="combien, ce n'est pas dit.",
               основание="combien de {Тмн} il y a {М} n'est pas dit",
               двоеточие=" : ", вопрос_знак=" ?"),
    "es": dict(думаю="creo que responderé {p}.", не_отвечу="creo que no responderé.",
               вопрос="¿cuántos {Тмн} hay {М}?", вопрос_ошибка="¿por cuánto me equivoqué?",
               вопрос_верно="¿qué es verdad?",
               сбылось="la predicción se cumplió.",
               не_сбылось="la predicción no se cumplió: pensaba {p}, y la respuesta es {v}.",
               ошибка="por {e}", думал="pensaba {p}, y la respuesta es {v}.",
               не_меняет="mi pensamiento no cambia el hecho",
               есть_вещи="hay {ПЛ} {М}.", не_сказано="cuántos, no se dice.",
               основание="no se dice cuántos {Тмн} hay {М}",
               двоеточие=": ", вопрос_знак="?"),
    "it": dict(думаю="penso che risponderò {p}.", не_отвечу="penso che non risponderò.",
               вопрос="quanti {Тмн} ci sono {М}?", вопрос_ошибка="quanto era il mio errore?",
               вопрос_верно="che cosa è vero?",
               сбылось="la previsione si è avverata.",
               не_сбылось="la previsione non si è avverata: pensavo {p}, e la risposta è {v}.",
               ошибка="{e}", думал="pensavo {p}, e la risposta è {v}.",
               не_меняет="il mio pensiero non cambia il fatto",
               есть_вещи="{М} ci sono {ПЛ}.", не_сказано="quanti, non è detto.",
               основание="non è detto quanti {Тмн} ci sono {М}",
               двоеточие=": ", вопрос_знак="?"),
    "pt": dict(думаю="penso que vou responder {p}.", не_отвечу="penso que não vou responder.",
               вопрос="quantos {Тмн} há {М}?", вопрос_ошибка="de quanto me enganei?",
               вопрос_верно="o que é verdade?",
               сбылось="a previsão realizou-se.",
               не_сбылось="a previsão não se realizou: eu pensava {p}, e a resposta é {v}.",
               ошибка="de {e}", думал="eu pensava {p}, e a resposta é {v}.",
               не_меняет="o meu pensamento não muda o facto",
               есть_вещи="há {ПЛ} {М}.", не_сказано="quantos, não é dito.",
               основание="não é dito quantos {Тмн} há {М}",
               двоеточие=": ", вопрос_знак="?"),
    "nl": dict(думаю="ik denk dat ik {p} zal antwoorden.", не_отвечу="ik denk dat ik niet zal antwoorden.",
               вопрос="hoeveel {Тмн} liggen {М}?", вопрос_ошибка="hoeveel was mijn fout?",
               вопрос_верно="wat is waar?",
               сбылось="de voorspelling kwam uit.",
               не_сбылось="de voorspelling kwam niet uit: ik dacht {p}, en het antwoord is {v}.",
               ошибка="{e}", думал="ik dacht {p}, en het antwoord is {v}.",
               не_меняет="mijn gedachte verandert het feit niet",
               есть_вещи="er liggen {ПЛ} {М}.", не_сказано="hoeveel, is niet gezegd.",
               основание="hoeveel {Тмн} {М} liggen, is niet gezegd",
               двоеточие=": ", вопрос_знак="?"),
    "pl": dict(думаю="myślę, że odpowiem {p}.", не_отвечу="myślę, że nie odpowiem.",
               вопрос="ile {Тмн} jest {М}?", вопрос_ошибка="o ile się pomyliłem?",
               вопрос_верно="co jest prawdą?",
               сбылось="przewidywanie się sprawdziło.",
               не_сбылось="przewidywanie się nie sprawdziło: myślałem {p}, a odpowiedź to {v}.",
               ошибка="o {e}", думал="myślałem {p}, a odpowiedź to {v}.",
               не_меняет="moja myśl nie zmienia faktu",
               есть_вещи="{М} są {ПЛ}.", не_сказано="ile, nie powiedziano.",
               основание="nie powiedziano, ile {Тмн} jest {М}",
               двоеточие=": ", вопрос_знак="?"),
}
ФОРМЫ = ("сбылось", "не_сбылось", "ошибка", "предсказал_незнание", "мысль_не_меняет_факт")


def _вещь(язык, Т, c):
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def _история(язык, М):
    """The tape: a place holds n things and one act adds m — the episode house's own words."""
    начало = E.РЕЧЬ[язык]["начало"].replace("{М}", М)
    шаг = (E.РЕЧЬ[язык]["шаг_плюс"].replace("{П}", E.ПОРЯДОК[язык][0])
           .replace("{m}", "{m1}").replace("{Тm}", "{Тm1}"))
    return начало + " " + шаг


def рамка(язык, форма, М, Т=0):
    р = РЕЧЬ[язык]
    вопрос = р["вопрос"].replace("{М}", М)
    состояние = E.РЕЧЬ[язык]["состояние"].replace("{М}", М)
    леджер = "{n} + {m1} = {v}"
    if форма == "предсказал_незнание":
        # ПРЕДСКАЗАННОЕ НЕЗНАНИЕ: голова отказа — дома пары, основание объявлено здесь
        история = р["есть_вещи"].replace("{М}", М).replace("{ПЛ}", "{ПЛ}") + " " + р["не_сказано"]
        ответ = (O.ГОЛОВА[язык] + р["двоеточие"] + р["основание"].replace("{М}", М) + ".")
        return (история + " " + р["не_отвечу"] + " " + вопрос + " " + ответ + " " + р["сбылось"])
    начало = _история(язык, М) + " " + р["думаю"]
    if форма == "сбылось":
        # ПРЕДСКАЗАНИЕ СОВПАЛО С ОТВЕТОМ: одна дыра на оба — разойтись они не могут
        ответ = состояние.replace("{v}", "{p}").replace("{Тv}", "{Тp}") + р["двоеточие"] + "{n} + {m1} = {p}."
        return начало.replace("{p}", "{p}") + " " + вопрос + " " + ответ + " " + р["сбылось"]
    if форма == "не_сбылось":
        ответ = состояние + р["двоеточие"] + леджер + "."
        return начало + " " + вопрос + " " + ответ + " " + р["не_сбылось"]
    if форма == "ошибка":
        # РАЗМЕР ОШИБКИ ЕСТЬ ЧИСЛО, И ОНО ПЕРЕСЧИТЫВАЕТСЯ
        ответ = состояние + р["двоеточие"] + леджер + "."
        хвост = р["ошибка"] + р["двоеточие"] + "{p} − {v} = {e}."
        return (начало + " " + вопрос + " " + ответ + " " + р["вопрос_ошибка"] + " " + хвост)
    # МЫСЛЬ ФАКТА НЕ МЕНЯЕТ — щит Кэмпбелла на самой странице
    ответ = состояние + р["двоеточие"] + леджер + "."
    return (_история(язык, М) + " " + р["думал"] + " " + р["вопрос_верно"] + " " + ответ
            + " " + р["не_меняет"] + ".")


def страница(язык, форма, Т, n=0, m=0, сдвиг=1, М=None):
    р = РЕЧЬ[язык]
    М = М if М is not None else T.МЕСТА[язык][Т % len(T.МЕСТА[язык])]
    if форма == "предсказал_незнание":
        поля = dict(ПЛ=ПЛЮРАЛЬ[язык][Т % len(ПЛЮРАЛЬ[язык])], Тмн=_вещь(язык, Т, 5))
        return рамка(язык, форма, М, Т).format(**поля)
    v = n + m
    p = v if форма == "сбылось" else v + сдвиг
    поля = dict(n=n, m1=m, v=v, p=p, e=abs(p - v), Тn=_вещь(язык, Т, n), Тm1=_вещь(язык, Т, m),
                Тv=_вещь(язык, Т, v), Тp=_вещь(язык, Т, p), Тмн=_вещь(язык, Т, 5))
    if язык in T.ЕСТЬ:
        поля["ЕСТЬn"] = T._есть(язык, n)
        поля["ЕСТЬv"] = T._есть(язык, p if форма == "сбылось" else v)
    return рамка(язык, форма, М, Т).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        мест = len(T.МЕСТА[язык])
        for i, n in enumerate(НАЧАЛА):
            for j, m in enumerate(ШАГИ):
                Т = (i + j) % видов
                М = T.МЕСТА[язык][(i + j) % мест]
                вон[страница(язык, "сбылось", Т, n, m, 0, М)] = (язык, "сбылось")
                for сдвиг in СДВИГИ:
                    вон[страница(язык, "не_сбылось", Т, n, m, сдвиг, М)] = (язык, "не_сбылось")
                    вон[страница(язык, "ошибка", Т, n, m, сдвиг, М)] = (язык, "ошибка")
                    вон[страница(язык, "мысль_не_меняет_факт", Т, n, m, сдвиг, М)] = (язык, "мысль_не_меняет_факт")
        for Т in range(видов):
            for М in T.МЕСТА[язык]:
                вон[страница(язык, "предсказал_незнание", Т, М=М)] = (язык, "предсказал_незнание")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    вещи = _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])
    есть = _альт(T.ЕСТЬ[язык]) if язык in T.ЕСТЬ else None
    дыры = {"n": r"\d+", "m1": r"\d+", "v": r"\d+", "p": r"\d+", "e": r"\d+",
            "Тn": вещи, "Тm1": вещи, "Тv": вещи, "Тp": вещи, "Тмн": вещи,
            "ПЛ": _альт(ПЛЮРАЛЬ[язык])}
    if есть:
        дыры["ЕСТЬn"] = есть
        дыры["ЕСТЬv"] = есть
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма, М)), язык, форма)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for М in T.МЕСТА[язык]]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(язык, форма, зн):
    if форма == "предсказал_незнание":
        # НИ ОДНОГО ЧИСЛА: предсказанное незнание и есть весь ответ
        return True
    n, m = int(зн["n"]), int(зн["m1"])
    if n < 1 or m < 1:
        return False
    v = int(зн.get("v", зн.get("p")))
    виды = None
    пары = [("Тn", n), ("Тm1", m)]
    if "v" in зн:
        пары.append(("Тv", int(зн["v"])))
    if "p" in зн:
        пары.append(("Тp", int(зн["p"])))
    for дыра, число in пары:
        if дыра not in зн:
            continue
        свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн[дыра], set())
                if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], число, язык) == зн[дыра]}
        if not свои:
            return False
        виды = свои if виды is None else виды & свои
        if not виды:
            return False
    if язык in T.ЕСТЬ:
        if "ЕСТЬn" in зн and зн["ЕСТЬn"] != T._есть(язык, n):
            return False
        if "ЕСТЬv" in зн and зн["ЕСТЬv"] != T._есть(язык, v):
            return False
    # ОТВЕТ ПЕРЕСЧИТЫВАЕТСЯ ИЗ ЛЕДЖЕРА, А НЕ ИЗ ПРЕДСКАЗАНИЯ (щит Кэмпбелла)
    if форма == "сбылось":
        return int(зн["p"]) == n + m
    if int(зн["v"]) != n + m:
        return False
    p = int(зн["p"])
    if форма == "не_сбылось":
        # «НЕ СБЫЛОСЬ» ОБЯЗАНО СТОЯТЬ НАД РАЗОШЕДШИМСЯ ПРЕДСКАЗАНИЕМ
        return p != int(зн["v"])
    if форма == "ошибка":
        # РАЗМЕР ОШИБКИ ПЕРЕСЧИТЫВАЕТСЯ ВЫЧИТАНИЕМ, И ОН НЕ НОЛЬ
        e = int(зн["e"])
        return e == p - int(зн["v"]) and e > 0
    # мысль_не_меняет_факт: ответ равен леджеру, а не мысли
    return p != int(зн["v"])


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose fact recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, зн)
    return False, False


def _хвост(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, n, m, М = 0, 5, 3, T.МЕСТА[язык][0]
        # (1) «СБЫЛОСЬ» НАД РАЗОШЕДШИМСЯ ПРЕДСКАЗАНИЕМ
        с = страница(язык, "сбылось", Т, n, m, 0, М)
        assert судить(с) == (True, True), с
        битая = с.replace("8", "9")
        assert судить(битая) == (True, False), битая
        # (2) «НЕ СБЫЛОСЬ» НАД СОВПАВШИМ
        нс = страница(язык, "не_сбылось", Т, n, m, 1, М)
        assert судить(нс) == (True, True), нс
        битая = нс.replace("9", "8")
        assert судить(битая) == (True, False), битая
        # (3) РАЗМЕР ОШИБКИ НЕ СХОДИТСЯ
        о = страница(язык, "ошибка", Т, n, m, 2, М)
        assert судить(о) == (True, True), о
        битая = о[:о.rindex("= ")] + "= 3."
        assert судить(битая) == (True, False), битая
        # (4) ОТВЕТ ПОШЁЛ ЗА ПРЕДСКАЗАНИЕМ, А НЕ ЗА ЛЕДЖЕРОМ — главная ложь этого дома
        м_ = страница(язык, "мысль_не_меняет_факт", Т, n, m, 1, М)
        assert судить(м_) == (True, True), м_
        хв = _хвост(м_)
        битая = м_[:хв] + м_[хв:].replace("8", "9")
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        н = страница(язык, "предсказал_незнание", Т, М=М)
        for стр in (с, нс, о, м_, н):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "сбылось", 0, 5, 3, 0, T.МЕСТА[язык][0]))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "не_сбылось", 0, 5, 3, 1, T.МЕСТА[язык][0]))
        print("  ", страница(язык, "ошибка", 0, 5, 3, 2, T.МЕСТА[язык][0]))
        print("  ", страница(язык, "мысль_не_меняет_факт", 0, 5, 3, 1, T.МЕСТА[язык][0]))
        print("  ", страница(язык, "предсказал_незнание", 0, М=T.МЕСТА[язык][0]))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
