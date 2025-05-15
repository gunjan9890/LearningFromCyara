# pip install selenium4
# pip install webdriver-manager
import time

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

opts = webdriver.ChromeOptions()
opts.add_argument("start-maximized")
driver = webdriver.Chrome(options=opts, service=ChromeService(ChromeDriverManager().install()))

# "祝你生日快乐"

# driver.get("https://translate.google.com/?sl=auto&tl=af&text=%E7%A5%9D%E4%BD%A0%E7%94%9F%E6%97%A5%E5%BF%AB%E4%B9%90&op=translate")

line_counter = 1
conversations = [
    ["Hey ", "...!!", " Lets chat ", "for a ", "while" + Keys.ENTER, "Here are the rules" + Keys.ENTER, "When I ask you question, it would end with a '?'", " ", " ", " " + Keys.ENTER, "And you just have to type your answer.", " ", " ", " " + Keys.ENTER, "No Enters pls or no colons (:) .. Haha..Just answer within ~5 seconds after", " ", " ", " "  + Keys.ENTER, "Sounds good ?. Let's try. Just Type 'Yes'" ],
    ["Awesome", " ", " ", " ", " ", "..Quick learner.." + Keys.ENTER + ": : : : : : : : : : : : : : : :: : : : : : : : : : : : : : " + Keys.ENTER, "Shall we start ?"],
    ["Great", " I hope", " you and the baby", " are doing great & enjoying each other's company well. All good ?" + Keys.ENTER],
    ["On this special day", " Let me take some of your time to Wish you happy birthday. Are you ready ?" + Keys.ENTER],
    ["How would you prefer to be wished ?", Keys.ENTER, "1. Plain Text", Keys.ENTER, "2. Some Fancy Text", Keys.ENTER, "3. Ya-Ya whatever dude"],
    ["Hmmm,"," ohh but"," this is just"," a plan text"," editor", Keys.ENTER, "Let me"," see what"," i ","can do ", Keys.ENTER,
     "******************************************************************************************", Keys.ENTER,
     "*  __    __       ___      .______   .______   ____    ____                              *", Keys.ENTER,
     "* |  |  |  |     /   \     |   _  \  |   _  \  \   \  /   /                              *", Keys.ENTER,
     "* |  |__|  |    /  ^  \    |  |_)  | |  |_)  |  \   \/   /                               *", Keys.ENTER,
     "* |   __   |   /  /_\  \   |   ___/  |   ___/    \_    _/                                *", Keys.ENTER,
     "* |  |  |  |  /  _____  \  |  |      |  |          |  |                                  *", Keys.ENTER,
     "* |__|  |__| /__/     \__\ | _|      | _|          |__|                                  *", Keys.ENTER,
     "*                                                                                        *", Keys.ENTER,
     "* .______    __  .______     .___________. __    __   _______       ___    ____    ____  *", Keys.ENTER,
     "* |   _  \  |  | |   _  \    |           ||  |  |  | |       \     /   \   \   \  /   /  *", Keys.ENTER,
     "* |  |_)  | |  | |  |_)  |   `---|  |----`|  |__|  | |  .--.  |   /  ^  \   \   \/   /   *", Keys.ENTER,
     "* |   _  <  |  | |      /        |  |     |   __   | |  |  |  |  /  /_\  \   \_    _/    *", Keys.ENTER,
     "* |  |_)  | |  | |  |\  \----.   |  |     |  |  |  | |  '--'  | /  _____  \    |  |      *", Keys.ENTER,
     "* |______/  |__| | _| `._____|   |__|     |__|  |__| |_______/ /__/     \__\   |__|      *", Keys.ENTER,
     "*                                                                                        *", Keys.ENTER,
     "******************************************************************************************", Keys.ENTER,
     Keys.ENTER, Keys.ENTER, "How was that ?", Keys.ENTER, "1. Woooow awesome" + Keys.ENTER, "2. Ok-ok not so impressive", Keys.ENTER, "3. Theek. not upto your level"
     ],
    ["Ohh really ??. Okay let me try to level up later", Keys.ENTER, "But first let tell you something you would have totally forgotten", " Remember that Akshay Khanna interview I asked you quite long back ?"],
    ["Great there were 3 reasons why watching that reminded me of you. " + Keys.ENTER, Keys.ENTER,
     "1. Save this with time stamp & watch later : https://www.youtube.com/watch?v=qxy47a7zpRU&t=553s", Keys.ENTER, "Keywords ['Naive', 'Just go with the flow']", Keys.ENTER, Keys.ENTER,
     "2. Another with time stamp & watch later : https://youtu.be/qxy47a7zpRU?t=647", Keys.ENTER, "Keywords ['Bad memory']" +  Keys.ENTER,
     "3. Dont have the exact time stamp, but look at his left hand being animated.", Keys.ENTER, "The way you do while talking" +  Keys.ENTER,
     "And ofcourse that song in [Gandhi my father].  ;)", Keys.ENTER, Keys.ENTER, Keys.ENTER, Keys.ENTER,
     "Okay", " Okay", " I know", " you got", " bored.", " But before ", "you go", " I have a ", "little magic", " trick for you.", Keys.ENTER, "Want to join ?"
    ]
]


