import json
import time
import traceback
import logging
from selenium.webdriver.common import action_chains
from selenium.webdriver.support import wait as Wait, expected_conditions as EC
from typing import Tuple
from selenium_testbase import SeleniumTestBase


class ZoomOutbound:

    def __init__(self, config: dict):
        self.close_cookie_button: Tuple[str, str] = (
            "xpath",  "//div[contains(@id,'onetrust-banner')]//button[contains(@class,'onetrust-close-btn')]")
        self.accept_cookies_button: Tuple[str, str] = (
            "xpath",  "//button[normalize-space()='Accept Cookies']")
        self.participants_before_invite = 0
        self.browser = SeleniumTestBase.get_driver()

    def _get_close_cookie_button(self):
        return SeleniumTestBase.get_driver().find_element(self.close_cookie_button[0], self.close_cookie_button[1])

    def _handle_cookie_popup(self) -> None:
        """
        Closes the Cookie Popup, if Popup is visible
        :return:
        """
        if SeleniumTestBase.is_present(self.accept_cookies_button):
            if SeleniumTestBase.get_element(self.accept_cookies_button).is_displayed():
                logging.info("Accept Cookie Button was found. Will click on the Accept Cookie Button")
                SeleniumTestBase.js_click(self.accept_cookies_button)
                time.sleep(2)
            else:
                logging.info("Accept Cookie Button was found in DOM but not visible on screen")

    def login_bridge_as_host(self, bridge_url: str, username: str, password: str):
        """
        Opens the Zoom Bridge & Logs in Zoom Conference as Host
        :param bridge_url: Conference URL of the Bridge
        :param username: Username or Email used to Login
        :param password: Password
        :return:
        """
        SeleniumTestBase.get_driver().get(bridge_url)
        logging.info(f"Opened Bridge URL [{bridge_url}]")
        self._handle_cookie_popup()

        terms_conditions_page = ZoomTermsAndConditionsPage()
        if SeleniumTestBase.is_present(terms_conditions_page.accept_terms_button):
            logging.info("On Terms and condition page, Accept Terms button was found.")
            SeleniumTestBase.get_element(terms_conditions_page.accept_terms_button).click()
            logging.info("Clicked on Accept Terms Button")
            time.sleep(2)

        # bridge_page = ZoomBridgePage()
        # bridge_page.sign_in_button.click()

        login_page = ZoomLoginPage()
        SeleniumTestBase.get_element(login_page.email_txt).send_keys(username)
        logging.info(f"Entered username [{username}]")
        SeleniumTestBase.get_element(login_page.password_txt).send_keys(password)
        logging.info("Entered password [{'*******'}]")
        SeleniumTestBase.get_element(login_page.sign_in_button).click()
        logging.info("Clicked on Sign Button")
        time.sleep(10)

    def open_bridge_url(self, bridge_url: str):
        """
        Opens the Zoom Bridge URL. Used in Approach 2. Directly open the Bridge Page (avoids login)
        :param bridge_url:
        :return:
        """
        SeleniumTestBase.get_driver().get(bridge_url)
        logging.info(f"Opened Bridge URL [{bridge_url}]")
        time.sleep(10)
        SeleniumTestBase.capture_screen()
        self._handle_cookie_popup()

        bridge_page = ZoomBridgePage()
        # check if modal for camera permission is present
        if SeleniumTestBase.is_present(bridge_page.continue_with_mic):
            SeleniumTestBase.click(bridge_page.continue_with_mic)
            logging.info(f"Clicked on Continue without Audio & Video")
            time.sleep(10)
            # check if modal for mic permission is present
            if SeleniumTestBase.is_present(bridge_page.continue_with_mic):
                SeleniumTestBase.click(bridge_page.continue_with_mic)
                logging.info(f"Clicked on Continue without Mic")
                time.sleep(10)

    def start_meeting(self, passcode: str, your_name: str):
        """
        Completes the Joining formalities of the Host to start meeting.
        :return:
        """
        bridge_page = ZoomBridgePage()
        # enter meeting passcode
        SeleniumTestBase.get_element(bridge_page.meeting_passcode_text).send_keys(passcode)
        logging.info(f"Entered Meeting Passcode [{passcode}]")
        # enter your name
        SeleniumTestBase.get_element(bridge_page.your_name_text).send_keys(your_name)
        logging.info(f"Entered Name as [{your_name}]")

        # click on Join Button
        SeleniumTestBase.get_element(bridge_page.join_button).click()
        SeleniumTestBase.capture_screen()
        logging.info(f"Clicked on Join Button : {SeleniumTestBase._screenshot_counter}")


        # wait for the Video Avtar to be visible
        logging.info(f"Current Page URL = [{SeleniumTestBase.get_driver().current_url}]")
        meeting_page = ZoomMeetingPage()
        wait = Wait.WebDriverWait(SeleniumTestBase.get_driver(), timeout=60)
        wait.until(EC.visibility_of_element_located(meeting_page.video_avtar))
        SeleniumTestBase.capture_screen()
        logging.info(f"Video Avtar is visible : {SeleniumTestBase._screenshot_counter}")
        meeting_page.hover_to_show_footer()
        SeleniumTestBase.capture_screen()
        logging.info(f"Hovered to make the Audio Button visible : {SeleniumTestBase._screenshot_counter}")

        logging.info("Meeting Page opened successfully")
        self._handle_cookie_popup()

    def connect_call(self, country_name: str, phone_number: str, country_code: str = "",
                         participant_name: str = "", timeout_seconds: int = 30) -> bool:
        """
        Invites a participant (The prompter) and wait for them to connect
        :param country_code: Phone country code of the participant. Eg +91 for india. Pass empty string if not required
        :param phone_number: Phone number of the participant
        :param country_name: Name of the Country. Pass empty string if not required
        :param participant_name: Optional field. Name of the participant
        :param timeout_seconds: Optional field. Waits for given seconds so that participant joins the call.
        Default time is 30 seconds.
        :return:
        """
        meeting_page = ZoomMeetingPage()
        meeting_page.expand_participants_section()
        meeting_page.expand_participants_section()
        logging.info(f"The Host Clicked on Participants Button")

        # check if Join Audio Dialog is present
        if not SeleniumTestBase.is_present(meeting_page.join_audio_dialog):
            logging.info("Join Audio Dialog was not found. Clicking on Join Audio Button")
            SeleniumTestBase.get_element(meeting_page.join_audio_button).click()
            logging.info(f"The Host Clicked on Join Audio Button")
            time.sleep(2)

        SeleniumTestBase.get_element(meeting_page.call_me_tab).click()
        logging.info("The Host Clicked on Call Me Button")
        SeleniumTestBase.get_element(meeting_page.call_me_country_div).click()
        logging.info("The Host Clicked on Country List")
        country_opt = (meeting_page.call_me_country_option[0], meeting_page.call_me_country_option[1].replace("?", country_name))
        SeleniumTestBase.get_element(country_opt).click()
        logging.info(f"The Host selected Country [{country_name}]")
        SeleniumTestBase.get_element(meeting_page.call_me_phone_number).send_keys(phone_number)
        logging.info(f"The Host entered Phone number [{phone_number}]")
        SeleniumTestBase.get_element(meeting_page.call_me_button).click()
        logging.info("The Host clicked on the Call Me Button")
        wait = Wait.WebDriverWait(SeleniumTestBase.get_driver(), 10)
        wait.until(EC.presence_of_element_located(meeting_page.call_me_connection_status))

        # wait till the participant either gets connected or fails to connect
        counter = 0
        while counter < timeout_seconds:
            # wait till the connection status is present in the DOM
            if "calling" in meeting_page.get_call_connection_status().lower():
                logging.info("The Host Dialed out the phone number to connect audio")

            if "ringing" in meeting_page.get_call_connection_status().lower():
                logging.info("The phone number is ringing")

            if "busy" in meeting_page.get_call_connection_status().lower():
                logging.info("The phone number is busy to connect audio")
                return False

            if "call accepted" in meeting_page.get_call_connection_status().lower():
                # wait till the join audio
                wait = Wait.WebDriverWait(SeleniumTestBase.get_driver(), timeout=60)
                wait.until(lambda d: not SeleniumTestBase.is_present(meeting_page.join_audio_dialog))
                time.sleep(2)
                # unmute if its in mute state
                meeting_page.unmute()
                meeting_page.unmute()
                return True

            time.sleep(1)
            counter = counter + 1
            logging.info(f"Waited {counter} seconds")
        logging.info(
            f"Participant [{participant_name}]-[{phone_number}] was not able to Join the Conference within [{timeout_seconds}] seconds")
        # SeleniumTestBase.get_element(meeting_page.cancel_callout_button).click()
        logging.info(f"Closed the Call out dialog")
        time.sleep(2)
        return False

    def close_bridge(self):
        """
        Closes the Bridge by Ending the meeting for all
        :return:
        """
        meeting_page = ZoomMeetingPage()
        self._handle_cookie_popup()
        time.sleep(2)
        meeting_page.hover_to_show_footer()
        SeleniumTestBase.get_element(meeting_page.leave_button).click()
        time.sleep(1)
        SeleniumTestBase.get_element(meeting_page.leave_button).click()
        logging.info(f"Clicked on Leave Button")
        time.sleep(2)
        SeleniumTestBase.get_element(meeting_page.leave_meeting_button).click()
        time.sleep(1)
        logging.info(f"Clicked on Leave Meeting Button")
        # just capturing 5 screenshots after meeting is closed (not required, but for video purpose)
        for i in range(0, 5):
            time.sleep(5)
            SeleniumTestBase.capture_screen()

    def create_execution_video(self):
        """
        Creates a video from the screenshots taken during execution
        :return:
        """
        pass
        # ScreenCapture.create_video_from_screenshots()

    def test_bridge_call_quality(self, config: dict):
        bridge_url: str = config.get("bridge_url")
        bridge_username: str = config.get("bridge_username")
        bridge_password: str = config.get("bridge_password")
        country_code: str = config.get("invitee_country_code")
        country_name: str = config.get("invitee_country_name")
        phone_number: str = config.get("invitee_phone_number")
        name: str = config.get("invitee_name")
        join_timeout: int = config.get("invitee_join_timeout")  # in seconds
        call_duration: int = config.get("call_duration")  # in seconds

        try:
            self.login_bridge_as_host(bridge_url, bridge_username, bridge_password)
            self.start_meeting()
            flag = self.connect_call(country_code=country_code, phone_number=phone_number, country_name=country_name,
                                     participant_name=name, timeout_seconds=join_timeout)
            if flag:
                prompter_duration_seconds = call_duration
                logging.info(f"Waiting for the Prompter to play enough Audio [{prompter_duration_seconds}]")
                for i in range(0, int(prompter_duration_seconds / 60)):
                    time.sleep(55)
                    # ScreenCapture.capture_screen(self.page)
                    logging.info(f"{(i + 1)} minutes over")

            self.close_bridge()
        except:
            # traceback.logging.info_exc()
            logging.info(traceback.format_exc())
            pass

        finally:
            SeleniumTestBase.capture_screen()
            SeleniumTestBase.get_driver().quit()
            # if not self.page.play_page.is_closed():
            #     ScreenCapture.capture_screen(self.page)
            #     self.page.play_page.close()
            #     self.play.stop()
            # self.create_execution_video()

    def test_bridge_call_quality_approach_2(self, config: dict):
        bridge_url: str = config.get("bridge_url")
        # bridge_username: str = config.get("bridge_username")
        # bridge_password: str = config.get("bridge_password")
        bridge_passcode: str = config.get("bridge_passcode")
        country_code: str = config.get("invitee_country_code")
        country_name: str = config.get("invitee_country_name")
        phone_number: str = config.get("invitee_phone_number")
        name: str = config.get("invitee_name")
        join_timeout: int = config.get("invitee_join_timeout")  # in seconds
        call_duration: int = config.get("call_duration")  # in seconds

        try:
            if SeleniumTestBase._enable_browser_HAR:
                self.start_browser_HAR_capture()
            self.open_bridge_url(bridge_url)
            self.start_meeting(bridge_passcode, "Spearline Bot")
            flag = self.connect_call(country_code=country_code, phone_number=phone_number, country_name=country_name,
                                     participant_name=name, timeout_seconds=join_timeout)
            if flag:
                prompter_duration_seconds = call_duration
                logging.info(f"Waiting for the Prompter to play enough Audio [{prompter_duration_seconds}]")
                for i in range(0, int(prompter_duration_seconds / 60)):
                    time.sleep(55)
                    # ScreenCapture.capture_screen(self.page)
                    logging.info(f"{(i + 1)} minutes over")

            self.close_bridge()
        except:
            # traceback.logging.info_exc()
            if SeleniumTestBase._enable_page_source_dump:
                SeleniumTestBase.dump_page_source()
            if SeleniumTestBase._enable_browser_HAR:
                self.stop_proxy_server()
                self.dump_HAR_file_contents()
            logging.info(traceback.format_exc())
            pass

        finally:
            SeleniumTestBase.capture_screen()
            logging.info(f"Captured the final screen before quitting")
            SeleniumTestBase.get_driver().quit()

    def start_browser_HAR_capture(self):
        if SeleniumTestBase._enable_browser_HAR:
            logging.info("Started capturing Network Logs with Headers, Cookies & Content")
            SeleniumTestBase.proxy_client.new_har("zoom_bridge", options={"captureHeaders": True, "captureCookies": True, "captureContent": True})

    def stop_proxy_server(self):
        if SeleniumTestBase._enable_browser_HAR:
            logging.info("Stopping the BrowserMob Proxy Server")
            SeleniumTestBase.browser_server.stop()

    def dump_HAR_file_contents(self):
        if SeleniumTestBase._enable_browser_HAR:
            har_data = SeleniumTestBase.proxy_client.har
            logging.info(
                f"Dumped Network logs into file [/home/screenshot/zoom_outbound/zoom_outbound_network_log.har]")
            with open("/home/screenshot/zoom_outbound/zoom_outbound_network_log.har", "w") as har_file:
                json.dump(har_data, har_file, indent=4)


