import tkinter.font as tkf

root_colour = "red"
main_title_colour = "orange"
cell_title_colour = "yellow"
cell_colour = "green"
text_colour = "black"


def init_fonts():
    fonts = {
        "main_title": tkf.Font(
            root=None,
            font=None,
            name="main_title",
            exists=False,
            family="century gothic",
            size=16,
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
            weight="normal")
    }

    return fonts
