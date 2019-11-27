SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu J
ORDER BY NbJeux, AnneePublicationJeu;

SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
GROUP BY AnneePublicationJeu
HAVING AVG(Complexite) >= 2.5
ORDER BY COUNT(*), AnneePublicationJeu;
