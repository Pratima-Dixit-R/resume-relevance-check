@echo off
title Resume Relevance Checker - Innomatics Research Labs

echo ========================================
echo Resume Relevance Checker
echo Innomatics Research Labs
echo ========================================

echo.
echo 🚀 Starting deployment...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Launch the unified deployment script
python deploy_unified.py

echo.
echo 🛑 Application stopped
echo.
pause