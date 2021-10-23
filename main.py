import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from selenium import webdriver

# https://stackoverflow.com/questions/40555930/selenium-chromedriver-executable-needs-to-be-in-path
from webdriver_manager.chrome import ChromeDriverManager


def login(username, pw, driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'loginUsername'))
        ).send_keys(username)

    driver.find_element_by_id('loginPassword').send_keys(pw)

    driver.find_element_by_css_selector(
        '#fm1 > div.form-group.text-center.submit-box > button').click()
    WebDriverWait(driver, 10)


def book(slot_time, driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="_TargetedContent_WAR_luminis_INSTANCE_7auCc2KRa4O0_TCBlockPanel"]/div[3]/div/div/div/div/div/div/div/div[20]/div/div/p/a'))
        ).click()

    time.sleep(0.9)
    # switch to the login tab
    # https://www.browserstack.com/guide/how-to-switch-tabs-in-selenium-python
    # prints parent window title
    print("Parent window title: " + driver.title)

    # get current window handle
    p = driver.current_window_handle
    print(f"Current window title: {p}")

    # get first child window
    chwd = driver.window_handles

    for w in chwd:
        # switch focus to child window
        if w != p:
            driver.switch_to.window(w)
    print("Current window title: " + driver.title)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/nav/div/a'))
            ).click()
    except Exception:
        print("fail to click the LOGIN button")
        pass

    print("Current window title: " + driver.title)
    # input the username
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME,
                                    'loginfmt'))
        ).send_keys('fb1n15@soton.ac.uk')

    # click the next button
    driver.find_element_by_id('idSIButton9').click()

    # input the password
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME,
                                    'passwd'))
        ).send_keys('Fanbi12345')

    # click the next button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID,
                                    'idSIButton9'))
        ).click()

    # in case for the stay signed in page
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,
                                        'idSIButton9'))
            ).click()
    except Exception:
        pass

    # click make a booking button
    # input the password
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div/main/div/div/div[2]/div/div[2]/form/input[2]"))
        ).click()

    print("Current window title: " + driver.title)

    # Search for badminton courts
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID,
                                    "ctl00_ctl11_SearchTextBox"))
        ).send_keys('Badminton 55 Mins')

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID,
                                    "ctl00_ctl11_SearchButton1"))
        ).click()

    # move to next week
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID,
                                    "ctl00_MainContent_dateForward1"))
        ).click()

    # select the time slot
    try:
        button_index = int(int(slot_time) - 7) * 7
        print(f"button index = {button_index}")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,
                                        f"ctl00_MainContent_cal_calbtn{button_index}"))
            ).click()
    except ValueError:
        print("No available slots")
        exit()

    # select the court
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "input[data-qa-id='button-ActivityID=HIFCASBADM ResourceID=0 Date=2021/10/30 Time=07:00 Availability= Available Court=Jubilee Court 1']"))
        ).click()

    # # conform the booking
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.ID,
    #                                 "ctl00_MainContent_cal_calbtn1"))
    #     ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'))
        ).send_keys('Fanbi12345')


def main(username, password, slot_time):
    t = datetime.datetime.now()
    print('[STARTING] Signing up for {} gym slot on {} at {}'.format(slot_time,
                                                                     t.strftime('%m:%d'),
                                                                     t.strftime('%H:%M')))

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # comment out to toggle headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://sussed.soton.ac.uk/")

    login(username, password, driver)
    book(slot_time, driver)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('username', type=str, help='Username')
    parser.add_argument('pw', type=str, help='Password')
    parser.add_argument('time', type=str, help='time of the slot')
    # parser.add_argument('floor', type=str, help='Select the gym floor you want')
    # parser.add_argument('time', type=str, help='Select the gym time you want')

    args = parser.parse_args()

    main(args.username, args.pw, args.time)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
