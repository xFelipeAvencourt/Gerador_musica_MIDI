import pygame.midi
import time
import random
from midiutil.MidiFile import MIDIFile


VOL_DEFAULT = 50
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
        self.current_volume = VOL_DEFAULT
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
                self.current_volume = min(self.current_volume + 10, VOL_MAX)
                acao['mudar_volume'] = self.current_volume
            elif char == MINUS:
                acao['tipo'] = 'mudar_volume'
                self.current_volume = max(self.current_volume - 10, 10)
                acao['mudar_volume'] = self.current_volume
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
                self.current_BPM = random.randint(BPM_DEFAULT, BPM_MAX)
                acao['mudar_BPM'] = self.current_BPM
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

            if acao['tipo'] == 'tocar_nota' and acao['nota'] is None:
                pass  
            else:
                executar.append(acao)
            self.last_char = text[i]
            i += 1
        return executar

class TextToMusicConverter:
    def __init__(self, bpm, volume, instrumento, config_callback=None, on_playback_finished=None):
        pygame.midi.init()
        self.midi_output = None
        for i in range(pygame.midi.get_count()):
            is_output= pygame.midi.get_device_info(i)
            if is_output:
                self.midi_output = pygame.midi.Output(i)
                break
        if self.midi_output is None:
            raise RuntimeError("Nenhum dispositivo MIDI de saída encontrado.")

        self.music_mapper = MusicMapper()
        self.music_mapper.current_BPM = bpm  
        self.instrumento = instrumento
        self.volume = volume
        self.bpm = bpm
        self.MIDI_exe = None
        self.config_callback = config_callback
        self.on_playback_finished = on_playback_finished
        
    def ConverterMusica(self, text):
        self.MIDI_exe = self.music_mapper.mapeamentoDaMusica(text)
        print(f"[DEBUG] ConverterMusica recebeu: '{text}'")
        string_acoes = gerar_string_acoes(self.MIDI_exe)
        Arquivo('MIDI_gerado.txt', 'w', string_acoes)
        print("Música convertida com sucesso!")

    def Play_MIDI(self):
         if self.config_callback:
           cfg = self.config_callback()
           self.music_mapper.current_instrumento = cfg['instrumento']
         else:
           self.music_mapper.current_instrumento = self.instrumento

         try:
             for action in self.MIDI_exe:
                if action['tipo'] == 'tocar_nota':
                    if self.config_callback:
                        config = self.config_callback()
                        bpm = self.bpm  
                        volume = self.volume  
                        instrumento = config['instrumento']
                        nota = action['nota']
                    else:
                        bpm = self.bpm
                        volume = self.volume
                        instrumento = self.music_mapper.current_instrumento
                        nota = action['nota']
                    bpm = self.bpm
                    volume = self.volume
                    instrumento = self.music_mapper.current_instrumento
                    nota = action['nota']

                    self._tocar_nota(nota, bpm, volume, instrumento)

                elif action['tipo'] == 'pausa':
                    time.sleep(0.25)
                elif action['tipo'] == 'alterar_instrumento':
                    self.music_mapper.current_instrumento = action['instrumento']
                elif action['tipo'] == 'mudar_volume':
                    self.volume = action['mudar_volume']
                elif action['tipo'] == 'mudar_oitava':
                    self.music_mapper.current_octave = action['mudar_oitava']
                elif action['tipo'] == 'mudar_BPM':
                    self.bpm = action['mudar_BPM']
         finally:
             if self.on_playback_finished:
                 self.on_playback_finished()

    def _tocar_nota(self, nota, bpm, volume, instrumento):
        
       # instrumento = self.music_mapper.current_instrumento
        #volume = self.music_mapper.current_volume
        canal = 0  

        print(f"[DEBUG] Tocando nota={nota}, instrumento={instrumento}, volume={volume}, bpm={bpm}")
    
        self.midi_output.set_instrument(instrumento, canal)
        self.midi_output.note_on(nota, volume, canal)
        time.sleep(60 / bpm)
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
        gerar_MIDI.tempo_atual = 0
        gerar_MIDI.instrumento_atual = None  
        gerar_MIDI.canal = 0
    nota = int(acao['nota'])
    volume = info.current_volume
    instrumento = info.current_instrumento
    canal = 0
    instrumento = getattr(info, "current_instrumento", 0)
    if gerar_MIDI.instrumento_atual != instrumento:
        gerar_MIDI.midi.addProgramChange(0, canal, gerar_MIDI.tempo_atual, instrumento)
        gerar_MIDI.instrumento_atual = instrumento

    gerar_MIDI.midi.addNote(
        track=0,
        channel=canal,
        pitch=nota,
        time=gerar_MIDI.tempo_atual,
        duration=1,
        volume=volume
    )
    gerar_MIDI.tempo_atual += 1

def Salvar_MIDI(texto, caminho_arquivo, config):
    try:
        gerar_MIDI.midi = MIDIFile(1)
        gerar_MIDI.midi.addTempo(0, 0, config["bpm"])
        gerar_MIDI.tempo_atual = 0
        gerar_MIDI.instrumento_atual = None  
        class FakeInfo:
            def __init__(self):
                self.current_volume = config["volume"]
                self.current_octave = OITAVA_DEFAULT 
                self.current_instrumento = config["instrumento"]
        mapper = MusicMapper()
        fake_info = FakeInfo()
        acoes = mapper.mapeamentoDaMusica(texto)
        for acao in acoes:
            if acao['tipo'] == 'tocar_nota' and acao['nota'] is not None:
                gerar_MIDI(acao, fake_info)
            elif acao['tipo'] == 'alterar_instrumento':
                fake_info.current_instrumento = acao['instrumento']
            elif acao['tipo'] == 'mudar_volume':
                fake_info.current_volume = acao['mudar_volume']
            elif acao['tipo'] == 'mudar_oitava':
                fake_info.current_octave = acao['mudar_oitava']
            elif acao['tipo'] == 'mudar_BPM':
                # Atualizar o tempo no MIDI se necessário
                pass
        with open(caminho_arquivo, "wb") as f:
            gerar_MIDI.midi.writeFile(f)
        print(f"[SUCESSO] Arquivo MIDI salvo em: {caminho_arquivo}")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar MIDI: {e}")
