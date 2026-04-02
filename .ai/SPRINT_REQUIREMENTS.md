## Sprint Requirements
<!-- Sprint ID: SCRUM-3 | Started: 2026-03-31 -->
<!-- Confluence Source: requirements v2 — https://fhir-healthcare.atlassian.net/wiki/spaces/~712020d364f26c180a47338114425b64719078/pages/1015810/requirements -->
**Sprint ID:** SCRUM-3

### Business Rules
- Create staging models for **three** data sources: MSSQL (remote), seed CSV (local), and AWS S3 (remote).
- All staging models must select all columns from their source and append `CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at`.
- All database object names must be `snake_case`.

### Transformation Logic

**1. MSSQL source (3 tables):**
- Connect via DuckDB MSSQL extension using env vars (`MSSQL_USER`, `MSSQL_PASSWORD`, `MSSQL_DATABASE`).
- `dbt_project.yml` `on-run-start` hooks:
  ```yaml
  on-run-start:
    - "INSTALL mssql FROM community;"
    - "LOAD mssql;"
    - "ATTACH 'mssql://{{ env_var(\"MSSQL_USER\") }}:{{ env_var(\"MSSQL_PASSWORD\") }}@127.0.0.1:1433?database={{ env_var(\"MSSQL_DATABASE\") }}' AS sql_server (TYPE MSSQL);"
  ```
- Select all columns from:
  - `sql_server.dbo.cats` → `stg_cats`
  - `sql_server.dbo.reviews` → `stg_reviews`
  - `sql_server.dbo.seafood_restaurants` → `stg_seafood_restaurants`

**2. Seed data (1 CSV):**
- Create `seeds/restaurant_reviews.csv` with 2 columns and 3 rows:
  ```csv
  restaurant_id,review
  101,5
  102,4
  103,5
  ```
- Staging model `stg_restaurant_reviews` references the seed via `{{ ref('restaurant_reviews') }}`.

**3. AWS S3 (1 CSV):**
- Read `s3://cat-photos-2026/dogs.csv` using DuckDB httpfs extension.
- S3 credentials are configured in `profiles.yml` via `env_var()`.
- Staging model `stg_dogs` reads directly via `read_csv_auto('s3://cat-photos-2026/dogs.csv')`.

### New Models / Sources
| Model | Source | Method |
|---|---|---|
| `stg_cats` | MSSQL `sql_server.dbo.cats` | `on-run-start` ATTACH + direct query |
| `stg_reviews` | MSSQL `sql_server.dbo.reviews` | `on-run-start` ATTACH + direct query |
| `stg_seafood_restaurants` | MSSQL `sql_server.dbo.seafood_restaurants` | `on-run-start` ATTACH + direct query |
| `stg_restaurant_reviews` | Seed CSV `restaurant_reviews.csv` | `{{ ref('restaurant_reviews') }}` |
| `stg_dogs` | S3 `s3://cat-photos-2026/dogs.csv` | `read_csv_auto()` via httpfs |

### Execution Prerequisites
- `.env` must contain `MSSQL_USER`, `MSSQL_PASSWORD`, `MSSQL_DATABASE`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.
- MSSQL server must be running and accessible at `127.0.0.1:1433`.
- S3 bucket `cat-photos-2026` must be accessible with the provided credentials.
- `source .env` or `load_dotenv()` must run before `dbt run`.

### Technical Dependencies
- dbt-duckdb (installed)
- DuckDB MSSQL community extension (installed at runtime via `on-run-start`)
- DuckDB httpfs extension (configured in `profiles.yml`)
- python-dotenv (in requirements.txt)

### Approved Assumptions
[None — pending Architect analysis]

### Acceptance Criteria
- All 5 staging models compile and run successfully via `dbt run`.
- `dbt test` passes with 0 failures (unique + not_null on all primary keys).
- `sources.yml` declares all external sources (MSSQL, S3).
- `schema.yml` documents all staging models with column descriptions and tests.
- Seed CSV `restaurant_reviews.csv` loads via `dbt seed`.

### Permanent Rules (will be promoted to CLAUDE.md on sprint close)
- **MSSQL via DuckDB:** Always use `(TYPE MSSQL)` in the ATTACH command and install the extension `FROM community`.