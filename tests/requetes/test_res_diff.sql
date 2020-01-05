SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(DISTINCT complexite) AS ComplexiteMoyenne
FROM Jeu J
ORDER BY NbJeux, AnneePublicationJeu;
