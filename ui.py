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
        padx=cfg.frame_pad,
        pady=cfg.frame_pad)

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
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

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

    # Get resource
    for resource in resources.values():

        # Get timeslot
        for timeslot in resource.bookings:

            # Get the coordinates of this resource at this timeslot
            table_column = resource_coords[resource.name]
            table_row = timeslot_coords[timeslot]

            # Make every 2nd row a different colour
            if table_row % 2 == 0:
                colour = cfg.cell_colour2
            else:
                colour = cfg.cell_colour1

            # Create a frame to contain everything in the cell
            cell_frame = tk.Frame(
                master=table_frame,
                bg=colour)
            cell_frame.grid(
                column=table_column,
                row=table_row,
                sticky="nesw")

            # If there are no bookings for this resource at this time
            if resource.bookings[timeslot] == "None":

                # Create a label that says "No bookings"
                booking = tk.Label(
                    master=cell_frame,
                    text="No bookings",
                    fg=cfg.empty_text_colour,
                    bg=colour,
                    font=fonts["empty"],
                    anchor="center")
                booking.pack(
                    fill="both",
                    expand=True)

            # If there ARE bookings for this resource at this time
            else:
                cell_column = 0
                cell_row = 0
                for row in range(cfg.line_limit):
                    cell_frame.rowconfigure(index=row, weight=1)

                for booking in resource.bookings[timeslot]:

                    # New column when reaching the configured line limit
                    if cell_row > cfg.line_limit-1:
                        cell_row = 0
                        cell_column += 2
                        table_frame.columnconfigure(
                            index=table_column,
                            weight=cell_column)

                    # The name of the user who made the booking
                    bookee = (booking + ": ")
                    label = tk.Label(
                        master=cell_frame,
                        text=bookee,
                        fg=cfg.booking_text_colour,
                        bg=colour,
                        font=fonts["cell"])
                    label.grid(
                        column=cell_column,
                        row=cell_row,
                        sticky="nsw",
                        padx=(5, 0))

                    # The amount booked by the user
                    quantity = resource.bookings[timeslot][booking]
                    label = tk.Label(
                        master=cell_frame,
                        text=quantity,
                        fg=cfg.booking_text_colour,
                        bg=colour,
                        font=fonts["cell"])
                    label.grid(
                        column=cell_column + 1,
                        row=cell_row,
                        sticky="nsw")

                    cell_row += 1

    print("Finished initialising bookings.")


def add_table_gridlines(table_frame, timeslot_coords, resource_coords):

    # If the config defines a weight of 0 for both, skip function
    if cfg.cell_gridline_weight_y < 1 and cfg.cell_gridline_weight_x < 1:
        pass

    else:
        # Define the start and end coordinates of the table
        last_row = len(list(timeslot_coords.values()))
        last_column = len(list(resource_coords.values()))

        # Get all cells (including title cells) in the table
        cell_list = table_frame.winfo_children()

        # If title padding is enabled in the config
        if cfg.cell_title_gridlines == True:
            for cell in cell_list:

                # Get the cell coordinates in the table
                info = cell.grid_info()
                row = info["row"]
                column = info["column"]

                # If the cell is a title cell, only pad the bottom
                if row == 0:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=(0, cfg.cell_gridline_weight_y))

                # If the cell is at the bottom of the table, only pad the top
                elif row == last_row:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=(cfg.cell_gridline_weight_y, 0))

                # If the cell is in the middle, pad the top and bottom
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=cfg.cell_gridline_weight_y)

                # If the cell is a title cell, only pad the right
                if column == 0:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=(0, cfg.cell_gridline_weight_x))

                # If the cell is at the end of the table, only pad the left
                elif column == last_column:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=(cfg.cell_gridline_weight_x, 0))

                # If the cell is somewhere in the middle, pad left and right
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=cfg.cell_gridline_weight_x)

        # If title padding is not enabled in the config
        else:

            for cell in cell_list:

                # Get the cell coordinates in the table
                info = cell.grid_info()
                row = info["row"]
                column = info["column"]

                # If the cell is a title or end cell, do not pad
                if row == 0 or column == 0:
                    pass

                # If the cell underneath a title cell, only pad the bottom
                elif row == 1:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=(0, cfg.cell_gridline_weight_y))

                # If the cell is on the end row, only pad the top
                elif row == last_row:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=(cfg.cell_gridline_weight_y, 0))

                # If the cell is in the middle, pad top and bottom
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        pady=cfg.cell_gridline_weight_y)

                # If the cell is a title or end cell, do not pad
                if column == 0 or row == 0:
                    pass

                # If the cell next to a title cell, only pad the right
                elif column == 1:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=(0, cfg.cell_gridline_weight_x))

                # If the cell is on the end column, only pad the left
                elif column == last_column:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=(cfg.cell_gridline_weight_x, 0))

                # If the cell is in the middle, pad left and right
                else:
                    cell.grid(
                        row=row,
                        column=column,
                        padx=cfg.cell_gridline_weight_x)


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
