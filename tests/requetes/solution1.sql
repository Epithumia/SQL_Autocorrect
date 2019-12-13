SELECT Jeu.IdJeu, NomJeu
FROM Jeu, Categorie, Propriete
WHERE Jeu.IdJeu = Categorie.IdJeu
AND Categorie.IdCategorie = Propriete.IdPropriete
AND NomPropriete = 'Exploration'
AND NoteMoyenne>=8
AND Rang IS NOT NULL
ORDER BY Rang;
