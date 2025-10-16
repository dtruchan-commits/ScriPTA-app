WITH 
-- Step 1: Base Z09 Data (equivalent to MV_P2R_Z09_DATA)
z09_base_data AS (
    SELECT DISTINCT
        -- Information on PTMS Z09 Classification
        inob.OBJEK AS MATNR,
        SUBSTRING(inob.OBJEK, 11, 18) AS MATNR8,
        ausp.ATINN,
        ausp.ATZHL,
        ausp.ATWRT,
        CAST(ausp.ATFLV AS STRING) AS ATFLV
    FROM efdataonelh_prd.generaldiscovery_masterdata_r.p2r_inob_view inob
    INNER JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_ausp_view ausp ON (
        inob.KLART = ausp.KLART
        AND inob.CUOBJ = ausp.OBJEK
        AND inob.MANDT = ausp.MANDT
        AND inob.OPSYS = ausp.OPSYS
    )
    WHERE inob.KLART = 'Z09'
        AND inob.OPSYS = 'P2R'
        AND inob.MANDT = '508'
        AND ausp.OPTYPE <> 'D'
),

-- Step 2: Z09 Data with Content (equivalent to MV_P2R_Z09_DATA_CONTENT)
z09_data_content AS (
    SELECT DISTINCT
        -- Information on PTMS Z09 Class and its Content
        base.MATNR,
        base.MATNR8,
        base.ATINN,
        cabnt.ATBEZ AS ATINN_TXT,
        base.ATZHL,
        base.ATWRT,
        base.ATFLV,
        CASE
            WHEN base.ATWRT = '' THEN base.ATFLV
            WHEN cawnt.ATWTB = '' THEN cawnt.ATWTB
            ELSE base.ATWRT
        END AS CONTENT
    FROM z09_base_data base
    LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cawnt_view cawnt 
        ON base.ATINN = cawnt.ATINN AND base.ATWRT = cawnt.ATWTB
    LEFT JOIN efdataonelh_prd.generaldiscovery_masterdata_r.p2r_cabnt_view cabnt 
        ON base.ATINN = cabnt.ATINN
    WHERE cabnt.SPRAS = 'E'
),

-- Step 3: Aggregated Content per Material/Attribute
z09_data_aggregated AS (
    SELECT
        MATNR,
        MATNR8,
        ATINN,
        CONCAT_WS(', ', COLLECT_LIST(CONTENT)) AS CONTENT_AGG
    FROM z09_data_content
    GROUP BY MATNR, MATNR8, ATINN
),

-- Step 4: Print Characteristics by value
z09_print_characteristics AS (
    SELECT
        MATNR,
        ATINN,
        CONTENT
    FROM z09_data_content
    GROUP BY MATNR, ATINN, CONTENT
)

