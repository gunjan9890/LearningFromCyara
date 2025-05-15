import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from train_search_result_page import TrainSearchResultPage


class TrainSearchPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.login_button: str = "//a[normalize-space()='LOGIN']"
        self.username_field: str = "//input[@formcontrolname='userid']"
        self.password_field: str = "//input[@formcontrolname='password']"
        self.captcha_field: str = "//input[@formcontrolname='captcha']"
        self.sign_in_button: str = "//button[normalize-space()='SIGN IN']"
        self.my_account_link: str = "//a[contains(text(),'MY ACCOUNT')]"

        # search form
        self.from_field: str = "//*[contains(@aria-label,'Enter From station')]//input"
        self.to_field: str = "//*[contains(@aria-label,'Enter To station')]//input"
        self.journey_date: str = "//*[contains(@aria-label,'Enter Journey Date')]//input"
        self.journey_class: str = "//*[@id='journeyClass']/div"
        self.journey_quota: str = "//*[@id='journeyQuota']/div"
        self.search_button: str = "//button[normalize-space()='Search']"

        # commons
        self.auto_complete_div: str = "//ul[contains(@class,'autocomplete')]"
        self.dropdown_div: str = "//ul[contains(@class,'dropdown-items')]"

    def open_irctc_search_page(self) -> None:
        self.driver.get("https://www.irctc.co.in/nget/train-search")

    def is_logged_in(self) -> bool:
        '''
        Checks if the user is already logged in or not
        :return:
        '''

        lst = self.driver.find_elements("xpath", self.login_button)
        if len(lst) > 0:
            return lst[0].is_displayed()
        return False

    def login_to_irctc(self, username: str, password: str) -> None:
        '''
        Assuming user is not already logged in, will click on Login -> Enter credentials -> wait for Captach -> submit
        :param username:
        :param password:
        :return:
        '''
        wait = WebDriverWait(driver=self.driver, timeout=60)
        wait.until(expected_conditions.visibility_of_element_located(("xpath", self.login_button)))

        self.driver.find_element("xpath", self.login_button).click()
        wait = WebDriverWait(driver=self.driver, timeout=10)
        wait.until(expected_conditions.visibility_of_element_located(("xpath", self.username_field)))
        self.driver.find_element("xpath", self.username_field).send_keys(username)
        self.driver.find_element("xpath", self.password_field).send_keys(password)
        captcha = input("Enter the Captcha you see on screen : ")
        self.driver.find_element("xpath", self.captcha_field).send_keys(captcha)
        self.driver.find_element("xpath", self.sign_in_button).click()

        wait = WebDriverWait(driver=self.driver, timeout=20)
        wait.until(expected_conditions.visibility_of_element_located(("xpath", self.my_account_link)))

    def enter_from_station(self, station_code) -> None:
        self.driver.find_element("xpath", self.from_field).send_keys(station_code)

        wait = WebDriverWait(driver=self.driver, timeout=5)
        wait.until(expected_conditions.visibility_of_element_located(("xpath", self.auto_complete_div)))

        option_list = self.driver.find_element("xpath", self.auto_complete_div)
        matching_options = option_list.find_elements("xpath",
                                                     f".//li[.//span[contains(normalize-space(),'{station_code}')]]")
        matching_options[0].click()

    def enter_journey_date(self, date) -> None:
        '''
        Date should be in dd/MM/yyyy format only
        :param date:
        :return:
        '''
        self.driver.find_element("xpath", self.journey_date).clear()
        self.driver.find_element("xpath", self.journey_date).send_keys(date)
        time.sleep(2)

    def enter_to_station(self, station_code) -> None:
        self.driver.find_element("xpath", self.to_field).send_keys(station_code)

        wait = WebDriverWait(driver=self.driver, timeout=5)
        wait.until(expected_conditions.visibility_of_element_located(("xpath", self.auto_complete_div)))

        option_list = self.driver.find_element("xpath", self.auto_complete_div)
        matching_options = option_list.find_elements("xpath",
                                                     f".//li[.//span[contains(normalize-space(),'{station_code}')]]")
        matching_options[0].click()

    def select_class(self, journey_class_name):
        '''
        Entering class code would be good like SL, 3A, 3E, 2A
        :param journey_class_name:
        :return:
        '''
        self.driver.find_element("xpath", self.journey_class).click()
        options_list = self.driver.find_element("xpath", self.dropdown_div)
        matching_options = options_list.find_elements("xpath",
                                                     f".//li[.//span[contains(normalize-space(),'{journey_class_name}')]]")
        matching_options[0].click()
        time.sleep(2)

    def select_quota(self, journey_quota):
        '''
        Entering full name would be good like GENERAL, TATKAL
        :param journey_class_name:
        :return:
        '''
        self.driver.find_element("xpath", self.journey_quota).click()
        options_list = self.driver.find_element("xpath", self.dropdown_div)
        matching_options = options_list.find_elements("xpath",
                                                     f".//li[.//span[contains(normalize-space(),'{journey_quota}')]]")
        matching_options[0].click()

    def click_search(self) -> None:
        self.driver.find_element(self.search_button).click()
        result_page = TrainSearchResultPage(self.driver)
        wait = WebDriverWait(driver=self.driver, timeout=60)
        wait.until(expected_conditions.presence_of_element_located("xpath", result_page.result_trains_wrapper))