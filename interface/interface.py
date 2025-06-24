import tkinter as tk
from interface.logo import Logo
from interface.input_bar import InputBar
from interface.tutorial_button import TutorialButton
from interface.footer import Footer
from interface.control_panel import ControlPanel
import pygame

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.controller = controller
        self.title("MUSIC.IT")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.resizable(False, False)
        self.configure(bg="white")
        

        # Monta a interface com os componentes modulares
        self.logo = Logo(self)
        self.input_bar = InputBar(self, self)
        #self.control_panel = ControlPanel(self, controller)
        self.control_panel = ControlPanel(self, self) 
        self.control_panel.place(relx=0.5, rely=0.65, anchor="center")  # Posiciona o painel de controle
        self.tutorial_button = TutorialButton(self, self)
        self.footer = Footer(self)
    def set_texto(self, texto):
        self.input_bar.entry.delete(0, 'end')
        self.input_bar.entry.insert(0, texto.strip())
    def get_texto_atual(self):
        return self.input_bar.entry.get()
    def get_configuracoes(self):
        return self.control_panel.get_configuracoes()
    def buscar(self, texto):
        print(f"Executando som para: {texto}")


