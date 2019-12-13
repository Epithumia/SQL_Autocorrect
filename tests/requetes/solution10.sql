SELECT COUNT(*) AS NbJeuxStegmaier, COUNT(Rang) AS NbJeuxClassesStegmaier
FROM Jeu, Conception, Personne
WHERE Jeu.IdJeu = Conception.IdJeu
AND IdConcepteur = IdPersonne
AND NomPersonne = 'Jamey Stegmaier';
