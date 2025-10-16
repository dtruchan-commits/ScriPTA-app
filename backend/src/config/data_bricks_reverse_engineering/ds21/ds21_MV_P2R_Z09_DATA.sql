SELECT DISTINCT
/* Information on PTMS Z09 Classification
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.p2r::DV_INOB"
   RXWSSTD."products.wsstd.dv.p2r::DV_AUSP"
 */
	RXWSSTD."products.wsstd.dv.p2r::DV_INOB".OBJEK AS MATNR,
	SUBSTRING (RXWSSTD."products.wsstd.dv.p2r::DV_INOB".OBJEK,11,18) "MATNR8",
	RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATINN,
	RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATZHL,
	RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATWRT,
	to_char(RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATFLV) AS ATFLV
FROM
	RXWSSTD."products.wsstd.dv.p2r::DV_INOB"
INNER JOIN RXWSSTD."products.wsstd.dv.p2r::DV_AUSP" ON 
	(RXWSSTD."products.wsstd.dv.p2r::DV_INOB".KLART = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".KLART)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_INOB".CUOBJ = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OBJEK)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_INOB".MANDT = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".MANDT)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_INOB".OPSYS = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OPSYS)
WHERE
	(((RXWSSTD."products.wsstd.dv.p2r::DV_INOB".KLART)= 'Z09')
		AND ((RXWSSTD."products.wsstd.dv.p2r::DV_INOB".OPSYS)= 'P2R')
			AND ((RXWSSTD."products.wsstd.dv.p2r::DV_INOB".MANDT)= '508')
				AND ((RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OPTYPE)<> 'D')) ORDER BY
	RXWSSTD."products.wsstd.dv.p2r::DV_INOB".OBJEK,
	RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATINN,
	RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATZHL