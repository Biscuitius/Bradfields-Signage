import themes
import tkinter as tk
from tkinter import ttk
from main import resources


def toggle_fullscreen(main_root, event=None):
    main_root.state = not main_root.state
    main_root.attributes("-fullscreen", main_root.state)
    return "break"


def init_root():
    main_root = tk.Tk()
    main_root.title("BARBS.EXE")
    main_root.attributes("-fullscreen", True)
    main_root.configure(background="purple")
    main_root.bind("<F11>", lambda e: toggle_fullscreen(main_root))

    root_frame = ttk.Frame(style="Root.TFrame")
    root_frame.pack(fill="both", expand=True, padx=8, pady=8)

    return main_root, root_frame


def init_title(master):

    title = ttk.Label(
        master=master,
        style="MainTitle.TLabel",
        text="Bradfields Room Booking",
        anchor="center")

    title.grid(column=0, row=0, sticky="nesw", pady=(0, 8))

    master.rowconfigure(0, weight=1)

    return title


def init_timeslots(master):

    ttk.Label(
        master=master,
        style="TableTitle.TLabel",
        text="Time Slot",
        anchor="center"
    ).grid(
        column=0,
        row=1,
        sticky="nesw")

    master.rowconfigure(1, weight=1)

    timeslots = [
        "AM",
        "Period 1",
        "Period 2",
        "Period 3",
        "Lunch",
        "Period 4",
        "Period 5"]

    timeslot_coords = {}
    count = 2

    for timeslot in timeslots:

        ttk.Label(
            master=master,
            style="TableCell.TLabel",
            text=timeslot,
            anchor="center"
        ).grid(
            column=0,
            row=count,
            sticky="nesw")

        master.rowconfigure(count, weight=1)

        timeslot_coords[timeslot] = count

        count += 1

    master.columnconfigure(0, weight=1)

    return timeslot_coords


def init_resource_tables(master, resource_names, title):

    resource_coords = {}
    count = 1

    for resource in resource_names:

        ttk.Label(
            master=master,
            text=resource,
            style="TableTitle.TLabel",
            anchor="center"
        ).grid(
            column=count,
            row=1,
            sticky="nesw")

        master.columnconfigure(count, weight=1)
        title.grid(column=0, row=0, columnspan=count+1)

        resource_coords[resource] = count

        count += 1

    return resource_coords


def init_bookings(master, resources, timeslot_coords, resource_coords):

    for resource in resources.values():
        for timeslot in resource.bookings:

            if resource.bookings[timeslot] == "None":

                ttk.Label(
                    master=master,
                    text="None",
                    style="TableCell.TLabel",
                    anchor="center"
                ).grid(
                    column=resource_coords[resource.name],
                    row=timeslot_coords[timeslot],
                    sticky="nesw"
                )

            else:

                cell_contents = "\n".join([
                    (
                        booking
                        + ": "
                        + resource.bookings[timeslot][booking]
                    )
                    for booking in resource.bookings[timeslot]
                ])

                ttk.Label(
                    master=master,
                    text=cell_contents,
                    style="TableCell.TLabel",
                    anchor="w"
                ).grid(
                    column=resource_coords[resource.name],
                    row=timeslot_coords[timeslot],
                    sticky="nesw"
                )


resource_names = [resource for resource in resources]

roots = init_root()
main_root = roots[0]
root_frame = roots[1]
theme = themes.init_theme()
title = init_title(root_frame)
timeslot_coords = init_timeslots(root_frame)
resource_coords = init_resource_tables(root_frame, resource_names, title)
init_bookings(root_frame, resources, timeslot_coords, resource_coords)

main_root.mainloop()
