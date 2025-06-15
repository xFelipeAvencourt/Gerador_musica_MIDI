#BIBLIOTECAS
import pygame
import time
import random

#################################################################################
# Inicializações: 
#################################################################################

# CONSTANTES DE INICIALIZAÇÃO:
VOL_DEFAULT = 10
OITAVA_DEFAULT = 4
BPM_DEFAULT = 60
NUM_ACOES = 3
LARGURA_COLUNA = 25

# CONSTANTES DO PROGRAMA
NOTAS = ['A','B','C','D','E','F','G']
LET_VOGAL = ['I','O','U'] # Vogais especiais
AUMENTA_OITAVA = ['.'] # caracteres que aumentam a oitava
NL = 10 # Nova linha
SPACE = ' '
PLUS = '+' # Dobrar o volume
MINUS = '-' # SETAR Volume inicial
VOL_MAX = 100 
OITAVA_MAX = 8
BPM_MAX = 240
uBPM = 80 # unidades BPM



#INSTRUMENTOS MIDI
PIANO = 0 
BANDONEON = '!' # 24 MID
AGOGE = ',' # 114 MID
TEL_TOCANDO = 125 # TEL TOCANDO MID


# TESTES


#################################################################################
# CLASSES:
#################################################################################

class MusicMapper:
    def __init__(self):
        self.instrumentos = PIANO  # instrumento padrão (piano)
        self.oitava = OITAVA_DEFAULT
        self.volume = VOL_DEFAULT
        self.current_octave = OITAVA_DEFAULT
        self.current_instrumento = PIANO  # instrumento padrão (piano)
        self.last_char = None
        self.BPM = BPM_DEFAULT


        # Mapeamento de letras maiúsculas para notas (A-H)
        self.NOTAS = {
            'A': 'A',
            'B': 'B',
            'C': 'C',
            'D': 'D',
            'E': 'E',
            'F': 'F',
            'G': 'G'
        }

        # instrumentos MIDI pré-definidos
        self.instrumentos = {
            0: PIANO,
            '!': 24,       # Bandoneon
            ',': 114       # Agogê
        }

    def mapeamentoDaMusica(self, text):
        """Mapeia um caractere para uma lista de ações musicais."""
        executar = []
        i = 0
        length = len(text)
        
        while i < length:
            char = text[i]
            acao = {
                'tipo': None,
                'nota': None,
                'instrumento': None,
                'mudar_volume': None,
                'mudar_oitava': None,
                'mudar_BPM': None
            }

            # Verificar BPM+
            if char == 'B' and i + 3 < length and text[i:i+4] == 'BPM+':
                acao['tipo'] = 'mudar_bpm'
                acao['mudar_BPM'] = min(self.BPM + uBPM, BPM_MAX)
                i += 3  # Pula os 3 caracteres ('BPM+') + o padrao (no final)

            # A-G ou a-g viram notas
            elif char in self.NOTAS or char.upper() in self.NOTAS:
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = self.NOTAS[char.upper()] + str(self.current_octave)
            
            # ESPAÇO: PAUSA/SILÊNCIO
            elif char == SPACE:
                acao['tipo'] = 'pausa'

            # MAIS: Dobra o volume
            elif char == PLUS:
                acao['tipo'] = 'mudar_volume'
                acao['mudar_volume'] = min(self.volume * 2, VOL_MAX)
                
            # Menos: Voltar ao volume Default
            elif char == MINUS:
                acao['tipo'] = 'mudar_volume'
                acao['mudar_volume'] = VOL_DEFAULT

            # i,I,o,O,u,U: se caractere anterior era nota, repete; else tel_tocando (125)
            elif char in LET_VOGAL or char.upper() in LET_VOGAL:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + str(self.current_octave)
                else:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = TEL_TOCANDO
            
            # R+ ou R-: Aumenta ou Diminui uma oitava
            elif char == 'R' and i + 1 < length:
                next_char = text[i + 1]
                if next_char == '+':    
                    acao['tipo'] = 'mudar_oitava'
                    acao['mudar_oitava'] = min(self.current_octave + 1, OITAVA_MAX)
                    i += 1
                
                elif next_char == '-':
                    acao['tipo'] = 'mudar_oitava'
                    acao['mudar_oitava'] = max(self.current_octave - 1, 0)
                    i += 1

            # '?': Toca uma nota aleatória (A-G)
            elif char == '?':
                random_nota = random.choice(list(self.NOTAS.values()))
                random_oitava = random.randint(1, 7)
                acao['tipo'] = 'tocar_nota'
                acao['nota'] = random_nota + str(random_oitava)
            
            # ';': Atribui um BPM aleatório
            elif char == ';':
                acao['tipo'] = 'mudar_bpm'
                acao['mudar_BPM'] = random.randint(BPM_DEFAULT, BPM_MAX)
                
            # '\n': Próximo instrumento
            elif char == NL:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = random.choice(list(self.instrumentos.values()))

            # '!' troca para Bandoneon
            elif char == BANDONEON:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = self.instrumentos['!']

            # Dígitos pares alteram o instrumento (current_instrumento + digito)
            elif char.isdigit() and Is_even(int(char)):
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = (self.current_instrumento + int(char)) % len(self.instrumentos)
            
            # ',' troca para Agogê
            elif char == AGOGE:
                acao['tipo'] = 'alterar_instrumento'
                acao['instrumento'] = self.instrumentos[',']

            # Outros caracteres: repete a nota anterior ou pausa
            else:
                if self.last_char and self.last_char.upper() in self.NOTAS:
                    acao['tipo'] = 'tocar_nota'
                    acao['nota'] = self.NOTAS[self.last_char.upper()] + str(self.current_octave)
                else:
                    acao['tipo'] = 'pausa'

            executar.append(acao)            
            self.last_char = text[i]
            i += 1

        return executar

        

