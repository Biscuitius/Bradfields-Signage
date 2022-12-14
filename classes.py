import requests
import re
from bs4 import BeautifulSoup


class Resource:

    def __init__(self, name):
        self.name = name
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

    def __init__(self, name, urlcode):
        self.name = name
        self.url = (
            "https://bradfields.roombookingsystem.co.uk/digitalsignage?code="
            + urlcode
        )

    def update(self):

        soup = BeautifulSoup(requests.get(self.url).text, "html.parser")

        div_list = soup.find_all(class_="timetableCell")

        current_resource = ""

        for item in div_list:

            search = re.findall(r"'.+?'", str(item))

            timeslot = search[5].replace("'", "")
            resource = search[10].replace("'", "")

            if resource != current_resource:
                current_resource = resource
                print("\n" + resource)

            print("   " + timeslot)

            bookings = {}

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

                    bookings[user] = quantity

            if len(bookings) == 0:

                print("      No bookings")

            else:

                for booking in bookings:

                    print(
                        "      "
                        + booking
                        + ": "
                        + bookings[booking]
                    )
