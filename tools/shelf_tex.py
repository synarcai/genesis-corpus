#!/usr/bin/env python3
"""ПОЛКА ИЗ TeX: книга Gutenberg, изданная только исходником LaTeX.

Математика Gutenberg (проект Distributed Proofreaders) лежит не текстом,
а исходником LaTeX и PDF: Дедекинд «Essays on the Theory of Numbers»,
Гильберт «Foundations of Geometry» и «Mathematical Problems», Буль
«Laws of Thought» и «Mathematical Analysis of Logic», Гаусс, Лагранж,
Евклид, Архимед, Клейн, Адамар — одиннадцать книг оснований, у которых
кузница полки получила 404 на .txt. Это ЧЕТВЁРТАЯ дорога на полку:
zip исходника → .tex → текст правилом.

ЧТО СНИМАЕТСЯ И ЧТО ОСТАЁТСЯ. Формула остаётся ФОРМУЛОЙ: «$a^2 + b^2$»
и выключная «$$ … $$» — язык книги, и своды его читают (латех у
арифметики, latex_readings у пакетов). Команды оформления (\\emph,
\\textit, \\textbf, \\Chapter, \\Section, \\footnote) отдают своё
содержимое словами; команды устройства (\\label, \\index, \\hyperref,
\\pagebreak, \\vspace, \\noindent) снимаются целиком; окружения
verbatim и tabular (шапка Gutenberg, таблицы) снимаются; заголовки
глав и разделов встают отдельными строками, окружённые пустотой (так
их читает охват понятия). Макросы, объявленные книгой (\\newcommand),
раскрываются ОДНИМ уровнем по объявлению; неизвестная команда без
аргумента снимается, с аргументом — оставляет аргумент.

Дорога честна ровно настолько, насколько мал остаток: отчёт печатает
число оставшихся обратных косых на тысячу слов, и книга, у которой
остаток велик, не кладётся (порог назван числом ниже).

Использование:
  python3 tools/shelf_tex.py --кэш <каталог> [--только dedekind_numbers] [--манифест]
"""

import argparse
import io
import pathlib
import re
import sys
import urllib.error
import urllib.request
import zipfile

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import shelf_fetch  # noqa: E402
import shelf_forge  # noqa: E402

UA = "genesis-corpus shelf_tex (contact: luxquant@gst.st)"
# ОСТАТОК КОМАНД НА ТЫСЯЧУ СЛОВ — порог честности дороги: книга, где
# после правил осталось больше, не кладётся, а её остаток печатается.
ПОРОГ_ОСТАТКА = 2.0

ПОЛКА = (
    shelf_forge.Книга(21016, "dedekind_numbers", "основания математики",
                      "трактат", 1888, 1901,
                      "Essays on the Theory of Numbers", "Richard Dedekind"),
    # «Mathematical Problems» Гильберта (71655) лежит лишь HTML с
    # формулами-картинками без alt — не текст; ждёт иного источника.
    shelf_forge.Книга(17384, "hilbert_geometry", "основания математики",
                      "трактат", 1899, 1902, "The Foundations of Geometry",
                      "David Hilbert"),
    shelf_forge.Книга(15114, "boole_laws", "логика", "трактат", 1854, 1854,
                      "An Investigation of the Laws of Thought",
                      "George Boole"),
    shelf_forge.Книга(36884, "boole_analysis", "логика", "статья",
                      1847, 1847, "The Mathematical Analysis of Logic",
                      "George Boole"),
    shelf_forge.Книга(36856, "gauss_surfaces", "математика", "трактат",
                      1827, 1902, "General Investigations of Curved Surfaces",
                      "Carl Friedrich Gauss"),
    shelf_forge.Книга(36640, "lagrange_lectures", "математика", "трактат",
                      1795, 1898, "Lectures on Elementary Mathematics",
                      "Joseph-Louis Lagrange"),
    shelf_forge.Книга(21076, "euclid_elements", "математика", "трактат",
                      -300, 1885, "The First Six Books of the Elements",
                      "Euclid"),
    shelf_forge.Книга(7825, "archimedes_method", "математика", "трактат",
                      -250, 1909, "Geometrical Solutions Derived from "
                      "Mechanics", "Archimedes"),
    shelf_forge.Книга(36154, "klein_evanston", "математика", "статья",
                      1894, 1894, "The Evanston Colloquium", "Felix Klein"),
    shelf_forge.Книга(29788, "hadamard_lectures", "математика", "статья",
                      1911, 1911, "Four Lectures on Mathematics",
                      "Jacques Hadamard"),
)


