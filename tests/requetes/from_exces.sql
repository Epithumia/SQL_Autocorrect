SELECT NomJeu, AnneePublicationJeu
FROM Jeu, VersionJeu, Version, DependanceLangage
WHERE Jeu.IdJeu = VersionJeu.IdJeu
AND DependanceLangage.IdDependance = Jeu.IdDepLang
AND VersionJeu.IdVersion = Version.IdVersion;
