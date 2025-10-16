SELECT DISTINCT
/* Information on PLANTS by Material  
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.pmd::DV_MARC"
 * RXWSSTD."products.wsstd.dv.pmd::DV_T001W"
 *  */
	plants.MATNR AS "MATNR",
	RIGHT(plants.MATNR,8) AS "MATNR8",
	string_agg(plants.werks,','order by plants.werks asc) as "PLANTS",
	replace_regexpr('([^,]+)(,\1)+' in string_agg(t001w.NAME1 ,','order by plants.werks asc) with '\1') as "PLANTS_TXT"
FROM RXWSSTD."products.wsstd.dv.pmd::DV_MARC" plants 
	LEFT JOIN RXWSSTD."products.wsstd.dv.pmd::DV_T001W" t001w ON plants.WERKS = t001w.WERKS 
WHERE MMSTA < '7' GROUP BY MATNR