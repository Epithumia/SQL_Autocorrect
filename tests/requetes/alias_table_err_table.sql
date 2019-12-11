SELECT Jeu.NomJeu, Jeu.AnneePublicationJeu
FROM Version V, VersionJeu, Jeu, Jeu
WHERE Jeu.IdJeu = VersionJeu.IdJeu
AND VersionJeu.IdVersion = V.IdVersion;
