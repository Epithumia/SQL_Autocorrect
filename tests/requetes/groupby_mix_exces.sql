SELECT NomPersonne
FROM ArtisteJeu AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne, A.NomPersonne, IdArtiste
HAVING COUNT(*) > 1;
