import argparse
import pickle
import sys
from itertools import filterfalse, islice
from numbers import Number
from typing import Tuple, List

import sqlparse
from moz_sql_parser import format, parse
from prettytable import PrettyTable
from pyparsing import ParseException
from sqlalchemy import create_engine
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from sql_autocorrect.models.statut import Statut, MaxLignes, ParseOk, NbLignesDiff, NbColDiff, ResultatsDiff, \
    AliasManquant, TableEnExces, TableManquante, AliasRepete, TableRepetee, OrderByAbsent, OrderByExces, OrderByManque, \
    OrderByMalTrie, OrderByDesordre, GroupByInutile, GroupByAbsent, GroupBySansAgregat, GroupByManque, GroupByExces, \
    HavingSansGB, HavingManquant, HavingInutile, SelectEtoile, SelectDesordre, SelectManque, SelectExces, StatutOk, \
    ErreurParsing, RequeteOk, RequeteInterrompue


def unique_everseen(iterable, key=None):
    """
    List unique elements, preserving order. Remember all elements ever seen."
    unique_everseen('AAAABBBCCDAABBB') --> A B C D
    unique_everseen('ABBCcAD', str.lower) --> A B C D

    :param iterable: elements to iterate
    :param key: comparison key
    :return: iterable with unique elements
    """
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


def parse_sql_rs_pretty(rs, nb_lignes=25):
    """
    Fonction qui prend un ResultProxy et qui renvoie un tableau PrettyTable avec le résultat de la requête.

    :param rs: Résultat (ResultProxy) de la requête
    :param nb_lignes: Nombre max de lignes à réupérer pour affichage
    :return: Tableau PrettyTable
    """
    sql_res = PrettyTable()
    sql_res.field_names = rs.keys()
    for row in islice(rs, nb_lignes):
        r = ['null' if x is None else x for x in list(row)]
        sql_res.add_row(r)
    return sql_res


def parse_sql_rs_data(rs: ResultProxy, max_lignes=1000000) -> Tuple[bool, List[Statut]]:
    correct = True
    nb_col = len(rs.keys())
    data = []
    statut = []
    if max_lignes:
        for row in islice(rs, max_lignes):
            data.append(row)
        nb_lignes = len(data)
        if nb_lignes == max_lignes:
            correct = False
            statut.append(MaxLignes())
        rs.close()
    else:
        data = list(rs)
        nb_lignes = len(data)
    statut.insert(0, ParseOk(data, nb_col, nb_lignes))
    return correct, statut


def compare_sql(s1, s2) -> Tuple[bool, List[Statut]]:
    correct = True
    statut = []
    c1 = s1.nb_col
    c2 = s2.nb_col
    res1 = s1.data[:]
    res2 = s2.data[:]
    if len(res1) != len(res2):
        correct = False
        statut.append(NbLignesDiff(len(res1), len(res2)))
    if c1 != c2:
        correct = False
        statut.append(NbColDiff(c1, c2))
    if not correct:
        return correct, statut
    for i in range(len(res1)):
        rs1 = sorted(res1[i], key=lambda x: (x is not None, '' if isinstance(x, Number) else type(x).__name__, x))
        rs2 = sorted(res2[i], key=lambda x: (x is not None, '' if isinstance(x, Number) else type(x).__name__, x))
        if rs1 != rs2:
            return False, [ResultatsDiff(rs1, rs2)]
    return True, []


def check_alias_agregat(sql) -> Tuple[bool, List[Statut]]:
    """
    Fonction qui vérifie les alias dans le SELECT pour vérifier que les agrégats ont été nommés

    :param sql:
    :return: Booléen, vrai si la vérification est ok ; liste de statuts
    :rtype: Tuple[bool, List[Statut]]

    """
    correct = True
    statut = []
    m = 0.25
    kw = ['count', 'sum', 'avg', 'min', 'max']
    sql_select = sql['select']
    if not isinstance(sql_select, list):
        sql_select = [sql_select]
        # Au cas où :
        # for w in kw:
        #     if w in sql_select['value'] and 'name' not in sql_select:
        #         correct = False
        #         d = format({'select': sql_select['value'][w]})[7:]
        #         statut.append(AliasManquant(w, d, m))
        #         m = 0
        # return correct, statut
    for item in sql_select:
        for w in kw:
            if w in item['value'] and 'name' not in item:
                correct = False
                d = format({'select': item['value'][w]})[7:]
                statut.append(AliasManquant(w, d, m))
                m = 0
    return correct, statut


