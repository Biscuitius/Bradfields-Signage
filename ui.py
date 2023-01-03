import themes
import tkinter as tk
import config
import time
from tkinter import ttk
from main import resources


def toggle_fullscreen(event=None):
    global main_root
    main_root.state = not main_root.state
    main_root.attributes("-fullscreen", main_root.state)
    return "break"


def get_font_tuple(style):
    "Takes a tkinter Style object and returns the font in a tuple"

    font = theme.lookup(style, "font")

    font_family = font[1:].split("}", 1)[0]
    font_size = int((font.split("} ", 1)[1]).split(" ", 1)[0])
    font_weight = (font.split("} ", 1)[1]).split(" ", 1)[1]

    return (font_family, font_size, font_weight)


def auto_resize_text(theme, widget_list):

    global resizing
    resizing = True

    print("resizing")

    main_root.update()

    widget_list.pop(0)  # Remove Title label (handled seperately)

    parent_width = root_frame.winfo_width()
    min_width = int((parent_width / 100) * 90)
    max_width = int((parent_width / 100) * 95)
    child_width = title.winfo_reqwidth()

    print("Parent Width: " + str(parent_width))
    print("Child Width: " + str(child_width))
    print("Min Width: " + str(min_width))
    print("Max Width: " + str(max_width))

    if child_width == 0:
        pass

    elif child_width < min_width or child_width > max_width:

        style = title.cget("style")
        font = get_font_tuple(style)
        font_family = font[0]
        font_size = font[1]
        font_weight = font[2]

        while child_width < max_width:

            font_size += 4
            theme.configure(style, font=(font_family, font_size, font_weight))
            root_frame.update()
            child_width = title.winfo_width()
            print(child_width)

            print(f"Increasing font size to {str(font_size)}...")
            time.sleep(0.5)

        while child_width > max_width:

            font_size -= 4
            theme.configure(style, font=(font_family, font_size, font_weight))
            root_frame.update()
            child_width = title.winfo_width()
            print(child_width)

            print(f"Decreasing font size to {str(font_size)}...")
            time.sleep(0.5)

    resizing = False


def init_root():
    global main_root
    main_root = tk.Tk()
    main_root.title("BARBS.EXE")
    main_root.attributes("-fullscreen", True)
    main_root.configure(background="purple")
    main_root.bind("<F11>", lambda e: toggle_fullscreen(main_root))
    root_frame = ttk.Frame(style="Root.TFrame")
    root_frame.pack(fill="both", expand=True, padx=8, pady=8)

    return root_frame


def init_title(master, theme):

    title = ttk.Label(
        master=master,
        style="MainTitle.TLabel",
        text=config.institute_name + " Room Booking",
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
                    anchor="center"
                ).grid(
                    column=resource_coords[resource.name],
                    row=timeslot_coords[timeslot],
                    sticky="nesw"
                )


resource_names = [resource for resource in resources]

resizing = False
main_root = 0
text_widgets = {}
root = init_root()
root_frame = root
theme = themes.init_theme()
title = init_title(root_frame, theme)
timeslot_coords = init_timeslots(root_frame)
resource_coords = init_resource_tables(root_frame, resource_names, title)
init_bookings(root_frame, resources, timeslot_coords, resource_coords)

main_root.bind('<Configure>', lambda e: None if resizing else auto_resize_text(
    theme, root_frame.winfo_children()))

main_root.mainloop()
