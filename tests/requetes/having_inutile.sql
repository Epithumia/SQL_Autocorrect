SELECT AnneePublicationJeu, COUNT(*) AS NbJeux
FROM Jeu
GROUP BY AnneePublicationJeu
HAVING COUNT(*) >= 1;
