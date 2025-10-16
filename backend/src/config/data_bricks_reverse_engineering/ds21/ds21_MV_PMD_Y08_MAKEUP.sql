SELECT DISTINCT
/* Information on PMD Y08 Class MAKEUP (Y08_LA_MAKEUP) Content by Material  
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL"
 * ⚠️Table missing in Databricks as of 2025-10-15
 *  */
	RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL".OBJEK AS MATNR18,
	SUBSTRING (OBJEK,11,18) "MATNR8",
	RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL".MERKMALSWERT AS MAKEUP
FROM
	RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL"
WHERE
	(((RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL".KLASSENART)= 'Y08')
		AND ((RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL".MERKMAL)= 'Y08_LA_MAKEUP')
			AND ((RXWSSTD."products.wsstd.dv.pmd::DV_OBJMERKMAL".KLASSE)= 'Y08_BHC_LABELING'))


