"""
Checks default Prompt behaviour for UnHandled Prompts.
Default value is "accept and notify". Notify basically means that throw an excpetion
"""
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def unhandled_confirmation_dismiss():
    """
    Here there will be no Alert Class involved.
    In real life this can be expected as "Unexpected Alerts", where the alerts might occur anytime, but not always
    :return:
    """

    chrome_options = webdriver.ChromeOptions()
    # You will see the Alert being handled, only when some action is being made after the Alert was generated.
    # Here we have set behaviour to dismiss, it means if there is a OK / Cancel dialog. It will click on Cancel.
    # If there is just OK dialog, it will click OK
    chrome_options.unhandled_prompt_behavior = "dismiss"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    # Check OK-Cancel Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    time.sleep(1)

    # clicking the above button produces an Alert.
    # But that does not mean, selenium knows about it yet.
    # Selenium will know there is an alert only if some operation is performed in the browser window
    # So i'll click on the Result label (which wont do anything)

    driver.find_element(By.XPATH, "//p[@id='result']").click()
    # now since there is an Alert Already opened, because of the Previous Click
    # And again, user wants to click on the 'Result' label, without handling the alert
    # our "chrome_options.unhandled_prompt_behavior" comes into picture.
    # Now selenium, checks if there are any setting provided by user to handle Alert
    # Here since we have given the value "dismiss"
    # It will click on "Cancel" button on the Alert.
    # This will be evident from the Screenshot
    # In the screenshot it should say "You clicked : Cancel" (since we set default as Dismiss)

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_ok_cancel_alert_dismissed.png"))

    driver.close()


def unhandled_alert_dismiss():
    # Now once you set the unhandled alert behaviour, you cannot change it unless you create a new Chrome Driver
    # So lets test how dismiss works when there is just OK alert

    chrome_options = webdriver.ChromeOptions()
    chrome_options.unhandled_prompt_behavior = "dismiss"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # Check OK Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    time.sleep(1)
    # Result Label
    driver.find_element(By.XPATH, "//p[@id='result']").click()

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_ok_alert_dismissed.png"))
    # Screenshot should have, "You successfully clicked an alert"

    driver.close()


def unhandled_prompt_dismiss():
    """
    An Alert prompt where you have to enter something into the Alert Box
    :return:
    """
    # So lets test how dismiss works when there is just a Prompt alert

    chrome_options = webdriver.ChromeOptions()
    chrome_options.unhandled_prompt_behavior = "dismiss"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # Check OK Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    time.sleep(1)
    # Result Label
    driver.find_element(By.XPATH, "//p[@id='result']").click()

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_prompt_dismissed.png"))
    # Screenshot should have, "You entered : null". Since we had not entered anything in the text, it will be null

    driver.close()


def unhandled_confirmation_accept():
    """
    Here there will be no Alert Class involved.
    In real life this can be expected as "Unexpected Alerts", where the alerts might occur anytime, but not always
    :return:
    """

    chrome_options = webdriver.ChromeOptions()
    # You will see the Alert being handled, only when some action is being made after the Alert was generated.
    # Here we have set behaviour to dismiss, it means if there is a OK / Cancel dialog. It will click on Cancel.
    # If there is just OK dialog, it will click OK
    chrome_options.unhandled_prompt_behavior = "accept"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    # Check OK-Cancel Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    time.sleep(1)

    # clicking the above button produces an Alert.
    # But that does not mean, selenium knows about it yet.
    # Selenium will know there is an alert only if some operation is performed in the browser window
    # So i'll click on the Result label (which wont do anything)

    driver.find_element(By.XPATH, "//p[@id='result']").click()
    # now since there is an Alert Already opened, because of the Previous Click
    # And again, user wants to click on the 'Result' label, without handling the alert
    # our "chrome_options.unhandled_prompt_behavior" comes into picture.
    # Now selenium, checks if there are any setting provided by user to handle Alert
    # Here since we have given the value "accept"
    # It will click on "OK" button on the Alert.
    # This will be evident from the Screenshot
    # In the screenshot it should say "You clicked : Ok" (since we set default as Dismiss)

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_ok_cancel_alert_accepted.png"))

    driver.close()


def unhandled_alert_accept():
    # Now once you set the unhandled alert behaviour, you cannot change it unless you create a new Chrome Driver
    # So lets test how dismiss works when there is just OK alert

    chrome_options = webdriver.ChromeOptions()
    chrome_options.unhandled_prompt_behavior = "accept"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # Check OK Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    time.sleep(1)
    # Result Label
    driver.find_element(By.XPATH, "//p[@id='result']").click()

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_ok_alert_accepted.png"))
    # Screenshot should have, "You successfully clicked an alert"

    driver.close()


def unhandled_prompt_accept():
    """
    An Alert prompt where you have to enter something into the Alert Box
    :return:
    """
    # So lets test how dismiss works when there is just a Prompt alert

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.unhandled_prompt_behavior = "accept"

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # Check OK Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    time.sleep(1)
    # Result Label
    driver.find_element(By.XPATH, "//p[@id='result']").click()

    time.sleep(1)
    driver.save_screenshot(os.path.join("screenshots", "unhandled_prompt_accepted.png"))
    # Screenshot should have, "You entered : ". Since we had not entered anything in the text,
    # it will be empty ("") as it was accepted & not null (when we had dismissed)

    driver.close()

# alert = driver.switch_to.alert
# print(alert.text)
# alert.accept()
# time.sleep(2)
#
# driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
# time.sleep(2)
#
# alert = driver.switch_to.alert
# print(alert.text)
# alert.dismiss()
# time.sleep(2)


# unhandled_confirmation_accept()
unhandled_alert_accept()
# unhandled_prompt_accept()

