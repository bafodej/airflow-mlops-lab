from airflow import DAG
from airflow.providers.smtp.operators.smtp import EmailOperator
from datetime import datetime

dag = DAG(
    dag_id='test_email_direct',
    start_date=datetime(2025, 10, 24),
    schedule=None,
    catchup=False
)

email_task = EmailOperator(
    task_id='test_email',
    to='bafodejaiteh2@gmail.com',
    subject='Test Email Direct Airflow',
    html_content='<p>Test simple email SMTP</p>',
    conn_id='smtp_gmail',
    dag=dag
)
