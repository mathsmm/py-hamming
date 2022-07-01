import random




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
    erros = []
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
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






'''     Essa função recebe um quadro de hamming 15-11 e a posicao do erro e muda o bit com erro.
        Ela retorna entao uma string com o codigo corrigido '''
def arrumar_quadro(quadro,posicao):
    certo = ''
    if quadro[posicao] == '0':
        certo = '1'
    else:
        certo = '0'
    correct = quadro[:posicao] + certo + quadro[posicao+1:]
    return correct






'''    Esta função recebe uma string(string) como qualquer quantidade de bits.
       Caso a string não tenha um tamanho divisivel por 11 são adicionados zeros ao fim da string
       Ela divide a string em pedaços de 11 bits para fazer a criação dos quadros. Entao ela cria os
    quadros e após isso ela adiciona o quadro criado a string codificada.
        A função retorna a string codificada com hamming aplicado '''
def codificar_string(string):
    codificada = ''
    for bit in range( 11 - ( ( len(string) ) % 11) ):
        string = '0' + string
    quadro = ''
    for index,bit in enumerate(string):
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
    for caractere in string:
        quadro += caractere
        if len( quadro ) == 16:
            teste = testar_quadro(quadro)
            if teste == -1:
                pass
            elif teste == -2:
                print('impossivel corrigir')
                erros += 1
            else:
                erros += 1
                quadro = arrumar_quadro(quadro,teste)
            limpo = ''
            for index,cada in enumerate(quadro):
                if index not in [0,1,2,4,8]:
                    limpo += cada
            decodificada += limpo
            quadro = ''
    print('erros:',erros)
    return decodificada
        





#TESTES
teste1 = 0
teste2 = 1


#gerar string com hamming apartir de uma string e salvar em um arquivo
if teste1:
    bits = ''
    a = "abcjwaoidjaowjdoawijdawahdahfiueshfihseifuh"
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
if teste2:
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






