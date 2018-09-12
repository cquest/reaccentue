import sys
import os.path
import re
import select
import csv
import pickle

from unidecode import unidecode


def add_dico(mot, dico):
    if mot < 'a':
        return
    maj = unidecode(mot).upper()
    if maj in dico:
        if mot not in dico[maj]:
            dico[maj].append(mot)
    else:
        dico[maj] = [mot]


def load_dico(fichier, dico):
    "Charge le dictionnaire MAJUSCULE > minuscules accentuées"
    with open(fichier, mode='r') as dicco:
        for mot in dicco:
            mot = mot.replace('\n', '')
            m = re.sub(r'/.*', '', mot)
            add_dico(m, dico)
            # pluriels et variantes
            pluriel = re.sub(r'.*/', '', mot)
            if pluriel == 'X.':
                add_dico(re.sub(r'i?l$', 'ux', m), dico)
                add_dico(re.sub(r'[aeoœ]u$', '\1x', m), dico)
            elif pluriel in ['S.', 'S=']:
                add_dico(re.sub(r'[^sxz]$', '\1s', m), dico)
            elif pluriel in ['I.']:
                add_dico(re.sub(r'[^sxz]$', '\1s', m), dico)
                add_dico(re.sub(r'a$', 'e', m), dico)
                add_dico(re.sub(r'([eo]|um)$', 'i', m), dico)
                add_dico(re.sub(r'um$', 'a', m), dico)
            elif pluriel == 'W.':
                add_dico(re.sub(r'e$', '', m), dico)
                add_dico(re.sub(r'e$', 'es', m), dico)
                add_dico(re.sub(r'e$', 'ux', m), dico)
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
