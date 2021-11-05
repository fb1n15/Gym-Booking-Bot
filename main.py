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


def book(days_in_future, slot_time, driver):
    # get current window handle
    p = driver.current_window_handle
    print(f"Current window title: {p}")

    # Search for badminton courts
    for i in range(30):
        # get first child window
        chwd = driver.window_handles

        for w in chwd:
            # switch focus to child window
            if w != p:
                driver.switch_to.window(w)
        print("Current window title: " + driver.title)

        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID,
                                            "ctl00_ctl11_SearchTextBox"))
                ).send_keys('Badminton 55 Mins')

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,
                                            "ctl00_ctl11_SearchButton1"))
                ).click()
        except TimeoutException:
            print("Please go to the booking page.")
            continue
        else:
            break

    if i == 29:  # fail to go to the booking page.
        print("Timeout, you could rerun the program.")
        exit()

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
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID,
                                            f"ctl00_MainContent_cal_calbtn{button_index}"))
                ).click()

            # select the court

            for court_index in range(4, 0, -1):
                try:
                    print("data-qa-id contains:")
                    print(
                            f"{slot_time}:00 Availability= Available Court=Jubilee Court {court_index}")
                    WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    f"input[data-qa-id*='{slot_time}:00 Availability= Available Court=Jubilee Court {court_index}']"))
                        ).click()

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
                print("Fail to book the slot, you could try to run the program again.")
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


def main(days_in_future, slot_time, change_website=False):
    print("Let's book a badminton court. 🐶")
    options = webdriver.ChromeOptions(

        )
    options.add_argument('headless')  # comment out to toggle headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    if change_website:
        driver.get("https://soton.leisurecloud.net/Connect/mrmlogin.aspx")
    else:
        driver.get("https://sussed.soton.ac.uk/")

    # login(username, password, driver)
    book(days_in_future, slot_time, driver)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # parser.add_argument('username', type=str, help='Username')
    # parser.add_argument('email', type=str, help='university email')
    # parser.add_argument('pw', type=str, help='Password')
    parser.add_argument('days_in_future', type=int,
                        help='Which date to book, e.g., 7 days later')
    parser.add_argument('time', type=str, help='time of the slot')
    parser.add_argument('-y', '--change_website', action='store_true',
                        help='to change the website address')

    args = parser.parse_args()
    print(args.change_website)

    main(args.days_in_future, args.time, args.change_website)
