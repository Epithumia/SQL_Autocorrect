SELECT A.IdPersonne, NomPersonne
FROM Jeu J, ArtisteJeu AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne, NomPersonne;
