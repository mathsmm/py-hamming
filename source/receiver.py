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


'''     Essa função recebe o nome do arquivo para decodificar e retorna o nome do arquivo final que será recriado apos a codificaçao'''
def decodificarArquivo(arquivo, novo_arquivo='original'):
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
    with open( novo_arquivo + '.' + extensao,'wb') as imagem:
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


def main():
    # Marca o tempo de execução
    import time
    start_time = time.time()

    decodificarArquivo(arquivo='files\\encoded.txt', novo_arquivo='files\\original')

    print("--- Tempo de execução: %s segundos ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()