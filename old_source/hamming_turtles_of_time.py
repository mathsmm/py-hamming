def criar_cabecalho(arquivo):
    cabecalho = ''
    extensao = arquivo.split('.')[1]

    t = 0
    with open(arquivo,'rb') as file:
        while True:
            dado = file.read(1)
            if str(dado) == "b''":
                break
            t += 1
    t *= 8
    resto = t % 11
    final = (t - resto) + ( 5 * (t // 11)) + resto
    extensao += '-'
    extensao += str(final)
    extensao += '-'
    
    bitsCabecalho = ''
    for i in extensao:
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        bitsCabecalho += b

    chave = 'bcc2022'
    stringC = ''
    for i in chave:
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        stringC += b


    repetirCabecalho = 10
    tamanhoCabecalho = (len(stringC) * (repetirCabecalho + 2))
    tamanhoCabecalho += len(bitsCabecalho) * repetirCabecalho
    tamanhoCabecalho += len(str(tamanhoCabecalho)*8) * repetirCabecalho


    stringT = ''
    for i in str(tamanhoCabecalho):
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        stringT += b

    cabecalho += stringC
    for i in range(repetirCabecalho):
        cabecalho += stringC
        cabecalho += bitsCabecalho
        cabecalho += stringT
    cabecalho += stringC

    return cabecalho


def lerCabecalho(t):
    chave = 'bcc2022'
    stringC = ''
    for i in chave:
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        stringC += b
    cabecalhos = []    
    f = ''
    data = ''
    on = False
    for index,i in enumerate(t):
        f += i
        if len(f) > len(stringC):
            f = f[1:]
        if not on:
            data += i
        if f == stringC:
            if not on:
                on = False
                bits = ''
                dados = ''
                for cada in data:
                    bits += cada
                    if len(bits) == 8:
                        dados += chr(int(bits,2))
                        bits = ''
                data = ''
                final = dados[:len(dados) - len(chave)]
                if final != '':
                    cabecalhos.append(final)
            else:
                on = True
    certo = ''
    for ix,x in enumerate(cabecalhos):
        for iy,y in enumerate(cabecalhos):
            if x == y and ix != iy:
                certo = x
    return certo


'''     Embaralhar hamming'''
def embaralhar(bits):
    resultado = ''
    qtd_quadros = len(bits) // 16
    print('quantidade:', qtd_quadros)
    for p in range(qtd_quadros):
        for i in range(16):
            resultado += bits[(i * 16) + p]
    return resultado



# '''   Essa função recebe uma string(bits) com os 11 bits para aplicar hamming.
#       Coloca as paridades nas posicoes que devem ficar e faz o calculo de paridade para escolher
#     o numero da paridade.
#       A função retorna uma string com 16 bits que é o quadro final com hamming 15 - 11 '''
# def criar_quadro(bits):
#     hamming = ''
#     checks = {
#         0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
#         1:[1,4,8,0,3,6,10],
#         2:[2,5,9,0,3,6,10],
#         4:[1,2,3,7,8,9,10],
#         8:[4,5,6,7,8,9,10]
#     }
#     n = 0
#     for bit in range(16):
#         if bit in [1,2,4,8]:
#             if paridade(checks[bit],bits):
#                 hamming += '0'
#             else:
#                 hamming += '1'
#         elif bit != 0:
#             hamming += bits[n]
#             n += 1       
#     if paridade(checks[0],hamming):
#         hamming = '0' + hamming 
#     else:
#         hamming = '1' + hamming
#     return hamming

def criar_quadro(bits_dados):
    """
    Recebe 11 bits de dados, calcula suas paridades e retorna uma lista que representa um quadro de Hamming estendido
    """
    result = list(range(16))
    soma_bit_hamm_estendido = 0
    i = 0
    xor_aplicado = 0
    # As posições j consideradas no laço são as posições dos bits de dados num quadro de Hamming já montado
    for j in [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:
        # Armazena o bit de dado i em sua devida posição no quadro de Hamming
        result[j] = bits_dados[i]

        # Se o bit na posição i estiver ligado, então:
            # Soma o bit de dado i para posteriormente verificar a paridade do bit da posição 0 do quadro de Hamming estendido;
            # Aplica-se XOR considerando sua posição num quadro já montado.
        # Ao final do laço, xor_aplicado terá exatamente os bits de paridade de Hamming que devem estar ligados, porém em base decimal
        if int(bits_dados[i]):
            soma_bit_hamm_estendido += 1
            xor_aplicado = xor_aplicado ^ j

        # Incrementa i para acessar a próxima posição do parâmetro bit_dados
        i += 1

    # Passa a variável xor_aplicado para binário, fatia a partir da posição 2 e adiciona zeros à esquerda para completar uma string de tamanho 4
    str_xor_aplicado = bin(xor_aplicado)[2:].zfill(4)

    i = 3
    # Cada k representa um bit de paridade de Hamming na posição 2 ** i
    for k in str_xor_aplicado:
        result[2**i] = k
        soma_bit_hamm_estendido += int(k)
        i -= 1

    # O bit da posição 0 (Hamming estendido) recebe sua devida paridade considerando-se todos os bits ligados até então
    result[0] = str(soma_bit_hamm_estendido % 2)

    return ''.join(result)




# '''   Essa função recebe uma string(bits) com 16 bits contendo hamming e verifica se a algum erro.
#       Ela retorna a posicao do bit com erro se houver 1 erro
#       Ela retorna -2 se tiver mais de um erro
#       Ela retorna -1 se não houver erro '''
# def testar_quadro(bits):
#     erro = 0
#     checks = {
#         0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
#         1:[1,5,9,13,3,7,11,15],
#         2:[2,6,10,14,3,7,11,15],
#         4:[4,5,6,7,12,13,14,15],
#         8:[8,9,10,11,12,13,14,15]
#     }    
#     for grupo in checks:
#         if grupo == 0: continue
#         if not paridade(checks[grupo],bits):
#             erro += grupo
#     if erro == 0:
#         return -1
#     elif erro != 0 and paridade(checks[0],bits):
#         return -2
#     else:
#         return erro

# def testar_quadro(quadro):
#     """
#     Recebe um quadro de Hamming estendido (16 bits) e retorna:

#     --> -1 se o algoritmo não detectar erro;\n
#     --> -2 se o algoritmo detectar erro mas não determinar sua posição;\n
#     --> a posição do erro em decimal se o algoritmo detectar erro e determinar sua posição.

#     LIMITAÇÃO: Se o algoritmo determinar a posição do erro e houver um número ímpar de erros diferente de 1, ele retornará a posição de um suposto erro. Desta forma, posteriormente um algoritmo de correção não poderá reparar o quadro de maneira acertiva!
#     """
#     soma_bit_hamm_estendido = int(quadro[0])
#     posicao_erro = 0

#     # Para o próximo laço, não é considerada a posição do primeiro bit do quadro
#     for i in range(1, 16):
#         # Se o bit na posição i estiver ligado, então:
#             # Soma o bit de dado i para posteriormente verificar a paridade do bit da posição 0 do quadro de Hamming estendido;
#             # Aplica-se XOR à variável posicao_erro e à posição i do bit ligado.
#         # Ao final do laço, a variável posicao_erro terá exatamente a posição do erro detectado em decimal
#         if int(quadro[i]):
#             soma_bit_hamm_estendido += 1
#             posicao_erro = posicao_erro ^ i

#     # Se a soma de todos os bits ligados for par, quadro_eh_par recebe True. Caso contrário, recebe False
#     quadro_eh_par = True if soma_bit_hamm_estendido % 2 == 0 else False

#     # Se posicao_erro for igual a zero, quer dizer que o algoritmo não detectou erro ou detectou mais de um erro que por acaso zeraram a variável por meio de XORs
#     if   posicao_erro == 0 and     quadro_eh_par:
#         return -1
#     elif posicao_erro != 0 and     quadro_eh_par:
#         return -2
#     elif posicao_erro == 0 and not quadro_eh_par:
#         return -2
#     else:
#         return posicao_erro

# '''    Essa função recebe uma string contendo quadros de hamming 15 - 11. Ela entao separa os quadros e testa um por vez.
#        Caso haja erro em algum dos quadros ela tenta resolver o erro.
#        Apos analizar todos os quadros a função remove todos os bits de paridade da string e retorna a sequencia original de bits
#     antes de ser aplicado o hamming 15 - 11'''
# def decodificar_quadro(string):
#     teste = testar_quadro(string)
#     if teste == -1:
#         pass
#     elif teste == -2:
#         print('quadro corrompido')
#     else:
#         if string[teste] == '0':
#             string = string[:teste] + '1' + string[teste+1:]
#         else:
#             string = string[:teste] + '0' + string[teste+1:]
#     limpo = ''
#     for index,cada in enumerate(string):
#         if index not in [0,1,2,4,8]:
#             limpo += cada
#     return limpo

def retornar_quadro_bit_flipado(quadro, posicao):
    """
    Recebe um quadro de Hamming estendido e retorna uma lista igual ao quadro, porém com o bit na posição especificada flipado
    """
    result = list(quadro)
    if quadro[posicao] == '1':
        result[posicao] = '0'
    else:
        result[posicao] = '1'

    return result

def decodificar_quadro(quadro):
    """
    Recebe um quadro de Hamming estendido (16 bits) e retorna, em string:

    --> Os bits de dados se o algoritmo não detectar erro;\n
    --> Vazio se o algoritmo detectar erro mas não determinar sua posição;\n
    --> Os bits de dados já corrigidos se o algoritmo detectar erro e determinar sua posição.

    LIMITAÇÃO: Se o algoritmo determinar a posição do erro e houver um número ímpar de erros diferente de 1, ele retornará os bits de dados corrigidos por uma suposta posição de erro. Desta forma, ele retorna os bits de dados corrigidos de uma maneira não acertiva!
    """
    posicoes_bits_dados = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
    bits_dados = []
    soma_primeiro_bit = int(quadro[0])
    posicao_erro = 0

    # Para o próximo laço, não é considerada a posição do primeiro bit do quadro
    for i in range(1, 16):
        if i in posicoes_bits_dados:
            bits_dados.append(quadro[i])

        # Se o bit na posição i estiver ligado, então:
            # Soma o bit de dado i para posteriormente verificar a paridade do bit da posição 0 do quadro de Hamming estendido;
            # Aplica-se XOR à variável posicao_erro e à posição i do bit ligado.
        # Ao final do laço, a variável posicao_erro terá exatamente a posição do erro detectado em decimal
        if int(quadro[i]):
            soma_primeiro_bit += 1
            posicao_erro = posicao_erro ^ i

    # Se a soma de todos os bits ligados for par, quadro_eh_par recebe True. Caso contrário, quadro_eh_par recebe False
    quadro_eh_par = True if soma_primeiro_bit % 2 == 0 else False

    # Se não for detectado erro, retorna os bits de dados
    if   posicao_erro == 0 and quadro_eh_par:
        return ''.join(bits_dados)

    # Se for detectado 2 ou mais erros, retorna string vazia
    elif (posicao_erro != 0 and quadro_eh_par) or (posicao_erro == 0 and not quadro_eh_par):
        return ''

    # Se for detectado 1 erro, flipa o bit incorreto e retorna os bits de dados
    else:
        bit_dados = []
        quadro_bit_flipado = retornar_quadro_bit_flipado(quadro, posicao_erro)
        for i in posicoes_bits_dados:
            bit_dados.append(quadro_bit_flipado[i])

        return ''.join(bit_dados)





'''    Essa funcao recebe o nome do arquivo para codificar o nome do arquivo que sera o resultado da codificaçao'''
def codificarArquivo(arquivo, novo_arquivo):
    with open(novo_arquivo, 'w') as arq_codificado:
        arq_codificado.write(criar_cabecalho(arquivo))
        str_bits = ''
        with open(arquivo, 'rb') as arq_normal:
            while True:
                dado = arq_normal.read(1)
                if str(dado) == "b''":
                    break
                byte = format(ord(dado), 'b')
                # byte = ('0' * ( 8 - len(byte))) + byte
                byte = byte.zfill(8)
                str_bits += byte
                if len(str_bits) >= 11:
                    arq_codificado.write(criar_quadro(str_bits[:11]))
                    str_bits = str_bits[11:]
            arq_codificado.write(str_bits)




'''     Essa função recebe o nome do arquivo para decodificar e retorna o nome do arquivo final que será recriado apos a codificaçao'''
def decodificarArquivo(arquivo,nome = 'arquivoDecodificado'):
    inicioArquivo = 0
    cabecalho = ''
    with open(arquivo,'r') as file:
        while True:
            cabecalho += file.read(1)
            if len(cabecalho) > 3000:
                break
    
    dadosCabecalho = lerCabecalho(cabecalho).split('-')
    extensao = dadosCabecalho[0]
    tamanhoDoArquivo = int(dadosCabecalho[1])
    inicioArquivo = int(dadosCabecalho[2])

    contagem = 0
    with open(arquivo,'r') as file:
        while True:
            dado = file.read(1)
            if dado == '':
                break
            contagem += 1
    if tamanhoDoArquivo != contagem-inicioArquivo:
        print('foram adicionados ou retirados bits. Arquivo corrompido')   
        return 

    bytesArray = bytearray()
    byte = ''
    r = False
    with open( nome + '.' + extensao,'wb') as imagem:
        string = ''
        contador_quadros_corrompidos = 0
        with open(arquivo,'r') as file:
            while True:
                dado = file.read(1)
                if dado == '':
                    break
                string += dado
                if len(string) == inicioArquivo and not r:
                    r = True
                    string = ''
                if r:
                    if len(string) == 16:
                        novos_dados = decodificar_quadro(string)
                        if novos_dados != '':
                            byte += novos_dados
                        else:
                            contador_quadros_corrompidos += 1
                            byte += '00000000000'
                        string = ''
                    if len(byte) >= 8:
                        bytesArray.append(int(byte[:8],2))
                        byte = byte[8:]
                    if len(bytesArray) >= 100:
                        imagem.write(bytesArray)
                        bytesArray = bytearray()

            if len(bytesArray) > 0:
                imagem.write(bytesArray)
            t = byte + string
            if len(t) == 8:
                bytesArray.append(int(byte[:8],2))
                imagem.write(bytesArray)
    print("Quantidade de quadros corrompidos:", contador_quadros_corrompidos)



#TESTES

#codificar arquivo e salvar codificaçao em outro arquivo
if 1:
    codificarArquivo(arquivo='image.jpg',novo_arquivo='encoded.txt')


#decodificar arquivo codificado e remontar o arquivo original
if 1:
    decodificarArquivo(arquivo='encoded.txt')