def добыть(книга, кэш):
    """Главный .tex книги из zip исходника — из кэша или с Gutenberg."""
    кэш.mkdir(parents=True, exist_ok=True)
    zip_ = кэш / f"{книга.ид}-t.zip"
    if not zip_.exists():
        адрес = f"https://www.gutenberg.org/files/{книга.ид}/{книга.ид}-t.zip"
        з = urllib.request.Request(адрес, headers={"User-Agent": UA})
        try:
            zip_.write_bytes(urllib.request.urlopen(з, timeout=300).read())
        except urllib.error.HTTPError as беда:
            if беда.code != 404:
                raise
            # ZIP НЕ ВЫЛОЖЕН — исходник лежит каталогом {id}-t/: его
            # .tex-файлы складываются в свой zip, и дорога дальше одна.
            _собрать_zip_из_каталога(книга, zip_)
    with zipfile.ZipFile(zip_) as z:
        имена = [и for и in z.namelist() if и.endswith(".tex")]
        # ГЛАВНЫЙ ФАЙЛ — ТОТ, ГДЕ \begin{document}; прочие суть включения.
        for имя in sorted(имена, key=len):
            сырое = z.read(имя)
            текст = _раскодировать(сырое)
            if r"\begin{document}" in текст:
                return текст, z, имена
    raise ValueError(f"{книга.имя}: в {zip_.name} нет .tex с \\begin{{document}}")


def _собрать_zip_из_каталога(книга, zip_):
    папка = f"https://www.gutenberg.org/files/{книга.ид}/{книга.ид}-t/"
    з = urllib.request.Request(папка, headers={"User-Agent": UA})
    список = urllib.request.urlopen(з, timeout=120).read().decode("utf-8", "replace")
    имена = sorted(set(re.findall(r'href="([^"/]+\.tex)"', список)))
    if not имена:
        raise ValueError(f"{книга.имя}: в каталоге {папка} нет .tex")
    with zipfile.ZipFile(zip_, "w", zipfile.ZIP_DEFLATED) as z:
        for имя in имена:
            з = urllib.request.Request(папка + имя, headers={"User-Agent": UA})
            z.writestr(имя, urllib.request.urlopen(з, timeout=300).read())


def _раскодировать(сырое):
    for кодировка in ("utf-8", "latin-1"):
        try:
            return сырое.decode(кодировка)
        except UnicodeDecodeError:
            continue
    return сырое.decode("utf-8", errors="replace")


# ПРАВИЛА — В ПОРЯДКЕ, И КАЖДОЕ НАЗВАНО.
КОММЕНТАРИЙ = re.compile(r"(?<!\\)%.*")
ОКРУЖЕНИЯ_ПРОЧЬ = ("verbatim", "PGtext", "tabular", "tabularx", "tabbing", "picture", "tikzpicture",
                   "figure", "table", "titlepage", "thebibliography")
ВЫКЛЮЧНЫЕ = ("equation", "equation*", "align", "align*", "gather", "gather*",
             "displaymath", "eqnarray", "eqnarray*", "multline", "multline*")
ЗАГОЛОВКИ = ("part", "chapter", "section", "subsection", "subsubsection",
             "Chapter", "Section", "Subsection", "paragraph")
ПРОЗРАЧНЫЕ = ("emph", "textit", "textbf", "textsc", "textrm", "texttt",
              "underline", "uppercase", "MakeUppercase", "mbox", "hbox",
              "text", "textup", "textsl", "Emph", "Textit", "footnote",
              "Footnote", "caption", "centerline", "Heading", "title",
              "author", "date", "quotation", "flushright", "flushleft",
              "center", "SubHeading", "ensuremath", "Figure")
