#!/bin/bash

# Remove existing virtual environment
if [ -d "venv" ]; then
    rm -rf venv
fi

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
