SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
GROUP BY AnneePublicationJeu
HAVING AVG(complexite) >= 2.5
ORDER BY COUNT(*), AnneePublicationJeu;
