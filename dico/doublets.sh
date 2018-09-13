# génération de fréquence de doublets de mot à partir d'un dump textuel de wikipedia FR
wget -nc http://redac.univ-tlse2.fr/corpus/wikipedia/wikipediaFR-TXT.txt.7z
7z e wikipediaFR-TXT.txt.7z
iconv wikipediaTXT.txt -f iso8859-1 -t utf8 > wikipediaUTF.txt
rm wikipediaTXT.txt
python doublets.py
rm wikipediaUTF.txt
