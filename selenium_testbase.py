import logging
from os import path

from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, List
from browsermobproxy import Server, Client


class SeleniumTestBase:
    # static variable
    _execute_on_server = False   # True if running on server, False if running on local
    _chromedriver_path = "/usr/bin/chromedriver"  # on ubuntu server
    _driver: WebDriver = None
    _screenshot_counter = 0
    _screenshot_folder = "/home/screenshot/zoom_outbound"  # on ubuntu server
    _screenshot_ref = ""
    _browser_mob_proxy_path = "/home/downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy"
    proxy_client: Client = None
    browser_server = None
    _enable_browser_HAR = False
    _enable_page_source_dump = False

    @staticmethod
    def get_proxy_server():
        # Start BrowserMob Proxy
        SeleniumTestBase.browser_server = Server(SeleniumTestBase._browser_mob_proxy_path)
        SeleniumTestBase.browser_server.start()
        SeleniumTestBase.proxy_client = SeleniumTestBase.browser_server.create_proxy()
        logging.info(f"Created BrowserMob Proxy instance [{SeleniumTestBase.proxy_client.__hash__()}]")
        return SeleniumTestBase.proxy_client

    @staticmethod
    def get_driver():
        if SeleniumTestBase._driver is None:
            _options = options.Options()
            _options.page_load_strategy = "normal"
            if SeleniumTestBase._execute_on_server:
                _options.add_argument("--headless")
                _options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
                _options.add_argument("--allow-insecure-localhost")  # Allow localhost certs
                _options.add_argument("--window-size=1920,1080")
                _options.add_argument("--use-fake-ui-for-media-stream")
                _options.add_argument("--use-fake-device-for-media-stream")

                if SeleniumTestBase._enable_browser_HAR:
                    _options.add_argument(f"--proxy-server={SeleniumTestBase.get_proxy_server().proxy}")
                _options.add_argument("--no-sandbox")
                _options.add_argument("--disable-dev-shm-usage")
                # _options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                #                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
                _options.add_argument("--disable-gpu")
                _options.add_argument("--disable-blink-features=AutomationControlled")
                _options.add_argument("--disable-infobars")
                _options.add_argument("--disable-notifications")
                _options.add_experimental_option("useAutomationExtension", False)
                _options.add_experimental_option("excludeSwitches", ["enable-automation"])
                SeleniumTestBase._driver = WebDriver(executable_path=SeleniumTestBase._chromedriver_path,
                                                     options=_options, keep_alive=True)
            else:
                # _options.add_argument("--headless")
                _options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
                _options.add_argument("--allow-insecure-localhost")  # Allow localhost certs
                _options.add_argument("--window-size=1920,1080")
                _options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
                SeleniumTestBase._screenshot_folder = r"D:\Workspace\PythonProjects\Selenium3Outbound\zoom_outbound_screenshots"
                SeleniumTestBase._driver = WebDriver(options=_options, keep_alive=True)

            SeleniumTestBase._driver.implicitly_wait(30)
            logging.info(f"Created Selenium WebDriver instance [{SeleniumTestBase._driver.__hash__()}]")
        return SeleniumTestBase._driver

    @staticmethod
    def is_present(locator: Tuple[str, str]) -> bool:
        """
        Checks if any matching element is found in the DOM mathcing the Locator
        :param locator: Tuple
        :return: True or False
        """
        SeleniumTestBase.get_driver().implicitly_wait(2)
        logging.info(f"Checking if element [{locator}] is present")
        if len(SeleniumTestBase.get_elements(locator)) > 0:
            SeleniumTestBase.get_driver().implicitly_wait(30)
            return True
        SeleniumTestBase.get_driver().implicitly_wait(30)
        return False

    @staticmethod
    def get_element(locator: Tuple[str, str], parent_element: WebElement = None) -> WebElement:
        """
        Finds the webelement based on the Locator passed. By default on Page
        :param locator: Tuple
        :param parent_element: if passed, the element will be found within this element
        :return: WebElement
        """

        logging.info(f"Finding element with type = [{locator[0]}] value = [{locator[1]}]")
        if parent_element is not None:
            element = parent_element.find_element(locator[0], locator[1])
            SeleniumTestBase.capture_screen()
            return element
        else:
            element = SeleniumTestBase.get_driver().find_element(locator[0], locator[1])
            SeleniumTestBase.capture_screen()
            return element

    @staticmethod
    def get_elements(locator: Tuple[str, str], parent_element: WebElement = None) -> List[WebElement]:
        """
        Finds the webelement based on the Locator passed. By default on Page
        :param locator: Tuple
        :param parent_element: if passed, the element will be found within this element
        :return: WebElement
        """
        logging.info(f"Finding list of elements with type = [{locator[0]}] value = [{locator[1]}]")
        if parent_element is not None:
            return parent_element.find_elements(locator[0], locator[1])
        else:
            return SeleniumTestBase.get_driver().find_elements(locator[0], locator[1])

    @staticmethod
    def js_click(locator: Tuple[str, str], parent_element: WebElement = None):
        element = SeleniumTestBase.get_element(locator, parent_element)
        SeleniumTestBase.get_driver().execute_script("arguments[0].style.border = 'thick solid #A349A4';", element)
        SeleniumTestBase.get_driver().execute_script("arguments[0].style.background = '#99D9EA';", element)
        SeleniumTestBase.capture_screen()
        SeleniumTestBase.get_driver().execute_script("arguments[0].click();", element)

    @staticmethod
    def click(locator: Tuple[str, str], parent_element: WebElement = None):
        element = SeleniumTestBase.get_element(locator, parent_element)
        SeleniumTestBase.get_driver().execute_script("arguments[0].style.border = 'thick solid #FF0000';", element)
        SeleniumTestBase.get_driver().execute_script("arguments[0].style.background = '#FFFF00';", element)
        SeleniumTestBase.capture_screen()
        element.click()

    @staticmethod
    def set_screenshot_reference(ref: str):
        SeleniumTestBase._screenshot_ref = ref
        logging.info(f"Screenshot reference set to: {ref}")

    @staticmethod
    def capture_screen():
        SeleniumTestBase._screenshot_counter += 1
        snap_str = SeleniumTestBase._screenshot_ref + "-" + str(SeleniumTestBase._screenshot_counter).zfill(3) + ".png"
        file_name = path.join(SeleniumTestBase._screenshot_folder, snap_str)
        logging.info(f"Capturing screenshot [{SeleniumTestBase._screenshot_counter}] at: {file_name}")
        SeleniumTestBase.get_driver().get_screenshot_as_file(filename=file_name)

    @staticmethod
    def dump_page_source():
        SeleniumTestBase._driver.switch_to.default_content()
        file_name = path.join(SeleniumTestBase._screenshot_folder, SeleniumTestBase._screenshot_ref + "page_source.txt")
        with open(file_name, "w") as file:
            file.write("*"*100 + "\n")
        total_windows = len(SeleniumTestBase._driver.window_handles)
        total_frames = len(SeleniumTestBase._driver.find_elements(By.TAG_NAME, "iframe"))
        body_tag = SeleniumTestBase._driver.find_element(By.TAG_NAME, "body")
        body_tag_html = SeleniumTestBase._driver.execute_script("return arguments[0].outerHTML;", body_tag)
        with open(file_name, "a") as file:
            file.write("-"*50 + "\n")
            file.write(f"Total Windows: {total_windows}" + "\n")
            file.write("-"*50 + "\n")
            file.write(f"Total Frames: {total_frames}" + "\n")
            file.write("-"*50 + "\n")
            file.write("=" * 50 + "\n")
            file.write(body_tag_html + "\n")
            file.write("=" * 100 + "\n")

        frame_list = SeleniumTestBase._driver.find_elements(By.TAG_NAME, "iframe")
        for i in range(0, len(frame_list)):
            SeleniumTestBase._driver.switch_to.frame(frame_list[0])
            body_tag = SeleniumTestBase._driver.find_element(By.TAG_NAME, "body")
            body_tag_html = SeleniumTestBase._driver.execute_script("return arguments[0].outerHTML;", body_tag)
            with open(file_name, "a") as file:
                file.write("-"*100 + "\n")
                file.write(f"Frame Body HTML:" + "\n")
                file.write(f"{body_tag_html}" + "\n")
            SeleniumTestBase._driver.switch_to.default_content()

    @property
    def execute_on_server(self):
        return self._execute_on_server
