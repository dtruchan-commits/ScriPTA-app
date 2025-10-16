-- Unified CTE that replaces all the dependent views for MV_PMD_MATERIAL_DATA_FOR_ARTWORK
-- This single CTE consolidates all the logic from the component views into one query
-- FILTERED FOR MATERIAL 91967086
-- TRANSLATED FOR DATABRICKS WITH TABLE MAPPINGS
WITH
    -- Base P2R tables for characteristic classification
    base_p2r_inob AS (
        SELECT DISTINCT
            OBJEK AS MATNR,
            SUBSTRING(OBJEK, 11, 18) AS MATNR8,
            CUOBJ,
            KLART,
            MANDT,
            OPSYS
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_inob_view
        WHERE
            KLART = 'Z09'
            AND OPSYS = 'P2R'
            AND MANDT = '508'
            AND OBJEK LIKE '%91967086%' -- Filter for material 91967086
    ),
    base_p2r_ausp AS (
        SELECT DISTINCT
            OBJEK,
            ATINN,
            ATZHL,
            ATWRT,
            CAST(ATFLV AS STRING) AS ATFLV,
            KLART,
            MANDT,
            OPSYS
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_ausp_view
        WHERE
            OPTYPE <> 'D'
            AND OPSYS = 'P2R'
            AND MANDT = '508'
    ),
    -- Characteristic value lookup
    p2r_cawnt AS (
        SELECT DISTINCT
            cawnt.ATINN,
            cawnt.ATZHL,
            cawnt.ADZHL,
            cawnt.ATWTB,
            cawn.ATWRT AS ATWTB_TXT
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cawnt_view cawnt
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cawn_view cawn ON cawnt.ADZHL = cawn.ADZHL
            AND cawnt.OPSYS = cawn.OPSYS
            AND cawnt.MANDT = cawn.MANDT
            AND cawnt.ATINN = cawn.ATINN
            AND cawnt.ATZHL = cawn.ATZHL
            INNER JOIN base_p2r_ausp ausp ON cawn.ATINN = ausp.ATINN
            AND cawn.OPSYS = ausp.OPSYS
            AND cawn.MANDT = ausp.MANDT
        WHERE
            ausp.KLART IN ('Z09', '017')
            AND (
                cawnt.SPRAS = 'E'
                OR cawnt.SPRAS = ''
            )
    ),
    -- Z09 raw data
    z09_raw_data AS (
        SELECT DISTINCT
            inob.MATNR,
            inob.MATNR8,
            ausp.ATINN,
            ausp.ATZHL,
            ausp.ATWRT,
            ausp.ATFLV
        FROM
            base_p2r_inob inob
            INNER JOIN base_p2r_ausp ausp ON inob.KLART = ausp.KLART
            AND inob.CUOBJ = ausp.OBJEK
            AND inob.MANDT = ausp.MANDT
            AND inob.OPSYS = ausp.OPSYS
    ),
    -- Z09 data with content processing
    z09_data_content AS (
        SELECT DISTINCT
            z09.MATNR,
            z09.MATNR8,
            z09.ATINN,
            cabnt.ATBEZ AS ATINN_TXT,
            z09.ATZHL,
            z09.ATWRT,
            z09.ATFLV,
            CASE
                WHEN z09.ATWRT = '' THEN z09.ATFLV
                WHEN cawnt.ATWTB = '' THEN cawnt.ATWTB
                ELSE z09.ATWRT
            END AS CONTENT,
            CASE
                WHEN z09.ATWRT = '' THEN z09.ATFLV
                WHEN z09.ATWRT = cawnt.ATWTB_TXT THEN cawnt.ATWTB
                WHEN cawnt.ATWTB = '' THEN cawnt.ATWTB
                ELSE z09.ATWRT
            END AS CONTENT_TXT
        FROM
            z09_raw_data z09
            LEFT JOIN p2r_cawnt cawnt ON z09.ATINN = cawnt.ATINN
            AND z09.ATWRT = cawnt.ATWTB_TXT
            LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cabnt_view cabnt ON z09.ATINN = cabnt.ATINN
        WHERE
            cabnt.SPRAS = 'E'
            OR cabnt.SPRAS IS NULL
    ),
    -- Z09 aggregated content 
    z09_data_aggregated AS (
        SELECT
            MATNR,
            MATNR8,
            array_join (array_sort (collect_list (CONTENT_TXT)), ', ') AS CONTENT_TXT_AGG,
            ATINN
        FROM
            z09_data_content
        GROUP BY
            MATNR,
            MATNR8,
            ATINN
    ),
    -- Z09 individual characteristics for print characteristics
    z09_data_char AS (
        SELECT
            MATNR,
            ATINN,
            CONTENT
        FROM
            z09_data_content
        GROUP BY
            MATNR,
            ATINN,
            CONTENT
    ),
    -- Z09 pivot for all characteristics
    z09_pivot AS (
        SELECT DISTINCT
            z09agg.MATNR,
            z09agg.MATNR8,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028219' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_manufacturer_codetype,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028220' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_manufacturer_code,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028204' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Responsible_for_specification,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028223' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_manufacturer_material,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028210' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Layout_approved,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028207' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Usage_Prefix,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028386' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Number_of_pages,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028228' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS ACF_Flag,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028216' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Visible_Markings,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028215' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Code,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028211' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Colors,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028212' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Number_colors_front,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028222' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_manufacturer,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028206' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Article_codetype,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028205' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Article_code,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028224' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_man_visible_markings,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028221' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Contract_manufacturer_mt_index,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028214' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Component_scrab_key,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028225' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Remarks,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028208' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Printed,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028213' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Number_colors_back,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028227' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Print_characteristics,
            MAX(
                CASE
                    WHEN z09agg.ATINN = '0000028209' THEN z09agg.CONTENT_TXT_AGG
                    ELSE NULL
                END
            ) AS Braille_text,
            -- Print characteristics individual flags
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '1' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Braille,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '2' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_FoilStamp,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '3' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_GoldHotFoil,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '4' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_EmbossDeboss,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '5' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_SpotVarnish,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '6' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_ScratchOff,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '7' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Lamination,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '8' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_DieCut,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '9' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Perforation,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '10' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_GlossVarnish,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '11' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Leafleting,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '12' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Folding,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '13' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_RichPaleGold,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '14' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_SilverHotFoil,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '15' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_Unvarnish,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '16' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_SecurityVarish,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '17' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_MattVarnish,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '17' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_CodingBySupplier,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '18' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_BKLogo,
            MAX(
                CASE
                    WHEN z09char.ATINN = '0000028227'
                    AND z09char.CONTENT = '19' THEN 'Yes'
                    ELSE 'No'
                END
            ) AS PrintChar_S_DR
        FROM
            z09_data_aggregated z09agg
            LEFT JOIN z09_data_char z09char ON z09agg.MATNR = z09char.MATNR
        GROUP BY
            z09agg.MATNR,
            z09agg.MATNR8
    ),
    -- Y08 Makeup data
    y08_makeup AS (
        SELECT DISTINCT
            INOB.OBJEK AS MATNR18,
            SUBSTRING(INOB.OBJEK, 11, 18) AS MATNR8,
            AUSP.ATWRT AS MAKEUP
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_inob_view INOB
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_ausp_view AUSP ON INOB.KLART = AUSP.KLART
            AND INOB.CUOBJ = AUSP.OBJEK
            AND INOB.MANDT = AUSP.MANDT
            AND INOB.OPSYS = AUSP.OPSYS
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cabn_view CABN ON AUSP.ATINN = CABN.ATINN
            AND AUSP.MANDT = CABN.MANDT
            AND AUSP.OPSYS = CABN.OPSYS
        WHERE
            INOB.KLART = 'Y08'
            AND INOB.OPSYS = 'P2R'
            AND INOB.MANDT = '508'
            AND AUSP.OPTYPE <> 'D'
            AND CABN.ATNAM = 'Y08_LA_MAKEUP'
            AND INOB.OBJEK LIKE '%91967086%' -- Filter for material 91967086
    ),
    -- Plants aggregated data
    plants_aggregated AS (
        SELECT DISTINCT
            plants.MATNR,
            RIGHT (plants.MATNR, 8) AS MATNR8,
            array_join (array_sort (collect_list (plants.WERKS)), ',') AS PLANTS,
            array_join (
                array_sort (array_distinct (collect_list (t001w.NAME1))),
                ','
            ) AS PLANTS_TXT
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.pmd_marc_view plants
            LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.pmd_t001w_view t001w ON plants.WERKS = t001w.WERKS
        WHERE
            plants.MMSTA < '7'
            AND plants.MATNR LIKE '%91967086%' -- Filter for material 91967086
        GROUP BY
            plants.MATNR
    ),
    -- TPM relations
    tpm_relations AS (
        SELECT DISTINCT
            pvcmpd.CMPID AS MATNR,
            RIGHT (pvcmpd.CMPID, 8) AS MATNR8,
            pnodid.PNAME AS TPM,
            pnodid.PNGUID
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pvcmpd_view pvcmpd
            JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_posvid_view posvid ON pvcmpd.PVGUID = posvid.PVGUID
            JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pnodid_view pnodid ON posvid.PNGUID = pnodid.PNGUID
            JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pncmp_view pncmp ON pnodid.PNGUID = pncmp.PNGUID
        WHERE
            posvid.PVTYPE = 'Z_PM'
            AND pvcmpd.CMPID LIKE '%91967086%' -- Filter for material 91967086
    ),
    -- TPM node names and status
    tpm_node_names AS (
        SELECT DISTINCT
            pnodid.PNGUID,
            pnodid.PNAME,
            pnodtx.PNTEXT_UP,
            pnodid.PNTYPE,
            pnodid.CREABY,
            to_date (cast(pnodid.CREADAT as string), 'yyyyMMdd') AS CREADAT,
            pnodid.CHNGBY,
            to_date (cast(pnodid.CHNGDAT as string), 'yyyyMMdd') AS CHNGDAT
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pnodid_view pnodid
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pnodtx_view pnodtx ON pnodid.PNGUID = pnodtx.PNGUID
            AND pnodid.MANDT = pnodtx.MANDT
            AND pnodid.OPSYS = pnodtx.OPSYS
        WHERE
            pnodid.OPSYS = 'P2R'
            AND pnodid.MANDT = '508'
            AND pnodtx.SPRAS = 'E'
            AND pnodid.PNTYPE IN (
                'Z_ECLASS',
                'Z_PACKTY',
                'Z_PT_GL',
                'Z_TAG',
                'Z_TPM',
                'Z_VIEWTA',
                'Z_GLPT'
            )
    ),
    tpm_node_status AS (
        SELECT DISTINCT
            OBJECT_ID AS PNGUID,
            OBJECT_PARAM_VAL AS STATUS
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_xplm_gos_params_view
        WHERE
            OPSYS = 'P2R'
            AND MANDT = '508'
            AND OBJECT_PARAM = 'PTMSSTATUS'
            AND SEQ_NO = '000002'
    ),
    -- Base node relations
    tpm_base_relations AS (
        SELECT DISTINCT
            prelid.GUID1 AS NODEID_PNGUID,
            node1.PNTYPE AS NODEPNTYPE,
            node1.PNAME AS NODE,
            node1.PNTEXT_UP AS NODETXT,
            prelid.GUID2 AS NODE_ITEMID_PNGUID,
            node2.PNTYPE AS NODE_ITEMPNTYPE,
            node2.PNAME AS NODE_ITEM,
            node2.PNTEXT_UP AS NODE_ITEMTXT,
            prelid.SORT AS SORT
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_prelid_view prelid
            JOIN tpm_node_names node1 ON prelid.GUID1 = node1.PNGUID
            JOIN tpm_node_names node2 ON prelid.GUID2 = node2.PNGUID
        WHERE
            prelid.OPSYS = 'P2R'
            AND prelid.MANDT = '508'
    ),
    -- ECLASS relations (ECLASS_S to ECLASS to GLPT)
    tpm_eclass_relations AS (
        SELECT DISTINCT
            node1.NODEID_PNGUID AS ECLASS_S_PNGUID,
            node1.NODE AS ECLASS_S,
            node1.NODETXT AS ECLASS_STXT,
            node2.NODEID_PNGUID AS ECLASS_PNGUID,
            node2.NODE AS ECLASS,
            node2.NODETXT AS ECLASSTXT,
            node2.NODE_ITEMID_PNGUID AS GLPT_PNGUID,
            node2.NODE_ITEM AS GLPT,
            node2.NODE_ITEMTXT AS GLPTTXT
        FROM
            tpm_base_relations node1
            JOIN tpm_base_relations node2 ON node1.NODE_ITEMID_PNGUID = node2.NODEID_PNGUID
        WHERE
            node1.NODEPNTYPE = 'Z_ECLASS'
            AND node2.NODEPNTYPE = 'Z_ECLASS'
    ),
    -- TPM to GLPT/ECLASS relations
    tpm_full_relations AS (
        SELECT DISTINCT
            noderelations.NODE_ITEMID_PNGUID AS TPM_PNGUID,
            noderelations.NODE_ITEM AS TPM,
            noderelations.NODE_ITEMTXT AS TPMTXT,
            noderelations.NODEID_PNGUID AS GLPT_PNGUID,
            noderelations.NODE AS GLPT,
            noderelations.NODETXT AS GLPTTXT,
            eclass_rel.ECLASS_PNGUID AS ECLASS_PNGUID,
            eclass_rel.ECLASS AS ECLASS,
            eclass_rel.ECLASSTXT AS ECLASSTXT,
            eclass_rel.ECLASS_S_PNGUID AS ECLASS_S_PNGUID,
            eclass_rel.ECLASS_S AS ECLASS_S,
            eclass_rel.ECLASS_STXT AS ECLASS_STXT
        FROM
            tpm_base_relations noderelations
            LEFT JOIN tpm_eclass_relations eclass_rel ON noderelations.NODEID_PNGUID = eclass_rel.GLPT_PNGUID
        WHERE
            noderelations.NODE_ITEMPNTYPE = 'Z_TPM'
            AND noderelations.NODEPNTYPE = 'Z_PT_GL'
    ),
    -- TPM data consolidated with proper relations
    tpm_data AS (
        SELECT DISTINCT
            pnodid.PNAME AS TPM,
            pnodtx.PNTEXT_UP AS TPMTXT,
            params.OBJECT_PARAM_VAL AS TPM_STATUS,
            pncmp.TPM_PMD_NO,
            pncmp.PNGUID,
            COALESCE(rel.GLPT, '') AS GLPT,
            COALESCE(rel.GLPTTXT, '') AS GLPTTXT,
            COALESCE(rel.ECLASS, '') AS ECLASS,
            COALESCE(rel.ECLASSTXT, '') AS ECLASSTXT,
            COALESCE(rel.ECLASS_S, '') AS ECLASS_S,
            COALESCE(rel.ECLASS_STXT, '') AS ECLASS_STXT
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pncmp_view pncmp
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pnodid_view pnodid ON pncmp.PNGUID = pnodid.PNGUID
            LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_pnodtx_view pnodtx ON pnodid.PNGUID = pnodtx.PNGUID
            AND pnodid.MANDT = pnodtx.MANDT
            AND pnodid.OPSYS = pnodtx.OPSYS
            AND pnodtx.SPRAS = 'E'
            LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_xplm_gos_params_view params ON pncmp.PNGUID = params.OBJECT_ID
            AND params.OPSYS = 'P2R'
            AND params.MANDT = '508'
            AND params.OBJECT_PARAM = 'PTMSSTATUS'
            AND params.SEQ_NO = '000002'
            LEFT JOIN tpm_full_relations rel ON pncmp.PNGUID = rel.TPM_PNGUID
        WHERE
            pnodid.OPSYS = 'P2R'
            AND pnodid.MANDT = '508'
            AND pnodid.PNTYPE = 'Z_TPM'
    ),
    -- Document relations base
    doc_relations AS (
        SELECT DISTINCT
            drad.OBJKY,
            CASE
                WHEN drad.DOKOB = 'MARA' THEN drad.OBJKY
                ELSE NULL
            END AS MATNR,
            CASE
                WHEN drad.DOKOB = 'MARA' THEN RIGHT (drad.OBJKY, 8)
                ELSE NULL
            END AS MATNR8,
            CASE
                WHEN drad.DOKOB = 'PNODID' THEN drad.OBJKY
                ELSE NULL
            END AS PNGUID,
            CASE
                WHEN drad.DOKOB = 'PNODID' THEN node.PNAME
                ELSE NULL
            END AS TPM,
            drad.DOKAR,
            drad.DOKNR,
            drad.DOKVR,
            drad.DOKTL,
            drad.DOKOB,
            drad.OBZAE,
            regexp_replace (
                concat (drad.DOKAR, drad.DOKNR, drad.DOKVR, drad.DOKTL),
                ' ',
                ''
            ) AS DOC_STRING
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_drad_view drad
            LEFT JOIN tpm_node_names node ON drad.OBJKY = node.PNGUID
        WHERE
            drad.DOKAR IN ('ACS', 'DRA', 'HRL', 'LRA', 'PDR', 'PMS', 'RMS')
            AND drad.DOKOB IN ('MARA', 'PNODID')
            AND drad.OPSYS = 'P2R'
            AND drad.MANDT = '508'
            AND drad.OPTYPE <> 'D'
            AND (
                (
                    drad.DOKOB = 'MARA'
                    AND drad.OBJKY LIKE '%91967086%'
                ) -- Filter material documents
                OR drad.DOKOB = 'PNODID'
            )
    ),
    -- Document names
    doc_names AS (
        SELECT DISTINCT
            drat.DOKAR,
            drat.DOKNR,
            drat.DOKVR,
            drat.DOKTL,
            drat.LANGU,
            drat.DKTXT,
            drat.LTXIN,
            drat.DKTXT_UC,
            to_date (cast(draw.ADATUM as string), 'yyyyMMdd') AS ADATUM,
            draw.DWNAM,
            regexp_replace (
                concat (drat.DOKAR, drat.DOKNR, drat.DOKVR, drat.DOKTL),
                ' ',
                ''
            ) AS DOC_STRING
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_drat_view drat
            INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_draw_view draw ON drat.DOKTL = draw.DOKTL
            AND drat.DOKVR = draw.DOKVR
            AND drat.DOKNR = draw.DOKNR
            AND drat.DOKAR = draw.DOKAR
            AND drat.MANDT = draw.MANDT
            AND drat.OPSYS = draw.OPSYS
        WHERE
            drat.DOKAR IN ('ACS', 'DRA', 'HRL', 'LRA', 'PDR', 'PMS', 'RMS')
            AND drat.LANGU = 'E'
            AND drat.OPSYS = 'P2R'
            AND drat.MANDT = '508'
            AND drat.OPTYPE <> 'D'
    ),
    -- Document max versions
    doc_max_versions AS (
        SELECT DISTINCT
            dname.DOKAR,
            dname.DOKNR,
            dname.DOKTL,
            MAX(dname.DOKVR) AS MAX_DOKVR,
            regexp_replace (
                concat (
                    dname.DOKAR,
                    dname.DOKNR,
                    MAX(dname.DOKVR),
                    dname.DOKTL
                ),
                ' ',
                ''
            ) AS DOC_STRING
        FROM
            doc_names dname
        GROUP BY
            dname.DOKAR,
            dname.DOKNR,
            dname.DOKTL
    ),
    -- Document filenames
    doc_filenames AS (
        SELECT DISTINCT
            files.DOKAR,
            files.DOKNR,
            files.DOKVR,
            files.DOKTL,
            files.FILE_IDX,
            files.DAPPL,
            files.FILENAME,
            regexp_replace (
                concat (
                    files.DOKAR,
                    files.DOKNR,
                    files.DOKVR,
                    files.DOKTL
                ),
                ' ',
                ''
            ) AS DOC_STRING
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.p2r_dms_doc_files_view files
        WHERE
            files.DOKAR IN ('ACS', 'DRA', 'HRL', 'LRA', 'PDR', 'PMS', 'RMS')
            AND files.OPSYS = 'P2R'
            AND files.MANDT = '508'
            AND files.OPTYPE <> 'D'
    ),
    -- Drawing type classification
    drawing_type AS (
        SELECT
            dra_type.DOC_STRING,
            CASE
                WHEN array_join (
                    collect_list (dra_type.IS_COMBINATION_DRAWING),
                    ''
                ) LIKE '%yes%' THEN 'yes'
                ELSE 'no'
            END AS IS_COMBINATION_DRAWING,
            CASE
                WHEN array_join (collect_list (dra_type.IS_DIELINE_DRAWING), '') LIKE '%yes%' THEN 'yes'
                ELSE 'no'
            END AS IS_DIELINE_DRAWING,
            CASE
                WHEN array_join (collect_list (dra_type.IS_DIELINE_DRAWING), '') LIKE '%yes%'
                OR array_join (
                    collect_list (dra_type.IS_COMBINATION_DRAWING),
                    ''
                ) LIKE '%yes%' THEN 'no'
                ELSE 'yes'
            END AS IS_OTHER_DRAWING
        FROM
            (
                SELECT DISTINCT
                    docname.DOC_STRING,
                    CASE
                        WHEN docname.DKTXT_UC LIKE '%COMBI%' THEN 'yes'
                        WHEN left (docname.DKTXT_UC, 3) = 'CD_' THEN 'yes'
                        ELSE 'no'
                    END AS IS_COMBINATION_DRAWING,
                    CASE
                        WHEN left (docname.DKTXT_UC, 8) = 'DIELINE_' THEN 'yes'
                        WHEN upper(content.CONTENT_TXT) = 'DIELINE' THEN 'yes'
                        ELSE 'no'
                    END AS IS_DIELINE_DRAWING
                FROM
                    doc_names docname
                    LEFT JOIN z09_data_content content -- Assuming we need this for 017 data content 
                    ON docname.DOC_STRING = content.CONTENT -- This may need adjustment based on actual 017 content structure
                WHERE
                    docname.DOKAR = 'DRA'
            ) dra_type
        GROUP BY
            dra_type.DOC_STRING
    ),
    -- Document info consolidated
    doc_info_current AS (
        SELECT DISTINCT
            relation.OBJKY,
            relation.MATNR,
            relation.MATNR8,
            relation.TPM,
            relation.PNGUID,
            -- LRA documents
            MAX(
                CASE
                    WHEN relation.DOKAR = 'LRA' THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS LRA,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'LRA' THEN maxver.MAX_DOKVR
                    ELSE NULL
                END
            ) AS LRA_VERSION,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'LRA' THEN docname.ADATUM
                    ELSE NULL
                END
            ) AS LRA_DATE,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'LRA' THEN fname.FILENAME
                    ELSE NULL
                END
            ) AS LRA_FILENAME,
            -- HRL documents  
            MAX(
                CASE
                    WHEN relation.DOKAR = 'HRL' THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS HRL,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'HRL' THEN maxver.MAX_DOKVR
                    ELSE NULL
                END
            ) AS HRL_VERSION,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'HRL' THEN docname.ADATUM
                    ELSE NULL
                END
            ) AS HRL_DATE,
            -- ACS documents
            MAX(
                CASE
                    WHEN relation.DOKAR = 'ACS' THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS ACS,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'ACS' THEN maxver.MAX_DOKVR
                    ELSE NULL
                END
            ) AS ACS_VERSION,
            -- Drawing aggregations
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_COMBINATION_DRAWING = 'yes' THEN relation.DOKNR
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_COMBINATION_AGG,
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_COMBINATION_DRAWING = 'yes' THEN docname.DKTXT_UC
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_COMBINATION_AGG_DKTXTUC,
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_DIELINE_DRAWING = 'yes' THEN relation.DOKNR
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_DIELINE_AGG,
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_DIELINE_DRAWING = 'yes' THEN docname.DKTXT_UC
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_DIELINE_AGG_DKTXTUC,
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_OTHER_DRAWING = 'yes' THEN relation.DOKNR
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_OTHER_AGG,
            array_join (
                collect_list (
                    CASE
                        WHEN relation.DOKAR = 'DRA'
                        AND drawtype.IS_OTHER_DRAWING = 'yes' THEN docname.DKTXT_UC
                        ELSE NULL
                    END
                ),
                ','
            ) AS DRA_OTHER_AGG_DKTXTUC,
            -- Individual DRA documents (you would extend this pattern for DRA_2 through DRA_10)
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 1 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_1,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 2 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_2,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 3 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_3,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 4 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_4,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 5 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_5,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 6 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_6,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 7 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_7,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 8 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_8,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 9 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_9,
            MAX(
                CASE
                    WHEN relation.DOKAR = 'DRA'
                    AND dra_rank.rn = 10 THEN relation.DOKNR
                    ELSE NULL
                END
            ) AS DRA_10
        FROM
            doc_relations relation
            LEFT JOIN doc_max_versions maxver ON relation.DOC_STRING = maxver.DOC_STRING
            LEFT JOIN doc_names docname ON maxver.DOC_STRING = docname.DOC_STRING
            LEFT JOIN doc_filenames fname ON maxver.DOC_STRING = fname.DOC_STRING
            LEFT JOIN drawing_type drawtype ON relation.DOC_STRING = drawtype.DOC_STRING
            LEFT JOIN (
                SELECT
                    DOC_STRING,
                    OBJKY,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            OBJKY
                        ORDER BY
                            DOKNR
                    ) as rn
                FROM
                    doc_relations
                WHERE
                    DOKAR = 'DRA'
            ) dra_rank ON relation.DOC_STRING = dra_rank.DOC_STRING
            AND relation.OBJKY = dra_rank.OBJKY
        GROUP BY
            relation.OBJKY,
            relation.MATNR,
            relation.MATNR8,
            relation.TPM,
            relation.PNGUID
    )
    -- Final SELECT statement with all joins
