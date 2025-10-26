from airflow import DAG
from airflow.providers.smtp.operators.smtp import EmailOperator 
from datetime import datetime

dag = DAG(
    dag_id='test_email_final',
    start_date=datetime(2025, 10, 24),
    schedule=None,
    catchup=False
)

# Email ultra-simple, sans HTML complexe
test_email = EmailOperator(
    task_id='success_notification',
    to='bafodejaiteh2@gmail.com',
    subject='Pipeline ML terminée avec succès',
    html_content='Ton contenu HTML ici',
    conn_id='smtp_gmail',  # Ta connexion existante
    dag=dag
)

test_email
