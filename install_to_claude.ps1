# BlenderMCP Claude Installer for PowerShell

Write-Host "========================================"
Write-Host "BlenderMCP Claude Installer" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host ""

# Get the absolute path of the BlenderMCP directory
$BlenderMCPPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$ParentDir = Split-Path -Parent $BlenderMCPPath
$MCPConfigPath = Join-Path $ParentDir ".mcp.json"

Write-Host "Installing BlenderMCP for Claude..."
Write-Host ""
Write-Host "Installation directory: $BlenderMCPPath" -ForegroundColor Yellow
Write-Host "Configuration file: $MCPConfigPath" -ForegroundColor Yellow
Write-Host ""

# Step 1: Install Python dependencies
Write-Host "Step 1: Installing Python dependencies..." -ForegroundColor Green
Set-Location $BlenderMCPPath
$pipResult = & pip install -r requirements.txt 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "Please ensure Python and pip are installed and accessible"
    Write-Host $pipResult
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Dependencies installed successfully!" -ForegroundColor Green

# Step 2: Create or update .mcp.json
Write-Host ""
Write-Host "Step 2: Configuring Claude MCP settings..." -ForegroundColor Green

# Check if .mcp.json exists
$config = @{ mcpServers = @{} }
$updateConfig = $true

if (Test-Path $MCPConfigPath) {
    Write-Host "Found existing .mcp.json, creating backup..."
    Copy-Item $MCPConfigPath "$MCPConfigPath.backup" -Force
    
    try {
        $existingConfig = Get-Content $MCPConfigPath -Raw | ConvertFrom-Json
        $config = $existingConfig
        
        if ($existingConfig.mcpServers.blender) {
            Write-Host "BlenderMCP is already configured in .mcp.json" -ForegroundColor Yellow
            Write-Host ""
            $response = Read-Host "Do you want to update the configuration? (Y/N)"
            if ($response -ne 'Y' -and $response -ne 'y') {
                Write-Host "Skipping configuration update."
                $updateConfig = $false
            }
        }
    }
    catch {
        Write-Host "WARNING: Could not parse existing .mcp.json, will create new one" -ForegroundColor Yellow
    }
}

if ($updateConfig) {
    # Add or update BlenderMCP configuration
    $config.mcpServers["blender"] = @{
        command = "python"
        args = @(Join-Path $BlenderMCPPath "main.py")
        env = @{
            PYTHONPATH = $BlenderMCPPath
        }
    }
    
    # Write updated config
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content $MCPConfigPath -Encoding UTF8
        Write-Host "Configuration updated successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: Failed to update configuration" -ForegroundColor Red
        Write-Host $_.Exception.Message
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Step 3: Test server startup
Write-Host ""
Write-Host "Step 3: Testing server startup..." -ForegroundColor Green
Start-Sleep -Seconds 2

$testResult = & python (Join-Path $BlenderMCPPath "main.py") --test 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Server test had issues. Check Blender installation." -ForegroundColor Yellow
    Write-Host "The server may still work if Blender is properly installed."
} else {
    Write-Host "Server test passed!" -ForegroundColor Green
}

# Step 4: Display success message
Write-Host ""
Write-Host "========================================"
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================"
Write-Host ""
Write-Host "BlenderMCP has been successfully configured for Claude."
Write-Host ""
Write-Host "Configuration file: $MCPConfigPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Restart Claude Desktop"
Write-Host "2. Look for 'blender' in the available MCP servers"
Write-Host "3. Test with commands like: 'Create a red cube in Blender'"
Write-Host ""
Write-Host "For more information, see:"
Write-Host "- setup_instructions.md"
Write-Host "- README.md"
Write-Host ""
Read-Host "Press Enter to exit"