class TextToMusicConverter:
    def __init__(self):
        pygame.mixer.init()
        self.music_mapper = MusicMapper()
        self.bpm = BPM_DEFAULT
        self.MID_exe = None

    def _pausa(self):
        print("Pausa")

    def ConverterMusica(self, text):
        self.MID_exe = self.music_mapper.mapeamentoDaMusica(text)
        string_acoes = gerar_string_acoes(self.MID_exe)
        Arquivo('MID_gerado.txt', 'w', string_acoes)
        print("Musica convertida com sucesso!\n\n")
        
    def Play_MID(self):

        for action in self.MID_exe:
            if action['tipo'] == 'tocar_nota':
                self._tocar_nota(action['nota'])
            elif action['tipo'] == 'pausa':
                self._pausa()
            elif action['tipo'] == 'alterar_instrumento':
                self.music_mapper.current_instrumento = action['instrumento']
            elif action['tipo'] == 'mudar_volume':
                self.music_mapper.volume = action['mudar_volume']
            elif action['tipo'] == 'mudar_oitava':
                self.music_mapper.current_octave = action['mudar_oitava']
            elif action['tipo'] == 'mudar_BPM':
                self.bpm = action['bpm']
            time.sleep(60 / self.bpm)
        

    def _tocar_nota(self, nota: str):
        instrumento_numero = self.music_mapper.current_instrumento
        instrumento_nome = "Desconhecido"
        
        for nome, numero in self.music_mapper.instrumentos.items():
            if numero == instrumento_numero:
                instrumento_nome = nome
                break
        
        output = (
            f"Tocando [{nota}] no instrumento [{instrumento_nome} "
            f"(ID: {instrumento_numero})]"
        )
        
        print(output)


# INFORMAÇOES DA MUSICA: TALVEZ??? Não especificado
class Info_Musica:
    def __init__(self, nome='', autor='', ano=0, genero='', arquivo=''):
        self.nome = nome
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.arquivo = arquivo

    def LerMusica(self):
        try:
            with open(self.arquivo, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Arquivo {self.arquivo} não encontrado.")
            return None


#################################################################################
# FUNÇÕES:
#################################################################################

def Is_even(numero):
    """
    Verifica se o número é par através da representação binária
    ao invés de fazer a divisão - mais custoso -
    """

    return numero & 1 == 0

def Arquivo(arquivo, modo='r', conteudo=None):
    try:
        if modo == 'r':
            with open(arquivo, 'r') as file:
                print("Arquivo lido com sucesso!")
                return file.read()
        elif modo == 'w':
            if conteudo is None:
                raise ValueError("Conteúdo não fornecido para escrita.")
            with open(arquivo, 'w') as file:
                file.write(conteudo)
                print("Arquivo escrito com sucesso!")
        else:
            raise ValueError("Modo inválido. Use 'r' para leitura ou 'w' para escrita.")
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao manipular o arquivo: {e}")
        return None
    
def gerar_string_acoes(music_actions):
    chaves = ['nota', 'instrumento', 'mudar_volume', 'mudar_oitava', 'mudar_BPM']
    
    grupos = [music_actions[i:i+3] for i in range(0, len(music_actions), 3)]
    
    linhas = []
    for grupo in grupos:
        partes = []
        for acao in grupo:
            texto = f"{acao['tipo']}:{next((acao.get(k, '') for k in chaves if k in acao), '')}".rstrip(':')
            partes.append(f"{texto.ljust(LARGURA_COLUNA)}")
        linhas.append(" | ".join(partes))
    
    return "\n".join(linhas)

#input_file = input("Digite o nome do arquivo: ")
print("LENDO O ARQUIVO:")
Musica_Text = Arquivo('Exorcista.txt')

print("Convertendo musica!")
Musica = TextToMusicConverter()
Musica.ConverterMusica(Musica_Text)
Musica.Play_MID()
