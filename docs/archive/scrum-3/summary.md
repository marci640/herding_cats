# Sprint 3 Archive — Sprint 01 — Staging Data
**Closed:** 2026-04-02
**Version:** 0.1.1
**Branch:** `SCRUM-3`

## Business Rules Applied
- Staging models created for three data sources: MSSQL, seed CSV, S3.
- All models dynamically append `CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS processed_at`.
- Strict enforcement of `snake_case` naming across all objects.

## Permanent Rules Promoted to CLAUDE.md
- **MSSQL via DuckDB:** Always use `(TYPE MSSQL)` in the ATTACH command and install the extension `FROM community`.

## Artifacts Produced
| File | Action |
|---|---|
| `models/staging/schema.yml` | Created |
| `models/staging/sources.yml` | Created |
| `models/staging/stg_cats.sql` | Created |
| `models/staging/stg_reviews.sql` | Created |
| `models/staging/stg_seafood_restaurants.sql` | Created |
| `models/staging/stg_restaurant_reviews.sql` | Created |
| `models/staging/stg_dogs.sql` | Created |
| `seeds/restaurant_reviews.csv` | Created |

## Test Results
Passed 21 / 21 total tests.
0 Failures.

## Auditor Findings
No findings. Completed successful audit across all constraints.
