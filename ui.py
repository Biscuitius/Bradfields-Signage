import themes
import tkinter as tk
import tkinter.font as tkf
import config
import time
from main import resources

resizing = False


def toggle_fullscreen(event=None):
    global main_root
    main_root.state = not main_root.state
    main_root.attributes("-fullscreen", main_root.state)
    return "break"


def adjust_font(font, min_height, max_height, text_height, step_size):

    old_size = font.cget("size")

    if text_height < min_height:
        print("Font too small, expanding...")
        new_size = old_size + step_size
    else:
        print("Font too big, shrinking...")
        new_size = old_size - step_size

    font.config(size=new_size)
    text_height = font.metrics("linespace")
    print("Changing font size to " + str(new_size))

    if text_height > min_height and text_height < max_height:
        print("Perfect size found")
        return True
    else:
        print("Perfect size not found, trying again...")
        return False


def autofit(label):

    print("Checking if text needs fitting...")

    global resizing
    resizing = True

    font = label.cget("font")
    font = fonts("font")

    label_frame = main_root.nametowidget(label.winfo_parent())

    label_height = label_frame.winfo_height()
    min_height = int((label_height / 100) * 85)
    max_height = int((label_height / 100) * 95)
    text_height = font.metrics("linespace")

    if text_height < min_height or text_height > max_height:

        print("Font needs to be fitted:")
        print("    Label Height: " + str(label_height))
        print("    Text Height: " + str(text_height))
        print("    Min Height: " + str(min_height))
        print("    Max Height: " + str(max_height))

        sweet_spot_found = False
        step_size = 1
        start_time = time.time()

        print("Beginning resize...")

        while not sweet_spot_found:

            sweet_spot_found = adjust_font(
                font,
                min_height,
                max_height,
                text_height,
                step_size
            )

        execution_time = time.time() - start_time

        print("Resizing finished, took " + str(execution_time))
    else:
        print("Text doesn't need refitting.")

    resizing = False


def init_root():
    global main_root
    main_root = tk.Tk()
    main_root.title("BARBS.EXE")
    main_root.attributes("-fullscreen", True)
    main_root.configure(bg=themes.root_colour)
    main_root.bind("<F11>", lambda e: toggle_fullscreen(main_root))
    root_frame = tk.Frame()
    root_frame.pack(fill="both", expand=True, padx=8, pady=8)

    return root_frame


def init_title(root_frame):

    title_frame = tk.Frame(master=root_frame)
    title_frame.pack_propagate(0)
    title_frame.pack(fill="both", expand=True)

    title = tk.Label(
        master=title_frame,
        bg=themes.main_title_colour,
        font=fonts["main_title"],
        text=config.institute_name + " Room Booking",
        anchor="center")

    title.pack(fill="both", expand=True)

    return title


def init_table(root_frame, resource_names, timeslots):

    print("Initialising table...")

    table_frame = tk.Frame(root_frame)
    table_frame.pack(fill="both", expand=True)
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    def init_timeslots():

        print("Initialising timeslots...")
        frame = tk.Frame(master=table_frame)

        frame.grid(
            column=0,
            row=0,
            sticky="nesw")

        tk.Label(
            master=frame,
            bg=themes.cell_title_colour,
            font=fonts["cell_title"],
            text="Time Slot",
            anchor="center"
        ).pack(fill="both", expand=True)

        timeslot_coords = {}
        count = 1

        for timeslot in timeslots:

            frame = tk.Frame(master=table_frame)

            frame.grid(
                column=0,
                row=count,
                sticky="nesw")

            tk.Label(
                master=frame,
                bg=themes.cell_title_colour,
                font=fonts["cell_title"],
                text=timeslot,
                anchor="center"
            ).pack(fill="both", expand=True)

            table_frame.rowconfigure(count, weight=1)

            timeslot_coords[timeslot] = count

            count += 1

        print("Finished initialising timeslots.")

        return timeslot_coords

    def init_resource_tables():

        print("Initialising resources...")

        resource_coords = {}
        count = 1

        for resource in resource_names:

            table_frame.columnconfigure(count, weight=1)

            frame = tk.Frame(master=table_frame)

            frame.grid(
                column=count,
                row=0,
                sticky="nesw")

            tk.Label(
                master=frame,
                text=resource,
                bg=themes.cell_colour,
                font=fonts["cell"],
                anchor="center"
            ).pack(fill="both", expand=True)

            resource_coords[resource] = count

            count += 1

        print("Finished initialising resources.")

        return resource_coords

    timeslot_coords = init_timeslots()
    resource_coords = init_resource_tables()

    print("Finished initialising table.")

    return table_frame, timeslot_coords, resource_coords


def init_bookings(table_frame, resources, timeslot_coords, resource_coords):

    print("Initialising bookings...")

    for resource in resources.values():

        for timeslot in resource.bookings:

            column = resource_coords[resource.name]
            row = timeslot_coords[timeslot]

            frame = tk.Frame(master=table_frame)
            frame.grid(column=column, row=row, sticky="nesw")

            if resource.bookings[timeslot] == "None":

                tk.Label(
                    master=frame,
                    text="None",
                    bg=themes.cell_colour,
                    font=fonts["cell"],
                    anchor="center"
                ).pack(fill="both", expand=True)

            else:

                cell_contents = "\n".join([
                    (
                        booking
                        + ": "
                        + resource.bookings[timeslot][booking]
                    )
                    for booking in resource.bookings[timeslot]
                ])

                tk.Label(
                    master=frame,
                    text=cell_contents,
                    bg=themes.cell_colour,
                    font=fonts["cell"],
                    anchor="center"
                ).pack(fill="both", expand=True)

    print("Finished initialising bookings.")


def find_frames_in_frame(frame):

    frames = []

    for widget in frame.winfo_children():
        if (
            type(widget) == "tkinter.tk.Frame"
        ) or (
            type(widget) == "tkinter.tk.Frame"
        ):
            frames.append(widget)

    return frames


def find_widgets_recursive(parent):

    unsearched_frames = [parent]
    widgets = {
        "frame": [],
        "label": []
    }

    while len(unsearched_frames) != 0:

        frame = unsearched_frames[0]
        unsearched_frames.pop(0)

        children = frame.winfo_children()

        for widget in children:

            if (
                isinstance(widget, tk.Frame)
            ) or (
                isinstance(widget, tk.Frame)
            ):
                widgets["frame"].append(widget)
                unsearched_frames.append(widget)

            elif (
                isinstance(widget, tk.Label)
            ) or (
                isinstance(widget, tk.Label)
            ):
                widgets["label"].append(widget)

    return widgets


def init_resizing(main_root, title):

    print("Initialising automatic font resizing...")

    widgets = find_widgets_recursive(main_root)

    label_list = widgets["label"]

    for label in label_list:

        if label == title:

            label.bind(
                "<Configure>",
                lambda e: None if resizing else autofit(
                    label)
            )

    print("Finished initialising automatic font resizing.")


def main():

    print("Starting intialisation...")
    global fonts

    resource_names = [resource for resource in resources]

    root_frame = init_root()

    fonts = themes.init_fonts()

    title = init_title(root_frame)

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

    main_root.update()

    init_resizing(main_root, title)

    main_root.update()

    print("Finished initialisation.")

    main_root.mainloop()


if __name__ == "__main__":
    main()
