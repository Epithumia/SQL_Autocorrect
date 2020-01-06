class Statut:
    def __init__(self):
        self.message = ''
        self.malus = 0.0
        self.exces = None
        self.manque = None
        self.attendu = None
        self.obtenu = None
        self.code = None
        self.col_name = None
        self.nb_col = None
        self.sql = None
        self.result_proxy = None
        self.resultat = None
        self.data = None
        self.messages = []

    def __repr__(self):
        r = str(type(self)) + '<' + str(self.code) + '> - <' + self.message + '>'
        if self.malus is not None:
            r += ' malus<' + str(self.malus) + '>'
        if self.exces is not None:
            r += 'exces<' + str(self.exces) + '>'
        if self.manque is not None:
            r += 'manque<' + str(self.manque) + '>'
        if self.attendu is not None:
            r += 'attendu<' + str(self.attendu) + '>'
        if self.obtenu is not None:
            r += 'obtenu<' + str(self.obtenu) + '>'
        if self.sql is not None:
            r += 'sql<' + str(self.sql) + '>'
        if self.data is not None:
            r += 'data<' + str(self.data) + '>'
        if len(self.messages):
            r += 'messages<' + str(self.messages) + '>'

        return r

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if type(self) is type(other):
            return str(self) == str(other)
        return False


class StatutOk(Statut):
    def __init__(self, sql):
        super().__init__()
        self.message = 'OK'
        self.code = -1
        self.sql = sql


class RequeteOk(Statut):
    def __init__(self, rs):
        super().__init__()
        self.code = -1
        self.result_proxy = rs
        self.malus = 0.0

    def set_resultat(self, resultat):
        self.resultat = str(resultat)
        self.result_proxy = None

    def set_messages(self, messages):
        self.messages = messages

    def set_malus(self, malus):
        self.malus = malus


class ParseOk(Statut):
    def __init__(self, data, nb_col, nb_lignes):
        super().__init__()
        self.code = -1
        self.data = data
        self.nb_col = nb_col
        self.nb_lignes = nb_lignes
        self.too_big = False


class RequeteInterrompue(Statut):
    def __init__(self, malus=5.0):
        super().__init__()
        self.code = 26
        self.malus = malus
        self.message = "Requête interrompue car trop longue."


class MaxLignes(Statut):
    def __init__(self, malus=100.0):
        super().__init__()
        self.code = 1
        self.message = "Le nombre maximum de lignes est atteint"
        self.malus = malus


class NbColDiff(Statut):
    def __init__(self, attendu, obtenu, malus=0.0):
        super().__init__()
        self.code = 2
        self.attendu = attendu
        self.obtenu = obtenu
        self.message = "Mauvais nombre de colonnes (attendu : " + str(attendu) + ", obtenu : " + str(obtenu) + ")"
        self.malus = malus


class NbLignesDiff(Statut):
    def __init__(self, attendu, obtenu, malus=0.5):
        super().__init__()
        self.code = 3
        self.attendu = attendu
        self.obtenu = obtenu
        self.message = "Mauvais nombre de lignes (attendu : " + str(attendu) + ", obtenu : " + str(obtenu) + ")"
        self.malus = malus


class ResultatsDiff(Statut):
    def __init__(self, attendu, obtenu, malus=0.5):
        super().__init__()
        self.code = 4
        self.attendu = attendu
        self.obtenu = obtenu
        self.message = "Les résultats sont différents : " + str(attendu) + " <> " + str(obtenu)
        self.malus = malus


class AliasManquant(Statut):
    def __init__(self, ag: str, col_name: str, malus: float = 0.25):
        super().__init__()
        self.code = 5
        self.ag = ag.upper()
        self.col_name = col_name
        self.message = self.ag + '(' + col_name + ') : mettez un alias'
        self.malus = malus


class TableEnExces(Statut):
    def __init__(self, exces, malus=0.5):
        super().__init__()
        self.code = 6
        self.exces = exces
        if exces > 1:
            self.message = "Il y a " + str(exces) + " tables en trop."
        else:
            self.message = "Il y a " + str(exces) + " table en trop."
        self.malus = malus * exces


