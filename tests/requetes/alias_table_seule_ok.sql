SELECT COUNT(*) AS NbAdh
FROM Adherent
WHERE dateAdhesion IS NOT NULL
AND codePostalAdherent BETWEEN 92000 and 92999;
