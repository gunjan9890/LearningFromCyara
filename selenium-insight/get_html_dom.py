from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://healenium.io/#rec410415567")

body = driver.find_element(by=By.XPATH, value="//body")
html = driver.execute_script("return arguments[0].outerHTML;", body)
print(html)

inputs = driver.find_elements(by=By.XPATH, value="//input[not(@type='submit') and not(@type='button') and not(@type='hidden')]")
buttons = driver.find_elements(by=By.XPATH, value="//*[(local-name()='input' and (@type='submit' or @type='button')) or (local-name()='button')]")

for input_field in inputs:
    list_of_attribs = None
    list_of_attribs = driver.execute_script("return arguments[0].outerHTML;", input_field)

    print(list_of_attribs)

for button_field in buttons:
    list_of_attribs = driver.execute_script("return arguments[0].outerHTML;", button_field)
    print(list_of_attribs)

driver.quit()