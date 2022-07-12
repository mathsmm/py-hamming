import random


# Intercalar
def embaralhar(bits):
    resultado = ''
    qtd_quadros = len(bits) // 16

    for x in range(16):
        for y in range(qtd_quadros):
            resultado += bits[(y*16)+x]

    return resultado

# Desintercalar
def desembaralhar(bits):
    resultado = ''
    qtd_quadros = len(bits) // 16

    for x in range(qtd_quadros):
        for y in range(16):
            resultado += bits[(y * qtd_quadros)+x]

    return resultado

'''
original = ''
for caractere in range(1600):
    original += random.choice(['1','0'])
print()
print('original:', original)
print()

emb = embaralhar(original)
print('emberare:',emb)
desemb = desembaralhar(emb)
print()
print('desembed:',desemb)
if original == desemb:
    print('ok')
else:
    print('erro')

'''