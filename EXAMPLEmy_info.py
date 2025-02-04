# Here is the location to fill in all your data for the web portal.
# (this is only designed to work with Michigan Connections Academy, but break it til you make it!)


username = ""
password = ""

# -----------------------------------------------------------------------
# URLs
# -----------------------------------------------------------------------

login_url = "https://www.connexus.com/login.aspx?partner=connectionsAcademy"

# success url is your home page, this is used to confirm the login was successful
# to find this url, just log in as you normally would and copy and paste the full url here
# for MI connections mine looked something like "https://www.connexus.com/webmail#/mailbox/{xxxxxxx}/folder/{yyyyyyyy}"
success_url = ""

home_url = "https://www.connexus.com/homepage#/caretaker/myhousehold"

assignments_url = "https://www.connexus.com/planner/overdueLessons.aspx?idWebuser=*******"
# (******* = your webuser id. copy a link to your overdue assignmnts page if you get lost)

attendance_url = ("https://www.connexus.com/attendance/enterAttendance.aspx?idLocation=*******&household=true&sendTo"
                  "=/homepage")
# again, the stars are probably your web id, or just copy a link to the attendance page.

# -----------------------------------------------------------------------
# no school: days when there is no school scheduled
# -----------------------------------------------------------------------

# school_calendar = "https://www.connectionsacademy.com/michigan-virtual-school/overview/school-calendar/"
# list of no_school days = 11-23, 11-24, 12-25, 12-26, 12-27, 12-28, 12-29, 12-30, 12-31, 1-1, 1-2, 1-3, 1-15, 2-19,
# 5-27

from datetime import date

today = date(2023, 11, 14)  # these are all formatted as: (year, month, day)
last_day = date(2024, 6, 7)
diff = last_day - today
days_left = diff.days

if today > last_day:
    is_summer = True
else:
    is_summer = False

# Here, I went through the school calendar and noted all the days that there was no school.
# I'm sure there's a better way, but here we are.
off_days = date(2023, 11, 23), date(2023, 11, 24), date(2023, 12, 25), date(2023, 12, 26), date(2023, 12, 27), date(
    2023, 12, 28), date(2023, 12, 29), date(2023, 12, 30), date(2023, 12, 31), date(2024, 1, 1), date(2024, 1, 2), date(
    2024, 1, 3), date(2024, 1, 15), date(2024, 2, 19), date(2024, 5, 27)

if today in off_days:
    no_school = True
else:
    no_school = False

# -----------------------------------------------------------------------
# Args
# -----------------------------------------------------------------------

# Sets whether a visible Chrome window will be displayed. IF SHIT GOES AWRY, SET THIS TO YES AND TRY TO FIGURE IT OUT
# This will accept yes, y, no and n, will default to non-headless (head-ed?)
is_headless = "no"

# This area will decide if the console window will keep itself open after finishing,
# so you can confirm that everything went well
# OR choose to close itself after all is finished with that Devil may care attitude of yours
keep_open = "yes"

# **************************************************************************************************************
# If you're feeling brave you can edit below this line to try and change the element id of the login/pass boxes,
# but it will almost certainly break all the things

username_id = "loginFormEmail"
password_id = "loginFormPassword"
submit_button_id = "loginFormButton"
