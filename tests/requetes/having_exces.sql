SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
GROUP BY AnneePublicationJeu
HAVING AVG(Complexite) >= 2.5
AND COUNT(*) > 1
ORDER BY COUNT(*), AnneePublicationJeu;
