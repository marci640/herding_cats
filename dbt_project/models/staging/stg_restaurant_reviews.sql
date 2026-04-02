{{ config(materialized='table') }}

SELECT
    CAST(restaurant_id AS INTEGER)    AS restaurant_id,
    CAST(review AS INTEGER)           AS review,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ ref('restaurant_reviews') }}
