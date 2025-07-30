"""
Subdivision and smoothing tools for detailed mesh work
"""
from typing import Any, Dict, List, Optional, Tuple
import logging
from blender_integration import blender_manager

logger = logging.getLogger(__name__)

def subdivide_surface(object_name: str, levels: int = 1, render_levels: int = None) -> Dict[str, Any]:
    """Apply subdivision surface modifier to an object.
    
    Args:
        object_name: Name of the object to subdivide
        levels: Subdivision levels for viewport
        render_levels: Subdivision levels for rendering (uses levels if None)
    
    Returns:
        Dictionary with operation result
    """
    if render_levels is None:
        render_levels = levels
    
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="SubdivisionSurface", type="SUBSURF")',
        f'modifier.levels = {levels}',
        f'modifier.render_levels = {render_levels}',
        f'results.append({{"action": "subdivide_surface", "object": "{object_name}", "levels": {levels}, "render_levels": {render_levels}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "subdivide_surface",
        "object_name": object_name,
        "parameters": {"levels": levels, "render_levels": render_levels},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def smooth_object(object_name: str, iterations: int = 1, factor: float = 0.5) -> Dict[str, Any]:
    """Apply smooth shading and smoothing to an object.
    
    Args:
        object_name: Name of the object to smooth
        iterations: Number of smoothing iterations
        factor: Smoothing factor (0.0 to 1.0)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'for i in range({iterations}):',
        f'    bpy.ops.mesh.vertices_smooth(factor={factor})',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'bpy.ops.object.shade_smooth()',
        f'results.append({{"action": "smooth_object", "object": "{object_name}", "iterations": {iterations}, "factor": {factor}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "smooth_object",
        "object_name": object_name,
        "parameters": {"iterations": iterations, "factor": factor},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def remesh_object(object_name: str, octree_depth: int = 4, scale: float = 0.99, mode: str = "BLOCKS") -> Dict[str, Any]:
    """Apply remesh modifier to create uniform topology.
    
    Args:
        object_name: Name of the object to remesh
        octree_depth: Level of detail (4-10 typical range)
        scale: Scale factor for remesh
        mode: Remesh mode ('BLOCKS', 'SMOOTH', 'SHARP', 'VOXEL')
    
    Returns:
        Dictionary with operation result
    """
    valid_modes = ['BLOCKS', 'SMOOTH', 'SHARP', 'VOXEL']
    if mode not in valid_modes:
        return {
            "success": False,
            "error": f"Invalid remesh mode: {mode}. Valid modes: {valid_modes}"
        }
    
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Remesh", type="REMESH")',
        f'modifier.mode = "{mode}"',
        f'modifier.octree_depth = {octree_depth}',
        f'modifier.scale = {scale}',
        f'bpy.ops.object.modifier_apply(modifier="Remesh")',
        f'results.append({{"action": "remesh_object", "object": "{object_name}", "mode": "{mode}", "octree_depth": {octree_depth}, "scale": {scale}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "remesh_object", 
        "object_name": object_name,
        "parameters": {"mode": mode, "octree_depth": octree_depth, "scale": scale},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def decimate_object(object_name: str, ratio: float = 0.5, decimate_type: str = "COLLAPSE") -> Dict[str, Any]:
    """Reduce mesh complexity using decimation.
    
    Args:
        object_name: Name of the object to decimate
        ratio: Reduction ratio (0.0 to 1.0)
        decimate_type: Type of decimation ('COLLAPSE', 'UNSUBDIV', 'DISSOLVE')
    
    Returns:
        Dictionary with operation result
    """
    valid_types = ['COLLAPSE', 'UNSUBDIV', 'DISSOLVE']
    if decimate_type not in valid_types:
        return {
            "success": False,
            "error": f"Invalid decimate type: {decimate_type}. Valid types: {valid_types}"
        }
    
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Decimate", type="DECIMATE")',
        f'modifier.decimate_type = "{decimate_type}"',
        f'modifier.ratio = {ratio}',
        f'bpy.ops.object.modifier_apply(modifier="Decimate")',
        f'results.append({{"action": "decimate_object", "object": "{object_name}", "type": "{decimate_type}", "ratio": {ratio}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "decimate_object",
        "object_name": object_name,
        "parameters": {"type": decimate_type, "ratio": ratio},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_edge_split(object_name: str, split_angle: float = 0.523599) -> Dict[str, Any]:
    """Add edge split modifier for sharp edges.
    
    Args:
        object_name: Name of the object
        split_angle: Angle threshold in radians (default ~30 degrees)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="EdgeSplit", type="EDGE_SPLIT")',
        f'modifier.split_angle = {split_angle}',
        f'modifier.use_edge_angle = True',
        f'results.append({{"action": "add_edge_split", "object": "{object_name}", "split_angle": {split_angle}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_edge_split",
        "object_name": object_name,
        "parameters": {"split_angle": split_angle},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def triangulate_mesh(object_name: str, quad_method: str = "BEAUTY", ngon_method: str = "BEAUTY") -> Dict[str, Any]:
    """Triangulate mesh faces.
    
    Args:
        object_name: Name of the object to triangulate
        quad_method: Method for triangulating quads ('BEAUTY', 'FIXED', 'FIXED_ALTERNATE', 'SHORTEST_DIAGONAL')
        ngon_method: Method for triangulating ngons ('BEAUTY', 'CLIP')
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'bpy.ops.mesh.quads_convert_to_tris(quad_method="{quad_method}", ngon_method="{ngon_method}")',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "triangulate_mesh", "object": "{object_name}", "quad_method": "{quad_method}", "ngon_method": "{ngon_method}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "triangulate_mesh",
        "object_name": object_name,
        "parameters": {"quad_method": quad_method, "ngon_method": ngon_method},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }