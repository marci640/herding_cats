"""
dlt source: Example API ingestion.
Replace the URL and parsing logic with your real source.
Each @dlt.resource becomes a table in the destination.
Group related resources under the @dlt.source for schema management.
"""

import dlt
import requests


@dlt.resource(table_name="raw_api_data", write_disposition="replace")
def get_api_data():
    """Fetch data from an external API and yield rows for dlt to load."""
    url = "https://api.example.com/data"
    response = requests.get(url)
    response.raise_for_status()
    yield response.json()


# ---------------------------------------------------------------------------
# Add more resources here. Each one maps to a separate destination table.
# ---------------------------------------------------------------------------
# @dlt.resource(table_name="raw_other_data", write_disposition="replace")
# def get_other_data():
#     ...


@dlt.source
def api_source():
    """Groups all API-related resources under a single source."""
    return [get_api_data()]


if __name__ == "__main__":
    """Standalone run for local testing outside Airflow."""
    pipeline = dlt.pipeline(
        pipeline_name="api_to_duckdb",
        destination="duckdb",
        dataset_name="raw",
    )
    load_info = pipeline.run(api_source())
    print(load_info)
