import unittest

import pytest
import sqlparse
from moz_sql_parser import parse

from sql_autocorrect.cli.parser import parse_solutions, check_select, check_tables, check_gb, check_alias_agregat, \
    check_ob, check_alias_table, check_having, check_syntax, check_where, parse_args, parse_requete, save_result
from sql_autocorrect.cli.reader import parse_affiche_args, affichage, load_result
from sql_autocorrect.models.statut import *


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        import os
        if os.path.exists("tests/temp.sqlac"):
            os.remove("tests/temp.sqlac")

    # Parser
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

    def test_syntax_ok(self):
        with open('tests/requetes/having_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
        correct, statut = check_syntax(stmt)
        self.assertEqual(correct, True)
        self.assertTrue(isinstance(statut, StatutOk))

    def test_syntax_error(self):
        with open('tests/requetes/test_parse_exception.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
        correct, statut = check_syntax(stmt)
        self.assertEqual(correct, False)
        self.assertTrue(isinstance(statut, ErreurParsing))
        msg = 'Erreur à la ligne 6, colonne 12 :\n<and J.rang not null>\n            ^'
        self.assertEqual(statut.message, msg)

    def test_check_run(self):
        self.assertTrue(True)  # Couvert par test_check_parse_requete

    def test_check_where(self):
        with open('tests/requetes/having_ok.sql', 'r') as r:
            stmt = r.read()
            stmt = sqlparse.split(stmt)[0]
        solutions = parse_solutions('tests/requetes/having_solution.sql')
        correct, statut = check_where(stmt, solutions)
        self.assertEqual(correct, True)
        self.assertEqual(len(statut), 0)

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_check_parse_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['test']
            parse_args(argv)
        self.assertEqual(pytest_wrapped_e.value.code, 2)
        msg = 'usage: sql-autocorrect [-h] -f FICHIER -s FICHIER -r FICHIER -db BDD\nsql-autocorrect: error: the following arguments are required: -f, -s, -r, -db\n'
        out, err = self.capsys.readouterr()
        self.assertEqual(err, msg)
        argv = ['-f', 'tests/requetes/from_ok.sql', '-s', 'tests/requetes/from_ok.sql', '-r', 'tests/resultat.sqlac',
                '-db', 'tests/bases/bgg_large.db']
        args = parse_args(argv)
        self.assertEqual(args.f, 'tests/requetes/from_ok.sql')
        self.assertEqual(args.s, 'tests/requetes/from_ok.sql')
        self.assertEqual(args.r, 'tests/resultat.sqlac')
        self.assertEqual(args.db, 'tests/bases/bgg_large.db')

    def test_check_parse_requete(self):
        fichier = 'tests/requetes/test_mem_limit.sql'
        db = 'tests/bases/bgg_large.db'
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = parse_requete(fichier, db, solutions)
        self.assertFalse(correct)
        self.assertTrue(isinstance(statut['syntax'], StatutOk))
        self.assertTrue(isinstance(statut['parse'], MaxLignes))
        fichier = 'tests/requetes/test_parse_exception.sql'
        solutions = parse_solutions('tests/requetes/select_solution.sql')
        correct, statut = parse_requete(fichier, db, solutions)
        self.assertFalse(correct)
        self.assertTrue(isinstance(statut['syntax'], ErreurParsing))
        self.assertEqual(statut['syntax'].message,
                         'Erreur à la ligne 6, colonne 12 :\n<and J.rang not null>\n            ^')
        fichier = 'tests/requetes/test0.sql'
        db = 'tests/bases/bgg_large.db'
        solutions = parse_solutions('tests/requetes/solution0.sql')
        correct, statut = parse_requete(fichier, db, solutions)
        self.assertFalse(correct)
        self.assertIsInstance(statut['syntax'], StatutOk)
        self.assertIsInstance(statut['select'][0], SelectExces)
        self.assertIsInstance(statut['label'][0], AliasManquant)
        self.assertIsInstance(statut['label'][1], AliasManquant)
        self.assertIsInstance(statut['tables'][0], TableEnExces)
        self.assertEqual(len(statut['alias']), 0)
        self.assertEqual(len(statut['where']), 0)
        self.assertEqual(len(statut['groupby']), 0)
        self.assertEqual(len(statut['having']), 0)
        self.assertIsInstance(statut['orderby'][0], OrderByExces)
        self.assertIsInstance(statut['orderby'][1], OrderByManque)
        self.assertIsInstance(statut['execution'], RequeteOk)
        fichier = 'tests/requetes/test1.sql'
        db = 'tests/bases/bgg_large.db'
        solutions = parse_solutions('tests/requetes/solution1.sql')
        correct, statut = parse_requete(fichier, db, solutions)
        self.assertTrue(correct)
        self.assertIsInstance(statut['syntax'], StatutOk)
        self.assertIsInstance(statut['execution'], RequeteOk)
        self.assertEqual(len(statut['select']), 0)
        self.assertEqual(len(statut['label']), 0)
        self.assertEqual(len(statut['tables']), 0)
        self.assertEqual(len(statut['alias']), 0)
        self.assertEqual(len(statut['where']), 0)
        self.assertEqual(len(statut['orderby']), 0)
        self.assertEqual(len(statut['groupby']), 0)
        self.assertEqual(len(statut['having']), 0)
        self.assertIsNone(statut['parse'])
        res = '''+--------+---------------------------------------------------------+
| IdJeu  |                          NomJeu                         |
+--------+---------------------------------------------------------+
| 174430 |                        Gloomhaven                       |
| 180263 |                    The 7th Continent                    |
| 96848  |                  Mage Knight Board Game                 |
| 205059 |           Mansions of Madness: Second Edition           |
| 221107 |                Pandemic Legacy: Season 2                |
| 233398 |                  Endeavor: Age of Sail                  |
| 187617 |               Nemo's War (Second Edition)               |
| 150997 |          Shadows of Brimstone: Swamps of Death          |
| 240196 |                     Betrayal Legacy                     |
| 257518 |                   Claustrophobia 1643                   |
| 276025 |                        Maracaibo                        |
| 262211 |                        Cloudspire                       |
| 169427 |           Middara: Unintentional Malum – Act 1          |
| 266121 |                Unlock! Heroic Adventures                |
| 243759 |                 Hellboy: The Board Game                 |
| 264198 |           Warhammer Quest: Blackstone Fortress          |
| 210232 |            Dungeon Degenerates: Hand of Doom            |
| 242653 |                         Mysthea                         |
| 248949 |                 Skull Tales: Full Sail!                 |
| 140125 |                          Fallen                         |
| 154910 |                 Darklight: Memento Mori                 |
| 212346 |         Shadows of Brimstone: Forbidden Fortress        |
| 264220 |            Tainted Grail: The Fall of Avalon            |
| 184267 |                         On Mars                         |
| 264196 | Dungeons & Dragons: Waterdeep – Dungeon of the Mad Mage |
+--------+---------------------------------------------------------+'''
        self.assertEqual(statut['execution'].resultat, res)
        fichier = 'tests/requetes/test_res_diff.sql'
        db = 'tests/bases/bgg_large.db'
        solutions = parse_solutions('tests/requetes/test_res_ok.sql')
        correct, statut = parse_requete(fichier, db, solutions)
        self.assertFalse(correct)
        self.assertIsInstance(statut['syntax'], StatutOk)
        self.assertIsInstance(statut['select'][0], SelectManque)
        self.assertIsInstance(statut['select'][1], SelectExces)
        self.assertEqual(len(statut['label']), 0)
        self.assertEqual(len(statut['tables']), 0)
        self.assertEqual(len(statut['alias']), 0)
        self.assertEqual(len(statut['where']), 0)
        self.assertEqual(len(statut['groupby']), 0)
        self.assertEqual(len(statut['having']), 0)
        self.assertEqual(len(statut['orderby']), 0)
        self.assertIsInstance(statut['execution'], RequeteOk)
        msg = 'Les résultats sont différents : [2.0339146936917394, 2019, 84826] <> [2.4521738653748066, 2019, 84826]'
        self.assertEqual(statut['execution'].messages[1], msg)

    def test_compare_sql(self):
        self.assertTrue(True)  # Couvert par test_check_parse_requete

    def test_parse_sql_rs_data(self):
        self.assertTrue(True)  # Couvert par test_check_parse_requete

    def test_parse_sql_rs_pretty(self):
        self.assertTrue(True)  # Couvert par test_check_parse_requete

    # Reader
    def test_affichage(self):
        argv = ['-r', 'tests/resultat_parse_exception.sqlac',
                '-g', '-c', '-res']
        args = parse_affiche_args(argv)
        correct, statuts = load_result(args.r)
        affichage(args, correct, statuts)
        out, err = self.capsys.readouterr()
        self.assertEqual(out, 'Erreur à la ligne 6, colonne 12 :\n<and J.rang not null>\n            ^\n-100\n')

        argv = ['-r', 'tests/resultat_max_lignes.sqlac',
                '-g', '-c', '-res']
        args = parse_affiche_args(argv)
        correct, statuts = load_result(args.r)
        affichage(args, correct, statuts)
        out, err = self.capsys.readouterr()
        self.assertTrue('Le nombre maximum de lignes est atteint' in out)

        argv = ['-r', 'tests/resultat_diff.sqlac',
                '-g', '-c', '-res']
        args = parse_affiche_args(argv)
        correct, statuts = load_result(args.r)
        affichage(args, correct, statuts)
        out, err = self.capsys.readouterr()
        self.assertTrue(
            'Les résultats sont différents : [2.0339146936917394, 2019, 84826] <> [2.4521738653748066, 2019, 84826]' in out)

        argv = ['-r', 'tests/resultat_ok.sqlac',
                '-g', '-c', '-res']
        args = parse_affiche_args(argv)
        correct, statuts = load_result(args.r)
        affichage(args, correct, statuts)
        out, err = self.capsys.readouterr()
        self.assertTrue('Pas de remarques sur la requête' in out)
        self.assertTrue('| IdJeu  |                          NomJeu                         |' in out)
        self.assertTrue('| 174430 |                        Gloomhaven                       |' in out)
        self.assertEqual('0', out[-2])

    def test_parse_affiche_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['test']
            parse_affiche_args(argv)
        self.assertEqual(pytest_wrapped_e.value.code, 2)
        msg = 'usage: sql-ac-res [-h] -r FICHIER [-g] [-c] [-res]\nsql-ac-res: error: the following arguments are required: -r\n'
        out, err = self.capsys.readouterr()
        self.assertEqual(err, msg)
        argv = ['-r', 'tests/resultat.sqlac',
                '-g', '-c', '-res']
        args = parse_affiche_args(argv)
        self.assertEqual(args.r, 'tests/resultat.sqlac')
        self.assertEqual(args.g, True)
        self.assertEqual(args.c, True)
        self.assertEqual(args.res, True)

    # Common
    def test_check_save_load(self):
        argv = ['-r', 'tests/resultat_diff.sqlac']
        args = parse_affiche_args(argv)
        correct, statuts = load_result(args.r)
        save_result('tests/temp.sqlac', correct, statuts)
        argv = ['-r', 'tests/temp.sqlac']
        args = parse_affiche_args(argv)
        correct2, statuts2 = load_result(args.r)
        print(hash(statuts['syntax']))
        self.assertEqual(correct, correct2)
        self.assertDictEqual(statuts, statuts2)
