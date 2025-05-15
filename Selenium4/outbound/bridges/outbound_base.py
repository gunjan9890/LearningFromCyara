from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from outbound.bridges.selenium_testbase import SeleniumTestBase


class OutboundBase:

    def __init__(self, config: dict):
        pass

    def get_email_field(self) -> WebElement:
        return SeleniumTestBase.get_driver().find_element(self.email_address_txt[0], self.email_address_txt[1])

    def get_password_field(self) -> WebElement:
        return SeleniumTestBase.get_driver().find_element(self.password_txt[0], self.password_txt[1])

    def get_signin_button(self) -> WebElement:
        return SeleniumTestBase.get_driver().find_element(self.signin_button[0], self.signin_button[1])

    def close_cookie_popup(self):
        if len(SeleniumTestBase.get_driver().find_elements(self.close_cookie_button[0], self.close_cookie_button[1])) > 0:
            SeleniumTestBase.get_driver().find_element(self.close_cookie_button[0], self.close_cookie_button[1]).click()

    def login_bridge_as_host(self, bridge_url: str = None, username: str = None, password: str = None):
        SeleniumTestBase.get_driver().get(bridge_url)
        # self.close_cookie_popup()

        # enter username / email
        self.get_email_field().send_keys(username)
        # enter password
        self.get_password_field().send_keys(password)
        # click on sign in / login button
        self.get_signin_button().click()

        # self.close_cookie_popup()