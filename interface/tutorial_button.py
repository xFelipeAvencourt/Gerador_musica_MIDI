import tkinter as tk
from PIL import Image, ImageTk

class TutorialButton:
    def __init__(self, parent, controller):
        img = Image.open("assets/tutorial_button.png")
        self.img_tk = ImageTk.PhotoImage(img)
        self.button = tk.Button(
            parent,
            image=self.img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=controller.abrir_tutorial,
            cursor="hand2"
        )
        self.button.place(x=1600, y=80)
