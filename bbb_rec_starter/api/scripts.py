from bigbluebutton_api_python import BigBlueButton

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from bbb_rec_starter.settings import BBB_SECRET, BBB_ENDPOINT


def start_recording(meeting_id, password, user):
    b = BigBlueButton(BBB_ENDPOINT, BBB_SECRET)
    meeting_url = b.get_join_meeting_url(user, meeting_id, password)

    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    try:
        browser.get(meeting_url)
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Close Join audio modal'][1]"))
            WebDriverWait(browser, 5).until(element_present)
        except TimeoutException:
            print("Timeout")
        close = browser.find_element_by_xpath("//button[@aria-label='Close Join audio modal'][1]")
        close.click()
        record = browser.find_element_by_xpath("//div[@aria-label='Not recording'][1]")
        record.click()
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//button[@aria-label='Yes'][1]"))
            WebDriverWait(browser, 3).until(element_present)
        except TimeoutException:
            print("Timeout")
        yes = browser.find_element_by_xpath("//button[@aria-label='Yes'][1]")
        yes.click()
    except:
        browser.get_screenshot_as_file(f"{meeting_id}.png")
    finally:
        browser.quit()
