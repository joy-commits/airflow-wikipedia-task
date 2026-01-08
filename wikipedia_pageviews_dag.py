from airflow.sdk import DAG
from pendulum import datetime, duration
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.smtp.operators.smtp import EmailOperator
from Wikipedia_pageviews.include.download import download_file 
from Wikipedia_pageviews.include.extract import extract_file
from Wikipedia_pageviews.include.process import process_and_load


# DAG Definition

with DAG(
    dag_id="wikipedia_pageviews",
    start_date=datetime(2025, 12, 25),
    schedule=None,
    catchup=False,
    default_args={
        "owner": "Ufuoma",
        "retries": 3,
        "retry_delay": duration(seconds=40)
    },
    template_searchpath = "/opt/airflow/dags/Wikipedia_pageviews/include/"
):

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres_conn",
        sql="include/analysis/create_table.sql"
    )

    download = PythonOperator(
        task_id="download",
        python_callable = download_file
    )

    extract = PythonOperator(
        task_id="extract",
        python_callable = extract_file
    )

    process = PythonOperator(
        task_id="load",
        python_callable = process_and_load
    )

    analyze_data = SQLExecuteQueryOperator(
        task_id="analyze",
        conn_id="postgres_conn",
        sql="include/analysis/analysis.sql"
    )

    send_notification = EmailOperator(
        task_id = "email",
        to = "ufuoma.ejite@gmail.com",
        subject = "Wikipedia Pageviews Pipeline SUCCESSFUL {{ ds }}",
        html_content = "include/email_template.html",
        mime_subtype = "html",
        conn_id = "smtp_conn"
    )

    create_table >> download >> extract >> process >> analyze_data >> send_notification