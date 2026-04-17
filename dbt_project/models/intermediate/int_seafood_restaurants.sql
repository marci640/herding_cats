{{ config(materialized='table') }}

SELECT
    s.restaurant_id,
    s.name AS restaurant_name,
    s.neighborhood,
    s.specialty_dish,
    s.outdoor_seating_for_napping,
    a.location_account AS api_location_account,
    a.dba_name AS api_dba_name,
    a.business_name AS api_business_name,
    a.street_address AS api_street_address,
    a.city AS api_city,
    a.zip_code AS api_zip_code,
    CASE
        WHEN a.normalized_restaurant_name IS NULL THEN 'unmatched'
        ELSE 'matched'
    END AS api_match_status,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ ref('stg_seafood_restaurants') }} AS s
LEFT JOIN {{ ref('stg_la_restaurants') }} AS a
    ON UPPER(TRIM(s.name)) = a.normalized_restaurant_name
