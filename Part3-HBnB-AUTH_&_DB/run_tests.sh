#!/bin/bash

# Set test environment
source setup_test.sh

# Run linting
flake8 models api tests

# Run tests with coverage
pytest tests/ -v --cov=models --cov=api --cov-report=html

# Run integration tests
python -m unittest tests/test_api/test_v1/test_integration.py -v

# Cleanup
source teardown_test.sh

# Define MySQL environment variables
export HBNB_MYSQL_USER=hbnb_dev
export HBNB_MYSQL_PWD=hbnb_dev_pwd
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=hbnb_dev_db
export HBNB_ENV=test

# Run the tests
python3 -m unittest discover tests