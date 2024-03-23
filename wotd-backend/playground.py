# from src.service.persistence_service import PersistenceService
#
# print('before')
# persistence = PersistenceService()
# print('middle: ', persistence)
# persistence.get_available_languages()
# print('after: ', persistence)
from typing import List

from dictcc import Dict

from src.data.dict_input.dict_options_item import DictOptionsItem, from_translation_tuples

response_tuples = Dict().translate(
    word='Behörde',
    from_language='en',
    to_language='de'
).translation_tuples
options: List[DictOptionsItem] = from_translation_tuples(response_tuples)
print(f'lookup options: {options}')
