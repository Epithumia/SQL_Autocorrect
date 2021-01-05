SELECT anneePublicationJeu, COUNT(*) AS NbJeux
FROM Jeu
GROUP BY anneePublicationJeu;
