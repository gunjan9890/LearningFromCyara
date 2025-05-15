import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


# VARIABLES
from selenium.webdriver.support.wait import WebDriverWait

IRCTC_USERNAME = "Gunjan9890"
IRCTC_PASSWORD = "Shiv#gunjan9890"

DESTINATION_FROM = "AHMEDABAD JN - ADI (AHMEDABAD)"
DESTINATION_TO = "NEW DELHI - NDLS (NEW DELHI)"
DATE_OF_JOURNEY = "13/05/2024"

TRAIN_NUMBER = "12915"

# navigation
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.irctc.co.in/nget/train-search")

# locators
login_btn = driver.find_element(By.XPATH, "//a[normalize-space()='LOGIN']")

# action
login_btn.click()

# locators
username_txt = driver.find_element(By.XPATH, "//input[@formcontrolname='userid']")
password_txt = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
captcha_txt = driver.find_element(By.XPATH, "//input[@formcontrolname='captcha']")
sign_in_btn = driver.find_element(By.XPATH, "//button[normalize-space()='SIGN IN']")

# action
username_txt.send_keys(IRCTC_USERNAME)
password_txt.send_keys(IRCTC_PASSWORD)
# captcha_txt.send_keys()
sign_in_btn.click()

# locators
destination_from = driver.find_element(By.XPATH, "//label[normalize-space()='From']/preceding-sibling::p-autocomplete//input")
destination_to = driver.find_element(By.XPATH, "//label[normalize-space()='To']/preceding-sibling::p-autocomplete//input")
journey_date = driver.find_element(By.XPATH, "//label[normalize-space()='DD/MM/YYYY *']/preceding-sibling::p-calendar//input")
quota_dropdown = driver.find_element(By.XPATH, "//p-dropdown[@id='journeyQuota']")
tatkal_option = driver.find_element(By.XPATH, "//p-dropdownitem[.//span[normalize-space()='TATKAL']]")
search_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Search']")

# action
wait = WebDriverWait(driver, 60)
wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//label[normalize-space()='From']/preceding-sibling::p-autocomplete//input")))
destination_from.send_keys(DESTINATION_FROM)
destination_to.send_keys(DESTINATION_TO)
journey_date.send_keys(DATE_OF_JOURNEY)
quota_dropdown.click()
time.sleep(0.25)
tatkal_option.click()
search_btn.click()

# locators
train_card_xpath = f"//div[contains(@class,'form-group no-pad col') and .//div[contains(@class,'train-heading') and contains(normalize-space(), '{TRAIN_NUMBER}')]]"
train_card = driver.find_element(By.XPATH, train_card_xpath)
wait = WebDriverWait(driver, 60)
wait.until(expected_conditions.visibility_of_element_located((By.XPATH, train_card_xpath)))
