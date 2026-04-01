# Active Assumptions — SCRUM-3

## A1: MSSQL Extension Availability — RESOLVED
- **Original Issue:** DuckDB MSSQL community extension returned HTTP 404 on DuckDB 1.4.2.
- **Resolution:** Upgraded DuckDB from 1.4.2 → 1.4.4. Extension installs and loads successfully. `on-run-start` hooks in `dbt_project.yml` work as intended.
- **Status:** ✅ RESOLVED — no TPM action needed.

## A2: MSSQL Table Schemas — RESOLVED
- **Original Issue:** Could not connect to MSSQL to discover table schemas (blocked by A1).
- **Resolution:** Connected to MSSQL via DuckDB extension. Discovered all 3 tables in `sql_server.dbo` schema:
  - **cats** (3 rows): `cat_id` INTEGER (PK), `name` VARCHAR, `age_years` DECIMAL(4,1), `favorite_toy` VARCHAR, `judgmental_level` INTEGER
  - **reviews** (3 rows): `review_id` INTEGER (PK), `cat_id` INTEGER (FK), `restaurant_id` INTEGER (FK), `paws_rating` VARCHAR, `hiss_count` INTEGER, `review_text` VARCHAR
  - **seafood_restaurants** (3 rows): `restaurant_id` INTEGER (PK), `name` VARCHAR, `neighborhood` VARCHAR, `specialty_dish` VARCHAR, `outdoor_seating_for_napping` BOOLEAN
- **Status:** ✅ RESOLVED — schema.yml updated with actual columns.

## A3: Seed CSV Column Names
- **Ambiguity/Gap:** Requirements specify "restaurant name, review text, star rating" with 3 columns and 3 rows. Exact `snake_case` column names are not specified.
- **Decision (Proposed Default):** Use column names: `restaurant_name` (VARCHAR), `review_text` (VARCHAR), `star_rating` (INTEGER). Add a synthetic primary key `review_id` (INTEGER) since none is specified and every model requires a unique+not_null PK test per CLAUDE.md.
- **Rationale:** snake_case versions of the described columns. A synthetic PK is required by the testing standard.
- **Implementation Impact:**
  - `seeds/restaurant_reviews.csv`: 4 columns (review_id, restaurant_name, review_text, star_rating), 3 rows
  - `models/staging/schema.yml`: `stg_restaurant_reviews` with 5 columns (4 source + processed_at), PK tests on review_id
- **TPM Action:** `approve` / `edit` / `reject`

## A4: dbt_project.yml Modification — RESOLVED
- **Original Issue:** CLAUDE.md rule says "Never modify dbt_project.yml during a sprint run." Requirements specify `on-run-start` hooks.
- **Resolution:** TPM directly modified `dbt_project.yml` to add `on-run-start` hooks (MSSQL install/load/attach). This is a TPM override of the immutability rule for this sprint since the hooks are part of the sprint requirements.
- **Status:** ✅ RESOLVED — TPM-directed change, no further action needed.

## A5: S3 dogs.csv Primary Key — RESOLVED
- **Original Issue:** Requirements don't explicitly name the primary key for dogs.csv.
- **Resolution:** Confirmed by inspecting S3 file. `dog_id` (BIGINT) is the natural PK (sequential 1–3). Schema: `dog_id`, `name`, `age_years`, `favorite_toy`, `judgmental_level`. 3 rows.
- **Status:** ✅ RESOLVED — schema.yml updated.
