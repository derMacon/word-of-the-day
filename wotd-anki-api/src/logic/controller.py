import os

from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from src.logic.persistence_manager import PersistenceManager
from src.logic.selenium_utils import *
from src.utils.logging_config import log


def extract_bearer_token():
    if 'DEBUG_TOKEN' in os.environ:
        token = os.environ['DEBUG_TOKEN']
        log.debug("using debug token: %s", token)
        return token

    authorization_header = request.headers.get('Authorization')

    out = None
    if authorization_header and authorization_header.startswith('Bearer '):
        # Extract the token by removing the 'Bearer ' prefix
        bearer_token = authorization_header[len('Bearer '):]

        # Now 'bearer_token' contains the Bearer token
        log.debug(f"Bearer Token: {bearer_token}")
        out = bearer_token
    else:
        log.error("No Bearer token found in the Authorization header")

    return out


class Controller:
    TIMEOUT_SEC = 3

    def __init__(self):
        service_obj = Service('./chromedriver-linux64/chromedriver')
        # self.driver = webdriver.Chrome(service=service_obj, options=set_chrome_options())
        # service_obj = Service('/usr/bin/chromedriver')
        self._driver = webdriver.Chrome(service=service_obj)
        self._cookie_manager = PersistenceManager()

    def login(self, email, password):
        log.debug("inside controller login")
        self._driver.get("https://ankiweb.net/account/login")
        insert_text(self._driver, "Email", email)
        insert_text(self._driver, "Password", password)
        self._driver.switch_to.active_element.send_keys(Keys.ENTER)

        token = retrieve_token(self._driver, TIMEOUT_SEC)
        log.debug("main token: %s", token)
        if token is None:
            log.error('no auth flag retrieved - TODO throw exception')
            # TODO exception + handler

        cookies = self._driver.get_cookies()
        self._cookie_manager.insert_data(key=token, data=cookies)

        self._driver.get("https://ankiweb.net/add")

        ms_passed = 0
        offset = 0.05
        while self._driver.get_cookie('ankiweb') == token or ms_passed > 500:
            sleep(offset)
            ms_passed = ms_passed + offset

        sleep(3)
        cookies = self._driver.get_cookies()
        token = retrieve_token(self._driver)
        log.debug("card token: %s", token)

        sleep(10)
        return token

    def set_cookies(self):
        token = extract_bearer_token()
        log.debug(f"token: {token}")
        self._driver.delete_all_cookies()
        self._driver.get("https://ankiweb.net/account/login")
        cookies = self._cookie_manager.read_data(token)
        if cookies is None:
            log.error(f'cookies not readable for token: {token}')
        else:
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def list_decks(self):
        self.set_cookies()
        self._driver.get('https://ankiweb.net/decks')
        sleep(100) # TODO delete this sleep
        main_elems = grab_main_elements(self._driver)
        return filter_deck_names(main_elems)

    def add_card(self, deck, front, back):
        self.set_cookies()
        sleep(3)
        # self.login('spam.sh@gmx.de', 'admin')
        # self._driver.get('https://ankiweb.net/decks')
        # self._driver.get('https://ankiweb.net/add')
        self._driver.get('https://ankiweb.net/account/settings')
        sleep(100)
        select_dropdown(self._driver, 'Deck', deck)
        insert_text(self._driver, 'Front', front)
        insert_text(self._driver, 'Back', back)

    def tear_down(self):
        self._driver.quit()
