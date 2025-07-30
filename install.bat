@echo off
echo Installing Blender MCP Server...
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    echo Please ensure Python and pip are installed and accessible
    pause
    exit /b 1
)

echo.
echo Step 2: Testing server startup...
timeout /t 2 /nobreak >nul
python main.py --test 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Server test had issues. Check Blender installation.
    echo The server may still work if Blender is properly installed.
) else (
    echo Server test passed!
)

echo.
echo Step 3: Adding to Claude MCP...
echo.

REM Get the current directory
set "CURRENT_DIR=%CD%"

echo Running: claude mcp add file:///%CURRENT_DIR:\=/%/
claude mcp add file:///%CURRENT_DIR:\=/%/

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Could not automatically add to Claude MCP.
    echo Please run manually:
    echo   claude mcp add file:///%CURRENT_DIR:\=/%/
    echo.
    echo Or add manually to your Claude config:
    echo   Location: %%APPDATA%%\Claude\claude_desktop_config.json
    echo   See claude_config_example.json for the configuration format
) else (
    echo Successfully added to Claude MCP!
)

echo.
echo Step 4: Installation complete!
echo.
echo Next steps:
echo 1. Restart Claude Desktop
echo 2. Test with: "Create a red cube in Blender"
echo.
echo See setup_instructions.md for detailed setup guide.
echo.
pause