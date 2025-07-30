"""
Blender MCP Server - Provides 3D model generation capabilities through Blender Python API
"""
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Optional, Tuple
import logging
import os
import sys
import json
import asyncio

# Configure logging to stderr to avoid interfering with stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("blender-mcp-server")

# Tool definitions
async def handle_get_server_info(arguments: dict) -> List[TextContent]:
    """Get information about the Blender MCP server capabilities."""
    from blender_integration import blender_manager
    
    result = {
        "name": "Blender MCP Server",
        "version": "1.0.0",
        "description": "MCP server for 3D model generation using Blender",
        "capabilities": [
            "create_primitive_objects",
            "modify_meshes", 
            "apply_materials",
            "scene_management",
            "file_operations"
        ]
    }
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_list_available_tools(arguments: dict) -> List[TextContent]:
    """List all available 3D modeling tools."""
    tools = [
        "create_cube",
        "create_sphere", 
        "create_cylinder",
        "create_plane",
        "create_cone",
        "save_blend_file",
        "export_model",
        "clear_scene",
        "get_server_info",
        "list_available_tools"
    ]
    return [TextContent(type="text", text=json.dumps(tools, indent=2))]

async def handle_create_cube(arguments: dict) -> List[TextContent]:
    """Create a cube in the Blender scene."""
    from blender_integration import blender_manager
    
    size = arguments.get("size", 2.0)
    location = arguments.get("location", [0, 0, 0])
    name = arguments.get("name", "Cube")
    
    operations = [
        f'bpy.ops.mesh.primitive_cube_add(size={size}, location={tuple(location)})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cube", "size": {size}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "object_name": name,
        "object_type": "cube",
        "parameters": {"size": size, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_create_sphere(arguments: dict) -> List[TextContent]:
    """Create a UV sphere in the Blender scene."""
    from blender_integration import blender_manager
    
    radius = arguments.get("radius", 1.0)
    location = arguments.get("location", [0, 0, 0])
    name = arguments.get("name", "Sphere")
    
    operations = [
        f'bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location={tuple(location)})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "sphere", "radius": {radius}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "object_name": name,
        "object_type": "sphere",
        "parameters": {"radius": radius, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_create_cylinder(arguments: dict) -> List[TextContent]:
    """Create a cylinder in the Blender scene."""
    from blender_integration import blender_manager
    
    radius = arguments.get("radius", 1.0)
    depth = arguments.get("depth", 2.0)
    location = arguments.get("location", [0, 0, 0])
    name = arguments.get("name", "Cylinder")
    
    operations = [
        f'bpy.ops.mesh.primitive_cylinder_add(radius={radius}, depth={depth}, location={tuple(location)})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cylinder", "radius": {radius}, "depth": {depth}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "object_name": name,
        "object_type": "cylinder", 
        "parameters": {"radius": radius, "depth": depth, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_create_plane(arguments: dict) -> List[TextContent]:
    """Create a plane in the Blender scene."""
    from blender_integration import blender_manager
    
    size = arguments.get("size", 2.0)
    location = arguments.get("location", [0, 0, 0])
    name = arguments.get("name", "Plane")
    
    operations = [
        f'bpy.ops.mesh.primitive_plane_add(size={size}, location={tuple(location)})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "plane", "size": {size}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "object_name": name,
        "object_type": "plane",
        "parameters": {"size": size, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_create_cone(arguments: dict) -> List[TextContent]:
    """Create a cone in the Blender scene."""
    from blender_integration import blender_manager
    
    radius1 = arguments.get("radius1", 1.0)
    radius2 = arguments.get("radius2", 0.0)
    depth = arguments.get("depth", 2.0)
    location = arguments.get("location", [0, 0, 0])
    name = arguments.get("name", "Cone")
    
    operations = [
        f'bpy.ops.mesh.primitive_cone_add(radius1={radius1}, radius2={radius2}, depth={depth}, location={tuple(location)})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cone", "radius1": {radius1}, "radius2": {radius2}, "depth": {depth}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "object_name": name,
        "object_type": "cone",
        "parameters": {"radius1": radius1, "radius2": radius2, "depth": depth, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_clear_scene(arguments: dict) -> List[TextContent]:
    """Clear all objects from the Blender scene."""
    from blender_integration import blender_manager
    
    operations = [
        'bpy.ops.object.select_all(action="SELECT")',
        'bpy.ops.object.delete(use_global=False, confirm=False)',
        'results.append({"action": "clear_scene", "status": "completed"})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "action": "clear_scene",
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_save_blend_file(arguments: dict) -> List[TextContent]:
    """Save the current Blender scene to a .blend file."""
    from blender_integration import blender_manager
    
    filepath = arguments.get("filepath", "")
    if not filepath:
        return [TextContent(type="text", text=json.dumps({"success": False, "error": "filepath is required"}))]
    
    if not filepath.endswith('.blend'):
        filepath += '.blend'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    operations = [
        f'bpy.ops.wm.save_as_mainfile(filepath=r"{filepath}")',
        f'results.append({{"action": "save_blend_file", "filepath": r"{filepath}", "status": "completed"}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "action": "save_blend_file",
        "filepath": filepath,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

async def handle_export_model(arguments: dict) -> List[TextContent]:
    """Export 3D model to various formats."""
    from blender_integration import blender_manager
    
    filepath = arguments.get("filepath", "")
    format = arguments.get("format", "obj").lower()
    selected_only = arguments.get("selected_only", False)
    
    if not filepath:
        return [TextContent(type="text", text=json.dumps({"success": False, "error": "filepath is required"}))]
    
    supported_formats = ['obj', 'fbx', 'stl', 'ply']
    
    if format not in supported_formats:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"Unsupported format: {format}. Supported: {supported_formats}"
        }))]
    
    # Ensure proper file extension
    if not filepath.endswith(f'.{format}'):
        filepath += f'.{format}'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Generate export operation based on format
    if format == 'obj':
        export_op = f'bpy.ops.export_scene.obj(filepath=r"{filepath}", use_selection={selected_only})'
    elif format == 'fbx':
        export_op = f'bpy.ops.export_scene.fbx(filepath=r"{filepath}", use_selection={selected_only})'
    elif format == 'stl':
        export_op = f'bpy.ops.export_mesh.stl(filepath=r"{filepath}", use_selection={selected_only})'
    elif format == 'ply':
        export_op = f'bpy.ops.export_mesh.ply(filepath=r"{filepath}", use_selection={selected_only})'
    
    operations = [
        export_op,
        f'results.append({{"action": "export_model", "filepath": r"{filepath}", "format": "{format}", "status": "completed"}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    response = {
        "success": result["success"],
        "action": "export_model",
        "filepath": filepath,
        "format": format,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]

# Register all tools
@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="get_server_info",
            description="Get information about the Blender MCP server capabilities",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_available_tools",
            description="List all available 3D modeling tools",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="create_cube",
            description="Create a cube in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "size": {
                        "type": "number",
                        "description": "Size of the cube",
                        "default": 2.0
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location as [x, y, z] array",
                        "default": [0, 0, 0]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the cube object",
                        "default": "Cube"
                    }
                }
            }
        ),
        Tool(
            name="create_sphere",
            description="Create a UV sphere in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "Radius of the sphere",
                        "default": 1.0
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location as [x, y, z] array",
                        "default": [0, 0, 0]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the sphere object",
                        "default": "Sphere"
                    }
                }
            }
        ),
        Tool(
            name="create_cylinder",
            description="Create a cylinder in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "Radius of the cylinder",
                        "default": 1.0
                    },
                    "depth": {
                        "type": "number",
                        "description": "Height/depth of the cylinder",
                        "default": 2.0
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location as [x, y, z] array",
                        "default": [0, 0, 0]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the cylinder object",
                        "default": "Cylinder"
                    }
                }
            }
        ),
        Tool(
            name="create_plane",
            description="Create a plane in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "size": {
                        "type": "number",
                        "description": "Size of the plane",
                        "default": 2.0
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location as [x, y, z] array",
                        "default": [0, 0, 0]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the plane object",
                        "default": "Plane"
                    }
                }
            }
        ),
        Tool(
            name="create_cone",
            description="Create a cone in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius1": {
                        "type": "number",
                        "description": "Bottom radius of the cone",
                        "default": 1.0
                    },
                    "radius2": {
                        "type": "number",
                        "description": "Top radius of the cone (0 for pointed)",
                        "default": 0.0
                    },
                    "depth": {
                        "type": "number",
                        "description": "Height of the cone",
                        "default": 2.0
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location as [x, y, z] array",
                        "default": [0, 0, 0]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the cone object",
                        "default": "Cone"
                    }
                }
            }
        ),
        Tool(
            name="clear_scene",
            description="Clear all objects from the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="save_blend_file",
            description="Save the current Blender scene to a .blend file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path where to save the .blend file"
                    }
                },
                "required": ["filepath"]
            }
        ),
        Tool(
            name="export_model",
            description="Export 3D model to various formats (obj, fbx, stl, ply)",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format",
                        "enum": ["obj", "fbx", "stl", "ply"],
                        "default": "obj"
                    },
                    "selected_only": {
                        "type": "boolean",
                        "description": "Export only selected objects",
                        "default": False
                    }
                },
                "required": ["filepath"]
            }
        )
    ]

# Register tool handlers
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    handlers = {
        "get_server_info": handle_get_server_info,
        "list_available_tools": handle_list_available_tools,
        "create_cube": handle_create_cube,
        "create_sphere": handle_create_sphere,
        "create_cylinder": handle_create_cylinder,
        "create_plane": handle_create_plane,
        "create_cone": handle_create_cone,
        "clear_scene": handle_clear_scene,
        "save_blend_file": handle_save_blend_file,
        "export_model": handle_export_model
    }
    
    handler = handlers.get(name)
    if not handler:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    try:
        return await handler(arguments)
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }))]

# Main function to run the server
async def main():
    """Main entry point for the MCP server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Blender MCP Server...")
    logger.info("Available tools: Basic primitives, scene management, file operations")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="blender-mcp-server",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())