SELECT AnneePublicationJeu, COUNT(*), COUNT(DISTINCT NbNotesUtilisateurs) AS NbJeuxEvalues
FROM Jeu
GROUP BY AnneePublicationJeu;
