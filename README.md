![](https://github.com/Epithumia/SQL_Autocorrect/workflows/Tests/badge.svg)

INSTALLATION
============

Testé avec Python 3.9.x, non compatible avec Python 3.10.x

```sh
git clone https://github.com/Epithumia/SQL_Autocorrect
cd SQL_Autocorrect
pip install .
```

Pour exécuter les tests :
Depuis le dossier SQL_Autocorrect, ```pip install ."[testing]"```


UTILISATION
===========

SQL_Autocorrect est composé de trois outils : `sql-ac-parse`, `sql-ac-res` et `sql-ac-grade`.

sql-ac-parse
------------

Le premier outil sert à exécuter une requête sur une base de données, la comparer à une ou plusieurs solutions,
puis à enregistrer le résultat obtenu.

sql-ac-res
----------

Le second outil prend un fichier de résultat généré par `sql-ac-parse` et va faire une sortie : numérique
(un nombre de points perdus) et/ou des commentaires et/ou le résultat (données) récupérées par la requête.

sql-ac-grade
------------

Le dernier outil va prendre en entree un ou plusieurs fichiers de résultat généré par `sql-ac-parse` et calculer
la note finale pour la ou les requêtes examinées précédemment.
