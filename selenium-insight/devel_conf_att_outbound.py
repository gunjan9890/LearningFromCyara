
#!/usr/bin/env python
# ===================================================================================
# ===================================================================================
#
#       Name:                   devel_conf_att_outbound.py
#       Purpose:                New Call Generation Script For Outbound Conference Call AT&T
#
#       Author:                 Dhaval Indrodiya
#
#       Created:                2020-06-26
#       Modified:               2020-06-26
#
#       Copyright:              (c) Spearline Ltd. 2020
#       Licence:                Copyright of Spearline Ltd.
#
# ===================================================================================
# ===================================================================================

# Selenium WebDriver Imports
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

# Spearline Send AWS Alert

SECRET_KEY = "8e74Ebn8572Rtjdyr8aVX3816bBt204"
MIN_POLL_FREQ = 10
CONNECTED_POLL_FREQ = 2
REFRESH_INTERVAL = 15
loginAction = "Action: Login\r\nUsername: admin\r\nSecret: mvemj6u9p\r\nEvents: off\r\n\r\n"
logoutAction = "Action: Logoff\r\n\r\n"
lastServer = None
lastConnection = True
CONF_RECORD = {}

frame_one = "thinIframe"
frame_by_xpath = "//iframe[@name='thinIframe']"

# start_meet_by_xpath = "//span[contains(text(),'Start a meeting')]"
start_meet_by_xpath = "//span[contains(text(),'Start')]"
frame = "mainFrame"
# signin_by_xpath = "//span[contains(text(),'Sign In')]"

# First Page Sign In Button
signin_button_bridge_page = '//*[@id="guest_signin_button"]/span'

# Second Page (Login Page)
email_by_xpath = "//input[@id='IDToken1']"
password_by_xpath = "//input[@id='IDToken2']"
signin_button_login_page = "//button[@id='Button1' or @id='IDButton2']"

close_button_by_xpath = "//button[@aria-label='Leave or end meeting']"
end_meeting_button_by_xpath = "//button[contains(text(),'End meeting')]"
end_meet_by_xpath = "//button[@title='End meeting']"
name_drop_by_xpath = "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]"
signout_button = "#dashboard_nav_logout_item"
host_button = "//button[@title='OK']"
# close_dialog_by_xpath = "//body/div[@id='mainview']/div[@id='layoutdomid']/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"
# close_dialog_by_xpath = "//button[@aria-label='Close']"
close_dialog_by_xpath = "//button[@data-doi='AUDIO:CLOSE_DIALOG:DIALOG_AUDIO_CONNECTING']"
audio_dialog_by_xpath = "//div[contains(@class, 'style-audio-select-text')]"
call_me_by_xpath = "//div[./span[contains(text(),'Call me')]]"
dial_out_by_xpath = "//button[@id='interstitial_start_btn']"
# not_connected_by_class = "style-content-3kl7a"
not_connected_by_class = "style-errormsg-1kv8b"

browser: webdriver.Chrome = None
bridgeUrl = "https://bofa-healthcheck.webex.com/"
bridgeUsername = "ga2735+QA03@plusalias.it.att.com" #"BofAQA-03"
bridgePassword = "QABoA-03"
countryName = "India"
countryPrefix = "+91"
ddiNumber = "9867441411"


def close_cookie_popup(browser):
    close_btn = browser.find_elements_by_xpath("//div[@role='alertdialog' and @class='cookie-manage-banner']//button[contains(@class,'close')]")
    if len(close_btn) > 0:
        close_btn[0].click()


def isolate_country(browser, countryName, countryCode):
    """Read everything visible on the page and try to isolate the element that has the country name on it, then click it.
    """
    print("Attempting to isolate {0}".format(countryName))
    browser.find_element_by_xpath("//input[@id='conn-callMe-input']").click()
    time.sleep(1)
    element = browser.find_element_by_xpath("//input[contains(@class, 'number-input')]")
    time.sleep(1)
    actions = ActionChains(browser)
    actions.click(element).send_keys(Keys.BACKSPACE + countryCode).perform()
    all_elements = browser.find_elements_by_xpath("//body//li")
    found_elements = []
    for el in all_elements:
        try:
            if countryName in el.get_attribute("aria-label"):
                print("Found {0}".format(countryName))
                found_elements.append(el)
        except(TypeError):
            pass


def enter_number(browser, number, element_xpath="//input[@placeholder='Phone number']"):
    browser.find_element_by_xpath(element_xpath).send_keys(number)
    entered_value = browser.find_element_by_xpath(
        element_xpath).get_attribute("value")
    new = entered_value.replace("-", "")
    print(new)
    if new != number:
        browser.find_element_by_xpath(
            element_xpath).send_keys(Keys.CONTROL + "a")
        browser.find_element_by_xpath(element_xpath).send_keys(Keys.DELETE)
        enter_number(browser, number, element_xpath)
    else:
        browser.find_element_by_xpath(element_xpath).send_keys(Keys.ENTER)


def ddi_init():
    print("[{0}] Starting Chrome and ChromeDriver")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
    })
    # browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
    #                            chrome_options=chrome_options)
    global browser
    browser = webdriver.Chrome(chrome_options=chrome_options)

    time.sleep(0.5)

    wait = WebDriverWait(browser, 10)
    browser.maximize_window()
    print("[{0}] - Browser Initialized")


def ddi_login():
    # Bridge Page
    browser.get(bridgeUrl)
    browser.maximize_window()
    print("[{0}] URL Opened Successfully".format(bridgeUrl))

    time.sleep(10)
    close_cookie_popup(browser)

    # Login Page
    browser.find_element_by_xpath(email_by_xpath).send_keys("{0}".format(bridgeUsername))
    browser.find_element_by_xpath(signin_button_login_page).click()
    browser.find_element_by_xpath(password_by_xpath).send_keys("{0}".format(bridgePassword))
    browser.find_element_by_xpath(signin_button_login_page).click()
    print("[{0}] - login Successfully - {1} - {2}")


def ddi_start_meeting():
    browser.find_element_by_xpath(start_meet_by_xpath).click()

    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, frame_by_xpath)))
    close_cookie_popup(browser)
    browser.switch_to.frame(frame_one)
    time.sleep(5)
    elements = browser.find_elements_by_xpath("//*[@id]")
    for el in elements:
        if el.get_attribute("id") == "welcome_skip":
            el.click()
    try:
        browser.find_element_by_xpath(audio_dialog_by_xpath).click()
    except:
        pass
    browser.find_element_by_xpath("//button[@id='voip']").click()
    time.sleep(1)
    browser.find_element_by_xpath(call_me_by_xpath).click()


def ddi_start_call():
    # isolate_country(browser, self.countryName,self.countryPrefix,self.callID)
    isolate_country(browser, countryName, countryPrefix)
    print("[{0}] - Entering phone number")
    enter_number(browser, ddiNumber)
    print("[{0}] - Entered phone number")
    browser.find_element_by_xpath(dial_out_by_xpath).click()
    time.sleep(5)
    try:
        browser.find_element_by_xpath(host_button).click()
        # ok_buttons=browser.find_elements_by_xpath("//button[@title='OK']")
        # ok_buttons[1].click()
        print("Dismissed new host message dialog")
    except:
        print("New host message dialog did not have to be dismissed")


ddi_init()
ddi_login()
ddi_start_meeting()
ddi_start_call()