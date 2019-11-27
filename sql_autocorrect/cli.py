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
    sql_res = PrettyTable()
    sql_res.field_names = rs.keys()
    for row in islice(rs, 25):
        r = ['null' if x is None else x for x in list(row)]
        sql_res.add_row(r)
    return sql_res


def check_alias_agregat(sql):
    msg = ''
    if not isinstance(sql, list):
        if 'count' in sql['value'] and 'name' not in sql:
            msg = 'COUNT(' + (sql['value']['count'] if 'distinct' not in sql['value']['count'] else 'DISTINCT ' +
                                                                                                    sql['value'][
                                                                                                        'count'][
                                                                                                        'distinct']) + ') : mettez un alias\n'
        return msg
    for item in sql:
        if 'count' in item['value'] and 'name' not in item:
            msg += 'COUNT(' + (item['value']['count'] if 'distinct' not in item['value']['count'] else 'DISTINCT ' +
                                                                                                       item['value'][
                                                                                                           'count'][
                                                                                                           'distinct']) + ') : mettez un alias\n'
    return msg


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
        # print(sol)
        # print(prop)
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = max(exces, len(prop) - len(c))
        # TODO: vérifier les jointures et donc récupérer ce qui dépasse
        # print(c)
    return "Il y a " + str(exces) + " table(s) en trop et " + str(manque) + " table(s) manquantes."


def main():
    import threading

    parser = argparse.ArgumentParser(prog='sql_parser')
    parser.add_argument("-f", type=str, required=True,
                        help="Fichier à analyser", metavar='FICHIER')
    parser.add_argument('-db', type=str, required=True,
                        help="Base sur laquelle exécuter la requête", metavar='BDD')
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
        print(sql)
        pprint(sql)
        print(check_alias_agregat(sql['select']))
        print(check_tables(sql['from'], ['Jeu', 'Personne']))
        print(check_tables(sql['from'], [['Jeu', 'Personne'], ['jeu']]))
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
            print(res)
        except OperationalError as e:
            if str(e.orig) == 'interrupted':
                print("Requête interrompue car trop longue à s'exécuter.")
            else:
                print(e)
        t.cancel()

if __name__ == '__main__':
    main()
