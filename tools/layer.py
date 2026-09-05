#!/usr/bin/env python3
"""THE PASS DISCIPLINE OF A GENESIS LAYER — one law, one place.

Fifteen generators carried this law as fifteen copies, and copies do
not stay equal. `shuffle` had split into FOUR bodies: two guarded the
empty list and two did not, so nine layers died with a bare
StopIteration on a pass that produced nothing — the very «empty walk»
fault the audit park forbids in its own instruments. The pass table
`[(7,5), (11,2), (13,9), (17,4), (19,12)]` stood unnamed in fourteen
files, and the seam, the byte count and the written line were written
out by hand fifteen times.

WHAT THE LAW ACTUALLY SAYS:
  · a layer is emitted in PASSES, and each pass varies its instances,
    so volume buys new facts instead of new weight (the knowledge-trail
    number: an x1 layer bought +9464 owned types where x22 layers
    bought zero);
  · each pass is SHUFFLED by a stride coprime with its length — a
    permutation, never a sample: nothing is dropped and nothing is
    doubled;
  · passes are separated by a FORM FEED, so the reader that cuts a
    corpus into worlds finds an honest seam.
"""

# ПРОХОДЫ: пять пар (шаг, сдвиг). Пары взаимно просты с обычными
# длинами проходов, и потому перестановка — настоящая; пятикратность
# взята из тропы знания, где слой ×1 покупал типы, а ×22 — вес.
PASSES = ((7, 5), (11, 2), (13, 9), (17, 4), (19, 12))
SEAM = "\n\x0c\n"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def shuffle(items, mult, shift):
    """A PERMUTATION, NOT A SAMPLE — and the empty list is empty.

    Nine of fifteen copies lacked this guard: `next()` over an empty
    range raises StopIteration, so a pass that produced nothing killed
    the generator with a traceback about iterators instead of writing
    nothing. A layer may legitimately produce no shows in a pass.
    """
    n = len(items)
    if n == 0:
        return []
    step = next(k for k in range(mult, mult + n) if gcd(k, n) == 1)
    return [items[(i * step + shift) % n] for i in range(n)]


# ВОРОТА ЗАПИСИ: СЛОЙ НЕ МОЖЕТ РОДИТЬСЯ С ЛОЖНОЙ ИЛИ НЕСУДИМОЙ СТРОКОЙ.
#
# Прежде порядок был иной: генератор писал файл, а суды спрашивали
# потом, обходом. Это ЛОВИТ дефект, но ДОПУСКАЕТ ЕГО СУЩЕСТВОВАНИЕ — и
# допустило дважды за час: «1 days after saturday» (английское
# согласование в слое календаря) и шесть честных русских ставок,
# объявленных ложью чужим судом из-за совпадения формы. Оба поймал
# обход, и оба УСПЕЛИ ЛЕЧЬ В КОРПУС.
#
# Здесь дефект становится НЕВОЗМОЖНЫМ, а не обнаружимым. Это разница
# между «мы это ловим» и «этого не бывает».
#
# ДВА УСЛОВИЯ, И ОБА ОБЯЗАТЕЛЬНЫ:
#  · ни одна строка не названа ЛОЖЬЮ ни одним судом;
#  · ни одна строка не осталась НЕСУДИМОЙ — рубеж охвата стоит на ста
#    процентах, и слой, приносящий несудимую форму, уронил бы его
#    завтра. Пусть падает сегодня, у своего автора, а не в общем обходе.
#
# ВОРОТА, КОТОРЫХ НЕТ, ОБЪЯВЛЯЮТ О СЕБЕ. Сборка в пустом дереве (прибор
# воспроизводимости) судов не имеет; запись не запрещается, но число
# живых судов ПЕЧАТАЕТСЯ. Тихо выключенная охрана хуже отсутствующей:
# отсутствие видно.
ВОРОТА_ВЫКЛ = "GENESIS_NO_GATE"


