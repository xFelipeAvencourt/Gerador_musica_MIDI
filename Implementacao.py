import pygame.midi
import time
import random
from midiutil.MidiFile import MIDIFile


# Constantes de configuração padrão
VOL_DEFAULT = 50
OITAVA_DEFAULT = 4
BPM_DEFAULT = 60
NUM_ACOES = 3
LARGURA_COLUNA = 25

# Constantes de volume
VOL_MAX = 100
VOL_MIN = 10
VOL_INCREMENTO = 10

# Constantes de oitava
OITAVA_MAX = 8
OITAVA_MIN = 1
OITAVA_INCREMENTO = 1

# Constantes de BPM
BPM_MAX = 240
BPM_INCREMENTO = 80

# Constantes MIDI
MIDI_UNIDADE = 12
CANAL_MIDI = 0
TRACK_MIDI = 0
TEMPO_INICIAL = 0
DURACAO_NOTA = 1

# Constantes de tempo
PAUSA_DURACAO = 0.25
SEGUNDOS_POR_MINUTO = 60

# Constantes de instrumentos
INSTRUMENTO_PIANO = 0
INSTRUMENTO_BANDONEON = 24
INSTRUMENTO_AGOGE = 114

# Constantes de notas MIDI
NOTA_A = 9
NOTA_B = 11
NOTA_C = 0
NOTA_D = 2
NOTA_E = 4
NOTA_F = 5
NOTA_G = 7

# Constantes de caracteres especiais
NOTAS = ['A','B','C','D','E','F','G']
LET_VOGAL = ['I','O','U']
AUMENTA_OITAVA = ['.']
NL = '\n'
SPACE = ' '
PLUS = '+'
MINUS = '-'

PIANO = 0
BANDONEON = '!'
AGOGE = ','
TEL_TOCANDO = 125

class MusicMapper:
    def __init__(self):
        self.instrumentos = {
            0: INSTRUMENTO_PIANO,
            '!': INSTRUMENTO_BANDONEON,
            ',': INSTRUMENTO_AGOGE
        }
        self.NOTAS = {
            'A': NOTA_A, 'B': NOTA_B, 'C': NOTA_C,
            'D': NOTA_D, 'E': NOTA_E, 'F': NOTA_F, 'G': NOTA_G
        }
        self.current_instrumento = INSTRUMENTO_PIANO
        self.current_octave = OITAVA_DEFAULT
        self.current_volume = VOL_DEFAULT
        self.current_BPM = BPM_DEFAULT
        self.last_char = None

    def mapeamento_da_musica(self, text):
        executar = []
        i = 0
        length = len(text)
        while i < length:
            char = text[i]
            acao = {'tipo': None, 'nota': None, 'instrumento': None, 'mudar_volume': None, 'mudar_oitava': None, 'mudar_BPM': None}
            if char == 'B' and i + 3 < length and text[i:i+4] == 'BPM+':
                acao['tipo'] = 'mudar_BPM'
                self.current_BPM = min(self.current_BPM + BPM_INCREMENTO, BPM_MAX)
                acao['mudar_BPM'] = self.current_BPM
                i += 3
            elif char in self.NOTAS or char.upper() in self.NOTAS:
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = self.NOTAS[char.upper()] + (self.current_octave * MIDI_UNIDADE)
            elif char == SPACE:
                acao['tipo'] = 'pausa'
            elif char == PLUS:
                acao['tipo'] = 'mudar_volume'
                self.current_volume = min(self.current_volume + VOL_INCREMENTO, VOL_MAX)
                acao['mudar_volume'] = self.current_volume
            elif char == MINUS:
                acao['tipo'] = 'mudar_volume'
                self.current_volume = max(self.current_volume - VOL_INCREMENTO, VOL_MIN)
                acao['mudar_volume'] = self.current_volume
            elif char in LET_VOGAL or char.upper() in LET_VOGAL:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + (self.current_octave * MIDI_UNIDADE)
                else:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = TEL_TOCANDO
            elif char == 'R' and i + 1 < length:
                next_char = text[i + 1]
                if next_char == '+':
                    acao['tipo'] = 'mudar_oitava'
                    self.current_octave = min(self.current_octave + OITAVA_INCREMENTO, OITAVA_MAX)
                    acao['mudar_oitava'] = self.current_octave
                    i += 1
                elif next_char == '-':
                    acao['tipo'] = 'mudar_oitava'
                    self.current_octave = max(self.current_octave - OITAVA_INCREMENTO, OITAVA_MIN)
                    acao['mudar_oitava'] = self.current_octave
                    i += 1
            elif char == '?':
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = random.choice(list(self.NOTAS.values())) + (random.randint(OITAVA_MIN, OITAVA_MAX - 1) * MIDI_UNIDADE)
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
            elif char.isdigit() and is_even(int(char)):
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = (self.current_instrumento + int(char)) % len(self.instrumentos)
            elif char == AGOGE:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = self.instrumentos[',']
            else:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + (self.current_octave * MIDI_UNIDADE)
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
        
    def converter_musica(self, text):
        self.MIDI_exe = self.music_mapper.mapeamento_da_musica(text)
        print(f"[DEBUG] converter_musica recebeu: '{text}'")
        string_acoes = gerar_string_acoes(self.MIDI_exe)
        arquivo('MIDI_gerado.txt', 'w', string_acoes)
        print("Música convertida com sucesso!")

    def play_midi(self):
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
                    time.sleep(PAUSA_DURACAO)
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
        canal = CANAL_MIDI  

        print(f"[DEBUG] Tocando nota={nota}, instrumento={instrumento}, volume={volume}, bpm={bpm}")
    
        self.midi_output.set_instrument(instrumento, canal)
        self.midi_output.note_on(nota, volume, canal)
        time.sleep(SEGUNDOS_POR_MINUTO / bpm)
        self.midi_output.note_off(nota, volume, canal)




    def __del__(self):
        try:
            if hasattr(self, "midi_output"):
                self.midi_output.close()
            if pygame.midi.get_init():
                pygame.midi.quit()
        except Exception as e:
            print(f"[AVISO] Erro ao finalizar pygame.midi: {e}")

