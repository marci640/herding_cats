{{ config(materialized='table') }}

WITH dog_lookup AS (
    SELECT MAX(dog_id) AS sir_barks_a_lot_id
    FROM {{ ref('stg_dogs') }}
    WHERE name = 'Sir Barks-a-Lot'
)
SELECT
    c.cat_id,
    c.name AS cat_name,
    c.age_years,
    c.favorite_toy,
    c.judgmental_level,
    CASE
        WHEN c.name = 'Sir Meows-a-Lot' THEN d.sir_barks_a_lot_id
        ELSE NULL
    END AS dog_friend,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM {{ ref('stg_cats') }} AS c
CROSS JOIN dog_lookup AS d