СНЯТЬ_С_АРГУМЕНТОМ = ("label", "index", "hypertarget", "hyperref", "pageref",
                      "ref", "eqref", "cite", "vspace", "hspace", "vspace*",
                      "hspace*", "setlength", "addtolength", "setcounter",
                      "addtocontents", "addcontentsline", "phantomsection",
                      "pagenumbering", "pagestyle", "thispagestyle",
                      "markboth", "markright", "newlabel", "include",
                      "input", "bibliographystyle", "bibliography",
                      "usepackage", "documentclass", "def", "let",
                      "renewcommand", "newcommand", "providecommand",
                      "DeclareMathOperator", "newenvironment", "Pagelabel",
                      "PageSep", "DPPageSep", "pagebreak", "linebreak",
                      "enlargethispage", "ChapterTocEntry", "PGLicense",
                      "nopagebreak", "setlist", "numberwithin", "graphicspath", "Runhead",
                      "PageLabel", "Pagelabel", "pagelabel", "Figref", "Pageref",
                      "DPtypo", "typo", "boolean", "setboolean", "newboolean",
                      "includegraphics", "rule", "hfill", "vfill")
СНЯТЬ_ГОЛЫЕ = ("noindent", "clearpage", "cleardoublepage", "newpage",
               "bigskip", "medskip", "smallskip", "par", "indent", "hfill",
               "vfill", "centering", "raggedright", "raggedleft", "small",
               "large", "Large", "LARGE", "huge", "Huge", "normalsize",
               "footnotesize", "scriptsize", "tiny", "itshape", "bfseries", "normalfont",
               "scshape", "upshape", "rmfamily", "sffamily", "ttfamily",
               "frontmatter", "mainmatter", "backmatter", "maketitle",
               "tableofcontents", "printindex", "newline", "linebreak",
               "nolinebreak", "protect", "relax", "null", "hrulefill",
               "dotfill", "quad", "qquad", "enspace", "thinspace",
               "PGCleanup", "flushbottom", "raggedbottom", "sloppy",
               "allowdisplaybreaks", "appendix")
ЛИГАТУРЫ = (("``", "«"), ("''", "»"), ("---", " — "), ("--", "–"),
            ("~", " "), ("\\,", " "), ("\\;", " "), ("\\ ", " "),
            ("\\-", ""), ("\\/", ""), ("\\&", "&"), ("\\%", "%"),
            ("\\#", "#"), ("\\_", "_"), ("\\{", "{"),
            ("\\}", "}"), ("\\textquoteleft", "‘"), ("\\textquoteright", "’"),
            ("\\ldots", "…"), ("\\dots", "…"), ("\\S", "§"), ("\\P", "¶"),
            ("\\ae", "æ"), ("\\AE", "Æ"), ("\\oe", "œ"), ("\\OE", "Œ"),
            ("\\ss", "ß"), ("\\lq", "‘"), ("\\rq", "’"), ("\\@", ""))
УДАРЕНИЯ = {"'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý",
                  "E": "É", "A": "Á"},
            "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù", "A": "À"},
            "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
            '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü", "A": "Ä",
                  "O": "Ö", "U": "Ü"},
            "~": {"n": "ñ", "a": "ã", "o": "õ"},
            "c": {"c": "ç", "C": "Ç"}}


def _аргумент(текст, i):
    """(содержимое, конец) фигурного аргумента, начатого в текст[i] == '{'."""
    глубина, j = 0, i
    while j < len(текст):
        if текст[j] == "{":
            глубина += 1
        elif текст[j] == "}":
            глубина -= 1
            if глубина == 0:
                return текст[i + 1:j], j + 1
        j += 1
    return текст[i + 1:], len(текст)


def _макросы(тело):
    """{имя: (число аргументов, замена)} — \\newcommand книги."""
    вон = {}
    for м in re.finditer(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?"
                         r"(?:\[(\d)\])?\s*(?=\{)", тело):
        замена, _ = _аргумент(тело, м.end())
        вон[м.group(1)] = (int(м.group(2) or 0), замена)
    return вон


