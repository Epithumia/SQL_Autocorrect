SELECT J.IdJeu, NomJeu
FROM Jeu J, Categorie C, Propriete P
WHERE J.IdJeu = C.IdJeu
AND C.IdCategorie = P.IdPropriete
AND NomPropriete = 'Exploration'
AND NoteMoyenne>=8
AND Rang > 0
ORDER BY Rang;
