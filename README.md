# Airflow MLOps Lab - Pipeline Machine Learning

📋 Description
Ce projet démontre l'industrialisation d'un pipeline ML avec Apache Airflow 3.1.0 pour automatiser le workflow complet d'un modèle de régression logistique sur le dataset advertising.csv (prédiction de conversions TV/radio/newspaper). Le pipeline orchestre 7 tâches critiques MLOps :​

load_data : Chargement dataset (Pandas, 200 samples).

preprocess_data : Nettoyage, scaling (MinMaxScaler), feature engineering.

separate_data : Split train/test (80/20, 160/40 samples).

build_model : Entraînement LogisticRegression (scikit-learn).

evaluate_model : Évaluation accuracy (XCom storage, typiquement 0.85+).

success_notification : Email SMTP (Gmail, alertes production).

call_api : Intégration Flask API (POST status sur port 5000, 200 OK confirmé).

Objectifs pédagogiques (basé sur énoncé Simplon Lille) :

Automatisation workflow ML (pas conception modèle).

Orchestration DAGs, monitoring, notifications, et intégrations externes.

MLOps production-ready : Traçabilité XCom, retries, health checks API v2.

Valeur MLOps : Pipeline reproductible, scalable (16 runs max), avec monitoring REST v2 et email alerts. Idéal pour formation Développeur IA/Data Analyse.​

🛠️ Stack Technique
Composant	Version	Rôle
Apache Airflow	3.1.0	Orchestration DAGs, scheduling (@daily), monitoring UI/API v2. ​
Docker & Docker Compose	20.x	Conteneurisation (webserver, scheduler, worker, postgres, flask). ​
Python	3.12.12	Scripts ML (scikit-learn, pandas), DAGs PythonOperator/BashOperator.
Scikit-learn	1.3+	Modèle LogisticRegression, preprocessing (train/test split, accuracy).
Flask	3.1.3	API supervision (port 5000, endpoints /api/v1/update-status, /api/v1/status).
PostgreSQL	16	Métadonnées (DAG runs, task instances, XCom accuracy), volumes persistants.
SMTP Provider	apache-airflow-providers-smtp	Notifications email (Gmail config). ​
Dépendances : pandas, numpy, joblib (sauvegarde modèle .pkl), requests (call_api).

Projet : Lab MLOps - Industrialisation pipeline ML avec Airflow.

 Installation & Démarrage
Prérequis
Docker : docker --version (20.x+ requis).

Docker Compose : docker compose version (v2+).

Git : Clone repo : git clone <ton-repo> && cd airflow-mlops-lab.

Python : 3.12 (pour dev local, optionnel).

Variables d'environnement : Crée .env avec SMTP Gmail (email/password/app-password).​

Fichier .env exemple (non commité) :



bash
git clone <repo> && cd airflow-mlops-lab
cp .env.example .env  # Édite avec tes credentials Gmail
Build & Démarrage Docker :

bash
docker compose up -d  # Démarre 7 services (webserver:8080, postgres:5432, flask:5000)
docker compose ps     # Vérifie : tous "Up" (healthy)
Initialisation Airflow (première fois) :

bash
docker compose exec airflow-worker airflow db init  # Crée tables PostgreSQL
docker compose exec airflow-worker airflow db upgrade  # Migrations 3.1.0
docker compose exec airflow-worker airflow users create \
  --username admin --firstname Admin --lastname User --role Admin \
  --email admin@example.com --password admin  # User admin/admin
Accès :


API v2 Health : curl http://localhost:8080/api/v2/monitor/health (tous "healthy").​

Flask API : curl http://localhost:5000/api/v1/status ({} ou status pipeline).

Swagger : Pas supporté en 3.1.0 (utilise API v2 endpoints directs).​

Vérification Pipeline :

UI : Active ml_pipeline_lab, trigger manual.

Logs : docker logs airflow-worker --tail 20 | grep "ml_pipeline_lab" (success 7/7 tâches).

Modèle : /opt/airflow/dags/ml_pipeline/model/logistic_regression_model.pkl (sauvegardé).

Temps estimé : 5-10 min (première fois), 1 min (redémarrage).

📖 Utilisation
Exécution Pipeline ML
UI Airflow (recommandé) :

Navigue : localhost:8080 → DAGs → ml_pipeline_lab.

Toggle "On", clique "Trigger DAG" (manual).

Graph View : Visualise 7 tâches (load_data → call_api).

Grid : Monitor status (toutes vertes après 634s).​

CLI Airflow :

bash
docker compose exec airflow-worker airflow dags list  # Liste DAGs (ml_pipeline_lab)
docker compose exec airflow-worker airflow dags trigger ml_pipeline_lab  # Trigger
docker compose exec airflow-worker airflow dags state ml_pipeline_lab manual__$(date +%Y-%m-%dT%H:%M:%S)  # Status
Monitoring :

