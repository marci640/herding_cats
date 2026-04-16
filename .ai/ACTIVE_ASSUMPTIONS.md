## Active Assumptions
<!-- Sprint ID: SCRUM-5 | Regenerated: 2026-04-16 -->
<!-- Confluence Source: 🤖 assumptions SCRUM-5 — https://fhir-healthcare.atlassian.net/wiki/spaces/SUDS/pages/16711681/assumptions+SCRUM-5 -->

## A1: API-to-restaurant join key
1. **Ambiguity/Gap:** The requirements say int_seafood_restaurants should join seafood restaurant data with the LA API data, but no exact join key is provided.
2. **Decision:** Join using a normalized restaurant-name match: `UPPER(TRIM(COALESCE(dba_name, business_name)))` from the API against `UPPER(TRIM(name))` from seafood restaurants. Preserve all seafood restaurant rows with a left join even when no API match is found.
3. **Rationale:** Confluence TEAM INPUT approved the name-based mapping and the requirements explicitly point to `dba_name` as the business-facing match field.
4. **Implementation Impact:** Affects `stg_la_restaurants`, `int_seafood_restaurants`, and downstream `cat_review_profile`. Adds normalized name handling and left-join behavior.
5. **TPM Action:** Resolved in Confluence TEAM INPUT — approved.

## A2: Dogs breed column defaulting
1. **Ambiguity/Gap:** The requirements say the dog table should include a breed column and that most dogs are beagles, but the current dogs source file does not contain a breed field.
2. **Decision:** Add a derived `breed` column to the dogs staging model and default current records to `beagle` unless a future upstream source provides an explicit breed value.
3. **Rationale:** Confluence TEAM INPUT approved this default and it preserves a deterministic rule that can be replaced cleanly later.
4. **Implementation Impact:** Affects `stg_dogs`, `int_cats_dogs`, and `cat_review_profile`. Adds the `breed` field to schema documentation and downstream joins.
5. **TPM Action:** Resolved in Confluence TEAM INPUT — approved.

## A3: LA API staging grain
1. **Ambiguity/Gap:** The earlier draft used `location_account` as the staging primary key, but the Confluence review clarified that the business grain should instead follow unique DBA names.
2. **Decision:** Filter the LA API staging model to rows with a unique normalized `dba_name` and use `normalized_restaurant_name` as the primary key for `stg_la_restaurants`. Keep `location_account` as an informational source attribute only. Data loss from excluding duplicate DBA names is explicitly accepted.
3. **Rationale:** TEAM INPUT explicitly rejected the `location_account` key and directed us to use DBA name uniqueness instead.
4. **Implementation Impact:** `stg_la_restaurants` tests move to `normalized_restaurant_name`; downstream enrichment continues to join on the normalized restaurant name and will exclude duplicate DBA-name records by design.
5. **TPM Action:** Approved.
