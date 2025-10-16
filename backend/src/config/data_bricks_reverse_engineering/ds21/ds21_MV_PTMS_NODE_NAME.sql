SELECT DISTINCT
/* Information on PTMS Nodes, e.g. TPM Name, Type...
 * Used Tables/Views:
 * RXWSSTD."products.wsstd.dv.p2r::DV_PNODID"
   RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX"
 */
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".PNGUID,
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".PNAME,
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".PNTYPE,
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".CREABY,
    TO_DATE (TO_CHAR(RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".CREADAT, 'yyyymmdd'),'yyyymmdd')as CREADAT,
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".CHNGBY,
    TO_DATE (TO_CHAR(RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".CHNGDAT, 'yyyymmdd'),'yyyymmdd')as CHNGDAT,
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX".PNTEXT_UP
FROM
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID"
INNER JOIN RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX" ON
    RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".PNGUID = RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX".PNGUID
 AND RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".MANDT  = RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX".MANDT
 AND RXWSSTD."products.wsstd.dv.p2r::DV_PNODID".OPSYS  = RXWSSTD."products.wsstd.dv.p2r::DV_PNODTX".OPSYS 
WHERE
    "products.wsstd.dv.p2r::DV_PNODID".OPSYS = 'P2R'
    AND "products.wsstd.dv.p2r::DV_PNODID".MANDT = '508'
    AND "products.wsstd.dv.p2r::DV_PNODTX".SPRAS = 'E'
    AND ("products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_ECLASS'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_PACKTY'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_PT_GL'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_TAG'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_TPM'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_VIEWTA'
    OR "products.wsstd.dv.p2r::DV_PNODID".PNTYPE = 'Z_TPM_GL')