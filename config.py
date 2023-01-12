import tkinter.font as tkf

"""================= TECHNICAL CONFIG ================="""

institute_name = "Bradfields Academy"
url_codes = {
    "90486ca55805467b81d465bdb3bc3b58&categoryID=38566"
}


"""================= GUI THEME CONFIG ================="""

root_colour = "#DDDDDD"
main_title_colour = "#FFFFFF"
table_frame_colour = "#D9D9D9"
cell_title_colour = "#75A9D1"
cell_colour1 = "#FCFCFC"
cell_colour2 = "#F3F3F3"

font_family = "century gothic"
main_title_text_colour = "#444444"
cell_title_text_colour = "#FFFFFF"
booking_text_colour = "#444444"
empty_text_colour = "#666666"

"""================= GUI SCALE CONFIG ================="""

line_limit = 3
root_pad = 8
frame_pad = 0
cell_weight = 3
cell_title_weight = 1
cell_gridline_weight_y = 1
cell_gridline_weight_x = 1
cell_title_gridlines = False


"""================= GUI FONTS CONFIG ================="""


def init_fonts():
    fonts = {
        "main_title": tkf.Font(
            root=None,
            font=None,
            name="main_title",
            exists=False,
            family="century gothic",
            size=24,
            weight="bold"),

        "cell_title": tkf.Font(
            root=None,
            font=None,
            name="cell_title",
            exists=False,
            family="century gothic",
            size=12,
            weight="bold"),

        "cell": tkf.Font(
            root=None,
            font=None,
            name="cell",
            exists=False,
            family="century gothic",
            size=12,
            weight="normal"),

        "empty": tkf.Font(
            root=None,
            font=None,
            name="empty",
            exists=False,
            family="century gothic",
            size=12,
            weight="normal",
            slant="italic")
    }

    return fonts
