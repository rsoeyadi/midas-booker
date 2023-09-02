def input_valid_time(prompt):
    while True:
        print("Enter the time in military format (HH:MM):")
        time_str = input(prompt)
        try:
            hour, minute = map(int, time_str.split(":"))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return hour, minute
            else:
                print("Invalid military time format. Please enter a valid time (HH:MM).")
        except ValueError:
            print("Invalid military time format. Please enter a valid time (HH:MM).")

hour, minute = input_valid_time("When do you need this to run? ")
with open("config.py", "r") as config_file:
    lines = config_file.readlines()

hour_line_present = any("hour =" in line for line in lines)
minute_line_present = any("minute =" in line for line in lines)

if hour_line_present and minute_line_present:
    for i in range(len(lines)):
        if "hour =" in lines[i]:
            lines[i] = f"hour = {hour}\n"
        elif "minute =" in lines[i]:
            lines[i] = f"minute = {minute}\n"

if not hour_line_present:
    lines.append(f"hour = {hour}\n")
if not minute_line_present:
    lines.append(f"minute = {minute}\n")

with open("config.py", "w") as config_file:
    config_file.writelines(lines)