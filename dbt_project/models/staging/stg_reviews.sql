{{ config(materialized='table') }}

SELECT
    CAST(review_id AS INTEGER)        AS review_id,
    CAST(cat_id AS INTEGER)           AS cat_id,
    CAST(restaurant_id AS INTEGER)    AS restaurant_id,
    CAST(paws_rating AS VARCHAR)      AS paws_rating,
    CAST(hiss_count AS INTEGER)       AS hiss_count,
    CAST(review_text AS VARCHAR)      AS review_text,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ source('sql_server', 'reviews') }}
