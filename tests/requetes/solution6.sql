SELECT NomJeu
FROM Personne, Conception, Jeu
WHERE IdPersonne = IdConcepteur
AND Conception.IdJeu = Jeu.IdJeu
AND NomPersonne = 'Bruno Faidutti'
AND Rang > 0
ORDER BY NomJeu;
