# -*- coding: utf-8 -*-
import time
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
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(30)

        # Load test data
        with open('testing-data/login_data.json', 'r') as login_json_file:
            cls.login_data = json.load(login_json_file)

        with open('testing-data/data.json', 'r') as json_file:
            cls.test_data = json.load(json_file)

        with open('testing-data/elements.json', 'r') as elements_file:
            cls.elements = json.load(elements_file)

        cls.urls = cls.elements["urls"]
        cls.page_elements = cls.elements["elements"]

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
        login_data_path = 'testing-data/login_data.json'
        with open(login_data_path, 'r') as file:
            login_data = json.load(file)

        login_data["login_data"]["current_password"] = new_password

        with open(login_data_path, 'w') as file:
            json.dump(login_data, file, indent=4)

    def login(self, data):
        driver = self.driver
        driver.get(self.urls["home"])
        driver.get(self.urls["login"])
        time.sleep(3)
        driver.find_element(By.ID, self.page_elements["login"]["email_field"]).clear()
        driver.find_element(By.ID, self.page_elements["login"]["email_field"]).send_keys(data["email"])
        driver.find_element(By.ID, self.page_elements["login"]["password_field"]).clear()
        driver.find_element(By.ID, self.page_elements["login"]["password_field"]).send_keys(data["current_password"])
        driver.find_element(By.XPATH, self.page_elements["login"]["login_button"]).click()

    def run_test_case(self, data):
        driver = self.driver
        driver.get(self.urls["change_password"])
        time.sleep(3)
        driver.find_element(By.ID, self.page_elements["change_password"]["new_password_field"]).clear()
        driver.find_element(By.ID, self.page_elements["change_password"]["new_password_field"]).send_keys(data["new_password"])
        driver.find_element(By.ID, self.page_elements["change_password"]["confirm_password_field"]).clear()
        driver.find_element(By.ID, self.page_elements["change_password"]["confirm_password_field"]).send_keys(data["confirm_password"])
        driver.find_element(By.XPATH, self.page_elements["change_password"]["continue_button"]).click()

    def logout(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, self.page_elements["logout"]["my_account"]).click()
        driver.find_element(By.XPATH, self.page_elements["logout"]["logout_link"]).click()
        driver.find_element(By.LINK_TEXT, self.page_elements["logout"]["continue_button"]).click()

    def verify_error_message(self, element_key):
        xpath = self.page_elements["messages"].get(element_key)
        expected_message = self.page_elements["expect_mess"].get(element_key)

        if xpath and expected_message:
            if self.is_element_present(By.XPATH, xpath):
                error_message = self.driver.find_element(By.XPATH, xpath).text
                if error_message == expected_message:
                    print(f"✅ Error message matches: '{error_message}'")
                else:
                    print(f"❌ Error message does not match. Expected: '{expected_message}', Found: '{error_message}'")
            else:
                print(f"❌ Error message element not found for key: {element_key}")
        else:
            print(f"❌ Invalid element key: {element_key}")

    def test_case_01(self):
        """Test case 1: Change password successfully"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_01"]

        self.login(data_login)
        self.run_test_case(data)
        self.assertIn("account/account", self.driver.current_url)
        self.update_login_data(data["new_password"])
        self.logout()

        self.login(data_login)
        self.logout()

    def test_case_02(self):
        """Test case 2: Incorrect new_password"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_02"]
        self.login(data_login)
        self.run_test_case(data)

        self.verify_error_message("new_password_error")

        self.logout()

    def test_case_03(self):
        """Test case 3: Confirm password does not match"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_03"]
        self.login(data_login)
        self.run_test_case(data)

        self.verify_error_message("confirm_password_error")

        self.logout()

    def test_case_04(self):
        """Test case 4: Incorrect both fields"""
        data_login = self.__class__.login_data["login_data"]
        data = self.__class__.test_data["test_case_04"]
        self.login(data_login)
        self.run_test_case(data)

        self.verify_error_message("new_password_error")
        self.verify_error_message("confirm_password_error")

        self.logout()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

# class TestSuite(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.driver = webdriver.Chrome()
#         cls.driver.maximize_window()
#         cls.driver.implicitly_wait(30)
#         cls.base_url = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
#         cls.verificationErrors = []
#         cls.accept_next_alert = True

#         with open('testing-data/login_data.json', 'r') as login_json_file:
#             cls.login_data = json.load(login_json_file)

#         with open('testing-data/data.json', 'r') as json_file:
#             cls.test_data = json.load(json_file)

#     def setUp(self):
#         self.driver = self.__class__.driver

#     def is_element_present(self, how, what):
#         try: self.driver.find_element(by=how, value=what)
#         except NoSuchElementException as e: return False
#         return True
    
#     def is_alert_present(self):
#         try: self.driver.switch_to.alert
#         except NoAlertPresentException as e: return False
#         return True
    
#     def close_alert_and_get_its_text(self):
#         try:
#             alert = self.driver.switch_to.alert
#             alert_text = alert.text
#             if self.accept_next_alert:
#                 alert.accept()
#             else:
#                 alert.dismiss()
#             return alert_text
#         finally: self.accept_next_alert = True
    
#     def update_login_data(self, new_password):
#         """Cập nhật mật khẩu mới vào file JSON."""
#         login_data_path = 'testing-data/login_data.json'
#         with open(login_data_path, 'r') as file:
#             login_data = json.load(file)

#         login_data["login_data"]["current_password"] = new_password

#         with open(login_data_path, 'w') as file:
#             json.dump(login_data, file, indent=4)
    
#     def login(self, data):
#         driver = self.driver
#         driver.get(self.base_url)
#         driver.find_element(By.XPATH, "//div[@id='widget-navbar-217834']/ul/li[6]/a/div/span").click()
#         driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
#         time.sleep(3)
#         driver.find_element(By.ID, "input-email").clear()
#         driver.find_element(By.ID, "input-email").send_keys(data["email"])
#         driver.find_element(By.ID, "input-password").clear()
#         driver.find_element(By.ID, "input-password").send_keys(data["current_password"])
#         driver.find_element(By.XPATH, "//input[@value='Login']").click()

#     def run_test_case(self, data):
#         driver = self.driver
#         driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/password")
#         time.sleep(3)
#         driver.find_element(By.ID, "input-password").clear()
#         driver.find_element(By.ID, "input-password").send_keys(data["new_password"])
#         driver.find_element(By.ID, "input-confirm").clear()
#         driver.find_element(By.ID, "input-confirm").send_keys(data["confirm_password"])
#         driver.find_element(By.XPATH, "//input[@value='Continue']").click()

#     def logout(self):
#         driver = self.driver
#         driver.find_element(By.LINK_TEXT, "My account").click()
#         driver.find_element(By.XPATH, "//a[contains(text(),'Logout')]").click()
#         driver.find_element(By.LINK_TEXT, "Continue").click()

#     def verify_error_message(self, xpath, expected_message):
#         print("")
#         if self.is_element_present(By.XPATH, xpath):
#             error_message = self.driver.find_element(By.XPATH, xpath).text
#             if error_message == expected_message:
#                 print(f"✅ Error message matches: '{error_message}'")
#             else:
#                 print(f"❌ Error message does not match. Expected: '{expected_message}', Found: '{error_message}'")
#         else:
#             print(f"❌ Error message element not found at XPath: {xpath}")
            
#     def test_case_01(self):
#         """Test case 1: Change password successfully"""
#         data_login = self.__class__.login_data["login_data"]
#         data = self.__class__.test_data["test_case_01"]

#         self.login(data_login)
#         self.run_test_case(data)
#         self.assertIn("account/account", self.driver.current_url)    
#         self.update_login_data(data_login["current_password"])
#         self.logout()

#         self.login(data_login)
#         self.logout()

#     def test_case_02(self):
#         """Test case 2: Incorrect new_password"""
#         data_login = self.__class__.login_data["login_data"]
#         data = self.__class__.test_data["test_case_02"]
#         self.login(data_login)
#         self.run_test_case(data)

#         self.verify_error_message("//div[@id='content']/form/div/div/div", "Password must be between 4 and 20 characters!")

#         self.logout()

#     def test_case_03(self):
#         """Test case 3: Confirm password does not match"""
#         data_login = self.__class__.login_data["login_data"]
#         data = self.__class__.test_data["test_case_03"]
#         self.login(data_login)
#         self.run_test_case(data)

#         self.verify_error_message("//div[@id='content']/form/div[2]/div/div", "Password confirmation does not match password!")

#         self.logout()

#     def test_case_04(self):
#         """Test case 4: Incorrect both field"""
#         data_login = self.__class__.login_data["login_data"]
#         data = self.__class__.test_data["test_case_04"]
#         self.login(data_login)
#         self.run_test_case(data)

#         self.verify_error_message("//div[@id='content']/form/div/div/div", "Password must be between 4 and 20 characters!")
#         self.verify_error_message("//div[@id='content']/form/div[2]/div/div", "Password confirmation does not match password!")

#         self.logout()

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         if cls.verificationErrors:
#             print("Errors occurred:", cls.verificationErrors)
