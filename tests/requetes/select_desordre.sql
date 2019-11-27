SELECT COUNT(*) AS NbJeux, AnneePublicationJeu
FROM Jeu
GROUP BY AnneePublicationJeu;
