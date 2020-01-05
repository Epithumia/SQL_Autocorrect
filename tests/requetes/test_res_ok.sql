SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu J
ORDER BY NbJeux, AnneePublicationJeu;
