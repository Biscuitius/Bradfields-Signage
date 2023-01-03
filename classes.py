import requests
import re
from bs4 import BeautifulSoup


class Resource:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.bookings = {
            "AM": {},
            "Period 1": {},
            "Period 2": {},
            "Period 3": {},
            "Lunch": {},
            "Period 4": {},
            "Period 5": {}
        }


class Category:

    def __init__(self, urlcode):
        self.url = (
            "https://bradfields.roombookingsystem.co.uk/digitalsignage?code="
            + urlcode
        )

    def update(self):

        self.resources = []
        resources = {}

        soup = BeautifulSoup(requests.get(self.url).text, "html.parser")

        search = soup.find(class_="greydark largest")
        search = re.search(r"<b>.+?</b>", str(search), flags=re.DOTALL)
        search = str(search.group())
        search = search[3:-4]
        self.name = search.replace("&amp;", "&")

        div_list = soup.find_all(class_="timetableCell")

        if len(div_list) == 0:
            error_list = soup.find_all("h2")
            print(error_list)
            error_occurred = True
        else:
            error_occurred = False

        current_resource = ""

        for item in div_list:

            search = re.findall(r"'.+?'", str(item))

            timeslot = search[5].replace("'", "")

            valid_timeslots = [
                "AM",
                "Period 1",
                "Period 2",
                "Period 3",
                "Lunch",
                "Period 4",
                "Period 5"
            ]

            if timeslot not in valid_timeslots:
                raise InvalidTimeSlot(self.name)

            resource = search[10].replace("'", "")

            if resource != current_resource:
                current_resource = resource
                resources[resource] = Resource(resource, self)

            search = re.search(r'title=".+?"', str(item), flags=re.DOTALL)

            if search:

                search = str(search.group())
                search = re.split("\n+", search)

                for booking in search:

                    booking = booking.replace(" ", "")
                    booking = booking.replace("\"", "")
                    booking = booking.replace("bookedby", "")
                    booking = booking.replace("title=", "")

                    quantity = ''.join(
                        [char for char in booking if char.isdigit()]
                    )

                    user = ''.join(
                        [char for char in booking if not char.isdigit()]
                    )

                    user = user.replace("\xa0", " ")
                    user = user.replace("\r", "")

                    resources[resource].bookings[timeslot][user] = quantity

            if not resources[resource].bookings[timeslot]:
                resources[resource].bookings[timeslot] = "None"

        self.resources = resources

        if error_occurred:
            raise SignageError(str(error_list[0])[4:-5])
        else:
            return resources


class InvalidTimeSlot(Exception):
    def __init__(self, category):

        self.message = f"""
BARBS only works with Period-based timeslots (i.e. AM, Period X, Lunch)
The category "{category}" doesn't use these.\n
"""

        super().__init__(self.message)


class SignageError(Exception):
    def __init__(self, message):

        self.message = f"""
The Room Booking Digital Signage link provided no valid information.
The following error message was provided by the site:\n
"{message}"\n
"""

        super().__init__(self.message)
