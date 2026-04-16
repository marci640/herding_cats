## Sprint Requirements
<!-- Sprint ID: SCRUM-5 | Started: 2026-04-15 -->
<!-- Confluence Source: requirements — https://fhir-healthcare.atlassian.net/wiki/spaces/SUDS/pages/14614534/requirements -->
**Sprint ID:** SCRUM-5

### Business Rules
- Create a new API-backed staging model named stg_la_restaurants using the Los Angeles public restaurant dataset.
- Reuse the existing dlt and Airflow orchestration pattern so ingestion completes before dbt transformations run.
- Preserve all available source columns from the API-backed raw table unless a downstream contract requires an explicit rename.
- Ensure dog-related data includes a breed column for downstream use, with most current dog records expected to be beagles.
- Keep all database objects in snake_case and include processed_at timestamps where required by project standards.

### Transformation Logic
**1. API ingestion**
- Ingest the Los Angeles dataset from https://data.lacity.org/api/v3/views/9hvm-fgmm/query.json using the existing dlt pipeline pattern.
- The endpoint is public and does not require authentication.
- Pull the full dataset, approximately 9000 rows, rather than a small sample window.
- Persist the ingested table into DuckDB so dbt can read from the same absolute database path used by the DAG.

**2. Staging**
- Build stg_la_restaurants from the API-ingested raw table.
- Keep all source columns available in the staging model.
- Update source declarations and schema documentation/tests to include the new API-backed data.
- Preserve the stg_ naming convention for restaurant reviews and all staging outputs.

**3. Intermediate**
- Build int_seafood_restaurants by joining seafood restaurant data with the API restaurant dataset and retaining the required columns from both.
- Ensure the dogs data exposed to downstream models includes a breed column, with most current records expected to be beagles.
- Update int_cats to add a dog_friend column populated with the matching dog_id.
- Only Sir Meows-a-Lot should map to Sir Barks-a-Lot for the dog_friend relationship.
- Build int_cats_dogs by joining cats to dogs on dog_friend.

**4. Final output**
- Build a cat_review_profile model that combines the relevant cat, dog, restaurant, and review data using the appropriate primary and foreign key relationships.

### New Models / Sources
| Model | Source | Method |
|---|---|---|
| stg_la_restaurants | LA City restaurant API | dlt ingestion into DuckDB raw table, then dbt staging |
| int_seafood_restaurants | stg_seafood_restaurants + stg_la_restaurants | dbt join preserving required columns |
| int_cats | stg_cats + stg_dogs logic | dbt enrichment with dog_friend mapping |
| int_cats_dogs | int_cats + stg_dogs | dbt join on dog_friend |
| cat_review_profile | staged and intermediate models | dbt final model |

### Execution Prerequisites
- Load the project environment from .env before running the DAG or dbt commands.
- Ensure dlt and dbt point to the same absolute DuckDB database path.
- The existing Airflow DAG should be used for local validation of the ingest and transform chain.
- The LA City API must be reachable during extraction.

### Technical Dependencies
- dbt-core
- dbt-duckdb
- duckdb
- astronomer-cosmos
- dlt with DuckDB support
- pandas
- sodapy
- python-dotenv

### Approved Assumptions
- None yet.

### Acceptance Criteria
- The LA restaurant API is ingested successfully into DuckDB using the existing dlt workflow.
- stg_la_restaurants and all sprint-touched downstream models compile and run successfully.
- schema.yml and sources.yml are updated to document the new data flow and tests.
- dog-related models include a breed column and preserve its values for downstream joins, with most current records expected to be beagles.
- dog_friend logic is implemented correctly for Sir Meows-a-Lot and Sir Barks-a-Lot.
- cat_review_profile builds successfully from the required joins.
- The local DAG runs the ingest and dbt chain against the same DuckDB file without path drift.

### Permanent Rules (will be promoted to CLAUDE.md on sprint close)
- None yet.
