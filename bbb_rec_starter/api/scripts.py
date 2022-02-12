from bigbluebutton_api_python import BigBlueButton

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from bbb_rec_starter.settings import BBB_SECRET, BBB_ENDPOINT


def start_recording(meeting_id):
    b = BigBlueButton(BBB_ENDPOINT, BBB_SECRET)
    if not b.is_meeting_running(meeting_id=meeting_id).is_meeting_running():
        return_code = 512
        status = "The specified meeting hasn't started yet"
        return status, return_code
    meeting_info = b.get_meeting_info(meeting_id=meeting_id)
    if not meeting_info.get_field("recording") == "true":
        return_code = 515
        status = "The specified meeting has recording not enabled"
        return status, return_code
    meeting_url = b.get_join_meeting_url(
        "StartRecordingUser", meeting_id, meeting_info.get_field("moderatorPW")
    )

    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    status = "ok"
    return_code = 200

    try:
        browser.get(meeting_url)
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Close Join audio modal'][1]"))
            WebDriverWait(browser, 5).until(element_present)
        except TimeoutException:
            print("Timeout")
        close = browser.find_element(By.XPATH, "//button[@aria-label='Close Join audio modal'][1]")
        close.click()
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Start recording'][1]"))
            WebDriverWait(browser, 2).until(element_present)
        except:
            try:
                element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Pause recording'][1]"))
                WebDriverWait(browser, 2).until(element_present)
                status = "The recording has already been started"
                return_code = 514
                return status, return_code
            except:
                element_present = expected_conditions.presence_of_element_located((By.XPATH, "//div[@aria-label='Resume recording'][1]"))
                WebDriverWait(browser, 2).until(element_present)
                status = "The recording has been paused manually"
                return_code = 514
                return status, return_code
        record = browser.find_element(By.XPATH, "//div[@aria-label='Start recording'][1]")
        print(record)
        record.click()
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Yes'][1]"))
            WebDriverWait(browser, 3).until(element_present)
        except TimeoutException:
            print("Timeout")
        yes = browser.find_element(By.XPATH, "//button[@aria-label='Yes'][1]")
        yes.click()
    except:
        status = "Internal server error. Contact server administrator to get further information."
        return_code = 500
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, "error-message"))
            WebDriverWait(browser, 5).until(element_present)
        except TimeoutException:
            print("Timeout")
            return status, return_code
        info = browser.find_element(By.XPATH, "error-message")
        if info.text == "You either did not supply a password or the password supplied is neither the attendee or moderator password for this conference.":
            return_code = 513
            status = "Wrong password for meeting specified"
        else:
            status = info.text
        browser.get_screenshot_as_file(f"{meeting_id}.png")
    finally:
        browser.quit()
    return status, return_code
