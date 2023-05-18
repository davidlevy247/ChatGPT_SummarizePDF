#!/bin/bash

# Navigate to the directory of the script
cd "$(dirname "$0")"

# Check if the virtual environment folder exists, if not create it and install required packages
if [ ! -d "SummarizePDF" ]; then
    python3 -m venv SummarizePDF
    source SummarizePDF/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install PyPDF2 openai cryptography
    deactivate
fi

source SummarizePDF/bin/activate
python3 pdf_summarizer.py
deactivate
