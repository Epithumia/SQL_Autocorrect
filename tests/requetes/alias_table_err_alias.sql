SELECT NomJeu, AnneePublicationJeu
FROM Version V, VersionJeu V, Jeu
WHERE Jeu.IdJeu = V.IdJeu
AND V.IdVersion = V.IdVersion;
