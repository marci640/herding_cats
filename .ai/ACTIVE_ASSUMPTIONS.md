# Active Assumptions — SCRUM-3
<!-- Confluence Source: requirements v2 — https://fhir-healthcare.atlassian.net/wiki/spaces/~712020d364f26c180a47338114425b64719078/pages/1015810/requirements -->
## A1: MSSQL Extension Availability — RESOLVED
1. **Ambiguity/Gap:** Requirements specify DuckDB MSSQL community extension but it returned HTTP 404 on DuckDB 1.4.2.
2. **Decision:** Upgrade DuckDB from 1.4.2 → 1.4.4 to install the extension successfully and use `on-run-start` hooks.
3. **Rationale:** Upgrading to 1.4.4 is the supported path to ensure the extension installs and loads properly for MSSQL connections.
4. **Implementation Impact:** DuckDB version bumped; `dbt_project.yml` hooks enabled.
5. **TPM Action:** ✅ RESOLVED — no TPM action needed.

## A2: MSSQL Table Schemas — RESOLVED
1. **Ambiguity/Gap:** Could not connect to MSSQL initially (blocked by A1), so exact table schemas were unknown.
2. **Decision:** Discovered tables `cats`, `reviews`, `seafood_restaurants` via DuckDB extension and mapped exact schemas (e.g., `cat_id` INTEGER PK, etc).
3. **Rationale:** Accurate table definitions are required for staging SQL.
4. **Implementation Impact:** `schema.yml` updated with actual columns.
5. **TPM Action:** ✅ RESOLVED — schema.yml updated with actual columns.

## A3: Seed CSV Column Names — RESOLVED
1. **Ambiguity/Gap:** Exact seed CSV column names were not specified in initial requirements.
2. **Decision:** Use explicit columns from updated requirements: `restaurant_id` (INTEGER, PK), `review` (INTEGER). No synthetic PK.
3. **Rationale:** Aligns with Confluence requirements (v2) specifying natural PK.
4. **Implementation Impact:** `schema.yml` and staging models updated to match explicit columns.
5. **TPM Action:** ✅ RESOLVED — schema.yml updated to match Confluence-specified columns.

## A4: dbt_project.yml Modification — RESOLVED
1. **Ambiguity/Gap:** CLAUDE.md prohibits modifying `dbt_project.yml` during a sprint run, but MSSQL `on-run-start` hooks are required for sprint setup.
2. **Decision:** Override immutability rule to add `on-run-start` hooks for MSSQL install/load/attach.
3. **Rationale:** TPM directly authorized this override as the hooks are part of the core sprint requirements.
4. **Implementation Impact:** `dbt_project.yml` modified by TPM.
5. **TPM Action:** ✅ RESOLVED — TPM-directed change, no further action needed.

## A5: S3 dogs.csv Primary Key — RESOLVED
1. **Ambiguity/Gap:** Requirements don't explicitly name the primary key for `dogs.csv`.
2. **Decision:** Use `dog_id` (BIGINT) as the natural PK.
3. **Rationale:** Confirmed by inspecting S3 file which contains sequence 1-3.
4. **Implementation Impact:** `schema.yml` updated.
5. **TPM Action:** ✅ RESOLVED — schema.yml updated.
