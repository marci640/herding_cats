{{ config(materialized='table') }}

SELECT
    r.review_id,
    r.cat_id,
    c.cat_name,
    c.dog_id AS dog_friend,
    c.dog_name,
    c.dog_breed,
    r.restaurant_id,
    s.restaurant_name,
    s.api_location_account,
    rr.review AS review_score,
    r.paws_rating,
    r.hiss_count,
    r.review_text,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ ref('stg_reviews') }} AS r
LEFT JOIN {{ ref('int_cats_dogs') }} AS c
    ON r.cat_id = c.cat_id
LEFT JOIN {{ ref('int_seafood_restaurants') }} AS s
    ON r.restaurant_id = s.restaurant_id
LEFT JOIN {{ ref('stg_restaurant_reviews') }} AS rr
    ON r.restaurant_id = rr.restaurant_id
