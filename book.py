import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime
import pytz  
import config
import room_config

def get_time_till(hour, min):
    now = datetime.datetime.now(pytz.timezone('America/New_York')) 
    target_time = now.replace(hour=hour, minute=min, second=0, microsecond=0)
    time_remaining = (target_time - now).total_seconds()
    if time_remaining < 0:
        target_time += datetime.timedelta(days=1)
        time_remaining = (target_time - now).total_seconds()
    return time_remaining

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(config.link)

for room in room_config.rooms:
    driver.find_element("xpath", room.room_number_xpath).click() 

time_remaining = get_time_till(config.hour, config.minute) 
time.sleep(time_remaining)

driver.find_element("xpath", "/html/body/form/button").click()

# choose the new day
today = driver.find_element(By.CLASS_NAME, "ui-datepicker-today")  # click today's date
siblings = today.find_elements(By.XPATH, "following-sibling::*") # the following dates in our row
next_row = today.find_elements(By.XPATH, "./../following-sibling::tr[1]//td") # the next row

if len(siblings) < 3: # we should check the next row
    next_row[ 3 - len(siblings) - 1].click()
else:
    siblings[2].click()

driver.find_element(By.XPATH, "/html/body/form/button[2]").click() # next button

for i, room in enumerate(room_config.rooms):
    Select(driver.find_element(By.XPATH, room.hour_xpath)).select_by_value(room.hour)
    Select(driver.find_element(By.XPATH, room.min_xpath)).select_by_value(room.min)
    Select(driver.find_element(By.XPATH, room.pm_xpath)).select_by_index(room.am_pm)

driver.find_element(By.XPATH, "/html/body/form/button[2]").click() # next button

Select(driver.find_element(By.XPATH, "/html/body/form/div[2]/table/tbody/tr/td[2]/select")).select_by_index(1) # reason for reservation

driver.find_element(By.XPATH, "/html/body/form/div[4]/table/tbody/tr[1]/td[2]/input").send_keys(config.name)
driver.find_element(By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td[2]/input").send_keys(config.email)
submit_button = driver.find_element(By.XPATH, "/html/body/form/div[4]/button")
submit_button.click()

print("Booking finished...")
time.sleep(1)
print("\nClosing now")
driver.close()