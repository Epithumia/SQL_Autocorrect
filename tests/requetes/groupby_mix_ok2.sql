SELECT DISTINCT A.IdPersonne, NomPersonne
FROM Artiste AJ1, Artiste AJ2, Personne A
WHERE AJ1.IdArtiste = A.IdPersonne
AND AJ2.IdArtiste = A.IdPersonne
AND AJ1.IdJeu <> AJ2.IdJeu;
