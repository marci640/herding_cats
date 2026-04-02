# Project Charter: Herding Cats Platform Template
**Goal:** Provide a reusable AI-centric dbt + Airflow ETL platform template, orchestrated by a Technical PM.

## Technical Standards
- **SQL Style:** Snowflake/DuckDB dialect; Uppercase keywords.
- **dbt Version:** 1.7+
- **Airflow:** Local execution using `Astro CLI` or `docker-compose`.
- **Testing:** Every model MUST have a `unique` and `not_null` test on the primary key.

## DuckDB Local Setup Notes
- **Profile schema:** `main` (default). Seeds load into `main` schema.
- **Seed path:** Place optional seed CSV files in `dbt_project/seeds/`.
- **Model reference:** Reference seeds with `ref('seed_name')` when used.
- **Prerequisites:** `pip install dbt-core dbt-duckdb`
- **External Database Connections:** When connecting to external databases via DuckDB extensions, always use `(TYPE [extension_name])` in the ATTACH command for network connections. 

## Definition of Done (DoD)
1. Staging and intermediate models compile successfully.
2. Transformations include `CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at` where required.
3. `dbt test` passes with 0 errors for sprint-touched models.
4. Airflow DAG runs `dbt seed` → `dbt run` → `dbt test` successfully.

## Zero-Tolerance Rules (Invariants)
- **Naming:** ALL database objects MUST be `snake_case`. No `CamelCase`, no `PascalCase`.
- **Handoffs:** The Transformer is FORBIDDEN from writing SQL until the Architect has produced a `schema.yml`.
- **Validation:** No PR can be generated unless the Auditor confirms 100% test coverage for Primary Keys.
- **Virtual Environment:** NEVER use system `python3`, `pip3`, or globally installed `dbt`. Always use `venv/bin/python`, `venv/bin/pip`, `venv/bin/dbt`. If `venv/bin/dbt` does not exist, halt and alert the user — do not fall back to system installs.

## System of Record (State Management)
- **Primary Logic:** `/.ai/SPRINT_REQUIREMENTS.md` (Updated by TPM)
- **Technical Spec:** `models/staging/schema.yml` (Updated by Architect)
- **Implementation:** `models/staging/*.sql` (Updated by Transformer)

## Agentic Handoff Protocol
1. **ARCHITECT:** Reads Requirements -> Generates `schema.yml`. 
   *IF schema.yml is missing documentation tags, the task is FAIL.*
2. **TRANSFORMER:** Reads `schema.yml` -> Generates SQL. 
   *SQL column names MUST match schema.yml exactly.*
3. **AUDITOR:** Executes `dbt compile` -> Compares SQL output against `schema.yml`.
   *Any mismatch triggers an automatic REJECT and REWORK loop.*

## Project Standards (Evolved)
Permanent rules promoted from completed sprints:
- **Profile Schema:** `main` (default). Seeds load into `main` schema — never use a custom `+schema` override for seeds in DuckDB.
- **Seed Reference Pattern:** Always use `ref('seed_name')` to reference seeds in models. Do not create a `sources.yml` entry for seeds.
- **External DB Connections:** When connecting to external databases via DuckDB extensions, always use `(TYPE [extension_name])` in the `ATTACH` command for network connections.
- **dbt_project.yml Immutability:** Never modify `dbt_project.yml` during a sprint run. Exception: seed configuration changes only.
- **Sprint Reset Timestamp Rollback:** During a sprint reset, restore `project_metadata.last_updated` in `/.ai/sprint_ledger.json` to the pre-sprint committed value.
- **Assumptions Consolidation Rule:** `/.ai/ACTIVE_ASSUMPTIONS.md` is temporary HITL state only. During sprint wrap-up, consolidate approved assumptions into the `### Approved Assumptions` section of the archived `sprint_[N]_requirements.md`.
- **Default Preflight Safety Gate:** Resolve all upstream table/model readiness issues for sprint-touched models before any full `dbt run` or `dbt test`.
- **Score Threshold Assumptions:** If score thresholds are ambiguous, they must be explicitly captured as approved assumptions before SQL merge.
- **Risk Classification Standards:** Any risk classification column must have `accepted_values` tests and documented business definitions.
- **Intervention Output Standards:** Intervention-facing categorical outputs must always include `accepted_values` tests and business definitions.
- **Confluence Version Tracking:** Whenever Confluence content is read into the process (requirements, assumptions, etc.), include a `Confluence Source: <page_title> v<N> — <URL>` line in the consuming file's header.- **MSSQL via DuckDB:** Always use `(TYPE MSSQL)` in the ATTACH command and install the extension `FROM community`.
