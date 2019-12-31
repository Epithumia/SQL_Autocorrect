SELECT J.NomJeu, J.Rang
FROM Jeu J, Categorie C, Propriete P
WHERE J.IdJeu = C.IdJeu
AND C.IdCategorie = P.IdPropriete
AND J.NoteMoyenne >= 8
and J.rang not null
Order by J.rang
