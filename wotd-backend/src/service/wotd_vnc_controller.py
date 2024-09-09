import os
import time
import uuid

from singleton_decorator import singleton
from vncdotool import api

from src.utils.logging_config import app_log


# TODO make functions static or use singleton decorator - only works without constants in the class (first put them into .ini file)

@singleton
class WotdVncController:
    """
    Since the anki connect addon does not provide the ability to login new users I implemented a simple workaround
    using a vnc viewer where it is possible to create new profiles (including setting the existing credentials for
    anki web) via shortcuts that are propaged through the viewer to the running anki desktop application. This
    application runs inside a docker container to be able to deploy it on a server.
    """

    def __init__(self):
        anki_connect_host = os.environ.get('ANKI_CONNECT_HOST', 'localhost')
        anki_connect_login_port = os.environ.get('ANKI_CONNECT_LOGIN_PORT', 5900)

        self.anki_connect_login_address_vnc = f'{anki_connect_host}::{anki_connect_login_port}'
        self.anki_connect_login_password = os.environ.get('ANKI_CONNECT_LOGIN_PASSWORD', '')

        self._client = api.connect(
            self.anki_connect_login_address_vnc,
            password=self.anki_connect_login_password
        )

    def teardown(self):
        app_log.debug('disconnecting vnc client')
        self._client.disconnect()

    def reset_connection(self):
        app_log.debug('reset vnc connection')
        self.teardown()
        self._client = api.connect(
            self.anki_connect_login_address_vnc,
            password=self.anki_connect_login_password
        )


    def login(self, username: str, password: str) -> str:
        # TODO mutex with housekeeping so no connection gets interrupted?
        self.reset_connection()

        app_log.debug(f"user '{username}' tries to login")

        profile_name = str(uuid.uuid4())
        # profile_name = 'test-profile-01'

        self._create_new_profile(profile_name)
        self._select_created_profile()
        self._login_anki_web(username, password)

        app_log.debug(f'login mechanism run complete for new profile with uuid: {profile_name}')

        return profile_name

    def _create_new_profile(self, profile_name: str):
        app_log.debug(f'creating new profile with uuid: {profile_name}')
        self._press_combination(['ctrl', 'shift', 'p'])
        self._press_combination(['tab'], repetitions=2)
        self._press_combination(['ctrl', ' '])
        self._type_str(profile_name)
        self._press_combination(['enter'])

    def _select_created_profile(self):
        app_log.debug('select created profile')
        self._press_combination(['shift', 'tab'])
        self._press_combination(['ctrl', ' '])

    def _login_anki_web(self, username, password):
        app_log.debug(f'login into anki web for user: {username}')
        self._press_combination(['y'])
        self._press_combination(['tab'], repetitions=2)
        self._type_str(username)
        self._press_combination(['tab'])
        self._type_str(password)
        self._press_combination(['enter'], delay_after_action=2)
        self._press_combination(['y'], delay_after_action=2)
        self._press_combination(['d'])

    def _press_combination(self, keys, repetitions=1, delay_after_action=.5):
        for _ in range(repetitions):
            for curr_key in keys:
                self._client.keyDown(curr_key)
            for curr_key in keys:
                self._client.keyUp(curr_key)
        time.sleep(delay_after_action)

    def _type_str(self, content, delay_after_action=.5):
        for curr_char in content:
            self._client.keyPress(curr_char)
        time.sleep(delay_after_action)

    # def api_push_card(self, anki_card: AnkiCard, headers: AnkiLoginResponseHeaders) -> bool:
    #     app_log.debug(f'push anki card: {str(anki_card)}')
    #     url = self.ANKI_API_BASE + '/add-card'
    #     data = asdict(anki_card)
    #     app_log.debug(f"push data '{data}' to url '{url}' with headers '{headers}'")
    #     return requests.get(url, json=data, headers=headers.to_map()).ok