def _раскрыть_макросы(тело, макросы):
    """Один уровень раскрытия макросов книги; аргументы — #1..#n.

    ПОГЛОЩЕНИЕ АРГУМЕНТОВ — ЯВНЫМ ПРОХОДОМ, а не заменой по образцу:
    первая редакция подставляла тело макроса, а его аргументы оставляла
    в тексте, и за каждым заголовком Дедекинда шёл его же хвост
    («XVIIIComparison of the Rational Numbers…» — метка страницы, номер и
    заглавие, склеенные из брошенных аргументов).
    """
    if not макросы:
        return тело
    имена = sorted(макросы, key=len, reverse=True)
    образец = re.compile(r"\\(" + "|".join(re.escape(и) for и in имена)
                         + r")(?![A-Za-z])")
    вон, i = [], 0
    while True:
        м = образец.search(тело, i)
        if not м:
            вон.append(тело[i:])
            break
        вон.append(тело[i:м.start()])
        n, тело_макроса = макросы[м.group(1)]
        j = м.end()
        аргументы = []
        for _ in range(n):
            while j < len(тело) and тело[j] in " \t\n":
                j += 1
            if j < len(тело) and тело[j] == "{":
                а, j = _аргумент(тело, j)
            elif j < len(тело):
                а, j = тело[j], j + 1
            else:
                а = ""
            аргументы.append(а)
        раскрытое = тело_макроса
        for k, а in enumerate(аргументы, 1):
            раскрытое = раскрытое.replace(f"#{k}", а)
        вон.append(раскрытое)
        i = j
    return "".join(вон)


def _снять_окружения(тело):
    for имя in ОКРУЖЕНИЯ_ПРОЧЬ:
        тело = re.sub(r"\\begin\{" + re.escape(имя) + r"\}.*?\\end\{"
                      + re.escape(имя) + r"\}", "\n", тело, flags=re.S)
    return тело


def _выключные(тело):
    """Выключная формула — своей строкой между $$."""
    for имя in ВЫКЛЮЧНЫЕ:
        тело = re.sub(r"\\begin\{" + re.escape(имя) + r"\}(.*?)\\end\{"
                      + re.escape(имя) + r"\}",
                      lambda м: "\n$$ " + " ".join(м.group(1).split()) + " $$\n",
                      тело, flags=re.S)
    тело = re.sub(r"\\\[(.*?)\\\]", lambda м: "\n$$ " + " ".join(
        м.group(1).split()) + " $$\n", тело, flags=re.S)
    тело = re.sub(r"\$\$(.*?)\$\$", lambda м: "\n$$ " + " ".join(
        м.group(1).split()) + " $$\n", тело, flags=re.S)
    return тело


def _ударения(тело):
    def з(м):
        знак, буква = м.group(1), м.group(2)
        return УДАРЕНИЯ.get(знак, {}).get(буква, буква)
    return re.sub(r"\\([\'`^\"~c])\{?([A-Za-z])\}?", з, тело)


