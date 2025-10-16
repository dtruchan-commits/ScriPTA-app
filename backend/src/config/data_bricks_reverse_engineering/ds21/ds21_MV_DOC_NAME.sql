SELECT DISTINCT
/* Information on Document names
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.p2r::DV_DRAW"
   RXWSSTD."products.wsstd.dv.p2r::DV_DRAT"
 */
	drat.DOKAR,
	drat.DOKNR,
	drat.DOKVR,
	drat.DOKTL,
	drat.LANGU,
	drat.DKTXT,
	drat.LTXIN,
	drat.DKTXT_UC,
	TO_DATE(TO_CHAR(draw.adatum,'yyyymmdd'),'yyyymmdd') AS "ADATUM",
	draw.DWNAM,
	REPLACE(drat.dokar||drat.doknr||drat.DOKVR||drat.DOKTL,' ','') AS "DOC_STRING"
FROM
	RXWSSTD."products.wsstd.dv.p2r::DV_DRAT" drat
INNER JOIN RXWSSTD."products.wsstd.dv.p2r::DV_DRAW" draw ON
	drat.DOKTL = draw.DOKTL
	AND drat.DOKVR = draw.DOKVR
	AND drat.DOKNR = draw.DOKNR
	AND drat.DOKAR = draw.DOKAR
	AND drat.MANDT = draw.MANDT
	AND drat.OPSYS = draw.OPSYS
WHERE
	drat.DOKAR IN ('ACS','DRA','HRL','LRA','PDR','PMS','RMS')
	AND drat.LANGU= 'E'
	AND drat.OPSYS= 'P2R'
	AND drat.MANDT= '508'
	AND drat.OPTYPE <> 'D'