-- Final Query: Z09 Data in Columns (equivalent to MV_P2R_Z09_DATA_CONTENT_IN_COLUMNS)
SELECT DISTINCT
    -- Information on PTMS Z09 Class and its Content by Material
    agg.MATNR,
    agg.MATNR8,
    MAX(CASE WHEN agg.ATINN = '0000028219' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_manufacturer_codetype,
    MAX(CASE WHEN agg.ATINN = '0000028220' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_manufacturer_code,
    MAX(CASE WHEN agg.ATINN = '0000028204' THEN agg.CONTENT_AGG ELSE NULL END) AS Responsible_for_specification,
    MAX(CASE WHEN agg.ATINN = '0000028223' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_manufacturer_material,
    MAX(CASE WHEN agg.ATINN = '0000028210' THEN agg.CONTENT_AGG ELSE NULL END) AS Layout_approved,
    MAX(CASE WHEN agg.ATINN = '0000028207' THEN agg.CONTENT_AGG ELSE NULL END) AS Usage_Prefix,
    MAX(CASE WHEN agg.ATINN = '0000028386' THEN agg.CONTENT_AGG ELSE NULL END) AS Number_of_pages,
    MAX(CASE WHEN agg.ATINN = '0000028228' THEN agg.CONTENT_AGG ELSE NULL END) AS ACF_Flag,
    MAX(CASE WHEN agg.ATINN = '0000028216' THEN agg.CONTENT_AGG ELSE NULL END) AS Visible_Markings,
    MAX(CASE WHEN agg.ATINN = '0000028215' THEN agg.CONTENT_AGG ELSE NULL END) AS Code,
    MAX(CASE WHEN agg.ATINN = '0000028211' THEN agg.CONTENT_AGG ELSE NULL END) AS Colors,
    MAX(CASE WHEN agg.ATINN = '0000028212' THEN agg.CONTENT_AGG ELSE NULL END) AS Number_colors_front,
    MAX(CASE WHEN agg.ATINN = '0000028222' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_manufacturer,
    MAX(CASE WHEN agg.ATINN = '0000028206' THEN agg.CONTENT_AGG ELSE NULL END) AS Article_codetype,
    MAX(CASE WHEN agg.ATINN = '0000028205' THEN agg.CONTENT_AGG ELSE NULL END) AS Article_code,
    MAX(CASE WHEN agg.ATINN = '0000028224' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_man_visible_markings,
    MAX(CASE WHEN agg.ATINN = '0000028221' THEN agg.CONTENT_AGG ELSE NULL END) AS Contract_manufacturer_mt_index,
    MAX(CASE WHEN agg.ATINN = '0000028214' THEN agg.CONTENT_AGG ELSE NULL END) AS Component_scrab_key,
    MAX(CASE WHEN agg.ATINN = '0000028225' THEN agg.CONTENT_AGG ELSE NULL END) AS Remarks,
    MAX(CASE WHEN agg.ATINN = '0000028208' THEN agg.CONTENT_AGG ELSE NULL END) AS Printed,
    MAX(CASE WHEN agg.ATINN = '0000028213' THEN agg.CONTENT_AGG ELSE NULL END) AS Number_colors_back,
    MAX(CASE WHEN agg.ATINN = '0000028227' THEN agg.CONTENT_AGG ELSE NULL END) AS Print_characteristics,
    MAX(CASE WHEN agg.ATINN = '0000028209' THEN agg.CONTENT_AGG ELSE NULL END) AS Braille_text,
    -- Print Characteristics Boolean Flags
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '1' THEN 'Yes' ELSE 'No' END) AS PrintChar_Braille,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '2' THEN 'Yes' ELSE 'No' END) AS PrintChar_FoilStamp,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '3' THEN 'Yes' ELSE 'No' END) AS PrintChar_Varnish,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '4' THEN 'Yes' ELSE 'No' END) AS PrintChar_Cryptoglyph,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '5' THEN 'Yes' ELSE 'No' END) AS PrintChar_PseudoCryptoglyph,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '6' THEN 'Yes' ELSE 'No' END) AS PrintChar_Peak,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '7' THEN 'Yes' ELSE 'No' END) AS PrintChar_Embossing,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '8' THEN 'Yes' ELSE 'No' END) AS PrintChar_CoinReactiveInk,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '9' THEN 'Yes' ELSE 'No' END) AS PrintChar_IriodinLacquer,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '10' THEN 'Yes' ELSE 'No' END) AS PrintChar_UVLacquer,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '11' THEN 'Yes' ELSE 'No' END) AS PrintChar_PerlmuttLacquer,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '12' THEN 'Yes' ELSE 'No' END) AS PrintChar_RichPaleGold,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '13' THEN 'Yes' ELSE 'No' END) AS PrintChar_SilverHotFoil,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '14' THEN 'Yes' ELSE 'No' END) AS PrintChar_Unvarnish,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '15' THEN 'Yes' ELSE 'No' END) AS PrintChar_SecurityVarnish,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '16' THEN 'Yes' ELSE 'No' END) AS PrintChar_MattVarnish,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '17' THEN 'Yes' ELSE 'No' END) AS PrintChar_CodingBySupplier,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '18' THEN 'Yes' ELSE 'No' END) AS PrintChar_BKLogo,
    MAX(CASE WHEN char.ATINN = '0000028227' AND char.CONTENT = '19' THEN 'Yes' ELSE 'No' END) AS PrintChar_S_DR
FROM z09_data_aggregated agg
LEFT JOIN z09_print_characteristics char ON agg.MATNR = char.MATNR
GROUP BY agg.MATNR, agg.MATNR8
ORDER BY agg.MATNR;

