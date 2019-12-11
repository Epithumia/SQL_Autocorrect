SELECT NomPersonne
FROM Artiste AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
HAVING COUNT(*) > 1;
