## Active Assumptions
<!-- Sprint ID: SCRUM-5 | Generated: 2026-04-15 -->
<!-- Confluence Source: assumptions — https://fhir-healthcare.atlassian.net/wiki/spaces/SUDS/pages/14712838/assumptions -->

## A1: API-to-restaurant join key
1. **Ambiguity/Gap:** The requirements say int_seafood_restaurants should join seafood restaurant data with the LA API data, but no exact join key is provided.
2. **Decision (Proposed Default):** Join using a normalized restaurant-name match: `UPPER(TRIM(COALESCE(dba_name, business_name)))` from the API against `UPPER(TRIM(name))` from seafood restaurants. Preserve all seafood restaurant rows with a left join even when no API match is found.
3. **Rationale:** The API does not expose the existing numeric `restaurant_id`, and the team note explicitly pointed to mapping `dba_name` to `name`.
4. **Implementation Impact:** Affects `stg_la_restaurants`, `int_seafood_restaurants`, and downstream `cat_review_profile`. Adds normalized name handling and left-join behavior.
5. **TPM Action:** approve / edit / reject

## A2: Dogs breed column defaulting
1. **Ambiguity/Gap:** The requirements say the dog table should include a breed column and that most dogs are beagles, but the current dogs source file does not contain a breed field.
2. **Decision (Proposed Default):** Add a derived `breed` column to the dogs staging model and default current records to `beagle` unless a future upstream source provides an explicit breed value.
3. **Rationale:** This satisfies the newly approved downstream requirement while preserving a deterministic rule that can be replaced cleanly later.
4. **Implementation Impact:** Affects `stg_dogs`, `int_cats_dogs`, and `cat_review_profile`. Adds the `breed` field to schema documentation and downstream joins.
5. **TPM Action:** approve / edit / reject

## A3: Primary key for LA API staging
1. **Ambiguity/Gap:** The LA API requirement does not specify the primary key for the new staging model.
2. **Decision (Proposed Default):** Use `location_account` as the primary key for `stg_la_restaurants`.
3. **Rationale:** It is present in the live API payload, non-human-readable, and suitable as a stable business location identifier.
4. **Implementation Impact:** Affects `stg_la_restaurants` tests and downstream enrichment columns in `int_seafood_restaurants` and `cat_review_profile`.
5. **TPM Action:** approve / edit / reject
