
import pygame.midi
import time
import random
from midiutil.MidiFile import MIDIFile

VOL_DEFAULT = 150
OITAVA_DEFAULT = 4
BPM_DEFAULT = 60
NUM_ACOES = 3
LARGURA_COLUNA = 25

NOTAS = ['A','B','C','D','E','F','G']
LET_VOGAL = ['I','O','U']
AUMENTA_OITAVA = ['.']
NL = '\n'
SPACE = ' '
PLUS = '+'
MINUS = '-'
VOL_MAX = 100
OITAVA_MAX = 8
BPM_MAX = 240
uBPM = 80
uMIDI = 12

PIANO = 0
BANDONEON = '!'
AGOGE = ','
TEL_TOCANDO = 125

class MusicMapper:
    def __init__(self):
        self.instrumentos = {
            0: 0,
            '!': 24,
            ',': 114
        }
        self.NOTAS = {
            'A': 9, 'B': 11, 'C': 0,
            'D': 2, 'E': 4, 'F': 5, 'G': 7
        }
        self.current_instrumento = 0
        self.current_octave = OITAVA_DEFAULT
        self.current_volume = 127
        self.current_BPM = BPM_DEFAULT
        self.last_char = None

    def mapeamentoDaMusica(self, text):
        executar = []
        i = 0
        length = len(text)
        while i < length:
            char = text[i]
            acao = {'tipo': None, 'nota': None, 'instrumento': None, 'mudar_volume': None, 'mudar_oitava': None, 'mudar_BPM': None}
            if char == 'B' and i + 3 < length and text[i:i+4] == 'BPM+':
                acao['tipo'] = 'mudar_BPM'
                self.current_BPM = min(self.current_BPM + uBPM, BPM_MAX)
                acao['mudar_BPM'] = self.current_BPM
                i += 3
            elif char in self.NOTAS or char.upper() in self.NOTAS:
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = self.NOTAS[char.upper()] + (self.current_octave * uMIDI)
            elif char == SPACE:
                acao['tipo'] = 'pausa'
            elif char == PLUS:
                acao['tipo'] = 'mudar_volume'
                self.current_volume = min(self.current_volume * 2, VOL_MAX)
                acao['mudar_volume'] = self.current_volume
            elif char == MINUS:
                acao['tipo'] = 'mudar_volume'
                self.current_volume = VOL_DEFAULT
                acao['mudar_volume'] = VOL_DEFAULT
            elif char in LET_VOGAL or char.upper() in LET_VOGAL:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + (self.current_octave * uMIDI)
                else:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = TEL_TOCANDO
            elif char == 'R' and i + 1 < length:
                next_char = text[i + 1]
                if next_char == '+':
                    acao['tipo'] = 'mudar_oitava'
                    self.current_octave = min(self.current_octave + 1, OITAVA_MAX)
                    acao['mudar_oitava'] = self.current_octave
                    i += 1
                elif next_char == '-':
                    acao['tipo'] = 'mudar_oitava'
                    self.current_octave = max(self.current_octave - 1, 1)
                    acao['mudar_oitava'] = self.current_octave
                    i += 1
            elif char == '?':
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = random.choice(list(self.NOTAS.values())) + (random.randint(1, OITAVA_MAX - 1) * uMIDI)
            elif char == ';':
                acao['tipo'] = 'mudar_BPM'
                acao['mudar_BPM'] = random.randint(BPM_DEFAULT, BPM_MAX)
            elif char == NL:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = random.choice(list(self.instrumentos.values()))
            elif char == BANDONEON:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = self.instrumentos['!']
            elif char.isdigit() and Is_even(int(char)):
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = (self.current_instrumento + int(char)) % len(self.instrumentos)
            elif char == AGOGE:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = self.instrumentos[',']
            else:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + (self.current_octave * uMIDI)
                else:
                    acao['tipo'] = 'pausa'

            if acao['tipo'] == 'tocar_nota' and acao['nota'] is not None:
                gerar_MIDI(acao, self)
            executar.append(acao)
            self.last_char = text[i]
            i += 1
        return executar

