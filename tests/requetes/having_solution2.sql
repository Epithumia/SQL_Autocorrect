SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
GROUP BY AnneePublicationJeu
HAVING AVG(Complexite) >= 2.5
AND AVG(Complexite) <= 4
OR AVG(Complexite) = 2
AND SUM(Complexite) = 10
ORDER BY COUNT(*), AnneePublicationJeu;
