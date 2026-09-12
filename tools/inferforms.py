#!/usr/bin/env python3
"""ДОМ СТРОГОГО ВЫВОДА — modus ponens, modus tollens и ДВЕ ОШИБКИ, названные так.

Карта форм рассуждения (reports/REASONING-2026-09-04.md) назвала главным долгом
корпуса modus tollens: корпус показывал ход от посылки к следствию и никогда —
от отрицания следствия к отрицанию посылки. Долг был назван вместе с условием
постройки: строить надо не на фактах мира («лёд не виден на поверхности →
лёд не плавает» есть строгая импликация, какой мир не даёт), а на СВОЁМ ряду
условных, каждое из которых строго.

Ряд выбран арифметический, и выбран он ради ОРАКУЛА. «Если число делится на 4,
оно делится на 2» строго не по объявлению, а по делению; всякий показ этого
дома проверяется ПЕРЕСЧЁТОМ, а не таблицей, и потому суд здесь не сторож
списка, а счётчик: подмени любое число — и суд поймает подмену сам, ничего не
зная о том, что дом хотел сказать.

ПЯТЬ ФОРМ, И ПОСЛЕДНИЕ ДВЕ ВАЖНЕЕ ПЕРВЫХ ТРЁХ:

  ЗАКОН      «если число делится на 4, оно делится на 2.»
  ПОНЕНС     «12 делится на 4. значит 12 делится на 2.»
  ТОЛЛЕНС    «7 не делится на 2. значит 7 не делится на 4.»
  ОБРАЩЕНИЕ  «6 делится на 2. значит ли, что 6 делится на 4? нет: 6 не делится на 4.»
  ОТРИЦАНИЕ  «6 не делится на 4. значит ли, что 6 не делится на 2? нет: 6 делится на 2.»

Три верных хода несут ВТОРУЮ, ВОПРОСНУЮ поверхность («12 делится на 4.
делится ли 12 на 2? да.»), и она не украшение: прибор ШИРОТЫ ВОПРОСА встал в
FAIL на первой волне этого дома — 1142 рода без вопросной поверхности при
рубеже 1109, — и долг уплачен ФОРМОЙ, а не сдвигом рубежа. Ошибки вопросную
поверхность несли с рождения, ибо ошибка иначе и не показывается: её надо
спросить, чтобы отвергнуть.

Две последние суть ОШИБКИ ВЫВОДА, показанные как ошибки: обращение импликации
и отрицание посылки. Корпус, показывающий только верные ходы, учит образцу;
корпус, показывающий неверный ход ВМЕСТЕ С ЕГО ОПРОВЕРЖЕНИЕМ, учит различать.
Свидетель у обеих ошибок ОДИН И ТОТ ЖЕ — число, делящееся на меньший делитель
и не делящееся на больший, — и это не экономия, а довод: одно наблюдение
рушит оба неверных хода разом.

Девять языков атаки. Слов нужно мало («делится на», «значит», «не», «если»),
и потому долга по языкам здесь нет.

    python3 tools/inferforms.py    # самопроверка с мутантами
"""
# (больший делитель, меньший; свидетели поненса; свидетели толленса; свидетели ошибок)
ПАРЫ = (
    (4, 2, (12, 20, 36), (7, 15, 23), (6, 10, 14)),
    (6, 3, (12, 18, 30), (7, 8, 20), (9, 15, 21)),
    (9, 3, (18, 27, 45), (7, 11, 20), (6, 12, 15)),
    (10, 5, (20, 30, 50), (7, 12, 23), (5, 15, 25)),
    (8, 4, (16, 24, 40), (6, 10, 22), (4, 12, 20)),
    (15, 5, (30, 45, 60), (7, 13, 22), (10, 20, 25)),
)

# ЧИСЛА ПРОВЕРЯЮТСЯ ПРИ ВВОЗЕ, а не на слово: дом, объявивший неверного
# свидетеля, не должен дожить до записи мира.
for _a, _b, _пон, _тол, _ош in ПАРЫ:
    assert _a % _b == 0 and _a != _b, (_a, _b)
    assert all(n % _a == 0 for n in _пон), (_a, _пон)
    assert all(m % _b for m in _тол), (_b, _тол)
    assert all(k % _b == 0 and k % _a for k in _ош), (_a, _b, _ош)