XCom Metrics : UI → evaluate_model → XCom (accuracy ~0.85).

Logs Tâches : UI → call_api → Logs (recherche "API Flask appelée : 200").

Email : Vérifie inbox Gmail (notification success).

API Flask : docker logs flask-api --tail 10 (POST reçu de call_api).

Planification :

Schedule : @daily (0 0 * * *).

Backfill : airflow dags backfill ml_pipeline_lab --start-date 2025-10-01.​

Exemple Sortie Pipeline
Dataset : 200 rows (TV, radio, newspaper → conversion 0/1).

Modèle : LogisticRegression, accuracy stockée XCom.

Artefacts : model/logistic_regression_model.pkl (joblib), data/preprocessed_advertising.csv.

Intégration : POST vers Flask API : {"dag_id": "ml_pipeline_lab", "status": "success"} (200 OK).

🏗️ Structure du Projet
text
airflow-mlops-lab/
├── dags/
│   ├── ml_airflow_lab.py          # DAG principal (7 tâches PythonOperator/BashOperator)
│   └── model_development.py       # Modèle ML source (LogisticRegression)
├── data/
│   └── advertising.csv            # Dataset input (200 samples)
├── model/
│   └── logistic_regression_model.pkl  # Modèle entraîné (output)
├── api/
│   └── app.py                     # Flask API (endpoints /api/v1/*)
├── docker-compose.yaml            # Services (airflow, postgres, flask)
├── .env.example                   # Config SMTP, DB (non commité)
├── requirements.txt               # Dépendances Python (scikit-learn, etc.)
└── README.md                      # Ce fichier
Volumes Docker (persistants) :

./dags:/opt/airflow/dags (code DAGs).

./logs:/opt/airflow/logs (logs tâches).

postgres_db_volume:/var/lib/postgresql/data (métadonnées XCom).

🔧 Commandes Utilitaires (Cheatsheet Intégré)
Lancement & Services Airflow
Commande	Description	Vérification
docker compose up -d	Démarre tout (, scheduler, flask:5000). ​	docker ps (7 conteneurs Up).
docker compose down	Arrête services (garde volumes).	docker compose ps (0 actifs).
airflow webserver --port 8080	Lance UI (standalone, non-Docker). ​	http://localhost:8080 (dashboard).
airflow scheduler	Lance orchestration DAGs.	ps aux | grep scheduler (PID > 0).
airflow db init	Initialise DB PostgreSQL.	airflow db check (healthy).
Logs & Monitoring
Commande	Description	Exemple Sortie
docker logs -f airflow-worker-1	Logs worker temps réel (tâches ML). ​	"Starting load_data task", "Accuracy: 0.85".
docker logs --tail 100 airflow-scheduler-1	Derniers logs scheduler (exécutions).	"DAG ml_pipeline_lab triggered".
docker logs -f flask-api-1	Logs API Flask (POST call_api).	POST /api/v1/update-status 200.
curl http://localhost:8080/api/v2/monitor/health	Health API v2 (tous healthy). ​	{"metadatabase":"healthy", "scheduler":"healthy"}.
docker compose restart airflow-scheduler	Relance scheduler (après edit DAG).	docker logs scheduler --tail 10 (redémarré).
Nginx (Proxy Optionnel)
Commande	Description	Vérification
sudo nginx -s reload	Recharge config reverse proxy. ​	ps aux | grep nginx (PID actif).
sudo nginx -t	Test config nginx.	nginx: configuration ok.
sudo systemctl status nginx	Statut service (systemd).	nginx.service: active (running).
Gestion Utilisateurs & DB
User Admin : admin / admin (ou tes creds : "admin": "geXFHK5pRahNywfE").​

DB Shell : docker compose exec postgres psql -U airflow -d airflow (\dt xcom pour metrics).

Nettoyage : docker volume prune (volumes orphelins), docker system prune -f (images inutiles).

Debugging Pipeline
DAG Status : UI → Grid (toutes tâches success/vertes).

XCom Inspect : UI → evaluate_model → XCom (clé accuracy, valeur float).

Email Test : docker compose exec airflow-worker airflow tasks test ml_pipeline_lab success_notification 2025-10-26.

API Test : curl -X POST http://localhost:5000/api/v1/update-status -d '{"status":"success"}' -H "Content-Type: application/json".


Logs Généraux : docker compose logs -f (tous services temps réel).
Erreurs Courantes : Vérifie docker-compose.yaml (ports, env vars), airflow.cfg (providers smtp installés).


👤 Auteur
Bafode Jaiteh
