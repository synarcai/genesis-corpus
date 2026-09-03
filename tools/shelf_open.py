#!/usr/bin/env python3
"""ПОЛКА ОТКРЫТЫХ КОРПУСОВ: современные книги и статьи о мозге, познании
и сознании под свободной лицензией — пятая дорога на полку.

СЛОВО ВЛАДЕЛЬЦА: «подготовить внешние качественные корпуса по
когнитивистике, нейропсихологии и всему, что связано с мозгом,
познанием, сознанием». Классика до 1929 года легла кузницей Gutenberg
(Юнг, Фрейд, Джеймс, Вундт). Здесь берётся ВТОРОЙ РАЗРЯД договора полки
(`declarations/SHELF.md`): издано до рубежа машины 2022 под лицензией,
совместимой с лицензией корпуса, — CC BY. CC BY-SA и CC BY-NC с корпусом
CC BY 4.0 несовместимы и не берутся, и это стоило дороге того самого
источника, ради которого её начали.

OPENSTAX ПЕРЕЛИЦЕНЗИРОВАЛСЯ, И ЭТО ЗАМЕРЕНО ПРИБОРОМ, А НЕ ПРОЧИТАНО В
НОВОСТЯХ. Дорога начиналась ради «Psychology 2e», «Biology 2e», «Anatomy
and Physiology 2e» и «Introduction to Philosophy», числившихся CC BY 4.0.
Замер 02.09.2026 по четырём свидетельствам самого издателя говорит иное:
LICENSE репозитория openstax/osbooks-psychology сменён на CC BY-NC-SA
коммитом от 2026-03-23, <md:license> коллекции — 2026-04-23; предисловие
книги ныне само пишет «licensed under a Creative Commons
Attribution-NonCommercial-ShareAlike 4.0»; CMS openstax.org называет
BY-NC-SA у всех действующих изданий, включая «Introduction to Behavioral
Neuroscience» (2024) и «Introduction to Philosophy» (2022). ОТСТАВЛЕННЫЕ
первые издания — «Psychology» (2014), «Biology» (2016), «Anatomy and
Physiology» (2013) — издатель и сегодня объявляет CC BY 4.0: так стоит в
его CMS, в JSON каждой книги в его же архиве, откуда берётся текст, и в
предисловии каждой из них. Они берутся; ушедший в BY-NC-SA текст — нет.
Взять старый коммит 2e под прежней лицензией было бы законно (грант CC
необратим), но это спор с издателем, а договор велит: спорное не берём,
спор дороже книги.

ЛИЦЕНЗИЯ ЧИТАЕТСЯ ИЗ САМОГО ИСТОЧНИКА ПРИ КАЖДОЙ КОВКЕ, а не из
объявления: JSON книги OpenStax несёт license.url, metadata Pressbooks —
license.url, XML статьи JATS — <license xlink:href>. Книга, чей источник
называет иную лицензию, чем объявлено здесь, не куётся, и отказ
печатается. Статья Europe PMC сверх того сверяется по году: изданная не
раньше рубежа машины не берётся, даже если поиск её отдал.

ЧИСТКА СТРУКТУРНАЯ, А НЕ СЛОВАРНАЯ (закон shelf_fetch): снимается
ПОДДЕРЕВО служебного узла, названное самим источником — классом,
data-type, ролью, тегом. Что снято и почему:
  * рисунки, подписи, таблицы, формулы без TeX, встроенные видео и
    H5P — не текст;
  * учебный аппарат — цели раздела, ключевые термины, итоги, вопросы,
    упражнения — по классу узла или по РУБРИКЕ: раздел, чей заголовок
    стоит в списке рубрик аппарата, снимается до следующего заголовка
    того же или старшего уровня; конспект («Summary», «Chapter Review»)
    снимается по договору — пересказ на полку не кладём;
  * библиография и сноски — по классу и по рубрике; внутритекстовый
    знак сноски — по СТРОЧНОМУ ПОЛОЖЕНИЮ (верхний индекс внутри ссылки),
    а верхний индекс вне ссылки остаётся: «Ca2+» и «10^14» суть текст,
    «[1]» — нет;
  * врезка с гиперссылкой НАРУЖУ («Visit this link to see…») —
    указатель, а не текст: снимается врезка (textbox, note), несущая
    ссылку на другой сайт; ссылка внутрь книги (#figure) врезку не губит;
  * пункт списка остаётся, если он ПРЕДЛОЖЕНИЕ — кончается знаком конца
    предложения или длиннее медианной строки прозы корпуса: посылки
    аргумента остаются, перечень терминов уходит;
  * отсылки к рисункам в скобках («(Figure 1.2)», «[link]») снимаются
    правилом, и опустевшие после них скобки — тоже.
Мера честности дороги печатается: сколько осталось «[link]», угловых и
пустых скобок на книгу.

ВТОРАЯ КОПИЯ ОДНОЙ КНИГИ ПРИНОСИТ НОЛЬ (shelf_kinds): «Neuroscience:
Canadian 1st Edition» Ju в первой части дословно переносит главы
«Anatomy and Physiology» OpenStax (3, 12–17); берутся её части 2–4 —
собственный текст Торонто, — а нервная система берётся у OpenStax.

УЗЛЫ МАНИФЕСТА НЕ ПИШУТСЯ В МАНИФЕСТ: его правит соседняя сессия в тот
же час, и две руки в одном файле суть гонка. Узлы складываются в
`reports/pending-manifest-open.json` (список узлов договора по имени
мира; свежий заменяет прежний); вписать их — дело хозяина манифеста.

Использование:
  python3 tools/shelf_open.py --кэш <каталог> [--только rebus_philosophy_of_mind,…]
"""

import argparse
import collections
import html
import html.parser
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import shelf_fetch  # noqa: E402
import shelf_kinds  # noqa: E402

# ИМЯ ПРОСИТЕЛЯ — В ФОРМЕ, КОТОРУЮ ПРИНИМАЮТ ХОСТЫ КНИГ: Pressbooks Rebus
# отвечает 403 на голое имя «genesis-corpus shelf_open (…)» и пропускает
# ту же подпись в общепринятой форме называющих себя ботов
# «Mozilla/5.0 (compatible; имя; контакт)». Имя и контакт те же.
UA = "Mozilla/5.0 (compatible; genesis-corpus shelf_open; contact: luxquant@gst.st)"
# Мы гости на чужом сервере: один поток, пауза между запросами, кэш.
ПАУЗА = 0.5
УЗЛЫ = КОРЕНЬ / "reports" / "pending-manifest-open.json"
# ЛИЦЕНЗИЯ КОРПУСА — CC BY 4.0 (LICENSE-DATA); совместима с ней лишь CC BY
# любой версии: «by/» без «-nc», «-sa», «-nd». Адрес лицензии у всех трёх
# источников один — creativecommons.org, — по нему она и узнаётся.
СВОБОДНАЯ = re.compile(r"creativecommons\.org/licenses/by/(\d\.\d)")
ИСТОЧНИК = "free-license"
OPENSTAX = "https://openstax.org"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
XLINK = "{http://www.w3.org/1999/xlink}href"
ДОРОГИ = ("pressbooks", "openstax", "europepmc")


class ОтказПолки(Exception):
    """Источник не отдал книгу тем, чем она объявлена."""


class Книга:
    """Объявление одной книги дороги — и ничего сверх объявленного."""

    def __init__(self, имя, тема, плотность, издано, заглавие, автор,
                 издатель, лицензия, происхождение, дорога, язык="en",
                 сайт=None, uuid=None, версия=None, главы=(), части=(),
                 запрос=None, источник=ИСТОЧНИК):
        self.имя = имя
        # ИСТОЧНИК ПО ДОГОВОРУ: издано до рубежа машины — free-license;
        # не раньше рубежа — только named-author с названным человеком.
        self.источник = источник
        self.тема = тема
        self.плотность = плотность
        self.издано = издано
        self.заглавие = заглавие
        self.автор = автор
        self.издатель = издатель
        self.лицензия = лицензия
        self.происхождение = происхождение
        self.дорога = дорога
        self.язык = язык
        self.сайт = сайт            # Pressbooks: корень книги
        self.uuid = uuid            # OpenStax: книга в архиве…
        self.версия = версия        # …и её пришпиленная версия
        self.главы = главы          # OpenStax: номера глав; пусто — все
        self.части = части          # Pressbooks: начала заглавий частей
        self.запрос = запрос        # Europe PMC: запрос поиска


# ЖУРНАЛЫ НАЗВАНЫ ПОИМЁННО, А НЕ ВЫБРАНЫ РЕЙТИНГОМ: те, чьи обзоры по
# мозгу и сознанию лежат в Europe PMC под CC BY полным текстом. Frontiers
# (586 + 255 обзоров на тот же запрос) не взяты: свод в четыре раза
# больше при рецензии слабее — полка растёт прожитым, а не объёмом.
ЖУРНАЛЫ = ("PLoS Biol", "Elife", "Philos Trans R Soc Lond B Biol Sci",
           "Neurosci Conscious", "Trends Cogn Sci", "Neuron", "Nat Commun",
           "PLoS Comput Biol", "Cortex", "Neuroimage", "Cognition",
           "Behav Brain Sci")
# СЛОВА ЗАГЛАВИЙ — три слова владельца (мозг, познание, сознание) и их
# ближайшие имена в языке журналов.
СЛОВА = ("consciousness", "conscious", "awareness", "mind", "cognition",
         "cognitive", "memory", "attention", "perception", "learning",
         "language", "decision", "representation", "inference",
         "prediction", "predictive", "brain", "neural", "neuron")
# ОКНО ЛЕТ: до рубежа машины; нижний край — год, с которого журналы
# Elsevier и Royal Society выкладывают CC BY.
ОКНО = (2010, shelf_kinds.РУБЕЖ_МАШИНЫ - 1)


