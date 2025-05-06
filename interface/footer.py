import tkinter as tk

class Footer:
    def __init__(self, parent):
        label = tk.Label(
            parent,
            text="INFO1120 - TÉCNICAS DE CONSTRUÇÃO DE PROGRAMAS",
            bg="white",
            fg="#90CAF9",
            font=("Montserrat", 8)
        )
        label.pack(side=tk.BOTTOM, pady=20)
