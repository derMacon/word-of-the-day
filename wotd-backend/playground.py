from src.data.anki.anki_card import AnkiCard

fst = AnkiCard(
    item_ids=[1, 2, 3],
    deck='test-deck',
    front='front-1',
    back='back-1'
)

snd = AnkiCard(
    item_ids=[4, 5, 6],
    deck='test-deck',
    front='front-1',
    back='back-2'
)

thrd = AnkiCard(
    item_ids=[4, 5, 6, 7],
    deck='test-deck',
    front='front-1',
    back='back-2 back-3'
)

print(f'before merge: {fst}')
out = fst.merge_cards([snd, thrd])
print(f'after merge: {fst}')
