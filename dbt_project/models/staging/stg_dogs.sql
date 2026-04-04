{% set dogs_csv_local_path = env_var('DOGS_CSV_LOCAL_PATH', '') %}

{{ config(materialized='table') }}

SELECT
    CAST(dog_id AS BIGINT)            AS dog_id,
    CAST(name AS VARCHAR)             AS name,
    CAST(age_years AS DOUBLE)         AS age_years,
    CAST(favorite_toy AS VARCHAR)     AS favorite_toy,
    CAST(judgmental_level AS BIGINT)   AS judgmental_level,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at
FROM read_csv_auto(
    '{% if dogs_csv_local_path %}{{ dogs_csv_local_path }}{% else %}s3://cat-photos-2026/dogs.csv{% endif %}'
)
