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
    Recebe um quadro de Hamming estendido (16 bits) e retorna:

    * Os bits de dados em string e False se o algoritmo não detectar erro;\n
    * String vazia e False se o algoritmo detectar erro mas não determinar sua posição;\n
    * Os bits de dados em string já corrigidos e True se o algoritmo detectar erro e determinar sua posição.

    - O segundo retorno é do tipo booleano e recebe True se o algoritmo efetuar a correção do quadro.

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
        return ''.join(bits_dados), False

    # Se for detectado 2 ou mais erros, retorna string vazia
    elif (posicao_erro != 0 and quadro_eh_par) or (posicao_erro == 0 and not quadro_eh_par):
        return '', False

    # Se for detectado 1 erro, flipa o bit incorreto e retorna os bits de dados
    else:
        bit_dados = []
        quadro_bit_flipado = retornar_quadro_bit_flipado(quadro, posicao_erro)
        for i in posicoes_bits_dados:
            bit_dados.append(quadro_bit_flipado[i])

        return ''.join(bit_dados), True

def ler_cabecalho(t):
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
    for index, i in enumerate(t):
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

def decodificar_arquivo(caminho_arquivo_codificado: str, caminho_arquivo_recriado='original'):
    """
    Decodifica um arquivo especificado e recria o arquivo original (antes de ser codificado)

    Se decodificar_quadro detectar um quadro corrompido, decodificar_arquivo adiciona 11 bits desligados na conversão para o arquivo original, ao invés dos dados de um quadro corrompido.
    """
    inicio_arquivo = 0
    cabecalho = ''
    with open(caminho_arquivo_codificado, 'r') as arq_codificado:
        cabecalho = arq_codificado.read(3000)

    dados_cabecalho = ler_cabecalho(cabecalho).split('-')
    extensao = dados_cabecalho[0]
    tamanho_arquivo = int(dados_cabecalho[1])
    inicio_arquivo = int(dados_cabecalho[2])

    with open(caminho_arquivo_recriado + '.' + extensao, 'wb') as arq_original:
        with open(caminho_arquivo_codificado,'r') as arq_codificado:
            contador_tamanho = 0
            string_auxiliar = ''
            dados = ''
            efetuou_correcao = False
            contador_quadros_verificados = 0
            contador_quadros_corrigidos = 0
            contador_quadros_corrompidos = 0
            bytesArray = bytearray()
            r = False
            while True:
                byte_dado = arq_codificado.read(8)
                contador_tamanho += len(byte_dado)
                if byte_dado == '':
                    break
                string_auxiliar += byte_dado
                if len(string_auxiliar) == inicio_arquivo and not r:
                    r = True
                    string_auxiliar = ''
                if r:
                    if len(string_auxiliar) == 16:
                        novos_dados, efetuou_correcao = decodificar_quadro(string_auxiliar)
                        contador_quadros_verificados += 1
                        if novos_dados != '' and not efetuou_correcao:
                            dados += novos_dados
                        elif novos_dados != '' and efetuou_correcao:
                            contador_quadros_corrigidos += 1
                            dados += novos_dados
                        else:
                            contador_quadros_corrompidos += 1
                            dados += '00000000000'
                        string_auxiliar = ''
                    if len(dados) >= 8:
                        bytesArray.append(int(dados[:8], 2))
                        dados = dados[8:]
                    if len(bytesArray) >= 10000:
                        arq_original.write(bytesArray)
                        bytesArray = bytearray()

            dados_residuais = dados + string_auxiliar
            bytesArray.append(int(dados_residuais[:8], 2))

            arq_original.write(bytesArray)
            # if len(t) == 8:
            #     bytesArray.append(int('0b' + byte[:8], 2))
            #     arq_original.write(bytesArray)
    diferenca_tamanho = (contador_tamanho - inicio_arquivo) - tamanho_arquivo
    if diferenca_tamanho != 0:
        print('*Foi detectada uma diferença de', diferenca_tamanho, 'bits ao comparar o tamanho do arquivo codificado armazenado em seu cabeçalho e seu atual tamanho. O arquivo pode estar corrompido')

    print("Quantidade de quadros verificados:", contador_quadros_verificados)
    print("Quantidade de quadros corrompidos:", contador_quadros_corrompidos)
    print("Quantidade de quadros corrigidos:", contador_quadros_corrigidos)


def main():
    # Marca o tempo de execução
    import time
    start_time = time.time()

    print()

    decodificar_arquivo(caminho_arquivo_codificado='files\\codificado.bin', caminho_arquivo_recriado='files\\original')

    print("--- Receiver --> Tempo de execução: %s segundos ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()