РАМКИ = {
    "ru": dict(закон="если число делится на {a}, оно делится на {b}. такое высказывание зовётся ИМПЛИКАЦИЕЙ: первая половина есть ПОСЫЛКА, вторая — СЛЕДСТВИЕ.",
               контрапозиция="«если число делится на {a}, оно делится на {b}» и «если число не делится на {b}, оно не делится на {a}» суть ОДНО высказывание в двух видах, и второе зовётся КОНТРАПОЗИЦИЕЙ первого. Вот {m}: оно не делится на {b} и не делится на {a}. А вот {n}: оно делится на {a} и делится на {b}. Числа, которое делится на {a} и не делится на {b}, нет вовсе — и потому обе записи запрещают ровно одно и то же.",
               поненс="{n} делится на {a}. значит {n} делится на {b}. этот ход зовётся УТВЕРЖДАЮЩИМ — modus ponens.",
               толленс="{m} не делится на {b}. значит {m} не делится на {a}. этот ход зовётся ОТРИЦАЮЩИМ — modus tollens.",
               обращение="{k} делится на {b}. значит ли, что {k} делится на {a}? нет: {k} не делится на {a}. эта ошибка зовётся ОБРАЩЕНИЕМ ИМПЛИКАЦИИ: из следствия не выводят посылки.",
               отрицание="{k} не делится на {a}. значит ли, что {k} не делится на {b}? нет: {k} делится на {b}. эта ошибка зовётся ОТРИЦАНИЕМ ПОСЫЛКИ: отвергнув посылку, не отвергают следствия.",),
    "en": dict(закон="if a number is divisible by {a}, it is divisible by {b}. such a statement is called an IMPLICATION: the first half is the ANTECEDENT, the second the CONSEQUENT.",
               контрапозиция="«if a number is divisible by {a}, it is divisible by {b}» and «if a number is not divisible by {b}, it is not divisible by {a}» are ONE statement in two shapes, and the second is called the CONTRAPOSITIVE of the first. Here is {m}: it is not divisible by {b} and not divisible by {a}. And here is {n}: it is divisible by {a} and divisible by {b}. There is no number at all that is divisible by {a} and not divisible by {b} — and so both shapes forbid exactly the same thing.",
               поненс="{n} is divisible by {a}. so {n} is divisible by {b}. this step is called AFFIRMING — modus ponens.",
               толленс="{m} is not divisible by {b}. so {m} is not divisible by {a}. this step is called DENYING — modus tollens.",
               обращение="{k} is divisible by {b}. does it follow that {k} is divisible by {a}? no: {k} is not divisible by {a}. this mistake is called AFFIRMING THE CONSEQUENT: from the consequent one does not infer the antecedent.",
               отрицание="{k} is not divisible by {a}. does it follow that {k} is not divisible by {b}? no: {k} is divisible by {b}. this mistake is called DENYING THE ANTECEDENT: rejecting the antecedent does not reject the consequent.",),
    "de": dict(закон="wenn eine Zahl durch {a} teilbar ist, ist sie durch {b} teilbar. eine solche Aussage heißt IMPLIKATION: die erste Hälfte ist der VORDERSATZ, die zweite der NACHSATZ.",
               контрапозиция="«wenn eine Zahl durch {a} teilbar ist, ist sie durch {b} teilbar» und «wenn eine Zahl nicht durch {b} teilbar ist, ist sie nicht durch {a} teilbar» sind EINE Aussage in zwei Gestalten, und die zweite heißt KONTRAPOSITION der ersten. Hier ist {m}: es ist nicht durch {b} teilbar und nicht durch {a} teilbar. Und hier ist {n}: es ist durch {a} teilbar und durch {b} teilbar. Eine Zahl, die durch {a} teilbar und nicht durch {b} teilbar wäre, gibt es gar nicht — und darum verbieten beide Gestalten genau dasselbe.",
               поненс="{n} ist durch {a} teilbar. also ist {n} durch {b} teilbar. dieser Schritt heißt BEJAHEND — modus ponens.",
               толленс="{m} ist nicht durch {b} teilbar. also ist {m} nicht durch {a} teilbar. dieser Schritt heißt VERNEINEND — modus tollens.",
               обращение="{k} ist durch {b} teilbar. folgt daraus, dass {k} durch {a} teilbar ist? nein: {k} ist nicht durch {a} teilbar. dieser Fehler heißt BEJAHUNG DES NACHSATZES: aus dem Nachsatz folgt der Vordersatz nicht.",
               отрицание="{k} ist nicht durch {a} teilbar. folgt daraus, dass {k} nicht durch {b} teilbar ist? nein: {k} ist durch {b} teilbar. dieser Fehler heißt VERNEINUNG DES VORDERSATZES: wer den Vordersatz verwirft, verwirft den Nachsatz nicht.",),
    "fr": dict(закон="si un nombre est divisible par {a}, il est divisible par {b}. un tel énoncé s'appelle une IMPLICATION : la première moitié est l'ANTÉCÉDENT, la seconde le CONSÉQUENT.",
               контрапозиция="« si un nombre est divisible par {a}, il est divisible par {b} » et « si un nombre n'est pas divisible par {b}, il n'est pas divisible par {a} » sont UN seul énoncé sous deux formes, et la seconde s'appelle la CONTRAPOSÉE de la première. Voici {m} : il n'est pas divisible par {b} et pas divisible par {a}. Et voici {n} : il est divisible par {a} et divisible par {b}. Un nombre divisible par {a} et non divisible par {b}, il n'y en a aucun — et donc les deux formes interdisent exactement la même chose.",
               поненс="{n} est divisible par {a}. donc {n} est divisible par {b}. ce pas s'appelle AFFIRMATIF — modus ponens.",
               толленс="{m} n'est pas divisible par {b}. donc {m} n'est pas divisible par {a}. ce pas s'appelle NÉGATIF — modus tollens.",
               обращение="{k} est divisible par {b}. en découle-t-il que {k} est divisible par {a} ? non : {k} n'est pas divisible par {a}. cette erreur s'appelle AFFIRMATION DU CONSÉQUENT : du conséquent on ne déduit pas l'antécédent.",
               отрицание="{k} n'est pas divisible par {a}. en découle-t-il que {k} n'est pas divisible par {b} ? non : {k} est divisible par {b}. cette erreur s'appelle NÉGATION DE L'ANTÉCÉDENT : rejeter l'antécédent ne rejette pas le conséquent.",),
    "es": dict(закон="si un número es divisible por {a}, es divisible por {b}. tal enunciado se llama IMPLICACIÓN: la primera mitad es el ANTECEDENTE, la segunda el CONSECUENTE.",
               контрапозиция="«si un número es divisible por {a}, es divisible por {b}» y «si un número no es divisible por {b}, no es divisible por {a}» son UN mismo enunciado en dos formas, y la segunda se llama CONTRARRECÍPROCO del primero. Aquí está {m}: no es divisible por {b} y no es divisible por {a}. Y aquí está {n}: es divisible por {a} y es divisible por {b}. Un número divisible por {a} y no divisible por {b} no existe — y por eso ambas formas prohíben exactamente lo mismo.",
               поненс="{n} es divisible por {a}. entonces {n} es divisible por {b}. este paso se llama AFIRMATIVO — modus ponens.",
               толленс="{m} no es divisible por {b}. entonces {m} no es divisible por {a}. este paso se llama NEGATIVO — modus tollens.",
               обращение="{k} es divisible por {b}. ¿se sigue que {k} es divisible por {a}? no: {k} no es divisible por {a}. este error se llama AFIRMACIÓN DEL CONSECUENTE: del consecuente no se deduce el antecedente.",
               отрицание="{k} no es divisible por {a}. ¿se sigue que {k} no es divisible por {b}? no: {k} es divisible por {b}. este error se llama NEGACIÓN DEL ANTECEDENTE: rechazar el antecedente no rechaza el consecuente.",),
    "it": dict(закон="se un numero è divisibile per {a}, è divisibile per {b}. un tale enunciato si chiama IMPLICAZIONE: la prima metà è l'ANTECEDENTE, la seconda il CONSEGUENTE.",
               контрапозиция="«se un numero è divisibile per {a}, è divisibile per {b}» e «se un numero non è divisibile per {b}, non è divisibile per {a}» sono UN solo enunciato in due forme, e la seconda si chiama CONTRONOMINALE del primo. Ecco {m}: non è divisibile per {b} e non è divisibile per {a}. Ed ecco {n}: è divisibile per {a} ed è divisibile per {b}. Un numero divisibile per {a} e non divisibile per {b} non esiste — e perciò entrambe le forme vietano esattamente la stessa cosa.",
               поненс="{n} è divisibile per {a}. quindi {n} è divisibile per {b}. questo passo si chiama AFFERMATIVO — modus ponens.",
               толленс="{m} non è divisibile per {b}. quindi {m} non è divisibile per {a}. questo passo si chiama NEGATIVO — modus tollens.",
               обращение="{k} è divisibile per {b}. ne segue che {k} è divisibile per {a}? no: {k} non è divisibile per {a}. questo errore si chiama AFFERMAZIONE DEL CONSEGUENTE: dal conseguente non si deduce l'antecedente.",
               отрицание="{k} non è divisibile per {a}. ne segue che {k} non è divisibile per {b}? no: {k} è divisibile per {b}. questo errore si chiama NEGAZIONE DELL'ANTECEDENTE: respingere l'antecedente non respinge il conseguente.",),
    "pt": dict(закон="se um número é divisível por {a}, é divisível por {b}. tal enunciado chama-se IMPLICAÇÃO: a primeira metade é o ANTECEDENTE, a segunda o CONSEQUENTE.",
               контрапозиция="«se um número é divisível por {a}, é divisível por {b}» e «se um número não é divisível por {b}, não é divisível por {a}» são UM só enunciado em duas formas, e a segunda chama-se CONTRARRECÍPROCA da primeira. Eis {m}: não é divisível por {b} e não é divisível por {a}. E eis {n}: é divisível por {a} e é divisível por {b}. Um número divisível por {a} e não divisível por {b} não existe — e por isso ambas as formas proíbem exatamente o mesmo.",
               поненс="{n} é divisível por {a}. portanto {n} é divisível por {b}. este passo chama-se AFIRMATIVO — modus ponens.",
               толленс="{m} não é divisível por {b}. portanto {m} não é divisível por {a}. este passo chama-se NEGATIVO — modus tollens.",
               обращение="{k} é divisível por {b}. segue-se que {k} é divisível por {a}? não: {k} não é divisível por {a}. este erro chama-se AFIRMAÇÃO DO CONSEQUENTE: do consequente não se deduz o antecedente.",
               отрицание="{k} não é divisível por {a}. segue-se que {k} não é divisível por {b}? não: {k} é divisível por {b}. este erro chama-se NEGAÇÃO DO ANTECEDENTE: rejeitar o antecedente não rejeita o consequente.",),
    "nl": dict(закон="als een getal deelbaar is door {a}, is het deelbaar door {b}. zo'n uitspraak heet een IMPLICATIE: de eerste helft is het ANTECEDENT, de tweede het CONSEQUENT.",
               контрапозиция="«als een getal deelbaar is door {a}, is het deelbaar door {b}» en «als een getal niet deelbaar is door {b}, is het niet deelbaar door {a}» zijn ÉÉN uitspraak in twee gedaanten, en de tweede heet de CONTRAPOSITIE van de eerste. Hier is {m}: het is niet deelbaar door {b} en niet deelbaar door {a}. En hier is {n}: het is deelbaar door {a} en deelbaar door {b}. Een getal dat deelbaar is door {a} en niet deelbaar door {b} bestaat helemaal niet — en daarom verbieden beide gedaanten precies hetzelfde.",
               поненс="{n} is deelbaar door {a}. dus {n} is deelbaar door {b}. deze stap heet BEVESTIGEND — modus ponens.",
               толленс="{m} is niet deelbaar door {b}. dus {m} is niet deelbaar door {a}. deze stap heet ONTKENNEND — modus tollens.",
               обращение="{k} is deelbaar door {b}. volgt daaruit dat {k} deelbaar is door {a}? nee: {k} is niet deelbaar door {a}. deze fout heet BEVESTIGING VAN HET CONSEQUENT: uit het consequent volgt het antecedent niet.",
               отрицание="{k} is niet deelbaar door {a}. volgt daaruit dat {k} niet deelbaar is door {b}? nee: {k} is deelbaar door {b}. deze fout heet ONTKENNING VAN HET ANTECEDENT: wie het antecedent verwerpt, verwerpt het consequent niet.",),
    "pl": dict(закон="jeśli liczba dzieli się przez {a}, dzieli się przez {b}. takie zdanie nazywa się IMPLIKACJĄ: pierwsza połowa to POPRZEDNIK, druga to NASTĘPNIK.",
               контрапозиция="«jeśli liczba dzieli się przez {a}, dzieli się przez {b}» i «jeśli liczba nie dzieli się przez {b}, nie dzieli się przez {a}» to JEDNO zdanie w dwóch postaciach, a druga nazywa się KONTRAPOZYCJĄ pierwszej. Oto {m}: nie dzieli się przez {b} i nie dzieli się przez {a}. A oto {n}: dzieli się przez {a} i dzieli się przez {b}. Liczby, która dzieli się przez {a} i nie dzieli się przez {b}, nie ma wcale — i dlatego obie postacie zakazują dokładnie tego samego.",
               поненс="{n} dzieli się przez {a}. więc {n} dzieli się przez {b}. ten krok nazywa się POTWIERDZAJĄCY — modus ponens.",
               толленс="{m} nie dzieli się przez {b}. więc {m} nie dzieli się przez {a}. ten krok nazywa się ZAPRZECZAJĄCY — modus tollens.",
               обращение="{k} dzieli się przez {b}. czy wynika z tego, że {k} dzieli się przez {a}? nie: {k} nie dzieli się przez {a}. ten błąd nazywa się POTWIERDZENIE NASTĘPNIKA: z następnika nie wynika poprzednik.",
               отрицание="{k} nie dzieli się przez {a}. czy wynika z tego, że {k} nie dzieli się przez {b}? nie: {k} dzieli się przez {b}. ten błąd nazywa się ZAPRZECZENIE POPRZEDNIKA: odrzucenie poprzednika nie odrzuca następnika.",),
}

