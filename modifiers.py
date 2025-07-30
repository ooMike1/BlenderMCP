"""
Modifier system for advanced object manipulation
"""
from typing import Any, Dict, List, Optional, Tuple
import logging
from blender_integration import blender_manager

logger = logging.getLogger(__name__)

def add_array_modifier(object_name: str, count: int = 3, offset: Tuple[float, float, float] = (2.0, 0.0, 0.0),
                      use_relative_offset: bool = True) -> Dict[str, Any]:
    """Add array modifier to duplicate objects.
    
    Args:
        object_name: Name of the object
        count: Number of duplicates
        offset: Offset between duplicates
        use_relative_offset: Use relative offset (vs absolute)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Array", type="ARRAY")',
        f'modifier.count = {count}',
        f'modifier.use_relative_offset = {use_relative_offset}',
        f'modifier.relative_offset_displace = {offset}',
        f'results.append({{"action": "add_array_modifier", "object": "{object_name}", "count": {count}, "offset": {offset}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_array_modifier",
        "object_name": object_name,
        "parameters": {"count": count, "offset": offset, "use_relative_offset": use_relative_offset},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_mirror_modifier(object_name: str, axis: str = "X", use_bisect: bool = False, 
                       merge_threshold: float = 0.001) -> Dict[str, Any]:
    """Add mirror modifier to create symmetrical objects.
    
    Args:
        object_name: Name of the object
        axis: Mirror axis ('X', 'Y', 'Z', or combinations like 'XY')
        use_bisect: Cut the mesh at the mirror plane
        merge_threshold: Distance for merging vertices
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Mirror", type="MIRROR")',
        f'modifier.use_axis[0] = {"X" in axis.upper()}',
        f'modifier.use_axis[1] = {"Y" in axis.upper()}', 
        f'modifier.use_axis[2] = {"Z" in axis.upper()}',
        f'modifier.use_bisect_axis[0] = {use_bisect and "X" in axis.upper()}',
        f'modifier.use_bisect_axis[1] = {use_bisect and "Y" in axis.upper()}',
        f'modifier.use_bisect_axis[2] = {use_bisect and "Z" in axis.upper()}',
        f'modifier.merge_threshold = {merge_threshold}',
        f'results.append({{"action": "add_mirror_modifier", "object": "{object_name}", "axis": "{axis}", "use_bisect": {use_bisect}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_mirror_modifier",
        "object_name": object_name,
        "parameters": {"axis": axis, "use_bisect": use_bisect, "merge_threshold": merge_threshold},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_solidify_modifier(object_name: str, thickness: float = 0.1, offset: float = -1.0) -> Dict[str, Any]:
    """Add solidify modifier to give thickness to surfaces.
    
    Args:
        object_name: Name of the object
        thickness: Thickness of the solidify
        offset: Offset factor (-1 to 1)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Solidify", type="SOLIDIFY")',
        f'modifier.thickness = {thickness}',
        f'modifier.offset = {offset}',
        f'results.append({{"action": "add_solidify_modifier", "object": "{object_name}", "thickness": {thickness}, "offset": {offset}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_solidify_modifier",
        "object_name": object_name,
        "parameters": {"thickness": thickness, "offset": offset},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_bevel_modifier(object_name: str, width: float = 0.1, segments: int = 1, 
                      limit_method: str = "NONE") -> Dict[str, Any]:
    """Add bevel modifier for rounded edges.
    
    Args:
        object_name: Name of the object
        width: Bevel width
        segments: Number of segments
        limit_method: Limit method ('NONE', 'ANGLE', 'WEIGHT', 'VGROUP')
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Bevel", type="BEVEL")',
        f'modifier.width = {width}',
        f'modifier.segments = {segments}',
        f'modifier.limit_method = "{limit_method}"',
        f'results.append({{"action": "add_bevel_modifier", "object": "{object_name}", "width": {width}, "segments": {segments}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_bevel_modifier",
        "object_name": object_name,
        "parameters": {"width": width, "segments": segments, "limit_method": limit_method},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_screw_modifier(object_name: str, angle: float = 6.28318, screw: float = 0.0, 
                      iterations: int = 1, axis: str = "Z") -> Dict[str, Any]:
    """Add screw modifier for spiral/helical shapes.
    
    Args:
        object_name: Name of the object
        angle: Rotation angle in radians (2π = full rotation)
        screw: Screw offset along axis
        iterations: Number of iterations
        axis: Rotation axis ('X', 'Y', 'Z')
    
    Returns:
        Dictionary with operation result
    """
    axis_map = {"X": 0, "Y": 1, "Z": 2}
    axis_index = axis_map.get(axis.upper(), 2)
    
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Screw", type="SCREW")',
        f'modifier.angle = {angle}',
        f'modifier.screw_offset = {screw}',
        f'modifier.iterations = {iterations}',
        f'modifier.axis = {axis_index}',
        f'results.append({{"action": "add_screw_modifier", "object": "{object_name}", "angle": {angle}, "screw": {screw}, "iterations": {iterations}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_screw_modifier",
        "object_name": object_name,
        "parameters": {"angle": angle, "screw": screw, "iterations": iterations, "axis": axis},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_wave_modifier(object_name: str, height: float = 0.5, width: float = 1.5, 
                     speed: float = 1.0, start_position_object: float = 0.0) -> Dict[str, Any]:
    """Add wave modifier for wave distortion.
    
    Args:
        object_name: Name of the object
        height: Wave amplitude
        width: Wave width
        speed: Wave speed
        start_position_object: Starting position along object
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'modifier = obj.modifiers.new(name="Wave", type="WAVE")',
        f'modifier.height = {height}',
        f'modifier.width = {width}',
        f'modifier.speed = {speed}',
        f'modifier.start_position_object = {start_position_object}',
        f'results.append({{"action": "add_wave_modifier", "object": "{object_name}", "height": {height}, "width": {width}, "speed": {speed}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_wave_modifier",
        "object_name": object_name,
        "parameters": {"height": height, "width": width, "speed": speed, "start_position_object": start_position_object},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_displacement_modifier(object_name: str, strength: float = 1.0, mid_level: float = 0.5) -> Dict[str, Any]:
    """Add displacement modifier with noise texture.
    
    Args:
        object_name: Name of the object
        strength: Displacement strength
        mid_level: Middle level (0-1)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'# Create displacement texture',
        f'tex = bpy.data.textures.new(name="DisplacementNoise", type="NOISE")',
        f'tex.noise_scale = 0.25',
        f'# Add displacement modifier',
        f'modifier = obj.modifiers.new(name="Displace", type="DISPLACE")',
        f'modifier.texture = tex',
        f'modifier.strength = {strength}',
        f'modifier.mid_level = {mid_level}',
        f'results.append({{"action": "add_displacement_modifier", "object": "{object_name}", "strength": {strength}, "mid_level": {mid_level}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_displacement_modifier",
        "object_name": object_name,
        "parameters": {"strength": strength, "mid_level": mid_level},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def apply_modifier(object_name: str, modifier_name: str) -> Dict[str, Any]:
    """Apply a modifier to make it permanent.
    
    Args:
        object_name: Name of the object
        modifier_name: Name of the modifier to apply
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.modifier_apply(modifier="{modifier_name}")',
        f'results.append({{"action": "apply_modifier", "object": "{object_name}", "modifier": "{modifier_name}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "apply_modifier",
        "object_name": object_name,
        "modifier_name": modifier_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }