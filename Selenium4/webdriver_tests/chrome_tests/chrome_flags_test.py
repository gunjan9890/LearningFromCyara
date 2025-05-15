import time

import selenium.webdriver as webdriver

# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")

# # options.add_argument("--deny-permission-prompts")
# # options.add_argument("--disable-popup-blocking")
#
#
# # options.add_argument("window-position=500,500")
# # options.add_argument("headless=new")
# # options.add_argument("enable-automation")
# driver = webdriver.Chrome(options=options)
# # driver.get("https://www.bbc.com/arabic")    # different language
# # driver.get("https://www.lodhagroup.in/hr/why-lodha")    # permission for notification
#
# # driver.get("https://www.rapidtables.com/tools/camera.html")   # test webcam
# driver.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_video_autoplay")     # auto play video
# # driver.get("https://www.msn.com/en-in/news/world/500-year-domination-of-the-world-is-ending-putin-s-fm-warns-the-west/ar-AA1lk4vH")   # auto play video
# time.sleep(10)
#
# driver.quit()


def auto_play_videos():
    """
    Chrome Options to Control Playing of Videos on a Page Automatically
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--enable-automation")
    # "no-user-gesture-required" means that the video will play automatically
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_video_autoplay")  # auto play video

    time.sleep(10)

    driver.quit()

    # ------------------------------------------------------------------------------------------------

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--enable-automation")
    # "user-gesture-required" means that the video will NOT play automatically
    options.add_argument("--autoplay-policy=user-gesture-required")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_video_autoplay")  # auto play video

    time.sleep(10)

    driver.quit()


def load_user_profile():
    """
    Loads a specific user profile
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--enable-automation")
    # options.add_argument("--no-first-run")
    options.add_argument(r"--user-data-dir=C:\Users\Spearline\AppData\Local\Google\Chrome\User Data")
    options.add_argument(r"--profile-directory=Profile 2")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")  # auto play video

    time.sleep(5)

    driver.quit()


def webcam():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--use-fake-ui-for-media-stream")
    driver = webdriver.Chrome()
    driver.get("https://www.rapidtables.com/tools/camera.html")
    time.sleep(30)
    driver.quit()
# auto_play_videos()
# load_user_profile()

webcam()