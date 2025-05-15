import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=opts)

counter = 2085

for i in range(1, 100):

    driver.get("https://services.gandhinagarmunicipal.com/DuesSearch.aspx")
    tnmnt_no = driver.find_element(By.XPATH, "//input[contains(@id,'TENEMENT_NO')]")
    search_btn = driver.find_element(By.XPATH, "//a[contains(@id,'Search')]")
    tnmnt_no.send_keys(f"1008C20{counter}")
    search_btn.click()
    time.sleep(1)

    # msg
    msg = driver.find_element(By.XPATH, "//div[@id='MSG']//button")
    if msg.is_displayed() > 0:
        print(f"No [1008C20{counter}]. Owner [------]. Address [------]")
        msg.click()
        counter = counter + 1
        continue

    wait = WebDriverWait(driver, 15)
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//table/tbody/tr[4]/td[2]")))

    property_address = driver.find_element(By.XPATH, "//table/tbody/tr[4]/td[2]")
    owner = driver.find_element(By.XPATH, "//table/tbody/tr[5]/td[2]")

    # if "MARUTI AMARKUNJ-2" in property_address.text.upper():
    print(f"No [1008C20{counter}]. Owner [{property_address.text}]. Address [{property_address.text}]")

    # print("-"*50)
    counter = counter + 1

driver.quit()
