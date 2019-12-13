SELECT NomJeu
FROM Personne, Conception, Jeu
WHERE IdPersonne = IdConcepteur
AND Conception.IdJeu = Jeu.IdJeu
AND NomPersonne = 'Bruno Faidutti'
AND Rang IS NOT NULL
ORDER BY NomJeu;
