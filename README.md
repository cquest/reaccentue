# reaccentue

Module python 3.x pour ré-accentuer du texte à partir d'un dictionnaire au format hunspell.

Le dictionnaire par défaut provient de http://www.dicollecte.org

Il est chargé initialement à partir des fichier ".dic" et ".aff" pour générer les variations de suffixes (féminin, pluriel, conjugaisons) et mis en cache pour les utilisations suivantes.

La capitalisation suit les règles utilisées en France par OpenStreetMap.


## Installation

```
git clone https://github.com/cquest/reaccentue.git
cd reaccentue
pip install -r requirements.txt
```

## Préparation des fichiers linguistiques

Certains mots peuvent exister avec et sans accents, par exemple: venus et vénus.

Pour lever l'ambiguïté, il est possible de s'appuyer sur le mot précédent et de déterminer la fréquence d'apparition la plus élevée.

Exemple: RUE DE VENUS -> Rue de Vénus

Pour calculer ces fréquences, le script doublets.sh s'appuie sur un dump textuel de la version française de wikipédia et génère un tableau du nombre d'apparition de chaque doublet de mots stocké dans un fichier freq5.pz.

```
cd dico
sh doublets.sh
cd ..
```

À la première exécution du script reaccentue.py, un dictionnaire sera contruit et stocké en cache (dico/cache.pz).

## Utilisation en ligne de commande

Il est possible de n'appliquer l'accentuation que sur une seule chaîne de texte:

```
python reaccentue.py "BOULEVARD DES MARECHAUX"
Boulevard des Maréchaux
```

ou sur un fichier CSV, en précisant son nom et la colonne à traiter:

`python reaccentue.py test.csv nom`


## Utilisation depuis python

```
from reaccentue import reaccentue

print(reaccentue('BOULEVARD DES MARECHAUX'))
```

## Tests

`pytest tests.py`
