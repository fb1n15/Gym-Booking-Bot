import time
from datetime import date
from datetime import datetime
from datetime import timedelta

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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


def book(email, days_in_future, slot_time, driver):
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
        ).send_keys(f'{email}')

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
    except TimeoutException:
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

    # select the time slot
    current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
    print(f"local time = {current_time}")
    deadline = "00:05:00"
    sunrise_time = "04:05:00"
    today = date.today()
    print("Today's date:", today)
    booking_date = today + timedelta(days=days_in_future)
    booking_date = booking_date.strftime("%Y/%m/%d")
    print("Booking date:", booking_date)

    # move to next week if days_in_futre > 6
    if days_in_future > 6:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,
                                        "ctl00_MainContent_dateForward1"))
            ).click()

        time.sleep(2)
        print("Must go to next page.")
    else:
        print("Don't need to go to next page.")

    while current_time >= sunrise_time or current_time <= deadline:
        try:
            if days_in_future <= 6:
                button_index = int(int(slot_time) - 7) * 7 + days_in_future
            else:  # because the calendar go to the next page.
                button_index = int(int(slot_time) - 7) * 7 + days_in_future - 7
            print(f"The date trying to book = {booking_date}")
            print(f"The time slot trying to book = {slot_time}")
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID,
                                            f"ctl00_MainContent_cal_calbtn{button_index}"))
                ).click()

            # select the court

            for court_index in range(1, 5):
                try:
                    if len(slot_time) == 1:
                        WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        f"input[data-qa-id='button-ActivityID=HIFCASBADM ResourceID=0 Date={booking_date} Time=0{slot_time}:00 Availability= Available Court=Jubilee Court {court_index}']"))
                            ).click()

                    elif len(slot_time) == 2:
                        print("data-qa-id:")
                        print(
                            f"input[data-qa-id='button-ActivityID=HIFCASBADM ResourceID=0 Date={booking_date} Time={slot_time}:00 Availability= Available Court=Jubilee Court {court_index}']")
                        WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        f"input[data-qa-id='button-ActivityID=HIFCASBADM ResourceID=0 Date={booking_date} Time={slot_time}:00 Availability= Available Court=Jubilee Court {court_index}']"))
                            ).click()
                    else:
                        print(
                            "Wrong slot time format, input 19 if you want to book a 7 p.m. court")
                except TimeoutException:
                    print(f"Fail to book court {court_index}.")
                    print(f"Try court {court_index + 1}.")
                    continue
                else:
                    break

            # conform the booking
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,
                                                "ctl00_MainContent_btnBasket"))
                    ).click()

            except TimeoutException:
                print("Fail to book the slot, you could try run the program again.")
            else:
                print(f"Successfully robbed the badminton court (court {court_index})!!!")
        except TimeoutException:
            print("No available slots, we will keep trying until 00:05")
            current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
            print(f"Current local time = {current_time}")
            driver.refresh()
        else:
            break

    # wait for a while
    try:
        WebDriverWait(driver, 180).until(
            EC.element_to_be_clickable((By.ID,
                                        "ctl00_MainContent_btnBasket"))
            ).click()
    except TimeoutException:
        print("Good Bye")


def main(username, email, password, days_in_future, slot_time):
    print("Let's book a badminton court. 🐶")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # comment out to toggle headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://sussed.soton.ac.uk/")

    login(username, password, driver)
    book(email, days_in_future, slot_time, driver)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('username', type=str, help='Username')
    parser.add_argument('email', type=str, help='university email')
    parser.add_argument('pw', type=str, help='Password')
    parser.add_argument('days_in_future', type=int,
                        help='Which date to book, e.g., 7 days later')
    parser.add_argument('time', type=str, help='time of the slot')

    args = parser.parse_args()

    main(args.username, args.email, args.pw, args.days_in_future, args.time)
