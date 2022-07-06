import random

def criarArquivo():
    arquivo = ''
    for i in range(300):
        arquivo += random.choice(['0','1'])
    with open('arquivo.txt','w') as file:
        file.write(arquivo)

#criarArquivo()
            
def adicionar_bit(quantidade_de_bits_adicionados):
    with open('arquivo.txt', 'r') as arquivo:
        file = arquivo.read()
        listadebits = list(file)
        posiçao_de_mudanca = random.randint(0, len(listadebits))
        quantidade_de_bits_adicionados = quantidade_de_bits_adicionados
        if quantidade_de_bits_adicionados >= 0:
            for line in range(quantidade_de_bits_adicionados):
                if listadebits[posiçao_de_mudanca + line] == '0' or '1':
                    listadebits.append("1")
        print(len(listadebits))

#adicionar_bit(5)

def rajada(quantidade_de_ruidos):
    with open('arquivo.txt', 'r') as arquivo:
        file = arquivo.read()
        listadebits= list(file)
        posicaoInicial = random.randint(0,5)
        quantidade_de_ruidos = quantidade_de_ruidos
        if quantidade_de_ruidos >= 0:
            for line in range(quantidade_de_ruidos):
                if listadebits[posicaoInicial + line]  == '0':
                    listadebits[posicaoInicial + line] = '1'
                else:
                    listadebits[posicaoInicial + line] = '0'
        print(listadebits)
#rajada(2)
def retirador(quantidade_de_bits_retirados):
    with open('arquivo.txt', 'r') as arquivo:
        file = arquivo.read()
        listadebits = list(file)
        posiçao_de_mudanca = random.randint(0, len(listadebits))
        quantidade_de_bits_retirados = quantidade_de_bits_retirados
        if quantidade_de_bits_retirados >= 0:
            for line in range(quantidade_de_bits_retirados):
                if listadebits[posiçao_de_mudanca + line] == '0' or '1':
                    listadebits.pop()
        print(len(listadebits))

#retirador(5)