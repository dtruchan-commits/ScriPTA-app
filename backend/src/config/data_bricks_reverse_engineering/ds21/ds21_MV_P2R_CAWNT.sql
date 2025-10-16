SELECT DISTINCT
/* Information on Classifikation Value Content and Context
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT"
   RXWSSTD."products.wsstd.dv.p2r::DV_CAWN"
 */
RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ATINN,
	RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ATZHL,
	RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ADZHL,
	RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ATWTB,
	RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".ATWRT AS ATWTB_TXT
FROM
	(RXWSSTD."products.wsstd.dv.p2r::DV_CAWN"
INNER JOIN RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT" ON
	(RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".ADZHL = RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ADZHL)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".OPSYS = RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".OPSYS)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".MANDT = RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".MANDT)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".ATINN = RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ATINN)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".ATZHL = RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".ATZHL))
INNER JOIN RXWSSTD."products.wsstd.dv.p2r::DV_AUSP" ON
	(RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".ATINN = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".ATINN)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".OPSYS = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OPSYS)
	AND (RXWSSTD."products.wsstd.dv.p2r::DV_CAWN".MANDT = RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".MANDT)
WHERE
	(((RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OPSYS)= 'P2R')
		AND ((RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".MANDT)= '508')
		AND ((RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".KLART)= 'Z09'
				OR (RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".KLART)= '017')
			AND ((RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".SPRAS)= 'E'
				OR (RXWSSTD."products.wsstd.dv.p2r::DV_CAWNT".SPRAS)= '')
				AND ((RXWSSTD."products.wsstd.dv.p2r::DV_AUSP".OPTYPE)<> 'D'))