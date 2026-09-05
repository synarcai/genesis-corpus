#!/usr/bin/env python3
"""THE HOUSE OF THE NUMBER LINE — the simplest questions a person checks a
speaker with, in nine languages: the neighbour of a number, which of two is
bigger, counting up and down, even or odd.

Born from the third band of conversation (BESEDA-3, 05.09): all four genera
were mute in all nine languages — the corpus compared horses with dogs and
proved parity in English derivations, but nobody had asked it «what number
comes after 9?». Every answer here is RECOMPUTED by the court from the
integers of the question, and every answer carries its ground: the bigger
number by the difference («9 − 7 = 2»), parity by the division («7 = 2 × 3 + 1»),
the neighbour and the row by the line itself. Generator and court read one
table; the world is CLOSED — a line of it that no frame reads is a lie.

    python3 tools/numberline.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# per language: the question and the answer of every form; {n} the number,
# {m} its neighbour, {a}/{b} the two of the question, {c}/{d} the bigger/smaller,
# {r} their difference, {h} the half, {ряд} the row «1, 2, 3»
ЯЗЫКИ = {
    "ru": dict(
        между=("назови число между {a} и {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("какое число стоит между {a} и {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("повтори числа: {ряд}.", "{ряд}."),
        повтори_воп=("я назвал числа: {ряд}. какие числа я назвал?", "{ряд}."),
        шагом=("считай двойками до {b}.", "{ряд}."),
        ряд_дальше=("продолжи ряд: {a}, {b}, {c}, ?", "{d}: шаг {ш}."),
        наибольшее=("какое число самое большое: {a}, {b} или {c}?", "{m}."),
        наименьшее=("какое число самое маленькое: {a}, {b} или {c}?", "{m}."),
        вдвое=("сколько будет вдвое больше {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. какое число пропущено?", "{k}: {s} − {a} = {k}."),
        больше_ли=("{c} больше {d}?", "да: {c} − {d} = {r}."),
        больше_ли_нет=("{d} больше {c}?", "нет, {d} меньше {c}: {c} − {d} = {r}."),
        на_сколько=("на сколько {c} больше {d}?", "на {r}: {c} − {d} = {r}."),
        словом=("как пишется число {n} словом?", "{N}."),
        половина=("сколько будет половина от {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("мне {a} {Га}. сколько мне будет через {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("какое число идёт после {n}?", "после {n} идёт {m}."),
        перед=("какое число идёт перед {n}?", "перед {n} идёт {m}."),
        больше=("что больше: {a} или {b}?", "{c} больше: {c} − {d} = {r}."),
        меньше=("что меньше: {a} или {b}?", "{d} меньше: {c} − {d} = {r}."),
        счёт=("сосчитай от {a} до {b}.", "{ряд}."),
        обратно=("сосчитай обратно от {b} до {a}.", "{ряд}."),
        чёт=("{n} — чётное или нечётное число?", "чётное: {n} = 2 × {h}.", "нечётное: {n} = 2 × {h} + 1."),
    ),
    "en": dict(
        между=("name a number between {a} and {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("what number lies between {a} and {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("repeat the numbers: {ряд}.", "{ряд}."),
        повтори_воп=("i said the numbers: {ряд}. what numbers did i say?", "{ряд}."),
        шагом=("count by twos up to {b}.", "{ряд}."),
        ряд_дальше=("continue the sequence: {a}, {b}, {c}, ?", "{d}: the step is {ш}."),
        наибольшее=("which number is the greatest: {a}, {b} or {c}?", "{m}."),
        наименьшее=("which number is the smallest: {a}, {b} or {c}?", "{m}."),
        вдвое=("what is twice {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. what number is missing?", "{k}: {s} − {a} = {k}."),
        больше_ли=("is {c} bigger than {d}?", "yes: {c} − {d} = {r}."),
        больше_ли_нет=("is {d} bigger than {c}?", "no, {d} is smaller than {c}: {c} − {d} = {r}."),
        на_сколько=("how much more is {c} than {d}?", "{r} more: {c} − {d} = {r}."),
        словом=("how do you write the number {n} in words?", "{N}."),
        # the share court owns «half of X is Y» — the answer is written in its frame
        половина=("what is half of {n}?", "half of {n} is {h}: {n} ÷ 2 = {h}."),
        возраст=("i am {a} {Га} old. how old will i be in {k} {Гk}?", "{s} {Гs} old: {a} + {k} = {s}."),
        после=("what number comes after {n}?", "after {n} comes {m}."),
        перед=("what number comes before {n}?", "before {n} comes {m}."),
        больше=("which is bigger: {a} or {b}?", "{c} is bigger: {c} − {d} = {r}."),
        меньше=("which is smaller: {a} or {b}?", "{d} is smaller: {c} − {d} = {r}."),
        счёт=("count from {a} to {b}.", "{ряд}."),
        обратно=("count down from {b} to {a}.", "{ряд}."),
        чёт=("is {n} an even or an odd number?", "even: {n} = 2 × {h}.", "odd: {n} = 2 × {h} + 1."),
    ),
    "de": dict(
        между=("nenne eine Zahl zwischen {a} und {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("welche Zahl liegt zwischen {a} und {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("wiederhole die Zahlen: {ряд}.", "{ряд}."),
        повтори_воп=("ich habe die Zahlen genannt: {ряд}. welche Zahlen habe ich genannt?", "{ряд}."),
        шагом=("zähle in Zweierschritten bis {b}.", "{ряд}."),
        ряд_дальше=("setze die Folge fort: {a}, {b}, {c}, ?", "{d}: der Schritt ist {ш}."),
        наибольшее=("welche Zahl ist die größte: {a}, {b} oder {c}?", "{m}."),
        наименьшее=("welche Zahl ist die kleinste: {a}, {b} oder {c}?", "{m}."),
        вдвое=("was ist das Doppelte von {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. welche Zahl fehlt?", "{k}: {s} − {a} = {k}."),
        больше_ли=("ist {c} größer als {d}?", "ja: {c} − {d} = {r}."),
        больше_ли_нет=("ist {d} größer als {c}?", "nein, {d} ist kleiner als {c}: {c} − {d} = {r}."),
        на_сколько=("um wie viel ist {c} größer als {d}?", "um {r}: {c} − {d} = {r}."),
        словом=("wie schreibt man die Zahl {n} in Worten?", "{N}."),
        половина=("was ist die Hälfte von {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ich bin {a} {Га} alt. wie alt werde ich in {k} {Гk} sein?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("welche Zahl kommt nach {n}?", "nach {n} kommt {m}."),
        перед=("welche Zahl kommt vor {n}?", "vor {n} kommt {m}."),
        больше=("was ist größer: {a} oder {b}?", "{c} ist größer: {c} − {d} = {r}."),
        меньше=("was ist kleiner: {a} oder {b}?", "{d} ist kleiner: {c} − {d} = {r}."),
        счёт=("zähle von {a} bis {b}.", "{ряд}."),
        обратно=("zähle rückwärts von {b} bis {a}.", "{ряд}."),
        чёт=("ist {n} eine gerade oder eine ungerade Zahl?", "gerade: {n} = 2 × {h}.", "ungerade: {n} = 2 × {h} + 1."),
    ),
    "fr": dict(
        между=("nomme un nombre entre {a} et {c}.", "{b} : {a} < {b} < {c}."),
        между_воп=("quel nombre se trouve entre {a} et {c} ?", "{b} : {a} < {b} < {c}."),
        повтори=("répète les nombres : {ряд}.", "{ряд}."),
        повтори_воп=("j'ai dit les nombres : {ряд}. quels nombres ai-je dits ?", "{ряд}."),
        шагом=("compte de deux en deux jusqu'à {b}.", "{ряд}."),
        ряд_дальше=("continue la suite : {a}, {b}, {c}, ?", "{d} : le pas est {ш}."),
        наибольшее=("quel est le plus grand nombre : {a}, {b} ou {c} ?", "{m}."),
        наименьшее=("quel est le plus petit nombre : {a}, {b} ou {c} ?", "{m}."),
        вдвое=("combien fait le double de {n} ?", "{d} : {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. quel nombre manque ?", "{k} : {s} − {a} = {k}."),
        больше_ли=("{c} est-il plus grand que {d} ?", "oui : {c} − {d} = {r}."),
        больше_ли_нет=("{d} est-il plus grand que {c} ?", "non, {d} est plus petit que {c} : {c} − {d} = {r}."),
        на_сколько=("de combien {c} est-il plus grand que {d} ?", "de {r} : {c} − {d} = {r}."),
        словом=("comment écrit-on le nombre {n} en lettres ?", "{N}."),
        половина=("combien fait la moitié de {n} ?", "{h} : {n} ÷ 2 = {h}."),
        возраст=("j'ai {a} {Га}. quel âge aurai-je dans {k} {Гk} ?", "{s} {Гs} : {a} + {k} = {s}."),
        после=("quel nombre vient après {n} ?", "après {n} vient {m}."),
        перед=("quel nombre vient avant {n} ?", "avant {n} vient {m}."),
        больше=("lequel est le plus grand : {a} ou {b} ?", "{c} est le plus grand : {c} − {d} = {r}."),
        меньше=("lequel est le plus petit : {a} ou {b} ?", "{d} est le plus petit : {c} − {d} = {r}."),
        счёт=("compte de {a} à {b}.", "{ряд}."),
        обратно=("compte à rebours de {b} à {a}.", "{ряд}."),
        чёт=("{n} est-il un nombre pair ou impair ?", "pair : {n} = 2 × {h}.", "impair : {n} = 2 × {h} + 1."),
    ),
    "es": dict(
        между=("di un número entre {a} y {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("¿qué número está entre {a} y {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("repite los números: {ряд}.", "{ряд}."),
        повтори_воп=("he dicho los números: {ряд}. ¿qué números he dicho?", "{ряд}."),
        шагом=("cuenta de dos en dos hasta {b}.", "{ряд}."),
        ряд_дальше=("continúa la serie: {a}, {b}, {c}, ?", "{d}: el paso es {ш}."),
        наибольшее=("¿cuál es el número más grande: {a}, {b} o {c}?", "{m}."),
        наименьшее=("¿cuál es el número más pequeño: {a}, {b} o {c}?", "{m}."),
        вдвое=("¿cuánto es el doble de {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. ¿qué número falta?", "{k}: {s} − {a} = {k}."),
        больше_ли=("¿{c} es mayor que {d}?", "sí: {c} − {d} = {r}."),
        больше_ли_нет=("¿{d} es mayor que {c}?", "no, {d} es menor que {c}: {c} − {d} = {r}."),
        # «{r} más» читалось бы судом арифметики как «{r} +» — «más» есть знак пакета; «en {r}» им не является
        на_сколько=("¿cuánto mayor es {c} que {d}?", "en {r}: {c} − {d} = {r}."),
        словом=("¿cómo se escribe el número {n} en letras?", "{N}."),
        половина=("¿cuánto es la mitad de {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("tengo {a} {Га}. ¿cuántos años tendré dentro de {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("¿qué número viene después del {n}?", "después del {n} viene el {m}."),
        перед=("¿qué número viene antes del {n}?", "antes del {n} viene el {m}."),
        больше=("¿cuál es mayor: {a} o {b}?", "{c} es mayor: {c} − {d} = {r}."),
        меньше=("¿cuál es menor: {a} o {b}?", "{d} es menor: {c} − {d} = {r}."),
        счёт=("cuenta del {a} al {b}.", "{ряд}."),
        обратно=("cuenta hacia atrás del {b} al {a}.", "{ряд}."),
        чёт=("¿{n} es un número par o impar?", "par: {n} = 2 × {h}.", "impar: {n} = 2 × {h} + 1."),
    ),
    "it": dict(
        между=("di' un numero tra {a} e {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("quale numero sta tra {a} e {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("ripeti i numeri: {ряд}.", "{ряд}."),
        повтори_воп=("ho detto i numeri: {ряд}. quali numeri ho detto?", "{ряд}."),
        шагом=("conta di due in due fino a {b}.", "{ряд}."),
        ряд_дальше=("continua la sequenza: {a}, {b}, {c}, ?", "{d}: il passo è {ш}."),
        наибольшее=("qual è il numero più grande: {a}, {b} o {c}?", "{m}."),
        наименьшее=("qual è il numero più piccolo: {a}, {b} o {c}?", "{m}."),
        вдвое=("quanto fa il doppio di {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. quale numero manca?", "{k}: {s} − {a} = {k}."),
        больше_ли=("{c} è maggiore di {d}?", "sì: {c} − {d} = {r}."),
        больше_ли_нет=("{d} è maggiore di {c}?", "no, {d} è minore di {c}: {c} − {d} = {r}."),
        на_сколько=("di quanto {c} è maggiore di {d}?", "di {r}: {c} − {d} = {r}."),
        словом=("come si scrive il numero {n} in lettere?", "{N}."),
        половина=("quanto fa la metà di {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ho {a} {Га}. quanti anni avrò tra {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        # the article bends before a vowel-initial number word: «dopo l'8», «dopo il 9»
        после=("che numero viene dopo {IL}{n}?", "dopo {IL}{n} viene {IM}{m}."),
        перед=("che numero viene prima {DEL}{n}?", "prima {DEL}{n} viene {IM}{m}."),
        больше=("quale è maggiore: {a} o {b}?", "{c} è maggiore: {c} − {d} = {r}."),
        меньше=("quale è minore: {a} o {b}?", "{d} è minore: {c} − {d} = {r}."),
        счёт=("conta da {a} a {b}.", "{ряд}."),
        обратно=("conta all'indietro da {b} a {a}.", "{ряд}."),
        чёт=("{n} è un numero pari o dispari?", "pari: {n} = 2 × {h}.", "dispari: {n} = 2 × {h} + 1."),
    ),
    "pt": dict(
        между=("diz um número entre {a} e {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("que número está entre {a} e {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("repete os números: {ряд}.", "{ряд}."),
        повтори_воп=("eu disse os números: {ряд}. que números eu disse?", "{ряд}."),
        шагом=("conta de dois em dois até {b}.", "{ряд}."),
        ряд_дальше=("continua a sequência: {a}, {b}, {c}, ?", "{d}: o passo é {ш}."),
        наибольшее=("qual é o maior número: {a}, {b} ou {c}?", "{m}."),
        наименьшее=("qual é o menor número: {a}, {b} ou {c}?", "{m}."),
        вдвое=("quanto é o dobro de {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. que número falta?", "{k}: {s} − {a} = {k}."),
        больше_ли=("{c} é maior do que {d}?", "sim: {c} − {d} = {r}."),
        больше_ли_нет=("{d} é maior do que {c}?", "não, {d} é menor do que {c}: {c} − {d} = {r}."),
        # «{r} a mais» — «mais» есть знак пакета («+»); «em {r}» знаком не читается
        на_сколько=("quanto é que {c} é maior do que {d}?", "em {r}: {c} − {d} = {r}."),
        словом=("como se escreve o número {n} por extenso?", "{N}."),
        половина=("quanto é a metade de {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("tenho {a} {Га}. quantos anos terei daqui a {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("que número vem depois do {n}?", "depois do {n} vem o {m}."),
        перед=("que número vem antes do {n}?", "antes do {n} vem o {m}."),
        больше=("qual é maior: {a} ou {b}?", "{c} é maior: {c} − {d} = {r}."),
        меньше=("qual é menor: {a} ou {b}?", "{d} é menor: {c} − {d} = {r}."),
        счёт=("conta de {a} a {b}.", "{ряд}."),
        обратно=("conta para trás de {b} a {a}.", "{ряд}."),
        чёт=("{n} é um número par ou ímpar?", "par: {n} = 2 × {h}.", "ímpar: {n} = 2 × {h} + 1."),
    ),
    "nl": dict(
        между=("noem een getal tussen {a} en {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("welk getal ligt tussen {a} en {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("herhaal de getallen: {ряд}.", "{ряд}."),
        повтори_воп=("ik heb de getallen genoemd: {ряд}. welke getallen heb ik genoemd?", "{ряд}."),
        шагом=("tel met sprongen van twee tot {b}.", "{ряд}."),
        ряд_дальше=("ga verder met de reeks: {a}, {b}, {c}, ?", "{d}: de stap is {ш}."),
        наибольшее=("welk getal is het grootste: {a}, {b} of {c}?", "{m}."),
        наименьшее=("welk getal is het kleinste: {a}, {b} of {c}?", "{m}."),
        вдвое=("wat is het dubbele van {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. welk getal ontbreekt?", "{k}: {s} − {a} = {k}."),
        больше_ли=("is {c} groter dan {d}?", "ja: {c} − {d} = {r}."),
        больше_ли_нет=("is {d} groter dan {c}?", "nee, {d} is kleiner dan {c}: {c} − {d} = {r}."),
        на_сколько=("hoeveel is {c} meer dan {d}?", "{r} meer: {c} − {d} = {r}."),
        словом=("hoe schrijf je het getal {n} in letters?", "{N}."),
        половина=("wat is de helft van {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ik ben {a} {Га} oud. hoe oud ben ik over {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("welk getal komt na {n}?", "na {n} komt {m}."),
        перед=("welk getal komt voor {n}?", "voor {n} komt {m}."),
        больше=("wat is groter: {a} of {b}?", "{c} is groter: {c} − {d} = {r}."),
        меньше=("wat is kleiner: {a} of {b}?", "{d} is kleiner: {c} − {d} = {r}."),
        счёт=("tel van {a} tot {b}.", "{ряд}."),
        обратно=("tel terug van {b} tot {a}.", "{ряд}."),
        чёт=("is {n} een even of een oneven getal?", "even: {n} = 2 × {h}.", "oneven: {n} = 2 × {h} + 1."),
    ),
    "pl": dict(
        между=("podaj liczbę między {a} a {c}.", "{b}: {a} < {b} < {c}."),
        между_воп=("jaka liczba leży między {a} a {c}?", "{b}: {a} < {b} < {c}."),
        повтори=("powtórz liczby: {ряд}.", "{ряд}."),
        повтори_воп=("podałem liczby: {ряд}. jakie liczby podałem?", "{ряд}."),
        шагом=("licz dwójkami do {b}.", "{ряд}."),
        ряд_дальше=("kontynuuj ciąg: {a}, {b}, {c}, ?", "{d}: krok wynosi {ш}."),
        наибольшее=("która liczba jest największa: {a}, {b} czy {c}?", "{m}."),
        наименьшее=("która liczba jest najmniejsza: {a}, {b} czy {c}?", "{m}."),
        вдвое=("ile to podwojone {n}?", "{d}: {n} × 2 = {d}."),
        пропуск=("{a} + ? = {s}. jakiej liczby brakuje?", "{k}: {s} − {a} = {k}."),
        больше_ли=("czy {c} jest większe od {d}?", "tak: {c} − {d} = {r}."),
        больше_ли_нет=("czy {d} jest większe od {c}?", "nie, {d} jest mniejsze od {c}: {c} − {d} = {r}."),
        на_сколько=("o ile {c} jest większe od {d}?", "o {r}: {c} − {d} = {r}."),
        словом=("jak zapisać liczbę {n} słownie?", "{N}."),
        половина=("ile to połowa z {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("mam {a} {Га}. ile będę mieć lat za {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("jaka liczba jest po {n}?", "po {n} jest {m}."),
        перед=("jaka liczba jest przed {n}?", "przed {n} jest {m}."),
        больше=("co jest większe: {a} czy {b}?", "{c} jest większe: {c} − {d} = {r}."),
        меньше=("co jest mniejsze: {a} czy {b}?", "{d} jest mniejsze: {c} − {d} = {r}."),
        счёт=("policz od {a} do {b}.", "{ряд}."),
        обратно=("policz wstecz od {b} do {a}.", "{ряд}."),
        чёт=("{n} to liczba parzysta czy nieparzysta?", "parzysta: {n} = 2 × {h}.", "nieparzysta: {n} = 2 × {h} + 1."),
    ),
}

ФОРМЫ = ("после", "перед", "больше", "меньше", "счёт", "обратно", "чёт", "на_сколько", "словом", "половина", "возраст",
         "пропуск", "больше_ли", "больше_ли_нет", "ряд_дальше", "наибольшее", "наименьшее", "вдвое",
         "между", "между_воп", "повтори", "повтори_воп", "шагом")
# SEVENTH BAND (06.09): the number between two (the gap of one — the answer is
# the only whole number), the numbers repeated as said, counting by twos
МЕЖДУ = ((3, 5), (7, 9), (1, 3), (10, 12), (14, 16), (18, 20), (5, 7), (11, 13))
ПОВТОРЫ = ((5, 3, 8), (2, 9, 4), (7, 7, 1), (10, 6, 3), (1, 2, 3), (8, 5, 9, 2), (4, 12, 6), (3, 3, 3))
ДВОЙКАМИ = (6, 8, 10, 12, 14, 16, 18, 20)
ПОВЕЛЕНИЯ = ("счёт", "обратно", "шагом")
# SIXTH BAND (05.09): the sequence continued by its step, the greatest and the
# smallest of three, the double
РЯДЫ = ((2, 2), (1, 1), (3, 3), (5, 1), (1, 2), (10, 2), (4, 3), (2, 1))      # (first term, step)
ТРОЙКИ_ЧИСЕЛ = ((3, 9, 5), (7, 2, 4), (12, 15, 11), (8, 1, 6), (20, 14, 17), (5, 10, 2), (9, 3, 6), (13, 18, 16))
# THE MISSING ADDEND (fifth band, 05.09): «3 + ? = 5. what number is missing? 2: 5 − 3 = 2.»
# — a hole in the equation, answered by the inverse operation
ПРОПУСКИ = ((3, 2), (5, 4), (7, 3), (2, 6), (9, 1), (4, 4), (6, 7), (8, 5))

# THE YEAR BENDS BY THE COUNT, and the rule is the pack's (count_agreement),
# not this file's: Russian «1 год / 3 года / 7 лет», Polish «rok / lata / lat»,
# the rest one plural. The forms are named by the pack's own names.
import json as _json
_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ГОД = {"ru": {"one": "год", "few": "года", "many": "лет"}, "pl": {"one": "rok", "few": "lata", "many": "lat"},
       "en": {"one": "year", "many": "years"}, "de": {"one": "Jahr", "many": "Jahre"}, "fr": {"one": "an", "many": "ans"},
       "es": {"one": "año", "many": "años"}, "it": {"one": "anno", "many": "anni"}, "pt": {"one": "ano", "many": "anos"},
       "nl": {"one": "jaar", "many": "jaar"}}
# THE CASE AFTER «IN» (fourth band, 05.09: «in 3 Jahre» was mute — German
# wants the dative plural «in 3 Jahren»): declared for the languages that bend
# the year after the preposition; the rest use the count form as it is.
ГОД_ПОСЛЕ = {"de": {"one": "Jahr", "many": "Jahren"}}
_ПАКЕТ = {}


def _пакет(язык):
    if язык not in _ПАКЕТ:
        _ПАКЕТ[язык] = _json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ПАКЕТ[язык]


def год(язык, k, после=False):
    """The count form of «year» for k by the pack's agreement rule; after the
    preposition («in 3 Jahren») the declared oblique form where the language bends it."""
    import langpack
    таблица = ГОД_ПОСЛЕ.get(язык, ГОД[язык]) if после else ГОД[язык]
    формы = list(таблица)
    i = langpack.count_form_index(_пакет(язык), {"forms": формы}, k)
    return таблица[формы[i]]


def числом(язык, n):
    """The numeral of n as the pack declares it, or None."""
    ч = _пакет(язык).get("numerals") or {}
    return ч.get(str(n))


ВОЗРАСТА = ((5, 1), (7, 3), (9, 2), (12, 5), (7, 1), (12, 3))
ВЕРХ = 20          # the line the house walks: 1..20
ДЛИНА_РЯДА = (3, 4, 5, 6)   # rows counted up or down

# ITALIAN ARTICLE BEFORE A DIGIT is the article before its WORD: «l'uno»,
# «l'otto», «l'undici», «il nove». Declared, not derived from spelling.
_ГЛАСНЫЕ_IT = frozenset({1, 8, 11, 18})


def _it(n):
    return ("l'" if n in _ГЛАСНЫЕ_IT else "il ",
            "dell'" if n in _ГЛАСНЫЕ_IT else "del ")


def _поля(n=None, m=None, a=None, b=None, ряд=None, язык=None, k=None, год_нужен=True, ш=None, тройка=None, форма=None):
    п = {}
    if ш is not None:
        return dict(a=a, b=a + ш, c=a + 2 * ш, d=a + 3 * ш, ш=ш)
    if тройка is not None:
        a_, b_, c_ = тройка
        return dict(a=a_, b=b_, c=c_, m=(max if форма == "наибольшее" else min)(тройка))
    if форма == "вдвое":
        return dict(n=n, d=2 * n)
    if форма in ("между", "между_воп"):
        return dict(a=a, b=a + 1, c=a + 2)
    if форма in ("повтори", "повтори_воп"):
        return dict(ряд=", ".join(str(x) for x in ряд))
    if форма == "шагом":
        return dict(b=b, ряд=", ".join(str(x) for x in range(2, b + 1, 2)))
    if n is not None:
        п.update(n=n, m=m, h=n // 2, IL=_it(n)[0], DEL=_it(n)[1])
        if язык is not None:
            п.update(N=числом(язык, n))
    if k is not None:
        s = a + k
        п.update(a=a, k=k, s=s)
        if год_нужен:
            п.update(Га=год(язык, a), Гk=год(язык, k, после=True), Гs=год(язык, s))
        return п
    if m is not None:
        п.update(IM=_it(m)[0])
    if a is not None:
        c, d = max(a, b), min(a, b)
        п.update(a=a, b=b, c=c, d=d, r=c - d)
    if ряд is not None:
        п.update(ряд=", ".join(str(x) for x in ряд))
    return п


# THE QUESTION AFTER THE COUNTING TASK — «count from 1 to 5. what do we get?
# 1, 2, 3, 4, 5.» An imperative carries no question by nature, and the width
# of asking (scripts/ask_width.py) counts a genus without a question surface
# as a debt; the house of tasks answers it with one declared question per
# language, and this house reads THE SAME table rather than declaring a second.
import taskforms as _T
ВОПРОС_ПОСЛЕ = _T.ВОПРОСЫ


def страница(язык, форма, вопросом=False, **чем):
    я = ЯЗЫКИ[язык][форма]
    п = _поля(язык=язык, год_нужен=(форма == "возраст"), форма=форма, **чем)
    if форма == "словом" and п.get("N") is None:
        return None            # numeral not declared by the pack — no page
    if форма == "чёт":
        ответ = я[1] if п["n"] % 2 == 0 else я[2]
    else:
        ответ = я[1]
    между = f" {ВОПРОС_ПОСЛЕ[язык]}" if вопросом else ""
    return f"{я[0].format(**п)}{между} {ответ.format(**п)}"


def пары(язык):
    """The pairs of «bigger/smaller»: two partners per number — one far along
    the line, one two steps away («7 or 9») — never itself."""
    for a in range(1, ВЕРХ + 1):
        b = (a * 7 + 3) % ВЕРХ + 1
        if b == a:
            b = b % ВЕРХ + 1
        yield a, b
        if a + 2 <= ВЕРХ and a + 2 != b:
            yield a, a + 2


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for n in range(1, ВЕРХ):
            вон[страница(язык, "после", n=n, m=n + 1)] = (язык, "после")
        for n in range(2, ВЕРХ + 1):
            вон[страница(язык, "перед", n=n, m=n - 1)] = (язык, "перед")
        for a, b in пары(язык):
            вон[страница(язык, "больше", a=a, b=b)] = (язык, "больше")
            вон[страница(язык, "меньше", a=b, b=a)] = (язык, "меньше")
        for a in range(1, 11):
            for k in ДЛИНА_РЯДА:
                if a + k - 1 > 10:
                    continue
                ряд = list(range(a, a + k))
                for вопросом in (False, True):
                    вон[страница(язык, "счёт", вопросом, a=a, b=a + k - 1, ряд=ряд)] = (язык, "счёт")
                    вон[страница(язык, "обратно", вопросом, a=a, b=a + k - 1, ряд=ряд[::-1])] = (язык, "обратно")
        for n in range(1, ВЕРХ + 1):
            вон[страница(язык, "чёт", n=n)] = (язык, "чёт")
            с = страница(язык, "словом", n=n)
            if с is not None:
                вон[с] = (язык, "словом")
            if n % 2 == 0:
                вон[страница(язык, "половина", n=n)] = (язык, "половина")
        for a, b in пары(язык):
            c, d = max(a, b), min(a, b)
            вон[страница(язык, "на_сколько", a=c, b=d)] = (язык, "на_сколько")
        for a, k in ВОЗРАСТА:
            вон[страница(язык, "возраст", a=a, k=k)] = (язык, "возраст")
        for a, k in ПРОПУСКИ:
            вон[страница(язык, "пропуск", a=a, k=k)] = (язык, "пропуск")
        for a, b in пары(язык):
            c, d = max(a, b), min(a, b)
            вон[страница(язык, "больше_ли", a=c, b=d)] = (язык, "больше_ли")
            вон[страница(язык, "больше_ли_нет", a=c, b=d)] = (язык, "больше_ли_нет")
        for a, ш in РЯДЫ:
            вон[страница(язык, "ряд_дальше", a=a, ш=ш)] = (язык, "ряд_дальше")
        for т3 in ТРОЙКИ_ЧИСЕЛ:
            вон[страница(язык, "наибольшее", тройка=т3)] = (язык, "наибольшее")
            вон[страница(язык, "наименьшее", тройка=т3)] = (язык, "наименьшее")
        for n in range(1, ВЕРХ + 1):
            вон[страница(язык, "вдвое", n=n)] = (язык, "вдвое")
        for a, c in МЕЖДУ:
            вон[страница(язык, "между", a=a)] = (язык, "между")
            вон[страница(язык, "между_воп", a=a)] = (язык, "между")
        for ряд in ПОВТОРЫ:
            вон[страница(язык, "повтори", ряд=list(ряд))] = (язык, "повтори")
            вон[страница(язык, "повтори_воп", ряд=list(ряд))] = (язык, "повтори")
        for b in ДВОЙКАМИ:
            for вопросом in (False, True):
                вон[страница(язык, "шагом", вопросом, b=b)] = (язык, "шагом")
    return вон


ПОКАЗЫ = _показы()

ДЫРЫ = {"n": r"(?P<n>\d+)", "m": r"(?P<m>\d+)", "a": r"(?P<a>\d+)", "b": r"(?P<b>\d+)",
        "c": r"(?P<c>\d+)", "d": r"(?P<d>\d+)", "r": r"(?P<r>\d+)", "h": r"(?P<h>\d+)",
        "ряд": r"(?P<ряд>\d+(?:, \d+)+)", "IL": r"(?:il |l')", "DEL": r"(?:del |dell')", "IM": r"(?:il |l')",
        "k": r"(?P<k>\d+)", "s": r"(?P<s>\d+)", "N": r"(?P<N>[^\W\d_]+(?:[ -][^\W\d_]+)*)",
        "Га": r"(?P<Га>[^\W\d_]+)", "Гk": r"(?P<Гk>[^\W\d_]+)", "Гs": r"(?P<Гs>[^\W\d_]+)",
        "ш": r"(?P<ш>\d+)"}


def _образец(шаблон, видены=None, суффикс=""):
    """A frame becomes a regex: every hole is named ONCE; a repeated hole
    becomes a back-reference, so «{c} … {c}» must carry the same number.
    The set of seen holes is shared between the question and the answer
    of one page, so the answer's {n} is the question's {n}."""
    видены = set() if видены is None else видены
    куски = []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            имя = кусок[1:-1]
            if имя in ("IL", "DEL", "IM"):
                куски.append(ДЫРЫ[имя])
            elif имя + суффикс in видены:
                куски.append(f"(?P={имя + суффикс})")
            else:
                # a suffix renames the holes of a second branch: an imperative and its
                # question twin live in ONE pattern, and the judge matches their numbers
                видены.add(имя + суффикс); куски.append(ДЫРЫ[имя].replace(f"(?P<{имя}>", f"(?P<{имя + суффикс}>"))
        else:
            куски.append(re.escape(кусок))
    return "".join(куски)


# imperative → its question twin: one genus, one pattern, two branches (the width
# of asking counts a pattern without a question surface as a debt)
БЛИЗНЕЦЫ = {"между": "между_воп", "повтори": "повтори_воп"}


def _образцы():
    вон = []
    for язык, формы in ЯЗЫКИ.items():
        for форма, я in формы.items():
            if форма in БЛИЗНЕЦЫ.values():
                continue                       # lives inside its imperative's pattern
            for k, ответ in enumerate(я[1:]):
                # one pattern over the whole page: the hole of the question and the
                # hole of the answer are the SAME hole, and a back-reference binds them
                между = "(?: " + re.escape(ВОПРОС_ПОСЛЕ[язык]) + ")?" if форма in ПОВЕЛЕНИЯ else ""
                общие = set()
                if форма in БЛИЗНЕЦЫ:
                    близнец = формы[БЛИЗНЕЦЫ[форма]][0]
                    вопрос = "(?:" + _образец(я[0], общие) + "|" + _образец(близнец, общие, "_2") + ")"
                    образ = re.compile("^" + вопрос + " " + _образец(ответ, set(), "_3") + "$")
                else:
                    образ = re.compile("^" + _образец(я[0], общие) + между + " " + _образец(ответ, общие) + "$")
                вон.append((образ, язык, форма, k))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the line is a page of a frame, and its numbers hold."""
    с = строка.strip()
    for образ, язык, форма, k in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        г = {к: (int(v) if v.isdigit() else v) for к, v in м.groupdict().items() if v is not None}
        if форма in БЛИЗНЕЦЫ:
            # the branch that matched carries the question's numbers; the answer's own
            # holes («_3») must agree with them
            вопрос = {(к[:-2] if к.endswith("_2") else к): v for к, v in г.items() if not к.endswith("_3")}
            ответ = {к[:-2]: v for к, v in г.items() if к.endswith("_3")}
            if any(ключ in ответ and ответ[ключ] != вопрос[ключ] for ключ in вопрос):
                return True, False
            г = dict(ответ, **вопрос)
        return True, _верно(форма, k, г, язык)
    return False, False


