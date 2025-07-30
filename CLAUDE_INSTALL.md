# BlenderMCP Claude Desktop Installation Guide

This guide helps you install BlenderMCP for use with Claude Desktop.

## Quick Installation

### Option 1: Batch Script (Recommended)
1. Run `install_to_claude.bat`
2. Restart Claude Desktop
3. You're ready to use BlenderMCP!

### Option 2: PowerShell Script
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Run: `.\install_to_claude.ps1`
4. Restart Claude Desktop

## What the Installer Does

1. **Installs Python dependencies** - All required packages for BlenderMCP
2. **Creates/Updates .mcp.json** - Adds BlenderMCP configuration to your project
3. **Tests the server** - Verifies basic functionality
4. **Backs up existing config** - If you already have .mcp.json, it creates a backup

## Configuration Details

The installer adds this configuration to `.mcp.json`:

```json
{
  "mcpServers": {
    "blender": {
      "command": "python",
      "args": ["C:\\path\\to\\BlenderMCP\\main.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\BlenderMCP"
      }
    }
  }
}
```

## Verifying Installation

After restarting Claude Desktop:

1. Check if BlenderMCP appears in available MCP servers
2. Try a simple command: "Create a red cube in Blender"
3. Check the logs if you encounter issues

## Troubleshooting

### Python/pip not found
- Ensure Python 3.8+ is installed and in PATH
- Try running `python --version` and `pip --version`

### Blender not found
- Install Blender from https://www.blender.org/
- The installer will try to find Blender automatically
- You can set a custom path in `config.json`

### Server test fails
- This is often OK if Blender isn't in PATH
- The server may still work correctly
- Check `setup_instructions.md` for manual configuration

### Permission errors
- Run the installer as Administrator
- Or use the PowerShell script with appropriate permissions

## Manual Installation

If the automated installer doesn't work:

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.mcp.json` in your project root
3. Add the configuration shown above
4. Update paths to match your system
5. Restart Claude Desktop

## Support

- See `README.md` for general information
- See `setup_instructions.md` for detailed setup
- Check logs in Claude Desktop for debugging