def запрос_обзоров():
    return ('(LICENSE:"cc by") AND (OPEN_ACCESS:y) AND (HAS_FT:y) AND '
            '(PUB_TYPE:"review") AND '
            f'(FIRST_PDATE:[{ОКНО[0]}-01-01 TO {ОКНО[1]}-12-31]) AND ('
            + " OR ".join(f'JOURNAL:"{ж}"' for ж in ЖУРНАЛЫ) + ") AND ("
            + " OR ".join(f'TITLE:"{с}"' for с in СЛОВА) + ")")


# NEUROSCIENCE OF CONSCIOUSNESS — ВЕСЬ ЖУРНАЛ, КРОМЕ ОБЗОРОВ: обзоры его уже
# лежат в своде обзоров, и второй запрос дополняет первый по построению
# (NOT review), а не по списку — вторая копия статьи невозможна.
ЖУРНАЛ_СОЗНАНИЯ = "Neurosci Conscious"
НАЧАЛО_ЖУРНАЛА_СОЗНАНИЯ = 2015


def запрос_журнала_сознания():
    return ('(LICENSE:"cc by") AND (OPEN_ACCESS:y) AND (HAS_FT:y) AND '
            f'(JOURNAL:"{ЖУРНАЛ_СОЗНАНИЯ}") AND (FIRST_PDATE:'
            f'[{НАЧАЛО_ЖУРНАЛА_СОЗНАНИЯ}-01-01 TO {ОКНО[1]}-12-31]) '
            'AND NOT (PUB_TYPE:"review")')


