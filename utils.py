from midiutil.MidiFile import MIDIFile
from constants import *
from music_mapper import MusicMapper

# Funções de manipulação de arquivos
def arquivo(arquivo, modo='r', conteudo=None):
    try:
        if modo == 'r':
            with open(arquivo, 'r') as f: 
                return f.read()
        elif modo == 'w':
            with open(arquivo, 'w') as f: 
                f.write(conteudo)
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

# Funções de manipulação MIDI
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
        
        current_volume = config["volume"]
        current_octave = OITAVA_DEFAULT 
        current_instrumento = config["instrumento"]
        
        mapper = MusicMapper()
        acoes = mapper.mapeamento_da_musica(texto)
        
        for acao in acoes:
            if acao['tipo'] == 'tocar_nota' and acao['nota'] is not None:
                info_temp = type('Info', (), {
                    'current_volume': current_volume,
                    'current_instrumento': current_instrumento
                })()
                gerar_midi(acao, info_temp)
            elif acao['tipo'] == 'alterar_instrumento':
                current_instrumento = acao['instrumento']
            elif acao['tipo'] == 'mudar_volume':
                current_volume = acao['mudar_volume']
            elif acao['tipo'] == 'mudar_oitava':
                current_octave = acao['mudar_oitava']
            elif acao['tipo'] == 'mudar_BPM':
                pass
        
        with open(caminho_arquivo, "wb") as f:
            gerar_midi.midi.writeFile(f)
        print(f"[SUCESSO] Arquivo MIDI salvo em: {caminho_arquivo}")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar MIDI: {e}") 