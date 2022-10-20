import json
from PIL import Image
import random

def def_member(id, name):
    memberDict = {}
    memberDict["id"] = id
    memberDict["name"] = name
    memberDict["points"] = 0
    memberDict["messages"] = 0
    memberDict["vocal"] = 0
    memberDict["xp"] = 0

    return memberDict
#-------------------------------------------------------------------------------
def maj_file_json(file, file_choice):
    with open(f'{file_choice}.json', 'w') as f:
        json.dump(file, f, indent=2)
#-------------------------------------------------------------------------------
def vocal_channels():
    channels = [505819477825552414,900391569742516274,902202043614244884,
                901510552562589746,901577019115077642]
    return channels
#-------------------------------------------------------------------------------
def calc_time(s):
    if s < 60:
        time = f"{s} sec"
        return time
    elif 60 <= s < 3600:
        m = s / 60
        time = f"{int(m)} min"
        return time
    elif 3600 <= s < 86400:
        h = s / (60*60)
        m = s / 60 % 60
        if m < 10:
            time = f"{int(h)}h0{int(m)}"
            return time
        else:
            time = f"{int(h)}h{int(m)}"
            return time
    else:
        h = s / (60*60)
        time = f"{int(h)}h"
        return time
#-------------------------------------------------------------------------------
def calc_lvl(xp):
    seuil = 725
    lvl = 0

    if xp > seuil:
        while xp > seuil:
            if lvl < 5:
                coef = 2
            elif 5 <= lvl < 10:
                coef = 1.5
            else:
                coef = 1.1

            seuil *= coef
            lvl += 1

        lvl -= 1

        return lvl, int(seuil)
    return lvl, int(seuil)
#-------------------------------------------------------------------------------
def del_accent(a):

    b = a.replace("é","e")
    c = b.replace("è","e")
    d = c.replace("ë","e")
    e = d.replace("ê","e")

    f = e.replace("à","a")
    g = f.replace("ä","a")
    h = g.replace("â","a")

    i = h.replace("ï","i")
    j = i.replace("î","i")

    k = j.replace("ô","o")
    l = k.replace("ö","o")

    m = l.replace("ù","u")
    n = m.replace("û","u")
    o = n.replace("ü","u")

    return o
#-------------------------------------------------------------------------------
def rarity(p):
    p1 = 0.04
    p2 = 0.02
    p3 = 0.001
    p4 = 0.00003
    p5 = 0.000001
    p6 = 0.0000007

    if p2 < p <= p1:#Commun
        return "⚪ Commun"
    elif p3 < p <= p2:#peu commun
        return "🟢 Peu Commun"
    elif p4 < p <= p3:#rare
        return "🔵 Rare"
    elif p5 < p <= p4:#epic
        return "🟣 Epic"
    elif p6 < p <= p5:#legendaire
        return "🟡 Légendaire"
    elif 0 < p <= p6:#mythique
        return "🔶 Mythique"
#-------------------------------------------------------------------------------
def calcRandom():

    x = 0
    luck_per_item = []
    save_id = []
    rarity_per_item = []
    #name = ['BG','WINGS','COLOR','CROWN','MOUTH','EYES']

    while x < 6:
        if x == 0:
            item = 0
        elif x == 1:
            item = 1
        elif x == 2:
            item = 2
        else:
            item = 3

        if item == 0:#background 4
            taux = random.randint(1,101)
            if taux <= 60:
                drop = 1; luck = 60; rarity = "⚪ Commun"
            elif 60 < taux <= 85:
                drop = 2; luck = 24; rarity = "🔵 Rare"
            elif 85 < taux <= 95:
                drop = 3; luck = 10; rarity = "🟣 Epic"
            else:
                drop = 4; luck = 6; rarity = "🟡 Légendaire"

        elif item == 1:#wings 8
            taux = random.randint(0,99)
            if taux < 25:
                drop = 0; luck = 25; rarity = "⚪ Commun"
            elif 25 <= taux < 50:
                drop = 1; luck = 25; rarity = "⚪ Commun"
            elif 50 <= taux < 68:
                drop = 2; luck = 18; rarity = "🟢 Peu commun"
            elif 68 <= taux < 81:
                drop = 3; luck = 13; rarity = "🔵 Rare"
            elif 81 <= taux < 91:
                drop = 4; luck = 10; rarity = "🟣 Epic"
            elif 91 <= taux < 96:
                drop = 5; luck = 5; rarity = "🟡 Légendaire"
            elif 96 <= taux < 99:
                drop = 6; luck = 3; rarity = "🟡 Légendaire"
            else:
                drop = 7; luck = 1; rarity = "🟠 Mythique"

        elif item == 2:#color 6
            taux = random.randint(1,101)
            if taux <= 34:
                drop = 1; luck = 34; rarity = "⚪ Commun"
            elif 34 < taux <= 60:
                drop = 2; luck = 25; rarity = "🟢 Peu commun"
            elif 60 < taux <= 80:
                drop = 3; luck = 20; rarity = "🔵 Rare"
            elif 80 < taux <= 95:
                drop = 4; luck = 15; rarity = "🟣 Epic"
            elif 95 < taux <= 100:
                drop = 5; luck = 5; rarity = "🟡 Légendaire"
            else:
                drop = 6; luck = 1; rarity = "🟠 Mythique"

        elif item == 3:#crown, eyes, mouth
            taux = random.randint(1,101)
            if taux <= 20:
                drop = 1; luck = 20; rarity = "⚪ Commun"
            elif 20 < taux <= 41:
                drop = 2; luck = 20; rarity = "⚪ Commun"
            elif 41 < taux <= 61:
                drop = 3; luck = 20; rarity = "⚪ Commun"
            elif 61 < taux <= 77:
                drop = 4; luck = 16; rarity = "🟢 Peu commun"
            elif 77 < taux <= 83:
                drop = 5; luck = 6; rarity = "🔵 Rare"
            elif 83 < taux <= 89:
                drop = 6; luck = 6; rarity = "🔵 Rare"
            elif 89 < taux <= 94:
                drop = 7; luck = 5; rarity = "🟣 Epic"
            elif 94 < taux <= 97:
                drop = 8; luck = 3; rarity = "🟡 Légendaire"
            elif 97 < taux <= 100:
                drop = 9; luck = 3; rarity = "🟡 Légendaire"
            else:
                drop = 10; luck = 1; rarity = "🟠 Mythique"

        save_id.append(drop); luck_per_item.append(luck/100); rarity_per_item.append(rarity)
        #print(name[x], ": -", "rareté :", rarity, "|", luck, "%")
        x += 1

    return save_id, luck_per_item, rarity_per_item
#-------------------------------------------------------------------------------
def alv(o):
    if o < 0.00000001:
        return 9
    elif o < 0.0000001:
        return 8
    elif o < 0.000001:
        return 7
    elif o < 0.00001:
        return 6
    elif o < 0.0001:
        return 5
    elif o < 0.001:
        return 4
    elif o < 0.01:
        return 3
    elif o < 0.1:
        return 2
    elif o < 1:
        return 1
