import os
import random



#   Essa função pega uma string de bits e verifica se a soma é par ou impar.
#   Retorna True se for par e False se for impar
def paridade(conjunto,bits):
    soma = 0
    for bit in conjunto:
        soma += int(bits[bit])
    if soma % 2 == 0:
        return True
    else:
        return False       



#   Essa função recebe uma string com os 11 bits.
#   Coloca todas nas suas posicoes e coloca os bits de paridade como devem ficar
#   A função retorn entao uma string com 16 bits que é o quadro final com hamming
def criar_quadro(bits):
    print('\n'*2)
    
    hamming = ''
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10],
        1:[1,4,8,0,3,6,10],
        2:[2,5,9,0,3,6,10],
        4:[1,2,3,7,8,9,10],
        8:[4,5,6,7,8,9,10]
    }
    
    n = 0
    for bit in range(16):
        if bit in [1,2,4,8]:
            if paridade(checks[bit],bits):
                hamming += '0'
            else:
                hamming += '1'
        elif bit != 0:
            hamming += bits[n]
            n += 1
            
    if paridade(checks[0],bits):
        hamming = '0' + hamming 
    else:
        hamming = '1' + hamming
        
    return hamming




#   Essa função recebe uma string com 16 bits contendo o hamming aplicado e verifica se a algum erro.
#   Ela retorna a posicao do bit com erro se ouver algum
#   Ela retorna -1 se não ouver erro
def testar_quadro(bits):
    erros = []
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        1:[1,5,9,13,3,7,11,15],
        2:[2,6,10,14,3,7,11,15],
        4:[4,5,6,7,12,13,14,15],
        8:[8,9,10,11,12,13,14,15]
    }
    
    for i in checks:
        if i == 0: continue
        if not paridade(checks[i],bits):
            erros.append(checks[i][1:])
    
    if len(erros) > 0:
        posicoes = []
        for conjunto in erros:
            for posicao in conjunto:
                if posicao not in posicoes:
                    posicoes.append(posicao)
        for posicao in posicoes:
            ok = True
            for conjunto in erros:
                if posicao not in conjunto:
                    ok = False
            if ok:
                return posicao
    return -1   





# Essa função recebe um quadro de hamming e a posicao do erro e muda o bit com erro.
# Ela retorn entao uma string com o codigo corrigido
def arrumar_quadro(quadro,posicao):
    certo = ''
    if quadro[posicao] == '0':
        certo = '1'
    else:
        certo = '0'
    correct = quadro[:posicao] + certo + quadro[posicao+1:]
    return correct