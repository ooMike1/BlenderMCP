"""
Blender MCP Server - Provides 3D model generation capabilities through Blender Python API
"""
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Optional, Tuple
import logging
import os
import json
from blender_integration import blender_manager

# Import advanced tool modules
from advanced_tools import *
from boolean_operations import *
from subdivide_smooth import *
from materials import *
from modifiers import *

# Configure logging to stderr to avoid interfering with stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=os.sys.stderr
)
logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = Server("blender-mcp-server")

@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """Get information about the Blender MCP server capabilities."""
    return {
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

@mcp.tool()
def list_available_tools() -> List[str]:
    """List all available 3D modeling tools."""
    return [
        "create_cube",
        "create_sphere", 
        "create_cylinder",
        "create_plane",
        "create_cone",
        "save_blend_file",
        "export_model",
        "clear_scene",
        "set_render_settings"
    ]

@mcp.tool()
def create_cube(size: float = 2.0, location: Tuple[float, float, float] = (0, 0, 0), name: str = "Cube") -> Dict[str, Any]:
    """Create a cube in the Blender scene.
    
    Args:
        size: Size of the cube (default: 2.0)
        location: Location as (x, y, z) tuple (default: (0, 0, 0))
        name: Name for the cube object (default: "Cube")
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'bpy.ops.mesh.primitive_cube_add(size={size}, location={location})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cube", "size": {size}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "cube",
        "parameters": {"size": size, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def create_sphere(radius: float = 1.0, location: Tuple[float, float, float] = (0, 0, 0), name: str = "Sphere") -> Dict[str, Any]:
    """Create a UV sphere in the Blender scene.
    
    Args:
        radius: Radius of the sphere (default: 1.0)
        location: Location as (x, y, z) tuple (default: (0, 0, 0))
        name: Name for the sphere object (default: "Sphere")
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location={location})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "sphere", "radius": {radius}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "sphere",
        "parameters": {"radius": radius, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def create_cylinder(radius: float = 1.0, depth: float = 2.0, location: Tuple[float, float, float] = (0, 0, 0), name: str = "Cylinder") -> Dict[str, Any]:
    """Create a cylinder in the Blender scene.
    
    Args:
        radius: Radius of the cylinder (default: 1.0)
        depth: Height/depth of the cylinder (default: 2.0)
        location: Location as (x, y, z) tuple (default: (0, 0, 0))
        name: Name for the cylinder object (default: "Cylinder")
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'bpy.ops.mesh.primitive_cylinder_add(radius={radius}, depth={depth}, location={location})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cylinder", "radius": {radius}, "depth": {depth}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "cylinder", 
        "parameters": {"radius": radius, "depth": depth, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def create_plane(size: float = 2.0, location: Tuple[float, float, float] = (0, 0, 0), name: str = "Plane") -> Dict[str, Any]:
    """Create a plane in the Blender scene.
    
    Args:
        size: Size of the plane (default: 2.0)
        location: Location as (x, y, z) tuple (default: (0, 0, 0))
        name: Name for the plane object (default: "Plane")
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'bpy.ops.mesh.primitive_plane_add(size={size}, location={location})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "plane", "size": {size}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "plane",
        "parameters": {"size": size, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def create_cone(radius1: float = 1.0, radius2: float = 0.0, depth: float = 2.0, location: Tuple[float, float, float] = (0, 0, 0), name: str = "Cone") -> Dict[str, Any]:
    """Create a cone in the Blender scene.
    
    Args:
        radius1: Bottom radius of the cone (default: 1.0)
        radius2: Top radius of the cone (default: 0.0 for pointed cone)
        depth: Height of the cone (default: 2.0)
        location: Location as (x, y, z) tuple (default: (0, 0, 0))
        name: Name for the cone object (default: "Cone")
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'bpy.ops.mesh.primitive_cone_add(radius1={radius1}, radius2={radius2}, depth={depth}, location={location})',
        f'bpy.context.active_object.name = "{name}"',
        f'results.append({{"object": "{name}", "type": "cone", "radius1": {radius1}, "radius2": {radius2}, "depth": {depth}, "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "cone",
        "parameters": {"radius1": radius1, "radius2": radius2, "depth": depth, "location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def clear_scene() -> Dict[str, Any]:
    """Clear all objects from the Blender scene."""
    operations = [
        'bpy.ops.object.select_all(action="SELECT")',
        'bpy.ops.object.delete(use_global=False, confirm=False)',
        'results.append({"action": "clear_scene", "status": "completed"})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "clear_scene",
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def save_blend_file(filepath: str) -> Dict[str, Any]:
    """Save the current Blender scene to a .blend file.
    
    Args:
        filepath: Path where to save the .blend file
    
    Returns:
        Dictionary with save result
    """
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
    
    return {
        "success": result["success"],
        "action": "save_blend_file",
        "filepath": filepath,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

@mcp.tool()
def export_model(filepath: str, format: str = "obj", selected_only: bool = False) -> Dict[str, Any]:
    """Export 3D model to various formats.
    
    Args:
        filepath: Output file path
        format: Export format ('obj', 'fbx', 'stl', 'ply') (default: 'obj')
        selected_only: Export only selected objects (default: False)
    
    Returns:
        Dictionary with export result
    """
    format = format.lower()
    supported_formats = ['obj', 'fbx', 'stl', 'ply']
    
    if format not in supported_formats:
        return {
            "success": False,
            "error": f"Unsupported format: {format}. Supported: {supported_formats}"
        }
    
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
    
    return {
        "success": result["success"],
        "action": "export_model",
        "filepath": filepath,
        "format": format,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

# ===== ADVANCED MESH EDITING TOOLS =====

@mcp.tool()
def create_mesh_from_vertices(vertices: List[Tuple[float, float, float]], 
                             faces: List[List[int]], 
                             name: str = "CustomMesh") -> Dict[str, Any]:
    """Create a custom mesh from vertices and faces."""
    return create_mesh_from_vertices(vertices, faces, name)

@mcp.tool()
def extrude_face(object_name: str, face_index: int, distance: float = 1.0) -> Dict[str, Any]:
    """Extrude a specific face of an object."""
    return extrude_face(object_name, face_index, distance)

@mcp.tool()
def inset_faces(object_name: str, thickness: float = 0.1, depth: float = 0.0) -> Dict[str, Any]:
    """Inset faces of an object."""
    return inset_faces(object_name, thickness, depth)

@mcp.tool()
def bevel_edges(object_name: str, offset: float = 0.1, segments: int = 1) -> Dict[str, Any]:
    """Bevel edges of an object."""
    return bevel_edges(object_name, offset, segments)

@mcp.tool()
def loop_cut(object_name: str, cuts: int = 1, smoothness: float = 0.0) -> Dict[str, Any]:
    """Add loop cuts to an object."""
    return loop_cut(object_name, cuts, smoothness)

@mcp.tool()
def scale_object(object_name: str, scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)) -> Dict[str, Any]:
    """Scale an object along different axes."""
    return scale_object(object_name, scale)

@mcp.tool()
def rotate_object(object_name: str, rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Dict[str, Any]:
    """Rotate an object."""
    return rotate_object(object_name, rotation)

@mcp.tool()
def move_object(object_name: str, location: Tuple[float, float, float]) -> Dict[str, Any]:
    """Move an object to a new location."""
    return move_object(object_name, location)

# ===== BOOLEAN OPERATIONS =====

@mcp.tool()
def boolean_union(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean union operation between two objects."""
    return boolean_union(object1_name, object2_name, result_name)

@mcp.tool()
def boolean_difference(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean difference operation (subtract object2 from object1)."""
    return boolean_difference(object1_name, object2_name, result_name)

@mcp.tool()
def boolean_intersection(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean intersection operation between two objects."""
    return boolean_intersection(object1_name, object2_name, result_name)

@mcp.tool()
def duplicate_object(object_name: str, new_name: str = None, offset: Tuple[float, float, float] = (0, 0, 0)) -> Dict[str, Any]:
    """Duplicate an object."""
    return duplicate_object(object_name, new_name, offset)

@mcp.tool()
def join_objects(object_names: List[str], result_name: str = "JoinedObject") -> Dict[str, Any]:
    """Join multiple objects into one."""
    return join_objects(object_names, result_name)

@mcp.tool()
def separate_object_by_loose_parts(object_name: str) -> Dict[str, Any]:
    """Separate an object into loose parts."""
    return separate_object_by_loose_parts(object_name)

# ===== SUBDIVISION AND SMOOTHING =====

@mcp.tool()
def subdivide_surface(object_name: str, levels: int = 1, render_levels: int = None) -> Dict[str, Any]:
    """Apply subdivision surface modifier to an object."""
    return subdivide_surface(object_name, levels, render_levels)

@mcp.tool()
def smooth_object(object_name: str, iterations: int = 1, factor: float = 0.5) -> Dict[str, Any]:
    """Apply smooth shading and smoothing to an object."""
    return smooth_object(object_name, iterations, factor)

@mcp.tool()
def remesh_object(object_name: str, octree_depth: int = 4, scale: float = 0.99, mode: str = "BLOCKS") -> Dict[str, Any]:
    """Apply remesh modifier to create uniform topology."""
    return remesh_object(object_name, octree_depth, scale, mode)

@mcp.tool()
def decimate_object(object_name: str, ratio: float = 0.5, decimate_type: str = "COLLAPSE") -> Dict[str, Any]:
    """Reduce mesh complexity using decimation."""
    return decimate_object(object_name, ratio, decimate_type)

@mcp.tool()
def add_edge_split(object_name: str, split_angle: float = 0.523599) -> Dict[str, Any]:
    """Add edge split modifier for sharp edges."""
    return add_edge_split(object_name, split_angle)

@mcp.tool()
def triangulate_mesh(object_name: str, quad_method: str = "BEAUTY", ngon_method: str = "BEAUTY") -> Dict[str, Any]:
    """Triangulate mesh faces."""
    return triangulate_mesh(object_name, quad_method, ngon_method)

# ===== MATERIALS AND TEXTURES =====

@mcp.tool()
def create_material(name: str, base_color: Tuple[float, float, float, float] = (0.8, 0.2, 0.2, 1.0), 
                   metallic: float = 0.0, roughness: float = 0.5, emission_strength: float = 0.0) -> Dict[str, Any]:
    """Create a new material with basic properties."""
    return create_material(name, base_color, metallic, roughness, emission_strength)

@mcp.tool()
def apply_material_to_object(object_name: str, material_name: str) -> Dict[str, Any]:
    """Apply a material to an object."""
    return apply_material_to_object(object_name, material_name)

@mcp.tool()
def create_glass_material(name: str, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                         ior: float = 1.45, transmission: float = 1.0) -> Dict[str, Any]:
    """Create a glass material."""
    return create_glass_material(name, color, ior, transmission)

@mcp.tool()
def create_metal_material(name: str, color: Tuple[float, float, float, float] = (0.7, 0.7, 0.7, 1.0),
                         roughness: float = 0.2) -> Dict[str, Any]:
    """Create a metallic material."""
    return create_metal_material(name, color, roughness)

@mcp.tool()
def create_emission_material(name: str, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
                           strength: float = 5.0) -> Dict[str, Any]:
    """Create an emissive/glowing material."""
    return create_emission_material(name, color, strength)

@mcp.tool()
def add_noise_texture(object_name: str, scale: float = 5.0, detail: float = 2.0, 
                     roughness: float = 0.5, distortion: float = 0.0) -> Dict[str, Any]:
    """Add procedural noise texture to an object's material."""
    return add_noise_texture(object_name, scale, detail, roughness, distortion)

@mcp.tool()
def add_uv_mapping(object_name: str) -> Dict[str, Any]:
    """Add UV mapping to an object."""
    return add_uv_mapping(object_name)

# ===== MODIFIERS =====

@mcp.tool()
def add_array_modifier(object_name: str, count: int = 3, offset: Tuple[float, float, float] = (2.0, 0.0, 0.0),
                      use_relative_offset: bool = True) -> Dict[str, Any]:
    """Add array modifier to duplicate objects."""
    return add_array_modifier(object_name, count, offset, use_relative_offset)

@mcp.tool()
def add_mirror_modifier(object_name: str, axis: str = "X", use_bisect: bool = False, 
                       merge_threshold: float = 0.001) -> Dict[str, Any]:
    """Add mirror modifier to create symmetrical objects."""
    return add_mirror_modifier(object_name, axis, use_bisect, merge_threshold)

@mcp.tool()
def add_solidify_modifier(object_name: str, thickness: float = 0.1, offset: float = -1.0) -> Dict[str, Any]:
    """Add solidify modifier to give thickness to surfaces."""
    return add_solidify_modifier(object_name, thickness, offset)

@mcp.tool()
def add_bevel_modifier(object_name: str, width: float = 0.1, segments: int = 1, 
                      limit_method: str = "NONE") -> Dict[str, Any]:
    """Add bevel modifier for rounded edges."""
    return add_bevel_modifier(object_name, width, segments, limit_method)

@mcp.tool()
def add_screw_modifier(object_name: str, angle: float = 6.28318, screw: float = 0.0, 
                      iterations: int = 1, axis: str = "Z") -> Dict[str, Any]:
    """Add screw modifier for spiral/helical shapes."""
    return add_screw_modifier(object_name, angle, screw, iterations, axis)

@mcp.tool()
def add_wave_modifier(object_name: str, height: float = 0.5, width: float = 1.5, 
                     speed: float = 1.0, start_position_object: float = 0.0) -> Dict[str, Any]:
    """Add wave modifier for wave distortion."""
    return add_wave_modifier(object_name, height, width, speed, start_position_object)

@mcp.tool()
def add_displacement_modifier(object_name: str, strength: float = 1.0, mid_level: float = 0.5) -> Dict[str, Any]:
    """Add displacement modifier with noise texture."""
    return add_displacement_modifier(object_name, strength, mid_level)

@mcp.tool()
def apply_modifier(object_name: str, modifier_name: str) -> Dict[str, Any]:
    """Apply a modifier to make it permanent."""
    return apply_modifier(object_name, modifier_name)