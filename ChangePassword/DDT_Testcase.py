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

        with open('testing-data/login.json', 'r') as login_json_file:
            cls.login_data = json.load(login_json_file)

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
    
    def update_login_data(self, new_password):
        """Cập nhật mật khẩu mới vào file JSON."""
        login_data_path = 'testing-data/login.json'
        with open(login_data_path, 'r') as file:
            login_data = json.load(file)

        login_data["login_data"]["current_password"] = new_password

        with open(login_data_path, 'w') as file:
            json.dump(login_data, file, indent=4)
    
    def login(self, data):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.XPATH, "//div[@id='widget-navbar-217834']/ul/li[6]/a/div/span").click()
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        driver.find_element(By.ID, "input-email").clear()
        driver.find_element(By.ID, "input-email").send_keys(data["email"])
        driver.find_element(By.ID, "input-password").clear()
        driver.find_element(By.ID, "input-password").send_keys(data["current_password"])
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

    def run_test_case(self, data):
        driver = self.driver
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/password")
        driver.find_element(By.ID, "input-password").clear()
        driver.find_element(By.ID, "input-password").send_keys(data["new_password"])
        driver.find_element(By.ID, "input-confirm").clear()
        driver.find_element(By.ID, "input-confirm").send_keys(data["confirm_password"])
        driver.find_element(By.XPATH, "//input[@value='Continue']").click()

        # # Check for success or error message
        # if self.is_element_present(By.CLASS_NAME, "alert-success"):
        #     print("Password changed successfully.")
        # elif self.is_element_present(By.CLASS_NAME, "alert-danger"):
        #     error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
        #     print(f"Error: {error_message}")

    def logout(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "My account").click()
        driver.find_element(By.XPATH, "//a[contains(text(),'Logout')]").click()
        driver.find_element(By.LINK_TEXT, "Continue").click()
    
    # def click_continue(self):
    #     self.driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    def test_case_01(self):
        """Test case 1: Change password successfully"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_01"]

        self.login(data_login)
        self.run_test_case(data)
        self.assertIn("account/account", self.driver.current_url)    
        self.update_login_data(data_login["current_password"])
        self.logout()

        self.login(data_login)
        self.logout()

    def test_case_02(self):
        """Test case 2: Incorrect new_password"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_02"]
        self.login(data_login)
        self.run_test_case(data)

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/div/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/div/div/div").click()

        self.logout()

    def test_case_03(self):
        """Test case 3: Confirm password does not match"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_03"]
        self.login(data_login)
        self.run_test_case(data)

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/div[2]/div/div").click()

        self.logout()

    def test_case_04(self):
        """Test case 4: Incorrect both field"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_04"]
        self.login(data_login)
        self.run_test_case(data)

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/div/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/div/div/div").click()

        if self.is_element_present(By.XPATH, "//div[@id='content']/form/div[2]/div/div"):
            self.driver.find_element(By.XPATH, "//div[@id='content']/form/div[2]/div/div").click()

        self.logout()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if cls.verificationErrors:
            print("Errors occurred:", cls.verificationErrors)
