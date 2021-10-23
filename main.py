import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

# https://stackoverflow.com/questions/40555930/selenium-chromedriver-executable-needs-to-be-in-path
from webdriver_manager.chrome import ChromeDriverManager


def login(username, pw, driver):
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, 'ctl00_MainContent_InputLogin'))
        ).send_keys(username)

    driver.find_element_by_id('ctl00_MainContent_InputPassword').send_keys(pw)

    driver.find_element_by_id('ctl00_MainContent_btnLogin').click()
    WebDriverWait(driver, 5)


def book(gym_time, driver):

    try:
        # Selects gym slot register button with corresponding time
        driver.find_element_by_id('ctl00_ctl11_SearchTextBox').send_keys('Badminton 55 Mins')
    except:
        raise Exception('Cannot search Badminton 55 Mins slots')


def main(gym_time):
    t = datetime.datetime.now()
    print('[STARTING] Signing up for {} gym slot on {} at {}'.format(gym_time,
                                                                     t.strftime('%m:%d'),
                                                                     t.strftime('%H:%M')))

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # comment out to toggle headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://soton.leisurecloud.net/Connect/mrmlogin.aspx")

    login('fb1n15@soton.ac.uk', 'Fanbi12345', driver)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
