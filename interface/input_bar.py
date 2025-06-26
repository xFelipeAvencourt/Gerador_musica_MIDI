import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from Implementacao import TextToMusicConverter
import threading
import time


class InputBar:
    def __init__(self, parent, controller):
        self.controller = controller
        self.is_playing = False
        self.parent = parent

        container = tk.Frame(parent, bg="white")
        container.place(relx=0.5, rely=0.50, anchor="center")

        input_frame = tk.Frame(container, bg="white")       
        input_frame.pack(side=tk.LEFT)
        
        # Campo de entrada
        #self.entry = ctk.CTkEntry(
        #input_frame,
        #placeholder_text="Insira o texto aqui...",
        #corner_radius=40,
        #width=400,
        #height=56,
        #fg_color="#F5F5F5",
        #text_color="black",
        #border_width=0  
         #   )
        #self.entry.pack(side=tk.LEFT)
        self.textbox = ctk.CTkTextbox(
            input_frame,
            width=400,
            height=20,
            fg_color="#F5F5F5",
            text_color="black",
            corner_radius=16
        )
        self.textbox.pack(side=tk.LEFT)
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
        play_img = Image.open("assets/play.png").resize((117, 56))
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

        reproducao_img = Image.open("assets/reproduzindo.png").resize((188, 36))
        self.reproducao_img_tk = ImageTk.PhotoImage(reproducao_img)
        self.reproducao_label = tk.Label(
            parent,
            image=self.reproducao_img_tk,
            bg="white"
        )


    def start_play(self):
        texto = self.textbox.get("0.0", tk.END)
        print(f"[DEBUG] Texto inserido: '{texto}'")
        if texto.strip():
            self.is_playing = True
            self.reproducao_label.place(relx=0.5, rely=0.9, anchor="center")

        try:
            config = self.controller.get_configuracoes()
            self.controller.buscar(texto)
            musica = TextToMusicConverter(
                bpm=config["bpm"],
                instrumento=config["instrumento"],
                volume=config["volume"],
                config_callback=self.controller.get_configuracoes,
                on_playback_finished=self.on_playback_finished
            )

            def tocar():
                 musica.converter_musica(texto)
                 if self.is_playing:
                        musica.play_midi()
                        print("Reprodução iniciada")

            threading.Thread(target=tocar, daemon=True).start()

        except Exception as e:
            print(f"[Erro] Falha ao executar: {e}")

    def on_playback_finished(self):
        """Callback chamado quando a reprodução MIDI termina"""
        if self.is_playing:
            self.parent.after(0, self.hide_reproducao)

    def hide_reproducao(self):
        self.is_playing = False
        self.reproducao_label.place_forget()
        print("Reprodução finalizada - imagem removida")

    def stop_play(self):
        self.is_playing = False
        self.reproducao_label.place_forget()
        print("Reprodução parada")

    def on_click(self):
        self.start_play()

    def clear_input(self):
        self.textbox.delete("0.0", tk.END)

    def get_texto_atual(self):
          return self.textbox.get("0.0", tk.END)

    

