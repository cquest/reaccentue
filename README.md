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
