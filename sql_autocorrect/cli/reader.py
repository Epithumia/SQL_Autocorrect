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


def cprint(msg, c):
    if c:
        print(msg)


def affichage(args, correct, statuts):
    score = 0
    if not isinstance(statuts['syntax'], StatutOk):
        print(statuts['syntax'].message)
        score = -statuts['syntax'].malus
    else:
        # Affichage des commentaires
        if args.c or args.g:
            if correct:
                cprint("Pas de remarques sur la requête", args.c)
            else:
                cprint("Commentaires sur la requête :", args.c)
                for statut in statuts['select']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['label']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['agregats']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['tables']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['alias']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['where']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['groupby']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['having']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                for statut in statuts['orderby']:
                    cprint(statut.message, args.c)
                    score -= statut.malus
                if statuts['parse'] is not None:
                    cprint(statuts['parse'].message, args.c)
                    score -= statuts['parse'].malus
                for m in statuts['execution'].messages:
                    cprint(m, args.c)
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