ГОЛОВЫ = {
    "ru": ("что следует из того, что число делится на {a}?", "что следует из того, что {n} делится на {a}?", "что следует из того, что {m} не делится на {b}?"),
    "en": ("what follows from a number being divisible by {a}?", "what follows from {n} being divisible by {a}?", "what follows from {m} not being divisible by {b}?"),
    "de": ("was folgt daraus, dass eine Zahl durch {a} teilbar ist?", "was folgt daraus, dass {n} durch {a} teilbar ist?", "was folgt daraus, dass {m} nicht durch {b} teilbar ist?"),
    "fr": ("que découle-t-il du fait qu'un nombre est divisible par {a} ?", "que découle-t-il du fait que {n} est divisible par {a} ?", "que découle-t-il du fait que {m} n'est pas divisible par {b} ?"),
    "es": ("¿qué se sigue de que un número sea divisible por {a}?", "¿qué se sigue de que {n} sea divisible por {a}?", "¿qué se sigue de que {m} no sea divisible por {b}?"),
    "it": ("che cosa segue dal fatto che un numero è divisibile per {a}?", "che cosa segue dal fatto che {n} è divisibile per {a}?", "che cosa segue dal fatto che {m} non è divisibile per {b}?"),
    "pt": ("o que se segue de um número ser divisível por {a}?", "o que se segue de {n} ser divisível por {a}?", "o que se segue de {m} não ser divisível por {b}?"),
    "nl": ("wat volgt eruit dat een getal deelbaar is door {a}?", "wat volgt eruit dat {n} deelbaar is door {a}?", "wat volgt eruit dat {m} niet deelbaar is door {b}?"),
    "pl": ("co wynika z tego, że liczba dzieli się przez {a}?", "co wynika z tego, że {n} dzieli się przez {a}?", "co wynika z tego, że {m} nie dzieli się przez {b}?"),
}