class TableManquante(Statut):
    def __init__(self, manque, malus=0.5):
        super().__init__()
        self.code = 7
        self.manque = manque
        if manque > 1:
            self.message = "Il y a " + str(manque) + " tables manquantes."
        else:
            self.message = "Il y a " + str(manque) + " table manquante."
        self.malus = malus * manque


class TableRepetee(Statut):
    def __init__(self, malus=0.5):
        super().__init__()
        self.code = 8
        self.malus = malus
        self.message = "Au moins une table est répétée deux fois sans alias."


class AliasRepete(Statut):
    def __init__(self, malus=0.25):
        super().__init__()
        self.code = 9
        self.malus = malus
        self.message = "Au moins unalias de table est utilisé deux fois."


class OrderByAbsent(Statut):
    def __init__(self, nb_col=2, malus=0.5):
        super().__init__()
        self.code = 10
        self.nb_col = nb_col
        self.malus = malus * nb_col
        self.message = "Il manque le ORDER BY."


class OrderByExces(Statut):
    def __init__(self, exces, malus=0.0):
        super().__init__()
        self.code = 11
        self.exces = exces
        self.malus = malus
        if exces > 1:
            self.message = "Il y a " + str(exces) + " colonnes de trop dans le ORDER BY."
        else:
            self.message = "Il y a " + str(exces) + " colonne de trop dans le ORDER BY."


class OrderByManque(Statut):
    def __init__(self, manque, malus=0.5):
        super().__init__()
        self.code = 12
        self.manque = manque
        self.malus = malus * manque
        if manque > 1:
            self.message = "Il y a " + str(manque) + " colonnes manquantes dans le ORDER BY."
        else:
            self.message = "Il y a " + str(manque) + " colonne manquante dans le ORDER BY."


class OrderByMalTrie(Statut):
    def __init__(self, nb_col, malus=0.5):
        super().__init__()
        self.code = 13
        self.nb_col = nb_col
        self.malus = malus * nb_col
        if nb_col > 1:
            self.message = "Il y a " + str(nb_col) + " colonnes mal triées (DESC/ASC) dans le ORDER BY."
        else:
            self.message = "Il y a " + str(nb_col) + " colonne mal triée (DESC/ASC) dans le ORDER BY."


class OrderByDesordre(Statut):
    def __init__(self, malus=0.5):
        super().__init__()
        self.code = 14
        self.malus = malus
        self.message = "Les colonnes du ORDER BY ne sont pas dans le bon ordre."


class GroupByInutile(Statut):
    def __init__(self, malus=1.0):
        super().__init__()
        self.code = 15
        self.malus = malus
        self.message = "GROUP BY inutile."


class GroupByAbsent(Statut):
    def __init__(self, nb_col, malus=1.0):
        super().__init__()
        self.code = 16
        self.nb_col = nb_col
        self.malus = malus * nb_col
        self.message = "GROUP BY inutile."


class GroupBySansAgregat(Statut):
    def __init__(self, malus=1.0):
        super().__init__()
        self.code = 17
        self.malus = malus
        self.message = "GROUP BY sans agrégat."


class GroupByManque(Statut):
    def __init__(self, manque, malus=0.5):
        super().__init__()
        self.code = 17
        self.manque = manque
        self.malus = malus * manque
        if manque > 1:
            self.message = "Il manque " + str(manque) + " colonnes dans le GROUP BY."
        else:
            self.message = "Il manque " + str(manque) + " colonne dans le GROUP BY."


class GroupByExces(Statut):
    def __init__(self, exces, malus=0.5):
        super().__init__()
        self.code = 17
        self.exces = exces
        self.malus = malus * exces
        if exces > 1:
            self.message = "Il manque " + str(exces) + " colonnes dans le GROUP BY."
        else:
            self.message = "Il manque " + str(exces) + " colonne dans le GROUP BY."


