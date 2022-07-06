import random
import os



'''     Embaralhar hamming'''
def embaralhar(bits):
    """
    
    """
    resultado = ''
    qtd_quadros = len(bits) // 16
    print('quantidade:', qtd_quadros)
    for p in range(qtd_quadros):
        for i in range(16):
            resultado += bits[(i * 16) + p]
    return resultado




def toBits(arquivo, qtd_bytes_por_vez=121):
    '''Converte arquivo para lista de bits e lista de bits para arquivos'''
    str_bytes = ''
    with open('arquivoBits.txt','w') as nArquivo:
        with open(arquivo,'rb') as file:
            while True:
                dado = file.read(1)
                if str(dado) == "b''":
                    break
                # ord do caractere, converte para binário
                byte = format(ord(dado),'b')
                # adiciona zeros no começo para ficar com um tamanho de 8 bits
                byte = ('0' * ( 8 - len(byte))) + byte
                str_bytes += byte
                if len(str_bytes) == qtd_bytes_por_vez * 8:
                    nArquivo.write(str_bytes)
                    str_bytes = ''
            nArquivo.write(str_bytes)



def toFile(listaDeBits, name='newFile'):
    nBits = bytearray()
    for i in listaDeBits:
        nBits.append(int(i,2))
    with open(name,'wb') as file:
        file.write(nBits)




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
    # for bit in range( 11 - ( ( len(string) ) % 11) ):
    #     string = '0' + string
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
                #print(f'quadro {nQuadro} esta corrompido')
            else:
                #print(f'Erro corrigido no quadro {nQuadro}')
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
    # print('erros:',erros)
    # if corrompido:
    #     print('Arquivo corrompido. Impossivel concertar')
    # else:
    #     print('Arquivo concertado com sucesso')
    return decodificada








        


#TESTES
testes = [1,2,4]

toBits('image.jpg', 128)

#codificar arquivo
if 1 in testes:
    toBits('image.jpg')
    praCodificar = ''
    string = ''
    with open('code.txt','w') as file:
        with open('arquivoBits.txt','r') as bits:
            while True:
                dado = bits.read(1)
                if dado == '':
                    break
                string += dado
                if len(string) == 11:
                    file.write(codificar_string(string))
                    string = ''
            #stringFinal = embaralhar(stringFinal)
            file.write(codificar_string(string))

#decodificar arquivo
if 2 in testes:
    with open('decode.txt','w') as arquivo:
        string = ''
        with open('code.txt','r') as file:
            while True:
                dado = file.read(1)
                if dado == '':
                    break
                string += dado
                if len(string) == 16:
                    arquivo.write(decodificar_string(string))
                    string = ''
            arquivo.write(string)
'''
            decoded = file.read()
            #decoded = embaralhar(decoded)
            decoded = decodificar_string(decoded)[5:]
            with open('original.txt','r') as doc:
                original = doc.read()
                print(f'original {len(original)}:',original[:100])
                print(f'decoded  {len(decoded)}:',decoded[:100])
                if original == decoded:
                    print('funcionando...')
                else:
                    print('quebrado...')
                lista = []
                string = ''
                for i in decoded:
                    string += str(i)
                    if len(string) == 8:
                        lista.append(string)
                        string = ''
                toFile(lista,name='novaImagem.jpg')
'''
#testar embaralhamento
if 3 in testes:
    s = ''
    l = 'abcdefghijklmnop'
    for y in range(10):
        for x in l:
            for i in range(16):
                s += x
    print('original:',s)
    emb = embaralhar(s)
    print('emb:',emb)
    print('desem:',embaralhar(emb))



if 4 in testes:
    string = ''
    lista = []
    with open('novaImagem.jpg','wb') as imagem:
        with open('decode.txt','r') as file:
            while True:
                dado = file.read(1)
                if dado == '':
                    break
                string += dado
                if len(string) == 8:
                    lista.append(string)
                    string = ''
                if len(lista) == 10:
                    nBits = bytearray()
                    for i in lista:
                        nBits.append(int(i,2))
                    imagem.write(nBits)
                    lista = []
            if lista != []:
                nBits = bytearray()
                for i in lista:
                    nBits.append(int(i,2))
                imagem.write(nBits)


def main():
    qtd_quadros_por_vez = 64