SELECT nomJeu
FROM Jeu J, DependanceLangage DL
WHERE J.IdDepLang = DL.IdDependance
AND DL.LibelleDependance like '%pas de vote%'
--ORDER BY AnneePublicationJeu;
