SELECT NomPersonne, COUNT(*) AS NbJeuxArtiste
FROM Jeu J, Artiste AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY IdPersonne;
