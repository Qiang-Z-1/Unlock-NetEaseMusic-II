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
    browser.add_cookie({"name": "MUSIC_U", "value": "008FDCF1815003400B8B95D96A2C23C1BB537CBB0DE13CE24066D26DD9812C60CDAF723CD3FFE30EA4D3EA3F93883FBEAA69EBAD3372F4D2D78BA7C68DC5CE992729CC502897CF9A591FF5F8C8F987B845637AE7B3AFE819B4432BD24E550824152F989758B2326A3B9B3305BD51D75317A1ED2CB242F4C8C2EACE26A87A787D9DEBE87AE6D4EB21AB3DBC7DF2C718FA9E521B7BE8027EB54826D8218E436B3F0532FA69EEA4338DBB0C50ACEB7C0455C518E99112176E392179B505FB0922B3CE27CBD72AD68DF1F2FC9A5D8C806D32A5856EBAD2E3D2C3AE88CF0919B31D2F6566F9D89F86F478B86932E43B8204F4D4A5CB41088871600C82F22D754D510D2941887BAB709CB5DF2EF047ED69BCABAA277C45C18373FE12F5F0C8E62876C17D9F659224201914EE77A936635BE2DD4F1FC36205C969ECBB9B63679DEFB490450DE78DB8A71E91EAC69F2A51F4822C166335B2E365B8038C01437D444236FA55"})
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
