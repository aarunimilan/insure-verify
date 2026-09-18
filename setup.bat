@echo off
echo ========================================
echo       DentalVerify Setup
echo ========================================
echo.

if not exist venv (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Virtual environment already exists.
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [4/4] Creating database...
python -m backend.init_db
if errorlevel 1 (
    echo Failed to initialize database.
    pause
    exit /b 1
)

echo.
echo ========================================
echo       Setup completed successfully!
echo ========================================
echo.
echo Setup is complete.
echo.
echo To start DentalVerify:
echo     venv\Scripts\activate
echo     uvicorn backend.main:app --reload
echo.
pause