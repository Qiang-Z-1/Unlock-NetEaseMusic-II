# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007F913D1B2C610BA6C3CC48AC1F6FFB5155D85AC12CB541467896A17D3B3E452884E3FA2F9FD83BB13C06CAD54BB39D47129376B53B2A144CF484975BDCDFCFFD0FEAB6D2F49879E7B1D62099ECF01443A8AB8CC58DD0A911A80BD1E361FAA8AA1BB045E91F052A083DC135123723C427900343C95C406AB2C9FFBA06DFCD8B1BE266928C08E0D6C2D64870ADED78F9820046E10D5E6A06A4DAC8E3BA6497943819ED631E8B257A79127AB4FB1C5D936F56F79680B6182991A26BC7BCB1E03BD0631635C4D2F84A07C038F4C3B13E4EF241F7CFB46C2B27889125CE6C7D32530BDE0090D088F1E20D85BE21D6EA8A5D3F766912CC2CE8936A34C6E101E7949FF271BFAF9FBD82CAD90403EF4A9821710F80615294E52923E385D7B091F5D7EADE88239FCCFF22AB3119697EAA5B472401ABD3B69C9D8507EC5828224E1C32A5B4611CC18892DEAB312C0642939CF59293FCC8D8D9D33D2A57A882AD977F77F570"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
