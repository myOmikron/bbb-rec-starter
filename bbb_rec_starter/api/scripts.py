from threading import Thread

from bigbluebutton_api_python import BigBlueButton
from bigbluebutton_api_python.exception import BBBException

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from bbb_rec_starter.settings import BBB_SECRET, BBB_ENDPOINT


class Fred(Thread):
    def __init__(self, meeting_id):
        super(Fred, self).__init__()
        self.meeting_id = meeting_id
        self.ret = ()
        self.browser = None

    def kill(self):
        self.browser.quit() if self.browser else None

    def run(self):
        self.ret = self.start_recording()

    def start_recording(self):
        meeting_id = self.meeting_id

        try:
            b = BigBlueButton(BBB_ENDPOINT, BBB_SECRET)
            try:
                meeting_info = b.get_meeting_info(meeting_id=meeting_id)
            except BBBException:
                return_code = 512
                status = "The specified meeting hasn't started yet"
                return status, return_code
            if not meeting_info.get_field("recording") == "true":
                return_code = 515
                status = "The specified meeting has recording not enabled"
                return status, return_code
            meeting_url = b.get_join_meeting_url(
                "StartRecordingUser", meeting_id, meeting_info.get_field("moderatorPW")
            )

            status = "ok"
            return_code = 200

            chrome_options = Options()
            chrome_options.headless = True
            chrome_options.add_argument("--window-size=1920,1080")
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browser.get(meeting_url)
            try:
                element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Close Join audio modal'][1]"))
                WebDriverWait(self.browser, 10).until(element_present)
            except TimeoutException:
                print("Timeout")
            close = self.browser.find_element(By.XPATH, "//button[@aria-label='Close Join audio modal'][1]")
            close.click()
            try:
                element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Start recording'][1]"))
                WebDriverWait(self.browser, 10).until(element_present)
            except:
                try:
                    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Pause recording'][1]"))
                    WebDriverWait(self.browser, 10).until(element_present)
                    status = "The recording has already been started"
                    return_code = 514
                    return status, return_code
                except:
                    element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Resume recording'][1]"))
                    WebDriverWait(self.browser, 10).until(element_present)
                    status = "The recording has been paused manually"
                    return_code = 514
                    return status, return_code
            record = self.browser.find_element(By.XPATH, "//div[@aria-label='Start recording'][1]")
            print(record)
            record.click()
            try:
                element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Yes'][1]"))
                WebDriverWait(self.browser, 10).until(element_present)
            except TimeoutException:
                print("Timeout")
            yes = self.browser.find_element(By.XPATH, "//button[@aria-label='Yes'][1]")
            yes.click()
        except:
            status = "Internal server error. Contact server administrator to get further information."
            return_code = 500
            try:
                element_present = expected_conditions.presence_of_element_located((By.ID, "error-message"))
                WebDriverWait(self.browser, 10).until(element_present)
            except TimeoutException:
                print("Timeout")
                return status, return_code
            info = self.browser.find_element(By.XPATH, "error-message")
            if info.text == "You either did not supply a password or the password supplied is neither the attendee or moderator password for this conference.":
                return_code = 513
                status = "Wrong password for meeting specified"
            else:
                status = info.text
            self.browser.get_screenshot_as_file(f"{meeting_id}.png")
        finally:
            self.kill()
        return status, return_code
