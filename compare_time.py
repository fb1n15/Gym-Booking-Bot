from datetime import datetime

# current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
# print(f"local time = {current_time}")
# deadline = "00:05:00"
# sunrise_time = "04:05:00"
#
# if deadline <= current_time <= sunrise_time:
#     print("We have passed the deadline")
# else:
#     print("We haven't reached the deadline")

# get the date
from datetime import date, timedelta

today = date.today()
print("Today's date:", today)
today = today + timedelta(days=7)
today = today.strftime("%Y/%m/%d")
print("Today's date:", today)
