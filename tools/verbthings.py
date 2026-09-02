"""A VERB TAKES ITS OWN KIND OF THINGS (03.09).

The lexical worlds paired any verb with any countable thing, and the frame
wore nonsense: «sara wrote 8 pencils», «ann bought 21 books and ate 12 books»,
«hugo reads 5 apples», «ann walks 2 pounds every day». A verb of eating takes
food, a verb of writing takes what is written, a verb of walking takes a
distance or a time — and the corpus that teaches speech must not teach the
contrary. One house declares what each verb takes; the generators draw their
things from it, and the episode court refuses a known verb with a thing of
the wrong kind (an unknown verb or an unknown thing is not judged here).
"""
ЕДА = {"apples", "cookies", "cakes", "pastries", "nuts", "eggs", "slices", "bananas", "oranges", "pears", "sweets",
       "candies", "sandwiches", "grapes", "plums", "buns", "pies", "loaves", "pancakes", "cherries", "carrots", "calories"}
ПИТЬЁ = {"cups", "glasses", "bottles", "gallons", "litres", "liters", "mugs"}
ВЫПЕЧКА = {"cookies", "cakes", "pies", "buns", "loaves", "pastries", "pancakes"}
ПИСЬМЕННОЕ = {"letters", "pages", "cards", "notes", "words", "lines", "poems", "essays", "stories", "chapters", "books"}
ЧТЕНИЕ = {"books", "pages", "letters", "cards", "stories", "poems", "chapters", "notes", "words", "lines"}
РАССТОЯНИЕ_ВРЕМЯ = {"miles", "kilometres", "kilometers", "metres", "meters", "feet", "steps", "laps", "minutes", "hours", "seconds"}
ВЕС = {"pounds", "kilograms", "grams"}
ОЧКИ = {"points", "goals", "runs"}
ДЕНЬГИ = {"dollars", "coins", "cents", "rubles", "euros"}
ПОСЕВ = {"seeds", "flowers", "trees", "bulbs"}
СБОР = {"shells", "stones", "stamps", "coins", "cards", "seeds", "flowers", "mushrooms", "berries", "nuts", "eggs", "apples", "pears", "plums", "cherries"}
ВРЕМЯ = {"minutes", "hours", "seconds", "days", "weeks", "months", "years"}
# what a hand picks: small countable things (not distances, not money, not points)
В_РУКЕ = {"books", "cards", "pens", "pencils", "balls", "marbles", "stamps", "coins", "shells", "stones", "flowers", "toys", "blocks",
          "buttons", "stickers", "balloons", "cups", "boxes", "bottles", "hats", "shirts", "keys", "rings", "pieces", "sticks", "leaves"}

# the verbs of the SVAMP/g1 bands the school lacked (e9 04.09): what they take
ПРЫЖОК = {"inches", "feet", "centimetres", "centimeters", "metres", "meters", "times"}
УПРАЖНЕНИЯ = {"push-ups", "crunches", "laps", "sit-ups", "jumps", "squats"}
ВЫПОЛНЕНИЕ = {"pages", "problems", "laps", "tasks", "exercises", "chapters", "levels"}
ПРОСМОТР = {"movies", "episodes", "films", "shows", "videos", "games"}
ВЫИГРЫШ = {"games", "tickets", "medals", "prizes", "rounds", "matches"}
ПОСЫЛКА = {"letters", "emails", "cards", "messages", "parcels", "postcards"}
УБОРКА = {"figures", "books", "stones", "boxes", "toys", "stickers", "weeds", "leaves"}
СБОР_ДЕНЕГ = {"dollars", "euros", "rubles", "coins"}
РОСТ = {"inches", "centimetres", "centimeters", "flowers", "plants", "trees", "tomatoes"}
ВЫБРОС = {"caps", "boxes", "cans", "bottles", "papers", "toys", "cards"}