def check_tables(sql, solutions) -> Tuple[bool, List[Statut]]:
    sql_from = sql['from']
    tables_solution = solutions['from']
    correct = True
    statut = []
    if not isinstance(sql_from, list):
        sql_from = [sql_from]
    manque = 9999
    exces = 9999
    prop = []
    for token in sql_from:
        if isinstance(token, dict):
            prop.append(token['value'].upper())
        else:
            prop.append(token.upper())
    for sol in tables_solution:
        sol = sorted([x.upper() for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = min(exces, len(prop) - len(c))
        # TODO: vérifier les jointures et donc récupérer ce qui dépasse
    if exces > 0:
        correct = False
        statut.append(TableEnExces(exces))
    if manque > 0:
        correct = False
        statut.append(TableManquante(manque))
    return correct, statut


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
        solutions['requete'] = []
        solutions['requete_txt'] = [s for s in solutions_sql if s != '']
        for stmt in solutions_sql:
            if stmt != '':
                sql = parse(stmt)
                solutions['requete'].append(sql)
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


def check_where(sql, solutions) -> Tuple[bool, List[Statut]]:
    correct = True
    statut = []
    return correct, statut


def check_alias_table(sql) -> Tuple[bool, List[Statut]]:
    sql_from = sql['from']
    liste_noms = []
    liste_alias = []
    correct = True
    check_alias = True
    check_table = True
    statut = []
    for token in sql_from:
        if isinstance(token, dict):
            # Vérifier qu'il n'y a pas deux fois le même alias
            alias = token['name']
            if alias in liste_alias and check_alias:
                correct = False
                check_alias = False
                statut.append(AliasRepete())
            else:
                liste_alias.append(alias)
        else:
            # Vérifier qu'il n'y a pas deux fois la même table sans alias
            nom = token
            if nom in liste_noms and check_table:
                correct = False
                check_table = False
                statut.append(TableRepetee())
            else:
                liste_noms.append(nom)
    return correct, statut


def check_ob(sql, solutions) -> Tuple[bool, List[Statut]]:
    # Comparer avec la solution
    # -- colonne doit être soit un dans le SELECT (colonne, calcul ou alias)(, soit dans le GROUP BY, soit un index).
    # -- vérifier si dans une des solutions (construire variantes orthogonales)
    correct = True
    statut = []
    solutions_ob = []
    s = 0
    for sol in solutions['requete']:
        cr_flag = False
        i = 0
        if len(solutions_ob) == 0:
            cr_flag = True
        if 'orderby' in sol.keys():
            sol_ob = sol['orderby']
            if not isinstance(sol['orderby'], list):
                sol_ob = [sol['orderby']]
            for token in sol_ob:
                if cr_flag:
                    solutions_ob.append(set())
                if isinstance(token['value'], dict):
                    token_val = str(token['value'])
                elif '.' in token['value']:
                    token_val = token['value'].split('.')[1]
                else:
                    token_val = token['value']
                    # Dans ce cas, cela pourrait être un alias, on cherche dans la solution courante
                    # la formule cachée et on la stocke à la place
                    sel = solutions['requete'][s]['select']
                    if not isinstance(sel, list):
                        sel = [sel]
                    for col in sel:
                        c = col.get('name', col['value'])
                        if c == token['value']:
                            token_val = str(col['value'])
                solutions_ob[i].add((token_val, token.get('sort', 'asc')))
                i += 1
        s += 1
    if len(solutions_ob) == 0:
        return correct, statut
    if 'orderby' not in sql:
        correct = False
        statut.append(OrderByAbsent(len(solutions_ob), 0.5))
        return correct, statut
    prop_ob = []
    sql_ob = sql['orderby']
    if not isinstance(sql_ob, list):
        sql_ob = [sql_ob]
    for token in sql_ob:
        if isinstance(token['value'], dict):
            token_val = str(token['value'])
        elif '.' in token['value']:
            token_val = token['value'].split('.')[1]
        else:
            token_val = token['value']
            # Dans ce cas, cela pourrait être un alias, on cherche dans la solution courante
            # la formule cachée et on la stocke à la place
            sel = sql['select']
            if not isinstance(sel, list):
                sel = [sel]
            for col in sel:
                c = col.get('name', col['value'])
                if c == token['value']:
                    token_val = str(col['value'])
        prop_ob.append((token_val, token.get('sort', 'asc')))
    exces = 0  # max(len(prop_ob) - len(solutions_ob), 0)
    manque = 0  # max(len(prop_ob) - len(solutions_ob), 0)
    sorts = 0
    desordre = False
    # On va créer des listes :
    # - les colonnes présentes indépendamment de l'ordre et du tri => manque +x
    liste_col_ob_sol = []
    liste_col_ob_sol_sort = []
    liste_col_ob_sql = []
    for token in solutions_ob:
        entry = []
        for poss in token:
            col, sort = poss
            entry.append(col.upper())
            liste_col_ob_sol_sort.append({col.upper(): sort.upper()})
        liste_col_ob_sol.append(entry)
    for token in prop_ob:
        col, sort = token
        liste_col_ob_sql.append(col.upper())
    for token in liste_col_ob_sol:
        if all(entry not in liste_col_ob_sql for entry in token):
            manque += 1
    # - Les colonnes inutiles => exces +x
    for col in liste_col_ob_sql:
        if col not in [list(x.keys())[0] for x in liste_col_ob_sol_sort]:
            exces += 1
    # - Les colonnes présentes avec le mauvais tri => sorts +x
    for token in prop_ob:
        col, sort = token
        col = col.upper()
        sort = sort.upper()
        for entry in liste_col_ob_sol_sort:
            if col in entry.keys() and sort != entry[col]:
                sorts += 1
    if exces == 0 and manque == 0:
        for i in range(len(prop_ob)):
            col, _ = prop_ob[i]
            col = col.upper()
            sols = [sol[0].upper() for sol in solutions_ob[i]]
            if col not in sols:
                desordre = True
    if exces > 0:
        correct = False
        statut.append(OrderByExces(exces))
    if manque > 0:
        correct = False
        statut.append(OrderByManque(manque))
    if sorts > 0:
        correct = False
        statut.append(OrderByMalTrie(sorts))
    if desordre:
        correct = False
        statut.append(OrderByDesordre())
    return correct, statut


def check_gb(sql, solutions) -> Tuple[bool, List[Statut]]:
    correct = True
    statut = []
    agregats = ['count', 'sum', 'avg', 'min', 'max']
    if not isinstance(solutions['requete'], list):
        solutions = [solutions['requete']]
    else:
        solutions = solutions['requete']
    if not isinstance(sql['select'], list):
        sql_select = [sql['select']]
    else:
        sql_select = sql['select']
    if not (any('groupby' in sol.keys() and len(sol['groupby']) for sol in solutions)):
        # Pas de GB dans les solutions
        if 'groupby' in sql.keys():
            # GROUP BY inutile
            correct = False
            statut.append(GroupByInutile())
        return correct, statut
    if all('groupby' in sol.keys() and len(sol['groupby']) for sol in solutions):
        # Forcément GB dans la solution
        if 'groupby' not in sql.keys():
            correct = False
            nb_col = min(len(sol['groupby']) for sol in solutions)
            statut.append(GroupByAbsent(nb_col))
            return correct, statut
        else:
            return exces_manque_gb(agregats, solutions, sql, sql_select)
    # Troisième branche : il y a une/+ solution avec et une/+ sans
    # Sous-cas #1 : pas de group by dans la proposition
    ag_select = []
    for token in sql_select:
        if isinstance(token, dict) and any(
                isinstance(token['value'], dict) and ag in token['value'].keys() for ag in agregats):
            ag_select.append(token)
    if 'groupby' not in sql.keys():
        # -- Si pas d'agrégat dans le select et pas de having  => return 0, 0, False
        if len(ag_select) == 0 and 'having' not in sql.keys():
            return correct, statut
        # -- Si pas d'agrégat dans le select mais having present : return 0, 0, False (sera analyse par check_having)
        if len(ag_select) == 0 and 'having' in sql.keys():
            return correct, statut
        # -- Si agrégat dans le select => manque N => return 0, N, False, False
        nb_col = 9999
        for sol in solutions:
            if 'groupby' in sol.keys():
                correct = False
                nb_col = min(nb_col, len(sol['groupby']))
                statut.append(GroupByAbsent(nb_col))
        return correct, statut
    else:
        # Sous-cas #2 :
        # -- group by sans agrégat => (0, 0, True)
        if len(ag_select) == 0 and 'having' not in sql.keys():
            correct = False
            statut.append(GroupBySansAgregat())
            return correct, statut
        # -- group by dans la proposition => comparer avec solutions à group by => exces/manque/ok
        solutions_gb = []
        for sol in solutions:
            if 'groupby' in sol.keys() and len(sol['groupby']):
                solutions_gb.append(sol)
        return exces_manque_gb(agregats, solutions_gb, sql, sql_select)


def exces_manque_gb(agregats, solutions, sql, sql_select) -> Tuple[bool, List[Statut]]:
    exces = 0
    manque = 9999
    correct = True
    statut = []
    if not isinstance(sql['groupby'], list):
        sql_gb = [sql['groupby']]
    else:
        sql_gb = sql['groupby']
    prop_gb = []
    for token in sql_gb:
        if isinstance(token, dict):
            prop_gb.append(str(token['value'].split('.')[-1]))
        else:
            prop_gb.append(str(token))
    for sol in solutions:
        if not isinstance(sol['groupby'], list):
            sol_gb = [sol['groupby']]
        else:
            sol_gb = sol['groupby']
        sol_s = sorted([str(x['value'].split('.')[-1]) for x in sol_gb if sol])
        from collections import Counter
        c = list((Counter(sol_s) & Counter(prop_gb)).elements())
        manque = min(manque, len(sol_s) - len(c))
        exces = max(exces, len(prop_gb) - len(c))
    if manque:
        prop_select = []
        for token in sql_select:
            if isinstance(token, dict):
                if not any(isinstance(token['value'], dict) and ag in token['value'].keys() for ag in agregats):
                    prop_select.append(str(token['value']))
            else:
                prop_select.append(str(token))
        if all(token in prop_gb for token in prop_select):
            # Il manque probablement juste un identifiant dans le GB pour couvrir contre les homonymes
            manque = manque / 2.0
    if manque > 0:
        correct = False
        statut.append(GroupByManque(manque))
    if exces > 0:
        correct = False
        statut.append(GroupByExces(exces))
    return correct, statut


def check_having(sql, solutions) -> Tuple[bool, List[Statut]]:
    sols = solutions
    correct = True
    statut = []
    if not isinstance(solutions, list):
        sols = [solutions]
    if 'having' in sql.keys() and 'groupby' not in sql.keys():
        correct = False
        statut.append(HavingSansGB())
        return correct, statut
    if all(('having' in sol.keys() and len(sol['having'])) for sol in sols) and 'having' not in sql.keys():
        min_having = 9999
        for sol in sols:
            s = sol['having']
            if not isinstance(sol['having'], list):
                s = [sol['having']]
            min_having = min(min_having, len(s))
        manque = min_having
        if manque > 0:
            correct = False
            statut.append(HavingManquant(manque))
        return correct, statut
    if not any('having' in sol.keys() and len(sol['having']) for sol in sols) and 'having' in sql.keys():
        correct = False
        statut.append(HavingInutile())
        return correct, statut
    # TODO: calculer manque et exces dans le cas où partiellement bon/faux
    return correct, statut


def check_select(sql, solutions) -> Tuple[bool, List[Statut]]:
    sql_select = sql['select']
    correct = True
    statut = []
    if not isinstance(sql_select, list):
        sql_select = [sql_select]
    # SELECT * au lieu de colonnes précises
    if sql_select[0] == '*' and '*' not in solutions['select']:
        correct = False
        statut.append(SelectEtoile())
        return correct, statut

    # Excès et/ou manque
    exces = 9999
    manque = 9999
    prop = []
    for token in sql_select:
        if isinstance(token, dict):
            prop.append(str(token['value']).split('.')[-1])
        else:
            prop.append(str(token))
    for sol in solutions['select']:
        sol = sorted([str(x).split('.')[-1] for x in sol])
        from collections import Counter
        c = list((Counter(sol) & Counter(prop)).elements())
        manque = min(manque, len(sol) - len(c))
        exces = min(exces, len(prop) - len(c))

    # Désordre = toutes les colonnes mais pas dans le bon ordre
    if not manque and not exces:
        desordre = True
        for sol in solutions['select']:
            sol = [str(x).split('.')[-1] for x in sol]
            if desordre and len(sol) == len(prop) and all(sol[i] == prop[i] for i in range(len(sol))):
                desordre = False
        if desordre:
            correct = False
            statut.append(SelectDesordre())
        return correct, statut
    else:
        correct = False
    if manque > 0:
        statut.append(SelectManque(manque))
    if exces > 0:
        statut.append(SelectExces(exces))
    return correct, statut


def check_syntax(stmt) -> Tuple[bool, Statut]:
    try:
        sql = parse(stmt)
        return True, StatutOk(sql)
    except ParseException as e:
        ligne = e.lineno
        col = e.col
        return False, ErreurParsing(ligne, col, e.line)


def check_run(stmt, conn) -> Tuple[bool, Statut]:
    import threading
    correct = True
    seconds = 15

    t = threading.Timer(seconds, conn.connection.interrupt)
    t.start()
    try:
        rs = conn.execute(stmt)
        statut = RequeteOk(rs)
    except OperationalError as e:  # pragma: nocover
        correct = False
        if str(e.orig) == 'interrupted':
            statut = RequeteInterrompue()
        else:
            t.cancel()
            raise e
    t.cancel()
    return correct, statut


def parse_requete(fichier, db, solutions):
    engine = create_engine('sqlite:///' + db, echo=False)
    # create a configured "Session" class
    bound_session = sessionmaker(bind=engine)

    # create a Session
    session = bound_session()
    conn = session.connection()
    statuts: dict = {}
    with open(fichier, 'r') as r:
        stmt = r.read()
        stmt = sqlparse.split(stmt)[0]

        correct, statuts['syntax'] = check_syntax(stmt)
    if correct:
        sql = statuts['syntax'].sql

        # Analyser le SELECT
        select_correct, statuts['select'] = check_select(sql, solutions)
        correct = correct and select_correct

        # Vérification des étiquettes dans le SELECT en cas de COUNT/SUM/AVG/MIN/MAX
        label_correct, statuts['label'] = check_alias_agregat(sql)
        correct = correct and label_correct

        # Vérification des tables manquantes/en trop
        tables_correct, statuts['tables'] = check_tables(sql, solutions)
        correct = correct and tables_correct

        # Vérification des alias de tables
        alias_tables_correct, statuts['alias'] = check_alias_table(sql)
        correct = correct and alias_tables_correct

        # TODO: Vérification des conditions dans le WHERE
        where_correct, statuts['where'] = check_where(sql, solutions)
        correct = correct and where_correct

        # Vérification des colonnes dans le ORDER BY
        ob_correct, statuts['orderby'] = check_ob(sql, solutions)
        correct = correct and ob_correct

        # Vérification des colonnes dans le GROUP BY
        gb_correct, statuts['groupby'] = check_gb(sql, solutions)
        correct = correct and gb_correct

        # TODO: Vérification des conditions dans le HAVING (partiellement fait)
        having_correct, statuts['having'] = check_having(sql, solutions)
        correct = correct and having_correct

        # Exécution de la requete
        exe_correct, statuts['execution'] = check_run(stmt, conn)
        correct = correct and exe_correct
        statut_res = []
        if exe_correct:
            _, r = check_run(stmt, conn)
            rs = statuts['execution'].result_proxy
            statuts['execution'].set_resultat(parse_sql_rs_pretty(rs))
            exe_correct, statut_res = parse_sql_rs_data(r.result_proxy)
            statuts['parse'] = None
        if not exe_correct:
            statuts['parse'] = statut_res[1]
        else:
            arr_res_bon = []
            arr_msg = []
            if isinstance(solutions, list):
                sol = solutions[0]
            else:
                sol = solutions
            qsol = sol['requete_txt']
            rsol = [conn.execute(q) for q in qsol]
            statuts_sol = []
            for r in rsol:
                _, statut_sol = parse_sql_rs_data(r)
                statuts_sol.append(statut_sol[0])
            i = 1
            for s in statuts_sol:
                res_bon, statut = compare_sql(s, statut_res[0])
                arr_res_bon.append(res_bon)
                arr_msg.extend(["Solution n°" + str(i)])
                arr_msg.extend(list(x.message for x in statut))
                i += 1
            if all(arr_res is False for arr_res in arr_res_bon):
                correct = False
                statuts['execution'].set_messages(arr_msg)
                statuts['execution'].set_malus(0.5)

    return correct, statuts


def parse_args(argv):
    parser = argparse.ArgumentParser(prog='sql-autocorrect')
    parser.add_argument("-f", type=str, required=True,
                        help="Fichier à analyser", metavar='FICHIER')
    parser.add_argument("-s", type=str, required=True,
                        help="Fichier de solution(s)", metavar='FICHIER')
    parser.add_argument("-r", type=str, required=True,
                        help="Fichier dans lequel stocker le résultat", metavar='FICHIER')
    parser.add_argument('-db', type=str, required=True,
                        help="Base sur laquelle exécuter la requête", metavar='BDD')
    args = parser.parse_args(argv)
    return args


def save_result(r, correct, statuts):
    with open(r, 'wb') as f:
        pickle.dump([correct, statuts], f)


def main():  # pragma: nocover
    args = parse_args(sys.argv[1:])
    solutions = parse_solutions(args.s)
    correct, statuts = parse_requete(args.f, args.db, solutions)
    save_result(args.r, correct, statuts)


if __name__ == '__main__':  # pragma: nocover
    main()
