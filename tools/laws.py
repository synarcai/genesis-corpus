#!/usr/bin/env python3
"""ДОМ ЗАКОНОВ МИРОВ — определения понятий рамок ФРАЗАМИ В СМЫСЛЕ РОДА.

Заказ holon (03.09, рынок определений): словарь полки отдал «root is the
underground portion of a plant» уравнению и «cell is a small apartment» —
сетке; понятие рамки называется ФРАЗОЙ, а не словом: «a root of an
equation», «a cell of a grid», «the remainder of a division». Ответ на
«what is a cell of a grid?» открывается той же фразой.

ОДИН ДОМ НА ГЕНЕРАТОР И СУД: суд делит с генератором определение, но не
вывод — текст закона живёт здесь, генератор пишет его утверждением и
ответом на вопрос, суд узнаёт его целиком. Закон — общее утверждение БЕЗ
чисел вопроса, чьи слова покрывают понятие рамки (holon, форма рассуждения):
организм покупает его носителем и пришивает к вердикту сам.
"""

# мир → [(вопрос en, вопрос ru, закон en, закон ru)]
ЗАКОНЫ = {
    "numbers": [
        ("what is a divisor of a number?", "что такое делитель числа?",
         "a divisor of a number is a whole number that divides it with remainder 0.",
         "делитель числа — это целое число, на которое оно делится с остатком 0."),
        ("what is the remainder of a division?", "что такое остаток от деления?",
         "the remainder of a division is what is left of the dividend after the largest whole multiple of the divisor is taken away.",
         "остаток от деления — это то, что остаётся от делимого после вычитания наибольшего целого кратного делителя."),
        ("what is a multiple of a number?", "что такое кратное числа?",
         "a multiple of a number is the product of that number and a whole number.",
         "кратное числа — это произведение этого числа и целого числа."),
        ("when are two numbers congruent modulo m?", "когда два числа сравнимы по модулю m?",
         "two numbers are congruent modulo m when they leave the same remainder on division by m.",
         "два числа сравнимы по модулю m, когда дают одинаковый остаток при делении на m."),
        ("what is a coprime pair?", "что такое взаимно простые числа?",
         "a coprime pair is two numbers whose greatest common divisor is 1.",
         "взаимно простые числа — это два числа, чей наибольший общий делитель равен 1."),
        ("what is an even number?", "что такое чётное число?",
         "an even number is a whole number that is divisible by 2.",
         "чётное число — это целое число, которое делится на 2."),
    ],
    "sequences": [
        ("what is an arithmetic progression?", "что такое арифметическая прогрессия?",
         "an arithmetic progression is a sequence in which each term exceeds the previous one by the same step.",
         "арифметическая прогрессия — это последовательность, в которой каждый член больше предыдущего на один и тот же шаг."),
        ("what is a geometric progression?", "что такое геометрическая прогрессия?",
         "a geometric progression is a sequence in which each term is the previous one multiplied by the same ratio.",
         "геометрическая прогрессия — это последовательность, в которой каждый член есть предыдущий, умноженный на одно и то же отношение."),
        ("what is the limit of a sequence?", "что такое предел последовательности?",
         "the limit of a sequence is the value that its terms approach as closely as we like.",
         "предел последовательности — это значение, к которому её члены подходят сколь угодно близко."),
        ("what is the derivative of a function?", "что такое производная функции?",
         "the derivative of a function at a point is the rate at which the function changes there: for t^n it is n × t^(n − 1).",
         "производная функции в точке — это скорость её изменения в этой точке: у t^n она равна n × t^(n − 1)."),
    ],
    "geometry": [
        ("what is the area of a rectangle?", "что такое площадь прямоугольника?",
         "the area of a rectangle is the product of its two sides.",
         "площадь прямоугольника — это произведение двух его сторон."),
        ("what is the perimeter of a rectangle?", "что такое периметр прямоугольника?",
         "the perimeter of a rectangle is twice the sum of its two sides.",
         "периметр прямоугольника — это удвоенная сумма двух его сторон."),
        ("what is the hypotenuse of a right triangle?", "что такое гипотенуза прямоугольного треугольника?",
         "the hypotenuse of a right triangle is the side opposite the right angle, and its square is the sum of the squares of the other two sides.",
         "гипотенуза прямоугольного треугольника — это сторона против прямого угла, и её квадрат равен сумме квадратов двух других сторон."),
    ],
    "linalg": [
        ("what is the dot product of two vectors?", "что такое скалярное произведение векторов?",
         "the dot product of two vectors is the sum of the products of their matching components.",
         "скалярное произведение векторов — это сумма произведений их одноимённых компонент."),
        ("what is the sum of two vectors?", "что такое сумма векторов?",
         "the sum of two vectors is the vector of the sums of their matching components, in the same order.",
         "сумма векторов — это вектор сумм их одноимённых компонент в том же порядке."),
    ],
    "space": [
        ("what is a cell of a grid?", "что такое клетка сетки?",
         "a cell of a grid is one square of the grid, filled (#) or empty (_).",
         "клетка сетки — это один квадрат сетки, закрашенный (#) или пустой (_)."),
        ("what is a side-neighbour of a cell?", "что такое сосед клетки по стороне?",
         "a side-neighbour of a cell is a cell that shares a side with it: above, below, to the left or to the right.",
         "сосед клетки по стороне — это клетка с общей стороной: сверху, снизу, слева или справа."),
        ("what is a path through empty cells by side?", "что такое путь по пустым клеткам по стороне?",
         "a path through empty cells by side is a chain of empty cells in which each cell is a side-neighbour of the next.",
         "путь по пустым клеткам по стороне — это цепь пустых клеток, в которой каждая клетка — сосед следующей по стороне."),
        ("what is a grid rotated 90° clockwise?", "что такое сетка после поворота на 90° по часовой стрелке?",
         "a grid rotated 90° clockwise is the grid whose first row is the old first column read from the bottom up.",
         "сетка после поворота на 90° по часовой стрелке — это сетка, чья первая строка есть прежний первый столбец, прочитанный снизу вверх."),
        ("what is a grid reflected left-right?", "что такое сетка после отражения слева направо?",
         "a grid reflected left-right is the grid in which every row is read backwards.",
         "сетка после отражения слева направо — это сетка, в которой каждая строка читается задом наперёд."),
        ("what is a grid shifted right by k?", "что такое сетка после сдвига вправо на k?",
         "a grid shifted right by k is the grid in which every filled cell moves k columns to the right and cells that leave the grid are lost.",
         "сетка после сдвига вправо на k — это сетка, в которой каждая закрашенная клетка переходит на k столбцов вправо, а вышедшие за сетку клетки теряются."),
    ],
    "mathspaces": [
        ("what is a vertex of a graph?", "что такое вершина графа?",
         "a vertex of a graph is one of its points.", "вершина графа — это одна из его точек."),
        ("what is an edge of a graph?", "что такое ребро графа?",
         "an edge of a graph is a pair of vertices that it joins.", "ребро графа — это пара вершин, которые оно соединяет."),
        ("what is the degree of a vertex?", "что такое степень вершины?",
         "the degree of a vertex is the number of edges at it.", "степень вершины — это число рёбер при ней."),
        ("what is a path in a graph?", "что такое путь в графе?",
         "a path in a graph is a chain of vertices in which each vertex is joined to the next by an edge.",
         "путь в графе — это цепь вершин, в которой каждая вершина соединена ребром со следующей."),
        ("when is a graph connected?", "когда граф связен?",
         "a graph is connected when every vertex is reached from every other vertex by a path.",
         "граф связен, когда каждая вершина достижима из каждой другой по пути."),
        ("what is the distance between two points?", "что такое расстояние между двумя точками?",
         "the distance between two points is the length of the segment that joins them.",
         "расстояние между двумя точками — это длина отрезка, который их соединяет."),
        ("what is the midpoint of a segment?", "что такое середина отрезка?",
         "the midpoint of a segment is the point at equal distance from both its ends.",
         "середина отрезка — это точка на равном расстоянии от обоих его концов."),
        ("what is the trace of a matrix?", "что такое след матрицы?",
         "the trace of a matrix is the sum of its diagonal entries.", "след матрицы — это сумма её диагональных элементов."),
        ("what is the determinant of a matrix?", "что такое определитель матрицы?",
         "the determinant of a matrix 2 by 2 is the product of its main diagonal minus the product of its other diagonal.",
         "определитель матрицы 2 на 2 — это произведение её главной диагонали минус произведение другой диагонали."),
        ("what is a line of the Fano plane?", "что такое линия плоскости Фано?",
         "a line of the Fano plane is a triple of its seven points, and any two points lie on exactly one line.",
         "линия плоскости Фано — это тройка её семи точек, и любые две точки лежат ровно на одной линии."),
    ],
    "physlaws": [
        ("what is pressure?", "что такое давление?",
         "pressure is force divided by the area it acts on.", "давление — это сила, делённая на площадь, на которую она действует."),
        ("what is conservation of momentum?", "что такое сохранение импульса?",
         "conservation of momentum means the sum of the momenta before equals the sum after.",
         "сохранение импульса означает, что сумма импульсов до равна сумме после."),
        ("what is the dimension of a quantity?", "что такое размерность величины?",
         "the dimension of a quantity is its formula in length, mass and time.",
         "размерность величины — это её формула через длину, массу и время."),
        ("what is the period of a wave?", "что такое период волны?",
         "the period of a wave is the time of one full oscillation, and frequency is the number of oscillations per unit of time.",
         "период волны — это время одного полного колебания, а частота — число колебаний в единицу времени."),
    ],
    "cybernetics": [
        ("what is the error of a control loop?", "что такое ошибка контура управления?",
         "the error of a control loop is the target minus the current value.", "ошибка контура управления — это цель минус текущее значение."),
        ("what is a closed loop?", "что такое замкнутый контур?",
         "a closed loop is a control loop that steps while the error is not 0 and stops when the error is 0.",
         "замкнутый контур — это контур управления, который делает шаг, пока ошибка не 0, и останавливается, когда ошибка равна 0."),
        ("what is an open loop?", "что такое разомкнутый контур?",
         "an open loop is a control loop that repeats its step regardless of the error and can overshoot the target.",
         "разомкнутый контур — это контур управления, который повторяет шаг независимо от ошибки и может проскочить цель."),
        ("what is requisite variety?", "что такое необходимое разнообразие?",
         "requisite variety is the law that a regulator can distinguish no more disturbances than it has states.",
         "необходимое разнообразие — это закон, по которому регулятор различает не больше возмущений, чем у него состояний."),
    ],
    "compsci": [
        ("what is the entropy of equally likely outcomes?", "что такое энтропия равновозможных исходов?",
         "the entropy of equally likely outcomes is the number of bits needed to name one of them: log2 of their number.",
         "энтропия равновозможных исходов — это число бит, нужное, чтобы назвать один из них: log2 их числа."),
        ("what is a bit?", "что такое бит?",
         "a bit is the information that tells apart two equally likely outcomes.",
         "бит — это информация, различающая два равновозможных исхода."),
        ("what is a finite automaton?", "что такое конечный автомат?",
         "a finite automaton is a set of states with transitions, and an input leads from state to state along them.",
         "конечный автомат — это множество состояний с переходами, и вход ведёт от состояния к состоянию по ним."),
        ("what is a decidable question?", "что такое разрешимый вопрос?",
         "a decidable question is a question that a procedure answers yes or no in finitely many steps.",
         "разрешимый вопрос — это вопрос, на который процедура отвечает да или нет за конечное число шагов."),
    ],
    "glyphs": [
        ("what is a glyph?", "что такое глиф?",
         "a glyph is a grid of 5 by 7 cells that shows one sign.", "глиф — это сетка 5 на 7 клеток, показывающая один знак."),
        ("what is a glyph row?", "что такое ряд глифов?",
         "a glyph row is a line of glyphs separated by one empty column each.",
         "ряд глифов — это строка глифов, разделённых по одному пустому столбцу."),
    ],
}


def ступень(мир):
    """Строки ступени определений мира: утверждение и ответ на вопрос, оба языка."""
    вон = []
    for в_en, в_ru, з_en, з_ru in ЗАКОНЫ[мир]:
        вон += [з_en, з_ru, f"{в_en} {з_en}", f"{в_ru} {з_ru}"]
    return вон


def свод(мир):
    """Множество строк, которые суд мира узнаёт целиком как свои законы."""
    return frozenset(ступень(мир))


def по_языкам(мир):
    """{язык: множество законов мира} — для судьи рассуждения мира."""
    return {"en": frozenset(з[2] for з in ЗАКОНЫ[мир]), "ru": frozenset(з[3] for з in ЗАКОНЫ[мир])}


def закон(мир, k, язык):
    """Закон мира номер k на языке."""
    return ЗАКОНЫ[мир][k][2 if язык == "en" else 3]
