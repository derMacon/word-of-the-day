from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from src.logic.persistence_manager import PersistenceManager
from src.logic.selenium_utils import *
from src.types.token_type import TokenType
from src.utils.logging_config import log


def extract_client_token(token_type: TokenType):
    # TODO - delte whole method if the debug routine is obsolete
    # if 'DEBUG_TOKEN' in os.environ:
    #     token = os.environ['DEBUG_TOKEN']
    #     log.debug("using debug token: %s", token)
    #     return token

    token = request.headers.get(token_type.name)
    log.debug(f'extracted client token for type {token_type}: {token}')

    # TODO check that output is None if not existent - log this

    return token


class Controller:
    TIMEOUT_SEC = 3

    def __init__(self):
        service_obj = Service('./chromedriver-linux64/chromedriver')
        # self.driver = webdriver.Chrome(service=service_obj, options=set_chrome_options())
        # service_obj = Service('/usr/bin/chromedriver')
        self._driver = webdriver.Chrome(service=service_obj)
        self._cookie_manager = PersistenceManager()

    def login(self, email, password):
        self._insert_credentials(email, password)
        main_token = self._persist_main_token()
        card_token = self._persist_card_token()
        return main_token, card_token

    def _insert_credentials(self, email: str, password: str):
        log.debug("inside controller login")
        self._driver.get("https://ankiweb.net/account/login")
        insert_text(self._driver, "Email", email)
        insert_text(self._driver, "Password", password)
        self._driver.switch_to.active_element.send_keys(Keys.ENTER)

    def _persist_main_token(self):
        main_token = retrieve_token(self._driver, TIMEOUT_SEC)
        log.debug("main token: %s", main_token)
        if main_token is None:
            log.error('no auth flag retrieved - TODO throw exception')
            # TODO exception + handler

        cookies = self._driver.get_cookies()
        self._cookie_manager.insert_data(token_type=TokenType.MAINTOKEN, key=main_token, data=cookies)

        return main_token

    def _persist_card_token(self, ):
        self._driver.get("https://ankiweb.net/add")

        old_token = self._driver.get_cookie('ankiweb')

        # wait until new cookie values get grabbed / or wait a defined maximum number of ms
        ms_passed = 0
        offset = 0.05
        while self._driver.get_cookie('ankiweb') == old_token or ms_passed > 500:
            sleep(offset)
            ms_passed = ms_passed + offset

        cookies = self._driver.get_cookies()
        card_token = retrieve_token(self._driver)

        log.debug("card token: %s", card_token)
        self._cookie_manager.insert_data(token_type=TokenType.CARDTOKEN, key=card_token, data=cookies)
        return card_token

    def set_cookies(self, token_type: TokenType):
        token = extract_client_token(token_type)

        log.debug(f"token: {token}")

        self._driver.delete_all_cookies()
        self._driver.get("https://ankiweb.net/account/login")
        # self._driver.get('https://ankiweb.net/add')
        cookies = self._cookie_manager.read_data(token_type=token_type, key=token)

        if cookies is None:
            log.error(f'cookies not readable for token: {token}')
        else:
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def set_cookies2(self, token_type: TokenType):
        token = extract_client_token(token_type)

        log.debug(f"token: {token}")

        self._driver.delete_all_cookies()
        # self._driver.get("https://ankiweb.net/account/login")
        self._driver.get('https://ankiweb.net/add')
        cookies = self._cookie_manager.read_data(token_type=token_type, key=token)
        log.debug(cookies)

        if cookies is None:
            log.error(f'cookies not readable for token: {token}')
        else:
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def list_decks(self):
        self._driver.get('https://ankiweb.net/decks')
        self.set_cookies(TokenType.MAINTOKEN)
        # sleep(100)  # TODO delete this sleep
        main_elems = grab_main_elements(self._driver)
        return filter_deck_names(main_elems)

    def add_card(self, deck, front, back):
        self.set_cookies(TokenType.MAINTOKEN)
        self._driver.get('https://ankiweb.net/decks')
        # sleep(4)
        # self._driver.coo
        try:
            self.set_cookies2(TokenType.CARDTOKEN)
        except Exception as e:
            pass
        sleep(2)
        self._driver.get('https://ankiweb.net/add')
        try:
            self.set_cookies2(TokenType.CARDTOKEN)
        except Exception as e:
            pass
        self._driver.get('https://ankiweb.net/add')

        # self.login('spam.sh@gmx.de', 'admin')
        # self._driver.get('https://ankiweb.net/decks')
        # self._driver.get('https://ankiweb.net/account/settings')
        sleep(100)
        select_dropdown(self._driver, 'Deck', deck)
        insert_text(self._driver, 'Front', front)
        insert_text(self._driver, 'Back', back)

    def tear_down(self):
        self._driver.quit()
