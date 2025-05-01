#BIBLIOTECAS


#################################################################################
# Inicializações: 
#################################################################################




# CONSTANTES DO PROGRAMA
NOTAS = ['A','B','C','D','E','F','G','H']
"""
Minha ideia é utilizar NOTAS para verificar pausas & silêncio
através do deslocamento, algo como: if (char + deslocamento in NOTAS)
pois, há uma sequencia ASCII entre os dois
"""
DESLOCAMENTO = 26 # tamanho da diferença de a para 'A', verifivar
VOL_MAX = 100 # volume máximo
OITAVA_MAX = 8 # oitava máxima

# TESTES


#################################################################################
# CLASSES:
#################################################################################



#################################################################################
# FUNÇÕES:
#################################################################################

def Is_Pair(numero):
    """
    Verifica se o número é par através da representação binária
    ao invés de fazer a divisão, o que é mais custoso
    """

    return numero & 1 == 0

def Gerar_texto(nome_arquivo = 'Musica.txt'):

    arq_musica = open(nome_arquivo, 'r')

    musica = arq_musica.read()
    arq_musica.close()
    
    print(musica)

Gerar_texto()