"""
Airflow DAG: dbt_pipeline
Herding Cats ETL orchestration DAG.
Flow: dlt ingest (raw schema) -> dbt seed -> Cosmos dbt transform (run + test)
"""

import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from pendulum import datetime

from airflow.decorators import dag, task
from cosmos import (
    DbtSeedLocalOperator,
    DbtTaskGroup,
    ExecutionConfig,
    ProfileConfig,
    ProjectConfig,
    RenderConfig,
    TestBehavior,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
AIRFLOW_HOME = Path(__file__).resolve().parent.parent
load_dotenv(AIRFLOW_HOME / ".env")  # Load S3/MSSQL creds for dbt + dlt tasks

DBT_PROJECT_PATH = AIRFLOW_HOME / "dbt_project"
DB_PATH = Path(os.getenv("DBT_DUCKDB_PATH", str(AIRFLOW_HOME / "warehouse.duckdb")))
DBT_BIN = str(AIRFLOW_HOME / "venv" / "bin" / "dbt")

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Shared Cosmos configs
PROFILE_CONFIG = ProfileConfig(
    profile_name="herding_cats",
    target_name="dev",
    profiles_yml_filepath=DBT_PROJECT_PATH / "profiles.yml",
)

EXECUTION_CONFIG = ExecutionConfig(
    dbt_executable_path=DBT_BIN,
)


@dag(
    dag_id="dbt_pipeline",
    description="Herding Cats dlt ingest + dbt seed/transform/test pipeline.",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["dbt", "dlt", "cosmos", "orchestration"],
)
def dbt_pipeline():

    # ------------------------------------------------------------------
    # 1. Ingest: dlt loads source data into DuckDB
    # ------------------------------------------------------------------
    @task
    def dlt_ingest():
        """
        Runs dlt pipeline(s) to load source data into the 'raw' schema
        in DuckDB. dbt then reads from raw via source() references.
        """
        import sys

        import dlt  # import inside task to avoid scheduler parse overhead

        project_root = str(AIRFLOW_HOME)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        from include.dlt_sources.api_source import api_source

        pipeline = dlt.pipeline(
            pipeline_name="source_ingestion",
            destination=dlt.destinations.duckdb(str(DB_PATH)),
            dataset_name="raw",
        )

        # Pass one or many sources/resources:
        #   pipeline.run([api_source(), other_source()])
        info = pipeline.run(api_source())
        log.info("dlt load complete: %s", info)

    # ------------------------------------------------------------------
    # 2. Seed: load CSV seeds into DuckDB (no-op when seeds/ is empty)
    # ------------------------------------------------------------------
    seed = DbtSeedLocalOperator(
        task_id="dbt_seed",
        project_dir=DBT_PROJECT_PATH,
        profile_config=PROFILE_CONFIG,
        execution_config=EXECUTION_CONFIG,
    )

    # ------------------------------------------------------------------
    # 3. Transform + Test: Cosmos renders dbt models as Airflow tasks
    # ------------------------------------------------------------------
    transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=PROFILE_CONFIG,
        execution_config=EXECUTION_CONFIG,
        render_config=RenderConfig(
            test_behavior=TestBehavior.AFTER_EACH,
        ),
    )

    # ------------------------------------------------------------------
    # Dependency chain
    # ------------------------------------------------------------------
    dlt_ingest() >> seed >> transform


dbt_pipeline()
