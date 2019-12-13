SELECT NomJeu, Rang
FROM Jeu, SousDomaineJeu, Famille
WHERE Jeu.IdJeu = SousDomaineJeu.IdJeu
AND IdSousDomaine = IdFamille
AND NomFamille = 'Strategy Games'
AND Rang IS NOT NULL
AND NbNotesUtilisateurs > 17000
ORDER BY Rang;
