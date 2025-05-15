from selenium.webdriver.chrome import webdriver, options
from dataclasses import dataclass
from dataclasses_json import dataclass_json
# from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


# @dataclass_json
# @dataclass
# class DriverConfig:
#     browser: str
#     timeout_in_seconds: int
#     arguments: list


# class CyaraSeleniumListener():
#
#     def before_click(self, element, driver: WebDriver) -> None:
#         pass
#         # if len(driver.find_elements("xpath", "//div[contains(@id,'onetrust-banner')]//button[contains(@class,'onetrust-close-btn')]")) > 0:
#         #     driver.find_element("xpath", "//div[contains(@id,'onetrust-banner')]//button[contains(@class,'onetrust-close-btn')]").click()
#
#     def after_click(self, element, driver) -> None:
#         pass
#
#     def before_navigate_to(self, url: str, driver) -> None:
#         print(f"navigating to url = [{url}]")
#
#     def after_navigate_to(self, url: str, driver) -> None:
#         print(f"opened url = [{url}] successfully.")
#
#     def before_find(self, by, value, driver) -> None:
#         print(f"trying to find element by [{by}] = [{value}]")
#
#     def after_find(self, by, value, driver) -> None:
#         count = driver.find_elements(by=by, value=value)
#         print(f"total matching elements found are [{len(count)}]")
#
#     def before_change_value_of(self, element: WebElement, driver) -> None:
#
#         print(f"entering value for element [{element.accessible_name}]")
#
#     def after_change_value_of(self, element: WebElement, driver) -> None:
#         print(f"entered value = [{element.get_property('value')}] for element [{element.accessible_name}]")


class SeleniumTestBase:

    # static variables
    _driver: WebDriver = None

    @staticmethod
    def get_driver(config: dict = None):
        if SeleniumTestBase._driver is None:
            _options = options.Options()
            _options.page_load_strategy = "normal"
            # _options.add_argument("--headless")
            _options.add_argument("--incognito")
            _options.add_argument("--disable-infobars")
            _options.add_argument("--disable-blink-features=AutomationControlled")
            _options.add_argument("--disable-features=VizDisplayCompositor")
            _options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
            # _options.add_argument("--disable-dev-shm-usage")
            # _options.add_argument("--no-sandbox")
            # _options.add_argument("--use-fake-ui-for-media-stream")
            # _options.add_argument("--use-fake-device-for-media-stream")
            SeleniumTestBase._driver = WebDriver(options=_options)
            # SeleniumTestBase._driver = EventFiringWebDriver(driver, CyaraSeleniumListener())
            SeleniumTestBase._driver.implicitly_wait(30)
            SeleniumTestBase._driver.set_window_size(width=1920, height=1080)
        return SeleniumTestBase._driver

    @staticmethod
    def is_present(locator: tuple[str, str]) -> bool:
        """
        Checks if any matching element is found in the DOM mathcing the Locator
        :param locator: Tuple
        :return: True or False
        """
        SeleniumTestBase.get_driver().wrapped_driver.implicitly_wait(2)
        if len(SeleniumTestBase.get_driver().find_elements(locator[0], locator[1])) > 0:
            SeleniumTestBase.get_driver().wrapped_driver.implicitly_wait(30)
            return True
        SeleniumTestBase.get_driver().wrapped_driver.implicitly_wait(30)
        return False

    @staticmethod
    def get_element(locator: tuple[str, str], parent_element: WebElement = None) -> WebElement:
        """
        Finds the webelement based on the Locator passed. By default on Page
        :param locator: Tuple
        :param parent_element: if passed, the element will be found within this element
        :return: WebElement
        """
        if parent_element is not None:
            return parent_element.find_element(locator[0], locator[1])
        else:
            return SeleniumTestBase.get_driver().find_element(locator[0], locator[1])

    @staticmethod
    def get_elements(locator: tuple[str, str], parent_element: WebElement = None) -> list[WebElement]:
        """
        Finds the webelement based on the Locator passed. By default on Page
        :param locator: Tuple
        :param parent_element: if passed, the element will be found within this element
        :return: WebElement
        """
        if parent_element is not None:
            return parent_element.find_elements(locator[0], locator[1])
        else:
            return SeleniumTestBase.get_driver().find_elements(locator[0], locator[1])
