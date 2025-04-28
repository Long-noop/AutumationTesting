# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import unittest
import json
import os   

class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)
        cls.base_url = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
        cls.verificationErrors = []
        cls.accept_next_alert = True

        with open('testing-data/data.json', 'r') as json_file:
            cls.test_data = json.load(json_file)

    def setUp(self):
        self.driver = self.__class__.driver

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to.alert
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def run_test_case_05(self, data):
        driver = self.driver
        driver.get(self.base_url)
        num = data["num"]
        limit = data["limit"]
        pages = data["pages"]
        expect_mess = data["expect_mess"] 
        print("")

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        dropdown = Select(driver.find_element(By.ID, "input-limit-212463"))
        dropdown.select_by_visible_text(limit)

        driver.find_element(By.XPATH, "//div[@id='mz-filter-panel-0-4']/div/div/div/label").click()
        time.sleep(7)

        try:
            for i in range(0, int(pages)):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                if i == 0:
                    print(f"✅ Successfully navigated to page {i + 1}.")
                if i > 0 and i < int(pages):
                    try:
                        driver.find_element(By.LINK_TEXT, str(i + 1)).click()
                        # time.sleep(2)
                        print(f"✅ Successfully navigated to page {i + 1}.")
                    except NoSuchElementException:
                        print(f"❌ Page {i + 1} link not found.")
                        break

                element = driver.find_element(By.XPATH, "//div[@id='entry_212470']/div/div[2]")
                message = element.text
                expected_message = expect_mess.get(f"page{i + 1}", "")
                if expected_message == message:
                    print(f"NumOfProduct: {num}. Limit: {limit}. Page {i + 1}. Message matches: '{message}")
                else:
                    raise ValueError(f"❌ Page {i + 1}. Message does not match. Expected: '{expected_message}', Found: '{message}'")

        except NoSuchElementException:
            print("❌ Page 2 link not found.")
        except ValueError as e:
            print(f"Exception: {e}")

    def test_case_05(self):
        """BVA05"""
        data = self.__class__.test_data["test_case_05"]
        self.run_test_case_05(data)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if cls.verificationErrors:
            print("Errors occurred:", cls.verificationErrors)
