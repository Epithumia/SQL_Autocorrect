SELECT AnneePublicationJeu, COUNT(*) AS NbJeux, COUNT(DISTINCT NbNotesUtilisateurs) AS NbJeuxEvalues
FROM Jeu
GROUP BY AnneePublicationJeu;
