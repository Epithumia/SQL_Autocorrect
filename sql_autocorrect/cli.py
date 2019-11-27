import argparse
from itertools import islice
from pprint import pprint

import sqlparse
from moz_sql_parser import parse
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
                if 'distinct' not in item['value'][w]:
                    d = item['value'][w]
                else:
                    d = 'DISTINCT ' + item['value'][w]['distinct']
                msg += w.upper() + '(' + d + ') : mettez un alias\n'
                score = -0.25
    return msg, score


def check_tables(sql, solution):
    if not isinstance(solution[0], list):
        solution = [solution]
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
    for sol in solution:
        sol = sorted([x.upper() for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = max(exces, len(prop) - len(c))
        # TODO: vérifier les jointures et donc récupérer ce qui dépasse
    return exces, manque


def main():
    import threading

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
        # Vérification des étiquettes dans le SELECT en cas de COUNT/SUM/AVG/MIN/MAX
        label, score_labels = check_alias_agregat(sql['select'])
        score += score_labels

        # Vérification des tables manquantes/en trop
        exces, manque = check_tables(sql['from'], [['Jeu', 'Personne'], ['jeu']])
        score += -0.5 * exces - manque
        if exces or manque:
            comm_tables = "Il y a " + str(exces) + " table(s) en trop et " + str(manque) + " table(s) manquantes."
        else:
            comm_tables = ''
        if args.c:
            if score < 0:
                print("Commentaires sur la requête :")
                print(label.strip())
                print(comm_tables)
            else:
                print("Pas de remarques")
        if args.g:
            print(score)
        # TODO: check WHERE
        # TODO: check GROUP BY
        # TODO: check HAVING
        # TODO: check ORDER BY

        seconds = 10
        t = threading.Timer(seconds, conn.connection.interrupt)
        t.start()
        try:
            rs = conn.execute(stmt)
            res = parse_sql_rs(rs)
            if args.res:
                print(res)
        except OperationalError as e:
            if str(e.orig) == 'interrupted':
                print("Requête interrompue car trop longue à s'exécuter.")
            else:
                print(e)
        t.cancel()


if __name__ == '__main__':
    main()
