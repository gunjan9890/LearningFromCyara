from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chromium.options import ChromiumOptions

from train_search_page import TrainSearchPage
from train_search_result_page import TrainSearchResultPage

options = ChromiumOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("disable-notifications")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = WebDriver(options)

current_state = 1
while(True):
    try:
        if current_state == 1:
            # # perform login
            # train_search = TrainSearchPage(driver)
            # train_search.open_irctc_search_page()
            # train_search.login_to_irctc("Gunjan_90", "Shiv#gunjan9890")
            print("Logging into IRCTC")
            t = 1/0

        elif current_state == 2:
            # # perform search
            # train_search = TrainSearchPage(driver)
            # train_search.enter_from_station("NDLS")
            # train_search.enter_to_station("NJP")
            # train_search.enter_journey_date("22/11/2024")
            # # train_search.select_class("3A")
            # train_search.select_quota("TATKAL")
            # train_search.click_search()
            print("Searching Train")
            t = 1 / 10

        elif current_state == 3:
            # result page
            # result_page = TrainSearchResultPage(driver)
            # result_page.get_train_wrapper("12506").select_journey_class("SL")
            # result_page.get_train_wrapper("12506").select_date_tile()
            # result_page.get_train_wrapper("12506").click_book_now()
            print("Selecting Train")

        elif current_state == 20:
            print("Completed all tasks")
            break

        current_state += 1

    except Exception as E:
        print("-"*60)
        print("Some error occurred during the execution")
        print("You can select any of the following option to continue")
        print("1. Choose '1' to perform Login Action")
        print("2. Choose '2' to perform Search Train Action")
        print("3. Choose '3' to perform Select Train Action")
        print("20. Choose '20' to stop execution & throw Error")
        print("-" * 60)
        current_state = int(input("enter you choice: "))
        if current_state == 20:
            print(E)

    finally:
        pass
        # print("finally")

print("done with execution")