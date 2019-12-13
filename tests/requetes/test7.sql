SELECT NomJeu, Rang
FROM Jeu, SousDomaineJeu, Famille
WHERE Jeu.IdJeu = SousDomaineJeu.IdJeu
AND IdSousDomaine = IdFamille
AND NomFamille = 'Strategy Games'
AND Rang > 0
AND NbNotesUtilisateurs > 17000
ORDER BY Rang;
