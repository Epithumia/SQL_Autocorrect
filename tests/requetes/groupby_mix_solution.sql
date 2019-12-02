SELECT NomPersonne
FROM ArtisteJeu AJ, Personne A
WHERE AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne, A.NomPersonne
HAVING COUNT(*) > 1;

SELECT DISTINCT A.IdPersonne, NomPersonne
FROM ArtisteJeu AJ1, ArtisteJeu AJ2, Personne A
WHERE AJ1.IdArtiste = A.IdPersonne
AND AJ2.IdArtiste = A.IdPersonne
AND AJ1.IdJeu <> AJ2.IdJeu;
