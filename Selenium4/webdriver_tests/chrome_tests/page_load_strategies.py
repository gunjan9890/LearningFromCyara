import os
import time

from selenium import webdriver


def normal_page_load_positive():
    """
    Page Load Strategy = "normal".
    Waits for all resources to download.
    This means that images, content will be downloaded and then resumed. However this still does not mean that all
    contents of the page is loaded.

    In short it will basically wait for the "loading" circle on the browser to be completed.
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "normal"
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.bseindia.com/")
    # here there is a graph.
    # By Default selenium will wait for the graph image to load, and then will be resumed
    # This will be evident from the Screenshot taken
    driver.save_screenshot(os.path.join("screenshots", "normal_load_positive.png"))
    driver.quit()


def normal_page_load_negative():
    """
    This is an example where the page is loaded, but there are 2 images, that does not load instantly.
    They load after 2 seconds.
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "normal"

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    t = os.getcwd()
    file_path = os.path.join(t, "html", "lazy_page.html")
    print(file_path)
    driver.get(f"file:///{file_path}")

    # When the page loads, there will be 3 images.
    # 1 image will load right away after the page is loaded, while other 2 images will get loaded after 2 seconds
    # This will be clear from the screenshot.
    # In the screenshot there will be 1 Scooter and 2 similar Cycles (as they are default image).
    # It should be Sports bike and Cruise bike
    driver.save_screenshot(os.path.join("screenshots", "normal_load_negative.png"))
    driver.quit()

    # ======================================================================================
    # In such cases where the page content is loading after domstate = ready

    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "normal"

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    t = os.getcwd()
    file_path = os.path.join(t, "html", "lazy_page.html")
    print(file_path)
    driver.get(f"file:///{file_path}")

    # This time we are waiting strictly for 3 seconds. Just to check the screenshot
    # So in real world applications
    time.sleep(3)
    driver.save_screenshot(os.path.join("screenshots", "normal_load_negative_with_wait.png"))
    driver.quit()


def eager_page_load():
    """
    Page Load Strategy = "eager".
    Just waits for dom access to be ready, but other resources may be still loading
    This means that images, content will NOT be downloaded. So some images may appear blank for example

    Here basically the "circle" might keep on rotating.

    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.bseindia.com/")
    # here there is a graph.
    # By Default selenium will wait only for the page to be ready, but the images might not be ready yet.
    # This will be evident from the Screenshot taken
    driver.save_screenshot(os.path.join("screenshots", "eager_load.png"))
    driver.quit()


def none_page_load():
    """
    Just navigates to the given page and then instantly moves ahead in the script.

    This will be faster, but you will have to manage the waits everytime on your own
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "none"
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.bseindia.com/")
    # it navigates and then instantly executes next step.
    # So the screenshot will appear blank.
    driver.save_screenshot(os.path.join("screenshots", "none_load.png"))
    driver.quit()


# normal_page_load_positive()
normal_page_load_negative()
# eager_page_load()
# none_page_load()
