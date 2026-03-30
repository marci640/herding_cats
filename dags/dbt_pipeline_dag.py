"""
Airflow DAG: dbt_pipeline
Generic dbt orchestration skeleton for the Herding Cats template.
Runs: dbt seed -> dbt run -> dbt test
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DBT_PROJECT_DIR = Path(__file__).resolve().parent.parent / "dbt_project"
DBT_PROFILES_DIR = DBT_PROJECT_DIR
DBT_BIN = Path(__file__).resolve().parent.parent / "venv" / "bin" / "dbt"

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# ---------------------------------------------------------------------------
# DAG Definition
# ---------------------------------------------------------------------------
with DAG(
    dag_id="dbt_pipeline",
    default_args=DEFAULT_ARGS,
    description="Generic dbt seed/run/test orchestration DAG.",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dbt", "template", "orchestration"],
) as dag:

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            f"{DBT_BIN} seed --profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            f"{DBT_BIN} run --profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            f"{DBT_BIN} test --profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    # Task dependency chain
    dbt_seed >> dbt_run >> dbt_test
