@echo off
REM — Run server in background (same window), then start client after a delay

echo ==============================================
echo Launching Live-Translator Server...
echo ==============================================
start /B python server\main.py

echo.
echo Server started.
echo.
echo Waiting 2 seconds before starting client...
timeout /t 2 /nobreak > nul

echo ==============================================
echo Launching Live-Translator Client...
echo ==============================================
python client\main.py

echo.
echo Both processes are now running.
pause
