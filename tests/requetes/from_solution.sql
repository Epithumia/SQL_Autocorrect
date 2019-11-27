SELECT NomJeu, AnneePublicationJeu
FROM Jeu, VersionJeu, Version
WHERE Jeu.IdJeu = VersionJeu.IdJeu
AND VersionJeu.IdVersion = Version.IdVersion;
