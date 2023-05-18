@echo on
cd /d %~dp0

REM Check if the virtual environment folder exists, if not create it
if not exist "SummarizePDF" (
    python -m venv SummarizePDF
)

REM Activate the virtual environment and install required packages
call .\SummarizePDF\Scripts\activate.bat
call python -m pip install --upgrade pip
call python -m pip install -r requirements.txt
call .\SummarizePDF\Scripts\deactivate.bat

REM Activate the virtual environment and run the script
call .\SummarizePDF\Scripts\activate.bat
python pdf_summarizer.py
call .\SummarizePDF\Scripts\deactivate.bat
