import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

print('hi')
# service_obj = Service('./chromedriver-linux64/chromedriver')
service_obj = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service_obj, options=set_chrome_options())

driver.get('https://www.wikipedia.de')

elements_with_text = driver.find_elements(By.XPATH, "//*[text()]")

# Extract and print the text from each element
for element in elements_with_text:
    print(element.text)

driver.quit()
print('the end')
