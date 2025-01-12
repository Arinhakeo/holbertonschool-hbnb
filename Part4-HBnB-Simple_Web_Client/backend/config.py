#!/usr/bin/python3
# backend/config.py
import os

# Configuration de base de données
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://votre_utilisateur:votre_mot_de_passe@localhost/votre_base_de_donnees')

# Autres configurations si nécessaire
SECRET_KEY = os.getenv('SECRET_KEY', 'votre_clé_secrète')