def _ворота(path, body):
    """Отказать в записи, если суд зовёт строку ложью или молчит о ней."""
    import os
    import pathlib
    if os.environ.get(ВОРОТА_ВЫКЛ):
        print(f"ВОРОТА ОТКЛЮЧЕНЫ ({ВОРОТА_ВЫКЛ}) — {path} записан без суда")
        return
    try:
        from panel import палата
        суд = палата()
    except Exception as беда:
        print(f"ВОРОТА БЕЗ ПАЛАТЫ ({беда}) — {path} записан без суда")
        return
    if not суд.живых:
        print(f"ВОРОТА БЕЗ СУДОВ (живых 0) — {path} записан без суда")
        return
    врем = pathlib.Path(str(path) + ".ворота")
    врем.write_text(body, encoding="utf-8")
    try:
        вердикты = суд.судить_файл(врем)
    finally:
        врем.unlink(missing_ok=True)
    ложных = [с for с, судимо, истинно, _ in вердикты if судимо and not истинно]
    немых = [с for с, судимо, _, _ in вердикты if not судимо]
    if ложных or немых:
        for с in ложных[:3]:
            print(f"  ЛОЖЬ: {с[:90]}")
        for с in немых[:3]:
            print(f"  НЕСУДИМО: {с[:90]}")
        raise SystemExit(
            f"ВОРОТА ЗАКРЫТЫ: {path} не записан — "
            f"ложных {len(ложных)}, несудимых {len(немых)} "
            f"(судов живых {суд.живых})")



# ПОТОЛОК ПОВТОРА СТРОКИ — LAW, А НЕ ЧИСЛО ПРОХОДОВ (05.09, вердикт коллегии
# по слову владельца: «только вы коллегиально можете решить»). Перепись
# повторов нашла: 50 % строк свода — точные копии, 40 % — сверх LAW=2, одна
# строка до 460 раз. Три ковки читателя: база 91/96, потолок по своду 91/96
# (word_integrity 0,99 → 1,0), потолок по блоку — третья строка реестра;
# ворота читателя holon пройдены (графа 102 = 102, истории 2 = 2, потерь 0).
# Копия сверх LAW не есть показ: скелет строки без дыр есть она сама, и третья
# копия не учит ничему, чему не научила вторая. Слово покупается при двух
# встречах — две копии дают ему ровно это. Счёт ведётся ПО МИРУ, через все
# проходы: мир есть единица свода, а не проход.
from langpack import LAW  # noqa: E402


def _потолок(shows, выдано):
    """Показы прохода без копий сверх LAW — счёт ведётся по всему миру.

    ПОРЯДОК ПЕРВОГО ВХОЖДЕНИЯ ХРАНИТСЯ, И ЭТО СУД, А НЕ ОБЕЩАНИЕ (условие
    holon/d5, снятое замером: сортированный дедуп того же содержания двигает
    три четверти покупок — страница есть отрезок ленты). Потолок лишь снимает
    копии сверх LAW; ни одна оставшаяся строка не меняет места относительно
    других — проверяется здесь же на каждом проходе.
    """
    вон = []
    for с in shows:
        if выдано.get(с, 0) >= LAW:
            continue
        выдано[с] = выдано.get(с, 0) + 1
        вон.append(с)
    # суд порядка: оставшиеся строки идут в том же порядке, что и в исходном проходе
    ит = iter(shows)
    for с in вон:
        for исх in ит:
            if исх == с:
                break
        else:
            raise AssertionError("потолок повтора переставил строку: " + с[:60])
    return вон


def emit(path, pass_shows, passes=PASSES):
    """Run the passes, weld them with seams, write, and say the number.

    `pass_shows(i)` returns the shows of pass i. The count printed is
    SHOWS, not lines: a show may span several lines (the fractions
    layer speaks one fact on three surfaces), and reporting lines would
    quietly inflate it.
    """
    blocks, total, выдано = [], 0, {}
    for pi, (mult, shift) in enumerate(passes):
        shows = _потолок(pass_shows(pi), выдано)
        total += len(shows)
        blocks.append("\n".join(shuffle(shows, mult, shift)))
    body = SEAM.join(blocks) + "\n"
    _ворота(path, body)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"written {path}: {len(body)} bytes, {total} shows")
    return body


def emit_grouped(path, pass_groups, passes=PASSES):
    """The same law where a pass carries SEVERAL kinds.

    Two layers (structures, units) weld one block per KIND per pass
    rather than one block per pass: their kinds are separate worlds of
    show and must not be interleaved by the shuffle. The stride is the
    pass's own, so a kind is permuted, never sampled — the law is the
    same law, applied one level down.
    """
    blocks, total, выдано = [], 0, {}
    for pi, (mult, shift) in enumerate(passes):
        for shows in pass_groups(pi):
            shows = _потолок(shows, выдано)
            total += len(shows)
            blocks.append("\n".join(shuffle(shows, mult, shift)))
    body = SEAM.join(blocks) + "\n"
    _ворота(path, body)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"written {path}: {len(body)} bytes, {total} shows")
    return body

