SELECT NomPersonne
FROM ArtisteJeu AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
HAVING COUNT(*) > 1;
