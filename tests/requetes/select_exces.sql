SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, COUNT(DISTINCT NomJeu) AS NbNoms
FROM Jeu
GROUP BY AnneePublicationJeu;
