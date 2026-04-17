{{ config(materialized='table') }}

WITH source_data AS (
    SELECT
        CAST(location_account AS VARCHAR)              AS location_account,
        CAST(business_name AS VARCHAR)                 AS business_name,
        CAST(dba_name AS VARCHAR)                      AS dba_name,
        CAST(street_address AS VARCHAR)                AS street_address,
        CAST(city AS VARCHAR)                          AS city,
        CAST(zip_code AS VARCHAR)                      AS zip_code,
        CAST(location_description AS VARCHAR)          AS location_description,
        CAST(location_start_date AS DATE)              AS location_start_date,
        CAST(mailing_address AS VARCHAR)               AS mailing_address,
        CAST(mailing_city AS VARCHAR)                  AS mailing_city,
        CAST(mailing_zip_code AS VARCHAR)              AS mailing_zip_code,
        CAST(council_district AS VARCHAR)              AS council_district,
        CAST(naics AS VARCHAR)                         AS naics,
        CAST(primary_naics_description AS VARCHAR)     AS primary_naics_description,
        CAST(location_1__type AS VARCHAR)              AS location_1,
        UPPER(TRIM(COALESCE(CAST(dba_name AS VARCHAR), CAST(business_name AS VARCHAR)))) AS normalized_restaurant_name
    FROM {{ source('raw', 'raw_api_data') }}
),
ranked AS (
    SELECT
        *,
        COUNT(*) OVER (PARTITION BY normalized_restaurant_name) AS restaurant_name_count,
        ROW_NUMBER() OVER (PARTITION BY normalized_restaurant_name ORDER BY location_account) AS restaurant_name_rank
    FROM source_data
    WHERE normalized_restaurant_name IS NOT NULL
      AND normalized_restaurant_name <> ''
)
SELECT
    location_account,
    business_name,
    dba_name,
    street_address,
    city,
    zip_code,
    location_description,
    location_start_date,
    mailing_address,
    mailing_city,
    mailing_zip_code,
    council_district,
    naics,
    primary_naics_description,
    location_1,
    normalized_restaurant_name,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM ranked
WHERE restaurant_name_count = 1
  AND restaurant_name_rank = 1