# ВОПРОСНАЯ ОБЁРТКА ЕСТЬ ГОЛОВА ПЛЮС САМ ПОКАЗ, и голова НЕ ПОЛЯРНА — обе
# половины этого правила куплены отказами судов, одна за другой.
#
# Первая волна писала «12 делится на 4. делится ли 12 на 2? да.», и прибор
# ШИРОТЫ ВОПРОСА остался при своём FAIL — по делу: он засчитывает вопрос роду,
# ЧИТАЮЩЕМУ ОТВЕТНУЮ ЧАСТЬ, а ответную часть «да.» не читает никто, и род
# утверждения оставался без вопроса. Значит ответом обязан быть ВЕСЬ показ.
#
# Вторая волна так и сделала — «делится ли 12 на 2? 12 делится на 4. значит 12
# делится на 2.» — и её остановили ВОРОТА: суд дознания назвал 72 строки
# ложью, ибо ПОЛЯРНЫЙ вопрос («ли», «is …?») обязан получить «да» или «нет»
# первым словом, а не вывод. Суд прав: так спрашивают и так отвечают.
#
# Отсюда голова невопросительно-полярная: «что следует из того, что 12 делится
# на 4?» Ответ на неё есть весь показ утверждения — и род утверждения получает
# свой вопрос, — а «да» не требуется, ибо не спрошено. Заодно ушли 18 отказов
# суда письма: испанское «¿todo número …?» открывалось необъявленным зачином,
# а «¿qué se sigue …?» открывается объявленным.
for _яз, _г in ГОЛОВЫ.items():
    РАМКИ[_яз]["закон_вопрос"] = _г[0] + " " + РАМКИ[_яз]["закон"]
    РАМКИ[_яз]["поненс_вопрос"] = _г[1] + " " + РАМКИ[_яз]["поненс"]
    РАМКИ[_яз]["толленс_вопрос"] = _г[2] + " " + РАМКИ[_яз]["толленс"]

