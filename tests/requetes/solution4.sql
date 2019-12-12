SELECT IdCompagnie, NomCompagnie
FROM Compagnie, Editeur, Jeu
WHERE Compagnie.IdCompagnie = IdEditeur
AND Editeur.IdJeu = Jeu.IdJeu
AND TypeJeu = 'Jeu de Société'
AND Rang > 0
GROUP BY IdCompagnie, NomCompagnie
HAVING MIN(Rang) = 1
ORDER BY NomCompagnie;
