SELECT DISTINCT Jeu.IdJeu, NomJeu
FROM Jeu, Editeur, Compagnie, NbJoueurs
WHERE Jeu.IdJeu = Editeur.IdJeu
AND IdEditeur = Compagnie.IdCompagnie
AND Jeu.IdJeu = NbJoueurs.IdJeu
AND AnneePublicationJeu = 2019
AND min <= 5
AND max >= 5
AND Type = 'Meilleur';
