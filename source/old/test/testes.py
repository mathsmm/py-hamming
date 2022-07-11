from encodings import utf_8


def paridade(conjunto, bits):
    """
    
    """
    soma = 0
    for bit in conjunto:
        soma += int(bits[bit])
    if soma % 2 == 0:
        return True
    else:
        return False


def criar_quadro(bits_dados):
    """
    Recebe 11 bits de dados, calcula suas paridades e retorna uma lista que representa um quadro de Hamming estendido
    """
    result = list(range(16))
    soma_primeiro_bit = 0
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
            soma_primeiro_bit += 1
            xor_aplicado = xor_aplicado ^ j

        # Incrementa i para acessar a próxima posição do parâmetro bit_dados
        i += 1

    # Passa a variável xor_aplicado para binário, fatia a partir da posição 2 e adiciona zeros à esquerda para completar uma string de tamanho 4
    str_xor_aplicado = bin(xor_aplicado)[2:].zfill(4)

    i = 3
    # Cada k representa um bit de paridade de Hamming na posição 2 ** i
    for k in str_xor_aplicado:
        result[2**i] = k
        soma_primeiro_bit += int(k)
        i -= 1

    # O bit da posição 0 (Hamming estendido) recebe sua devida paridade considerando-se todos os bits ligados até então
    result[0] = str(soma_primeiro_bit % 2)

    return ''.join(result)


def testar_quadro_jose(bits):
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

def testar_quadro(quadro):
    """
    Recebe um quadro de Hamming estendido (16 bits) e retorna:

    --> -1 se o algoritmo não detectar erro;\n
    --> -2 se o algoritmo detectar erro mas não determinar sua posição;\n
    --> a posição do erro em decimal se o algoritmo detectar erro e determinar sua posição.

    LIMITAÇÃO: Se o algoritmo determinar a posição do erro e houver um número ímpar de erros diferente de 1, ele retornará a posição de um suposto erro. Desta forma, posteriormente um algoritmo de correção não poderá reparar o quadro de maneira acertiva!
    """
    soma_primeiro_bit = int(quadro[0])
    posicao_erro = 0

    # Para o próximo laço, não é considerada a posição do primeiro bit do quadro
    for i in range(1, 16):
        # Se o bit na posição i estiver ligado, então:
            # Soma o bit de dado i para posteriormente verificar a paridade do bit da posição 0 do quadro de Hamming estendido;
            # Aplica-se XOR à variável posicao_erro e à posição i do bit ligado.
        # Ao final do laço, a variável posicao_erro terá exatamente a posição do erro detectado em decimal
        if int(quadro[i]):
            soma_primeiro_bit += 1
            posicao_erro = posicao_erro ^ i

    # Se a soma de todos os bits ligados for par, quadro_eh_par recebe True. Caso contrário, recebe False
    quadro_eh_par = True if soma_primeiro_bit % 2 == 0 else False

    # Se posicao_erro for igual a zero, quer dizer que o algoritmo não detectou erro ou detectou mais de um erro que por acaso zeraram a variável por meio de XORs
    if   posicao_erro == 0 and     quadro_eh_par:
        return -1
    elif posicao_erro != 0 and     quadro_eh_par:
        return -2
    elif posicao_erro == 0 and not quadro_eh_par:
        return -2
    else:
        return posicao_erro


def aplicar_xor(lista_posicoes: list):
    """Aplica xor em todos os elementos de uma lista e retorna uma string em binário. Deve receber uma lista de posições de bits ligados.
    """
    # Result recebe o valor da primeira posição da lista de posições
    result = lista_posicoes[0]
    i = 1
    # Passa por cada posição, aplica XOR e armazena em result
    while i < len(lista_posicoes):
        result = result ^ lista_posicoes[i]
        i += 1

    # Passa o resultado para binário, fatia a partir da posição 2 e adiciona zeros à esquerda para completar uma string de tamanho 4
    return bin(result)[2:].zfill(4)

'''    Essa função recebe uma string contendo quadros de hamming 15 - 11. Ela entao separa os quadros e testa um por vez.
       Caso haja erro em algum dos quadros ela tenta resolver o erro.
       Apos analizar todos os quadros a função remove todos os bits de paridade da string e retorna a sequencia original de bits
    antes de ser aplicado o hamming 15 - 11'''
def decodificar_quadro_jose(string):
    teste = testar_quadro(string)
    if teste == -1:
        pass
    elif teste == -2:
        print('quadro corrompido')
    else:
        if string[teste] == '0':
            string = string[:teste] + '1' + string[teste+1:]
        else:
            string = string[:teste] + '0' + string[teste+1:]
    limpo = ''
    for index,cada in enumerate(string):
        if index not in [0,1,2,4,8]:
            limpo += cada
    return limpo

def retornar_quadro_bit_flipado(quadro, posicao):
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

# bytes_as_bits = ''
# bytes = b'\xf0\x0f'
# for byte in bytes:
#     bytes_as_bits = ' '.join(format(byte, '08b'))
#     print(type(format(byte, '08b')))

i = '123456789'
print(i[2:])
print(i[::2])
print(i[:2])