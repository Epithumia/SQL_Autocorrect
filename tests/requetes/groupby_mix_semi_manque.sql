SELECT NomPersonne
FROM Artiste AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
GROUP BY A.NomPersonne
HAVING COUNT(*) > 1;
