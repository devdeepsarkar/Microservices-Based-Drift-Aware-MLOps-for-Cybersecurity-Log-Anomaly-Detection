@echo off
echo Activating virtual environment...
call venv\Scripts\activate

echo Starting FastAPI Prediction Service (port 8000)...
start "Prediction Service" cmd /k "cd /d %~dp0prediction_service && python app.py"

echo Waiting for prediction service to start...
timeout /t 3 /nobreak > nul

echo Starting Drift Detection Service (port 8001)...
start "Drift Service" cmd /k "cd /d %~dp0drift_service && python app.py"

echo Starting Streamlit Frontend (port 8501)...
start "Dashboard" cmd /k "cd /d %~dp0 && streamlit run frontend/app.py"

echo.
echo All services are running!
echo   Prediction Service : http://localhost:8000
echo   Drift Service      : http://localhost:8001
echo   Dashboard          : http://localhost:8501
echo.
echo Three new windows have opened for each service.
echo Close those windows individually to stop each service.
echo.
pause
