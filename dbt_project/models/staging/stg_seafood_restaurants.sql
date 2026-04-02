{{ config(materialized='table') }}

SELECT
    CAST(restaurant_id AS INTEGER)              AS restaurant_id,
    CAST(name AS VARCHAR)                       AS name,
    CAST(neighborhood AS VARCHAR)               AS neighborhood,
    CAST(specialty_dish AS VARCHAR)              AS specialty_dish,
    CAST(outdoor_seating_for_napping AS BOOLEAN) AS outdoor_seating_for_napping,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP)        AS processed_at
FROM {{ source('sql_server', 'seafood_restaurants') }}
