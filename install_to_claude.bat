@echo off
setlocal enabledelayedexpansion

echo ========================================
echo BlenderMCP Claude Installer
echo ========================================
echo.

:: Get the absolute path of the BlenderMCP directory
set "BLENDER_MCP_PATH=%~dp0"
:: Remove trailing backslash
set "BLENDER_MCP_PATH=%BLENDER_MCP_PATH:~0,-1%"

:: Get the parent directory (where .mcp.json should be)
for %%i in ("%BLENDER_MCP_PATH%") do set "PARENT_DIR=%%~dpi"
set "PARENT_DIR=%PARENT_DIR:~0,-1%"
set "MCP_CONFIG_PATH=%PARENT_DIR%\.mcp.json"

echo Installing BlenderMCP for Claude...
echo.
echo Installation directory: %BLENDER_MCP_PATH%
echo Configuration file: %MCP_CONFIG_PATH%
echo.

:: Step 1: Install Python dependencies
echo Step 1: Installing Python dependencies...
cd /d "%BLENDER_MCP_PATH%"
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    echo Please ensure Python and pip are installed and accessible
    pause
    exit /b 1
)

:: Step 2: Create or update .mcp.json
echo.
echo Step 2: Configuring Claude MCP settings...

:: Check if .mcp.json exists
if exist "%MCP_CONFIG_PATH%" (
    echo Found existing .mcp.json, creating backup...
    copy "%MCP_CONFIG_PATH%" "%MCP_CONFIG_PATH%.backup" >nul
    
    :: Read existing content and check if it already has BlenderMCP
    powershell -Command "if ((Get-Content '%MCP_CONFIG_PATH%' -Raw | ConvertFrom-Json).mcpServers.blender) { exit 1 } else { exit 0 }"
    if !errorlevel! equ 1 (
        echo BlenderMCP is already configured in .mcp.json
        echo.
        echo Do you want to update the configuration? (Y/N)
        set /p UPDATE_CONFIG=
        if /i "!UPDATE_CONFIG!" neq "Y" (
            echo Skipping configuration update.
            goto :test_server
        )
    )
)

:: Create Python script to update JSON
echo Creating configuration updater...
(
echo import json
echo import os
echo 
echo config_path = r"%MCP_CONFIG_PATH%"
echo blender_mcp_path = r"%BLENDER_MCP_PATH%"
echo 
echo # Load existing config or create new one
echo if os.path.exists(config_path^):
echo     with open(config_path, 'r'^) as f:
echo         config = json.load(f^)
echo else:
echo     config = {"mcpServers": {}}
echo 
echo # Add or update BlenderMCP configuration
echo config["mcpServers"]["blender"] = {
echo     "command": "python",
echo     "args": [os.path.join(blender_mcp_path, "main.py"^)],
echo     "env": {
echo         "PYTHONPATH": blender_mcp_path
echo     }
echo }
echo 
echo # Write updated config
echo with open(config_path, 'w'^) as f:
echo     json.dump(config, f, indent=2^)
echo 
echo print("Configuration updated successfully!"^)
) > "%TEMP%\update_mcp_config.py"

python "%TEMP%\update_mcp_config.py"
if %errorlevel% neq 0 (
    echo ERROR: Failed to update configuration
    pause
    exit /b 1
)

del "%TEMP%\update_mcp_config.py"

:test_server
:: Step 3: Test server startup
echo.
echo Step 3: Testing server startup...
timeout /t 2 /nobreak >nul
python "%BLENDER_MCP_PATH%\main.py" --test 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Server test had issues. Check Blender installation.
    echo The server may still work if Blender is properly installed.
) else (
    echo Server test passed!
)

:: Step 4: Display success message
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo BlenderMCP has been successfully configured for Claude.
echo.
echo Configuration file: %MCP_CONFIG_PATH%
echo.
echo Next steps:
echo 1. Restart Claude Desktop
echo 2. Look for "blender" in the available MCP servers
echo 3. Test with commands like: "Create a red cube in Blender"
echo.
echo For more information, see:
echo - setup_instructions.md
echo - README.md
echo.
pause