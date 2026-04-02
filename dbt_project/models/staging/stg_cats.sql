{{ config(materialized='table') }}

SELECT
    CAST(cat_id AS INTEGER)           AS cat_id,
    CAST(name AS VARCHAR)             AS name,
    CAST(age_years AS DECIMAL(4,1))   AS age_years,
    CAST(favorite_toy AS VARCHAR)     AS favorite_toy,
    CAST(judgmental_level AS INTEGER)  AS judgmental_level,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ source('sql_server', 'cats') }}
