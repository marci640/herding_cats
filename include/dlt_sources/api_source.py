"""dlt source for the Los Angeles restaurant dataset."""

import os
from pathlib import Path

import dlt
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


BASE_URL = "https://data.lacity.org/resource/9hvm-fgmm.json"
PAGE_SIZE = 1000


@dlt.resource(table_name="raw_api_data", write_disposition="replace")
def get_api_data():
    """Fetch the full LA restaurant dataset and yield one row at a time."""
    offset = 0

    while True:
        response = requests.get(
            BASE_URL,
            params={"$limit": PAGE_SIZE, "$offset": offset},
            timeout=30,
        )
        response.raise_for_status()
        rows = response.json()

        if not rows:
            break

        for row in rows:
            yield row

        if len(rows) < PAGE_SIZE:
            break

        offset += PAGE_SIZE


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
    db_path = os.getenv("DBT_DUCKDB_PATH")
    pipeline = dlt.pipeline(
        pipeline_name="api_to_duckdb",
        destination=dlt.destinations.duckdb(db_path),
        dataset_name="raw",
    )
    load_info = pipeline.run(api_source())
    print(load_info)
