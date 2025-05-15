# Selenium WebDriver Imports
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

frame_one = "thinIframe"
frame_by_xpath = "//iframe[@name='thinIframe']"
pass_by_xpath = "//input[@id='mwx-ipt-password']"
user_by_xpath = "//input[@id='mwx-ipt-username']"
start_meet_by_xpath = "//span[contains(text(),'Start')]"
start_meeting_frame_btn_xpath = "//button[text()='Start meeting']"
join_meet_by_web = "//li[contains(text(),'Use web app')]"
frame = "mainFrame"
# signin_by_xpath = "//span[contains(text(),'Sign In')]"
close_button_by_xpath = "//button[@aria-label='Leave or end meeting']"
end_meeting_button_by_xpath = "//button[contains(text(),'End meeting')]"
end_meet_by_xpath = "//div[@role='dialog']//button[contains(text(),'End meeting')]"
name_drop_by_xpath = "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]"
signout_button = "#dashboard_nav_logout_item"
host_button = "//button[@title='OK']"
close_dialog_by_xpath = "//button[@data-doi='AUDIO:CLOSE_DIALOG:DIALOG_AUDIO_CONNECTING']"
audio_dialog_by_xpath = "//button[@id='voip']"
call_me_by_xpath = "//span[contains(text(), 'Call me')]"
dial_out_by_xpath = "//button[@id='interstitial_start_btn']"
not_connected_by_class = "style-errormsg-1kv8b"


def isolate_country(browser, countryName, countryCode):
    """Read everything visible on the page and try to isolate the element that has the country name on it, then click it.
    """
    print("Attempting to isolate {0}".format(countryName))

    browser.find_element_by_xpath("//input[@id='conn-callMe-input']").click()  # newid
    time.sleep(1)
    element = browser.find_element_by_xpath(
        "//input[contains(@class, 'number-input')]")  # /div[2]/input")
    time.sleep(1)
    actions = ActionChains(browser)
    actions.click(element).send_keys(Keys.BACKSPACE + countryCode).perform()
    all_elements = browser.find_elements_by_xpath("//body//li")
    found_elements = []
    for el in all_elements:
        try:
            if countryName in el.get_attribute("aria-label"):
                found_elements.append(el)
        except(TypeError):
            pass


def handle_cookie_popup(browser):
    cookie_btn = browser.find_elements_by_xpath(
        "//div[@class='cookie-banner-container']//button[.//span[text()='Accept']]")
    if len(cookie_btn) != 0:
        print("Cookie Popup Found. Closed the popup by Accepting Cookie...")
        cookie_btn[0].click()


def click_element_by_xpath(browser, element_xpath):
    """Click on an element, keep trying until it succeeds.
    """
    try:
        browser.find_element_by_xpath(element_xpath).click()
    except:
        click_element(browser, By.XPATH, element_xpath)


def click_element(browser, type, element):
    """Click on an element.
    """
    wait = WebDriverWait(browser, 30)
    el = wait.until(EC.element_to_be_clickable((type, element)))
    el.click()


def enter_number(browser, number, element_xpath="//input[@placeholder='Phone number']"):
    browser.find_element_by_xpath(element_xpath).send_keys(number)
    entered_value = browser.find_element_by_xpath(
        element_xpath).get_attribute("value")
    new = entered_value.replace("-", "")
    if new != number:
        browser.find_element_by_xpath(
            element_xpath).send_keys(Keys.CONTROL + "a")
        browser.find_element_by_xpath(element_xpath).send_keys(Keys.DELETE)
        enter_number(browser, number, element_xpath)
    else:
        browser.find_element_by_xpath(element_xpath).send_keys(Keys.ENTER)


def signout(browser):
    "Logout of account"
    click_element(browser, By.XPATH, name_drop_by_xpath)
    time.sleep(2)
    click_element(browser, By.CSS_SELECTOR, signout_button)
    time.sleep(5)
    print("Logged out...........")


# browser.quit()

