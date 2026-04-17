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
- Ingest the Los Angeles dataset using the public resource endpoint and persist it into the shared DuckDB warehouse used by dbt and Airflow.
- Pull the full dataset rather than a small sample window.

**2. Staging**
- Build stg_la_restaurants from the API-ingested raw table.
- Keep all source columns available in the staging model.
- Deduplicate the staged restaurant grain to unique normalized DBA names for downstream enrichment.

**3. Intermediate**
- Build int_seafood_restaurants by joining seafood restaurant data with the API restaurant dataset.
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
- The LA City API must be reachable during extraction.

### Technical Dependencies
- dbt-core
- dbt-duckdb
- duckdb
- astronomer-cosmos
- dlt with DuckDB support
- pandas
- python-dotenv

### Approved Assumptions
## A1: API-to-restaurant join key — APPROVED
1. **Ambiguity/Gap:** The requirements say int_seafood_restaurants should join seafood restaurant data with the LA API data, but no exact join key is provided.
2. **Decision:** Join using a normalized restaurant-name match: `UPPER(TRIM(COALESCE(dba_name, business_name)))` from the API against `UPPER(TRIM(name))` from seafood restaurants. Preserve all seafood restaurant rows with a left join even when no API match is found.
3. **Rationale:** Confluence TEAM INPUT approved the name-based mapping and the requirements explicitly point to dba_name as the business-facing match field.
4. **Implementation Impact:** Affects stg_la_restaurants, int_seafood_restaurants, and cat_review_profile. Adds normalized name handling and left-join behavior.

## A2: Dogs breed column defaulting — APPROVED
1. **Ambiguity/Gap:** The requirements say the dog table should include a breed column and that most dogs are beagles, but the current dogs source file does not contain a breed field.
2. **Decision:** Add a derived breed column to the dogs staging model and default current records to beagle unless a future upstream source provides an explicit breed value.
3. **Rationale:** This preserves a deterministic rule that can be replaced cleanly later.
4. **Implementation Impact:** Affects stg_dogs, int_cats_dogs, and cat_review_profile.

## A3: LA API staging grain — APPROVED
1. **Ambiguity/Gap:** The earlier draft used location_account as the staging primary key, but the Confluence review clarified that the business grain should instead follow unique DBA names.
2. **Decision:** Filter the LA API staging model to rows with a unique normalized dba_name and use normalized_restaurant_name as the primary key for stg_la_restaurants. Keep location_account as an informational source attribute only. Data loss from excluding duplicate DBA names is explicitly accepted.
3. **Rationale:** TEAM INPUT explicitly rejected the location_account key and directed us to use DBA name uniqueness instead.
4. **Implementation Impact:** stg_la_restaurants tests move to normalized_restaurant_name; downstream enrichment continues to join on the normalized restaurant name and excludes duplicate DBA-name records by design.

### Acceptance Criteria
- The LA restaurant API is ingested successfully into DuckDB using the dlt workflow.
- stg_la_restaurants and all sprint-touched downstream models compile and run successfully.
- Dog-related models include a breed column and preserve its values for downstream joins.
- cat_review_profile builds successfully from the required joins.
- The local DAG runs the ingest and dbt chain against the same DuckDB file without path drift.

### Permanent Rules (will be promoted to CLAUDE.md on sprint close)
- None.
