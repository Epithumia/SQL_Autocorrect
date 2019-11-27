import unittest

import sqlparse
from moz_sql_parser import parse

from sql_autocorrect.cli import parse_solutions, check_select, check_tables


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
        self.assertTupleEqual(check_tables(sql['from'], solutions), (0, 1))
