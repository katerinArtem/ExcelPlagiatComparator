import binascii
def canonize(source:str):
        stop_symbols = '.,!?:;-\n\r()'
        stop_words = ('nan','unnamed','none')
        return ( [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)] )


def genshingle(source:str,shingleLen:int):
    out = [] 
    for i in range(len(source)-(shingleLen-1)):
        out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))
    return out


def compaire (source1:str,source2:str):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
    return same*2/float(len(source1) + len(source2))*100


def compare(text1:str,text2:str,shingleLen:int):
    return compaire(genshingle(canonize(text1),shingleLen),genshingle(canonize(text2),shingleLen))
