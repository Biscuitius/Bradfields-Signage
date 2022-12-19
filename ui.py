import tkinter as tk
from tkinter import ttk
import styles
from main import resources


def toggle_fullscreen(root, event=None):
    root.state = not root.state
    root.attributes("-fullscreen", root.state)
    return "break"


def init_root():
    root = tk.Tk()
    root.title("EXAMPLE")
    root.config(padx=10, pady=10)
    root.resizable(False, False)
    root.bind("<F11>", lambda e: toggle_fullscreen(root))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    return root


def init_resources(root, resources):

    ttk.Style().configure("TFrame", background="red")

    i = 0
    for resource in resources.values():

        ttk.Frame(root).grid(column=i, row=0, sticky="nesw")
        root.columnconfigure(i, weight=1)

        i += 1


root = init_root()

init_resources(root, resources)

root.mainloop()