SELECT
    -- Material Data
    MATDATA.MATNR AS MATNR,
    COALESCE(MATDATA.MAKTX, '') AS MATERIAL_DESCRIPTION,
    COALESCE(MATDATA.MTART, '') AS MATERIAL_TYPE,
    COALESCE(MATDATA.MSTAE, '') AS XPLANT_STATUS,
    COALESCE(MATDATA.PRDHATXT, '') AS PRDHATXT,
    -- Makeup
    COALESCE(MAKEUP.MAKEUP, '') AS MAKEUP,
    -- Plants
    COALESCE(PLANTS.PLANTS, '') AS PLANTS,
    COALESCE(PLANTS.PLANTS_TXT, '') AS PLANTS_TXT,
    -- Z09 Characteristics
    COALESCE(Z09DATA.Contract_manufacturer_codetype, '') AS CONTRACT_MANUFACTURER_CODETYPE,
    COALESCE(Z09DATA.Contract_manufacturer_code, '') AS CONTRACT_MANUFACTURER_CODE,
    COALESCE(Z09DATA.Responsible_for_specification, '') AS RESPONSIBLE_FOR_SPECIFICATION,
    COALESCE(Z09DATA.Contract_manufacturer_material, '') AS CONTRACT_MANUFACTURER_MATERIAL,
    COALESCE(Z09DATA.Layout_approved, '') AS LAYOUT_APPROVED,
    COALESCE(Z09DATA.Usage_Prefix, '') AS USAGE_PREFIX,
    COALESCE(Z09DATA.Number_of_pages, '') AS NUMBER_OF_PAGES,
    COALESCE(Z09DATA.ACF_Flag, '') AS ACF_FLAG,
    COALESCE(Z09DATA.Visible_Markings, '') AS VISIBLE_MARKINGS,
    COALESCE(Z09DATA.Code, '') AS CODE,
    COALESCE(Z09DATA.Colors, '') AS COLORS,
    COALESCE(Z09DATA.Number_colors_front, '') AS NUMBER_COLORS_FRONT,
    COALESCE(Z09DATA.Contract_manufacturer, '') AS CONTRACT_MANUFACTURER,
    COALESCE(Z09DATA.Article_codetype, '') AS ARTICLE_CODETYPE,
    COALESCE(Z09DATA.Article_code, '') AS ARTICLE_CODE,
    COALESCE(Z09DATA.Contract_man_visible_markings, '') AS CONTRACT_MAN_VISIBLE_MARKINGS,
    COALESCE(Z09DATA.Contract_manufacturer_mt_index, '') AS CONTRACT_MANUFACTURER_MT_INDEX,
    COALESCE(Z09DATA.Component_scrab_key, '') AS COMPONENT_SCRAB_KEY,
    COALESCE(Z09DATA.Remarks, '') AS REMARKS,
    COALESCE(Z09DATA.Printed, '') AS PRINTED,
    COALESCE(Z09DATA.Number_colors_back, '') AS NUMBER_COLORS_BACK,
    COALESCE(Z09DATA.Print_characteristics, '') AS PRINT_CHARACTERISTICS,
    COALESCE(Z09DATA.Braille_text, '') AS BRAILLE_TEXT,
    -- Print characteristics individual flags
    COALESCE(Z09DATA.PrintChar_Braille, '') AS PRINTCHAR_BRAILLE,
    COALESCE(Z09DATA.PrintChar_FoilStamp, '') AS PRINTCHAR_FOILSTAMP,
    COALESCE(Z09DATA.PrintChar_GoldHotFoil, '') AS PRINTCHAR_GOLDHOTFOIL,
    COALESCE(Z09DATA.PrintChar_EmbossDeboss, '') AS PRINTCHAR_EMBOSSDEBOSS,
    COALESCE(Z09DATA.PrintChar_SpotVarnish, '') AS PRINTCHAR_SPOTVARNISH,
    COALESCE(Z09DATA.PrintChar_ScratchOff, '') AS PRINTCHAR_SCRATCHOFF,
    COALESCE(Z09DATA.PrintChar_Lamination, '') AS PRINTCHAR_LAMINATION,
    COALESCE(Z09DATA.PrintChar_DieCut, '') AS PRINTCHAR_DIECUT,
    COALESCE(Z09DATA.PrintChar_Perforation, '') AS PRINTCHAR_PERFORATION,
    COALESCE(Z09DATA.PrintChar_GlossVarnish, '') AS PRINTCHAR_GLOSSVARNISH,
    COALESCE(Z09DATA.PrintChar_Leafleting, '') AS PRINTCHAR_LEAFLETING,
    COALESCE(Z09DATA.PrintChar_Folding, '') AS PRINTCHAR_FOLDING,
    COALESCE(Z09DATA.PrintChar_RichPaleGold, '') AS PRINTCHAR_RICHPALEGOLD,
    COALESCE(Z09DATA.PrintChar_SilverHotFoil, '') AS PRINTCHAR_SILVERHOTFOIL,
    COALESCE(Z09DATA.PrintChar_Unvarnish, '') AS PRINTCHAR_UNVARNISH,
    COALESCE(Z09DATA.PrintChar_SecurityVarish, '') AS PRINTCHAR_SECURITYVARISH,
    COALESCE(Z09DATA.PrintChar_MattVarnish, '') AS PRINTCHAR_MATTVARNISH,
    COALESCE(Z09DATA.PrintChar_CodingBySupplier, '') AS PRINTCHAR_CODINGBYSUPPLIER,
    COALESCE(Z09DATA.PrintChar_BKLogo, '') AS PRINTCHAR_BKLOGO,
    COALESCE(Z09DATA.PrintChar_S_DR, '') AS PRINTCHAR_S_DR,
    -- Linked Documents
    COALESCE(DOCS.DRA_COMBINATION_AGG, '') AS DRA_COMBINATION,
    COALESCE(DOCS.DRA_COMBINATION_AGG_DKTXTUC, '') AS DRA_COMBINATION_DKTXTUC,
    COALESCE(DOCS.DRA_DIELINE_AGG, '') AS DRA_DIELINE,
    COALESCE(DOCS.DRA_DIELINE_AGG_DKTXTUC, '') AS DRA_DIELINE_DKTXTUC,
    COALESCE(DOCS.DRA_OTHER_AGG, '') AS DRA_OTHER,
    COALESCE(DOCS.DRA_OTHER_AGG_DKTXTUC, '') AS DRA_OTHER_DKTXTUC,
    regexp_replace (
        concat (
            'CD: ',
            COALESCE(DOCS.DRA_COMBINATION_AGG, '--'),
            '; Die: ',
            COALESCE(DOCS.DRA_DIELINE_AGG, '--'),
            '; Other: ',
            COALESCE(DOCS.DRA_OTHER_AGG, '--')
        ),
        'DRA_',
        ''
    ) AS DRA_ALL,
    concat (
        'CD: ',
        COALESCE(DOCS.DRA_COMBINATION_AGG_DKTXTUC, '--'),
        '; Die: ',
        COALESCE(DOCS.DRA_DIELINE_AGG_DKTXTUC, '--'),
        '; Other:',
        COALESCE(DOCS.DRA_OTHER_AGG_DKTXTUC, '--')
    ) AS DRA_ALL_DKTXTUC,
    COALESCE(DOCS.DRA_1, '') AS DRA_1,
    COALESCE(DOCS.DRA_2, '') AS DRA_2,
    COALESCE(DOCS.DRA_3, '') AS DRA_3,
    COALESCE(DOCS.DRA_4, '') AS DRA_4,
    COALESCE(DOCS.DRA_5, '') AS DRA_5,
    COALESCE(DOCS.DRA_6, '') AS DRA_6,
    COALESCE(DOCS.DRA_7, '') AS DRA_7,
    COALESCE(DOCS.DRA_8, '') AS DRA_8,
    COALESCE(DOCS.DRA_9, '') AS DRA_9,
    COALESCE(DOCS.DRA_10, '') AS DRA_10,
    COALESCE(DOCS.LRA, '') AS LRA,
    COALESCE(DOCS.LRA_VERSION, '') AS LRA_VERSION,
    COALESCE(DOCS.LRA_DATE, '') AS LRA_DATE,
    COALESCE(DOCS.LRA_FILENAME, '') AS LRA_FILENAME,
    COALESCE(DOCS.HRL, '') AS HRL,
    COALESCE(DOCS.HRL_VERSION, '') AS HRL_VERSION,
    COALESCE(DOCS.HRL_DATE, '') AS HRL_DATE,
    COALESCE(DOCS.ACS, '') AS ACS,
    COALESCE(DOCS.ACS_VERSION, '') AS ACS_VERSION,
    -- TPM
    TPM.TPM_PMD_NO AS TPM_DRAWING,
    TPMREL.TPM AS TPM,
    TPM.TPMTXT AS TPMTXT,
    TPM.TPM_STATUS AS TPM_STATUS,
    TPM.GLPT AS GLPT,
    TPM.GLPTTXT AS GLPTTXT,
    TPM.ECLASS AS ECLASS,
    TPM.ECLASSTXT AS ECLASSTXT,
    TPM.ECLASS_S AS ECLASS_S,
    TPM.ECLASS_STXT AS ECLASS_S_TXT
