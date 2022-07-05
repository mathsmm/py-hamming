def cortar_string_de_bits_original(string: str):
    resto = len(string) % 11
    if resto == 0:
        return string
    return string[:-resto], string[-resto:]

print(cortar_string_de_bits_original('100101101110110000000'))
