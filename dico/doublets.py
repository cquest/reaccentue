import re
import sys
import pickle
import gzip

freq = dict()


def update_freq(texte):
    mots = re.sub(r"([=,:;\.'’•\(\)\[\]\{\}\-«»0-9]+)", ' | ', texte).lower().split()
    prev = None
    for mot in mots:
        if mot == '|':
            mot = None
        if prev is not None and mot is not None:
            if prev+' '+mot in freq:
                freq[prev+' '+mot] = freq[prev+' '+mot] + 1
            else:
                freq[prev+' '+mot] = 1
        prev = mot


n = 0
with open('wikipediaUTF.txt','r') as wp:
    lines = wp.readlines()
    for t in lines:
        n = n + 1
        t = re.sub(r'^\<.*\>', '', t)
        if t != '':
            update_freq(t)

# enregistrement en cache
with gzip.open('freq.pz', 'wb') as cache:
        pickle.dump(freq, cache)
# enregistrement limité aux entrées présentes plus de 5 fois
f2 = {key:val for key, val in freq.items() if val > 5}
with gzip.open('freq5.pz', 'wb') as cache:
        pickle.dump(f2, cache)
