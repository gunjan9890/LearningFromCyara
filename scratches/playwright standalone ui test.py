import time

from playwright.sync_api import sync_playwright

def run():
    play = sync_playwright().start()
    browser = play.chromium.launch(
        headless=False, slow_mo=100)

    iphone = play.devices['iPhone 13 Pro landscape']
    context = browser.new_context(record_video_dir=r"C:\Users\Spearline\Desktop\Layered Reports\videos", record_video_size={"width":1200, "height":800})

    page = context.new_page()
    page.goto("https://www.google.com")
    print(page.url)
    # other actions...
    time.sleep(2)

    page.goto("https://cron.spearline.com/login?from=%2Fjob%2Fqa_automated_tests-scripts%2Fjob%2Fautomatedtests%2F")
    time.sleep(2)

    page.goto("https://zoom.us/")
    time.sleep(2)
    page.locator("xpath=//div[@d='gunjan']").click()

    page.goto("https://www.ringcentral.com/")
    time.sleep(2)


    browser.close()


run()