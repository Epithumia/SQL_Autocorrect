import argparse
from itertools import islice, filterfalse
from pprint import pprint

import sqlparse
from moz_sql_parser import parse, format
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


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
                d = format({'select': item['value'][w]})[7:]
                msg += w.upper() + '(' + d + ') : mettez un alias\n'
                score = -0.25
    return msg, score


def check_tables(sql, solutions):
    tables_solution = solutions['from']
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
    for sol in tables_solution:
        sol = sorted([x.upper() for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = max(exces, len(prop) - len(c))
        # TODO: vérifier les jointures et donc récupérer ce qui dépasse
    return exces, manque


def parse_solutions(fichier):
    solutions = {}
    with open(fichier, 'r') as f:
        sol_sql = f.read()
        solutions_sql = sqlparse.split(sol_sql)
        solutions['from'] = []
        solutions['select'] = []
        solutions['where'] = []
        solutions['groupby'] = []
        solutions['having'] = []
        solutions['orderby'] = []
        for stmt in solutions_sql:
            if stmt != '':
                sql = parse(stmt)
                sol_select = sql['select']
                if not isinstance(sol_select, list):
                    sol_select = [sol_select]
                t = []
                for col in sol_select:
                    if isinstance(col, dict):
                        t.append(col['value'])
                    else:
                        t.append(col)
                if len(t):
                    solutions['select'].append(t)
                solutions['select'] = list(map(list, unique_everseen(map(tuple, solutions['select']), str)))
                sol_from = sql['from']
                if not isinstance(sol_from, list):
                    sol_from = [sol_from]
                t = []
                for table in sol_from:
                    if isinstance(table, dict):
                        t.append(table['value'])
                    else:
                        t.append(table)
                if len(t):
                    solutions['from'].append(t)
                solutions['from'] = list(map(list, unique_everseen(map(tuple, solutions['from']))))
                if 'orderby' in sql.keys():
                    sol_ob = sql['orderby']
                    if not isinstance(sol_ob, list):
                        sol_ob = [sol_ob]
                    t = []
                    for col in sol_ob:
                        if isinstance(col, dict):
                            t.append(col['value'])
                        else:
                            t.append(col)
                    if len(t):
                        solutions['orderby'].append(t)
                    solutions['orderby'] = list(map(list, unique_everseen(map(tuple, solutions['orderby']), str)))
                if 'groupby' in sql.keys():
                    sol_gb = sql['groupby']
                    if not isinstance(sol_gb, list):
                        sol_gb = [sol_gb]
                    t = []
                    for col in sol_gb:
                        if isinstance(col, dict):
                            t.append(col['value'])
                        else:
                            t.append(col)
                    if len(t):
                        solutions['groupby'].append(t)
                    solutions['groupby'] = list(map(list, unique_everseen(map(tuple, solutions['groupby']), str)))
                if 'where' in sql.keys():
                    sol_where = sql['where']
                    if not isinstance(sol_where, list):
                        sol_where = [sol_where]
                    t = []
                    for cond in sol_where:
                        t.append(cond)
                    if len(t):
                        solutions['where'].append(t)
                    solutions['where'] = list(map(list, unique_everseen(map(tuple, solutions['where']), str)))
                if 'having' in sql.keys():
                    sol_having = sql['having']
                    if not isinstance(sol_having, list):
                        sol_having = [sol_having]
                    t = []
                    for cond in sol_having:
                        t.append(cond)
                    if len(t):
                        solutions['having'].append(t)
                    solutions['having'] = list(map(list, unique_everseen(map(tuple, solutions['having']), str)))
    return solutions


def check_where(param, solutions):
    return 0, 0


def check_ob(sql, solutions):
    return 0, 0


def check_gb(param, solutions):
    return 0, 0


def check_having(param, solutions):
    return 0, 0


def check_select(sql_select, solutions):
    if not isinstance(sql_select, list):
        sql_select = [sql_select]
    # SELECT * au lieu de colonnes précises
    if sql_select[0] == '*' and '*' not in solutions['select']:
        return 0, 0, False, True

    # Excès et/ou manque
    exces = 0
    manque = 9999
    prop = []
    for token in sql_select:
        if isinstance(token, dict):
            prop.append(str(token['value']))
        else:
            prop.append(str(token))
    for sol in solutions['select']:
        sol = sorted([str(x) for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = max(exces, len(prop) - len(c))

    # Désordre = toutes les colonnes mais pas dans le bon ordre
    if all(len(sql_select) == len(x) for x in solutions['select']) and not any(
            all(a['value'] == b for a, b in zip(sql_select, solutions['select'][i])) for i in
            range(len(solutions['select']))):
        return 0, 0, True, False
    return exces, manque, False, False


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
        exces_sel, manque_sel, desordre_sel, etoile = check_select(sql['select'], solutions)
        comm_select = ''
        if etoile:
            comm_select = 'Il ne faut pas faire SELECT *, on veut des informations précises.'
        else:
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
        exces, manque = check_tables(sql['from'], solutions)
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
        if min([len(x) for x in solutions['orderby']]) and 'orderby' not in sql.keys():
            comm_ob = "Le ORDER BY est manquant"
            score -= 1
        if 'orderby' in sql.keys():
            desordre_ob, manque_ob = check_ob(sql['orderby'], solutions)
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
        if 'groupby' in sql.keys():
            desordre_gb, manque_gb = check_gb(sql['groupby'], solutions)

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
    parser.add_argument("-s", type=str, required=True,
                        help="Fichier de solution(s)", metavar='FICHIER')
    parser.add_argument('-db', type=str, required=True,
                        help="Base sur laquelle exécuter la requête", metavar='BDD')
    parser.add_argument('-g', default=False, action='store_true',
                        help="Mode note (défaut : non)")
    parser.add_argument('-c', default=True, action='store_true',
                        help="Mode commentaire (défaut : oui)")
    parser.add_argument('-res', default=False, action="store_true",
                        help="Affiche le résultat de la requête")
    args = parser.parse_args()
    solutions = parse_solutions(args.s)
    pprint(solutions)
    parse_requete(args, solutions)


if __name__ == '__main__':
    main()