ЯЗЫКИ = tuple(РАМКИ)
ФОРМЫ = ("закон", "поненс", "толленс", "обращение", "отрицание", "контрапозиция",
         "закон_вопрос", "поненс_вопрос", "толленс_вопрос")
_СВИДЕТЕЛИ = {"поненс": 2, "толленс": 3, "обращение": 4, "отрицание": 4,
              "поненс_вопрос": 2, "толленс_вопрос": 3}

# КОНТРАПОЗИЦИЯ БЕРЁТ ДВУХ СВИДЕТЕЛЕЙ РАЗОМ, и оттого стои́т особо: прочие формы
# показывают ХОД и довольствуются одним числом, а эта показывает РАВНОСИЛЬНОСТЬ двух
# записей — и двух чисел ей мало было бы взять из одного ряда.
#
#     ХОД ПОКАЗЫВАЕТСЯ ОДНИМ СЛУЧАЕМ, РАВНОСИЛЬНОСТЬ — ДВУМЯ СРАЗУ: одним, где обе
#     записи молчат, и одним, где обе говорят.
_ДВА_СВИДЕТЕЛЯ = {"контрапозиция": (3, 2)}

for _яз in ЯЗЫКИ:
    assert set(РАМКИ[_яз]) == set(ФОРМЫ), _яз


