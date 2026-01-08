# Import dependencies
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
import datetime

from dotenv import load_dotenv
load_dotenv()

COMPANIES = os.getenv('COMPANIES').split(",")


# Function to process and load data into Postgres
def process_and_load(**kwargs):
    """
    Process the text file, filter for companies, 
    and load into Postgres.
    """

    # Gotten from previous task.
    txt_path = kwargs['ti'].xcom_pull(key='txt_path', task_ids='extract')
    txt_filename = kwargs['ti'].xcom_pull(key='txt_filename', task_ids='extract')

    # Parse: pageviews-20251225-180000.txt as 2025-12-25 18:00:00
    txt_filename = os.path.basename(txt_filename)
    date_time_str = txt_filename[11:26]
    view_datetime = datetime.datetime.strptime(date_time_str, "%Y%m%d-%H%M%S")
    
    data = []  # List to hold filtered rows.
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()  # Split by spaces.
            if len(parts) == 4 and parts[0] == 'en':  # English desktop only.
                page_title = parts[1]
                if page_title in COMPANIES: # Check if page title matches any company.
                    views = int(parts[2])
                    data.append((page_title, views, view_datetime, parts[0]))
    
    if not data:
        raise ValueError("No data found for the companies.")
    
    # Use PostgresHook to connect and insert.
    hook = PostgresHook(postgres_conn_id='postgres_conn')  # The connection ID.
    #insert data into the table
    hook.insert_rows(
        table='pageviews',
        rows=data,
        target_fields=['company', 'views', 'view_datetime', 'project'],
        commit_every=1000 # Commit every 1000 rows
    )

    print(f"Inserted {len(data)} rows into the table.")