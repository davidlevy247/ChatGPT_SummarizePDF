#!/bin/bash
set -e

cd "$(dirname "$0")"

# Check if the virtual environment folder exists, if not create it
if [ ! -d "SummarizePDF" ]; then
    python3 -m venv SummarizePDF
fi

# Activate the virtual environment and install required packages
source ./SummarizePDF/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
deactivate

# Activate the virtual environment and run the script
source ./SummarizePDF/bin/activate
python3 pdf_summarizer.py
deactivate
