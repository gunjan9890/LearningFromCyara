import time
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from train_search_page import TrainSearchPage
from train_search_result_page import TrainSearchResultPage

# --------------   D R I V E R    I N I T #


options = ChromiumOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("disable-notifications")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = WebDriver(options)
# --------------    D R I V E R    I N I T #

try:
    train_search = TrainSearchPage(driver)
    train_search.open_irctc_search_page()
    train_search.login_to_irctc("Gunjan_90", "Shiv#gunjan9890")

    # search form
    train_search.enter_from_station("NDLS")
    train_search.enter_to_station("NJP")
    train_search.enter_journey_date("22/11/2024")
    # train_search.select_class("3A")
    train_search.select_quota("TATKAL")
    train_search.click_search()

    # result page
    result_page = TrainSearchResultPage(driver)
    result_page.get_train_wrapper("12506").select_journey_class("SL")
    result_page.get_train_wrapper("12506").select_date_tile()
    result_page.get_train_wrapper("12506").click_book_now()

    time.sleep(10)

except Exception as E:
    print("*"*50)
    print("There occured some error in your code")
    print("*" * 50)
    print("If you are in middle of something, you can do manually and I'll wait else I will close the browser")
    print("*" * 50)
    print("*" * 50)
    print("Enter 'yes' to STOP immediately.")
    print("Enter 'no' so I can go on PAUSE mode & keep the browser running")
    y = input("Enter your choice : ")
    if "no" in y.lower():
        z = input("Okay waiting for your input before giving error : ")
    else:
        raise E

finally:
    driver.close()