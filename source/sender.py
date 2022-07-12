def criar_quadro(bits_dados):
    """
    Recebe 11 bits de dados, calcula suas paridades e retorna uma string que representa um quadro de Hamming estendido
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
    """  1001  """
    for k in str_xor_aplicado:
        result[2**i] = k
        soma_primeiro_bit += int(k)
        i -= 1

    # O bit da posição 0 (Hamming estendido) recebe sua devida paridade considerando-se todos os bits ligados até então
    result[0] = str(soma_primeiro_bit % 2)

    return ''.join(result)

import os

def criar_cabecalho(arquivo):
    cabecalho = ''
    extensao = arquivo.split('.')[1]

    t = os.path.getsize(f"{arquivo}")
    # with open(arquivo, 'rb') as file:
    #     while True:
    #         dado = file.read(1)
    #         if str(dado) == "b''":
    #             break
    #         t += 1

    t *= 8
    resto = t % 11
    final = (t - resto) + ( 5 * (t // 11)) + resto
    extensao += '-'
    extensao += str(final)
    extensao += '-'

    bits_cabecalho = ''
    for i in extensao:
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        bits_cabecalho += b

    chave = 'bcc2022'
    stringC = ''
    for i in chave:
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        stringC += b


    repetir_cabecalho = 10
    tamanho_cabecalho = (len(stringC) * (repetir_cabecalho + 2))
    tamanho_cabecalho += len(bits_cabecalho) * repetir_cabecalho
    tamanho_cabecalho += len(str(tamanho_cabecalho)*8) * repetir_cabecalho


    stringT = ''
    for i in str(tamanho_cabecalho):
        b = format(ord(i),'b')
        b = '0' * ( 8 - len(b)) + b
        stringT += b

    cabecalho += stringC
    for i in range(repetir_cabecalho):
        cabecalho += stringC
        cabecalho += bits_cabecalho
        cabecalho += stringT
    cabecalho += stringC

    return cabecalho

# def codificarArquivo(caminho_arquivo_original: str, caminho_arquivo_codificado='codificado.txt'):
#     """
#     Converte um arquivo qualquer em um arquivo de texto em binário e aplica codificação de Hamming. O arquivo de texto gerado é cerca de 12 vezes maior que o arquivo original
#     """
#     with open(caminho_arquivo_codificado, 'w') as arq_codificado:
#         arq_codificado.write(criar_cabecalho(caminho_arquivo_original))
#         str_bits = ''
#         with open(caminho_arquivo_original, 'rb') as arq_original:
#             while True:
#                 dado = arq_original.read(1)
#                 if str(dado) == "b''":
#                     break
#                 byte = format(ord(dado), 'b')
#                 byte = byte.zfill(8)
#                 str_bits += byte
#                 if len(str_bits) >= 11:
#                     arq_codificado.write(criar_quadro(str_bits[:11]))
#                     str_bits = str_bits[11:]
#             arq_codificado.write(str_bits)

def codificarArquivo(caminho_arquivo_original: str, caminho_arquivo_codificado='codificado.bin'):
    """
    Converte um arquivo qualquer em um arquivo binário e aplica codificação de Hamming.
    """
    with open(caminho_arquivo_codificado, 'wb') as arq_codificado:
        cabecalho = criar_cabecalho(caminho_arquivo_original)
        i = 0
        while True:
            cabecalho_cortado = cabecalho[i:i+8]
            if len(cabecalho_cortado) == 0:
                break
            arq_codificado.write(int(cabecalho_cortado, base=2).to_bytes(1, byteorder='big'))
            i += 8

        bytes_formatados = ''
        with open(caminho_arquivo_original, 'rb') as arq_original:
            while True:
                dado = arq_original.read(1)
                if str(dado) == "b''":
                    break
                byte_formatado = format(ord(dado), '08b')
                # byte = byte.zfill(8)
                bytes_formatados += byte_formatado
                if len(bytes_formatados) >= 11:
                    quadro = criar_quadro(bytes_formatados[:11])
                    arq_codificado.write(int(quadro, base=2).to_bytes(2, byteorder='big'))
                    bytes_formatados = bytes_formatados[11:]

            arq_codificado.write(int(bytes_formatados, base=2).to_bytes(2, byteorder='big'))
            # arq_codificado.write(bytes_formatados)


def main():
    # Marca o tempo de execução
    import time
    start_time = time.time()

    print()

    codificarArquivo(caminho_arquivo_original='files\\image3.jpg', caminho_arquivo_codificado='files\\codificado.bin')

    print("--- Sender --> Tempo de execução: %s segundos ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()