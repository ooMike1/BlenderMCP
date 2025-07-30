# Blender MCP Server Setup Instructions

## Prerequisites

1. **Python 3.8+** installed and accessible via `python` command
2. **Blender 3.6+** installed and accessible (will auto-detect common locations)
3. **MCP-compatible client** installed

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MCP Client

Add the server to your MCP client's configuration (see `mcp_config_example.json`):

```json
{
  "mcpServers": {
    "blender": {
      "command": "python", 
      "args": ["path/to/BlenderMCP/main.py"]
    }
  }
}
```

### 3. Verify Installation

Restart your MCP client and test with:
```
"Create a cube"
```

## Troubleshooting

### Common Issues:

**"Blender executable not found"**
- Ensure Blender is installed
- Modify `blender_integration.py` to specify custom Blender path if needed

**"Module not found" errors**
- Ensure all Python dependencies are installed: `pip install -r requirements.txt`
- Check that PYTHONPATH is set correctly in the configuration

**"Permission denied" errors**
- Ensure the Python script has execution permissions
- Check that the file paths in the configuration are correct

**Server timeout**
- Complex operations may need longer timeout
- Check Blender installation and ensure it can run in background mode

### Custom Blender Path

If Blender is not in a standard location, modify `blender_integration.py` to specify custom path.

## Support

For issues:
1. Check console output for errors
2. Ensure Blender runs from command line: `blender --version`
3. Verify file paths in configuration