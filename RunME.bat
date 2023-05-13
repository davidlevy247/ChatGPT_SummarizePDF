@echo on
cd /d %~dp0

REM Check if the virtual environment folder exists, if not create it and install required packages
if not exist "SummarizePDF" (
    python -m venv SummarizePDF
    call .\SummarizePDF\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install PyPDF2 openai
    call .\SummarizePDF\Scripts\deactivate.bat
)

call .\SummarizePDF\Scripts\activate.bat
python pdf_summarizer.py
call .\SummarizePDF\Scripts\deactivate.bat
