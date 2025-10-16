SELECT DISTINCT
pvcmpd.cmpid AS "MATNR",
	   RIGHT(pvcmpd.cmpid,8) AS "MATNR8",
	   PNODID.PNAME AS "TPM",
	   pnodid.pnguid AS "PNGUID"
FROM
	"RXWSSTD"."products.wsstd.dv.p2r::DV_PVCMPD" pvcmpd
JOIN "RXWSSTD"."products.wsstd.dv.p2r::DV_POSVID" posvid ON pvcmpd.PVGUID = posvid.PVGUID 
JOIN "RXWSSTD"."products.wsstd.dv.p2r::DV_PNODID" pnodid ON posvid.PNGUID = pnodid.PNGUID 
JOIN "RXWSSTD"."products.wsstd.dv.p2r::DV_PNCMP" pncmp ON pnodid.PNGUID  = pncmp.PNGUID
WHERE posvid.PVTYPE = 'Z_PM' ORDER BY pvcmpd.CMPID