SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
GROUP BY AnneePublicationJeu
ORDER BY COUNT(*), AnneePublicationJeu;
