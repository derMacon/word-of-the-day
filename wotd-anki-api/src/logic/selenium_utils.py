from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.logging_config import log

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
    log.debug('check if logged in, timeout: %s', timeout)
    sec = 0
    check_complete = False
    token = None

    while not check_complete:

        for cookie in driver.get_cookies():
            if cookie['name'] == 'ankiweb':
                token = cookie['value']

        if timeout is not None:
            sleep(1)
            sec = sec + 1

        check_complete = (timeout is None or sec >= timeout
                          or token is not None or check_complete)

    return token


def insert_text_by_placeholder(driver, placeholder: str, input_text: str):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form"))
    )
    form_elems = element.find_elements(By.XPATH, "./child::*")
    field = next(filter(lambda elem: elem.text == placeholder, form_elems), None)

    if not field:
        print(f'not able to find {placeholder} field')
        # TODO throw exception

    field.find_element(By.XPATH, "./child::input").send_keys(input_text)


def insert_text_by_label(driver, label: str, input_text: str):
    label_elem = find_label(driver, label)
    sibling = find_next_sibling(label_elem)
    text_box = find_first_child(sibling)
    text_box.send_keys(input_text)


def find_label(driver, text: str):
    span_xpath = f"//span[text()='{text}']"
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, span_xpath))
    )


def find_next_sibling(elem: WebElement):
    return elem.find_element(By.XPATH, './following-sibling::*')


def find_first_child(elem: WebElement):
    out = elem.find_elements(By.XPATH, './child::*')
    if out:
        return out[0]
    log.error(f"no child element found for: {elem}")
    return None


def select_dropdown(driver, label: str, option_title: str):
    label_elem = find_label(driver, label)
    sibling = find_next_sibling(label_elem)
    dropdown_element = sibling.find_element(By.CLASS_NAME, "svelte-select")
    dropdown_element.click()

    # Wait for the dropdown options to be visible (adjust the timeout as needed)
    wait = WebDriverWait(driver, 10)
    dropdown_options = (wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'svelte-select-list')))[0]
                        .find_elements(By.XPATH, './child::*'))
    option_str = [opt.text for opt in dropdown_options]
    log.debug(f"dropdown for {label} has the following options: {option_str}")

    option_idx = option_str.index(option_title)
    dropdown_options[option_idx].click()


def insert_text_in_alert(driver, text: str):
    alert = Alert(driver)
    alert.send_keys(text)
    alert.accept()


def click_button(driver, title: str):
    available_buttons = driver.find_elements(By.XPATH, '//button')
    options = [btn.text for btn in available_buttons]
    log.debug(f"searching button with title '{title}' in available buttons: {options}")
    btn_idx = options.index(title)
    available_buttons[btn_idx].click()


def find_nth_child(elem: WebElement, n: int):
    out = elem.find_elements(By.XPATH, './child::*')
    if out and len(out) > n:
        return out[n]
    log.error(f"no child element found for n = {n} in: {elem}")
    return None


def grab_main_elements(driver):
    sleep(.1)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//main"))
    )
    sleep(.1)
    return element.find_elements(By.XPATH, "./child::*")


def filter_deck_names(main_elements):
    out = []
    for curr_elem in main_elements[:-2]:
        out.append(curr_elem.text.split('\n')[0].strip())
    return out
