# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
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
    def wait_for_page_load(self, driver, timeout=10):
        """Đợi cho đến khi trang web tải xong."""
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
    def run_test_case_02(self, data):
        driver = self.driver
        driver.get(self.base_url)
        print("")

        for test_case in data:
            num = test_case["num"]
            limit = test_case["limit"]
            filters = test_case["filters"]

            driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=product%2Fsearch&search=")
            dropdown = Select(driver.find_element(By.ID, "input-limit-212463"))
            dropdown.select_by_visible_text(limit)
            for filter_xpath in filters:
                driver.find_element(By.XPATH, filter_xpath).click()
            
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            if self.is_element_present(By.XPATH,"//div[@id='entry_212470']/div/div[2]"):
                try:
                    message = driver.find_element(By.XPATH, "//div[@id='entry_212470']/div/div[2]").text
                    expected_message = "Showing 1 to 15 of 15 (1 Pages)"
                    if message == expected_message:
                        print(f"✅NumOfProduct: {num}. Limit: {limit}. Message matches: '{message}'")
                    else:
                        raise ValueError(f"❌ Message does not match. Expected: '{expected_message}', Found: '{message}'")
                except ValueError as e:
                    print(f"Exception: {e}")
            time.sleep(3)

    def test_case_02(self):
        """BVA02"""
        data = self.__class__.test_data["test_case_02"]
        self.run_test_case_02(data)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if cls.verificationErrors:
            print("Errors occurred:", cls.verificationErrors)
