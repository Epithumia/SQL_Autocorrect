import unittest

import sqlparse
from moz_sql_parser import parse

from sql_autocorrect.cli import parse_solutions, check_select, check_tables, check_gb, check_alias_agregat, check_ob, \
    check_alias_table, check_having


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_select_ok(self):
        with open('tests/requetes/select_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql, solutions), (0, 0, False, False))

    def test_select_etoile(self):
        with open('tests/requetes/select_etoile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql, solutions), (0, 0, False, True))

    def test_select_exces(self):
        with open('tests/requetes/select_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql, solutions), (1, 0, False, False))

    def test_select_manque(self):
        with open('tests/requetes/select_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql, solutions), (0, 1, False, False))

    def test_select_desordre(self):
        with open('tests/requetes/select_desordre.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql, solutions), (0, 0, True, False))

    def test_from_ok(self):
        with open('tests/requetes/from_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql, solutions), (0, 0))

    def test_from_exces(self):
        with open('tests/requetes/from_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql, solutions), (1, 0))

    def test_from_manque(self):
        with open('tests/requetes/from_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql, solutions), (0, 2))

    def test_groupby_seul_ok(self):
        with open('tests/requetes/groupby_seul_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False))

    def test_groupby_seul_exces(self):
        with open('tests/requetes/groupby_seul_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (1, 0, False))

    def test_groupby_seul_manque(self):
        with open('tests/requetes/groupby_seul_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 1, False))

    def test_groupby_seul_semi_manque(self):
        with open('tests/requetes/groupby_seul_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0.5, False))

    def test_groupby_seul_absent(self):
        with open('tests/requetes/groupby_seul_absent.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 2, False))

    def test_groupby_simple_ok(self):
        with open('tests/requetes/groupby_simple_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False))

    def test_groupby_simple_inutile(self):
        with open('tests/requetes/groupby_simple_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, True))

    def test_groupby_mix_ok1(self):
        with open('tests/requetes/groupby_mix_ok1.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False))

    def test_groupby_mix_manque(self):
        with open('tests/requetes/groupby_mix_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 1, False))

    def test_groupby_mix_semi_manque(self):
        with open('tests/requetes/groupby_mix_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0.5, False))

    def test_groupby_mix_exces(self):
        with open('tests/requetes/groupby_mix_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (1, 0, False))

    def test_groupby_mix_ok2(self):
        with open('tests/requetes/groupby_mix_ok2.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False))

    def test_groupby_mix_groupby_inutile(self):
        with open('tests/requetes/groupby_mix_groupby_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, True))

    def test_groupby_mix_agregat_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_select_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 2, False))

    def test_groupby_mix_having_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_having_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False))

    def test_alias_agregat_simple_ok(self):
        with open('tests/requetes/alias_agregat_simple_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertTupleEqual(check_alias_agregat(sql), ('', 0))

    def test_alias_agregat_simple_manque(self):
        with open('tests/requetes/alias_agregat_simple_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertTupleEqual(check_alias_agregat(sql), ("COUNT(*) : mettez un alias", -0.25))

    def test_alias_agregat_mix_ok(self):
        with open('tests/requetes/alias_agregat_mix_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertTupleEqual(check_alias_agregat(sql), ('', 0))

    def test_alias_agregat_mix_semi_manque(self):
        with open('tests/requetes/alias_agregat_mix_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertTupleEqual(check_alias_agregat(sql), ("COUNT(*) : mettez un alias", -0.25))

    def test_alias_agregat_mix_manque(self):
        with open('tests/requetes/alias_agregat_mix_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertTupleEqual(check_alias_agregat(sql), (
            "COUNT(*) : mettez un alias\nCOUNT(DISTINCT(NbNotesUtilisateurs)) : mettez un alias", -0.25))

    def test_orderby_ok(self):
        with open('tests/requetes/orderby_ok_alias.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        self.assertEqual(check_ob(sql, solutions), (0, 0, 0, False))

    def test_orderby_manque(self):
        with open('tests/requetes/orderby_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        self.assertEqual(check_ob(sql, solutions), (0, 5, 0, False))

    def test_orderby_manque_4(self):
        with open('tests/requetes/orderby_manque_4.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        self.assertEqual(check_ob(sql, solutions), (0, 4, 0, False))

    def test_orderby_err_mixte(self):
        with open('tests/requetes/orderby_err_mixte.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        self.assertEqual(check_ob(sql, solutions), (1, 2, 2, False))

    def test_orderby_desordre(self):
        with open('tests/requetes/orderby_desordre.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/orderby_solution.sql')
        self.assertEqual(check_ob(sql, solutions), (0, 0, 1, True))

    def test_alias_table_ok(self):
        with open('tests/requetes/alias_table_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertEqual(check_alias_table(sql), False)

    def test_alias_table_err_alias(self):
        with open('tests/requetes/alias_table_err_alias.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertEqual(check_alias_table(sql), True)

    def test_alias_table_err_table(self):
        with open('tests/requetes/alias_table_err_table.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        self.assertEqual(check_alias_table(sql), True)

    def test_having_ok(self):
        with open('tests/requetes/having_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        self.assertEqual(check_having(sql, solutions), (0, 0, False, False))

    def test_having_manquant(self):
        with open('tests/requetes/having_manquant.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        self.assertEqual(check_having(sql, solutions), (0, 1, False, False))

    def test_having_inutile(self):
        with open('tests/requetes/having_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertEqual(check_having(sql, solutions), (0, 0, False, True))

    def test_having_sans_gb(self):
        with open('tests/requetes/having_sans_gb.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        self.assertEqual(check_having(sql, solutions), (0, 0, True, False))
