# BlenderMCP

Model Context Protocol server for Blender 3D operations.

## Overview

BlenderMCP enables programmatic control of Blender through MCP, allowing creation and manipulation of 3D objects via natural language commands.

## Installation

1. Clone repository:
```bash
git clone https://github.com/ooMike1/BlenderMCP.git
cd BlenderMCP
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your MCP client (see `mcp_config_example.json`):
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

## Requirements

- Python 3.8+
- Blender 3.6+
- MCP-compatible client

## Features

### Basic Tools
- **Object Creation**: Cubes, spheres, cylinders, planes, cones
- **Scene Management**: Clear scene, save files, export models
- **Formats**: OBJ, FBX, STL, PLY export support

### Advanced Tools
- **Boolean Operations**: Union, difference, intersection
- **Modifiers**: Array, bevel, solidify, subdivision surface
- **Materials**: Basic material application
- **Mesh Operations**: Subdivide and smooth meshes

## Usage

Start server:
```bash
python main.py
```

Example commands:
- "Create a 2x2x2 cube at origin"
- "Apply boolean union to cube and sphere"
- "Export scene as model.obj"
- "Add array modifier with 5 copies"

## Configuration

See `setup_instructions.md` for detailed setup guide.

## Files

- `main.py` - Entry point
- `server.py` - Core MCP server
- `blender_integration.py` - Blender API interface
- `advanced_tools.py` - Extended functionality
- `boolean_operations.py` - Boolean operations
- `modifiers.py` - Modifier tools
- `materials.py` - Material handling

## Troubleshooting

**Blender not found:** Ensure Blender is in PATH or at:
- Windows: `C:\Program Files\Blender Foundation\Blender\`
- macOS: `/Applications/Blender.app`
- Linux: `/usr/bin/blender`

## License

See LICENSE file for details.