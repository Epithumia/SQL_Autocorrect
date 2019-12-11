SELECT Jeu.NomJeu, Jeu.AnneePublicationJeu
FROM Version V, VersionJeu, Jeu, Jeu J2
WHERE Jeu.IdJeu = VersionJeu.IdJeu
AND VersionJeu.IdVersion = V.IdVersion
AND Jeu.Complexite > J2.Complexite
AND J2.NomJeu = 'Scythe';
