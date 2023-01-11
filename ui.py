import tkinter as tk
import tkinter.font as tkf
import config as cfg
from main import resources

resizing = False


def toggle_fullscreen(event=None):
    global main_root
    main_root.state = not main_root.state
    main_root.attributes("-fullscreen", main_root.state)
    return "break"


def init_root():
    global main_root
    main_root = tk.Tk()
    main_root.title("BARBS.EXE")
    main_root.attributes("-fullscreen", True)
    main_root.configure(bg=cfg.root_colour)
    main_root.bind("<F11>", lambda e: toggle_fullscreen(main_root))
    root_frame = tk.Frame(bg=cfg.root_colour)
    root_frame.pack(
        fill="both",
        expand=True,
        padx=cfg.root_pad_x,
        pady=cfg.root_pad_y)

    return root_frame


def init_title(root_frame):

    title_frame = tk.Frame(
        master=root_frame,
        bg=cfg.root_colour)
    title_frame.pack(
        fill="both",
        expand=True,
        padx=cfg.title_pad_x,
        pady=cfg.title_pad_y)

    title = tk.Label(
        master=title_frame,
        bg=cfg.main_title_colour,
        fg=cfg.main_title_text_colour,
        font=fonts["main_title"],
        text=cfg.institute_name + " Room Booking",
        anchor="center")

    title.pack(fill="both", expand=True)

    return title


def init_table(root_frame, resource_names, timeslots):

    print("Initialising table...")
    padding_frame = tk.Frame(
        master=root_frame,
        bg=cfg.table_frame_colour)
    padding_frame.pack(
        fill="both",
        expand=True)

    table_frame = tk.Frame(
        master=padding_frame,
        bg=cfg.table_frame_colour)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=cfg.table_pad_x,
        pady=cfg.table_pad_y)
    table_frame.rowconfigure(0, weight=0)
    table_frame.columnconfigure(0, weight=0)

    def init_timeslots():

        print("Initialising timeslots...")
        frame = tk.Frame(
            master=table_frame,
            bg=cfg.table_frame_colour)
        frame.grid(
            column=0,
            row=0,
            sticky="nesw")

        tk.Label(
            master=frame,
            bg=cfg.cell_title_colour,
            fg=cfg.cell_title_text_colour,
            font=fonts["cell_title"],
            text="Time Slot",
            anchor="center"
        ).pack(
            fill="both",
            expand=True,
            padx=cfg.cell_pad_x,
            pady=cfg.cell_pad_y)

        timeslot_coords = {}
        count = 1

        for timeslot in timeslots:

            frame = tk.Frame(
                master=table_frame,
                bg=cfg.table_frame_colour)
            frame.grid(
                column=0,
                row=count,
                sticky="nesw")

            tk.Label(
                master=frame,
                bg=cfg.cell_title_colour,
                fg=cfg.cell_title_text_colour,
                font=fonts["cell_title"],
                text=timeslot,
                anchor="center"
            ).pack(
                fill="both",
                expand=True,
                padx=cfg.cell_pad_x,
                pady=cfg.cell_pad_y)

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

            frame = tk.Frame(
                master=table_frame,
                bg=cfg.table_frame_colour)
            frame.grid(
                column=count,
                row=0,
                sticky="nesw")

            tk.Label(
                master=frame,
                text=resource,
                bg=cfg.cell_title_colour,
                fg=cfg.cell_title_text_colour,
                font=fonts["cell_title"],
                anchor="center"
            ).pack(
                fill="both",
                expand=True,
                padx=cfg.cell_pad_x,
                pady=cfg.cell_pad_y)

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

            frame = tk.Frame(
                master=table_frame,
                bg=cfg.table_frame_colour)
            frame.grid(column=column, row=row, sticky="nesw")

            if resource.bookings[timeslot] == "None":

                booking = tk.Label(
                    master=frame,
                    text="None",
                    fg=cfg.cell_text_colour,
                    font=fonts["cell"],
                    anchor="center")
                booking.pack(
                    fill="both",
                    expand=True,
                    padx=cfg.cell_pad_x,
                    pady=cfg.cell_pad_y)

            else:

                cell_contents = "\n".join([
                    (
                        booking
                        + ": "
                        + resource.bookings[timeslot][booking]
                    )
                    for booking in resource.bookings[timeslot]
                ])

                booking = tk.Label(
                    master=frame,
                    text=cell_contents,
                    fg=cfg.cell_text_colour,
                    font=fonts["cell"],
                    anchor="center")
                booking.pack(
                    fill="both",
                    expand=True,
                    padx=cfg.cell_pad_x,
                    pady=cfg.cell_pad_y)

            if row == 2 or row == 4 or row == 6:
                booking.configure(bg=cfg.cell_colour2)
            else:
                booking.configure(bg=cfg.cell_colour1)

    print("Finished initialising bookings.")


def main():

    print("Starting intialisation...")
    global fonts

    resource_names = [resource for resource in resources]

    root_frame = init_root()

    fonts = cfg.init_fonts()

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

    print("Finished initialisation.")

    main_root.mainloop()


if __name__ == "__main__":
    main()
