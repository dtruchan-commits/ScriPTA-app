SELECT DISTINCT
/* Information on PTMS Nodes Status of TPM, TAG and TA
 * Used Tables/Views:
 * products.wsstd.dv.p2r::DV_XPLM_GOS_PARAMS
 */
	OBJECT_ID AS PNGUID,
	OBJECT_PARAM_VAL AS STATUS
FROM 
RXWSSTD."products.wsstd.dv.p2r::DV_XPLM_GOS_PARAMS"
WHERE opsys = 'P2R'
AND MANDT = '508'
AND OBJECT_PARAM = 'PTMSSTATUS'
AND SEQ_NO = '000002'