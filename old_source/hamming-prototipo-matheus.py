import math



"""
posicoes = {
    0: ["todos os bits. Fazer checagem na hora com todos"],
    2**0:
}
"""
def retornar_qtd_checagens(tamanho_quadro):
    return math.log(tamanho_quadro, 2)

def retornar_lista_posicoes_bits_ligados(sequencia_bits):
    """Recebe uma sequência de bits e retorna, em lista, a posição de cada bit ligado (1)
    """
    lista_posicoes_bits_ligados = []
    i = 0
    while i < len(sequencia_bits):
        # Se o bit estiver ligado, a posição dele é gravada
        if sequencia_bits[i]:
           lista_posicoes_bits_ligados.append(i)
        i += 1

    return lista_posicoes_bits_ligados

def aplicar_xor(lista_posicoes: list):
    """Aplica xor em todos os elementos de uma lista e retorna o resultado. Deve receber uma lista de posições de bits ligados.
    """
    result = lista_posicoes[0]
    i = 1
    # Passa por cada posição, aplica xor e armazena em result
    while i < len(lista_posicoes):
        result = result ^ lista_posicoes[i]
        i += 1

    return result

def cortar_string_de_bits_original(string: str):
    resto = len(string) % 11
    if resto == 0:
        return string
    return string[:-resto], string[-resto:]

def retornar_quadro_corrigido():

# print(aplicar_xor(retornar_lista_posicoes_bits_ligados([1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0])))



