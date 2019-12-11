SELECT DISTINCT A.IdPersonne, NomPersonne
FROM Jeu J, Artiste AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne;
