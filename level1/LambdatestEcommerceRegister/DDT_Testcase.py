# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import unittest
import json
import os   

class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
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

    def run_test_case(self, data):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.LINK_TEXT, "My account").click()
        driver.find_element(By.LINK_TEXT, "Register").click()

        driver.find_element(By.ID, "input-firstname").clear()
        driver.find_element(By.ID, "input-firstname").send_keys(data.get('firstname', ''))

        driver.find_element(By.ID, "input-lastname").clear()
        driver.find_element(By.ID, "input-lastname").send_keys(data.get('lastname', ''))

        driver.find_element(By.ID, "input-email").clear()
        driver.find_element(By.ID, "input-email").send_keys(data.get('email', ''))

        driver.find_element(By.ID, "input-telephone").clear()
        driver.find_element(By.ID, "input-telephone").send_keys(data.get('telephone', ''))

        driver.find_element(By.ID, "input-password").clear()
        driver.find_element(By.ID, "input-password").send_keys(data.get('password', ''))

        driver.find_element(By.ID, "input-confirm").clear()
        driver.find_element(By.ID, "input-confirm").send_keys(data.get('confirm_password', ''))

        driver.find_element(By.XPATH, "//div[@id='content']/form/div/div/div/label").click()

    def logout(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "My account").click()
        driver.find_element(By.XPATH, "//a[contains(text(),'Logout')]").click()
        driver.find_element(By.LINK_TEXT, "Continue").click()
    
    def click_continue(self):
        self.driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    def test_case_01(self):
        """Test case 1: Register with valid data"""
        data = self.__class__.test_data["test_case_01"]
        self.run_test_case(data)
        self.click_continue()
        self.assertIn("account/success", self.driver.current_url)    

        self.logout()

    def test_case_02(self):
        """Test case 2: Register with missing firstname"""
        data = self.__class__.test_data["test_case_02"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[2]/div/div").click()

        # if self.is_alert_present():
        #     alert_text = self.close_alert_and_get_its_text()
        #     print(f"Alert appeared: {alert_text}")

    def test_case_03(self):
        """Test case 3: Register with invalid lastname"""
        data = self.__class__.test_data["test_case_03"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[3]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[3]/div/div").click()
    
    def test_case_04(self):
        """Test case 4: Register with missing telephonenumber"""
        data = self.__class__.test_data["test_case_04"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[5]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[5]/div/div").click()

    def test_case_05(self):
        """Test case 5: Register with invalid email"""
        data = self.__class__.test_data["test_case_05"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[4]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[4]/div/div").click()
    
    def test_case_06(self):
        """Test case 6: Register with invalid password"""
        data = self.__class__.test_data["test_case_06"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/fieldset[2]/div/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/fieldset[2]/div/div/div").click()

    def test_case_07(self):
        """Test case 7: Register with confirm password miss matched"""
        data = self.__class__.test_data["test_case_07"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/fieldset[2]/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/fieldset[2]/div[2]/div/div").click()
    
    def test_case_08(self):
        """Test case 8: Register with not accept privacy policy"""
        data = self.__class__.test_data["test_case_08"]
        self.run_test_case(data)

        self.driver.find_element(By.XPATH, "//div[@id='content']/form/div/div/div/label").click()
        self.click_continue()

        if self.is_element_present(By.XPATH, "//div[@id='account-register']/div"):
            self.driver.find_element(By.XPATH, "//div[@id='account-register']/div").click()

    def test_case_09(self):
        """Test case 9: Register fail with all invalid filed"""
        data = self.__class__.test_data["test_case_09"]
        self.run_test_case(data)
        self.click_continue()

        if self.is_element_present(By.XPATH, "//div[@id='account-register']/div"):
            self.driver.find_element(By.XPATH, "//div[@id='account-register']/div").click()
        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[2]/div/div").click()
        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[3]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[3]/div/div").click()
        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[4]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[4]/div/div").click()
        if self.is_element_present(By.XPATH, "//fieldset[@id='account']/div[5]/div/div"):
            self.driver.find_element(By.XPATH, "//fieldset[@id='account']/div[5]/div/div").click()
        if self.is_element_present(By.XPATH, "//div[@id='content']/form/fieldset[2]/div/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/fieldset[2]/div/div/div").click()
        if self.is_element_present(By.XPATH, "//div[@id='content']/form/fieldset[2]/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/fieldset[2]/div[2]/div/div").click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if cls.verificationErrors:
            print("Errors occurred:", cls.verificationErrors)
