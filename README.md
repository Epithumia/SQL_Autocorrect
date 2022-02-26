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

# Outils

SQL_Autocorrect est composé de trois outils : `sql-ac-parse`, `sql-ac-res` et `sql-ac-grade`.

## sql-ac-parse

Le premier outil sert à exécuter une requête sur une base de données, la comparer à une ou plusieurs solutions,
puis à enregistrer le résultat obtenu.

### Utilisation

```sh
sql-ac-parse [-h] -f FICHIER -s FICHIER -r FICHIER -db BDD
```

### Arguments et options

```shell
  -h, --help  Affiche cette aide
  -f FICHIER  Fichier à analyser
  -s FICHIER  Fichier de solution(s)
  -r FICHIER  Fichier dans lequel stocker le résultat [par défaut : resultat.sqlac]
  -db BDD     Base sur laquelle exécuter la requête
```
Le fichier à analyser est un fichier texte contenant une requête. S'il y a de multiples requêtes,
seule la première est prise en compte.

Le fichier de solutions est un fichier texte contenant une ou plusieurs requêtes solutions, qui
servent de référence pour évaluer la requête à analyser.

Le fichier de résultat sert à stocker le résultat de l'analyse pour être ensuite traité par l'un
des deux autres outils.

# Limitations

L'analyse n'est pas toute puissante et est aujourd'hui limitée à certains aspects du SQL. Ainsi,
l'outil est pour le moment limité aux requêtes SELECT _sans imbrication_, et parmi ces requêtes,
tout n'est pas analysé. À l'heure actuelle, sont traités :
 - les colonnes du SELECT (colonnes manquantes ou surnuméraires)
 - les alias (dans le SELECT ou le FROM)
 - les tables (tables manquantes ou inutiles)
 - les agrégats dans le SELECT
 - le GROUP BY
 - le HAVING (partiellement)
 - le ORDER BY (ordre et colonnes manquantes ou surnuméraires, sens des tris)

Il manque en particulier tout ce qui est WHERE et jointures

## sql-ac-res

Le second outil prend un fichier de résultat généré par `sql-ac-parse` et va faire une sortie : numérique
(un nombre de points perdus) et/ou des commentaires et/ou le résultat (données) récupérées par la requête.

### Utilisation

```sh
sql-ac-res [-h] -r FICHIER [-g] [-c] [-res]
```

### Arguments et options

```shell
  -h, --help  Affiche cette aide
  -r FICHIER  Fichier de résultat
  -g          Mode note
  -c          Mode commentaire
  -res        Affiche le résultat de la requête
```

Le fichier attendu est un fichier de résultat généré par `sql-ac-parse`.

Le mode note (`-g`) calcule un score (une pénalité, en fait) qui peut être ensuite exploitée pour de la notation automatique.

Le mode commentaire (`-c`) affiche les observations textuelles relatives aux erreurs détectées.
Par exemple, TODO

Le mode résultat (`-res`) affiche dans la console le résultat de l'exécution.

## sql-ac-grade

Le dernier outil va prendre en entrée un ou plusieurs fichiers de résultat généré par `sql-ac-parse` et calculer
la note finale pour la ou les requêtes examinées précédemment.

### Utilisation

```sh
sql-ac-grade mono [-h] -r FICHIER -b BAREME
```
ou
```sh
sql-ac-grade multi [-h] -f FICHIER -p CHEMIN
```

### Arguments et options

```shell
  {multi,mono}  Aide pour chaque commande
    multi       Note plusieurs résultats automatiquement
    mono        Note un seul résultat

  -h, --help    Affiche l'aide
```

En mode `mono`:
```shell
  -r FICHIER  Fichier de résultat
  -b BAREME   Barème
```

Le mode mono sert à générer une note pour le module VPL de Moodle. Il prend en entrée un fichier
de résultat et un nombre correspondant au barème de la question.

En mode `multi`:
```shell
  -f FICHIER  Fichier de notes
  -p CHEMIN   Chemin vers les résultats
```

Le mode multi sert à générer un ensemble de notes pour le module VPL de Moodle. Il prend en entrée un fichier
de barème (une question --nombre-- par ligne) et un chemin vers un dossier dans lequel tous les fichiers
resultat*.sqlac (resultat1.sqlac...resultatN.sqlac) seront lus.
