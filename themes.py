from tkinter import ttk
from config import theme


def init_theme():
    theme = ttk.Style()
    theme.configure(style="Root.TFrame", background="purple")
    theme.configure(style="TableTitle.TLabel", background="red")
    theme.configure(style="TableCell.TLabel", background="blue")
    theme.configure(style="MainTitle.TLabel", background="green")
    return theme


class Theme():
    def __init__(self, name):
        self.name = name


Fortis_Theme = {
    "MainTitle"
}
