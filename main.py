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
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'loginUsername'))
        ).send_keys(username)

    driver.find_element_by_id('loginPassword').send_keys(pw)

    driver.find_element_by_css_selector(
        '#fm1 > div.form-group.text-center.submit-box > button').click()
    WebDriverWait(driver, 5)


def book(gym_time, driver):
    WebDriverWait(driver, 5).until(
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
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/nav/div/a'))
            ).click()
    except Exception:
        print("fail to click the LOGIN button")
        pass

    print("Current window title: " + driver.title)
    # input the username
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME,
                                    'loginfmt'))
        ).send_keys('fb1n15@soton.ac.uk')

    # click the next button
    driver.find_element_by_id('idSIButton9').click()

    # input the password
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME,
                                    'passwd'))
        ).send_keys('Fanbi12345')

    # click the next button
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID,
                                    'idSIButton9'))
        ).click()

    # in case for the stay signed in page
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID,
                                        'idSIButton9'))
            ).click()
    except Exception:
        pass

    # click make a booking button
    # input the password
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div/main/div/div/div[2]/div/div[2]/form/input[2]"))
        ).click()

    print("Current window title: " + driver.title)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'))
        ).send_keys('Fanbi12345')


def main(gym_time):
    t = datetime.datetime.now()
    print('[STARTING] Signing up for {} gym slot on {} at {}'.format(gym_time,
                                                                     t.strftime('%m:%d'),
                                                                     t.strftime('%H:%M')))

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # comment out to toggle headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://sussed.soton.ac.uk/")

    login('fb1n15', 'Fanbi12345', driver)
    book(17, driver)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
