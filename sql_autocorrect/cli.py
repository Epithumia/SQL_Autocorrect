import argparse
from itertools import islice
from pprint import pprint

import sqlparse
from moz_sql_parser import parse, format
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


def parse_sql_rs(rs):
    """
    Fonction qui prend un ResultProxy et qui renvoie un tableau PrettyTable avec le résultat de la requête.

    :param rs: Résultat (ResultProxy) de la requête
    :return: Tableau PrettyTable
    """
    sql_res = PrettyTable()
    sql_res.field_names = rs.keys()
    for row in islice(rs, 25):
        r = ['null' if x is None else x for x in list(row)]
        sql_res.add_row(r)
    return sql_res


def check_alias_agregat(sql):
    """
    Fonction qui vérifie les alias dans le SELECT pour vérifier que les agrégats ont été nommés
    :param sql:
    :return:
    """
    msg = ''
    score = 0
    kw = ['count', 'sum', 'avg', 'min', 'max']
    if not isinstance(sql, list):
        for w in kw:
            if w in sql['value'] and 'name' not in sql:
                if 'distinct' not in sql['value'][w]:
                    d = sql['value'][w]
                else:
                    d = 'DISTINCT ' + sql['value'][w]['distinct']
                msg = w.upper() + '(' + d + ') : mettez un alias\n'
                score = -0.25
        return msg, score
    for item in sql:
        for w in kw:
            if w in item['value'] and 'name' not in item:
                # if 'distinct' not in item['value'][w]:
                #    d = item['value'][w]
                # else:
                #    d = 'DISTINCT ' + item['value'][w]['distinct']
                d = format({'select': item['value'][w]})[7:]
                msg += w.upper() + '(' + d + ') : mettez un alias\n'
                score = -0.25
    return msg, score