def type_message(message: list[str]):
    global line_counter
    global driver

    sub_actions = ActionChains(driver)
    for msg in message:
        sub_actions.send_keys(msg).pause(0.2)
    sub_actions.send_keys(Keys.ENTER).pause(0.2)
    sub_actions.perform()
    line_counter += 1


def wait_for_response():
    global driver
    # wait for some response in next line
    for i in range(0, 60):
        # lines = driver.find_elements(By.XPATH, "//div[@class='view-line']")
        if len(driver.find_elements(By.XPATH, "//div[@class='view-line']")[line_counter-1].text) > 0:
            break
        time.sleep(1)
    time.sleep(5)

def get_total_line_count():
    return len(driver.find_elements(By.XPATH, "//div[@class='view-line']"))


def fetch_their_response():
    global driver
    return driver.find_elements(By.XPATH, "//div[@class='view-line']")[line_counter-1].text


driver.get("https://rustpad.io/#r8KuIR")
time.sleep(5)
editor = driver.find_elements(By.XPATH, "//div[contains(@class,'editor')]")[1]
actions = ActionChains(driver)
actions.click(editor).perform()

for line in conversations:
    # type the message
    try:
        type_message(line)
        line_counter = get_total_line_count()
        wait_for_response()
        resp = fetch_their_response()
        type_message([Keys.ENTER])
    except:
        continue


type_message(["Cool...", "You know", " its Arijit's Birthday", " today as well", Keys.ENTER, "So i have integrated his soul in this notepad", Keys.ENTER, "After exactly 5 seconds type any random keys on the keyboard and you should here some music"])

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
driver2 = webdriver.Chrome(options=opts, service=ChromeService(ChromeDriverManager().install()))

driver2.get("https://www.musicca.com/piano")
time.sleep(1)

# (from arijit's rough pad).
# arijit uses "#" to indicate a pause
arijit_notes = ["2g", "2g", "#", "3a", "#", "2g", "##", "3c", "3b", "####",
             "2g", "2g", "#", "3a", "#", "2g", "##", "3d", "3c", "####",
             "2g", "2g", "#", "3g", "#", "3e", "#", "3c", "3b", "#", "3a", "####",
             "3f", "3f", "##", "3e", "3c", "3d", "3c", "###"]
# but since you are so obsessed with colon. Let me change it to ":"
the_notes = ["2g", "2g", ":", "3a", ":", "2g", "::", "3c", "3b", "::::",
             "2g", "2g", ":", "3a", ":", "2g", "::", "3d", "3c", "::::",
             "2g", "2g", ":", "3g", ":", "3e", ":", "3c", "3b", ":", "3a", "::::",
             "3f", "3f", "::", "3e", ":", "3c", "::", "3d", ":", "3c", ":::"]

actions = ActionChains(driver2)
# check check
element = driver2.find_element(By.XPATH, f"//*[@data-note='1c']")
actions.move_to_element_with_offset(to_element=element, xoffset=2, yoffset=80).click().perform()
actions.move_to_element_with_offset(to_element=element, xoffset=2, yoffset=80).click().perform()
time.sleep(2)

for note in the_notes:
    time.sleep(0.15)
    if "#" in note or ":" in note:
        for i in range(0, len(note) - 1):
            time.sleep(0.25)
        continue
    element = driver2.find_element(By.XPATH, f"//*[@data-note='{note}']")
    actions.move_to_element_with_offset(to_element=element, xoffset=2, yoffset=80).click().perform()

type_message([Keys.ENTER])
type_message([Keys.ENTER])
type_message(["Aaaai Haaai ... GAJAB ??", " these were your reaction ??", Keys.ENTER, "Thank you ... Thank you..."])
type_message([Keys.ENTER + "Keep smiling like this, and have a wonderful year ahead"])
time.sleep(2)
type_message([Keys.ENTER])
type_message([
"*******************************************************" + Keys.ENTER,
"*    _  _    __  ___ .______   ____    ____  _______  *" + Keys.ENTER,
"*  _| || |_ |  |/  / |   _  \  \   \  /   / |   ____| *"+ Keys.ENTER,
"* |_  __  _||  '  /  |  |_)  |  \   \/   /  |  |__    *"+ Keys.ENTER,
"*  _| || |_ |    <   |   _  <    \_    _/   |   __|   *"+ Keys.ENTER,
"* |_  __  _||  .  \  |  |_)  |     |  |     |  |____  *"+ Keys.ENTER,
"*   |_||_|  |__|\__\ |______/      |__|     |_______| *"+ Keys.ENTER,
"*                                                     *"+ Keys.ENTER,
"*******************************************************"+ Keys.ENTER,
])

time.sleep(5)
driver.quit()
driver2.quit()