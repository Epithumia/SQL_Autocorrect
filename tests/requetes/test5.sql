SELECT Jeu.IdJeu, NomJeu, COUNT(*) AS NbExtensions
FROM Jeu, Extension, Categorie, Propriete
WHERE Jeu.IdJeu = IdJeuBase
AND Jeu.IdJeu = Categorie.IdJeu
AND Categorie.IdCategorie = IdPropriete
AND NomPropriete = 'Collectible Components'
GROUP BY Jeu.IdJeu, NomJeu
ORDER BY NbExtensions DESC, NomJeu;
