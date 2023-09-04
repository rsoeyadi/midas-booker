# Practice Room Booking Automation

This Python script project automates the process of booking practice rooms at the New England Conservatory. The script runs on a schedule specified by the user, ensuring that you can book a room as soon as it becomes available.

## Features

- Books practice rooms at the New England Conservatory.
- Allows scheduling room bookings up to 4 days in advance.
- Runs on a specified schedule using military time (HH:MM).
- Generates and maintains room configuration data.
- Utilizes Selenium for web automation.

## Prerequisites

Before using this script, ensure you have the following:

- Python 3.x installed on your system.
- Selenium library installed (`pip install selenium`).
- Pytz library installed (`pip install pytz`).
- Chrome WebDriver installed and configured. [Download here](https://chromedriver.chromium.org/downloads).
- `config.py` and `room_config.py` files set up with your preferences.
- Name, NEC email address, and the link to the reservation system

## Getting Started

1. Clone this repository to your local machine:

   ```shell
   git clone <repository-url>
   cd <repository-directory>
