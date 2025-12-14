# Airflow MLOps Lab - Pipeline Machine Learning

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Airflow 3.1.0](https://img.shields.io/badge/Airflow-3.1.0-orange)](https://airflow.apache.org)
[![Docker](https://img.shields.io/badge/Docker-20.x-green)](https://docker.com)

## 📋 Description
Industrialisation d'un pipeline ML avec Apache Airflow 3.1.0 : automatisation d'un modèle de régression logistique sur `advertising.csv` (prédiction conversions TV/radio/newspaper, 200 échantillons). 7 tâches MLOps orchestrées :

- `load_data` : Chargement Pandas.
- `preprocess_data` : Nettoyage, MinMaxScaler, features.
- `separate_data` : Split 80/20.
- `build_model` : Entraînement LogisticRegression (scikit-learn).
- `evaluate_model` : Accuracy ~0.85 (XCom).
- `success_notification` : Email SMTP Gmail.
- `call_api` : POST Flask API (port 5000, 200 OK).

**Valeur** : Automatisation workflow , monitoring UI/API v2, traçabilité XCom/retries, scalable (16 runs). Idéal pour MLOps production-ready en formation IA/Data.

## 🛠️ Stack

| Outil            | Version | Rôle |
|------------------|---------|------|
| Airflow         | 3.1.0  | DAGs, scheduling @daily, UI/API v2. |
| Docker Compose  | 20.x   | Conteneurs (webserver, scheduler, Postgres, Flask). |
| Python          | 3.12   | Scripts ML/Pandas, operators. |
| Scikit-learn    | 1.3+   | Modèle, preprocessing. |
| Flask           | 3.1.3  | API /api/v1/status. |
| PostgreSQL      | 16     | Métadonnées XCom. |
| SMTP            | -      | Notifications Gmail. |

Dépendances : `pandas`, `numpy`, `joblib`, `requests`. Voir `requirements.txt`.

## 🚀 Installation & Démarrage
### Prérequis
- Docker 20.x+ / Compose v2+.
- Git : `git clone https://github.com/bafodej/airflow-mlops-lab && cd airflow-mlops-lab`.
- `.env` : Copiez `.env.example`, ajoutez Gmail SMTP (email/app-password).

### Lancement
docker compose up -d # 7 services : webserver:8080, Flask:5000
docker compose ps # Tous "Up"

text

### Init Airflow (1re fois)
docker compose exec airflow-worker airflow db init
docker compose exec airflow-worker airflow db upgrade
docker compose exec airflow-worker airflow users create --username admin --email admin@example.com --password admin # Accès : admin/admin

text

### Vérif
- Health : `curl localhost:8080/api/v2/monitor/health`.
- API : `curl localhost:5000/api/v1/status`.
- Pipeline : UI:8080 → `ml_pipeline_lab` → Trigger. Logs : `docker logs airflow-worker | grep ml_pipeline_lab` (7/7 success). Modèle : `model/logistic_regression_model.pkl`.

Temps : 5 min premier, 1 min relance.

## 📖 Utilisation
- **UI** : localhost:8080 → DAGs → `ml_pipeline_lab` → On/Trigger. Graph : Tâches ; Grid : Vert ~10 min.
- **CLI** : `docker compose exec airflow-worker airflow dags trigger ml_pipeline_lab`.
- Monitoring : XCom accuracy (UI), email Gmail, logs Flask POST.
- Schedule : @daily ; Backfill : `--start-date 2025-10-01`.

**Sortie** : Artefacts `.pkl`/CSV ; Intégration API success.


text
Volumes : dags/logs persistants, Postgres data.

## 🔧 Commandes Rapides
- Down : `docker compose down`.
- Logs : `docker compose logs -f`.
- Test Email/API : Voir code pour tâches test.
- Erreurs : Check ports/env, SMTP providers.

## 👤 Auteur
Bafode Jaiteh – Formation Développeur IA/Data Simplon Lille. [GitHub](https://github.com/bafodej) | [LinkedIn](https://linkedin.com/in/bafodejaiteh).
