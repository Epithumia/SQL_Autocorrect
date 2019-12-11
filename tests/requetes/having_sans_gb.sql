SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, AVG(complexite) AS ComplexiteMoyenne
FROM Jeu
HAVING AVG(Complexite) >= 2.5
ORDER BY COUNT(*), AnneePublicationJeu;
