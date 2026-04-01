# Active Assumptions — SCRUM-3

## A1: MSSQL Extension Does Not Exist (BLOCKER)
- **Ambiguity/Gap:** Requirements specify `INSTALL mssql FROM community` and `ATTACH ... (TYPE MSSQL)`. The DuckDB MSSQL community extension does **not exist** — HTTP 404 on all tested DuckDB versions (1.1.0–1.4.2) and platforms (osx_arm64, linux_amd64).
- **Decision (Proposed Default):** Replace `on-run-start` ATTACH approach with a **dlt ingestion pipeline** using `dlt.sources.sql_database` (backed by `pymssql` or `sqlalchemy+pyodbc`). dlt extracts MSSQL tables into the DuckDB `raw` schema. Staging models then read from `{{ source('raw', 'cats') }}`, `{{ source('raw', 'reviews') }}`, `{{ source('raw', 'seafood_restaurants') }}`. This reuses the existing dlt ingest task in the Airflow DAG. Requires adding `dlt[mssql]` (which installs `pymssql`) to `requirements.txt`.
- **Rationale:** dlt already has a production-grade SQL database source connector. This avoids a non-existent extension and keeps `dbt_project.yml` immutable (satisfies CLAUDE.md rule).
- **Implementation Impact:**
  - `dbt_project.yml`: NO changes needed (immutability preserved)
  - `include/dlt_sources/`: New MSSQL source module
  - `dags/dbt_pipeline_dag.py`: Update dlt_ingest task to include MSSQL extraction
  - `models/staging/sources.yml`: Add `raw.cats`, `raw.reviews`, `raw.seafood_restaurants`
  - `models/staging/stg_cats.sql`, `stg_reviews.sql`, `stg_seafood_restaurants.sql`: Use `{{ source('raw', ...) }}` instead of direct MSSQL query
  - `requirements.txt`: Add `dlt[mssql]` or `pymssql`
- **TPM Action:** `approve` / `edit` / `reject`

## A2: MSSQL Table Schemas Unknown
- **Ambiguity/Gap:** Requirements say "select all columns" from cats, reviews, seafood_restaurants but the actual column names and types are unknown. Cannot connect to discover schema (blocked by A1).
- **Decision (Proposed Default):** Once A1 is resolved and dlt extracts the tables, discover schemas at runtime. For now, schema.yml will define only the guaranteed columns: a primary key placeholder (`id`) and `processed_at`. After first dlt extraction, Architect will patch schema.yml with actual columns.
- **Rationale:** Cannot write a complete schema contract without seeing the data. Staging models will use `SELECT *, CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at` pattern to pass through all columns.
- **Implementation Impact:**
  - `models/staging/schema.yml`: Partial schema for MSSQL models (PK + processed_at only until table inspection)
  - `stg_cats.sql`, `stg_reviews.sql`, `stg_seafood_restaurants.sql`: `SELECT *` with processed_at appended
- **TPM Action:** `approve` / `edit` / `reject`

## A3: Seed CSV Column Names
- **Ambiguity/Gap:** Requirements specify "restaurant name, review text, star rating" with 3 columns and 3 rows. The Confluence page includes an image of sample data that cannot be read programmatically. Exact `snake_case` column names are not specified.
- **Decision (Proposed Default):** Use column names: `restaurant_name` (VARCHAR), `review_text` (VARCHAR), `star_rating` (INTEGER). Add a synthetic primary key `review_id` (INTEGER) since none is specified and every model requires a unique+not_null PK test per CLAUDE.md.
- **Rationale:** snake_case versions of the described columns. A synthetic PK is required by the testing standard.
- **Implementation Impact:**
  - `seeds/restaurant_reviews.csv`: 4 columns (review_id, restaurant_name, review_text, star_rating), 3 rows
  - `models/staging/schema.yml`: `stg_restaurant_reviews` with 5 columns (4 source + processed_at), PK tests on review_id
- **TPM Action:** `approve` / `edit` / `reject`

## A4: dbt_project.yml Immutability Exception
- **Ambiguity/Gap:** Requirements specify `on-run-start` hooks in `dbt_project.yml`. CLAUDE.md states "Never modify dbt_project.yml during a sprint run. Exception: seed configuration changes only."
- **Decision (Proposed Default):** Do NOT add `on-run-start` hooks (rendered moot by A1 resolution via dlt). No `dbt_project.yml` modifications needed.
- **Rationale:** A1's dlt-based approach eliminates the need for `on-run-start` hooks entirely. `dbt_project.yml` immutability rule is preserved.
- **Implementation Impact:** `dbt_project.yml` remains unchanged.
- **TPM Action:** `approve` / `edit` / `reject`

## A5: S3 dogs.csv Primary Key Confirmed
- **Ambiguity/Gap:** Requirements don't explicitly name the primary key for dogs.csv.
- **Decision (Proposed Default):** Use `dog_id` (BIGINT) as primary key. Confirmed by inspecting S3 file — schema is: `dog_id` (BIGINT), `name` (VARCHAR), `age_years` (DOUBLE), `favorite_toy` (VARCHAR), `judgmental_level` (BIGINT). 3 rows.
- **Rationale:** Direct inspection of `s3://cat-photos-2026/dogs.csv` confirmed the schema. `dog_id` is the natural primary key (sequential integers 1–3).
- **Implementation Impact:**
  - `models/staging/schema.yml`: `stg_dogs` with 6 columns (5 source + processed_at), PK tests on dog_id
- **TPM Action:** `approve` / `edit` / `reject`