class HavingManquant(Statut):
    def __init__(self, manque, malus=0.5):
        super().__init__()
        self.code = 18
        self.manque = manque
        self.malus = malus * manque
        if manque > 1:
            self.message = "Il manque " + str(manque) + " conditions dans le HAVING."
        else:
            self.message = "Il manque " + str(manque) + " condition dans le HAVING."


class HavingExces(Statut):
    def __init__(self, exces, malus=0.5):
        super().__init__()
        self.code = 19
        self.exces = exces
        self.malus = malus * exces
        if exces > 1:
            self.message = "Il y a " + str(exces) + " conditions en trop dans le HAVING."
        else:
            self.message = "Il y a " + str(exces) + " condition en trop dans le HAVING."


class HavingInutile(Statut):
    def __init__(self, malus=1):
        super().__init__()
        self.code = 20
        self.malus = malus
        self.message = "Il n'y a pas besoin de HAVING."


class HavingSansGB(Statut):
    def __init__(self, malus=1):
        super().__init__()
        self.code = 20
        self.malus = malus
        self.message = "HAVING sans GROUP BY."


class SelectEtoile(Statut):
    def __init__(self, malus=1):
        super().__init__()
        self.code = 21
        self.malus = malus
        self.message = "SELECT * au lieu des colonnes demandées."


class SelectDesordre(Statut):
    def __init__(self, malus=0.0):
        super().__init__()
        self.code = 22
        self.malus = malus
        self.message = "Les colonnes du SELECT ne sont pas dans l'ordre demandé."


class SelectExces(Statut):
    def __init__(self, exces, malus=0.25):
        super().__init__()
        self.code = 23
        self.malus = malus
        self.exces = exces
        if exces > 1:
            self.message = "Il y a " + str(exces) + " colonnes en trop dans le SELECT."
        else:
            self.message = "Il y a " + str(exces) + " colonne en trop dans le SELECT."


class SelectManque(Statut):
    def __init__(self, manque, malus=0.25):
        super().__init__()
        self.code = 24
        self.malus = malus * manque
        self.manque = manque
        if manque > 1:
            self.message = "Il y a " + str(manque) + " colonnes manquantes dans le SELECT."
        else:
            self.message = "Il y a " + str(manque) + " colonne manquante dans le SELECT."


class ErreurParsing(Statut):
    def __init__(self, ligne, colonne, code, malus=100):
        super().__init__()
        self.code = 25
        message = "Erreur à la ligne " + str(ligne) + ", colonne " + str(colonne) + " :\n<" + code + ">\n"
        for _ in range(colonne):
            message += " "
        message += "^"
        self.message = message
        self.malus = malus


class EmptyQuery(Statut):
    def __init__(self, malus=100):
        super().__init__()
        self.code = 27
        self.message = "Requête vide"
        self.malus = malus


class DistinctManquant(Statut):
    def __init__(self, malus=1):
        super().__init__()
        self.code = 28
        self.message = "DISTINCT manquant."
        self.malus = malus


class DistinctInutile(Statut):
    def __init__(self, malus=1):
        super().__init__()
        self.code = 29
        self.message = "DISTINCT inutile."
        self.malus = malus


class MauvaisAgregat(Statut):
    def __init__(self, ag_sql, ag_sol, pos, malus=1):
        super().__init__()
        self.code = 30
        self.message = "Agrégat n°" + str(pos + 1) + " : mauvais agrégat (" + ag_sql + " au lieu de " + ag_sol + ")."
        self.malus = malus


class MauvaiseColAgregat(Statut):
    def __init__(self, pos, malus=1):
        super().__init__()
        self.code = 31
        self.message = "Agrégat n°" + str(pos + 1) + " : mauvaise colonne."
        self.malus = malus


class MauvaisDistinctAgregat(Statut):
    def __init__(self, pos, inutile, malus=1):
        super().__init__()
        self.code = 32
        if inutile:
            self.message = "Agrégat n°" + str(pos + 1) + " : DISTINCT inutile."
        else:
            self.message = "Agrégat n°" + str(pos + 1) + " : DISTINCT manquant."
        self.malus = malus
