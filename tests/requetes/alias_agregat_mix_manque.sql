SELECT AnneePublicationJeu, COUNT(*), COUNT(DISTINCT NbNotesUtilisateurs)
FROM Jeu
GROUP BY AnneePublicationJeu;
