SELECT NomPersonne, COUNT(*) AS NbJeuxArtiste
FROM Jeu J, ArtisteJeu AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne, A.NomPersonne;

SELECT A.IdPersonne, NomPersonne, COUNT(*) AS NbJeuxArtiste
FROM Jeu J, ArtisteJeu AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY A.IdPersonne, A.NomPersonne;
