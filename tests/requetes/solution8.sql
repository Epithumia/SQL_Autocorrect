SELECT NomPropriete As "Categorie", ROUND(AVG(NotePonderee),2) AS "Moyenne des notes",
       ROUND(AVG(Complexite),2) AS "Complexite moyenne"
FROM Propriete, Categorie, Jeu
WHERE IdPropriete = IdCategorie
AND Categorie.IdJeu = Jeu.IdJeu
AND NotePonderee > 0
GROUP BY IdPropriete, NomPropriete
ORDER BY "Moyenne des notes" DESC, "Complexite moyenne" DESC;