def _команды(тело):
    """Заголовки, прозрачные, снимаемые — по спискам; остаток — правилом."""
    вон, i = [], 0
    образец = re.compile(r"\\([A-Za-z]+\*?|.)")
    while True:
        м = образец.search(тело, i)
        if not м:
            вон.append(тело[i:])
            break
        вон.append(тело[i:м.start()])
        имя = м.group(1)
        j = м.end()
        if имя.rstrip("*") in ЗАГОЛОВКИ:
            # Необязательный короткий заголовок [..] снимается.
            if j < len(тело) and тело[j] == "[":
                k = тело.find("]", j)
                j = k + 1 if k > 0 else j
            if j < len(тело) and тело[j] == "{":
                а, j = _аргумент(тело, j)
                вон.append("\n\n" + " ".join(_команды(а).split()) + "\n\n")
        elif имя.rstrip("*") in ПРОЗРАЧНЫЕ:
            while j < len(тело) and тело[j] == "[":
                k = тело.find("]", j)
                j = k + 1 if k > 0 else j
            if j < len(тело) and тело[j] == "{":
                а, j = _аргумент(тело, j)
                # АРГУМЕНТ ЧИТАЕТСЯ ТЕМИ ЖЕ ПРАВИЛАМИ: сноска несёт свой
                # курсив («\\footnote{\\textit{Vorlesungen} …}»), и без
                # рекурсии он оставался командой.
                а = _команды(а)
                вон.append(а if имя not in ("footnote", "Footnote")
                           else " (" + " ".join(а.split()) + ") ")
        elif имя.rstrip("*") in СНЯТЬ_С_АРГУМЕНТОМ:
            while j < len(тело) and тело[j] in "[{":
                if тело[j] == "[":
                    k = тело.find("]", j)
                    j = k + 1 if k > 0 else j + 1
                else:
                    _, j = _аргумент(тело, j)
        elif имя == "ifthenelse":
            # \ifthenelse{условие}{да}{нет}: у книг DP условие есть
            # \boolean{FixTypos} — берётся ветвь «да» (исправленный текст).
            ветви = []
            for _ in range(3):
                while j < len(тело) and тело[j] in " \n":
                    j += 1
                if j < len(тело) and тело[j] == "{":
                    а, j = _аргумент(тело, j)
                    ветви.append(а)
            if len(ветви) == 3:
                вон.append(_команды(ветви[1]))
        elif имя == "item":
            метка = ""
            if j < len(тело) and тело[j] == "[":
                k = тело.find("]", j)
                метка, j = (тело[j + 1:k], k + 1) if k > 0 else ("", j + 1)
            вон.append("\n" + (метка + " " if метка.strip() else "• "))
        elif имя in ("begin", "end"):
            if j < len(тело) and тело[j] == "{":
                _, j = _аргумент(тело, j)
            while j < len(тело) and тело[j] == "[":
                k = тело.find("]", j)
                j = k + 1 if k > 0 else j + 1
            вон.append("\n")
        elif имя in СНЯТЬ_ГОЛЫЕ or len(имя) == 1 and not имя.isalpha():
            if имя == "\\":
                вон.append("\n")
            elif len(имя) == 1 and not имя.isalpha():
                вон.append(имя)   # \& \% и прочие уже сняты лигатурами
        else:
            # НЕИЗВЕСТНАЯ КОМАНДА: с аргументом оставляет аргумент, без —
            # снимается; счёт остатка ведётся по ней отдельно.
            if j < len(тело) and тело[j] == "{":
                а, j = _аргумент(тело, j)
                вон.append(_команды(а))
        i = j
    return "".join(вон)


def текст(tex):
    """Текст книги из исходника — по правилам выше, в их порядке."""
    tex = tex.replace("\r\n", "\n").replace("\r", "\n")
    tex = КОММЕНТАРИЙ.sub("", tex)   # и в макросах книги: их тела входят в текст
    тело = tex.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    макросы = _макросы(tex.split(r"\begin{document}", 1)[0])
    тело = _снять_окружения(тело)
    тело = _раскрыть_макросы(тело, макросы)
    тело = _выключные(тело)
    # ФОРМУЛЫ ПРЯЧУТСЯ на время правил над прозой и возвращаются целыми.
    формулы = []
    # ЭКРАНИРОВАННЫЙ ДОЛЛАР — ЦЕНА, А НЕ ГРАНИЦА ФОРМУЛЫ: «\$1.00 net»
    # в каталоге издателя первой редакцией был принят за начало формулы,
    # и всё до следующего доллара ушло в формулу непрочищенным (228
    # \raisebox у Дедекинда — оттуда).
    тело = тело.replace("\\$", "\x02")

    def спрятать(м):
        формулы.append(" ".join(м.group(0).split()))
        return f"\x01{len(формулы) - 1}\x01"
    # ФОРМУЛА НЕ ПЕРЕХОДИТ ПУСТУЮ СТРОКУ: одиночный «$» или «\\(» в
    # записке переписчика прятал под видом формулы тысячи знаков книги,
    # и они возвращались сырыми (Гаусс: 46 \\normalsize). Формула
    # ограничена абзацем и разумной длиной.
    тело = re.sub(r"\$\$ .*? \$\$|\$(?:(?!\$|\n\n).){1,1200}?\$"
                  r"|\\\((?:(?!\\\)|\n\n).){1,1200}?\\\)", спрятать, тело,
                  flags=re.S)
    тело = _ударения(тело)
    for было, стало in ЛИГАТУРЫ:
        тело = тело.replace(было, стало)
    тело = _команды(тело)
    тело = re.sub(r"\x01(\d+)\x01", lambda м: формулы[int(м.group(1))], тело)
    тело = тело.replace("\x02", "$")
    тело = тело.replace("{", "").replace("}", "")
    тело = re.sub(r"[ \t]+", " ", тело)
    тело = re.sub(r" *\n *", "\n", тело)
    тело = re.sub(r"\n{3,}", "\n\n", тело)
    return тело.strip() + "\n"


