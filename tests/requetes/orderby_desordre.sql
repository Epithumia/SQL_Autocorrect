SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, J.NbNotesUtilisateurs*NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY AJ.IdArtiste, NomPersonne, Points, NomJeu, AJ.IdJeu;
