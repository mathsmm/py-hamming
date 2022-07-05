import random


# Comentários do Matheus com "#"


# Verificar solução matemática para os bits de checagem serem 
# aplicados em qualquer tamanho de quadro!
# Isto vale para a criação e verificação de quadros!

# checks = {
#         (todos (range(tamanho_quadro)))
#         0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],

#         (começa do 1, +4 quatro vezes, -4 a partir do 15, quatro vezes)
#         1:[1,5,9,13,3,7,11,15],

#         (começa do 2, + 4 quatro vezes, -4 a partir do 15, quatro vezes)
#         2:[2,6,10,14,3,7,11,15],

#         (começa do 4, +1 quatro vezes, -1 a partir do 15, quatro vezes)
#         4:[4,5,6,7,12,13,14,15],

#         (começa do 8, +1 oito vezes)
#         8:[8,9,10,11,12,13,14,15]
#     }    

'''     Essa função pega uma string de bits e verifica se a soma dos bits é par ou impar.
        Para isso ela recebe um lista(conjunto) com posicoes e uma string(bits) com os bits. Entao ela usa as
    posicoes da lista para pegar o numero na string para fazer o calculo
        Retorna True se for par e False se for impar '''
    # Parâmetro "conjunto" eu acho que ficaria melhor com outro nome.
    # Que tal "posicoes_checagem"?
def paridade(conjunto, bits):
    soma = 0
    # Não seria melhor "posicao" ao invés de "bit"?
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
    # Posições dos bits fixas para 11, 4. Verificar solução matemática
    # para quadros com 32, 64, 128 e 256 bits.
    checks = {
        0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        1:[1,4,8,0,3,6,10],
        2:[2,5,9,0,3,6,10],
        4:[1,2,3,7,8,9,10],
        8:[4,5,6,7,8,9,10]
    }
    n = 0
    # Quando a variável "bit" está com valor 0, não
    # ocorre qualquer ação com ela! range deve ser:
    # range(1, 16)
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






