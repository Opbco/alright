"""
Alright is unofficial Python wrapper for whatsapp web made as an inspiration from PyWhatsApp
allowing you to send messages, images, video and documents programmatically using Python
"""

import re
import os
import sys
import time
import logging
import platformdirs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
    TimeoutException,
)
from webdriver_manager.chrome import ChromeDriverManager
from functools import wraps
import requests

LOGGER = logging.getLogger()


def retry(num_retries, exception_to_check, sleep_time=0):
    """
    Decorator that retries the execution of a function if it raises a specific exception.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, num_retries+1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(
                        f"{func.__name__} raised {e.__class__.__name__}. Retrying...")
                    if i < num_retries:
                        time.sleep(sleep_time)
            # Raise the exception if the function was not successful after the specified number of retries
            raise e
        return wrapper
    return decorate


class WhatsAppMinfopra(object):
    def __init__(self, browser=None, time_out=600):
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout

        self.BASE_URL = "https://dossier.minfopra.gov.cm/"
        self.MINESEC_BASE_URL = "https://minesecdrh.cm/api/"

        if not browser:
            browser = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=self.chrome_options,
            )

            handles = browser.window_handles
            for _, handle in enumerate(handles):
                if handle != browser.current_window_handle:
                    browser.switch_to.window(handle)
                    browser.close()

        self.browser = browser
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        self.wait = WebDriverWait(self.browser, time_out)
        self.cli()
        self.login()

    @property
    def chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument(
            "--user-data-dir=" + platformdirs.user_data_dir("OPBco")
        )
        if sys.platform == "win32":
            chrome_options.add_argument("--profile-directory=Default")
        else:
            chrome_options.add_argument("start-maximized")
        return chrome_options

    def cli(self):
        """
        LOGGER settings  [nCKbr]
        """
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s -- [%(levelname)s] >> %(message)s"
            )
        )
        LOGGER.addHandler(handler)
        LOGGER.setLevel(logging.INFO)

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def catch_alert(self, seconds=10):
        """catch_alert()

        catches any sudden alert
        """
        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            LOGGER.exception(f"An exception occurred: {e}")
            return False

    @retry(num_retries=3, exception_to_check=UnexpectedAlertPresentException, sleep_time=1)
    def enter_name_matricule(self, name_matricule):
        search_box = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="code_dossier"]',
                )
            )
        )
        search_box.clear()
        search_box.send_keys(name_matricule)
        search_box.send_keys(Keys.ENTER)
        try:
            element_present = EC.presence_of_all_elements_located((By.XPATH, "//table[contains(@class, 'table_dossier_ajax')]/tbody"))
            messages  = self.wait.until(element_present)
            clean_messages = []
            for message in messages:
                _message = WhatsAppMinfopra.clean_message(message)
                if _message is None:
                    LOGGER.info(f"Unknown message format: {_message}")
                else:
                    clean_messages.append(_message)
            return clean_messages
        except TimeoutException:
            print("Timed out waiting for page to load")

    @staticmethod
    def clean_message(messager):
        _message = messager.text.split("\n")
        message = {
            "sender": '',
            "time": '',
                    "message": "",
                    "unread": False,
                    "no_of_unread": 0,
                    "group": False,
        }
        if len(_message) == 2:
            message["sender"] = _message[0]
            message["time"] = _message[1]
        elif len(_message) == 3:
            message["sender"] = _message[0]
            message["time"] = _message[1]
            message["message"] = _message[2]
        elif len(_message) == 4:
            message["sender"] = _message[0]
            message["time"] = _message[1]
            message["message"] = _message[2]
            message["unread"] = _message[-1].isdigit()
            message["no_of_unread"] = int(
                _message[-1]) if _message[-1].isdigit() else 0
        elif len(_message) == 5:
            message["sender"] = _message[0]
            message["time"] = _message[1]
            message["message"] = ""
            message["unread"] = _message[-1].isdigit()
            message["no_of_unread"] = int(
                _message[-1]) if _message[-1].isdigit() else 0
            message["group"] = False
        elif len(_message) == 6:
            message["sender"] = _message[0]
            message["time"] = _message[1]
            message["message"] = _message[4]
            message["unread"] = _message[-1].isdigit()
            message["no_of_unread"] = int(
                _message[-1]) if _message[-1].isdigit() else 0
            message["group"] = True
        else:
            message = None

        return message
