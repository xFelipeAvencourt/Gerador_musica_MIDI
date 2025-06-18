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
            command=self.toggle_tutorial,
            cursor="hand2"
        )
        self.button.place(x=1600, y=80)
        self.parent = parent
        
        self.tutorial_frame = tk.Frame(
            parent,
            bg="#E6F3FF",
            width=300,
            height=200
        )
        self.tutorial_frame.place(x=1600, y=10)
        
        # Texto do tutorial
        self.tutorial_text = tk.Label(
            self.tutorial_frame,
            text = "Bem-vindo ao Gerador de Música a partir de Texto!\n\n" + \
                "Este software transforma texto em música com base em regras simples:\n" + \
                "Letras A–G: geram notas musicais (Lá, Si, Dó, etc.)\n" + \
                "Espaço: pausa ou silêncio\n" + \
                "'+': dobra o volume atual\n" + \
                "'-': volume volta ao padrão inicial\n" + \
                "Vogais O, I, U: repetem a nota anterior ou tocam som de telefone\n" + \
                "'R+': aumenta a oitava atual\n" + \
                "'R-': diminui a oitava atual\n" + \
                "'?': toca uma nota aleatória entre A e G\n" + \
                "Nova linha: troca o instrumento (definido pelo grupo)\n" + \
                "'BPM+': aumenta o ritmo em 80 BPM\n" + \
                "';': define um BPM aleatório\n" + \
                "Outros caracteres: continuam a execução atual (NOP)\n"  ,
            bg="#E6F3FF",
            fg="#00A3FF", 
            wraplength=280,
            justify="left",
            padx=20,
            pady=20
        )
        self.tutorial_text.pack(expand=True, fill="both")
        
        # Inicialmente esconde o tutorial
        self.tutorial_frame.place_forget()
        
    def toggle_tutorial(self):
        if self.tutorial_frame.winfo_ismapped():
            self.tutorial_frame.place_forget()
        else:
            self.tutorial_frame.place(x=1600, y=150)
