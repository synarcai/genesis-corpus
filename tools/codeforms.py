#!/usr/bin/env python3
"""ДОМ КОДА — свои малые программы на Python и Rust с поведением (25.09, наряд ведущего по слову владельца: свод —
школа продукта ozar; п. 2 «код как корпус», металингвистика 03.09 — грамматику свод покупает из показов).

Свод говорил о программах лишь псевдокодом («если x > 4 то y = 1», `prog`; «sum for i from 1 to 4 is 10»,
`programs`; «function add(a, b) return a + b», `eng_proof`) и ни разу не показал НАСТОЯЩЕГО кода с его
поведением: определение, вызов и что он возвращает; тест, который проходит, и тест, который падает, — с
причиной и правкой; разбор функции по частям; одна и та же функция на двух языках. Продукту, который пишет и
чинит код, это — первая грамматика.

ДВЕНАДЦАТЬ СВОИХ ПРОГРАММ, КАЖДАЯ В ДВУХ ЗАПИСЯХ: Python в одну строку («def add(a, b): return a + b») и Rust
(«fn add(a: i32, b: i32) -> i32 { a + b }»), с тремя вызовами и одной ошибкой, какую делают руками (вычитание
вместо сложения, `x * 2` вместо `x * x`, перевёрнутое сравнение, забытые скобки у `a + b // 2`). Код один на
всех языках, рассказ — на девяти: «`add(2, 3)` returns 5», «`add(2, 3)` возвращает 5», «`add(2, 3)` gibt 5 zurück».
Публичных наборов (HumanEval, MBPP, SWE) здесь нет — ни текста, ни строя задач: программы свои.

    ВСЯКИЙ РЕЗУЛЬТАТ — ИНТЕРПРЕТАТОРА: генератор ИСПОЛНЯЕТ код, чтобы узнать, что вернёт вызов и упадёт ли
    тест, а суд исполняет его снова своей рукой — Python в огороженном пространстве имён, Rust переводом малого
    подмножества (арифметика, сравнение, `if … { } else { }`), — и страница, где сказано не то, что вышло, ложна.

ШЕСТЬ РОДОВ НА ДВУХ ЯЗЫКАХ КОДА: вызов и результат; вопрос о результате и ответ; тест, который проходит, и
почему; тест, который падает, — почему (что вернул вызов вместо ожидаемого) и правка (после неё вызов
возвращает ожидаемое, и тест проходит); разбор функции (имя, сколько параметров и какие, что возвращает);
перевод той же функции с Python на Rust.

ГРАНИЦА, НАЗВАННАЯ: целые без знака в аргументах (целое деление Rust к нулю и Python вниз совпадают лишь на
неотрицательных), тела в одно выражение, без строк, списков и циклов — это следующий шаг дома, не этот.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import frgram  # noqa: E402 — французская элизия после подстановки
import svampforms as S  # noqa: E402 — счётная ячейка пакета
from actturn import ЯЗЫКИ  # noqa: E402 — девять языков атаки

# ======================================================================================================
# ПРОГРАММЫ: имя, параметры, тело Python, тело Rust, тип результата, три вызова, ошибка (Python, Rust), вызов теста
# ======================================================================================================
ПРОГРАММЫ = (
    ("add", ("a", "b"), "a + b", "a + b", "i32", ((2, 3), (7, 5), (10, 4)), ("a - b", "a - b"), (2, 3)),
    ("sub", ("a", "b"), "a - b", "a - b", "i32", ((9, 4), (12, 5), (20, 8)), ("b - a", "b - a"), (9, 4)),
    ("double", ("x",), "x * 2", "x * 2", "i32", ((4,), (7,), (15,)), ("x + 2", "x + 2"), (4,)),
    ("square", ("x",), "x * x", "x * x", "i32", ((3,), (6,), (9,)), ("x * 2", "x * 2"), (3,)),
    ("maximum", ("a", "b"), "a if a > b else b", "if a > b { a } else { b }", "i32", ((3, 8), (9, 2), (5, 5)),
     ("a if a < b else b", "if a < b { a } else { b }"), (3, 8)),
    ("minimum", ("a", "b"), "a if a < b else b", "if a < b { a } else { b }", "i32", ((4, 9), (8, 1), (6, 6)),
     ("a if a > b else b", "if a > b { a } else { b }"), (4, 9)),
    ("is_even", ("n",), "n % 2 == 0", "n % 2 == 0", "bool", ((4,), (7,), (10,)), ("n % 2 == 1", "n % 2 == 1"), (4,)),
    ("is_positive", ("n",), "n > 0", "n > 0", "bool", ((5,), (0,), (12,)), ("n >= 0", "n >= 0"), (0,)),
    ("area", ("w", "h"), "w * h", "w * h", "i32", ((3, 4), (5, 6), (7, 2)), ("w + h", "w + h"), (3, 4)),
    ("perimeter", ("w", "h"), "2 * (w + h)", "2 * (w + h)", "i32", ((3, 4), (5, 6), (7, 2)),
     ("2 * w + h", "2 * w + h"), (3, 4)),
    ("last_digit", ("n",), "n % 10", "n % 10", "i32", ((47,), (128,), (305,)), ("n // 10", "n / 10"), (47,)),
    ("middle", ("a", "b"), "(a + b) // 2", "(a + b) / 2", "i32", ((4, 10), (7, 13), (20, 30)),
     ("a + b // 2", "a + b / 2"), (4, 10)),
)
ЯЗЫКИ_КОДА = ("python", "rust")


def определение(код, имя, парам, тело, тип_):
    if код == "python":
        return f"def {имя}({', '.join(парам)}): return {тело}"
    return f"fn {имя}({', '.join(p + ': i32' for p in парам)}) -> {тип_} {{ {тело} }}"


def вызов(имя, аргументы):
    return f"{имя}({', '.join(str(a) for a in аргументы)})"


def значение(код, v):
    """Результат литералом своего языка: True у Python, true у Rust."""
    if isinstance(v, bool):
        return ("True" if v else "False") if код == "python" else ("true" if v else "false")
    return str(v)


def тест(код, выз, ожидаемое):
    return f"assert {выз} == {ожидаемое}" if код == "python" else f"assert_eq!({выз}, {ожидаемое})"


def правка(код, тело):
    return f"return {тело}" if код == "python" else f"{{ {тело} }}"


def исполнить(имя, парам, тело_py, аргументы):
    """Что вернёт вызов — исполнением одной строки Python в пустом пространстве имён (генератор узнаёт, не пишет)."""
    пространство = {}
    exec(f"def {имя}({', '.join(парам)}): return {тело_py}", {"__builtins__": {}}, пространство)  # noqa: S102
    return пространство[имя](*аргументы)


# ======================================================================================================
# РЕЧЬ
# ======================================================================================================
ПАРАМЕТР = {"en": ("parameter", "parameters"), "ru": ("параметр", "параметра", "параметров"),
            "de": ("Parameter", "Parameter"), "fr": ("paramètre", "paramètres"), "es": ("parámetro", "parámetros"),
            "it": ("parametro", "parametri"), "pt": ("parâmetro", "parâmetros"), "nl": ("parameter", "parameters"),
            "pl": ("parametr", "parametry", "parametrów")}
РЕЧЬ = {
    "en": dict(возвращает="{call} returns {v}", вопрос="what does {call} return?",
               проходит="the test {test} passes because {call} returns {v}",
               падает="the test {test} fails because {call} returns {actual}, not {expected}",
               правка="the fix: {fix}; then {call} returns {expected} and the test passes",
               разбор="{code} — the function {name} takes {n}: {params}, and returns {expr}", и="and",
               перевод="{py} is written in Rust as {rs}"),
    "ru": dict(возвращает="{call} возвращает {v}", вопрос="что возвращает {call}?",
               проходит="тест {test} проходит, потому что {call} возвращает {v}",
               падает="тест {test} падает, потому что {call} возвращает {actual}, а не {expected}",
               правка="правка: {fix}; тогда {call} возвращает {expected}, и тест проходит",
               разбор="{code} — функция {name} принимает {n}: {params}, и возвращает {expr}", и="и",
               перевод="{py} на Rust пишется так: {rs}"),
    "de": dict(возвращает="{call} gibt {v} zurück", вопрос="was gibt {call} zurück?",
               проходит="der Test {test} besteht, weil {call} {v} zurückgibt",
               падает="der Test {test} schlägt fehl, weil {call} {actual} statt {expected} zurückgibt",
               правка="die Korrektur: {fix}; dann gibt {call} {expected} zurück, und der Test besteht",
               разбор="{code} — die Funktion {name} nimmt {n}: {params}, und gibt {expr} zurück", и="und",
               перевод="{py} lautet in Rust {rs}"),
    "fr": dict(возвращает="{call} renvoie {v}", вопрос="que renvoie {call} ?",
               проходит="le test {test} réussit parce que {call} renvoie {v}",
               падает="le test {test} échoue parce que {call} renvoie {actual} et non {expected}",
               правка="la correction : {fix} ; alors {call} renvoie {expected} et le test réussit",
               разбор="{code} — la fonction {name} prend {n} : {params}, et renvoie {expr}", и="et",
               перевод="{py} s'écrit en Rust ainsi : {rs}"),
    "es": dict(возвращает="{call} devuelve {v}", вопрос="¿qué devuelve {call}?",
               проходит="la prueba {test} pasa porque {call} devuelve {v}",
               падает="la prueba {test} falla porque {call} devuelve {actual} y no {expected}",
               правка="la corrección: {fix}; entonces {call} devuelve {expected} y la prueba pasa",
               разбор="{code} — la función {name} recibe {n}: {params}, y devuelve {expr}", и="y",
               перевод="{py} se escribe en Rust así: {rs}"),
    "it": dict(возвращает="{call} restituisce {v}", вопрос="cosa restituisce {call}?",
               проходит="il test {test} passa perché {call} restituisce {v}",
               падает="il test {test} fallisce perché {call} restituisce {actual} e non {expected}",
               правка="la correzione: {fix}; allora {call} restituisce {expected} e il test passa",
               разбор="{code} — la funzione {name} riceve {n}: {params}, e restituisce {expr}", и="e",
               перевод="{py} in Rust si scrive così: {rs}"),
    "pt": dict(возвращает="{call} devolve {v}", вопрос="o que devolve {call}?",
               проходит="o teste {test} passa porque {call} devolve {v}",
               падает="o teste {test} falha porque {call} devolve {actual} e não {expected}",
               правка="a correção: {fix}; então {call} devolve {expected} e o teste passa",
               разбор="{code} — a função {name} recebe {n}: {params}, e devolve {expr}", и="e",
               перевод="{py} escreve-se em Rust assim: {rs}"),
    "nl": dict(возвращает="{call} geeft {v} terug", вопрос="wat geeft {call} terug?",
               проходит="de test {test} slaagt omdat {call} {v} teruggeeft",
               падает="de test {test} faalt omdat {call} {actual} teruggeeft in plaats van {expected}",
               правка="de correctie: {fix}; dan geeft {call} {expected} terug en slaagt de test",
               разбор="{code} — de functie {name} neemt {n}: {params}, en geeft {expr} terug", и="en",
               перевод="{py} schrijf je in Rust als {rs}"),
    "pl": dict(возвращает="{call} zwraca {v}", вопрос="co zwraca {call}?",
               проходит="test {test} przechodzi, bo {call} zwraca {v}",
               падает="test {test} nie przechodzi, bo {call} zwraca {actual}, a nie {expected}",
               правка="poprawka: {fix}; wtedy {call} zwraca {expected} i test przechodzi",
               разбор="{code} — funkcja {name} przyjmuje {n}: {params}, i zwraca {expr}", и="i",
               перевод="{py} w Ruście zapisuje się tak: {rs}"),
}

ВЫЗОВ = "вызов и результат"
ВОПРОС = "вопрос о результате вызова"
ПРОХОДИТ = "тест проходит — почему"
ПАДАЕТ = "тест падает — почему и правка"
РАЗБОР = "разбор функции по частям"
ПЕРЕВОД = "та же функция на Rust"
РОДЫ = (ВЫЗОВ, ВОПРОС, ПРОХОДИТ, ПАДАЕТ, РАЗБОР, ПЕРЕВОД)


def к(текст):
    """Код в обратных кавычках — как пишет его помощник в беседе."""
    return f"`{текст}`"


def _фр(язык, строка):
    return frgram.элизия(строка) if язык == "fr" else строка


def параметров(язык, n):
    return f"{n} {S._счёт(ПАРАМЕТР[язык], n, язык)}"


def список(язык, парам):
    return парам[0] if len(парам) == 1 else f"{', '.join(парам[:-1])} {РЕЧЬ[язык]['и']} {парам[-1]}"


# СБОРКА — части приходят готовыми строками; суд подаёт в неё метки и получает рамку дома
def сборка(язык, род, code, call="", v="", test="", actual="", expected="", fix="", name="", n="", params="", expr="",
           rs=""):
    р = РЕЧЬ[язык]
    if род == ВЫЗОВ:
        текст = f"{к(code)}. " + р["возвращает"].format(call=к(call), v=v) + "."
    elif род == ВОПРОС:
        # ОТВЕТ — ПРЕДЛОЖЕНИЕМ, ЭХОМ ВОПРОСА (М-2009: рынок рамок вопроса покупает форму ПЕРВОГО предложения ответа
        # по скелету вопроса — носитель эхом, значение дырой; голое «5.» формы не несёт)
        текст = (f"{к(code)}. " + р["вопрос"].format(call=к(call)) + " "
                 + р["возвращает"].format(call=к(call), v=v) + ".")
    elif род == ПРОХОДИТ:
        текст = f"{к(code)}. " + р["проходит"].format(test=к(test), call=к(call), v=v) + "."
    elif род == ПАДАЕТ:
        текст = (f"{к(code)}. " + р["падает"].format(test=к(test), call=к(call), actual=actual, expected=expected)
                 + ". " + р["правка"].format(fix=к(fix), call=к(call), expected=expected) + ".")
    elif род == РАЗБОР:
        текст = р["разбор"].format(code=к(code), name=name, n=n, params=params, expr=к(expr)) + "."
    else:
        текст = р["перевод"].format(py=к(code), rs=к(rs)) + "."
    return _фр(язык, текст)


# ======================================================================================================
# ПОКАЗЫ — генератор узнаёт результаты исполнением
# ======================================================================================================
def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for имя, парам, тело_py, тело_rs, тип_, вызовы, ошибка, выз_теста in ПРОГРАММЫ:
            тела = {"python": тело_py, "rust": тело_rs}
            for код in ЯЗЫКИ_КОДА:
                опр = определение(код, имя, парам, тела[код], тип_)
                for арг in вызовы:
                    v = значение(код, исполнить(имя, парам, тело_py, арг))
                    for род in (ВЫЗОВ, ВОПРОС):
                        вон.setdefault(сборка(язык, род, опр, call=вызов(имя, арг), v=v), (язык, род, код))
                выз = вызов(имя, выз_теста)
                ожидаемое = значение(код, исполнить(имя, парам, тело_py, выз_теста))
                вон.setdefault(сборка(язык, ПРОХОДИТ, опр, call=выз, v=ожидаемое, test=тест(код, выз, ожидаемое)),
                               (язык, ПРОХОДИТ, код))
                ошибочное = определение(код, имя, парам, ошибка[0 if код == "python" else 1], тип_)
                вышло = значение(код, исполнить(имя, парам, ошибка[0], выз_теста))
                вон.setdefault(сборка(язык, ПАДАЕТ, ошибочное, call=выз, test=тест(код, выз, ожидаемое), actual=вышло,
                                      expected=ожидаемое, fix=правка(код, тела[код])), (язык, ПАДАЕТ, код))
                вон.setdefault(сборка(язык, РАЗБОР, опр, name=имя, n=параметров(язык, len(парам)),
                                      params=список(язык, парам), expr=тела[код]), (язык, РАЗБОР, код))
            вон.setdefault(сборка(язык, ПЕРЕВОД, определение("python", имя, парам, тело_py, тип_),
                                  rs=определение("rust", имя, парам, тело_rs, тип_)), (язык, ПЕРЕВОД, "python"))
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_мира():
    """Ошибка программы обязана ронять свой тест: иначе страница «тест падает» лгала бы о коде."""
    for имя, парам, тело_py, _rs, _т, вызовы, ошибка, выз_теста in ПРОГРАММЫ:
        assert исполнить(имя, парам, тело_py, выз_теста) != исполнить(имя, парам, ошибка[0], выз_теста), имя
        assert all(a >= 0 for арг in вызовы + (выз_теста,) for a in арг), имя


_самопроверка_мира()


def _самопроверка():
    import asking  # noqa: PLC0415 — зачины вопросов у дома пары
    по_роду = {}
    for стр, (язык, род, _код) in ПОКАЗЫ.items():
        по_роду.setdefault(род, set()).add(язык)
        if род == ВОПРОС:
            вопрос = стр[стр.index("`. ") + 3:стр.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    пустые = [р for р in РОДЫ if по_роду.get(р) != set(ЯЗЫКИ)]
    assert not пустые, f"род не кован на всех языках: {пустые}"
    for язык in ("en", "ru", "de"):
        for род in (ПАДАЕТ, РАЗБОР):
            print("  ", next(с for с, (я, р, код) in ПОКАЗЫ.items() if я == язык and р == род and код == "rust"))
    сч = {р: sum(1 for _я, род, _к in ПОКАЗЫ.values() if род == р) for р in РОДЫ}
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, программ {len(ПРОГРАММЫ)}): "
          + ", ".join(f"{р} {n}" for р, n in сч.items()))


if __name__ == "__main__":
    _самопроверка()
