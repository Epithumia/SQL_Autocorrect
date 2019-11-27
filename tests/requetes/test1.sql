SELECT AnneePublicationJeu, COUNT(DISTINCT J.NomJeu) AS "Noms uniques",
       COUNT(*), AVG(complexite)
FROM Jeu J
WHERE IdJeu > 100000
OR IdJeu < 50000
GROUP BY AnneePublicationJeu
HAVING AVG(Complexite) >= 2.5
ORDER BY AnneePublicationJeu, 2;
