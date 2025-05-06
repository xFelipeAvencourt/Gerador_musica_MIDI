import tkinter as tk
import customtkinter as ctk

class InputBar:
    def __init__(self, parent, controller):
        self.controller = controller

        container = tk.Frame(parent, bg="white")
        container.place(relx=0.5, rely=0.50, anchor="center")

        self.entry = ctk.CTkEntry(
            container,
            placeholder_text="Insira o texto aqui...",
            corner_radius=20,
            width=400,
            height=35,
            fg_color="#F5F5F5",
            text_color="black",
            border_width=0
        )
        self.entry.pack(side=tk.LEFT)

        self.button = ctk.CTkButton(
            container,
            text="PLAY",
            corner_radius=20,
            command=self.on_click,
            fg_color="#CCEDFF",
            text_color="#00A3FF",
            width=100,
            height=35
        )
        self.button.pack(side=tk.LEFT)

    def on_click(self):
        texto = self.entry.get()
        self.controller.buscar(texto)
