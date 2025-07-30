# Blender MCP Server

A Model Context Protocol (MCP) server that provides 3D model generation capabilities using Blender's Python API.

## Features

- **Primitive Object Creation**: Create cubes, spheres, cylinders, planes, and cones
- **Scene Management**: Clear scenes, save .blend files 
- **Model Export**: Export to OBJ, FBX, STL, and PLY formats
- **Flexible Parameters**: Customize size, location, and naming for all objects
- **Error Handling**: Comprehensive error reporting and logging

## Requirements

- Python 3.8+
- Blender 3.6+ installed and available in PATH or at standard locations
- MCP dependencies (see requirements.txt)

## Installation

### Quick Install for Claude Desktop (Windows)

1. Clone this repository:
```bash
git clone <repository-url>
cd BlenderMCP
```

2. Run the Claude-specific installer:
```bash
install_to_claude.bat
```
This will automatically configure BlenderMCP for Claude Desktop.

3. Restart Claude Desktop

### Quick Install (Other MCP Clients)

1. Clone this repository:
```bash
git clone <repository-url>
cd BlenderMCP
```

2. **Windows**: Run the installer
```bash
install.bat
```

**macOS/Linux**: Install dependencies and configure MCP
```bash
pip install -r requirements.txt
# Configure your MCP client with the server path
```

3. Restart your MCP client

### Manual Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd BlenderMCP
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your MCP client:
```bash
# Add the BlenderMCP server to your MCP client configuration
# See your MCP client documentation for specific instructions
```

4. Ensure Blender is installed and accessible:
   - Add Blender to your system PATH, or
   - Install at standard locations:
     - Windows: `C:\Program Files\Blender Foundation\Blender\blender.exe`
     - macOS: `/Applications/Blender.app/Contents/MacOS/Blender`
     - Linux: `/usr/bin/blender`

## Usage

### Running the Server

Start the MCP server:
```bash
python main.py
```

The server will communicate via JSON-RPC over stdio, following the MCP specification.

### Available Tools

#### Object Creation
- `create_cube(size, location, name)` - Create a cube
- `create_sphere(radius, location, name)` - Create a UV sphere  
- `create_cylinder(radius, depth, location, name)` - Create a cylinder
- `create_plane(size, location, name)` - Create a plane
- `create_cone(radius1, radius2, depth, location, name)` - Create a cone

#### Scene Management  
- `clear_scene()` - Remove all objects from the scene
- `save_blend_file(filepath)` - Save scene as .blend file
- `export_model(filepath, format, selected_only)` - Export to various formats

#### Information
- `get_server_info()` - Get server capabilities and version info
- `list_available_tools()` - List all available tool names

### Example Usage

Once configured in your MCP client, you can use natural language commands:

```
"Create a red cube at position (2, 0, 0) and a blue sphere next to it"
"Make a simple house with a cube base and triangle roof"  
"Export my current scene as an OBJ file to ~/models/my_scene.obj"
```

## Configuration

### Custom Blender Path

If Blender is not in a standard location, you can specify the path by modifying `blender_integration.py`:

```python
blender_manager = BlenderManager("/path/to/your/blender/executable")
```

### MCP Configuration  

#### Claude Desktop
The `install_to_claude.bat` script automatically configures Claude Desktop. It creates or updates a `.mcp.json` file in your project directory.

For more details, see `CLAUDE_INSTALL.md`.

#### Other MCP Clients
The installation process attempts to configure your MCP client automatically. If you need to configure manually, refer to your MCP client's documentation for configuration file locations.

**Manual configuration example:**
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

See `setup_instructions.md` for detailed setup guide.

## Architecture

The server consists of several key components:

- **server.py**: Main MCP server with tool definitions
- **blender_integration.py**: Blender subprocess management and Python API integration
- **main.py**: Entry point and server startup

### How It Works

1. MCP tools receive parameters from the client
2. Python scripts are generated with Blender API calls  
3. Blender runs in background mode to execute scripts
4. Results are parsed and returned to Claude
5. Error handling ensures robust operation

## Troubleshooting

### Common Issues

**"Blender executable not found"**
- Ensure Blender is installed and in PATH
- Check that the executable exists at expected locations
- Modify the BlenderManager initialization with custom path

**"Script execution timed out"**  
- Complex operations may need longer timeout
- Modify timeout parameter in `execute_blender_script()`

**Import/Export errors**
- Ensure target directories exist and are writable
- Check file format support in your Blender version

### Logging

The server logs important events and errors. Check console output for debugging information.

## Contributing

This is a basic implementation focused on primitive object creation. Potential enhancements:

- Material and texture application
- Advanced mesh editing operations
- Animation and keyframe support  
- Lighting and camera setup tools
- Batch processing capabilities

## License

This project is provided as-is for educational and development purposes.