class ZoomTermsAndConditionsPage:
    """
    Terms & Conditions page
    """
    def __init__(self):
        # super().__init__()
        self.accept_terms_button: Tuple[str, str] = (
            "xpath",  "//div[@id='privacy_unlogin_layout1']//button[text()='I Agree']")


class ZoomBridgePage:
    def __init__(self):
        # super().__init__(job_id=None)
        self.sign_in_button: Tuple[str, str] = ("xpath",  "//button[@id='button_sign_in']")
        self.user_icon: Tuple[str, str] = ("xpath", "//div[contains(@class,'avatar-container')]")
        self.sign_out_button: Tuple[str, str] = ("xpath", "//button[text()='Sign Out']")
        self.launch_meeting_button: Tuple[str, str] = ("xpath", "//div[normalize-space()='Launch Meeting']")
        self.continue_with_mic: Tuple[str, str] = ("xpath", "//permission[@id='ask-permission-button']")
        self.continue_without_mic: Tuple[str, str] = ("xpath", "//div[@class='ask-permission-prompt']//div[contains(@class,'continue-without')]")
        self.join_from_browser_link: Tuple[str, str] = ("xpath", "//a[normalize-space()='Join from your browser']")
        self.meeting_passcode_text: Tuple[str, str] = ("xpath", "//input[@id='input-for-pwd']")
        self.your_name_text: Tuple[str, str] = ("xpath", "//input[@id='input-for-name']")
        self.join_button: Tuple[str, str] = ("xpath", "//button[normalize-space()='Join']")
        self.i_agree_button: Tuple[str, str] = ("xpath", "//button[normalize-space()='I Agree']")


