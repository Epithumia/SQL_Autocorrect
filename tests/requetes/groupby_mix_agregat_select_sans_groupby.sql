SELECT NomPersonne, COUNT(*)
FROM ArtisteJeu AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne;
