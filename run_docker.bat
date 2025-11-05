@echo off
echo ========================================
echo Single-Cell Analysis Docker Setup
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    echo Steps:
    echo 1. Press Windows Key
    echo 2. Search for "Docker Desktop"
    echo 3. Click to open
    echo 4. Wait for it to start
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

echo Building Docker image...
docker-compose build sc-analysis

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [OK] Build successful!
echo.
echo Running analysis pipeline...
echo This will:
echo   1. Download PBMC 3k dataset
echo   2. Run quality control
echo   3. Perform clustering analysis
echo   4. Generate visualizations
echo   5. Create interactive HTML report
echo.
echo Expected runtime: 5-10 minutes
echo.

docker-compose up sc-analysis

echo.
echo ========================================
echo Analysis Complete!
echo ========================================
echo.
echo Results saved to: results\single_cell_analysis\
echo.
echo Opening interactive report...
start results\single_cell_analysis\interactive_report.html

echo.
pause
