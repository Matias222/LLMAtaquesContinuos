import unicodedata

def is_allowed(s):

    # caso 2: permitir acentos (latinos extendidos)
    for ch in s:
        # Saltar los caracteres de control o vacíos
        if not ch.isprintable():
            return False
        # Si es ASCII, es válido
        if ch.isascii():
            continue
        # Revisar que pertenezca al alfabeto latino
        name = unicodedata.name(ch, "")
        if "LATIN" not in name:
            return False
    return True

arr=["mat","mat,","matí"]

ascii_toks = []
for i in range(len(arr)):

    print(arr[i])

    if not is_allowed(arr[i]):
        ascii_toks.append(i)

print(ascii_toks)