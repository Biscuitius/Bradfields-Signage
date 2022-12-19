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

    return root


def init_resources(root, resources):
    i = 0
    for resource in resources.values():
        ttk.Frame(root, style="body").pack()

        i += 1


root = init_root()

init_resources(root, resources)

root.mainloop()
