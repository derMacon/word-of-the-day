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


# import time
# import nltk
# from nltk.corpus import wordnet as wn
#
# Ensure wordnet is downloaded
# nltk.download('wordnet')


# def autocomplete_word(prefix):
#     # Get all words in WordNet
#     words = set(wn.all_lemma_names())
#
#     # Find words starting with the prefix
#     completions = [word for word in words if word.startswith(prefix)]
#
#     return completions


# import enchant

#
# def autocomplete_word(prefix):
#     # Create a dictionary for English
#     d = enchant.Dict("de_DE")
#     # d = enchant.Dict("en_US")
#
#     # Get suggestions that start with the prefix
#     suggestions = d.suggest(prefix)
#
#     # Filter to only include words starting with the prefix (autocomplete behavior)
#     return [word for word in suggestions if word.startswith(prefix)]
#
#
# # Example usage
# prefix = "wasse"
#
# start = time.time()
# suggestions = autocomplete_word(prefix)
# end = time.time()
# print(f'elapsed api call: {end - start}')
#
# print(suggestions[:10])  # Show only the first 10 suggestions
#



MERGING_SEPERATOR = ' | '

print('out: ', MERGING_SEPERATOR.join([None, 'snd']))
