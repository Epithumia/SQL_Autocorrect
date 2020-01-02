class Statut():
    def __init__(self):
        self.message = None
        self.malus = 0.0
        self.exces = None
        self.manque = None
        self.attendu = None
        self.obtenu = None
        self.code = None
        self.col_name = None
        self.nb_col = None


class StatutOk(Statut):
    def __init__(self):
        super().__init__()
        self.code = -1


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
            self.message = "Il manque " + str(manque) + "colonnes dans le GROUP BY."
        else:
            self.message = "Il manque " + str(manque) + "colonne dans le GROUP BY."


class GroupByExces(Statut):
    def __init__(self, exces, malus=0.5):
        super().__init__()
        self.code = 17
        self.exces = exces
        self.malus = malus * exces
        if exces > 1:
            self.message = "Il manque " + str(exces) + "colonnes dans le GROUP BY."
        else:
            self.message = "Il manque " + str(exces) + "colonne dans le GROUP BY."
