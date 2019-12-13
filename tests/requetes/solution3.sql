SELECT IdCompagnie, NomCompagnie
FROM Compagnie, Editeur, Jeu
WHERE Compagnie.IdCompagnie = IdEditeur
AND Editeur.IdJeu = Jeu.IdJeu
AND TypeJeu = 'Jeu de Société'
GROUP BY IdCompagnie, NomCompagnie
HAVING MIN(Rang) = 2
ORDER BY NomCompagnie;
