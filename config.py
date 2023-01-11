import tkinter.font as tkf

"""================= TECHNICAL CONFIG ================="""

institute_name = "Bradfields Academy"
url_codes = {
    "90486ca55805467b81d465bdb3bc3b58&categoryID=38566",
    "3e4333ba5d8a4071acbd64ca218be245&categoryID=35400",
    "d939505748a7491784179b3f1d76acb4&categoryID=35332"
}


"""================= GUI THEME CONFIG ================="""

root_colour = "#DDDDDD"
main_title_colour = "#FFFFFF"
table_frame_colour = "#FFFFFF"
cell_title_colour = "#75A9D1"
cell_colour1 = "#FCFCFC"
cell_colour2 = "#F3F3F3"

font_family = "century gothic"
main_title_text_colour = "#444444"
cell_title_text_colour = "#FFFFFF"
booking_text_colour = "#444444"
empty_text_colour = "#666666"

"""================= GUI SCALE CONFIG ================="""

root_pad = 7
frame_pad = 0
title_pad = 2
cell_weight = 3
cell_title_weight = 1
cell_spacing_vertical = 0
cell_spacing_horizontal = 2
cell_title_spacing = False


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
            size=8,
            weight="normal")
    }

    return fonts
