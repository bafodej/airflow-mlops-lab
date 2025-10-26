FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances Flask
RUN pip install flask requests

# Copie de l'API Flask
COPY api/flask_api.py /app/flask_api.py

# Expose le port 5000
EXPOSE 5000

# Commande de démarrage
CMD ["python", "flask_api.py"]
