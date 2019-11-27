SELECT NomJeu, AnneePublicationJeu
FROM Jeu, VersionJeu
WHERE Jeu.IdJeu = VersionJeu.IdJeu;
