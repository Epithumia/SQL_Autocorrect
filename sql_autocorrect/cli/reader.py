import argparse
import pickle
import sys

from sql_autocorrect.models.statut import StatutOk


def load_result(r):
    with open(r, 'rb') as f:
        data = pickle.load(f)
        correct = data[0]
        statuts = data[1]
        return correct, statuts


def affiche_resultat():  # pragma: nocover
    args = parse_affiche_args(sys.argv[1:])
    correct, statuts = load_result(args.r)
    affichage(args, correct, statuts)


def affichage(args, correct, statuts):
    score = 0
    if not isinstance(statuts['syntax'], StatutOk):
        print(statuts['syntax'].message)
        score = -statuts['syntax'].malus
    else:
        # Affichage des commentaires
        if args.c:
            if correct:
                print("Pas de remarques sur la requête")
            else:
                print("Commentaires sur la requête :")
                for statut in statuts['select']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['label']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['tables']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['alias']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['where']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['groupby']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['having']:
                    print(statut.message)
                    score -= statut.malus
                for statut in statuts['orderby']:
                    print(statut.message)
                    score -= statut.malus
                if statuts['parse'] is not None:
                    print(statuts['parse'].message)
                    score -= statuts['parse'].malus
                for m in statuts['execution'].messages:
                    print(m)
                score -= statuts['execution'].malus
        # Affichage du résultat
        if args.res and statuts['parse'] is None and statuts['execution'].resultat is not None:
            print(statuts['execution'].resultat)
    # Affichage de la note
    if score < -100:
        score = -100
    if args.g:
        print(score)


def parse_affiche_args(argv):
    parser = argparse.ArgumentParser(prog='sql-ac-res')
    parser.add_argument("-r", type=str, required=True,
                        help="Fichier de résultat", metavar='FICHIER')
    parser.add_argument('-g', default=False, action='store_true',
                        help="Mode note (défaut : non)")
    parser.add_argument('-c', default=False, action='store_true',
                        help="Mode commentaire (défaut : oui)")
    parser.add_argument('-res', default=False, action="store_true",
                        help="Affiche le résultat de la requête")
    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    affiche_resultat()  # pragma: nocover
