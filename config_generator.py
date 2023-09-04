import os

name = input("Enter your name: ")
email = input("Enter your email: ")
link = input("Enter the link: ")

file_exists = os.path.isfile("config.py")

with open("config.py", "a") as config_file:
    if not file_exists:
        config_file.write("# This is a new configuration file\n")
    config_file.write(f"name = '{name}'\n")
    config_file.write(f"email = '{email}'\n")
    config_file.write(f"link = '{link}'\n")

if not file_exists:
    print("Configuration file (config.py) has been created.")
else:
    print("Configuration file (config.py) has been updated.")

