"""
If you set the accept insecure certificates flag to True, then there will be no warning page
"""
import os
import time

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.accept_insecure_certs = True

driver = webdriver.Chrome(chrome_options)
driver.get('https://self-signed.badssl.com/')
# to get list of other such websites visit "https://badssl.com/"

driver.save_screenshot(os.path.join("screenshots", "invalid_certificate_page_opened.png"))
time.sleep(2)

driver.close()

# By default that flag is False.
# When its false, there is a warning message

chrome_options = webdriver.ChromeOptions()
# chrome_options.accept_insecure_certs = False

driver = webdriver.Chrome(chrome_options)
driver.get('https://self-signed.badssl.com/')

driver.save_screenshot(os.path.join("screenshots", "invalid_certificate_warning.png"))
time.sleep(2)

driver.close()
