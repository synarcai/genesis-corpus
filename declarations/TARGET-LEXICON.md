# ЦЕЛЕВОЙ СЛОВАРЬ: слова, которые корпус ОБЯЗУЕТСЯ прожить

Все меры корпуса до сего дня спрашивали одно: **верна ли строка**.
Ни одна не спрашивала **хватает ли слов**. Оттого корпус, у которого
судимость сто процентов и ноль лжи на ста двадцати тысячах строк,
умирал на школьном вопросе «Janey counted the apples in the parking
lot» — не потому, что чего-то не знал по существу, а потому, что не
видел слова «parking» ни разу.

Здесь объявлен словарь, который корпус берётся прожить. Объявление —
не список красивых слов, а ДОГОВОР: `scripts/lexicon_reach.py`
измеряет, сколько из объявленного действительно живёт в мирах показов
и сколько раз, и падает, если договор не выполнен.

Слово считается ПРОЖИТЫМ, если встречается в мирах показов не менее
двух раз (то же правило, что у поля LANGPACK-ONCE: сказанное однажды
не выучивается).

Список ведётся по родам быта, а не по алфавиту: род называет, ЧЕГО
корпусу не хватает, и потому подсказывает, какой мир строить.

## места
school, class, room, house, home, garden, park, parking, street, road,
shop, store, market, kitchen, office, library, station, farm, field,
river, forest, mountain, city, town, village, yard, floor, wall, door,
window, table, chair, bed, box, bag, basket, shelf, bottle, cup, plate

## время быта
morning, day, evening, night, week, weekend, month, year, hour, minute,
today, yesterday, tomorrow, now, later, early, late, first, next, last,
before, after, during, while, again, once, twice, always, never, often

## люди и роли
boy, girl, man, woman, child, children, friend, teacher, student,
worker, driver, baker, farmer, seller, buyer, doctor, neighbour,
brother, sister, mother, father, family, people, everyone, someone

## действия быта
buy, buys, bought, sell, sells, sold, give, gives, gave, take, takes,
took, make, makes, made, put, puts, get, gets, got, keep, keeps, kept,
find, finds, found, lose, loses, lost, count, counts, counted, write,
writes, wrote, read, reads, walk, walks, walked, run, runs, ran, eat,
eats, ate, drink, drinks, drank, work, works, worked, play, plays,
played, wait, waits, waited, start, starts, started, finish, finishes,
finished, break, breaks, broke, fill, fills, filled, empty, empties,
emptied, share, shares, shared, spend, spends, spent, save, saves,
saved, pay, pays, paid, cost, costs, earn, earns, earned, need, needs,
needed, want, wants, wanted, know, knows, knew, think, thinks, thought,
say, says, said, tell, tells, told, ask, asks, asked, answer, answers,
answered, see, sees, saw, look, looks, looked, hear, hears, heard,
realize, realizes, realized, decide, decides, decided, remain, remains,
remained, leave, leaves, left, arrive, arrives, arrived, return,
returns, returned, bring, brings, brought, carry, carries, carried

## вещи быта
apple, apples, book, books, pen, pens, pencil, pencils, card, cards,
coin, coins, ticket, tickets, box, boxes, bag, bags, bottle, bottles,
egg, eggs, cake, cakes, bread, milk, water, tea, coffee, sugar, salt,
flower, flowers, tree, trees, stone, stones, toy, toys, ball, balls,
shirt, shoes, hat, chair, chairs, lamp, lamps, key, keys, letter,
letters, page, pages, line, lines, note, notes, list, lists

## отношения и сравнение
more, less, fewer, most, least, than, as, same, different, equal,
together, apart, each, every, both, all, some, none, other, another,
half, twice, double, triple, total, altogether, in all, remaining,
rest, left over, per, each other

## речь задачи
how, many, much, what, which, who, when, where, why, if, then, so,
because, therefore, hence, and, or, but, not, no, yes, there, here,
now, still, already, only, just, about, around, nearly, exactly
