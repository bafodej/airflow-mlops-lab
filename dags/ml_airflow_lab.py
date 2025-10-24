from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.smtp.operators.smtp import EmailOperator

import sys
sys.path.insert(0, '/opt/airflow/dags/ml_pipeline/src')

from model_development import (
    load_data,
    preprocess_data,
    separate_data,
    build_model,
    evaluate_model
)
import pandas as pd
import numpy as np

# Arguments par défaut
default_args = {
    'owner': 'bafode',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 22),
    'email': ['bafode@example.com'],  # Remplace par ton email
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Fonctions wrapper pour XCom
def task_load_data(**context):
    """Charge les données"""
    df = load_data()
    context['ti'].xcom_push(key='dataframe', value=df.to_json())
    return "Data loaded successfully"

def task_preprocess_data(**context):
    """Prétraite les données"""
    df_json = context['ti'].xcom_pull(key='dataframe', task_ids='load_data')
    df = pd.read_json(df_json)
    X, y = preprocess_data(df)
    
    context['ti'].xcom_push(key='X', value=X.to_json())
    context['ti'].xcom_push(key='y', value=y.tolist())
    return "Data preprocessed successfully"

def task_separate_data(**context):
    """Sépare train/test"""
    X_json = context['ti'].xcom_pull(key='X', task_ids='preprocess_data')
    y_list = context['ti'].xcom_pull(key='y', task_ids='preprocess_data')
    
    X = pd.read_json(X_json)
    y = pd.Series(y_list)
    
    X_train, X_test, y_train, y_test = separate_data(X, y)
    
    context['ti'].xcom_push(key='X_train', value=X_train.tolist())
    context['ti'].xcom_push(key='y_train', value=y_train.tolist())
    context['ti'].xcom_push(key='X_test', value=X_test.tolist())
    context['ti'].xcom_push(key='y_test', value=y_test.tolist())
    
    return "Data separated successfully"

def task_build_model(**context):
    """Entraîne le modèle"""
    X_train = np.array(context['ti'].xcom_pull(key='X_train', task_ids='separate_data'))
    y_train = np.array(context['ti'].xcom_pull(key='y_train', task_ids='separate_data'))
    
    model = build_model(X_train, y_train)
    return "Model built and saved successfully"

def task_evaluate_model(**context):
    """Évalue le modèle"""
    X_test = np.array(context['ti'].xcom_pull(key='X_test', task_ids='separate_data'))
    y_test = np.array(context['ti'].xcom_pull(key='y_test', task_ids='separate_data'))
    
    import joblib
    from pathlib import Path
    
    model_path = Path('/opt/airflow/dags/ml_pipeline/model/logistic_regression_model.pkl')
    model = joblib.load(model_path)
    
    accuracy = evaluate_model(model, X_test, y_test)
    context['ti'].xcom_push(key='accuracy', value=float(accuracy))
    
    return f"Model evaluated. Accuracy: {accuracy:.4f}"

# Définition du DAG
with DAG(
    'ml_pipeline_lab',
    default_args=default_args,
    description='Pipeline ML automatisé avec Airflow',
    schedule='@daily',
    catchup=False,
    tags=['ml', 'pipeline', 'production'],
) as dag:

    # Tâche 1 : Chargement des données
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=task_load_data,
    )

    # Tâche 2 : Prétraitement
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=task_preprocess_data,
    )

    # Tâche 3 : Séparation train/test
    separate_data_task = PythonOperator(
        task_id='separate_data',
        python_callable=task_separate_data,
    )

    # Tâche 4 : Entraînement du modèle
    build_model_task = PythonOperator(
        task_id='build_model',
        python_callable=task_build_model,
    )

    # Tâche 5 : Évaluation
    evaluate_model_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=task_evaluate_model,
    )

    # Tâche 6 : Notification succès
    success_notification = BashOperator(
        task_id='success_notification',
        bash_command='echo "Pipeline ML completed successfully!"',
    )

    # Définir les dépendances
    load_data_task >> preprocess_data_task >> separate_data_task >> build_model_task >> evaluate_model_task >> success_notification

