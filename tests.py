import unittest

import sqlparse
from moz_sql_parser import parse

from sql_autocorrect.cli import parse_solutions, check_select, check_tables, check_gb, check_alias_agregat, check_ob, \
    check_alias_table, check_having
from sql_autocorrect.statut import *


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_select_ok(self):
        with open('tests/requetes/select_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_select(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_select_etoile(self):
        with open('tests/requetes/select_etoile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_select(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], SelectEtoile))

    def test_select_exces(self):
        with open('tests/requetes/select_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_select(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], SelectExces))
        self.assertEqual(statut[0].exces, 1)

    def test_select_manque(self):
        with open('tests/requetes/select_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_select(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], SelectManque))
        self.assertEqual(statut[0].manque, 1)

    def test_select_desordre(self):
        with open('tests/requetes/select_desordre.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_select(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], SelectDesordre))

    def test_from_ok(self):
        with open('tests/requetes/from_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        correct, statut = check_tables(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_from_exces(self):
        with open('tests/requetes/from_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        correct, statut = check_tables(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], TableEnExces))
        self.assertEqual(statut[0].exces, 1)

    def test_from_manque(self):
        with open('tests/requetes/from_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        correct, statut = check_tables(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], TableManquante))
        self.assertEqual(statut[0].manque, 2)

    def test_groupby_seul_ok(self):
        with open('tests/requetes/groupby_seul_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_groupby_seul_exces(self):
        with open('tests/requetes/groupby_seul_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByExces))
        self.assertEqual(statut[0].exces, 1)

    def test_groupby_seul_manque(self):
        with open('tests/requetes/groupby_seul_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByManque))
        self.assertEqual(statut[0].manque, 1)

    def test_groupby_seul_semi_manque(self):
        with open('tests/requetes/groupby_seul_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByManque))
        self.assertEqual(statut[0].manque, 0.5)

    def test_groupby_seul_absent(self):
        with open('tests/requetes/groupby_seul_absent.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByAbsent))
        self.assertEqual(statut[0].nb_col, 2)

    def test_groupby_simple_ok(self):
        with open('tests/requetes/groupby_simple_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_groupby_simple_inutile(self):
        with open('tests/requetes/groupby_simple_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByInutile))

    def test_groupby_mix_ok1(self):
        with open('tests/requetes/groupby_mix_ok1.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_groupby_mix_manque(self):
        with open('tests/requetes/groupby_mix_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByManque))
        self.assertEqual(statut[0].manque, 1)

    def test_groupby_mix_semi_manque(self):
        with open('tests/requetes/groupby_mix_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByManque))
        self.assertEqual(statut[0].manque, 0.5)

    def test_groupby_mix_exces(self):
        with open('tests/requetes/groupby_mix_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByExces))
        self.assertEqual(statut[0].exces, 1)

    def test_groupby_mix_ok2(self):
        with open('tests/requetes/groupby_mix_ok2.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_groupby_mix_groupby_inutile(self):
        with open('tests/requetes/groupby_mix_groupby_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupBySansAgregat))

    def test_groupby_mix_agregat_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_select_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], GroupByAbsent))
        self.assertEqual(statut[0].nb_col, 2)

    def test_groupby_mix_having_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_having_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        correct, statut = check_gb(sql, solutions)
        print(statut)
        self.assertEqual(correct, True)  # Vérifié par check HAVING
        self.assertEqual(len(statut), 0)

    def test_alias_agregat_simple_ok(self):
        with open('tests/requetes/alias_agregat_simple_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_agregat(sql)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_alias_agregat_simple_manque(self):
        with open('tests/requetes/alias_agregat_simple_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_agregat(sql)
        self.assertEqual(correct, False)
        self.assertEqual(statut[0].malus, 0.25)
        self.assertEqual(statut[0].message, "COUNT(*) : mettez un alias")

    def test_alias_agregat_mix_ok(self):
        with open('tests/requetes/alias_agregat_mix_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_agregat(sql)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_alias_agregat_mix_semi_manque(self):
        with open('tests/requetes/alias_agregat_mix_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_agregat(sql)
        self.assertEqual(correct, False)
        self.assertEqual(statut[0].malus, 0.25)
        self.assertEqual(statut[0].message, "COUNT(*) : mettez un alias")

    def test_alias_agregat_mix_manque(self):
        with open('tests/requetes/alias_agregat_mix_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_agregat(sql)
        self.assertEqual(correct, False)
        malus = sum(x.malus for x in statut)
        self.assertEqual(malus, 0.25)
        self.assertEqual(statut[0].message, "COUNT(*) : mettez un alias")
        self.assertEqual(statut[1].message, "COUNT(DISTINCT(NbNotesUtilisateurs)) : mettez un alias")

    def test_orderby_ok(self):
        with open('tests/requetes/orderby_ok_alias.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        correct, statut = check_ob(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_orderby_manque(self):
        with open('tests/requetes/orderby_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        correct, statut = check_ob(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], OrderByAbsent))
        self.assertEqual(statut[0].nb_col, 5)

    def test_orderby_manque_4(self):
        with open('tests/requetes/orderby_manque_4.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        correct, statut = check_ob(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], OrderByManque))
        self.assertEqual(statut[0].manque, 4)

    def test_orderby_err_mixte(self):
        with open('tests/requetes/orderby_err_mixte.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        correct, statut = check_ob(sql, solutions)
        self.assertTrue(len(statut), 3)
        self.assertTrue(isinstance(statut[0], OrderByExces))
        self.assertEqual(statut[0].exces, 1)
        self.assertTrue(isinstance(statut[1], OrderByManque))
        self.assertEqual(statut[1].manque, 2)
        self.assertTrue(isinstance(statut[2], OrderByMalTrie))
        self.assertEqual(statut[2].nb_col, 2)

    def test_orderby_desordre(self):
        with open('tests/requetes/orderby_desordre.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        correct, statut = check_ob(sql, solutions)
        self.assertEqual(correct, False)
        self.assertEqual(len(statut), 2)
        self.assertTrue(isinstance(statut[0], OrderByMalTrie))
        self.assertEqual(statut[0].nb_col, 1)
        self.assertTrue(isinstance(statut[1], OrderByDesordre))

    def test_alias_table_ok(self):
        with open('tests/requetes/alias_table_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_table(sql)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_alias_table_err_alias(self):
        with open('tests/requetes/alias_table_err_alias.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_table(sql)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], AliasRepete))

    def test_alias_table_err_table(self):
        with open('tests/requetes/alias_table_err_table.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        correct, statut = check_alias_table(sql)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], TableRepetee))

    def test_having_ok(self):
        with open('tests/requetes/having_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        correct, statut = check_having(sql, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    def test_having_manquant(self):
        with open('tests/requetes/having_manquant.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        correct, statut = check_having(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], HavingManquant))
        self.assertEqual(statut[0].manque, 1)

    # TODO : calculer manque et exces dans le cas où partiellement bon/faux
    # def test_having_exces(self):
    #     with open('tests/requetes/having_exces.sql', 'r') as r:
    #         stmt = r.read()
    #         stmt = sqlparse.split(stmt)[0]
    #         sql = parse(stmt)
    #     solutions = parse_solutions('tests/requetes/having_solution.sql')
    #     correct, statut = check_having(sql, solutions)
    #     self.assertEqual(correct, False)
    #     self.assertTrue(isinstance(statut[0], HavingExces))
    #     self.assertEqual(statut[0].exces, 1)
    #     # self.assertEqual(check_having(sql, solutions), (1, 0, False, False))
    #
    # def test_having_manque1(self):
    #     with open('tests/requetes/having_manque1.sql', 'r') as r:
    #         stmt = r.read()
    #         stmt = sqlparse.split(stmt)[0]
    #         sql = parse(stmt)
    #     solutions = parse_solutions('tests/requetes/having_solution2.sql')
    #     correct, statut = check_having(sql, solutions)
    #     self.assertEqual(correct, False)
    #     self.assertTrue(isinstance(statut[0], HavingManquant))
    #     self.assertEqual(statut[0].manque, 1)

    def test_having_inutile(self):
        with open('tests/requetes/having_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = check_having(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], HavingInutile))

    def test_having_sans_gb(self):
        with open('tests/requetes/having_sans_gb.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        correct, statut = check_having(sql, solutions)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut[0], HavingSansGB))
