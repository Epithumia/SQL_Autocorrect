SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, J.NbNotesUtilisateurs * J.NoteMoyenne AS Score
FROM Jeu J, Artiste AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY P.NomPersonne, AJ.IDArtiste, Score DESC, J.NomJeu, J.IdJeu;
