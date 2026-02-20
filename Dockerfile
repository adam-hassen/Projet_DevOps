# Utiliser Python 3.12-slim (plus récent et avec moins de vulnérabilités)
FROM python:3.12-slim-bookworm

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Mettre à jour les paquets système et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Créer le dossier pour les exports Excel
RUN mkdir -p /app/exports && \
    chmod 777 /app/exports

# Copier tout le projet
COPY . .

# Exposer le port
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app.py"]