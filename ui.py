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
        padx=cfg.root_pad,
        pady=cfg.root_pad)

    return root_frame


def init_title(root_frame):

    title_frame = tk.Frame(
        master=root_frame,
        bg=cfg.table_frame_colour)
    title_frame.pack(
        fill="both",
        expand=True,
        pady=(0, cfg.root_pad))

    title = tk.Label(
        master=title_frame,
        bg=cfg.main_title_colour,
        fg=cfg.main_title_text_colour,
        font=fonts["main_title"],
        text=cfg.institute_name + " Room Booking",
        anchor="center")

    title.pack(
        fill="both",
        expand=True,
        padx=cfg.title_pad,
        pady=cfg.title_pad)

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
        padx=cfg.frame_pad,
        pady=cfg.frame_pad)
    table_frame.rowconfigure(0, weight=cfg.cell_title_weight)
    table_frame.columnconfigure(0, weight=cfg.cell_title_weight)

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
            text="",
            anchor="center"
        ).pack(
            fill="both",
            expand=True)

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
                expand=True)

            table_frame.rowconfigure(count, weight=cfg.cell_weight)

            timeslot_coords[timeslot] = count

            count += 1

        print("Finished initialising timeslots.")

        return timeslot_coords

    def init_resource_tables():

        print("Initialising resources...")

        resource_coords = {}
        count = 1

        for resource in resource_names:

            table_frame.columnconfigure(count, weight=cfg.cell_weight)

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
                expand=True)

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
                    fg=cfg.empty_text_colour,
                    font=fonts["cell"],
                    anchor="center")
                booking.pack(
                    fill="both",
                    expand=True)

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
                    fg=cfg.booking_text_colour,
                    font=fonts["cell"],
                    anchor="center")
                booking.pack(
                    fill="both",
                    expand=True)

            """ Make every 2nd row a different colour """
            if row % 2 == 0:
                booking.configure(bg=cfg.cell_colour2)
            else:
                booking.configure(bg=cfg.cell_colour1)

    print("Finished initialising bookings.")


def add_table_gridlines(table_frame, timeslot_coords, resource_coords):
    if cfg.cell_spacing_vertical < 1 and cfg.cell_spacing_horizontal < 1:
        pass
    else:
        last_row = len(list(timeslot_coords.values()))
        last_column = len(list(resource_coords.values()))

        """ Get all cells (including title cells) in the table """
        cell_list = table_frame.winfo_children()

        for cell in cell_list:
            info = cell.grid_info()
            row = info["row"]
            column = info["column"]

            if row % 2 == 1:
                if row == last_row:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=(cfg.cell_spacing_vertical, 0))
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=cfg.cell_spacing_vertical)

            if column % 2 == 1:
                if column == last_column:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=(cfg.cell_spacing_horizontal, 0))
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=cfg.cell_spacing_horizontal)


def main():

    print("Starting intialisation...")
    global fonts

    resource_names = [resource for resource in resources]

    root_frame = init_root()

    fonts = cfg.init_fonts()

    init_title(root_frame)

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

    add_table_gridlines(table_frame, timeslot_coords, resource_coords)

    print("Finished initialisation.")

    main_root.mainloop()


if __name__ == "__main__":
    main()
