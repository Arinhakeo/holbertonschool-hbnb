#!/bin/bash

# Supprimer les __pycache__ et fichiers .pyc
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -exec rm -f {} +

# Supprimer le répertoire htmlcov s'il existe
if [ -d "htmlcov" ]; then
    rm -r htmlcov
fi

# Supprimer le fichier de log
if [ -f "logg.txt" ]; then
    rm logg.txt
fi

# Supprimer le répertoire tests_backup s'il existe
if [ -d "tests_backup" ]; then
    rm -r tests_backup
fi

# Supprimer les fichiers non nécessaires
rm -f create_test_script.sh
rm -f setup_test.sh
rm -f teardown_test.sh

echo "Nettoyage terminé !"