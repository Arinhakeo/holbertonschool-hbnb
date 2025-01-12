#!/bin/bash

# Couleurs pour les logs
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Pas de couleur

echo -e "${GREEN}=== Configuration de l'environnement virtuel ===${NC}"

# Vérification et activation de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo -e "${RED}[INFO] venv non détecté. Création d'un environnement virtuel...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
echo -e "${GREEN}[INFO] Environnement virtuel activé.${NC}"

# Installation des modules nécessaires
echo -e "${GREEN}=== Installation des dépendances ===${NC}"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERREUR] Problème lors de l'installation des dépendances. Vérifiez votre requirements.txt.${NC}"
    exit 1
fi

# Vérification des modules critiques
modules=("flask" "python-dotenv" "sqlalchemy" "flask-cors")
for module in "${modules[@]}"; do
    pip show $module > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERREUR] Le module $module n'est pas installé.${NC}"
        echo -e "${RED}[ACTION] Installation manuelle de $module...${NC}"
        pip install $module
    fi
done

# Vérification de dotenv
if [ ! -f "../.env" ]; then
    echo -e "${RED}[INFO] Fichier .env introuvable. Création d'un fichier .env par défaut.${NC}"
    cat <<EOT > ../.env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///hbnb_dev.db
EOT
    echo -e "${GREEN}[INFO] Fichier .env créé avec succès.${NC}"
else
    echo -e "${GREEN}[INFO] Fichier .env détecté.${NC}"
fi

# Lancer le serveur Flask
echo -e "${GREEN}=== Lancement du serveur Flask ===${NC}"
cd backend
python3 app.py

# Fin du script
deactivate
echo -e "${GREEN}=== Fin de l'exécution du script ===${NC}"
