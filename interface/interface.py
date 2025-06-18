import tkinter as tk
from interface.logo import Logo
from interface.input_bar import InputBar
from interface.tutorial_button import TutorialButton
from interface.footer import Footer
from interface.control_panel import ControlPanel

class Interface(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("MUSIC.IT")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.resizable(False, False)
        self.configure(bg="white")

        # Monta a interface com os componentes modulares
        self.logo = Logo(self)
        self.input_bar = InputBar(self, controller)
        self.control_panel = ControlPanel(self, controller)
        self.control_panel.place(relx=0.5, rely=0.6, anchor="center")  # Posiciona o painel de controle
        self.tutorial_button = TutorialButton(self, controller)
        self.footer = Footer(self)