def _верно(форма, k, г, язык):
    if форма in ("между", "между_воп"):
        return г["b"] == г["a"] + 1 and г["c"] == г["a"] + 2
    if форма in ("повтори", "повтори_воп"):
        return True      # the row of the answer is bound to the row of the question by back-reference
    if форма == "шагом":
        b = г["b"]
        return b % 2 == 0 and г["ряд"] == ", ".join(str(x) for x in range(2, b + 1, 2))
    if форма == "ряд_дальше":
        a, b, c, d, ш = г["a"], г["b"], г["c"], г["d"], г["ш"]
        return ш >= 1 and b - a == ш and c - b == ш and d - c == ш
    if форма in ("наибольшее", "наименьшее"):
        тройка = (г["a"], г["b"], г["c"])
        return len(set(тройка)) == 3 and г["m"] == (max if форма == "наибольшее" else min)(тройка)
    if форма == "вдвое":
        return г["d"] == 2 * г["n"]
    if форма == "пропуск":
        return г["s"] == г["a"] + г["k"]
    if форма in ("больше_ли", "больше_ли_нет"):
        return г["c"] > г["d"] and г["r"] == г["c"] - г["d"]
    if форма == "на_сколько":
        return г["c"] > г["d"] and г["r"] == г["c"] - г["d"]
    if форма == "словом":
        return г["N"] == числом(язык, г["n"])
    if форма == "половина":
        return г["n"] % 2 == 0 and г["h"] == г["n"] // 2
    if форма == "возраст":
        a, k_, s = г["a"], г["k"], г["s"]
        return s == a + k_ and (г["Га"], г["Гk"], г["Гs"]) == (год(язык, a), год(язык, k_, после=True), год(язык, s))
    if форма == "после":
        return г["m"] == г["n"] + 1
    if форма == "перед":
        return г["m"] == г["n"] - 1
    if форма in ("больше", "меньше"):
        a, b = г["a"], г["b"]
        return a != b and г["c"] == max(a, b) and г["d"] == min(a, b) and г["r"] == г["c"] - г["d"]
    if форма in ("счёт", "обратно"):
        a, b = г["a"], г["b"]
        ряд = [int(x) for x in г["ряд"].split(", ")]
        ждём = list(range(a, b + 1)) if форма == "счёт" else list(range(b, a - 1, -1))
        return a < b and ряд == ждём
    if форма == "чёт":
        n, h = г["n"], г["h"]
        чётное = (k == 0)
        return (n % 2 == 0) == чётное and h == n // 2
    return False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for показ in list(ПОКАЗЫ)[::37]:
        битая = re.sub(r"(\d+)\.$", lambda м: f"{int(м.group(1)) + 1}.", показ)
        if битая != показ:
            # a mutant that breaks the frame itself («+ 2» for «+ 1») is a lie by
            # closure, not by count: the house reads it as no page at all
            assert судить(битая) in ((True, False), (False, False)), битая
            мутанты += судить(битая) == (True, False)
    for язык in ("ru", "en", "it"):
        print("  ", страница(язык, "после", n=8, m=9))
        print("  ", страница(язык, "больше", a=7, b=9))
        print("  ", страница(язык, "чёт", n=7))
        print("  ", страница(язык, "счёт", a=1, b=5, ряд=[1, 2, 3, 4, 5]))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
