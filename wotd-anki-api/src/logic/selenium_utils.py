from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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


def retrieve_token(driver, timeout=None):
    print('check if logged in')
    sec = 0
    check_complete = False
    token = None

    while not check_complete:

        for cookie in driver.get_cookies():
            print(f"cookie: {cookie}")
            if cookie['name'] == 'ankiweb':
                token = cookie['value']

        if timeout is not None:
            sleep(1)
            sec = sec + 1

        check_complete = check_complete or sec >= timeout or token is not None

        print('wait')
    print('after eval')
    return token

def insert_text(driver, label: str, input_text: str):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form"))
    )
    form_elems = element.find_elements(By.XPATH, "./child::*")
    field = next(filter(lambda elem: elem.text == label, form_elems), None)

    if not field:
        print(f'not able to find {label} field')
        # TODO throw exception

    field.find_element(By.XPATH, "./child::input").send_keys(input_text)


def select_dropdown(driver, label: str, option: str):
    pass


def grab_main_elements(driver):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//main"))
    )
    return element.find_elements(By.XPATH, "./child::*")


def filter_deck_names(main_elements):
    out = []
    for curr_elem in main_elements[:-2]:
        out.append(curr_elem.text.split('\n')[0].strip())
    return out
