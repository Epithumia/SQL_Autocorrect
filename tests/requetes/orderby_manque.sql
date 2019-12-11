SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, J.NbNotesUtilisateurs * J.NoteMoyenne AS Score
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste;