def check_tables(sql, solutions):
    if not isinstance(solutions[0], list):
        solutions = [solutions]
    if not isinstance(sql, list):
        sql = [sql]
    manque = 9999
    exces = 0
    prop = []
    for token in sql:
        if isinstance(token, dict):
            prop.append(token['value'].upper())
        else:
            prop.append(token.upper())
    for sol in solutions:
        sol = sorted([x.upper() for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = max(exces, len(prop) - len(c))
        # TODO: vérifier les jointures et donc récupérer ce qui dépasse
    return exces, manque


def parse_solutions():
    pass


def check_where(param, solutions):
    return 0, 0


def check_ob(param, solutions):
    return 0, 0


def check_gb(param, solutions):
    return 0, 0


def check_having(param, solutions):
    return 0, 0

def check_select(param, solutions):
    return 0, 0, 0

def parse_requete(args, solutions):
    import threading
    engine = create_engine('sqlite:///' + args.db, echo=False)
    # create a configured "Session" class
    bound_session = sessionmaker(bind=engine)

    # create a Session
    session = bound_session()
    conn = session.connection()
    with open(args.f, 'r') as r:
        stmt = r.read()
        stmt = sqlparse.split(stmt)[0]
        sql = parse(stmt)
        pprint(sql)
        score = 0

        # TODO: Vérifier les colonnes du SELECT
        exces_sel, manque_sel, desordre_sel = check_select(sql['select'], solutions)
        comm_select = ''
        if exces_sel:
            comm_select += 'Il y a ' + str(exces_sel) + ' colonne(s) en trop.\n'
        if manque_sel:
            comm_select += 'Il manque ' + str(manque_sel) + ' colonne(s).\n'
        if desordre_sel:
            comm_select += 'Les colonnes sont dans le désordre.'


        # Vérification des étiquettes dans le SELECT en cas de COUNT/SUM/AVG/MIN/MAX
        label, score_labels = check_alias_agregat(sql['select'])
        score += score_labels

        # Vérification des tables manquantes/en trop
        exces, manque = check_tables(sql['from'], solutions['from'])
        score += -0.5 * exces - manque
        if exces and not manque:
            comm_tables = "Il y a " + str(exces) + " table(s) en trop."
        elif manque and not exces:
            comm_tables = "Il y a " + str(manque) + " table(s) manquantes."
        elif manque and exces:
            comm_tables = "Il y a " + str(exces) + " table(s) en trop et " + str(manque) + " table(s) manquantes."
        else:
            comm_tables = ''

        # TODO: Vérification des conditions dans le WHERE
        comm_where = ''
        if 'where' in sql.keys():
            exces_w, manque_w = check_where(sql['where'], solutions)
            if exces_w and not manque_w:
                comm_where = "Il y a " + str(exces_w) + " contrainte(s) en trop."
            elif manque_w and not exces_w:
                comm_where = "Il y a " + str(manque_w) + " contrainte(s) manquantes."
            elif manque_w and exces_w:
                comm_where = "Il y a " + str(exces_w) + " contrainte(s) en trop et " + str(
                    manque_w) + " contrainte(s) manquantes."
            else:
                comm_where = ''

        # TODO: Vérification des colonnes dans le ORDER BY
        comm_ob = ''
        if 'order by' in sql.keys():
            desordre_ob, manque_ob = check_ob(sql['order by'], solutions)
            if desordre_ob and not manque_ob:
                comm_ob = "Les colonnes du ORDER BY sont dans le désordre."
            elif manque_ob and not desordre_ob:
                comm_ob = "Il y a " + str(manque_ob) + " critère(s) de tri manquant(s)."
            elif manque_ob and desordre_ob:
                comm_ob = "Les colonnes du ORDER BY sont dans le désordre et il y a " + str(
                    manque_ob) + " critère(s) de tri manquant(s)."
            else:
                comm_ob = ''

        # TODO: Vérification des colonnes dans le GROUP BY
        comm_gb = ''
        if 'group by' in sql.keys():
            desordre_gb, manque_gb = check_gb(sql['group by'], solutions)

        # TODO: Vérification des conditions dans le HAVING
        comm_having = ''
        if 'having' in sql.keys():
            exces_having, manque_having = check_having(sql['having'], solutions)

        # Affichage des commentaires
        if args.c:
            if score < 0:
                print("Commentaires sur la requête :")
                print(comm_select.rstrip()) if comm_select else None
                print(label.strip())
                print(comm_tables) if comm_tables else None
                print(comm_where) if comm_where else None
                print(comm_gb) if comm_gb else None
                print(comm_having) if comm_having else None
                print(comm_ob) if comm_ob else None
            else:
                print("Pas de remarques")

        # Affichage de la note
        if args.g:
            print(score)

        seconds = 10
        t = threading.Timer(seconds, conn.connection.interrupt)
        t.start()
        try:
            rs = conn.execute(stmt)
            res = parse_sql_rs(rs)

            # Affichage du résultat
            if args.res:
                print(res)
        except OperationalError as e:
            if str(e.orig) == 'interrupted':
                print("Requête interrompue car trop longue à s'exécuter.")
            else:
                print(e)
        t.cancel()


def main():
    parser = argparse.ArgumentParser(prog='sql_parser')
    parser.add_argument("-f", type=str, required=True,
                        help="Fichier à analyser", metavar='FICHIER')
    parser.add_argument('-db', type=str, required=True,
                        help="Base sur laquelle exécuter la requête", metavar='BDD')
    parser.add_argument('-g', default=False, action='store_true',
                        help="Mode note (défaut : non)")
    parser.add_argument('-c', default=True, action='store_true',
                        help="Mode commentaire (défaut : oui)")
    parser.add_argument('-res', default=False, action="store_true",
                        help="Affiche le résultat de la requête")
    args = parser.parse_args()
    #solutions = parse_solutions()
    solutions = {}
    solutions['from'] = [['Jeu', 'Personne'], ['jeu']]
    parse_requete(args, solutions)


if __name__ == '__main__':
    main()
