SELECT DISTINCT 
/* Information on Type of Drawing (Combination, Dieline, Other)
* Used Tables/Views:
	SXOKEDSX.MV_DOC_NAME
 	SXOKEDSX.MV_P2R_017_DATA_CONTENT
*/
 dra_type.DOC_STRING AS "DOC_STRING",
--Check if aggregated String of all Combination and Dieline drawings contains "yes"	
	CASE WHEN STRING_AGG(dra_type.IS_Combination_Drawing,'') LIKE '%yes%' THEN 'yes' ELSE 'no' END AS "IS_COMBINATION_DRAWING",
	CASE WHEN STRING_AGG(dra_type.IS_Dieline_Drawing,'') LIKE '%yes%' THEN 'yes' ELSE 'no' END AS "IS_DIELINE_DRAWING",
--Check if aggregated DIELINE or COMBINATION String contain 'YES'. If both do not contain 'yes', then it's a Other Drawing
	CASE WHEN STRING_AGG(dra_type.IS_Dieline_Drawing,'') LIKE '%yes%' OR STRING_AGG(dra_type.IS_Combination_Drawing,'') LIKE '%yes%' THEN 'no' ELSE 'yes' END AS "IS_OTHER_DRAWING"
FROM (
	--Sub Select to get information on row-level if it is a dieline or combination drawing
	SELECT DISTINCT 
		docname.DOC_STRING,
		--Combination Drawing: Name = COMBI oder CD_
		CASE 
			WHEN docname.DKTXT_UC LIKE '%COMBI%' THEN 'yes'
			WHEN LEFT(docname.DKTXT_UC,3) = 'CD_' THEN 'yes'
			ELSE 'no'
		END AS "IS_COMBINATION_DRAWING",
		--Dieline Drawing: Y08 DiELINE oder NAME = DIELINE
		CASE 
			WHEN LEFT(docname.DKTXT_UC,8) = 'DIELINE_' THEN 'yes'
			WHEN ucase(content.CONTENT_TXT) = 'DIELINE' THEN 'yes' --AND NOT (docname.DKTXT_UC LIKE '%COMBI%' OR LEFT(docname.DKTXT_UC,3) = 'CD_') THEN 'yes'
			ELSE 'no'
		END AS "IS_DIELINE_DRAWING"
		FROM  
		SXOKEDSX.MV_DOC_NAME docname
		LEFT JOIN SXOKEDSX.MV_P2R_017_DATA_CONTENT content ON docname.DOC_STRING = content.DOC_STRING 
		WHERE docname.DOKAR = 'DRA') dra_type
GROUP BY dra_type.doc_string