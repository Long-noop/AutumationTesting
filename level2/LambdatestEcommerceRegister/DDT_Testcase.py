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
        cls.verificationErrors = []
        cls.accept_next_alert = True

        # Load test data
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

    def verify_error_message(self, element_key):
        xpath = self.page_elements["messages"].get(element_key)
        expected_message = self.page_elements["expect_mess"].get(element_key)
        print("")
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

    def run_test_case(self, data):
        driver = self.driver
        driver.get(self.urls["home"])
        driver.get(self.urls["register"])

        # Điền thông tin vào các trường
        driver.find_element(By.ID, self.page_elements["register"]["firstname_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["firstname_field"]).send_keys(data.get('firstname', ''))

        driver.find_element(By.ID, self.page_elements["register"]["lastname_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["lastname_field"]).send_keys(data.get('lastname', ''))

        driver.find_element(By.ID, self.page_elements["register"]["email_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["email_field"]).send_keys(data.get('email', ''))

        driver.find_element(By.ID, self.page_elements["register"]["telephone_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["telephone_field"]).send_keys(data.get('telephone', ''))

        driver.find_element(By.ID, self.page_elements["register"]["password_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["password_field"]).send_keys(data.get('password', ''))

        driver.find_element(By.ID, self.page_elements["register"]["confirm_password_field"]).clear()
        driver.find_element(By.ID, self.page_elements["register"]["confirm_password_field"]).send_keys(data.get('confirm_password', ''))

        driver.find_element(By.XPATH, self.page_elements["register"]["privacy_policy_checkbox"]).click()

    def logout(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, self.page_elements["logout"]["my_account"]).click()
        driver.find_element(By.XPATH, self.page_elements["logout"]["logout_link"]).click()
        driver.find_element(By.LINK_TEXT, self.page_elements["logout"]["continue_button"]).click()
    
    def click_continue(self):
        self.driver.find_element(By.XPATH, self.page_elements["register"]["continue_button"]).click()

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

        self.verify_error_message("firstname_error") 

    def test_case_03(self):
        """Test case 3: Register with invalid lastname"""
        data = self.__class__.test_data["test_case_03"]
        self.run_test_case(data)
        self.click_continue()

        self.verify_error_message("lastname_error")

    def test_case_04(self):
        """Test case 4: Register with missing telephonenumber"""
        data = self.__class__.test_data["test_case_04"]
        self.run_test_case(data)
        self.click_continue()

        self.verify_error_message("telephone_error")

    def test_case_05(self):
        """Test case 5: Register with invalid email"""
        data = self.__class__.test_data["test_case_05"]
        self.run_test_case(data)
        self.click_continue()

        self.verify_error_message("email_error")

    def test_case_06(self):
        """Test case 6: Register with invalid password"""
        data = self.__class__.test_data["test_case_06"]
        self.run_test_case(data)
        self.click_continue()

        self.verify_error_message("password_error")

    def test_case_07(self):
        """Test case 7: Register with confirm password miss matched"""
        data = self.__class__.test_data["test_case_07"]
        self.run_test_case(data)
        self.click_continue()

        self.verify_error_message("confirm_password_error")

    def test_case_08(self):
        """Test case 8: Register with not accept privacy policy"""
        data = self.__class__.test_data["test_case_08"]
        self.run_test_case(data)

        self.driver.find_element(By.XPATH, self.page_elements["register"]["privacy_policy_checkbox"]).click()
        self.click_continue()

        self.verify_error_message("privacy_policy_error")

    def test_case_09(self):
        """Test case 9: Register fail with all invalid filed"""
        data = self.__class__.test_data["test_case_09"]
        self.run_test_case(data)

        self.driver.find_element(By.XPATH, self.page_elements["register"]["privacy_policy_checkbox"]).click()
        self.click_continue()

        self.verify_error_message("firstname_error")
        self.verify_error_message("lastname_error")
        self.verify_error_message("email_error")
        self.verify_error_message("telephone_error")
        self.verify_error_message("password_error")
        self.verify_error_message("confirm_password_error")
        self.verify_error_message("privacy_policy_error")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        if cls.verificationErrors:
            print("Errors occurred:", cls.verificationErrors)