OPENSTAX_АВТОРЫ = "OpenStax, Rice University; senior contributing authors "
ПОЛКА = (
    # OPENSTAX — ОТСТАВЛЕННЫЕ ПЕРВЫЕ ИЗДАНИЯ ПОД CC BY 4.0 (см. шапку).
    # Год «издано» — publish_date издателя (CMS openstax.org); версия —
    # defaultVersion архива на день замера, чтобы всякий мог повторить
    # обход и сличить. Старшие авторы — из предисловия каждой книги.
    Книга("openstax_psychology", "психология", "трактат", 2014,
          "Psychology (1st edition, retired)",
          OPENSTAX_АВТОРЫ + "Rose M. Spielman (content lead), Kathryn "
          "Dumper, William Jenkins, Arlene Lacombe, Marilyn Lovett, Marion "
          "Perlmutter", "OpenStax", "CC BY 4.0",
          f"{OPENSTAX}/details/books/psychology", "openstax",
          uuid="4abf04bf-93a0-45c3-9cbc-2cefd46e68cc", версия="8993bfc"),
    Книга("openstax_biology_nervous", "нейронаука", "трактат", 2016,
          "Biology (1st edition, retired), chapters 35–36: The Nervous "
          "System; Sensory Systems",
          OPENSTAX_АВТОРЫ + "Yael Avissar, Jung Choi, Jean DeSaix, Vladimir "
          "Jurukovski, Robert Wise, Connie Rye", "OpenStax", "CC BY 4.0",
          f"{OPENSTAX}/details/books/biology", "openstax",
          uuid="185cbf87-c72e-48f5-b51e-f14f21b5eabd", версия="e989ec3",
          главы=(35, 36)),
    Книга("openstax_anatomy_nervous", "нейронаука", "трактат", 2013,
          "Anatomy and Physiology (1st edition, retired), chapters 12–16: "
          "The Nervous System and Nervous Tissue; Anatomy of the Nervous "
          "System; The Somatic Nervous System; The Autonomic Nervous "
          "System; The Neurological Exam",
          OPENSTAX_АВТОРЫ + "J. Gordon Betts, Peter Desaix, Eddie Johnson, "
          "Jody E. Johnson, Oksana Korol, Dean Kruse, Brandon Poe, James A. "
          "Wise, Mark Womble, Kelly A. Young", "OpenStax", "CC BY 4.0",
          f"{OPENSTAX}/details/books/anatomy-and-physiology", "openstax",
          uuid="14fb4ad7-39a1-4eee-ab6e-3ef2482e3e22", версия="ccce780",
          главы=(12, 13, 14, 15, 16)),
    # REBUS COMMUNITY «INTRODUCTION TO PHILOSOPHY» — CC BY 4.0 по metadata
    # Pressbooks, авторы глав названы в ней же и встают под заголовком
    # каждой главы (атрибуция CC BY). Взяты два тома о сознании и
    # познании; «Logic», «Ethics», «Philosophy of Religion», «Aesthetics»
    # той же серии и той же лицензии лежат за словом владельца.
    Книга("rebus_philosophy_of_mind", "философия", "трактат", 2019,
          "Introduction to Philosophy: Philosophy of Mind",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-of-mind/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-of-mind"),
    Книга("rebus_epistemology", "философия познания", "трактат", 2021,
          "Introduction to Philosophy: Epistemology",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-epistemology/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-epistemology"),
    # ECAMPUSONTARIO — Ju, «Neuroscience: Canadian 1st Edition» (2018 по
    # записи библиотеки eCampusOntario), CC BY 4.0 по metadata Pressbooks.
    # Часть 1 — дословно OpenStax A&P и не берётся (см. шапку).
    Книга("ecampus_ju_neuroscience", "нейронаука", "трактат", 2018,
          "Neuroscience: Canadian 1st Edition Open Textbook, units 2–4: "
          "Neurodegeneration; Fundamental Neuroscience Techniques; Emergent "
          "Topics in Neuroscience", "William Ju, University of Toronto, "
          "with student contributors", "eCampusOntario", "CC BY 4.0",
          "https://ecampusontario.pressbooks.pub/neuroscience/",
          "pressbooks", сайт="https://ecampusontario.pressbooks.pub/neuroscience",
          части=("Unit 2", "Unit 3", "Unit 4")),
    # EUROPE PMC — обзоры когнитивной нейронауки и науки о сознании из
    # двенадцати журналов, каждый под CC BY по своему XML; авторы, журнал,
    # год и PMCID встают строкой под заглавием каждой статьи.
    Книга("europepmc_cognition_reviews", "нейронаука", "статья", ОКНО[1],
          "Reviews in cognitive neuroscience and consciousness science, "
          f"{ОКНО[0]}–{ОКНО[1]}", "authors named at each article",
          "Europe PMC (journals named in the query)", "CC BY",
          "https://europepmc.org/", "europepmc", запрос=запрос_обзоров()),
    # ВТОРОЙ ЗАКАЗ (02.09, слово лида): остальные тома серии Rebus — той же
    # дорогой, по строке объявления на том.
    Книга("rebus_logic", "логика", "трактат", 2020,
          "Introduction to Philosophy: Logic",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-logic/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-logic"),
    Книга("rebus_ethics", "философия", "трактат", 2019,
          "Introduction to Philosophy: Ethics",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-ethics/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-ethics"),
    Книга("rebus_philosophy_of_religion", "философия", "трактат", 2020,
          "Introduction to Philosophy: Philosophy of Religion",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-of-religion/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-of-religion"),
    Книга("rebus_aesthetics", "философия", "трактат", 2021,
          "Introduction to Philosophy: Aesthetic Theory and Practice",
          "authors named at each chapter", "Rebus Community", "CC BY 4.0",
          "https://press.rebus.community/intro-to-phil-aesthetics/",
          "pressbooks", сайт="https://press.rebus.community/intro-to-phil-aesthetics"),
    # OPENSTAX POLAND «PSYCHOLOGIA» — польская адаптация Psychology 2e (2020).
    # Лицензия CC BY 4.0 держится по всем свидетельствам издателя на
    # 02.09.2026: CMS openstax.org, JSON книги в архиве (deed.pl), предисловие
    # («Creative Commons Uznanie autorstwa 4.0 Międzynarodowe»), LICENSE
    # репозитория osbooks-psychologia (не перелицензирован). Год — publish_date
    # издателя. Твёрцы польского издания — из предисловия («Twórcy Psychologii
    # wydanej przez OpenStax Poland»); первый мир прозы на польском.
    Книга("openstax_psychologia_pl", "психология", "трактат", 2020,
          "Psychologia (polska adaptacja Psychology 2e)",
          "OpenStax Poland; autor rozdziału: Joanna Czarnota-Bojarska; redaktorzy "
          "i autorzy uzupełnień: Ewa Czerniawska, Agata Kudlik, Dorota Karwowska, "
          "Agnieszka Małkowska-Szkutnik; original senior authors Rose M. Spielman, "
          "William J. Jenkins, Marilyn D. Lovett", "OpenStax Poland", "CC BY 4.0",
          f"{OPENSTAX}/details/books/psychologia-polska", "openstax", язык="pl",
          uuid="728df0bb-e07f-489d-91e3-4734a5932f92", версия="0708931"),
    Книга("europepmc_consciousness_articles", "нейронаука", "статья", ОКНО[1],
          f"Neuroscience of Consciousness, all articles but reviews, "
          f"{НАЧАЛО_ЖУРНАЛА_СОЗНАНИЯ}–{ОКНО[1]}", "authors named at each article",
          "Europe PMC (Oxford University Press journal)", "CC BY",
          "https://europepmc.org/", "europepmc", запрос=запрос_журнала_сознания()),
    # ИСПАНСКИЕ ИЗДАНИЯ OPENSTAX (третий заказ 02.09, слово владельца: все
    # языки с избытком). Четыре свидетельства издателя на 02.09.2026:
    # «Física universitaria» тт. 1–3 — CC BY 4.0 везде (LICENSE репозитория
    # osbooks-fisica-universitaria-bundle от 2021-10-27, JSON книги в архиве,
    # предисловие «Creative Commons Atribución 4.0 Internacional (CC BY 4.0)»,
    # CMS у тома 1; у томов 2–3 поле лицензии CMS пусто — не BY-NC-SA);
    # издано 2021 (publish_date издателя). «Precálculo 2ed» и «Química 2ed»
    # — CC BY 4.0 везде, но изданы издателем в 2022 (2022-05-18, 2022-06-02):
    # по договору полки текст не раньше рубежа машины берётся лишь с
    # названными людьми — источник named-author, авторы из предисловий.
    # «Cálculo» тт. 1–3 — BY-NC-SA везде (не берётся); «Química: Comenzando
    # con los átomos 2ed» — та же «Química» с переставленными главами
    # (вторая копия несёт ноль); «Biología» по-испански у издателя нет.
    Книга("openstax_fisica_1_es", "естествознание", "трактат", 2021,
          "Física universitaria, volumen 1 (Mecánica, ondas, acústica)",
          "Samuel J. Ling (Truman State University), Jeff Sanny (Loyola "
          "Marymount University), William Moebs; edición en español OpenStax",
          "OpenStax", "CC BY 4.0", f"{OPENSTAX}/details/books/física-universitaria-volumen-1",
          "openstax", язык="es", uuid="175c88b6-f89b-4eba-9514-bc45e2139a1d",
          версия="9281eb6"),
    Книга("openstax_fisica_2_es", "естествознание", "трактат", 2021,
          "Física universitaria, volumen 2 (Termodinámica, electricidad y magnetismo)",
          "Samuel J. Ling, Jeff Sanny, William Moebs; edición en español OpenStax",
          "OpenStax", "CC BY 4.0", f"{OPENSTAX}/details/books/física-universitaria-volumen-2",
          "openstax", язык="es", uuid="da02605d-6d69-447c-a9b9-caf06dc4f413",
          версия="9281eb6"),
    Книга("openstax_fisica_3_es", "естествознание", "трактат", 2021,
          "Física universitaria, volumen 3 (Óptica y física moderna)",
          "Samuel J. Ling, Jeff Sanny, William Moebs; edición en español OpenStax",
          "OpenStax", "CC BY 4.0", f"{OPENSTAX}/details/books/física-universitaria-volumen-3",
          "openstax", язык="es", uuid="b647a9b9-7631-45a1-a8e7-5acc3a44fc01",
          версия="9281eb6"),
    Книга("openstax_precalculo_es", "математика", "трактат", 2022,
          "Precálculo 2ed", "Jay Abramson (Arizona State University) con autores "
          "colaboradores nombrados en el prefacio; edición en español OpenStax 2022",
          "OpenStax", "CC BY 4.0", f"{OPENSTAX}/details/books/precálculo-2ed",
          "openstax", язык="es", uuid="52f5163f-a7e1-4545-b0fa-8001df262ca9",
          версия="ea84f53", источник="named-author"),
    Книга("openstax_quimica_es", "естествознание", "трактат", 2022,
          "Química 2ed", "Paul Flowers (University of North Carolina at Pembroke), "
          "Klaus Theopold (University of Delaware), Richard Langley (Stephen F. "
          "Austin State University), William R. Robinson; edición en español OpenStax 2022",
          "OpenStax", "CC BY 4.0", f"{OPENSTAX}/details/books/química-2ed",
          "openstax", язык="es", uuid="462aa3f1-d65d-4cd9-a5ee-3214f95769b8",
          версия="9b2eeca", источник="named-author"),
    # ПОЛЬСКАЯ ФИЗИКА OPENSTAX POLAND (четвёртый заказ 03.09): «Fizyka dla
    # szkół wyższych» тт. 1–3 — адаптация University Physics, CC BY 4.0 по
    # четырём свидетельствам на 03.09.2026 (CMS: Creative Commons Attribution
    # License 4.0, издано 2017-12-05 и 2018-06-11; LICENSE репозитория
    # osbooks-fizyka-bundle «Attribution 4.0 International» от 2021-03-18 без
    # правок; JSON книг в архиве by/4.0/deed.pl; предисловие «Creative Commons
    # Uznanie autorstwa 4.0 Międzynarodowe»). Переводчики и авторы адаптации
    # названы в предисловии («Tłumacze i autorzy adaptacji»). Математики и
    # химии у OpenStax Poland нет: кроме физики и психологии в CMS лишь
    # «Mikroekonomia» (2022) и «Makroekonomia» (2023) — не наш ряд.
    Книга("openstax_fizyka_1_pl", "естествознание", "трактат", 2017,
          "Fizyka dla szkół wyższych, tom 1 (Mechanika, fale, akustyka)",
          "OpenStax Poland (fundacja Katalyst Education); tłumacze i autorzy "
          "adaptacji nazwani w przedmowie (Adam Bednorz, Anna Błachowicz, Tomasz "
          "Błachowicz, Beata Bochentyn, Juliusz P. Braun, Bartosz Brzostowski i "
          "inni); original senior authors Samuel J. Ling, Jeff Sanny, William Moebs",
          "OpenStax Poland", "CC BY 4.0", f"{OPENSTAX}/details/books/fizyka-dla-szkół-wyższych-tom-1",
          "openstax", язык="pl", uuid="4eaa8f03-88a8-485a-a777-dd3602f6c13e",
          версия="0cd082f"),
    Книга("openstax_fizyka_2_pl", "естествознание", "трактат", 2018,
          "Fizyka dla szkół wyższych, tom 2 (Termodynamika, elektryczność i magnetyzm)",
          "OpenStax Poland (fundacja Katalyst Education); tłumacze i autorzy "
          "adaptacji nazwani w przedmowie; original senior authors Samuel J. Ling, "
          "Jeff Sanny, William Moebs",
          "OpenStax Poland", "CC BY 4.0", f"{OPENSTAX}/details/books/fizyka-dla-szkół-wyższych-tom-2",
          "openstax", язык="pl", uuid="16ab5b96-4598-45f9-993c-b8d78d82b0c6",
          версия="0cd082f"),
    Книга("openstax_fizyka_3_pl", "естествознание", "трактат", 2018,
          "Fizyka dla szkół wyższych, tom 3 (Optyka i fizyka współczesna)",
          "OpenStax Poland (fundacja Katalyst Education); tłumacze i autorzy "
          "adaptacji nazwani w przedmowie; original senior authors Samuel J. Ling, "
          "Jeff Sanny, William Moebs",
          "OpenStax Poland", "CC BY 4.0", f"{OPENSTAX}/details/books/fizyka-dla-szkół-wyższych-tom-3",
          "openstax", язык="pl", uuid="bb62933e-f20a-4ffc-90aa-97b36c296c3e",
          версия="0cd082f"),
    # ОТВЕРГНУТЫЕ, И ПОЧЕМУ (замер 02.09.2026):
    # * OpenStax «Psychology 2e», «Biology 2e», «Anatomy and Physiology
    #   2e», «Introduction to Philosophy», «Introduction to Behavioral
    #   Neuroscience», «Concepts of Biology» — CC BY-NC-SA 4.0 (см. шапку).
    # * Levy, «Psychology: The Science of Human Potential» (BCcampus,
    #   CC BY 4.0) — хост pressbooks.bccampus.ca закрыт проверкой
    #   Cloudflare для всякого не-браузера, и честного пути к тексту нет;
    #   зеркало Marshall Digital Scholar лежит лишь PDF — дороги PDF у
    #   полки нет.
    # * Stevens, Stamp, LeBlanc, «Introduction to Psychology &
    #   Neuroscience» (Dalhousie, CC BY 4.0) — сшита из OpenStax 2e, Noba
    #   и Саскачевана (последние два CC BY-NC-SA): права смешаны, спорное
    #   не берём.
    # * Malavanti, «Cognition» (Baylor) и «Cognitive Foundations» —
    #   CC BY-NC-SA. Noba Project, Lumen, Stangor, Wikibooks — BY-NC-SA
    #   или BY-SA.
    # * OpenStax «Psychologia» (польский перевод 2e, 2020) — CC BY 4.0 и
    #   по сей день (репозиторий osbooks-psychologia не перелицензирован):
    #   годится, но по-польски; ждёт слова владельца о польской прозе.
)


def судить_объявление():
    """Дорога сверяет СВОЁ объявление раньше, чем тронет источник."""
    беды = []
    for к in ПОЛКА:
        if к.тема not in shelf_kinds.ТЕМЫ:
            беды.append(f"{к.имя}: тема «{к.тема}» вне набора")
        if к.плотность not in shelf_kinds.ПЛОТНОСТИ:
            беды.append(f"{к.имя}: плотность «{к.плотность}» вне набора")
        if к.источник not in shelf_kinds.ИСТОЧНИКИ:
            беды.append(f"{к.имя}: источник «{к.источник}» вне набора")
        if к.источник == "free-license" and к.издано >= shelf_kinds.РУБЕЖ_МАШИНЫ:
            беды.append(f"{к.имя}: издано {к.издано} — не раньше рубежа "
                        f"машины {shelf_kinds.РУБЕЖ_МАШИНЫ}, а источник free-license")
        if к.источник == "named-author" and not к.автор.strip():
            беды.append(f"{к.имя}: источник named-author, а автор не назван")
        if к.язык not in shelf_kinds.ЯЗЫКИ:
            беды.append(f"{к.имя}: язык «{к.язык}» вне набора")
        if not re.fullmatch(r"CC BY(?: \d\.\d)?", к.лицензия):
            беды.append(f"{к.имя}: лицензия «{к.лицензия}» не CC BY")
        if к.дорога not in ДОРОГИ:
            беды.append(f"{к.имя}: дорога «{к.дорога}» неизвестна")
    имена = collections.Counter(к.имя for к in ПОЛКА)
    беды += [f"имя «{и}» объявлено дважды" for и, n in имена.items() if n > 1]
    return беды


def взять(адрес, файл):
    """Ответ источника — из кэша, а если его нет, одним запросом с паузой."""
    if файл.is_file():
        return файл.read_bytes()
    з = urllib.request.Request(адрес, headers={"User-Agent": UA})
    тело = urllib.request.urlopen(з, timeout=180).read()
    файл.parent.mkdir(parents=True, exist_ok=True)
    файл.write_bytes(тело)
    time.sleep(ПАУЗА)
    return тело


def лицензия_источника(адрес_или_текст):
    """«CC BY x.y», если источник назвал совместимую лицензию, иначе None."""
    м = СВОБОДНАЯ.search(адрес_или_текст or "")
    return f"CC BY {м.group(1)}" if м else None


def сверить_лицензию(книга, названная):
    лиц = лицензия_источника(названная)
    if не_та_лицензия(книга, лиц):
        raise ОтказПолки(f"источник называет лицензию «{названная or '—'}», "
                         f"объявлено {книга.лицензия}")
    return лиц


def не_та_лицензия(книга, лиц):
    """Объявлено «CC BY» — любая версия; «CC BY 4.0» — ровно она."""
    if лиц is None:
        return True
    return книга.лицензия != "CC BY" and лиц != книга.лицензия


# ---------------------------------------------------------------- HTML
ПУСТЫЕ = {"br", "img", "hr", "meta", "link", "input", "source", "wbr",
          "col", "area", "base", "embed", "param", "track"}
СНЯТЬ_ТЕГ = {"figure", "figcaption", "table", "script", "style", "iframe",
             "template", "button", "svg", "math", "nav", "form", "audio",
             "video", "object", "noscript", "select", "textarea", "canvas",
             "map", "head", "title"}
ЗАГОЛОВКИ = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
ПУНКТЫ = {"li", "dt", "dd"}
БЛОЧНЫЕ = {"p", "div", "section", "article", "header", "footer", "aside",
           "blockquote", "dl", "ul", "ol", "pre", "center", "details",
           "summary", "main", "body", "html"} | set(ЗАГОЛОВКИ) | ПУНКТЫ
СТРОЧНЫЕ = {"span", "a", "em", "strong", "i", "b", "sup", "sub", "small",
            "abbr", "cite", "code", "q", "u", "s", "var", "big", "tt",
            "font", "time", "mark", "kbd", "label", "dfn", "bdi", "ruby"}
# КЛЕЙМА СЛУЖЕБНЫХ ПОДДЕРЕВЬЕВ — ровно те лексемы класса, data-type и
# роли, которыми источники метят свой аппарат; сравнение по целой
# лексеме, ибо «glossary» как подстрока съел бы «glossary-term» — слово
# самого текста (Rebus помечает им термин в предложении).
СЛУЖЕБНЫЕ_КЛЕЙМА = {
    # Pressbooks
    "footnotes", "wp-caption", "learning-objectives", "key-takeaways",
    "exercises", "textbox--learning-objectives", "textbox--key-takeaways",
    "textbox--exercises", "screen-reader-text", "h5p-content", "h5p-iframe",
    "media-attributions", "interactive-content",
    # OpenStax (архив): рисунок с подписью, оглавление главы, заглавие
    # страницы (стоит и в дереве книги), цели раздела, глоссарий,
    # упражнения, уравнения, врезки-указатели наружу и вопросы к рисунку
    "os-figure", "os-caption-container", "os-chapter-outline",
    "link-to-learning", "interactive", "interactive-embedded-homework",
    "interactive-embedded-reading", "art-connection", "visual-connection",
    "chapter-objectives", "os-eoc", "os-index", "os-reference",
    # OpenStax по-испански и по-польски: врезка «Compruebe lo aprendido»
    # (упражнение с решением), врезка встроенного видео, номер уравнения
    # (сама формула — текст, см. MathML→TeX ниже).
    "check-understanding", "media-2", "os-equation-number",
    "os-chapter-objectives", "os-chapter-objective",
    "data-type:abstract", "data-type:glossary", "data-type:exercise",
    "data-type:document-title", "data-type:media",
    "data-type:footnote-refs", "role:doc-footnote", "role:doc-endnotes",
}
ВРЕЗКИ = {"textbox", "data-type:note"}


class Разбор(html.parser.HTMLParser):
    """Абзацы, заголовки и пункты страницы; служебные поддеревья не читаются."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.куски = []          # (текст, уровень, вид)
        self.текущий = []
        self.уровень = 0
        self.вид = "абзац"
        self.глубина = 0
        self.вон_с = None
        self.в_ссылке = None
        self.пункты = []         # глубины открытых пунктов списка
        self.врезки = []         # [маркер, глубина, ссылка наружу]

    @staticmethod
    def _клейма(свойства):
        д = dict(свойства)
        вон = set((д.get("class") or "").split())
        for имя in ("data-type", "role"):
            if д.get(имя):
                вон.add(f"{имя}:{д[имя]}")
        return вон, д.get("href") or ""

    def handle_starttag(self, тег, свойства):
        if тег in ПУСТЫЕ:
            if тег == "br" and self.вон_с is None:
                self.текущий.append(" ")
            return
        self.глубина += 1
        if self.вон_с is not None:
            return
        клейма, href = self._клейма(свойства)
        if (тег in СНЯТЬ_ТЕГ or клейма & СЛУЖЕБНЫЕ_КЛЕЙМА
                or (тег == "sup" and self.в_ссылке is not None)):
            if тег not in СТРОЧНЫЕ:
                self._закрыть()
            self.вон_с = self.глубина
            return
        if клейма & ВРЕЗКИ:
            # ГРАНИЦЫ ВРЕЗКИ ОСТАЮТСЯ В КУСКАХ МЕТКАМИ: рубрика аппарата,
            # начатая внутри врезки («Chapter Objectives» у A&P), кончается
            # с врезкой, а не съедает страницу до следующего заголовка.
            self._закрыть()
            self.врезки.append([len(self.куски), self.глубина, False])
            self.куски.append(("", 0, "начало"))
        if тег == "a":
            if href.startswith("http") and self.врезки:
                self.врезки[-1][2] = True
            if self.в_ссылке is None:
                self.в_ссылке = self.глубина
        if тег in ЗАГОЛОВКИ:
            self._закрыть()
            self.уровень, self.вид = ЗАГОЛОВКИ[тег], "заголовок"
        elif тег in ПУНКТЫ:
            self._закрыть()
            self.пункты.append(self.глубина)
            self.вид = "пункт"
        elif тег in БЛОЧНЫЕ:
            self._закрыть()

    def handle_endtag(self, тег):
        if тег in ПУСТЫЕ:
            return
        if self.вон_с is not None:
            # ГЛУБИНА СЧИТАЕТСЯ ПО ВСЕМ ТЕГАМ (шрам shelf_fetch).
            if self.глубина <= self.вон_с:
                self.вон_с = None
            self.глубина = max(0, self.глубина - 1)
            return
        if тег in БЛОЧНЫЕ:
            self._закрыть()
        if self.пункты and self.пункты[-1] == self.глубина:
            self.пункты.pop()
        if self.врезки and self.врезки[-1][1] == self.глубина:
            маркер, _, наружу = self.врезки.pop()
            if наружу:
                del self.куски[маркер:]
            else:
                self.куски.append(("", 0, "конец"))
        if self.в_ссылке == self.глубина:
            self.в_ссылке = None
        self.глубина = max(0, self.глубина - 1)

    def handle_data(self, данные):
        if self.вон_с is None:
            self.текущий.append(данные)

    def _закрыть(self):
        текст = " ".join("".join(self.текущий).split())
        self.текущий = []
        if текст:
            self.куски.append((текст, self.уровень, self.вид))
        self.уровень = 0
        self.вид = "пункт" if self.пункты else "абзац"


def разобрать(страница, счёт=None):
    р = Разбор()
    р.feed(формулы_в_tex(страница, счёт if счёт is not None else collections.Counter()))
    р._закрыть()
    return р.куски


# ------------------------------------------------------- ФОРМУЛЫ MathML
# ФОРМУЛА ОСТАЁТСЯ ФОРМУЛОЙ, И ЯЗЫК ЕЁ — TeX (закон дороги TeX). Архив
# OpenStax несёт формулы MathML без TeX-аннотации («Física universitaria»:
# 98 формул в абзацах и 26 выключных на одну главу); перевод — ПРАВИЛОМ по
# элементам разметки (дробь, степень, индекс, корень, стрелка над буквой,
# таблица), знаки — таблицей соответствий, греческие буквы — макросами.
# Что правило не знает, отдаётся словами узла и считается вслух; блок, не
# разобранный как XML, — тоже.
ЗНАКИ_TEX = {
    "×": r"\times", "·": r"\cdot", "⋅": r"\cdot", "−": "-", "–": "-", "±": r"\pm",
    "∓": r"\mp", "≤": r"\le", "≥": r"\ge", "≠": r"\ne", "≈": r"\approx",
    "≡": r"\equiv", "∝": r"\propto", "→": r"\to", "←": r"\leftarrow",
    "↔": r"\leftrightarrow", "⇒": r"\Rightarrow", "⇐": r"\Leftarrow",
    "⇔": r"\Leftrightarrow", "∞": r"\infty", "∑": r"\sum", "∏": r"\prod",
    "∫": r"\int", "∬": r"\iint", "∮": r"\oint", "∂": r"\partial", "∇": r"\nabla",
    "∈": r"\in", "∉": r"\notin", "⊂": r"\subset", "⊆": r"\subseteq", "⊃": r"\supset",
    "∪": r"\cup", "∩": r"\cap", "∅": r"\emptyset", "∘": r"\circ", "°": r"^\circ",
    "′": "'", "″": "''", "⋯": r"\cdots", "…": r"\ldots", "⋮": r"\vdots", "∼": r"\sim",
    "≃": r"\simeq", "≅": r"\cong", "≪": r"\ll", "≫": r"\gg", "∀": r"\forall",
    "∃": r"\exists", "¬": r"\neg", "∧": r"\wedge", "∨": r"\vee", "⊥": r"\perp",
    "∥": r"\parallel", "∠": r"\angle", "ℏ": r"\hbar", "ℓ": r"\ell", "∗": "*",
    "⟨": r"\langle", "⟩": r"\rangle", "‖": r"\|", "{": r"\{", "}": r"\}",
    "√": r"\surd", "∆": r"\Delta", "\u2061": "", "\u2062": "", "\u2063": "",
    "\u2064": "", "\u00a0": " ", "\u200b": "", "%": r"\%", "&": r"\&", "#": r"\#",
}
ГРЕЧЕСКИЕ = dict(zip("αβγδεζηθικλμνξοπρστυφχψω",
                     "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda "
                     "mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega".split()))
ГРЕЧЕСКИЕ.update({"Γ": "Gamma", "Δ": "Delta", "Θ": "Theta", "Λ": "Lambda", "Ξ": "Xi",
                  "Π": "Pi", "Σ": "Sigma", "Φ": "Phi", "Ψ": "Psi", "Ω": "Omega",
                  "ϵ": "varepsilon", "ϕ": "varphi", "ϑ": "vartheta", "ϱ": "varrho",
                  "ς": "varsigma", "ϖ": "varpi"})
ФУНКЦИИ = {"sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan",
           "sinh", "cosh", "tanh", "coth", "log", "ln", "exp", "lim", "max", "min",
           "det", "sup", "inf", "arg", "deg", "dim", "gcd", "hom", "ker", "lg"}
# Испанская и польская запись функций — в имена TeX.
ФУНКЦИИ_ЯЗЫКА = {"sen": "sin", "tg": "tan", "ctg": "cot", "arcsen": "arcsin",
                 "arctg": "arctan", "cosec": "csc", "cotg": "cot", "sh": "sinh",
                 "ch": "cosh", "th": "tanh"}
НАДПИСИ = {"→": "vec", "⇀": "vec", "⃗": "vec", "¯": "bar", "‾": "bar", "―": "bar",
           "^": "hat", "ˆ": "hat", "˙": "dot", "¨": "ddot", "~": "tilde", "˜": "tilde",
           "̃": "tilde", "̂": "hat", "̇": "dot", "̈": "ddot", "̄": "bar", "→": "vec"}
БОЛЬШИЕ = {r"\sum", r"\prod", r"\int", r"\iint", r"\oint", r"\lim", r"\max",
           r"\min", r"\sup", r"\inf"}
МАТЕМАТИКА = re.compile(r"<math\b[^>]*>.*?</math>", re.S)
АННОТАЦИЯ = re.compile(r"<annotation(?:-xml)?\b[^>]*>.*?</annotation(?:-xml)?>", re.S)
# Именованная сущность HTML, не известная XML, — в знак.
СУЩНОСТЬ = re.compile(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)[A-Za-z][A-Za-z0-9]*;")


def _tex_знаки(текст):
    return "".join(ЗНАКИ_TEX.get(з, ("\\" + ГРЕЧЕСКИЕ[з] + " ") if з in ГРЕЧЕСКИЕ else з)
                   for з in текст)


def tex_узла(эл, счёт):
    """TeX узла MathML — по правилам разметки; неизвестное — словами."""
    и = _имя(эл)
    дети = list(эл)

    def т(д):
        return tex_узла(д, счёт)
    if и in ("annotation", "annotation-xml", "mphantom"):
        return ""
    if и == "semantics":
        return т(дети[0]) if дети else ""
    if и == "mi":
        слово = (эл.text or "").strip()
        if len(слово) > 1 and слово.isalpha() and слово.isascii():
            слово = ФУНКЦИИ_ЯЗЫКА.get(слово, слово)
            return ("\\" + слово + " ") if слово in ФУНКЦИИ else r"\mathrm{" + слово + "}"
        слово = _tex_знаки(слово)
        return (r"\mathbf{" + слово + "}") if эл.get("mathvariant") == "bold" else слово
    if и == "mn":
        return (эл.text or "").strip()
    if и == "mo":
        return " " + _tex_знаки((эл.text or "").strip()) + " "
    if и == "mtext":
        слова = " ".join((эл.text or "").replace("{", "").replace("}", "").split())
        return (r"\text{" + слова + "}") if слова else " "
    if и == "mspace":
        return " "
    if и == "mfrac" and len(дети) >= 2:
        return (т(дети[0]) + "/" + т(дети[1])) if эл.get("bevelled") == "true" \
            else r"\frac{" + т(дети[0]) + "}{" + т(дети[1]) + "}"
    if и == "msup" and len(дети) >= 2:
        return "{" + т(дети[0]) + "}^{" + т(дети[1]) + "}"
    if и == "msub" and len(дети) >= 2:
        return "{" + т(дети[0]) + "}_{" + т(дети[1]) + "}"
    if и == "msubsup" and len(дети) >= 3:
        return "{" + т(дети[0]) + "}_{" + т(дети[1]) + "}^{" + т(дети[2]) + "}"
    if и == "msqrt":
        return r"\sqrt{" + "".join(т(д) for д in дети) + "}"
    if и == "mroot" and len(дети) >= 2:
        return r"\sqrt[" + т(дети[1]) + "]{" + т(дети[0]) + "}"
    if и in ("mover", "munder", "munderover") and len(дети) >= 2:
        основа = т(дети[0])
        if и == "mover":
            знак = "".join(дети[1].itertext()).strip()
            if знак in НАДПИСИ:
                return "\\" + НАДПИСИ[знак] + "{" + основа + "}"
            return r"\overset{" + т(дети[1]) + "}{" + основа + "}"
        низ = т(дети[1])
        if и == "munder":
            return (основа.strip() + "_{" + низ + "}") if основа.strip() in БОЛЬШИЕ \
                else r"\underset{" + низ + "}{" + основа + "}"
        верх = т(дети[2]) if len(дети) >= 3 else ""
        return (основа.strip() + "_{" + низ + "}^{" + верх + "}") if основа.strip() in БОЛЬШИЕ \
            else r"\overset{" + верх + r"}{\underset{" + низ + "}{" + основа + "}}"
    if и == "mtable":
        ряды = [" & ".join(т(я) for я in ряд if _имя(я) == "mtd")
                for ряд in дети if _имя(ряд) in ("mtr", "mlabeledtr")]
        return r"\begin{matrix} " + r" \\ ".join(ряды) + r" \end{matrix}"
    if и in ("mtr", "mtd", "mlabeledtr"):
        return " ".join(т(д) for д in дети)
    if и == "mfenced":
        о, з = эл.get("open", "("), эл.get("close", ")")
        return (r"\left" + (о or ".") + " " + ", ".join(т(д) for д in дети)
                + r" \right" + (з or "."))
    if и in ("math", "mrow", "mstyle", "mpadded", "menclose", "merror", "maction",
             "mmultiscripts", "mprescripts", "none"):
        return "".join(т(д) for д in дети)
    счёт["неизвестных"] += 1
    return " ".join("".join(эл.itertext()).split())


def tex_из_mathml(блок, счёт):
    """TeX формулы из блока <math>…</math>; блок, не разобранный как XML,
    отдаёт свои слова и считается."""
    блок = СУЩНОСТЬ.sub(lambda м: html.unescape(м.group(0)), АННОТАЦИЯ.sub("", блок))
    try:
        корень = ET.fromstring(блок)
    except ET.ParseError:
        счёт["не разобрано"] += 1
        return " ".join(re.sub(r"<[^>]+>", " ", блок).split())
    tex = " ".join(tex_узла(корень, счёт).split())
    return re.sub(r"\s+([_^])", r"\1", tex)


def формулы_в_tex(страница, счёт):
    """Каждый <math> страницы — TeX между долларами: выключная формула —
    «$$ … $$» своей строкой, формула в абзаце — «$…$» в нём."""
    def замена(м):
        блок = м.group(0)
        tex = tex_из_mathml(блок, счёт)
        if not tex:
            return " "
        счёт["формул"] += 1
        return f"\n$$ {tex} $$\n" if 'display="block"' in блок[:200] else f" ${tex}$ "
    return МАТЕМАТИКА.sub(замена, страница)


# ------------------------------------------------------------ ПРАВИЛА
# РУБРИКИ АППАРАТА — заголовки, под которыми учебник и статья держат не
# текст, а аппарат: списки, вопросы, библиографию, конспект. Заголовок
# сверяется целиком, без номера главы и раздела перед ним.
РУБРИКИ = (
    r"references?", r"further readings?", r"bibliography", r"works cited",
    r"(?:media |image |figure )?attributions?", r"(?:chapter )?citations?",
    r"(?:end|foot)?notes", r"glossary", r"key terms", r"key takeaways?",
    r"(?:learning|section|chapter) objectives", r"\w+(?: \w+)? questions?",
    r"exercises?", r"quiz(?:zes)?", r"chapter review", r"(?:section |chapter )?summary",
    r"suggested readings?", r"(?:additional|recommended|external) (?:resources?|readings?|links?)",
    r"about the (?:authors?|contributors?)", r"acknowledge?ments?",
    r"test yourself", r"check your understanding", r"answer key", r"answers",
    r"licens(?:e|ing)(?: and attribution)?(?: information)?", r"version history",
    r"adoption form", r"feedback and suggestions", r"review statement",
    r"accessibility assessment", r"(?:chapter )?outline", r"(?:table of )?contents",
    r"highlights", r"to the (?:instructor|student)s?",
    r"(?:electronic )?supplementary (?:materials?|information|data|figures?|tables?|methods?)",
    r"supporting information", r"funding", r"competing interests",
    r"conflicts? of interest", r"author contributions", r"data availability",
    r"ethics statement", r"abbreviations", r"declarations?", r"index", r"preface",
    r"free response", r"multiple choice",
    # OpenStax Poland: ключевые понятия, итоги, проверь знания, тренируй
    # критическое мышление, развивайся; библиография, указатели, предисловие.
    r"kluczowe pojęcia", r"podsumowanie", r"sprawdź wiedzę", r"ćwicz myślenie krytyczne",
    r"rozwijaj się", r"bibliografia", r"skorowidz(?: \w+)*", r"przedmowa", r"literatura",
    r"podsumowanie rozdziału", r"najważniejsze wzory", r"pytania(?: \w+)*", r"zadania(?: \w+)*",
    r"dodatek \w+", r"odpowiedzi", r"sprawdź, czy rozumiesz", r"cele dydaktyczne",
    # OpenStax по-испански: сводная страница обзора главы (архив её и не
    # отдаёт), ключевые термины и уравнения, итоги, упражнения, задачи,
    # практика, домашняя работа, решения, приложения, указатель.
    r"revisión del capítulo", r"repaso del capítulo", r"términos clave", r"ecuaciones clave",
    r"resumen(?: del capítulo)?", r"ejercicios(?: \w+)*", r"práctica", r"tarea para la casa",
    r"resúmalo todo(?::.*)?", r"referencias", r"soluciones", r"preguntas(?: \w+)*",
    r"problemas(?: \w+)*", r"prefacio", r"índice", r"apéndice \w+", r"compruebe lo aprendido",
    r"objetivos de aprendizaje", r"glosario",
)
РУБРИКА = re.compile(
    r"^(?:(?:chapter|unit|part|section|rozdział|capítulo|unidad|sección)\s+[\dIVX]+[:.]?\s*"
    r"|\d+(?:\.\d+)*\.?\s+|[ivx]+\.\s+)?"
    r"(?:" + "|".join(РУБРИКИ) + r")\s*[:.]?$", re.I)
# ОТСЫЛКА К РИСУНКУ В СКОБКАХ снимается вместе со скобками; предложение
# «Figure 1.2 shows…» — текст, и оно остаётся.
ОТСЫЛКА = re.compile(
    r"\s*\(\s*(?:see\s+|cf\.\s+|also\s+|zob\.\s+|patrz\s+|v[ée]ase\s+|vea\s+|ver\s+|"
    r"consulte\s+)?(?:la\s+|el\s+|las\s+|los\s+)?(?:figures?|figs?\.?|tables?|boxes?|"
    r"videos?|equations?|eqs?\.?|panels?|ilustracj\w*|rysun\w*|tabel\w*|ramk\w*|"
    r"figuras?|tablas?|ecuaci[oó]n(?:es)?|gr[aá]ficos?|cuadros?|im[aá]gen(?:es)?|"
    r"równani\w*|wz[oó]r\w*|wykres\w*)"
    r"\s*[\dA-Za-z][\dA-Za-z.\-–]*(?:\([a-z]\))?"
    r"(?:\s*(?:and|,|;|–|-|&|to|i|oraz|y|e|o|a)\s*(?:la\s+|el\s+)?"
    r"(?:figures?|figs?\.?|tables?|ilustracj\w*|tabel\w*|figuras?|tablas?|ecuaci[oó]n(?:es)?)?\s*"
    r"(?:[\dA-Za-z][\dA-Za-z.\-–]*)?(?:\([a-z]\))?)*\s*\)", re.I)
# ОПУСТЕВШИЕ СКОБКИ: после снятия ссылки на рисунок или номера цитаты в
# них остаются лишь служебные слова — «(see and )», «[ ]», «( )».
ПУСТЫЕ_СКОБКИ = re.compile(
    r"\s*[\(\[]\s*(?:(?:see|cf\.?|e\.g\.,?|i\.e\.,?|also|and|but|in|"
    r"reviewed in|[;,–—-]|\s)+)?[\)\]]")
# КРАЙ СКОБКИ ПОСЛЕ СНЯТОГО НОМЕРА: «(; see also Cymbalyuk et al.)»,
# «(Smith 2000, )», «(…, see)» — знак, стоявший при номере, уходит с ним.
КРАЙ_СКОБКИ = re.compile(r"([\(\[])\s*(?:[;,]\s*)+|(?:\s*[;,])+\s*([\)\]])")
# ДВА СНЯТЫХ НОМЕРА ПОДРЯД оставляют два знака подряд: «(; ; Mahajan» —
# знак, стоявший при снятом, уходит с ним, как и у края.
ДВОЙНОЙ_ЗНАК = re.compile(r"([;,])\s*(?:[;,]\s*)+")
ХВОСТ_SEE = re.compile(r",?\s*\bsee\s*([\)\]])")
ПРОБЕЛ_ПЕРЕД_ЗНАКОМ = re.compile(r"\s+([,.;:!?%])")
ПРОБЕЛ_У_СКОБКИ = re.compile(r"([\(\[])\s+|\s+([\)\]])")
ПУСТАЯ_ССЫЛКА = "[link]"
ПРЕДЛОЖЕНИЕ = re.compile(r"[.!?…][”’\"')\]]*$")
# ЗАМЕР 02.09 по 222 215 строкам семи прозаических сводов корпуса
# (shelf_fetch): медиана строки — 54 знака. Пункт списка длиннее
# медианной строки прозы есть проза по длине, каким бы знаком ни кончался.
МЕДИАНА_СТРОКИ = 54


def предложение(текст):
    return bool(ПРЕДЛОЖЕНИЕ.search(текст)) or len(текст) > МЕДИАНА_СТРОКИ


def без_аппарата(куски):
    """Раздел под рубрикой аппарата — до следующего заголовка того же или
    старшего уровня — снимается целиком."""
    вон, снимаем_до, вложенность, вложенность_рубрики = [], None, 0, 0
    for текст, уровень, вид in куски:
        if вид == "начало":
            вложенность += 1
            continue
        if вид == "конец":
            вложенность -= 1
            if снимаем_до is not None and вложенность < вложенность_рубрики:
                снимаем_до = None
            continue
        if вид == "заголовок":
            if (снимаем_до is not None and уровень <= снимаем_до
                    and вложенность <= вложенность_рубрики):
                снимаем_до = None
            if РУБРИКА.match(текст.strip()):
                снимаем_до, вложенность_рубрики = уровень, вложенность
                continue
        if снимаем_до is None:
            вон.append((текст, уровень, вид))
    return вон


# ФОРМУЛА ОСТАЁТСЯ ФОРМУЛОЙ (закон дороги TeX): шорткод Pressbooks
# «[latex]…[/latex]» отдаёт TeX между долларами, как своды корпуса.
ФОРМУЛА = re.compile(r"\[latex\](.*?)\[/latex\]", re.S)


def чистый(текст):
    т = ФОРМУЛА.sub(lambda м: " $" + " ".join(м.group(1).split()) + "$ ", текст)
    т = т.replace(ПУСТАЯ_ССЫЛКА, "")
    т = ОТСЫЛКА.sub("", т)
    # ПУСТЫЕ СКОБКИ СНИМАЮТСЯ ДВАЖДЫ — до края и после: номер цитаты
    # стоял в своих скобках внутри чужих, «([]; see also Kelso [])», и
    # край скобки виден лишь после того, как внутренняя пара ушла.
    т = ПУСТЫЕ_СКОБКИ.sub("", т)
    т = ДВОЙНОЙ_ЗНАК.sub(r"\1 ", т)
    т = КРАЙ_СКОБКИ.sub(lambda м: м.group(1) or м.group(2), т)
    т = ХВОСТ_SEE.sub(r"\1", т)
    т = ПУСТЫЕ_СКОБКИ.sub("", т)
    т = ПРОБЕЛ_ПЕРЕД_ЗНАКОМ.sub(r"\1", т)
    т = ПРОБЕЛ_У_СКОБКИ.sub(lambda м: м.group(1) or м.group(2), т)
    return " ".join(т.split())


def без_пустых_разделов(куски):
    """Заголовок раздела без текста — перед концом единицы или перед
    заголовком не глубже себя — не пишется: вводная страница главы у A&P
    вся из рисунка и целей, и «Introduction» над пустотой есть ложь."""
    while True:
        вон, снято = [], 0
        for i, (т, з, у) in enumerate(куски):
            if з:
                след = куски[i + 1] if i + 1 < len(куски) else None
                if след is None or (след[1] and след[2] <= у):
                    снято += 1
                    continue
            вон.append((т, з, у))
        куски = вон
        if not снято:
            return [(т, з) for т, з, _у in куски]


def прибрать(куски):
    """Куски одной главы или статьи → [(текст, заголовок)] по правилам."""
    вон = []
    for текст, уровень, вид in без_аппарата(куски):
        if вид == "пункт" and not предложение(текст):
            continue
        т = чистый(текст)
        if not т:
            continue
        # ПОВТОР ЗАГОЛОВКА ПОДРЯД — ярлык врезки, отданный архивом дважды
        # («Everyday Connection» в h3 и в h4 у Biology), — пишется раз.
        if вид == "заголовок" and вон and вон[-1][1] and вон[-1][0] == т:
            continue
        вон.append((т, вид == "заголовок", уровень))
    return без_пустых_разделов(вон)


def заглавие_узла(сырое):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", сырое)).split())


# ---------------------------------------------------------- PRESSBOOKS
def pressbooks_json(книга, кэш, путь):
    тело = взять(f"{книга.сайт}/wp-json/pressbooks/v2/{путь}",
                 кэш / книга.имя / (путь.replace("/", "_") + ".json"))
    return json.loads(тело.decode("utf-8"))


def pressbooks_единицы(книга, кэш, счёт):
    """[(куски главы)], автор — главы книги с авторами под заголовками."""
    мета = pressbooks_json(книга, кэш, "metadata")
    лиц = сверить_лицензию(книга, (мета.get("license") or {}).get("url"))
    # ИМЕНА ЛИЦ — ИЗ ВСЕХ СПИСКОВ МЕТАДАННЫХ, а не из одного «author»:
    # введение к книге пишет её редактор, и его slug лежал бы под
    # заголовком неразрешённым («heather-salazar»).
    имена = {л.get("slug"): л.get("name") for список in мета.values()
             if isinstance(список, list) for л in список
             if isinstance(л, dict) and л.get("@type") == "Person"}
    авторы = [л.get("name") for л in мета.get("author", []) if isinstance(л, dict)]
    редакторы = [л.get("name") for л in мета.get("editor", []) if isinstance(л, dict)]
    оглавление = pressbooks_json(книга, кэш, "toc")
    единицы = []

    def единица(часть, узел):
        заглавие = заглавие_узла(узел.get("title", {}).get("rendered", ""))
        куски = []
        if часть:
            куски.append((часть, 1, "заголовок"))
        куски.append((заглавие, 2 if часть else 1, "заголовок"))
        # АВТОР ГЛАВЫ — строкой под заголовком: атрибуция CC BY.
        # SLUG ГЛАВЫ КОРОЧЕ SLUG'А МЕТАДАННЫХ, когда имя несёт роль в скобках
        # («valery-vino» против «valery-vino-book-editor»): берётся лицо,
        # чей slug начинается с названного; иначе slug остаётся как есть.
        свои = [имена.get(с) or next((н for сл, н in имена.items()
                                       if сл and н and сл.startswith(с)), с)
                for с in (узел.get("meta") or {}).get("pb_authors", [])]
        if свои:
            куски.append((", ".join(свои), 0, "абзац"))
        куски += разобрать(узел.get("content", {}).get("rendered", ""), счёт)
        return куски

    for фм in оглавление.get("front-matter", []):
        if заглавие_узла(фм["title"]).startswith("Introduction to the Book"):
            единицы.append(единица(None, pressbooks_json(
                книга, кэш, f"front-matter/{фм['id']}")))
    прежняя = None
    for часть in оглавление.get("parts", []):
        имя_части = заглавие_узла(часть.get("title") or "")
        if книга.части and not имя_части.startswith(книга.части):
            continue
        for гл in часть.get("chapters", []):
            if РУБРИКА.match(заглавие_узла(гл["title"])):
                continue
            узел = pressbooks_json(книга, кэш, f"chapters/{гл['id']}")
            # Заглавие части — заголовком лишь перед её первой главой и
            # лишь когда части объявлены: у Rebus часть зовётся «Chapters».
            свежая = имя_части if (книга.части and имя_части != прежняя) else None
            единицы.append(единица(свежая, узел))
            прежняя = имя_части
    автор = ", ".join(sorted(а for а in авторы if а))
    if редакторы:
        автор += ("; " if автор else "") + "ed. " + ", ".join(р for р in редакторы if р)
    return единицы, автор or книга.автор, лиц


# ------------------------------------------------------------ OPENSTAX
def openstax_архив(кэш):
    """Корень архива — из release.json REX на день ковки; версия книги
    пришпилена объявлением, корень меняется с выпусками сайта."""
    тело = взять(f"{OPENSTAX}/rex/release.json", кэш / "openstax" / "release.json")
    return json.loads(тело)["archiveUrl"]


def openstax_json(книга, кэш, архив, ссылка, файл):
    тело = взять(f"{OPENSTAX}{архив}/contents/{ссылка}.json",
                 кэш / книга.имя / файл)
    return json.loads(тело)


ГЛАВА = re.compile(r"(?:Chapter|Rozdział|Capítulo)\s+(\d+)\s*(.*)")


def openstax_единицы(книга, кэш, счёт):
    """[(куски страницы)], отказы — страницы объявленных глав, без аппарата.

    СВОДНАЯ СТРАНИЦА ГЛАВЫ АРХИВОМ НЕ ОТДАЁТСЯ: «Revisión del capítulo»
    у «Física universitaria» собирается при сборке книги, и на её id архив
    отвечает 404. Она рубрика и не запрашивается; страница же, отказанная
    архивом иначе, считается отказом и книгу не роняет."""
    архив = openstax_архив(кэш)
    книга_json = openstax_json(книга, кэш, архив,
                               f"{книга.uuid}@{книга.версия}", "book.json")
    лиц = сверить_лицензию(книга, (книга_json.get("license") or {}).get("url"))
    единицы, отказы = [], collections.Counter()

    def обход(узел):
        for дитя in узел.get("contents", []):
            if "contents" not in дитя:
                continue          # предисловие, указатель, библиография
            заглавие = заглавие_узла(дитя.get("title", ""))
            м = ГЛАВА.match(заглавие)
            if not м:
                обход(дитя)       # раздел книги (Unit) — глубже
                continue
            if книга.главы and int(м.group(1)) not in книга.главы:
                continue
            первая = True
            for стр in дитя["contents"]:
                имя_стр = заглавие_узла(стр.get("title", ""))
                if РУБРИКА.match(имя_стр):
                    continue
                ид = стр["id"].split("@")[0]
                try:
                    стр_json = openstax_json(
                        книга, кэш, архив, f"{книга.uuid}@{книга.версия}:{ид}",
                        f"{ид}.json")
                except urllib.error.HTTPError as беда:
                    отказы[f"HTTP {беда.code}"] += 1
                    continue
                куски = ([(заглавие, 1, "заголовок")] if первая else [])
                куски.append((имя_стр, 2, "заголовок"))
                куски += разобрать(стр_json.get("content", ""), счёт)
                единицы.append(куски)
                первая = False

    обход(книга_json.get("tree", {}))
    return единицы, книга.автор, лиц, отказы


# ----------------------------------------------------------- EUROPE PMC
def europepmc_поиск(книга, кэш):
    """Все находки запроса, курсором до конца; кэш — снимок дня ковки."""
    файл = кэш / книга.имя / "search.json"
    if файл.is_file():
        return json.loads(файл.read_text(encoding="utf-8"))
    все, курсор = [], "*"
    while True:
        адрес = f"{EUROPEPMC}/search?" + urllib.parse.urlencode(
            {"query": книга.запрос, "resultType": "lite", "pageSize": 1000,
             "format": "json", "cursorMark": курсор})
        з = urllib.request.Request(адрес, headers={"User-Agent": UA})
        д = json.loads(urllib.request.urlopen(з, timeout=180).read())
        time.sleep(ПАУЗА)
        куски = д.get("resultList", {}).get("result", [])
        все += куски
        след = д.get("nextCursorMark")
        if not куски or not след or след == курсор:
            break
        курсор = след
    файл.parent.mkdir(parents=True, exist_ok=True)
    файл.write_text(json.dumps(все, ensure_ascii=False), encoding="utf-8")
    return все


def _имя(эл):
    return эл.tag.split("}")[-1]


ЛИШНЕЕ_JATS = {"fig", "table-wrap", "supplementary-material", "graphic",
               "media", "object-id", "label", "caption", "fn", "fig-group",
               "table-wrap-group", "math", "ref-list", "glossary", "def-list",
               "table", "ack", "app-group", "notes", "fn-group"}
ЛИШНИЙ_РЕФЕРАТ = {"graphical", "teaser", "author-highlights", "highlights",
                  "toc", "precis", "web-summary", "video", "editor"}
# ЛИЦЕНЗИЯ, НАЗВАННАЯ СЛОВАМИ БЕЗ АДРЕСА: PLOS и Royal Society до 2015
# писали «distributed under the terms of the Creative Commons Attribution
# License» и не давали ссылки. Слова читаются, оговорка NC/SA/ND — тоже;
# версия, если не названа, не выдумывается («CC BY»).
ЛИЦЕНЗИЯ_СЛОВАМИ = re.compile(
    r"Creative Commons Attribution(?:\s+(\d\.\d))?"
    r"(?:\s+(?:International|Unported|Generic))?\s+Licen[cs]e", re.I)
ОГОВОРКА = re.compile(r"Non[- ]?Commercial|Share[- ]?Alike|No[- ]?Deriv", re.I)


def текст_jats(эл):
    """Текст узла JATS: цитата с именем автора остаётся, номер цитаты и
    отсылка к рисунку уходят, формула — TeX'ом, если он есть."""
    вон = [эл.text or ""]
    for д in эл:
        и = _имя(д)
        if и == "xref":
            с = "".join(д.itertext())
            if д.get("ref-type") == "bibr" and re.search(r"[A-Za-z]", с):
                вон.append(с)
        elif и in ("inline-formula", "disp-formula"):
            tex = next((т for т in д.iter() if _имя(т) == "tex-math"), None)
            if tex is not None:
                ф = " ".join("".join(tex.itertext()).split()).strip("$ ")
                вон.append(f" $$ {ф} $$ " if и == "disp-formula" else f" ${ф}$ ")
        elif и in ЛИШНЕЕ_JATS:
            pass
        elif и == "break":
            вон.append(" ")
        else:
            вон.append(текст_jats(д))
        вон.append(д.tail or "")
    return "".join(вон)


def куски_jats(эл, уровень, вон):
    for д in эл:
        и = _имя(д)
        if и == "sec":
            з = д.find("title")
            if з is not None:
                вон.append((" ".join(текст_jats(з).split()), уровень, "заголовок"))
            куски_jats(д, уровень + 1, вон)
        elif и == "boxed-text":
            з = д.find("title")
            if з is None:
                з = д.find("caption/title")
            if з is not None:
                вон.append((" ".join(текст_jats(з).split()), уровень, "заголовок"))
            куски_jats(д, уровень + 1, вон)
        elif и in ("p", "disp-quote"):
            вон.append((" ".join(текст_jats(д).split()), 0, "абзац"))
        elif и == "list":
            for пункт in д:
                if _имя(пункт) == "list-item":
                    вон.append((" ".join(текст_jats(пункт).split()), 0, "пункт"))
        elif и == "disp-formula":
            tex = next((т for т in д.iter() if _имя(т) == "tex-math"), None)
            if tex is not None:
                вон.append(("$$ " + " ".join("".join(tex.itertext()).split()).strip("$ ")
                            + " $$", 0, "абзац"))
        elif и in ("title", "caption") or и in ЛИШНЕЕ_JATS:
            continue
        else:
            куски_jats(д, уровень, вон)


def статья_jats(xml, pmcid):
    """(куски, год) статьи или (None, почему): лицензия и год — из XML."""
    корень = ET.fromstring(xml)
    названная, словами = "", ""
    for л in корень.iter():
        if _имя(л) == "license":
            названная = л.get(XLINK) or ""
            for р in л.iter():
                названная = названная or р.get(XLINK) or ""
            словами = " ".join("".join(л.itertext()).split())
            м = re.search(r"creativecommons\.org/licenses/[a-z\-]+/\d\.\d", словами)
            названная = названная or (м.group() if м else "")
            break
    лиц = лицензия_источника(названная)
    if лиц is None and not названная:
        м = ЛИЦЕНЗИЯ_СЛОВАМИ.search(словами)
        if м and not ОГОВОРКА.search(словами):
            лиц = "CC BY" + (f" {м.group(1)}" if м.group(1) else "")
    if лиц is None:
        return None, f"лицензия «{названная or словами[:60] or '—'}»"
    мета = корень.find(".//article-meta")
    годы = [int(г.text) for д in мета.findall("pub-date") for г in д
            if _имя(г) == "year" and г.text and г.text.strip().isdigit()]
    if not годы:
        return None, "год не назван"
    год = min(годы)
    if год >= shelf_kinds.РУБЕЖ_МАШИНЫ:
        return None, f"издано {год}"
    заглавие_эл = мета.find(".//title-group/article-title")
    заглавие = " ".join(текст_jats(заглавие_эл).split()) if заглавие_эл is not None else pmcid
    авторы = []
    for к in мета.iter():
        if _имя(к) != "contrib" or к.get("contrib-type") not in (None, "author"):
            continue
        н = next((д for д in к if _имя(д) == "name"), None)
        if н is not None:
            авторы.append(" ".join(х for х in (н.findtext("given-names"),
                                                н.findtext("surname")) if х))
        else:
            кол = next((д for д in к if _имя(д) == "collab"), None)
            if кол is not None:
                авторы.append(" ".join("".join(кол.itertext()).split()))
    журнал = корень.findtext(".//journal-meta//journal-title") or ""
    # АТРИБУЦИЯ CC BY — строкой под заглавием: авторы, журнал, год, PMCID.
    # Восемь имён, дальше «et al.»: так пишут сами журналы.
    имена = ", ".join(авторы[:8]) + (" et al." if len(авторы) > 8 else "")
    куски = [(заглавие, 1, "заголовок"),
             (f"{имена} — {журнал}, {год}. {pmcid}, {лиц}.", 0, "абзац")]
    for р in мета.iter():
        if _имя(р) == "abstract" and (р.get("abstract-type") or "") not in ЛИШНИЙ_РЕФЕРАТ:
            for п in р.iter():
                if _имя(п) == "p":
                    куски.append((" ".join(текст_jats(п).split()), 0, "абзац"))
    тело = корень.find(".//body")
    if тело is not None:
        куски_jats(тело, 2, куски)
    return куски, год


def europepmc_единицы(книга, кэш):
    """[(куски статьи)] в порядке год → журнал → PMCID; отказы считаются."""
    найдено = europepmc_поиск(книга, кэш)
    найдено.sort(key=lambda р: (int(р.get("pubYear") or 0),
                                р.get("journalTitle") or "", р.get("pmcid") or ""))
    единицы, отказы, годы = [], collections.Counter(), []
    for р in найдено:
        pmcid = р.get("pmcid")
        if not pmcid:
            отказы["без PMCID"] += 1
            continue
        try:
            xml = взять(f"{EUROPEPMC}/{pmcid}/fullTextXML",
                        кэш / "europepmc" / f"{pmcid}.xml")
        except urllib.error.HTTPError as беда:
            отказы[f"HTTP {беда.code}"] += 1
            continue
        try:
            куски, год = статья_jats(xml, pmcid)
        except ET.ParseError:
            отказы["XML не разобран"] += 1
            continue
        if куски is None:
            отказы[год] += 1
            continue
        единицы.append(куски)
        годы.append(год)
    return единицы, отказы, годы


# --------------------------------------------------------------- КОВКА
def плотность_по_мере(объявленная, доля):
    """Трактат и статья обязаны быть не реже порога; иначе — исследование."""
    if объявленная in ("трактат", "статья") and доля < shelf_kinds.ПОРОГ_ПЛОТНОСТИ:
        return "исследование"
    return объявленная


def объявление(книга, плотность, издано, автор, лиц, происхождение, байт):
    узел = shelf_kinds.объявление_мира(
        имя=книга.имя, файл=f"shelf/{книга.язык}/{книга.имя}.txt",
        жанр=(f"{книга.заглавие} — {автор}; {книга.издатель} {издано} "
              f"под {лиц}"),
        язык=книга.язык, тема=книга.тема, плотность=плотность,
        издано=издано, происхождение=f"{происхождение} ({лиц})",
        судится=[], размер=байт, источник=книга.источник)
    узел["автор"] = автор
    return узел


def ковать(книга, кэш):
    отказы, годы, формулы = {}, [], collections.Counter()
    if книга.дорога == "pressbooks":
        единицы, автор, лиц = pressbooks_единицы(книга, кэш, формулы)
        происхождение = f"pressbooks:{книга.сайт}"
    elif книга.дорога == "openstax":
        единицы, автор, лиц, отказы = openstax_единицы(книга, кэш, формулы)
        происхождение = (f"openstax-archive:{книга.uuid}@{книга.версия}, "
                         f"{книга.происхождение}")
    else:
        единицы, отказы, годы = europepmc_единицы(книга, кэш)
        автор, лиц = книга.автор, книга.лицензия
        происхождение = (f"europepmc:{len(единицы)} articles by query "
                         f"{книга.запрос}")
    if not единицы:
        raise ОтказПолки("источник не отдал ни одной единицы текста")
    строки = []
    for куски in единицы:
        строки += shelf_fetch.строки(прибрать(куски))
    тело, отложенное = shelf_fetch.отложить(строки)
    выход = КОРЕНЬ / "shelf" / книга.язык
    байт, строк = shelf_fetch.записать(выход / f"{книга.имя}.txt", тело)
    ещё = (shelf_fetch.записать(выход / f"{книга.имя}.holdout.txt", отложенное)
           if отложенное else (0, 0))
    текст = "\n".join(тело)
    слов = len(re.findall(r"\w+", текст))
    # МЕРА БЕРЁТ ПРИЗНАКИ ЯЗЫКА МИРА (shelf_kinds.ПРИЗНАКИ_ЯЗЫКА): польская
    # книга меряется польскими словами определения и вывода.
    доля, предложений, счёт = shelf_kinds.плотность(текст, книга.язык)
    плотность = плотность_по_мере(книга.плотность, доля)
    остаток = {"[link]": текст.count(ПУСТАЯ_ССЫЛКА),
               "<>": текст.count("<") + текст.count(">"),
               "()": len(re.findall(r"[\(\[]\s*[\)\]]", текст))}
    # ГОД СВОДА СТАТЕЙ — год самой поздней взятой статьи, а не объявление.
    издано = max(годы) if годы else книга.издано
    print(f"  {книга.имя:<28} единиц {len(единицы):>4} строк {строк:>6} "
          f"отложено {ещё[1]:>5} слов {слов:>8} байт {байт:>9} "
          f"плотность {доля:.3f} по {предложений} предл "
          f"(опр {счёт['определение']}, выв {счёт['вывод']}, "
          f"ссыл {счёт['ссылка']}) → {плотность}"
          + (f" издано {издано}" if годы else "")
          + f" остаток {остаток}"
          + (f" формул {формулы['формул']} (неизвестных узлов "
             f"{формулы['неизвестных']}, не разобрано {формулы['не разобрано']})"
             if формулы["формул"] else "")
          + (f" отказов {dict(отказы)}" if отказы else ""))
    return объявление(книга, плотность, издано, автор, лиц, происхождение, байт)


МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"


def сложить_узлы(узлы, путь):
    """Файл ожидания несёт лишь узлы, которых В МАНИФЕСТЕ ЕЩЁ НЕТ: вписанный
    хозяином манифеста узел из ожидания уходит сам, и файл не растёт
    ложью о невписанном. Манифест здесь только читается."""
    было = json.loads(путь.read_text(encoding="utf-8")) if путь.is_file() else []
    по_имени = {у["name"]: у for у in было}
    for у in узлы:
        по_имени[у["name"]] = у
    if МАНИФЕСТ.is_file():
        вписаны = {м.get("name") for м in
                   json.loads(МАНИФЕСТ.read_text(encoding="utf-8")).get("worlds", [])}
        по_имени = {и: у for и, у in по_имени.items() if и not in вписаны}
    путь.parent.mkdir(parents=True, exist_ok=True)
    путь.write_text(json.dumps([по_имени[и] for и in sorted(по_имени)],
                               ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return len(по_имени)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--кэш", required=True)
    ap.add_argument("--только", default="",
                    help="имена книг через запятую; пусто — вся полка")
    ap.add_argument("--узлы", default=str(УЗЛЫ),
                    help="куда складывать узлы манифеста, ждущие вставки")
    а = ap.parse_args()
    беды = судить_объявление()
    if беды:
        for б in беды:
            print(f"  ОБЪЯВЛЕНИЕ {б}")
        print(f"ПОЛКА ОТКАЗ: {len(беды)} бед в объявлении, источника не трогаем")
        return 2
    кэш = pathlib.Path(а.кэш)
    отбор = {и.strip() for и in а.только.split(",") if и.strip()}
    неизвестные = отбор - {к.имя for к in ПОЛКА}
    if неизвестные:
        print(f"ПОЛКА ОТКАЗ: имена не объявлены — {', '.join(sorted(неизвестные))}")
        return 2
    книги = [к for к in ПОЛКА if not отбор or к.имя in отбор]
    узлы = []
    for книга in книги:
        try:
            узлы.append(ковать(книга, кэш))
        except (ОтказПолки, OSError, ValueError, KeyError) as беда:
            print(f"  ОТКАЗ {книга.имя}: {беда}")
    if узлы:
        всего = сложить_узлы(узлы, pathlib.Path(а.узлы))
        print(f"  УЗЛЫ: {len(узлы)} сложено в {а.узлы}, всего там {всего}")
    print(f"ПОЛКА ОТКРЫТЫХ КОРПУСОВ: {len(узлы)} книг из {len(книги)}")
    return 0 if len(узлы) == len(книги) else 1


if __name__ == "__main__":
    sys.exit(main())
