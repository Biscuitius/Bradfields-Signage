from tkinter import ttk
import tkinter.font as tkf


def init_theme():

    test_font = ("century gothic", 12, "bold")

    theme = ttk.Style()
    theme.configure(style="Root.TFrame", background="purple")
    theme.configure(
        style="TableTitle.TLabel",
        font=test_font,
        background="red")
    theme.configure(
        style="TableCell.TLabel",
        font=test_font,
        background="blue")
    theme.configure(
        style="MainTitle.TLabel",
        font=test_font,
        background="green")

    return theme
