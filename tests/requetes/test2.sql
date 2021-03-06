SELECT DISTINCT Jeu.IdJeu, NomJeu
FROM Jeu, Editeur, Compagnie, NbJoueurs
WHERE Jeu.IdJeu = Editeur.IdJeu
AND IdEditeur = Compagnie.IdCompagnie
AND Jeu.IdJeu = NbJoueurs.IdJeu
AND SiteWebCompagnie is not null
AND AnneePublicationJeu = 2019
AND Minimum <= 5
AND Maximum >= 5
AND Type = 'Meilleur';
