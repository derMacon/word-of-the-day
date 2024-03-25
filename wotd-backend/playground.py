# from src.service.persistence_service import PersistenceService
#
# print('before')
# persistence = PersistenceService()
# print('middle: ', persistence)
# persistence.get_available_languages()
# print('after: ', persistence)
import requests

from src.service.autocomplete_api_fetcher import lookup_autocomplete

# response_tuples = Dict().translate(
#     word='Behörde',
#     from_language='en',
#     to_language='de'
# ).translation_tuples
# options: List[DictOptionsItem] = from_translation_tuples(response_tuples)
# print(f'lookup options: {options}')


# auto_comp = lookup_autocomplete('doo')


params = {
    'prefix': 'doo',
    'num': 10
}

AUTOCOMPLETE_API_SERVER_ADDRESS = 'https://api.imagineville.org'
AUTOCOMPLETE_API_BASE = AUTOCOMPLETE_API_SERVER_ADDRESS + '/word/predict'

plain_response = requests.get(AUTOCOMPLETE_API_BASE, params=params).json()
print(f'plain response: {plain_response}')
