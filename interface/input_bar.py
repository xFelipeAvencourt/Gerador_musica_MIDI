import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class InputBar:
    def __init__(self, parent, controller):
        self.controller = controller
        self.is_playing = False
        self.parent = parent  

        container = tk.Frame(parent, bg="white")
        container.place(relx=0.5, rely=0.50, anchor="center")

        self.entry = ctk.CTkEntry(
            container,
            placeholder_text="Insira o texto aqui...",
            corner_radius=40,
            width=400,
            height=56,
            fg_color="#F5F5F5",
            text_color="black",
            border_width=0
        )
        self.entry.pack(side=tk.LEFT)

        # Botão Clear Input
        clear_img = Image.open("assets/clear.png").resize((20, 20))
        self.clear_img_tk = ImageTk.PhotoImage(clear_img)
        self.clear_button = tk.Button(
            container,
            image=self.clear_img_tk,
            bd=0,
            bg="#F5F5F5",
            activebackground="#F5F5F5",
            command=self.clear_input,
            cursor="hand2"
        )
        self.clear_button.place(x=360, y=18)

        # Botão PLAY
        play_img = Image.open("assets/play.png").resize((105, 56))
        self.play_img_tk = ImageTk.PhotoImage(play_img)
        self.play_button = tk.Button(
            container,
            image=self.play_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.start_play,
            cursor="hand2"
        )
        self.play_button.pack(side=tk.LEFT)

        
        # Botão reproduzindo 
        pause_img = Image.open("assets/pause.png").resize((234, 48))
        self.pause_img_tk = ImageTk.PhotoImage(pause_img)
        self.pause_button = tk.Button(
            parent,
            image=self.pause_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.stop_play,
            cursor="hand2"
        )

    def start_play(self):
        texto = self.entry.get()
        if texto.strip(): 
            self.pause_button.place(relx=0.5, rely=0.9, anchor="center")
            self.is_playing = True
            # todo: Implementar a lógica para iniciar a reprodução
            print("Reprodução iniciada")
            self.controller.buscar(texto)
    
    def stop_play(self):
        self.pause_button.place_forget()
        self.is_playing = False
        # todo: Implementar a lógica para parar a reprodução
        print("Reprodução parada")
    
    def on_click(self):
        self.start_play()

    def clear_input(self):
        self.entry.delete(0, tk.END)
