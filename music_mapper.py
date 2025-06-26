import random
from constants import *

def is_even(n): 
    return n & 1 == 0

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