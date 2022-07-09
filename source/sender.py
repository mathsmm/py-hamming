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


def main():
    # Marca o tempo de execução
    import time
    start_time = time.time()

    codificarArquivo(arquivo='files\\image1.jpg', novo_arquivo='files\\encoded.txt')

    print("--- Tempo de execução: %s segundos ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()