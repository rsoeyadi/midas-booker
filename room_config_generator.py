from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import config

def input_valid_time(prompt):
    while True:
        time_str = input(prompt)
        try:
            hour, minute = map(int, time_str.split(":"))
            if 0 <= hour <= 12 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"
            else:
                print("Invalid time format. Please enter a valid time (HH:MM).")
        except ValueError:
            print("Invalid time format. Please enter a valid time (HH:MM).")


def generate_xpaths(index):
    base_xpath = "/html/body/form/div[2]/div/div[{}]/select[{}]"
    return {
        "hour_xpath": f"\'{base_xpath.format(6 * index, 1)}\'",
        "min_xpath": f"\'{base_xpath.format(6 * index, 2)}\'",
        "pm_xpath": f"\'{base_xpath.format(6 * index, 3)}\'",
    }


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(config.link)

room_labels = driver.find_elements(
    By.XPATH, "/html/body/form/div[2]/div/label")
rooms = [room.text for room in room_labels]

selected_room = rooms[0]
print("WARNING: this will overwrite your current room configuration. Press ctrl + c at any time to cancel and exit\n")
sleep(3)

room_data = []
while True:
    room = {}
    while True:
        print("Available Rooms:")
        for index, room_label in enumerate(rooms, 1):
            print(f"{index}. {room_label}")

        choice = input(
            "\nSelect a room (enter the number) or type \"exit\" to quit:\n")

        if choice.lower() == "exit":
            quit()
        try:
            choice = int(choice)
            if 1 <= choice <= len(room_labels):
                selected_room = rooms[choice - 1]  # Adjust for 0-based index
                room["room_number_xpath"] = f'"/html/body/form/div[2]/div//label[text()=\'{selected_room}\']"'
                break
            else:
                print("Invalid selection. Please choose a valid room number.")
        except ValueError:
            print("Invalid input. Please enter a valid room number or \"exit\".")

    available_hours = [str(i) for i in range(1, 13)]  # [1, 2, 3, ..., 12]
    available_minutes = [f"{i:02d}" for i in range(
        0, 60, 10)]  # [00, 10, 20, ..., 50]
    while True:
        print("\nAvailable Hours:")
        for index, hour_option in enumerate(available_hours, 1):
            print(f"{index}. {hour_option}")

        hour_choice = input("\nSelect an hour (enter the number): ")

        if hour_choice.isdigit() and 1 <= int(hour_choice) <= len(available_hours):
            selected_hour = available_hours[int(hour_choice) - 1]
            break
        else:
            print("Invalid selection. Please choose a valid hour.")

    while True:
        print("\nAvailable Minutes:")
        for index, minute_option in enumerate(available_minutes, 1):
            print(f"{index}. {minute_option}")

        minute_choice = input("\nSelect a minute (enter the number): ")

        if minute_choice.isdigit() and 1 <= int(minute_choice) <= len(available_minutes):
            selected_minute = available_minutes[int(minute_choice) - 1]
            break
        else:
            print("Invalid selection. Please choose a valid minute.")

    room["hour"] = '\"' + selected_hour + '\"'
    room["min"] = '\"' + selected_minute + '\"'
    room["am_pm"] = int(input("Enter 0 for AM or 1 for PM: "))
    print(
        f"ADDED: {selected_room} at {selected_hour}:{selected_minute} {'PM' if room['am_pm'] else 'AM'}")

    room.update(generate_xpaths(len(room_data) + 1))
    room_data.append(room)

    if len(rooms) == 5:
        break

    another_room = input("Do you want to add another room (yes/no)? ").lower()
    if "y" not in another_room:
        break
    rooms.remove(selected_room)

class Room:
    def __init__(self, room_number_xpath, hour, min, am_pm, hour_xpath, min_xpath, pm_xpath):
        self.room_number_xpath = room_number_xpath
        self.hour = hour
        self.min = min
        self.am_pm = am_pm
        self.hour_xpath = hour_xpath
        self.min_xpath = min_xpath
        self.pm_xpath = pm_xpath

rooms = [Room(**data) for data in room_data]

with open("room_config.py", "w") as file:
    file.write('class Room:\n')
    file.write(
        '    def __init__(self, room_number_xpath, hour, min, am_pm, hour_xpath, min_xpath, pm_xpath):\n')
    file.write('        self.room_number_xpath = room_number_xpath\n')
    file.write('        self.hour = hour\n')
    file.write('        self.min = min\n')
    file.write('        self.am_pm = am_pm\n')
    file.write('        self.hour_xpath = hour_xpath\n')
    file.write('        self.min_xpath = min_xpath\n')
    file.write('        self.pm_xpath = pm_xpath\n\n')
    file.write('room_data = [\n')

    for room in rooms:
        file.write('    {\n')
        file.write(f'        "room_number_xpath": {room.room_number_xpath},\n')
        file.write(f'        "hour": {room.hour},\n')
        file.write(f'        "min": {room.min},\n')
        file.write(f'        "am_pm": {room.am_pm},\n')
        file.write(f'        "hour_xpath": {room.hour_xpath},\n')
        file.write(f'        "min_xpath": {room.min_xpath},\n')
        file.write(f'        "pm_xpath": {room.pm_xpath},\n')
        file.write('    },\n')
    file.write(']\n\n')
    file.write('rooms = [Room(**data) for data in room_data] # unpack\n')

print("room_config.py file generated successfully.")
