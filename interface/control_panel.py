import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from Implementacao import salvar_midi

class ControlPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.bpm_var = tk.IntVar(value=120)
        self.volume_var = tk.IntVar(value=50)
        
        self.first_line = tk.Frame(self, bg="white")
        self.first_line.pack(pady=20)

        # Botão BPM
        bpm_img = Image.open("assets/bpm.png").resize((117, 48))
        self.bpm_img_tk = ImageTk.PhotoImage(bpm_img)
        self.bpm_modal_button = tk.Button(
            self.first_line,
            image=self.bpm_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.open_bpm_modal,
            cursor="hand2"
        )
        self.bpm_modal_button.pack(side=tk.LEFT, padx=10)

        # Botão Volume
        volume_img = Image.open("assets/volume.png").resize((131, 48))
        self.volume_img_tk = ImageTk.PhotoImage(volume_img)
        self.volume_modal_button = tk.Button(
            self.first_line,
            image=self.volume_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.open_volume_modal,
            cursor="hand2"
        )
        self.volume_modal_button.pack(side=tk.LEFT, padx=10)

        # Botão SAVE
        try:
            save_img = Image.open("assets/save.png").resize((131, 48))
            self.save_img_tk = ImageTk.PhotoImage(save_img)
            self.save_button = tk.Button(
                self.first_line,
                image=self.save_img_tk,
                bd=0,
                bg="white",
                activebackground="white",
                command=self.save_midi,
                cursor="hand2"
            )
            self.save_button.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"[Erro] Falha ao carregar imagem do botão salvar: {e}")

        self.second_line = tk.Frame(self, bg="white")
        self.second_line.pack(pady=(10, 0))

        # # Botão de recentes
        # recentes_img = Image.open("assets/recentes.png").resize((234, 48))
        # self.recentes_img_tk = ImageTk.PhotoImage(recentes_img)
        # self.recentes_button = tk.Button(
        #     self.second_line,
        #     image=self.recentes_img_tk,
        #     bd=0,
        #     bg="white",
        #     activebackground="white",
        #     command=self.open_recentes_modal,
        #     cursor="hand2"
        # )
        # self.recentes_button.pack(side=tk.LEFT, padx=10)

        # Botão de upload (carregar arquivo)
        upload_img = Image.open("assets/upload.png").resize((234, 48))
        self.upload_img_tk = ImageTk.PhotoImage(upload_img)
        self.upload_button = tk.Button(
            self.second_line,
            image=self.upload_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.upload_file,
            cursor="hand2"
        )
        self.upload_button.pack(side=tk.LEFT, padx=10)

        # Botão de instrumentos
        instrumento_img = Image.open("assets/instrumento.png").resize((234, 48))
        self.instrumento_img_tk = ImageTk.PhotoImage(instrumento_img)
        self.instrument_modal_button = tk.Button(
            self.second_line,
            image=self.instrumento_img_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.open_instrument_modal,
            cursor="hand2"
        )
        self.instrument_modal_button.pack(side=tk.LEFT, padx=10)
        self.instruments = ["Piano", "Guitarra", "Violino", "Flauta", "Bateria"]
        self.instrument_var = tk.StringVar(value=self.instruments[0])
    
    def update_bpm(self, value):
        # todo: Atualizar o valor do BPM
        self.bpm_var.set(int(float(value)))
        print(f"BPM atualizado para: {self.bpm_var.get()}")

    def update_volume(self, value):
        # todo: Atualizar o valor do Volume
        self.volume_var.set(int(float(value)))
        print(f"Volume atualizado para: {self.volume_var.get()}")

    def upload_file(self):
    
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo .txt",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                    print(f"[DEBUG] Conteúdo do arquivo lido: {conteudo[:50]}...")
                    self.controller.set_texto(conteudo)
            except Exception as e:
                print(f"[ERRO] Falha ao ler arquivo: {e}")

    def open_bpm_modal(self):
        bpm_modal = tk.Toplevel(self)
        bpm_modal.title("Ajustar BPM")
        bpm_modal.geometry("300x120")
        bpm_modal.transient(self)
        bpm_modal.grab_set()
        bpm_modal.configure(bg="white")

        bpm_label = tk.Label(bpm_modal, text="BPM:", bg="white", font=("Arial", 12))
        bpm_label.pack(pady=(10, 0))

        bpm_slider = ttk.Scale(
            bpm_modal,
            from_=20,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.bpm_var,
            length=200,
            command=self.update_bpm
        )
        bpm_slider.pack(pady=10)

        bpm_value_label = tk.Label(bpm_modal, textvariable=self.bpm_var, bg="white", font=("Arial", 12))
        bpm_value_label.pack()

    def open_volume_modal(self):
        volume_modal = tk.Toplevel(self)
        volume_modal.title("Ajustar Volume")
        volume_modal.geometry("300x120")
        volume_modal.transient(self)
        volume_modal.grab_set()
        volume_modal.configure(bg="white")

        volume_label = tk.Label(volume_modal, text="Volume:", bg="white", font=("Arial", 12))
        volume_label.pack(pady=(10, 0))

        volume_slider = ttk.Scale(
            volume_modal,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            length=200,
            command=self.update_volume
        )
        volume_slider.pack(pady=10)

        volume_value_label = tk.Label(volume_modal, textvariable=self.volume_var, bg="white", font=("Arial", 12))
        volume_value_label.pack()

    def open_instrument_modal(self):
        modal = tk.Toplevel(self)
        modal.title("Selecionar Instrumento")
        modal.geometry("300x120")
        modal.transient(self)
        modal.grab_set()
        modal.configure(bg="white")

        label = tk.Label(modal, text="Instrumento:", bg="white", font=("Arial", 12))
        label.pack(pady=(10, 0))

        combo = ttk.Combobox(
            modal,
            textvariable=self.instrument_var,
            values=self.instruments,
            state="readonly",
            width=20
        )
        combo.pack(pady=10)

        btn_ok = tk.Button(modal, text="OK", command=modal.destroy)
        btn_ok.pack(pady=(0, 10))

    # def open_recentes_modal(self):
    #     # todo: Implementar a lógica para o modal de recentes
    #     print("Botão de recentes clicado!")
    def get_configuracoes(self):
        return {
            "bpm": self.bpm_var.get(),
            "instrumento": self.instruments.index(self.instrument_var.get()) * 24,
            "volume": self.volume_var.get()
        }

    def save_midi(self):
        try:
            # Pegar o texto do input_bar através do controller
            texto = self.controller.get_texto_atual()
            if not texto or not texto.strip():
                print("[Aviso] Nenhum texto para salvar")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".mid",
                filetypes=[("MIDI files", "*.mid")],
                title="Salvar arquivo MIDI"
            )
            if file_path:
                config = self.get_configuracoes()
                salvar_midi(texto, file_path, config)
                print(f"[Info] MIDI salvo em: {file_path}")
        except Exception as e:
            print(f"[Erro] Falha ao salvar MIDI: {e}")
