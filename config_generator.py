name = input("Enter your name: ")
email = input("Enter your email: ")
link = input("Enter the link: ")

with open("config.py", "w") as config_file:
    config_file.write(f"name = '{name}'\n")
    config_file.write(f"email = '{email}'\n")
    config_file.write(f"link = '{link}'\n")

print("Configuration file (config.py) has been generated.")