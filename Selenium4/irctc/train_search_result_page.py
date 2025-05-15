from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class TrainWrapper:
    def __init__(self, driver: WebDriver, wrapper_element: WebElement):
        self.driver = driver
        self.wrapper = wrapper_element
        self.train_heading: WebElement = self.wrapper.find_element("xpath", ".//div[contains(@class,'train-heading')]")

    def select_journey_class(self, class_code):
        self.wrapper.find_element("xpath", f".//table//td[.//div[contains(normalize-space(),'{class_code}')]]").click()

    def select_date_tile(self):
        dates_list = self.wrapper.find_elements("xpath", f"//table//td")
        dates_list[1].click()

    def click_book_now(self):
        self.wrapper.find_element("xpath", ".//button[normalize-space()='Book Now']").click()


class TrainSearchResultPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.result_trains_wrapper: str = "//app-train-avl-enq"

    def get_train_wrapper(self, train_no) -> TrainWrapper:
        train_list = self.driver.find_elements("xpath", self.result_trains_wrapper)
        for t in train_list:
            train = TrainWrapper(self.driver, t)
            if train_no in train.train_heading.text:
                return train
        return TrainWrapper(self.driver, train_list[0])
