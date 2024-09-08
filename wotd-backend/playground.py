from src.data.anki.anki_connect_get_profiles import AnkiConnectRequestGetProfiles
from src.data.dict_input.anki_login_response_headers import UnsignedAuthHeaders
from src.service.wotd_api_fetcher import WotdAnkiConnectFetcher

WotdAnkiConnectFetcher()._validate_if_profile_present('asdfasdf')