class ZoomLoginPage:
    def __init__(self):
        self.email_txt: Tuple[str, str] = ("xpath", "//input[@id='email']")
        self.password_txt: Tuple[str, str] = ("xpath", "//input[@id='password']")
        self.sign_in_button: Tuple[str, str] = ("xpath", "//button[./span[contains(text(),'Sign In')]]")


class ZoomMeetingPage:
    def __init__(self):

        self.join_audio_button: Tuple[str, str] = ("xpath", "//button[contains(@class,'join-audio')]")
        self.join_audio_dialog: Tuple[str, str] = ("xpath", "//div[@class='join-dialog']")
        self.computer_audio_tab: Tuple[str, str] = ("xpath", "//span[text()='Computer Audio']/parent::div")
        self.call_me_tab: Tuple[str, str] = ("xpath", "//span[text()='Call Me']/parent::div")
        self.join_audio_by_computer_button: Tuple[str, str] = (
            "xpath", "//button[text()='Join Audio by Computer']")
        self.call_me_country_div: Tuple[str, str] = (
            "xpath", "//div[@class='join-audio-by-call-out']//div[contains(@class,'country-select')]")
        self.call_me_country_option: Tuple[str, str] = (
            "xpath", "//div[@id='react-select-3-listbox']//div[contains(text(),'?')]")
        self.call_me_phone_number: Tuple[str, str] = (
            "xpath", "//div[@class='join-audio-by-call-out']//input[contains(@class,'phone-number')]")
        self.call_me_button: Tuple[str, str] = ("xpath", "//button[text()='Call Me']")
        self.call_me_connection_status: Tuple[str, str] = ("xpath", "//p[contains(@class,'connection-status')]")

        self.video_avtar: Tuple[str, str] = ("xpath", "//div[@class='video-avatar__avatar-name']")
        self.video_layout: Tuple[str, str] = ("xpath", "//div[@class='video-share-layout']")
        self.participants_button: Tuple[str, str] = ("xpath", "//button[.//span[text()='Participants']]")
        self.participant_section: Tuple[str, str] = ("xpath", "//div[@aria-label='participants']")
        self.invite_participant_button: Tuple[str, str] = ("xpath", "//button[text()='Invite']")
        self.no_of_participants: Tuple[str, str] = ("xpath", "//div[@class='participants-item-position']")
        self.call_out_tab: Tuple[str, str] = ("xpath", "//button[.//span[text()='Call Out']]")
        self.invitee_name_txt: Tuple[str, str] = ("xpath", "//input[@id='inviteeName']")
        self.invitee_phone_txt: Tuple[str, str] = ("xpath", "//input[@id='inviteePhone']")
        self.invitee_country_list: Tuple[str, str] = (
            "xpath", "//div[contains(@class,'country-code-select')]")
        self.call_participant_button: Tuple[str, str] = ("xpath", "//button[text()='Call']")
        self.cancel_callout_button: Tuple[str, str] = (
            "xpath", "//div[contains(@class,'invite-footer')]//button[text()='Cancel']")
        self.end_button: Tuple[str, str] = ("xpath", "//button[normalize-space()='End']")
        self.end_meeting_for_all_button: Tuple[str, str] = (
            "xpath", "//button[text()='End Meeting for All']")
        self.leave_button: Tuple[str, str] = ("xpath", "//button[@aria-label='End']")
        self.leave_meeting_button: Tuple[str, str] = ("xpath", "//button[normalize-space()='Leave Meeting']")

    def get_call_connection_status(self) -> str:
        if SeleniumTestBase.is_present(self.call_me_connection_status):
            return SeleniumTestBase.get_element(self.call_me_connection_status).text

    def expand_participants_section(self):
        if not SeleniumTestBase.is_present(self.participant_section):
            self.hover_to_show_footer()
            SeleniumTestBase.get_element(self.participants_button).click()
            time.sleep(1)

    def unmute(self):
        if SeleniumTestBase.is_present(self.join_audio_button):
            logging.info(f'Currently you have to [{SeleniumTestBase.get_element(self.join_audio_button).get_attribute("aria-label")}]')
            if "unmute" in SeleniumTestBase.get_element(self.join_audio_button).get_attribute("aria-label").lower():
                self.hover_to_show_footer()
                SeleniumTestBase.get_element(self.join_audio_button).click()
                time.sleep(2)

    def hover_to_show_footer(self):
        if SeleniumTestBase.is_present(self.join_audio_button):
            if not SeleniumTestBase.get_element(self.join_audio_button).is_displayed():
                # hover over the meeting page to make audio button visible
                actions = action_chains.ActionChains(SeleniumTestBase.get_driver())
                actions.move_to_element(SeleniumTestBase.get_element(self.video_layout)).perform()
                time.sleep(0.5)
                actions.move_to_element_with_offset(SeleniumTestBase.get_element(self.video_layout), 15, 15).perform()
