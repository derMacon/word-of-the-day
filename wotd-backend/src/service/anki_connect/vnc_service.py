import filecmp
import os
import socket
import time
import uuid

from singleton_decorator import singleton
from vncdotool import api

from src.data.error.anki_vnc_error import AnkiVncError
from src.service.anki_connect.anki_connect_fetcher import AnkiConnectFetcher
from src.utils.logging_config import app_log

LOGIN_MAX_RETRIES = 3
# TODO do we need these?
NEED_TO_LOGIN_SCREENSHOT_01 = 'res/vnc/expected-screens/need-to-download-collection-after-login-01.png'
NEED_TO_LOGIN_SCREENSHOT_02 = 'res/vnc/expected-screens/need-to-download-collection-after-login-02.png'
NEED_TO_LOGIN_SCREENSHOT_03 = 'res/vnc/expected-screens/need-to-download-collection-after-login-03.png'
INVALID_CREDENTIALS = 'res/vnc/expected-screens/invalid-credentials.png'
ACCOUNT_REQUIRED = 'res/vnc/expected-screens/account-required-pop-up.png'
EMPTY_COLLECTION = 'res/vnc/expected-screens/empty-collection.png'
CURR_SCREENSHOT_PATH = 'res/vnc/screenshots-at-runtime/screenshot.png'


@singleton
class VncService:
    """
    Since the anki connect addon does not provide the ability to login new users I implemented a simple workaround
    using a vnc viewer where it is possible to create new profiles (including setting the existing credentials for
    anki web) via shortcuts that are propaged through the viewer to the running anki desktop application. This
    application runs inside a docker container to be able to deploy it on a server.
    """

    def __init__(self):
        anki_connect_hostname = os.environ.get('ANKI_CONNECT_HOST', 'localhost')
        anki_connect_ip = socket.gethostbyname(anki_connect_hostname)
        anki_connect_login_port = os.environ.get('ANKI_CONNECT_LOGIN_PORT', 5900)

        self.anki_connect_login_address_vnc = f'{anki_connect_ip}::{anki_connect_login_port}'
        app_log.debug(f"init vnc client with login address: '{self.anki_connect_login_address_vnc}'")
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

        if AnkiConnectFetcher.check_if_profile_present(profile_name):
            raise AnkiVncError('anki profile already present - should not be the case since we want to create '
                               'a new profile')
        self._create_new_profile(profile_name)
        self._select_created_profile()
        self._login_anki_web(username, password)

        if not self._invalid_credentials() and AnkiConnectFetcher.check_if_profile_present(profile_name):
            app_log.debug(f'login mechanism run complete for new profile with uuid: {profile_name}')
            return profile_name

        raise AnkiVncError(f'login failed for {username} with profile uuid {profile_name}')

    def _create_new_profile(self, profile_name: str):
        app_log.debug(f'creating new profile with uuid: {profile_name}')
        self._press_combination(['ctrl', 'shift', 'p'], delay_after_action=2)
        self._press_combination(['tab'], repetitions=2)
        self._press_combination(['ctrl', ' '])
        self._type_str(profile_name)
        self._press_combination(['enter'])

    def _select_created_profile(self):
        app_log.debug('select created profile')
        # self._press_combination(['d'], delay_after_action=2)
        self._press_combination(['shift', 'tab'])
        self._press_combination(['ctrl', ' '])

    def _login_anki_web(self, username, password):
        app_log.debug(f'login into anki web for user: {username}')
        self._press_combination(['y'], delay_after_action=2)

        app_log.debug('entering credentials')
        self._click_mouse(450, 403)
        self._type_str(username)
        self._press_combination(['tab'])
        self._type_str(password)
        self._press_combination(['enter'], delay_after_action=2)
        self._press_combination(['y'])
        self._press_combination(['d'])
        self._select_need_to_download_content_pop_up()

        app_log.debug(f'after loging in for user: {username}')

    def _press_combination(self, keys, repetitions=1, delay_after_action=.5):
        for _ in range(repetitions):
            for curr_key in keys:
                self._client.keyDown(curr_key)
            for curr_key in keys:
                self._client.keyUp(curr_key)
        time.sleep(delay_after_action)

    def _click_mouse(self, x_pos: int, y_pos: int, delay_after_action=0):
        app_log.debug(f'clicking mouse at: ({x_pos}, {y_pos})')
        self._client.mouseMove(x_pos, y_pos)
        self._client.mouseDown(1)
        self._client.mouseUp(1)
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

    # def _sync_credentials_were_confirmed(self):
    #     app_log.debug('before capturing screenshot')
    #     self._client.captureScreen(CURR_SCREENSHOT_PATH)
    #     # user_needs_to_select_remote_download = filecmp.cmp(CURR_SCREENSHOT_PATH, NEED_TO_LOGIN_SCREENSHOT)
    #     # app_log.debug(f'user needs to select remote download from pop up: {user_needs_to_select_remote_download}')

    def _select_need_to_download_content_pop_up(self):
        app_log.debug('before capturing screenshot')
        self._client.captureScreen(CURR_SCREENSHOT_PATH)
        user_needs_to_select_remote_download = filecmp.cmp(CURR_SCREENSHOT_PATH, NEED_TO_LOGIN_SCREENSHOT_01)
        app_log.debug(f'user needs to select remote download from pop up: {user_needs_to_select_remote_download}')

        if user_needs_to_select_remote_download:
            app_log.debug('user clicking button download button')
            # self._client.mouseMove(480, 510)
            # self._client.mouseDown(1)
            # self._client.mouseUp(1)
            self._click_mouse(480, 510)

    def _invalid_credentials(self) -> bool:
        app_log.debug('before capturing credential screen screenshot')
        self._client.captureScreen(CURR_SCREENSHOT_PATH)
        invalid_credentials = filecmp.cmp(CURR_SCREENSHOT_PATH, INVALID_CREDENTIALS)
        app_log.debug(f'user needs provided invalid credentials: {invalid_credentials}')

        if invalid_credentials:
            self._press_combination(['enter'])  # acknowledge invalid creds screen
            self._click_mouse(560, 470)  # cancel account required pop up

        return invalid_credentials

    def _account_required_screen(self) -> bool:
        app_log.debug('before capturing credential screen screenshot')
        self._client.captureScreen(CURR_SCREENSHOT_PATH)
        account_required = filecmp.cmp(CURR_SCREENSHOT_PATH, ACCOUNT_REQUIRED)
        app_log.debug(f'user needs to provide credentials: {account_required}')
        return account_required

    def confirm_sync(self) -> None:
        time.sleep(2)
        # clicking 'download from anki web'
        self._click_mouse(480, 510, delay_after_action=.5)
        self._click_mouse(480, 510)

        app_log.debug('confirming sync')
        self._press_combination(['y'], delay_after_action=1)
        self._click_mouse(635, 380, delay_after_action=.5)
        self._click_mouse(635, 380, delay_after_action=.5)


    def _test(self) -> bool:
        app_log.debug('test')
        self._client.captureScreen(CURR_SCREENSHOT_PATH)
        # account_required = filecmp.cmp(CURR_SCREENSHOT_PATH, EMPTY_COLLECTION)
        # app_log.debug(f'out: {account_required}')
        # return account_required
        return True
