# from src.data.anki.anki_card import AnkiCard
#
# fst = AnkiCard(
#     item_ids=[1, 2, 3],
#     deck='test-deck',
#     front='front-1',
#     back='back-1',
#     ts='2024-09-11 00:03:41'
# )
#
# snd = AnkiCard(
#     item_ids=[4, 5, 6],
#     deck='test-deck',
#     front='front-1',
#     back='back-2',
#     ts='2024-09-11 00:04:41'
# )
#
# thrd = AnkiCard(
#     item_ids=[4, 5, 6, 7],
#     deck='test-deck',
#     front='front-1',
#     back='back-2 back-3',
#     ts='2024-09-11 00:08:41'
# )
#
# lst = [snd, thrd, fst]
#
# print(sorted(lst, key=lambda card: card.ts))
from src.data.dict_input import now

print(type(now()))

