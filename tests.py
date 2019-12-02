import unittest

import sqlparse
from moz_sql_parser import parse

from sql_autocorrect.cli import parse_solutions, check_select, check_tables, check_gb, check_alias_agregat


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_select_ok(self):
        with open('tests/requetes/select_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql['select'], solutions), (0, 0, False, False))

    def test_select_etoile(self):
        with open('tests/requetes/select_etoile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql['select'], solutions), (0, 0, False, True))

    def test_select_exces(self):
        with open('tests/requetes/select_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql['select'], solutions), (1, 0, False, False))

    def test_select_manque(self):
        with open('tests/requetes/select_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql['select'], solutions), (0, 1, False, False))

    def test_select_desordre(self):
        with open('tests/requetes/select_desordre.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        self.assertTupleEqual(check_select(sql['select'], solutions), (0, 0, True, False))

    def test_from_ok(self):
        with open('tests/requetes/from_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql['from'], solutions), (0, 0))

    def test_from_exces(self):
        with open('tests/requetes/from_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql['from'], solutions), (1, 0))

    def test_from_manque(self):
        with open('tests/requetes/from_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/from_solution.sql')
        self.assertTupleEqual(check_tables(sql['from'], solutions), (0, 2))

    def test_groupby_seul_ok(self):
        with open('tests/requetes/groupby_seul_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False, False))

    def test_groupby_seul_exces(self):
        with open('tests/requetes/groupby_seul_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (1, 0, False, False))

    def test_groupby_seul_manque(self):
        with open('tests/requetes/groupby_seul_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 1, False, False))

    def test_groupby_seul_semi_manque(self):
        with open('tests/requetes/groupby_seul_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0.5, False, False))

    def test_groupby_seul_absent(self):
        with open('tests/requetes/groupby_seul_absent.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_seul_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 2, False, False))

    def test_groupby_simple_ok(self):
        with open('tests/requetes/groupby_simple_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False, False))

    def test_groupby_simple_inutile(self):
        with open('tests/requetes/groupby_simple_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_simple_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, True, False))

    def test_groupby_mix_ok1(self):
        with open('tests/requetes/groupby_mix_ok1.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False, False))

    def test_groupby_mix_manque(self):
        with open('tests/requetes/groupby_mix_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 1, False, False))

    def test_groupby_mix_semi_manque(self):
        with open('tests/requetes/groupby_mix_semi_manque.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0.5, False, False))

    def test_groupby_mix_exces(self):
        with open('tests/requetes/groupby_mix_exces.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (1, 0, False, False))

    def test_groupby_mix_ok2(self):
        with open('tests/requetes/groupby_mix_ok2.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False, False))

    def test_groupby_mix_groupby_inutile(self):
        with open('tests/requetes/groupby_mix_groupby_inutile.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, True, False))

    def test_groupby_mix_agregat_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_select_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 2, False, False))

    def test_groupby_mix_having_sans_groupby(self):
        with open('tests/requetes/groupby_mix_agregat_having_sans_groupby.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
            sql = parse(stmt)
        solutions = parse_solutions('tests/requetes/groupby_mix_solution.sql')
        self.assertTupleEqual(check_gb(sql, solutions), (0, 0, False, False))

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
