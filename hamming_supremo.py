import random
import os



'''     Embaralhar hamming'''
def embaralhar(bits):
    resultado = ''
    qtd_quadros = len(bits) // 16
    print('quantidade:', qtd_quadros)
    for p in range(qtd_quadros):
        for i in range(16):
            resultado += bits[(i * 16) + p]
    return resultado






'''     Essa função pega uma string de bits e verifica se a soma dos bits é par ou impar.
        Para isso ela recebe um lista(conjunto) com posicoes e uma string(bits) com os bits. Entao ela usa as
    posicoes da lista para pegar o numero na string para fazer o calculo
        Retorna True se for par e False se for impar '''
def paridade(conjunto,bits):
    soma = 0
    for bit in conjunto:
        soma += int(bits[bit])
    if soma % 2 == 0:
        return True
    else:
        return False
    




'''   Essa função recebe uma string(bits) com os 11 bits para aplicar hamming.
      Coloca as paridades nas posicoes que devem ficar e faz o calculo de paridade para escolher
    o numero da paridade.
      A função retorna uma string com 16 bits que é o quadro final com hamming 15 - 11 '''
def criar_quadro(bits):
    hamming = ''
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
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
    if paridade(checks[0],hamming):
        hamming = '0' + hamming 
    else:
        hamming = '1' + hamming
    return hamming






'''   Essa função recebe uma string(bits) com 16 bits contendo hamming e verifica se a algum erro.
      Ela retorna a posicao do bit com erro se houver 1 erro
      Ela retorna -2 se tiver mais de um erro
      Ela retorna -1 se não houver erro '''
def testar_quadro(bits):
    erro = 0
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        1:[1,5,9,13,3,7,11,15],
        2:[2,6,10,14,3,7,11,15],
        4:[4,5,6,7,12,13,14,15],
        8:[8,9,10,11,12,13,14,15]
    }    
    for grupo in checks:
        if grupo == 0: continue
        if not paridade(checks[grupo],bits):
            erro += grupo
    if erro == 0:
        return -1
    elif erro != 0 and paridade(checks[0],bits):
        return -2
    else:
        return erro






'''    Esta função recebe uma string(string) como qualquer quantidade de bits.
       Caso a string não tenha um tamanho divisivel por 11 são adicionados zeros ao fim da string
       Ela divide a string em pedaços de 11 bits para fazer a criação dos quadros. Entao ela cria os
    quadros e após isso ela adiciona o quadro criado a string codificada.
        A função retorna a string codificada com hamming aplicado '''
def codificar_string(string):
    codificada = ''
    quadro = ''
    for index, bit in enumerate(string):
        quadro += bit
        if len(quadro) == 11:
            codificada += criar_quadro(quadro)
            quadro = ''
    return codificada





'''    Essa função recebe uma string contendo quadros de hamming 15 - 11. Ela entao separa os quadros e testa um por vez.
       Caso haja erro em algum dos quadros ela tenta resolver o erro.
       Apos analizar todos os quadros a função remove todos os bits de paridade da string e retorna a sequencia original de bits
    antes de ser aplicado o hamming 15 - 11'''
def decodificar_string(string):
    decodificada = ''
    quadro = ''
    erros = 0
    corrompido = False
    nQuadro = 0
    for caractere in string:
        quadro += caractere
        if len( quadro ) == 16:
            nQuadro += 1
            teste = testar_quadro(quadro)
            if teste == -1:
                pass
            elif teste == -2:
                corrompido = True
                erros += 2
            else:
                erros += 1
                if quadro[teste] == '0':
                    quadro = quadro[:teste] + '1' + quadro[teste+1:]
                else:
                    quadro = quadro[:teste] + '0' + quadro[teste+1:]
            limpo = ''
            for index,cada in enumerate(quadro):
                if index not in [0,1,2,4,8]:
                    limpo += cada
            decodificada += limpo
            quadro = ''
    return decodificada





'''    Essa funcao recebe o nome do arquivo para codificar o nome do arquivo que sera o resultado da codificaçao'''
def codificarArquivo(arquivo,novoArquivo):
    with open(novoArquivo,'w') as coded:
        str_bytes = ''
        with open(arquivo,'rb') as file:
            while True:
                dado = file.read(1)
                if str(dado) == "b''":
                    break
                byte = format(ord(dado),'b')
                byte = ('0' * ( 8 - len(byte))) + byte
                str_bytes += byte
                if len(str_bytes) >= 11:
                    coded.write(codificar_string(str_bytes[:11]))
                    str_bytes = str_bytes[11:]
            coded.write(str_bytes)





'''     Essa função recebe o nome do arquivo para decodificar e retorna o nome do arquivo final que será recriado apos a codificaçao'''
def decodificarArquivo(arquivo,novoArquivo):
    bytesArray = bytearray()
    byte = ''
    with open(novoArquivo,'wb') as imagem:
        string = ''
        with open(arquivo,'r') as file:
            while True:
                dado = file.read(1)
                if dado == '':
                    break
                string += dado
                if len(string) == 16:
                    byte += decodificar_string(string)
                    string = ''
                if len(byte) >= 8:
                    bytesArray.append(int(byte[:8],2))
                    byte = byte[8:]
                if len(bytesArray) >= 100:
                    imagem.write(bytesArray)
                    bytesArray = bytearray()
            if len(bytesArray) > 0:
                imagem.write(bytesArray)








#TESTES                
testes = [1,2]

#codificar arquivo e salvar codificaçao em outro arquivo
if 1 in testes:
    codificarArquivo(arquivo='image.jpg',novoArquivo='code.txt')


#decodificar arquivo codificado e remontar o arquivo original
if 2 in testes:
    decodificarArquivo(arquivo='code.txt',novoArquivo='novaImagem.jpg')

