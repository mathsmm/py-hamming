def toBits(arquivo):
    with open(arquivo,'rb') as file:
        hexadecimais = str(file.read())
        bits = ''
        for x in hexadecimais:
            bits += format(ord(x),'b')
            bits += ' '
        return bits

def toHexadecimal(bits):
    hexadecimal = ''
    for bit in bits.split(' '):
        try:
            hexadecimal += chr(int(bit,2))
        except: pass
    return hexadecimal

bits = toBits('arquivo.jpg')
print(toHexadecimal(bits))
