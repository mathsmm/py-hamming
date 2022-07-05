def toBits(arquivo):
    listaDeBits = []
    bits = bytearray()
    with open(arquivo,'rb') as file:
        while True:
            dado = file.read(1)
            if str(dado) == "b''":
                break
            bit = format(ord(dado),'b')
            if len(bit) != 8:
                while len(bit) != 8:
                    bit = '0' + bit
            listaDeBits.append(bit)
            bits.append(int(bit,2))
    return listaDeBits

def toFile(listaDeBits):
    nBits = bytearray()
    for i in listaDeBits:
        nBits.append(int(i,2))
    with open('novaImagem.jpg','wb') as file:
        file.write(nBits)

toFile(toBits('imagem.jpg'))
