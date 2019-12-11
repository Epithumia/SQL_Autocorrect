SELECT NomPersonne, COUNT(*)
FROM Artiste AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne;
