SELECT NomJeu, AnneePublicationJeu
FROM Version V, VersionJeu, Jeu
WHERE Jeu.IdJeu = VersionJeu.IdJeu
AND VersionJeu.IdVersion = V.IdVersion;
