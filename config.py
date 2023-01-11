import tkinter.font as tkf

"""================= TECHNICAL CONFIG ================="""

institute_name = "Bradfields Academy"
url_codes = {
    "90486ca55805467b81d465bdb3bc3b58&categoryID=38566",
    "3e4333ba5d8a4071acbd64ca218be245&categoryID=35400",
    "d939505748a7491784179b3f1d76acb4&categoryID=35332"
}


"""================= GUI THEME CONFIG ================="""

root_colour = "#D5E0ED"
main_title_colour = "#84B8D8"
table_frame_colour = "#FFFFFF"
cell_title_colour = "#D5E0ED"
cell_colour1 = "#ECECEC"
cell_colour2 = "#F7F7F7"

font_family = "century gothic"
main_title_text_colour = "#FFFFFF"
cell_title_text_colour = "#3165A5"
cell_text_colour = "#000000"

"""================= GUI SCALE CONFIG ================="""

cell_pad_x = 1
cell_pad_y = 1
title_pad_x = 1
title_pad_y = (1, 7)
root_pad_x = 7
root_pad_y = 7
table_pad_x = 1
table_pad_y = 1


"""================= GUI FONTS CONFIG ================="""


def init_fonts():
    fonts = {
        "main_title": tkf.Font(
            root=None,
            font=None,
            name="main_title",
            exists=False,
            family="century gothic",
            size=8,
            weight="bold"),

        "cell_title": tkf.Font(
            root=None,
            font=None,
            name="cell_title",
            exists=False,
            family="century gothic",
            size=8,
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
