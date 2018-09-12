import sys
import os.path
import re
import select
import csv
import pickle

from unidecode import unidecode


def add_dico(mot, dico):
    if mot < 'A':
        return
    maj = unidecode(mot).upper()
    if maj in dico:
        if mot not in dico[maj]:
            dico[maj].append(mot)
    else:
        dico[maj] = [mot]


def load_word(mot, dico, affixes):
    m = re.sub(r'/.*', '', mot)
    add_dico(m, dico)
    rules = re.sub(r'.*/', '', mot)
    while rules != '':
        rule = rules[0:2]
        rules = rules[2:]
        if rule in affixes:
            if affixes[rule]['type'] == 'SFX':
                for r in affixes[rule]['rules']:
                    if re.search(r[4]+'$', m):
                        suffixe = re.sub(r'/.*', '', re.sub(r[2]+'$', r[3], m))
                        if suffixe != m:
                            add_dico(suffixe, dico)
                        if '/' in r[3]:
                            load_word(re.sub(r[2]+'$', r[3], m), dico, affixes)
            if affixes[rule]['type'] == 'PFX':
                for r in affixes[rule]['rules']:
                    if re.search('^'+r[4], m):
                        if '/' in r[3]:
                            add_dico(re.sub(r'/.*', '', re.sub('^'+r[2],
                                            r[3], m)), dico)
                            load_word(re.sub('^'+r[2], r[3], m), dico, affixes)
                        elif re.sub('^'+r[2], r[3], m) != m:
                            add_dico(re.sub('^'+r[2], r[3], m), dico)
                            print('-> ', re.sub('^'+r[2], r[3], m), r)


def load_dico(fichier, dico):
    "Charge le dictionnaire MAJUSCULE > minuscules accentuées"

    # charge les définitions des suffixes (SFX)
    affixes = dict()
    try:
        with open(fichier+'.aff', mode='r') as affix:
            for aff in affix:
                af = aff.split()
                if len(af) == 4 and af[0] in ['SFX']:  # header
                    affixes[af[1]] = {'type': af[0], 'cross_product': af[2],
                                      'rules': []}
                if len(af) > 4 and af[0] in ['SFX']:  # rules
                    if af[2] == '0':
                        af[2] = ''
                    if af[3][0] == '0':
                        af[3] = af[3][1:]
                    affixes[af[1]]['rules'].append(af)
    except:
        pass

    # charge le contenu du dictionaire en appliquant préfixes/suffixes
    with open(fichier+'.dic', mode='r') as dicco:
        for mot in dicco:
            mot = mot.replace('\n', '')
            load_word(mot, dico, affixes)

    return dico


def reaccente(maj):
    for mot in maj.split():
        if mot.lower() in articles:
            maj = maj.replace(mot, mot.lower())
        elif mot.upper() in dico and len(dico[mot.upper()]) == 1:
            maj = maj.replace(mot, dico[mot.upper()][0].capitalize())
        else:
            maj = maj.replace(mot, mot.lower().capitalize())
    return maj


dico = None
try:
    if (os.path.getmtime('dico/fr-toutesvariantes.dic') <
        os.path.getmtime('dico/cache.p')):
        with open('dico/cache.p', 'rb') as dico_cache:
                dico = pickle.load(dico_cache)
except:
    pass

if dico is None:
    dico = dict()
    dico = load_dico('dico/fr-toutesvariantes.dic',  dico)
    dico = load_dico('dico/complements.dic', dico)
    with open('dico/cache', 'w') as dico_cache:
        dico_cache.write(json.dumps(dico))

articles = ['le', 'la', 'les',
            'un',  'une', 'des',
            'à', 'au', 'aux',
            'du', 'de',
            'et', 'ou']

if __name__ == "__main__":
    if len(sys.argv) == 1:
        if select.select([sys.stdin, ], [], [], 0.0)[0]:
            lines = sys.stdin.readlines()
            for l in lines:
                print(reaccente(l.replace('\n', '')))
        else:
            print("""Usage:  reaccente.py texte ou fichier
        reaccente.py 'BOULEVARD DU MARECHAL JEAN MARIE DE LATTRE DE TASSIGNY'
        reaccente.py fichier.txt""")
    else:
        print(reaccente(sys.argv[1]))
