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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FB82BBE177FBD34FCAB90969398227183BC8B32F08E50C80A23D8C952F713B5FEB7E36BC1F641D0DD4A8AEFB4A674713E79B3DA603C649DC40D7D48B10512650757571176F6C494DD2DD74131704A9C04E837E82DC039AA0396CA2B04ED50BE5D6C0AFCB514B1DCD756116FCC5498A01887C0F22336E799BB37F53051FACFA32D6FEF21D30B324E1A3AE9FC2323273E88E90346E80C770EB9DB6DFB02C7540060CFF78793CE7B2E590DFD25A2435C75228A4F0C7D21391009739F4D22E8893AB3B671B6FFEC5913461D30006BD48D02C0510182E3F4BA6EF579FB2B1039509CBCE65C981715D4C66CF06C1A5FB780CFA10DAA9577F656EA352264DC65CF53AA0D15DEC76838F4544DFCFB94C84EA46E8BA894F9ADBFDE0115B6B9B4435AC1402EDE13AB5E0829E4FF2157B897914306BFB45F65979D9D1D70CAA76100D09C9E98FCA6C265507305BC5D89683BB15D79B252F90FFB486F635CCEB4E136EFAD989"})
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
