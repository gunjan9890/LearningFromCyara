import time

from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
print(chrome_options.browser_version)
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://in.mashable.com/")

# wait for 2 seconds
# time.sleep(2)

# close the driver
driver.close()
