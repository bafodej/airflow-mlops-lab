from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

dag_status = {}

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """Statut du pipeline - simple stockage mémoire"""
    dag_id = request.args.get('dag_id', 'ml_pipeline_lab')
    status_data = dag_status.get(dag_id, {})
    return jsonify(status_data)

@app.route('/api/v1/update-status', methods=['POST'])
def update_status():
    """Met à jour le statut depuis Airflow"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'})
        dag_id = data.get('dag_id')
        status = data.get('status', 'unknown')
        
        dag_status[dag_id] = {
            'status': status,
            'run_id': data.get('run_id', 'unknown'),
            'accuracy': data.get('accuracy', None),
            'updated': datetime.now().isoformat()
        }
        
        print(f"API Flask - Statut {status} pour {dag_id}")
        return jsonify({
            'status': 'updated',
            'dag_id': dag_id,
            'accuracy': data.get('accuracy', None)
        })
        
    except Exception as e:
        print(f"Erreur API Flask: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/v1/dag-status/<dag_id>', methods=['GET'])
def get_dag_status(dag_id):
    """Endpoint Airflow REST (optionnel, peut rester)"""
    try:
        import requests
        airflow_url = 'http://airflow-apiserver:8080'
        api_url = f"{airflow_url}/api/v1/dags/{dag_id}/dagRuns"
        
        response = requests.get(api_url, params={'limit': 1})
        if response.status_code == 200:
            dag_runs = response.json()
            if dag_runs['dag_runs']:
                latest_run = dag_runs['dag_runs'][0]
                return jsonify(latest_run)
                
        return jsonify({
            'dag_id': dag_id,
            'status': 'error',
            'message': f'API Airflow indisponible: {response.status_code}'
        })
    except Exception as e:
        return jsonify({
            'dag_id': dag_id,
            'status': 'error',
            'message': f'Erreur API: {str(e)}'
        })

@app.route('/api/v1/status', methods=['GET'])
def get_status_main():
    """Endpoint principal - statut par défaut"""
    dag_id = request.args.get('dag_id', 'ml_pipeline_lab')
    return get_dag_status(dag_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
