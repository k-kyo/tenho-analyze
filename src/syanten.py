suit_order = ['m', 'p', 's', 'z']

def normal_syanten(tehai):
    mentu = 0
    toitu = 0
    kouho = 0
    syanten = 8
    for i in range(34):
        q = i//9
        mod = i%9
        if 2<=tehai[q][mod]:
            tehai[q][mod]-=2
            syanten = mentu_cut(tehai, 0, mentu, toitu+1, kouho, syanten)
            tehai[q][mod]+=2
    syanten = mentu_cut(tehai, 0, mentu, toitu, kouho, syanten)
    return syanten

def mentu_cut(tehai, s, mentu, toitu, kouho, syanten):
    for i in range(s, 34):
        q = i//9
        mod = i%9
        if tehai[q][mod]:
            break
    if s>=34:
        syanten = taatu_cut(tehai, 0, mentu, toitu, kouho, syanten)
        return syanten
    if tehai[q][mod]>=3:
        tehai[q][mod]-=3
        syanten = mentu_cut(tehai, i, mentu+1, toitu, kouho, syanten)
        tehai[q][mod]+=3
    if mod<7 and i<27 and tehai[q][mod+1] and tehai[q][mod+2]:
        tehai[q][mod]-=1
        tehai[q][mod+1]-=1
        tehai[q][mod+2]-=1
        syanten = mentu_cut(tehai, i, mentu+1, toitu, kouho, syanten)
        tehai[q][mod]+=1
        tehai[q][mod+1]+=1
        tehai[q][mod+2]+=1
    return mentu_cut(tehai, i+1, mentu, toitu, kouho, syanten)

def taatu_cut(tehai, s, mentu, toitu, kouho, syanten):
    for i in range(s, 34):
        q = i//9
        mod = i%9
        if tehai[q][mod]:
            break
    if s>=34:
        temp = 8-mentu*2-kouho-toitu
        if temp<syanten:
            syanten = temp
        return syanten
    if mentu+kouho<4:
        if tehai[q][mod]==2:
            tehai[q][mod]-=2
            syanten = taatu_cut(tehai, i, mentu, toitu, kouho+1, syanten)
            tehai[q][mod]+=2
        if mod<8 and i<27 and tehai[q][mod+1]:
            tehai[q][mod]-=1
            tehai[q][mod+1]-=1
            syanten = taatu_cut(tehai, i, mentu, toitu, kouho+1, syanten)
            tehai[q][mod]+=1
            tehai[q][mod+1]+=1
        if mod<7 and i<27 and tehai[q][mod+2]:
            tehai[q][mod]-=1
            tehai[q][mod+2]-=1
            syanten = taatu_cut(tehai, i, mentu, toitu, kouho+1, syanten)
            tehai[q][mod]+=1
            tehai[q][mod+2]+=1
    return taatu_cut(tehai, i+1, mentu, toitu, kouho, syanten)

def tiitoitu_syanten(tehai):
    toitu = 0
    syurui = 0
    syanten_tiitoi = 0
    for i in range(34):
        q = i//9
        mod = i%9
        if not tehai[q][mod]:
            continue
        syurui+=1
        if tehai[q][mod]>=2:
            toitu+=1
    syanten_tiitoi=6-toitu
    if syurui<7:
        syanten_tiitoi+=7-syurui
    return syanten_tiitoi

def kokusi_syanten(tehai):
    kokusi_toitu = 0
    syanten_kokusi=13
    for i in range(27):
        q = i//9
        mod = i%9
        if mod==0 or mod==8:
            if not tehai[q][mod]:
                continue
            syanten_kokusi-=1
            if tehai[q][mod]>=2 and kokusi_toitu==0:
                kokusi_toitu=1
    for i in range(7):
        if not tehai[3][i]:
            continue
        syanten_kokusi-=1
        if tehai[3][i]>=2 and kokusi_toitu==0:
            kokusi_toitu=1
    syanten_kokusi-=kokusi_toitu
    return syanten_kokusi

def syanten(tehai):
    if sum(sum(tehai, [])) >= 13:
        return min(normal_syanten(tehai), tiitoitu_syanten(tehai), kokusi_syanten(tehai))
    else:
        return normal_syanten(tehai)

def syanten_yukou(tehai):
    menzen, furo = tehai
    temp = []
    for _ in range(len(furo)):
        for i in range(7):
            mod = i%9
            if menzen[3][mod]:
                continue
            menzen[3][mod]+=3
            temp.append(mod)
            break
    n = syanten(menzen)
    y = []
    for i in range(34):
        q = i//9
        mod = i%9
        if menzen[q][mod]==4:
            continue
        menzen[q][mod]+=1
        if syanten(menzen)<n:
            y.append(str(mod+1)+suit_order[q])
        menzen[q][mod]-=1
    for mod in temp:
        menzen[3][mod]-=3
    return (n, y)