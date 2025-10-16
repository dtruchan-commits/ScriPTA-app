SELECT DISTINCT
/* Information on max Document version
 * Used Tables/Views:
 * SXOKEDSX.MV_DOC_NAME
 */
dname.DOKAR AS "DOKAR",
dname.DOKNR AS "DOKNR",
dname.doktl AS "DOKTL",
max(dname.DOKVR) AS "MAX_DOKVR",
REPLACE(dname.dokar||dname.doknr||max(dname.DOKVR)||dname.DOKTL,' ','') AS "DOC_STRING"
FROM 
SXOKEDSX.MV_DOC_NAME dname
GROUP BY DOKAR, DOKNR, DOKTL