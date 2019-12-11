SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, J.NbNotesUtilisateurs*NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY NomPersonne, AJ.IdArtiste, Points DESC, NomJeu, AJ.IdJeu;

SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, NbNotesUtilisateurs*J.NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY NomPersonne, P.IdPersonne,  NbNotesUtilisateurs*NoteMoyenne DESC, NomJeu, J.IdJeu;

SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, NbNotesUtilisateurs*NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY NomPersonne, P.IdPersonne,  J.NbNotesUtilisateurs*NoteMoyenne DESC, NomJeu, J.IdJeu;

SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, NbNotesUtilisateurs*NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY NomPersonne, P.IdPersonne,  NbNotesUtilisateurs*J.NoteMoyenne DESC, NomJeu, J.IdJeu;

SELECT AJ.IdArtiste, P.NomPersonne, J.IdJeu, NomJeu, NbNotesUtilisateurs*NoteMoyenne AS Points
FROM Jeu J, ArtisteJeu AJ, Personne P
WHERE J.IdJeu = AJ.IdJeu
AND P.IdPersonne = AJ.IdArtiste
ORDER BY P.NomPersonne, P.IdPersonne,  J.NbNotesUtilisateurs*J.NoteMoyenne DESC, NomJeu, J.IdJeu;
