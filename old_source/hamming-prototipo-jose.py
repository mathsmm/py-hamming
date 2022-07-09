import random


# Se o código adicionar ou tirar bits do arquivo original, pode corrompê-lo!

def paridade(posicoes_checagem, sequencia_bits):
    """
    Retorna True caso as posições específicas de uma sequência de bits for par. Caso contrário, retorna False
    """
    soma = 0
    i = 0
    while i < posicoes_checagem:
        soma += int(sequencia_bits[i])
        i += 1

    if soma % 2 == 0:
        return True
    return False

def criar_quadro_16bits(bits_dados):
    """
    Recebe 11 bits de dados, verifica paridades e retorna uma string que representa um quadro de hamming estendido com tamanho de 16 bits.
    """
    result = ''
    posicoes_checagem = {
        0:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 
        1:[1, 4, 8, 0, 3, 6, 10], 
        2:[2, 5, 9, 0, 3, 6, 10], 
        4:[1, 2, 3, 7, 8, 9, 10], 
        8:[4, 5, 6, 7, 8, 9, 10]
    }
    i = 1
    j = 0
    while i < 16:
        if i in [1,2,4,8]:
            if paridade(posicoes_checagem[i], bits_dados):
                result += '0'
            else:
                result += '1'
        else:
            result += bits_dados[j]
            j += 1

    if paridade(posicoes_checagem[0], result):
        result = '0' + result 
    else:
        result = '1' + result

    return result

def testar_quadro_hamming(quadro_hamming: str):
    """
    Recebe uma string que representa um quadro de hamming estendido, com 16 bits de tamanho, e:

    Retorna a posição do bit incorreto se houver somente 1 bit errado;\n
    Retorna -2 se tiver mais de um bit errado;\n
    Retorna -1 se não houver erro.
    """
    posicoes_checagem = {
        0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
        1: [1, 5, 9,  13, 3,  7,  11, 15], 
        2: [2, 6, 10, 14, 3,  7,  11, 15], 
        4: [4, 5, 6,  7,  12, 13, 14, 15], 
        8: [8, 9, 10, 11, 12, 13, 14, 15]
    }

    posicao_erro = 0
    for chave in posicoes_checagem:
        if not paridade(posicoes_checagem[chave], quadro_hamming):
            posicao_erro += chave

    paridade_bit_especial = paridade(posicoes_checagem[0], quadro_hamming)

    if   posicao_erro == 0 and paridade_bit_especial:
        return -1
    elif posicao_erro != 0 and paridade_bit_especial:
        return -2
    elif posicao_erro == 0 and not paridade_bit_especial:
        return -2
    else:
        return posicao_erro

def cortar_string_de_bits_original(string: str):
    resto = len(string) % 11
    if resto == 0:
        return string
    return string[:-resto], string[-resto:]





# DEVE SER APLICADO HAMMING LINHA POR LINHA A PARTIR DO ARQUIVO DE TEXTO!!
# EDER VAI USAR ARQUIVOS MUITO GRANDES PARA SEREM ARMAZENADOS INTEIROS DENTRO DE UMA STRING
'''    Esta função recebe uma string(string) como qualquer quantidade de bits.
       Caso a string não tenha um tamanho divisivel por 11 são adicionados zeros ao fim da string
       Ela divide a string em pedaços de 11 bits para fazer a criação dos quadros. Entao ela cria os
    quadros e após isso ela adiciona o quadro criado a string codificada.
        A função retorna a string codificada com hamming aplicado '''
def codificar_string(string):
    str_codificada = ''
    # for bit in range( 11 - ( ( len(string) ) % 11) ):
        # string = '0' + string
    quadro = ''
    for index,bit in enumerate(string):
        quadro += bit
        if len(quadro) == 11:
            str_codificada += criar_quadro_16bits(quadro)
            quadro = ''
    return str_codificada





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
                print(f'quadro {nQuadro} esta corrompido')
            else:
                print(f'Erro corrigido no quadro {nQuadro}')
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
    print('erros:',erros)
    if corrompido:
        print('Arquivo corrompido. Impossivel concertar')
    else:
        print('Arquivo concertado com sucesso')
    return decodificada
        





#TESTES
testes = [2]


#gerar string com hamming apartir de uma string e salvar em um arquivo
if 1 in testes:
    bits = ''
    a = "fseiufhseuhf"
    for x in a:
        bits += format(ord(x), 'b')
    with open('original.txt','w') as file:
        file.write(bits)
    stringFinal = codificar_string(bits)
    for index,s in enumerate(stringFinal):
        print(s,end='\t')
        if ( index + 1 ) % 4 == 0:
            print()
        if ( index + 1 ) % 16 == 0:
            print()
            print()
    with open('code.txt','w') as file:
        file.write(stringFinal)


#testar decodificação de arquivo
if 2 in testes:
    with open('code.txt','r') as file:
        decoded = decodificar_string(file.read())
        with open('original.txt','r') as doc:
            original = doc.read()
            filler = 0
            for index,i in enumerate(decoded):
                if i == '1':
                    filler = index
                    break
            decoded = decoded[index:]
            print('original:',original)
            print('decoded :',decoded)
            if original == decoded:
                print('funcionando...')
            else:
                print('quebrado...')






