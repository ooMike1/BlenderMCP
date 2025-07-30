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
echo Step 3: MCP Configuration...
echo.
echo Please configure your MCP client to use this server.
echo Server location: %CD%
echo.
echo Refer to your MCP client documentation for configuration instructions.

echo.
echo Step 4: Installation complete!
echo.
echo Next steps:
echo.
echo For Claude Desktop users:
echo   Run install_to_claude.bat to automatically configure Claude
echo.
echo For other MCP clients:
echo   1. Configure your MCP client to use this server
echo   2. Server location: %CD%
echo   3. Restart your MCP client
echo   4. Test with: "Create a red cube in Blender"
echo.
echo See setup_instructions.md for detailed setup guide.
echo.
pause