from tkinter import ttk
import tkinter.font as tkf


def init_fonts(root):

    fonts = {

        "main_title_font": tkf.Font(
            root=root,
            font=None,
            name="main_title_font",
            exists=False,
            family="century gothic",
            size=16,
            weight="bold"
        ),

        "cell_title_font": tkf.Font(
            root=root,
            font=None,
            name="cell_title_font",
            exists=False,
            family="century gothic",
            size=12,
            weight="bold"
        ),

        "cell_font": tkf.Font(
            root=root,
            font=None,
            name="cell_font",
            exists=False,
            family="century gothic",
            size=12,
            weight="normal"
        )
    }

    return fonts


def init_theme(fonts):

    theme = ttk.Style()
    theme.configure(style="Root.TFrame", background="purple")
    theme.configure(
        style="TableTitle.TLabel",
        font=fonts["cell_title_font"],
        background="red")
    theme.configure(
        style="TableCell.TLabel",
        font=fonts["cell_font"],
        background="blue")
    theme.configure(
        style="MainTitle.TLabel",
        font=fonts["main_title_font"],
        background="green")

    return theme