class TextToMusicConverter:
    def __init__(self, bpm=BPM_DEFAULT, instrumento=PIANO):
        pygame.midi.init()
        self.midi_output = None
        for i in range(pygame.midi.get_count()):
            interf, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
            if is_output:
                self.midi_output = pygame.midi.Output(i)
                break
        if self.midi_output is None:
            raise RuntimeError("Nenhum dispositivo MIDI de saída encontrado.")

        self.music_mapper = MusicMapper()
        self.music_mapper.current_instrumento = instrumento
        self.bpm = bpm
        self.MIDI_exe = None

    def ConverterMusica(self, text):
        self.MIDI_exe = self.music_mapper.mapeamentoDaMusica(text)
        print(f"[DEBUG] ConverterMusica recebeu: '{text}'")
        string_acoes = gerar_string_acoes(self.MIDI_exe)
        Arquivo('MIDI_gerado.txt', 'w', string_acoes)
        print("Música convertida com sucesso!")

    def Play_MIDI(self):
        for action in self.MIDI_exe:
            if action['tipo'] == 'tocar_nota':
                self._tocar_nota(action['nota'])
            elif action['tipo'] == 'pausa':
                time.sleep(0.25)
            elif action['tipo'] == 'alterar_instrumento':
                self.music_mapper.current_instrumento = action['instrumento']
            elif action['tipo'] == 'mudar_volume':
                self.music_mapper.current_volume = action['mudar_volume']
            elif action['tipo'] == 'mudar_oitava':
                self.music_mapper.current_octave = action['mudar_oitava']
            elif action['tipo'] == 'mudar_BPM':
                self.bpm = action['mudar_BPM']

    def _tocar_nota(self, nota: int):
        
        instrumento = self.music_mapper.current_instrumento
        volume = self.music_mapper.current_volume
        canal = 0  

        print(f"[DEBUG] Tocando nota={nota}, instrumento={instrumento}, volume={volume}, bpm={self.bpm}")
    
        self.midi_output.set_instrument(instrumento, canal)
        self.midi_output.note_on(nota, volume, canal)
        time.sleep(60 / self.bpm)
        self.midi_output.note_off(nota, volume, canal)




    def __del__(self):
        try:
            if hasattr(self, "midi_output"):
                self.midi_output.close()
            if pygame.midi.get_init():
                pygame.midi.quit()
        except Exception as e:
            print(f"[AVISO] Erro ao finalizar pygame.midi: {e}")

def Is_even(n): return n & 1 == 0

def Arquivo(arquivo, modo='r', conteudo=None):
    try:
        if modo == 'r':
            with open(arquivo, 'r') as f: return f.read()
        elif modo == 'w':
            with open(arquivo, 'w') as f: f.write(conteudo)
    except Exception as e:
        print(f"Erro no arquivo: {e}")

def gerar_string_acoes(acoes):
    chaves = ['nota', 'instrumento', 'mudar_volume', 'mudar_oitava', 'mudar_BPM']
    linhas = []
    for grupo in [acoes[i:i+3] for i in range(0, len(acoes), 3)]:
        partes = []
        for acao in grupo:
            texto = f"{acao['tipo']}:{next((acao.get(k, '') for k in chaves if k in acao), '')}".rstrip(':')
            partes.append(texto.ljust(LARGURA_COLUNA))
        linhas.append(" | ".join(partes))
    return "\n".join(linhas)

def gerar_MIDI(acao, info):
    if not hasattr(gerar_MIDI, "midi"):
        gerar_MIDI.midi = MIDIFile(1)
        gerar_MIDI.midi.addTempo(0, 0, BPM_DEFAULT)
        gerar_MIDI.canal = 0
    nota = int(acao['nota'])
    volume = info.current_volume
    oitava = info.current_octave
    gerar_MIDI.midi.addNote(0, 0, nota + (oitava * 12), 0, 1, volume)
    gerar_MIDI.canal = 0

def Salvar_MIDI(texto, caminho_arquivo):
    try:
        gerar_MIDI.midi = MIDIFile(1)
        gerar_MIDI.midi.addTempo(0, 0, BPM_DEFAULT)
        mapper = MusicMapper()
        mapper.mapeamentoDaMusica(texto)  
        if hasattr(gerar_MIDI, "midi"):
            with open(caminho_arquivo, "wb") as f:
                gerar_MIDI.midi.writeFile(f)
    except Exception as e:
        print(f"[ERRO] Falha ao salvar MIDI: {e}")