ЧУЖОЙ_АБЗАЦ = re.compile(r"Project Gutenberg|This PDF file|Transcriber'?s? Note|recompiled for screen|www\.gutenberg|LaTeX source", re.I)


def абзацы(текст_):
    """Строки книги: абзац — одной строкой; заголовок — своей."""
    вон = []
    for кусок in текст_.split("\n\n"):
        кусок = " ".join(кусок.split())
        # ШАПКА GUTENBERG И ЗАПИСКА ПЕРЕПИСЧИКА — НЕ ТЕКСТ КНИГИ (как
        # благодарности у кузницы): абзац о самом файле снимается.
        # …но лишь КОРОТКИЙ: длинный абзац с упоминанием Gutenberg есть
        # текст книги (Адамар: одна такая строка уносила 13 тысяч слов).
        if ЧУЖОЙ_АБЗАЦ.search(кусок) and len(кусок.split()) < 120:
            continue
        if кусок:
            вон.append(кусок)
            вон.append("")
    return вон


def остаток(строки):
    """Обратных косых ВНЕ ФОРМУЛ на тысячу слов — мера честности дороги.
    Внутри формул TeX есть язык книги («\\frac», «\\sum») и не остаток."""
    без = [re.sub(r"\$\$ .*? \$\$|\$[^$]+\$", " ", с) for с in строки]
    слов = sum(len(re.findall(r"[A-Za-z]+", с)) for с in строки)
    косых = sum(с.count("\\") for с in без)
    return 1000 * косых / слов if слов else 0.0


def ковать(книга, кэш, манифест):
    tex, _z, имена = добыть(книга, кэш)
    строки = абзацы(текст(tex))
    ост = остаток(строки)
    слов = sum(len(re.findall(r"[A-Za-z]+", с)) for с in строки)
    if ост > ПОРОГ_ОСТАТКА:
        print(f"  ОТКАЗ {книга.имя}: остаток команд {ост:.1f} на тысячу слов "
              f"при пороге {ПОРОГ_ОСТАТКА} — дорога не дочищена")
        return None
    тело, отложенное = shelf_fetch.отложить(строки)
    выход = КОРЕНЬ / "shelf" / "en"
    байт, строк = shelf_fetch.записать(выход / f"{книга.имя}.txt", тело)
    ещё = (shelf_fetch.записать(выход / f"{книга.имя}.holdout.txt", отложенное)
           if отложенное else (0, 0))
    формул = sum(с.count("$") for с in тело) // 2
    print(f"  {книга.имя:<22} строк {строк:>6} отложено {ещё[1]:>5} слов "
          f"{слов:>7} формул {формул:>5} остаток {ост:.2f}‰ "
          f"(tex-файлов {len(имена)})")
    return книга


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--кэш", required=True)
    ap.add_argument("--только", default="")
    ap.add_argument("--манифест", action="store_true")
    а = ap.parse_args()
    кэш = pathlib.Path(а.кэш) / "tex"
    хотим = set(а.только.split(",")) if а.только else None
    легли = []
    for книга in ПОЛКА:
        if хотим and книга.имя not in хотим:
            continue
        try:
            к = ковать(книга, кэш, а.манифест)
        except Exception as беда:  # noqa: BLE001 — отчёт, не падение
            print(f"  ОТКАЗ {книга.имя}: {беда}")
            continue
        if к:
            легли.append(к)
    if а.манифест and легли:
        заменено, добавлено = shelf_forge.вписать_в_манифест(легли)
        print(f"  МАНИФЕСТ: заменено {заменено}, добавлено {добавлено}")
    print(f"ПОЛКА TeX: {len(легли)} книг из {len(ПОЛКА) if not хотим else len(хотим)}")
    return 0 if легли else 2


if __name__ == "__main__":
    sys.exit(main())
