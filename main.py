from classes import Category
from config import url_codes

categories = []
resources = {}


def startup():
    for code in url_codes:
        categories.append(Category(code))
    update()


def update():
    for category in categories:
        resources.update(category.update())


# def print_bookings():

#     for resource in resources.values():
#         print("   ", end="")
#         print(resource.name)

#         for timeslot in resource.bookings:
#             print("\n      ", end="")
#             print(timeslot)

#             if resource.bookings[timeslot] == "None":
#                 print("         None")
#             else:
#                 for booking in resource.bookings[timeslot]:
#                     print("         ", end="")
#                     print(
#                         booking
#                         + ": "
#                         + resource.bookings[timeslot][booking]
#                     )
#         print("\n--------------------------------\n")


startup()
# print_bookings()
