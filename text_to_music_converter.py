import time
import pygame.midi
from constants import *
from music_mapper import MusicMapper
from utils import arquivo, gerar_string_acoes

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
        arquivo('arquivos/MIDI_gerado.txt', 'w', string_acoes)
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