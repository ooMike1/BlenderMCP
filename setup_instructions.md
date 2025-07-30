# Blender MCP Server Setup Instructions

## Prerequisites

1. **Python 3.8+** installed and accessible via `python` command
2. **Blender 3.6+** installed and accessible (will auto-detect common locations)
3. **MCP-compatible client** installed

## Installation Steps

### 1. Install Python Dependencies

Open a terminal in the BlenderMCP directory and run:

```bash
pip install -r requirements.txt
```

### 2. Test the Server

Test that the server starts correctly:

```bash
python main.py
```

The server should start without errors. Press Ctrl+C to stop.

### 3. Configure MCP Client

#### Configuration:

1. Add the server to your MCP client's configuration file:

```json
{
  "mcpServers": {
    "blender": {
      "command": "python", 
      "args": ["path/to/BlenderMCP/main.py"],
      "env": {
        "PYTHONPATH": "path/to/BlenderMCP"
      }
    }
  }
}
```

2. Refer to your MCP client's documentation for specific configuration instructions.

### 4. Verify Installation

Restart your MCP client and test with a simple command:

```
"Create a red cube and a blue sphere next to each other"
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

If Blender is not in a standard location, modify `blender_integration.py`:

```python
# Line ~24, replace with your Blender path
blender_manager = BlenderManager("C:\\path\\to\\your\\blender.exe")
```

## Usage Examples

Once configured, you can use natural language commands:

**Basic Objects:**
- "Create a cube and sphere"
- "Make a red cylinder with glass material"

**Advanced Modeling:**
- "Create a house shape using boolean operations"
- "Make a gear using screw modifier on a tooth profile" 
- "Design a smooth organic form using subdivision surfaces"

**Materials & Textures:**
- "Apply a metal material to the cube"
- "Add noise texture to create a rocky surface"
- "Create a glowing emission material"

**Modifiers:**
- "Use array modifier to create a row of pillars"
- "Add mirror modifier for symmetrical design"
- "Apply wave modifier for organic distortion"

## File Structure

```
BlenderMCP/
├── main.py                 # Server entry point
├── server.py              # MCP server with all tools
├── blender_integration.py # Blender API integration
├── advanced_tools.py      # Advanced mesh editing
├── boolean_operations.py  # Boolean operations
├── subdivide_smooth.py    # Subdivision & smoothing
├── materials.py           # Materials & textures  
├── modifiers.py           # Modifier system
├── requirements.txt       # Python dependencies
├── config.json           # Server configuration
├── config.json           # MCP server configuration
└── README.md             # Documentation
```

## Support

For issues or questions:
1. Check the console output for error messages
2. Ensure Blender can run from command line: `blender --version`
3. Test Python imports: `python -c "from mcp.server.fastmcp import FastMCP"`
4. Verify file paths are correct in the configuration