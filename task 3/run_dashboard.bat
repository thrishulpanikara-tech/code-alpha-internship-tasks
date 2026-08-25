@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo   Books Analytics Dashboard
echo ========================================
echo.
echo Starting... Your browser will open automatically.
echo If not, open: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard.
echo.
python -m streamlit run 04_dashboard.py
pause