ГЛАГОЛ_БЕРЁТ = {
    "jumped": ПРЫЖОК, "jumps": ПРЫЖОК, "jump": ПРЫЖОК,
    # «do/does/did» — лёгкий глагол и вспомогательный разом («how many minutes
    # do 2 hours equal?»): дом о нём молчит; как дело он судится рамкой семейства.
    "completed": ВЫПОЛНЕНИЕ, "completes": ВЫПОЛНЕНИЕ, "complete": ВЫПОЛНЕНИЕ,
    "watched": ПРОСМОТР, "watches": ПРОСМОТР, "watch": ПРОСМОТР,
    "won": ВЫИГРЫШ, "wins": ВЫИГРЫШ, "win": ВЫИГРЫШ,
    "sent": ПОСЫЛКА, "sends": ПОСЫЛКА, "send": ПОСЫЛКА,
    "removed": УБОРКА, "removes": УБОРКА, "remove": УБОРКА,
    "raised": СБОР_ДЕНЕГ | РОСТ, "raises": СБОР_ДЕНЕГ | РОСТ, "raise": СБОР_ДЕНЕГ | РОСТ,
    "grew": РОСТ, "grown": РОСТ, "grows": РОСТ, "grow": РОСТ,
    "threw": ВЫБРОС, "throws": ВЫБРОС, "throw": ВЫБРОС,
    "ate": ЕДА, "eats": ЕДА, "eat": ЕДА, "eaten": ЕДА,
    "drank": ПИТЬЁ, "drinks": ПИТЬЁ, "drink": ПИТЬЁ, "drunk": ПИТЬЁ,
    "baked": ВЫПЕЧКА, "bakes": ВЫПЕЧКА, "bake": ВЫПЕЧКА,
    "wrote": ПИСЬМЕННОЕ, "writes": ПИСЬМЕННОЕ, "write": ПИСЬМЕННОЕ, "written": ПИСЬМЕННОЕ,
    "read": ЧТЕНИЕ, "reads": ЧТЕНИЕ,
    "walks": РАССТОЯНИЕ_ВРЕМЯ, "walked": РАССТОЯНИЕ_ВРЕМЯ, "runs": РАССТОЯНИЕ_ВРЕМЯ | ОЧКИ, "ran": РАССТОЯНИЕ_ВРЕМЯ,
    "drove": РАССТОЯНИЕ_ВРЕМЯ, "drives": РАССТОЯНИЕ_ВРЕМЯ, "swam": РАССТОЯНИЕ_ВРЕМЯ, "swims": РАССТОЯНИЕ_ВРЕМЯ,
    "weighs": ВЕС, "weighed": ВЕС, "lifts": ВЕС, "lifted": ВЕС,
    "scored": ОЧКИ, "scores": ОЧКИ,
    "earns": ДЕНЬГИ, "earned": ДЕНЬГИ, "paid": ДЕНЬГИ, "pays": ДЕНЬГИ,
    # money is spent, and so is time
    "spends": ДЕНЬГИ | ВРЕМЯ, "spent": ДЕНЬГИ | ВРЕМЯ,
    "planted": ПОСЕВ, "plants": ПОСЕВ,
    "collected": СБОР | В_РУКЕ, "collects": СБОР | В_РУКЕ, "picked": СБОР | ЕДА | В_РУКЕ, "picks": СБОР | ЕДА | В_РУКЕ,
}
ВСЕ_ВЕЩИ = set().union(*ГЛАГОЛ_БЕРЁТ.values())


def берёт(глагол, вещь):
    """True — the pair is admissible or not this house's business (an unknown
    verb, or a thing no pool names); False — a known verb with a thing of
    the wrong kind."""
    род = ГЛАГОЛ_БЕРЁТ.get(глагол)
    if род is None or вещь not in ВСЕ_ВЕЩИ:
        return True
    return вещь in род


def годные(глаголы, вещи, ключ=None):
    """The things of a pool that every verb of the frame admits (the pool
    itself when nothing is constrained); `ключ` names the English plural of
    an item that is not a plain string."""
    ключ = ключ or (lambda в: в if isinstance(в, str) else в[-1])
    вон = [в for в in вещи if all(берёт(г, ключ(в)) for г in глаголы)]
    return вон or list(вещи)


def подобрать(глаголы, вещи, k, ключ=None):
    """The k-th admissible thing of the pool for the verbs of a frame."""
    г = годные(глаголы, вещи, ключ)
    return г[k % len(г)]


def индекс(глаголы, вещи, k, ключ=None):
    """The index in the pool of the k-th admissible thing — for a second
    pool that runs parallel to the first (Russian things beside English)."""
    return вещи.index(подобрать(глаголы, вещи, k, ключ))
