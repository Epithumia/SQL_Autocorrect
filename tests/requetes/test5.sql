SELECT J2.NomJeu
FROM Jeu J1, Jeu J2, Accessoire A
WHERE J1.IdJeu = A.IdJeuSociete
AND J2.IdJeu = A.IdAccessoire
AND J1.NomJeu = 'Scythe'
ORDER BY J2.NomJeu;
