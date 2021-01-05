SELECT NomPersonne, COUNT(*) AS NbJeuxArtiste
FROM Jeu J, Artiste AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY A.idPersonne, A.nomPersonne;

SELECT A.IdPersonne, NomPersonne, COUNT(*) AS NbJeuxArtiste
FROM Jeu J, Artiste AJ, Personne A
WHERE J.IdJeu = AJ.IdJeu
AND AJ.IdArtiste = A.IdPersonne
GROUP BY A.idPersonne, A.nomPersonne;
