from time import sleep

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT_SEC = 3


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def check_if_logged_in(timeout=None):
    print('check if logged in')
    sec = 0
    found_cookie = False
    check_complete = False

    while not check_complete:

        for cookie in driver.get_cookies():
            print(f"cookie: {cookie}")
            found_cookie = found_cookie or cookie['name'] == 'has_auth'

        if timeout is not None:
            sleep(1)
            sec = sec + 1

        check_complete = check_complete or sec >= timeout or found_cookie

        print('wait')
    print('after eval')
    return found_cookie


def insert_text(label: str, input_text: str):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form"))
    )
    form_elems = element.find_elements(By.XPATH, "./child::*")
    field = next(filter(lambda elem: elem.text == label, form_elems), None)

    if not field:
        print(f'not able to find {label} field')
        # TODO throw exception

    field.find_element(By.XPATH, "./child::input").send_keys(input_text)


print('hi')
service_obj = Service('./chromedriver-linux64/chromedriver')
# service_obj = Service('/usr/bin/chromedriver')

driver = webdriver.Chrome(service=service_obj, options=set_chrome_options())
# driver = webdriver.Chrome(service=service_obj)

# driver.get('https://www.ankiweb.net/about')
driver.get('https://ankiweb.net/account/login')

for cookie in driver.get_cookies():
    print(f"cookie: {cookie}")

insert_text("Email", os.environ['EMAIL'])
insert_text("Password", os.environ['PASSWORD'])
driver.switch_to.active_element.send_keys(Keys.ENTER)

user_logged_in = check_if_logged_in(TIMEOUT_SEC)

print("user is logged in: ", user_logged_in)

# sleep(500)

driver.quit()
print('the end')
