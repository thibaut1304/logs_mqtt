#!/bin/bash

set -e  # Exit on error

# Variables UID/GID
USER_UID=$(id -u)
USER_GID=$(id -g)

# .env path
ENV_FILE=".env"

# 🔄 Remplace ou ajoute UID/GID dans .env
update_env_var() {
  VAR_NAME="$1"
  VAR_VALUE="$2"
  if grep -q "^${VAR_NAME}=" "$ENV_FILE" 2>/dev/null; then
    sed -i "s|^${VAR_NAME}=.*|${VAR_NAME}=${VAR_VALUE}|" "$ENV_FILE"
  else
    echo "${VAR_NAME}=${VAR_VALUE}" >> "$ENV_FILE"
  fi
}

echo "📦 Mise à jour de .env avec UID=${USER_UID}, GID=${USER_GID}"
touch "$ENV_FILE"
update_env_var "UID" "$USER_UID"
update_env_var "GID" "$USER_GID"
update_env_var "TZ" "Europe/Paris"

# 📁 Création des dossiers logs/ et conf/
echo "📁 Création des dossiers logs/ et conf/"
mkdir -p logs conf
chown "$USER_UID:$USER_GID" logs conf

# ▶️ Lancer docker-compose
echo "🚀 Lancement de docker-compose..."
docker-compose down && docker-compose up --build -d