FROM
    -- Standard Material data - using base material tables
    -- Note: You may need to adjust table names and field mappings for your environment
    (
        SELECT DISTINCT
            mara.MATNR,
            makt.MAKTX,
            mara.MTART,
            mara.MSTAE,
            mara.PRDHA AS PRDHATXT -- Product hierarchy field might be named differently
        FROM
            efdataonelh_prd.generaldiscovery_masterdata_r.pmd_mara_view mara
            LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.pmd_makt_view makt ON mara.MATNR = makt.MATNR
            AND makt.SPRAS = 'E' -- English language
        WHERE
            mara.MATNR LIKE '%91967086%' -- Filter for material 91967086
    ) MATDATA
    -- Makeup
    LEFT JOIN y08_makeup MAKEUP ON MATDATA.MATNR = MAKEUP.MATNR18
    -- Plants
    LEFT JOIN plants_aggregated PLANTS ON MATDATA.MATNR = PLANTS.MATNR
    -- Z09 Data
    LEFT JOIN z09_pivot Z09DATA ON MATDATA.MATNR = Z09DATA.MATNR
    -- Linked Documents
    LEFT JOIN doc_info_current DOCS ON MATDATA.MATNR = DOCS.OBJKY
    -- TPM - Standard Join to have only materials with TPM
    JOIN tpm_relations TPMREL ON MATDATA.MATNR = TPMREL.MATNR
    LEFT JOIN tpm_data TPM ON TPMREL.PNGUID = TPM.PNGUID
WHERE
    MATDATA.MTART IN ('YTXT', 'YPM', 'YPMN') -- Material TYPE
    AND MATDATA.MSTAE < '9'
    AND left (TPM.TPM, 3) = 'TPM'
ORDER BY
    MATDATA.MATNR DESC;