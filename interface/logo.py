import tkinter as tk
from PIL import Image, ImageTk

class Logo:
    def __init__(self, parent):
        img = Image.open("assets/logo.png")
        self.logo_tk = ImageTk.PhotoImage(img)
        self.label = tk.Label(parent, image=self.logo_tk, bg="white")
        self.label.place(relx=0.5, rely=0.4, anchor="center")
