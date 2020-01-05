import argparse
import sys

from sql_autocorrect.cli.reader import load_result
from sql_autocorrect.models.statut import StatutOk


def mono_grade(fichier_resultat: str, bareme: float) -> None:
    score = grade(fichier_resultat, bareme)
    note = bareme - score
    print("Grade :=>> ", note)


def multigrade(fichier_notes: str) -> None:
    with open(fichier_notes, 'r') as f:
        scores = f.readlines()
        scores = [float(s.strip()) for s in scores]
        score_total = sum(scores)
        note = score_total

        for i in range(len(scores)):
            r = 'resultat' + str(i + 1) + '.sqlac'
            bareme = scores[i]
            score = grade(r, bareme)
            print("Comment :=>> Requête n°", i, " : ", score)
            note -= score

        note_finale = 100 * note / score_total

        print("Grade :=>> ", note_finale)


def grade(r, bareme) -> float:
    correct, statuts = load_result(r)
    score = 0
    if not isinstance(statuts['syntax'], StatutOk):
        score = -(statuts['syntax'].malus)
    else:
        if not correct:
            for statut in statuts['select']:
                score -= statut.malus
            for statut in statuts['label']:
                score -= statut.malus
            for statut in statuts['tables']:
                score -= statut.malus
            for statut in statuts['alias']:
                score -= statut.malus
            for statut in statuts['where']:
                score -= statut.malus
            for statut in statuts['groupby']:
                score -= statut.malus
            for statut in statuts['having']:
                score -= statut.malus
            for statut in statuts['orderby']:
                score -= statut.malus
            if statuts['parse'] is not None:
                score -= statuts['parse'].malus
            score -= statuts['execution'].malus
    # Affichage de la note
    score = -score
    if score > bareme:
        score = bareme

    return score


def parse_grade_args(argv):
    parser = argparse.ArgumentParser(prog='sql-ac-grade')
    subparsers = parser.add_subparsers(help='aide pour chaque commande')
    subparsers.required = True

    # create the parser for the "command_1" command
    parser_a = subparsers.add_parser('multi', help='Note plusieurs résultats automatiquement')
    parser_a.set_defaults(func='multi')
    parser_a.add_argument("-f", type=str, required=True,
                          help="Fichier de notes", metavar='FICHIER')

    # create the parser for the "command_2" command
    parser_b = subparsers.add_parser('mono', help='Note un seul résultat')
    parser_b.set_defaults(func='mono')
    parser_b.add_argument("-r", type=str, required=True,
                          help="Fichier de résultat", metavar='FICHIER')
    parser_b.add_argument("-b", type=float, required=True,
                          help="Barême", metavar='BAREME')
    args = parser.parse_args(argv)
    return args


def calc_grade():  # pragma: nocover
    args = parse_grade_args(sys.argv[1:])
    if args.func == 'multi':
        multigrade(args.f)
    else:
        mono_grade(args.r, args.b)


if __name__ == '__main__':
    calc_grade()  # pragma: nocover