def is_even(n): return n & 1 == 0

def arquivo(arquivo, modo='r', conteudo=None):
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
    for grupo in [acoes[i:i+NUM_ACOES] for i in range(0, len(acoes), NUM_ACOES)]:
        partes = []
        for acao in grupo:
            texto = f"{acao['tipo']}:{next((acao.get(k, '') for k in chaves if k in acao), '')}".rstrip(':')
            partes.append(texto.ljust(LARGURA_COLUNA))
        linhas.append(" | ".join(partes))
    return "\n".join(linhas)

def gerar_midi(acao, info):
    if not hasattr(gerar_midi, "midi"):
        gerar_midi.midi = MIDIFile(1)
        gerar_midi.midi.addTempo(TRACK_MIDI, CANAL_MIDI, BPM_DEFAULT)
        gerar_midi.tempo_atual = TEMPO_INICIAL
        gerar_midi.instrumento_atual = None  
        gerar_midi.canal = CANAL_MIDI
    nota = int(acao['nota'])
    volume = info.current_volume
    instrumento = info.current_instrumento
    canal = CANAL_MIDI
    instrumento = getattr(info, "current_instrumento", INSTRUMENTO_PIANO)
    if gerar_midi.instrumento_atual != instrumento:
        gerar_midi.midi.addProgramChange(TRACK_MIDI, canal, gerar_midi.tempo_atual, instrumento)
        gerar_midi.instrumento_atual = instrumento

    gerar_midi.midi.addNote(
        track=TRACK_MIDI,
        channel=canal,
        pitch=nota,
        time=gerar_midi.tempo_atual,
        duration=DURACAO_NOTA,
        volume=volume
    )
    gerar_midi.tempo_atual += 1

def salvar_midi(texto, caminho_arquivo, config):
    try:
        gerar_midi.midi = MIDIFile(1)
        gerar_midi.midi.addTempo(TRACK_MIDI, CANAL_MIDI, config["bpm"])
        gerar_midi.tempo_atual = TEMPO_INICIAL
        gerar_midi.instrumento_atual = None  
        class FakeInfo:
            def __init__(self):
                self.current_volume = config["volume"]
                self.current_octave = OITAVA_DEFAULT 
                self.current_instrumento = config["instrumento"]
        mapper = MusicMapper()
        fake_info = FakeInfo()
        acoes = mapper.mapeamento_da_musica(texto)
        for acao in acoes:
            if acao['tipo'] == 'tocar_nota' and acao['nota'] is not None:
                gerar_midi(acao, fake_info)
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
            gerar_midi.midi.writeFile(f)
        print(f"[SUCESSO] Arquivo MIDI salvo em: {caminho_arquivo}")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar MIDI: {e}")