# def end_meeting(browser):
#    """end meeting and Sign out from conf to prevent account being locked for 24 hrs.
#    """
#    end_meeting_button_by_xpath = "//button[contains(text(),'End meeting')]"
#    end_meet_by_xpath = "//button[@title='End meeting']"
#    click_element_by_xpath(browser, close_button_by_xpath)
#    click_element_by_xpath(browser, end_meeting_button_by_xpath)
#    time.sleep(5)
#    click_element_by_xpath(browser, end_meet_by_xpath)
#    print("Meeting ended")
#    time.sleep(10)
def end_meeting(browser):
    """end meeting and Sign out from conf to prevent account being locked for 24 hrs.
    """
    # end_meet_by_xpath = "//button[@title='End meeting']"
    # Click on X button to Stop Meeting
    close_meeting_x_button = browser.find_element(By.XPATH, close_button_by_xpath)
    browser.execute_script("arguments[0].click();", close_meeting_x_button)
    time.sleep(2)
    # Click on End Meeting button
    end_for_all_btn = browser.find_element(By.XPATH, end_meeting_button_by_xpath)
    browser.execute_script("arguments[0].click();", end_for_all_btn)
    time.sleep(2)
    # Click on End Meeting Button on End Meeting for all Confirm Popup
    end_for_all = browser.find_element(By.XPATH, end_meet_by_xpath)
    browser.execute_script("arguments[0].click();", end_for_all)
    time.sleep(2)
    print("Meeting ended")
    time.sleep(10)


def browser_init():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"')
    # browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    browser.maximize_window()
    return browser


def browser_login(browser, url, username, password, callid):
    browser.get(url)
    browser.maximize_window()
    print(f'URL : {url} opened for [{callid}].')
    element = browser.find_element(By.XPATH, "//div[@id='frame_outter']")
    el = browser.find_element(By.XPATH, "//span[contains(text(),'Sign in')]")
    el.click()
    handle_cookie_popup(browser)
    wait = WebDriverWait(browser, 30)

    # Login Page
    email_by_xpath = "//input[@id='IDToken1']"
    password_by_xpath = "//input[@id='IDToken2']"
    signin_button_login_page = "//button[@id='Button1' or @id='IDButton2']"
    browser.find_element_by_xpath(email_by_xpath).send_keys("{0}".format(username))
    browser.find_element_by_xpath(signin_button_login_page).click()
    browser.find_element_by_xpath(password_by_xpath).send_keys("{0}".format(password))
    browser.find_element_by_xpath(signin_button_login_page).click()

    print(f'Login successful for [{callid}]: username : {username} pass: {password}')
    return browser


def start_meeting(browser, callid):
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, start_meet_by_xpath)))
    handle_cookie_popup(browser)
    browser.save_screenshot("/home/screenshot/webex_test_gvs_2.png")
    start_btn = browser.find_element_by_xpath(start_meet_by_xpath)
    # meet_by_web = browser.find_element_by_xpath(join_meet_by_web)
    # browser.execute_script("arguments[0].click();", meet_by_web)
    # browser.save_screenshot("/home/screenshot/webex_test_gvs_3.png")
    time.sleep(2)
    browser.execute_script("arguments[0].click();", start_btn)
    print(f"Meeting Started for callid : {callid}")
    browser.save_screenshot("/home/screenshot/webex_test_gvs_4.png")
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, frame_by_xpath)))
    browser.switch_to.frame(frame_one)
    time.sleep(5)
    browser.save_screenshot("/home/screenshot/webex_test_gvs_5.png")

    elements = browser.find_elements_by_xpath("//*[@id]")
    for el in elements:
        if el.get_attribute("id") == "welcome_skip":
            el.click()
    try:
        browser.find_element_by_xpath(audio_dialog_by_xpath).click()
    except:
        pass

    wait.until(EC.presence_of_element_located((By.XPATH, call_me_by_xpath)))
    browser.find_element_by_xpath(call_me_by_xpath).click()
    # browser.find_element_by_xpath(start_meeting_frame_btn_xpath).click()

    browser.save_screenshot("/home/screenshot/webex_test_gvs_6.png")


def start_call(browser, country, country_code, phone_num, callid):
    search_elements = isolate_country(browser, country, country_code)
    handle_cookie_popup(browser)
    print(f"[{callid}]- Entering phone number : {phone_num}")
    enter_number(browser, phone_num)
    browser.find_element_by_xpath(dial_out_by_xpath).click()
    print(f"[{callid}]- Call started.")
    time.sleep(50)
    try:
        browser.find_element_by_class_name(not_connected_by_class)
        logging.error(f"[{callid}] Could not connect to {country_code}{phone_num}.")
        browser.find_element_by_xpath(close_dialog_by_xpath).click()
        return False
    except Exception:
        return True


def close_meeting(browser):
    end_meeting(browser)
    time.sleep(10)
    browser.switch_to.window(browser.window_handles[0])
    signout(browser)
    browser.quit()


b = browser_init()
browser_login(b,"https://bofa-healthcheck.webex.com/", "ga2735+QA21@plusalias.it.att.com", "QABoA-21", "")