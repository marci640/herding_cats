{{ config(materialized='table') }}

SELECT
    c.cat_id,
    c.cat_name,
    d.dog_id,
    d.name AS dog_name,
    d.breed AS dog_breed,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ ref('int_cats') }} AS c
LEFT JOIN {{ ref('stg_dogs') }} AS d
    ON c.dog_friend = d.dog_id
