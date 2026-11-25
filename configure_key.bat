@echo off
cd /d "%~dp0"

echo CampusResolve AI - Gemini API Configuration

python -c "from pathlib import Path; from getpass import getpass; key=getpass('Enter your Gemini API key: ').strip(); assert key, 'API key cannot be empty'; Path('.gemini_key').write_text(key, encoding='utf-8')"

if errorlevel 1 (
    echo API key configuration failed.
) else (
    echo API key configured successfully.
)

pause