def страница(язык, форма, пара, i=0):
    a, b, пон, тол, ош = ПАРЫ[пара % len(ПАРЫ)]
    р = РАМКИ[язык][форма]
    if форма in ("закон", "закон_вопрос"):
        return р.format(a=a, b=b)
    if форма in _ДВА_СВИДЕТЕЛЯ:
        ряд_m, ряд_n = (ПАРЫ[пара % len(ПАРЫ)][к] for к in _ДВА_СВИДЕТЕЛЯ[форма])
        return р.format(a=a, b=b, m=ряд_m[i % len(ряд_m)], n=ряд_n[i % len(ряд_n)])
    ряд = ПАРЫ[пара % len(ПАРЫ)][_СВИДЕТЕЛИ[форма]]
    с = ряд[i % len(ряд)]
    return р.format(a=a, b=b, n=с, m=с, k=с)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for пара in range(len(ПАРЫ)):
            for форма in ("закон", "закон_вопрос"):
                вон[страница(язык, форма, пара)] = (язык, форма)
            for форма in (ф for ф in ФОРМЫ if ф in _СВИДЕТЕЛИ):
                for i in range(len(ПАРЫ[пара][_СВИДЕТЕЛИ[форма]])):
                    вон[страница(язык, форма, пара, i)] = (язык, форма)
            for форма in _ДВА_СВИДЕТЕЛЯ:
                for i in range(len(ПАРЫ[пара][_ДВА_СВИДЕТЕЛЯ[форма][0]])):
                    вон[страница(язык, форма, пара, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def main():
    поймано = 0
    всего = 0
    for язык in ЯЗЫКИ:
        a, b, пон, тол, ош = ПАРЫ[0]
        мутанты = (РАМКИ[язык]["поненс"].format(a=a, b=b, n=ош[0]),        # n не делится на a
                   РАМКИ[язык]["толленс"].format(a=a, b=b, m=пон[0]),      # m делится на b
                   РАМКИ[язык]["обращение"].format(a=a, b=b, k=пон[0]),    # свидетель делится на a
                   РАМКИ[язык]["закон"].format(a=b, b=a),                   # закон обращён
                   РАМКИ[язык]["поненс_вопрос"].format(a=a, b=b, n=ош[0]))  # вопрос о неделящемся
        for м in мутанты:
            всего += 1
            поймано += 0 if м in ПОКАЗЫ else 1
        print(f"  {язык}: {страница(язык, 'толленс', 0)}")
    print(f"  мутантов вне показов: {поймано} из {всего}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, пар {len(ПАРЫ)}, форм {len(ФОРМЫ)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
