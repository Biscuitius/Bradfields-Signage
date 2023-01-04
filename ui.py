import themes
import tkinter as tk
import tkinter.font as tkf
import config
import time
from tkinter import ttk
from main import resources


def toggle_fullscreen(event=None):
    global main_root
    main_root.state = not main_root.state
    main_root.attributes("-fullscreen", main_root.state)
    return "break"


def expand_font(fonts, font, font_size, min_height, max_height, text_height, step_size):
    """
    Increase font size until the text is bigger than the label
    """
    while text_height < max_height:
        font_size += step_size
        fonts[font].config(size=font_size)
        text_height = fonts["main_title_font"].metrics("linespace")
        print(f"Increasing font size to {str(font_size)}...")

    """
    The loop above stops when the text steps over the max size,
    this bit pushes it one step back
    """
    fonts[font].config(size=(font_size-step_size))
    text_height = fonts["main_title_font"].metrics("linespace")

    if text_height < min_height and text_height > max_height:
        return False
    else:
        return True


def shrink_font(fonts, font, font_size, min_height, max_height, text_height, step_size):
    """
    Decrease font size until the text is smaller than the label
    """
    while text_height > max_height:
        font_size -= step_size
        fonts[font].config(size=font_size)
        text_height = fonts["main_title_font"].metrics("linespace")
        print(f"Decreasing font size to {str(font_size)}...")

    if text_height < min_height and text_height > max_height:
        return False
    else:
        return True


def auto_resize(main_root, title_frame, table_frame, fonts):

    global resizing
    resizing = True

    title = title_frame.winfo_children()[0]

    main_root.update()

    root_height = main_root.winfo_reqheight()

    def resize_title():

        title_frame_height = int(root_height / 7)

        title_frame.configure(height=title_frame_height)

        main_root.update()

        min_height = int((title_frame_height / 100) * 70)
        max_height = int((title_frame_height / 100) * 95)
        text_height = fonts["main_title_font"].metrics("linespace")

        print("Frame Height: " + str(title_frame_height))
        print("Text Height: " + str(text_height))
        print("Min Height: " + str(min_height))
        print("Max Height: " + str(max_height))

        if text_height < min_height or text_height > max_height:

            """ Get current font settings """
            font = title.cget("font")
            font_size = fonts[font].cget("size")

            sweet_spot_found = False
            step_size = 5
            start_time = time.time()

            while not sweet_spot_found:

                if text_height < min_height:
                    sweet_spot_found = expand_font(
                        fonts,
                        font,
                        font_size,
                        min_height,
                        max_height,
                        text_height,
                        step_size
                    )

                if text_height > max_height:
                    sweet_spot_found = shrink_font(
                        fonts,
                        font,
                        font_size,
                        min_height,
                        max_height,
                        text_height,
                        step_size
                    )

                step_size -= 1

            execution_time = time.time() - start_time

            print(execution_time)

    resize_title()

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


def init_title(root_frame, fonts):

    title_frame = tk.Frame(master=root_frame)

    title_frame.grid(column=0, row=0, sticky="new")

    title = tk.Label(
        master=title_frame,
        font=fonts["main_title_font"],
        text=config.institute_name + " Room Booking",
        anchor="center")

    title.pack(fill="both")

    root_frame.rowconfigure(0, weight=1)

    return title_frame


def init_table(root_frame, resource_names, timeslots):

    table_frame = tk.Frame(root_frame)
    table_frame.grid(column=0, row=1, sticky="nesw")

    def init_timeslots():

        ttk.Label(
            master=table_frame,
            style="TableTitle.TLabel",
            text="Time Slot",
            anchor="center"
        ).grid(
            column=0,
            row=0,
            sticky="nesw")

        table_frame.rowconfigure(1, weight=1)

        timeslot_coords = {}
        count = 1

        for timeslot in timeslots:

            ttk.Label(
                master=table_frame,
                style="TableCell.TLabel",
                text=timeslot,
                anchor="center"
            ).grid(
                column=0,
                row=count,
                sticky="nesw")

            table_frame.rowconfigure(count, weight=1)

            timeslot_coords[timeslot] = count

            count += 1

        table_frame.columnconfigure(0, weight=1)

        return timeslot_coords

    def init_resource_tables():

        resource_coords = {}
        count = 0

        for resource in resource_names:

            ttk.Label(
                master=table_frame,
                text=resource,
                style="TableTitle.TLabel",
                anchor="center"
            ).grid(
                column=count,
                row=1,
                sticky="nesw")

            table_frame.columnconfigure(count, weight=1)

            resource_coords[resource] = count

            count += 1

        return resource_coords

    timeslot_coords = init_timeslots()
    resource_coords = init_resource_tables()

    return table_frame, timeslot_coords, resource_coords


def init_bookings(table_frame, resources, timeslot_coords, resource_coords):

    for resource in resources.values():
        for timeslot in resource.bookings:

            if resource.bookings[timeslot] == "None":

                ttk.Label(
                    master=table_frame,
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
                    master=table_frame,
                    text=cell_contents,
                    style="TableCell.TLabel",
                    anchor="center"
                ).grid(
                    column=resource_coords[resource.name],
                    row=timeslot_coords[timeslot],
                    sticky="nesw"
                )


def main():

    resource_names = [resource for resource in resources]

    resizing = False
    root_frame = init_root()

    fonts = themes.init_fonts(root_frame)
    theme = themes.init_theme(fonts)

    title_frame = init_title(root_frame, fonts)

    timeslots = [
        "AM",
        "Period 1",
        "Period 2",
        "Period 3",
        "Lunch",
        "Period 4",
        "Period 5"]

    table = init_table(root_frame, resource_names, timeslots)
    table_frame = table[0]
    timeslot_coords = table[1]
    resource_coords = table[2]

    init_bookings(table_frame, resources, timeslot_coords, resource_coords)

    main_root.bind('<Configure>', lambda e: None if resizing else auto_resize(
        main_root,
        title_frame,
        table_frame,
        fonts
    ))

    main_root.mainloop()


if __name__ == "__main__":
    main()
