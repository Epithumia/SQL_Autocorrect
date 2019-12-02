SELECT NomPersonne
FROM ArtisteJeu AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne
HAVING COUNT(*) > 1;
