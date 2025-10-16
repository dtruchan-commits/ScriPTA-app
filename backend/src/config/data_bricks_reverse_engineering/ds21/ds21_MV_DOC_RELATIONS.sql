SELECT DISTINCT
/* Information on Document relations between materials or TPMs.
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.p2r::DV_DRAD"
   SXOKEDSX.MV_PTMS_NODE_NAME
 */
	drad.OBJKY AS "OBJKY",
	map(drad.dokob,'MARA',drad.OBJKY,null) AS "MATNR",
	map(drad.dokob,'MARA',RIGHT(drad.OBJKY,8),NULL) AS "MATNR8",
	map(drad.dokob,'PNODID',drad.OBJKY,null) AS "PNGUID",
	map(drad.dokob,'PNODID',node.PNAME,null) AS "TPM",
	drad.DOKAR AS "DOKAR",
	drad.DOKNR AS "DOKNR",
	drad.DOKVR AS "DOKVR",
	drad.DOKTL AS "DOKTL",
	drad.DOKOB AS "DOKOB", 
	drad.OBZAE AS "OBZAE",
	REPLACE(drad.dokar||drad.doknr||drad.DOKVR||drad.DOKTL,' ','') AS "DOC_STRING"
FROM
	RXWSSTD."products.wsstd.dv.p2r::DV_DRAD" drad
	LEFT JOIN SXOKEDSX.MV_PTMS_NODE_NAME node ON drad.OBJKY = node.PNGUID 
WHERE
	drad.DOKAR IN ('ACS','DRA','HRL', 'LRA', 'PDR', 'PMS', 'RMS')
	AND drad.DOKOB IN ('MARA','PNODID')
	AND drad.OPSYS= 'P2R'
	AND drad.MANDT= '508'
	AND drad.OPTYPE<> 'D'