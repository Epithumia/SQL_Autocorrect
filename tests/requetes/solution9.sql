SELECT COUNT(DISTINCT IdPersonne) AS NbConcepteursVF
FROM Conception, TravailVersion, Langue, Propriete, VersionJeu
WHERE IdConcepteur = IdPersonne
AND TravailVersion.IdVersion = Langue.IdVersion
AND IdLangage = IdPropriete
AND VersionJeu.IdVersion = TravailVersion.IdVersion
AND Conception.IdJeu = VersionJeu.IdJeu
AND NomPropriete = 'French';

SELECT COUNT(DISTINCT IdConcepteur) AS NbConcepteursVF
FROM Conception, TravailVersion, Langue, Propriete, VersionJeu
WHERE IdConcepteur = IdPersonne
AND TravailVersion.IdVersion = Langue.IdVersion
AND IdLangage = IdPropriete
AND VersionJeu.IdVersion = TravailVersion.IdVersion
AND Conception.IdJeu = VersionJeu.IdJeu
AND NomPropriete = 'French';
