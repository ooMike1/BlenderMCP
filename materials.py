"""
Material and texture application system
"""
from typing import Any, Dict, List, Optional, Tuple
import logging
from blender_integration import blender_manager

logger = logging.getLogger(__name__)

def create_material(name: str, base_color: Tuple[float, float, float, float] = (0.8, 0.2, 0.2, 1.0), 
                   metallic: float = 0.0, roughness: float = 0.5, emission_strength: float = 0.0) -> Dict[str, Any]:
    """Create a new material with basic properties.
    
    Args:
        name: Name for the material
        base_color: RGBA color values (0.0-1.0)
        metallic: Metallic factor (0.0-1.0)
        roughness: Roughness factor (0.0-1.0)
        emission_strength: Emission strength
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'mat = bpy.data.materials.new(name="{name}")',
        f'mat.use_nodes = True',
        f'bsdf = mat.node_tree.nodes["Principled BSDF"]',
        f'bsdf.inputs["Base Color"].default_value = {base_color}',
        f'bsdf.inputs["Metallic"].default_value = {metallic}',
        f'bsdf.inputs["Roughness"].default_value = {roughness}',
        f'bsdf.inputs["Emission Strength"].default_value = {emission_strength}',
        f'results.append({{"action": "create_material", "material": "{name}", "base_color": {base_color}, "metallic": {metallic}, "roughness": {roughness}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "create_material",
        "material_name": name,
        "properties": {
            "base_color": base_color,
            "metallic": metallic,
            "roughness": roughness,
            "emission_strength": emission_strength
        },
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def apply_material_to_object(object_name: str, material_name: str) -> Dict[str, Any]:
    """Apply a material to an object.
    
    Args:
        object_name: Name of the object
        material_name: Name of the material to apply
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'mat = bpy.data.materials["{material_name}"]',
        f'if obj.data.materials:',
        f'    obj.data.materials[0] = mat',
        f'else:',
        f'    obj.data.materials.append(mat)',
        f'results.append({{"action": "apply_material", "object": "{object_name}", "material": "{material_name}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "apply_material",
        "object_name": object_name,
        "material_name": material_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def create_glass_material(name: str, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                         ior: float = 1.45, transmission: float = 1.0) -> Dict[str, Any]:
    """Create a glass material.
    
    Args:
        name: Name for the material
        color: RGBA color values
        ior: Index of refraction
        transmission: Transmission factor
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'mat = bpy.data.materials.new(name="{name}")',
        f'mat.use_nodes = True',
        f'bsdf = mat.node_tree.nodes["Principled BSDF"]',
        f'bsdf.inputs["Base Color"].default_value = {color}',
        f'bsdf.inputs["Metallic"].default_value = 0.0',
        f'bsdf.inputs["Roughness"].default_value = 0.0',
        f'bsdf.inputs["IOR"].default_value = {ior}',
        f'bsdf.inputs["Transmission"].default_value = {transmission}',
        f'bsdf.inputs["Alpha"].default_value = 0.1',
        f'mat.blend_method = "BLEND"',
        f'results.append({{"action": "create_glass_material", "material": "{name}", "ior": {ior}, "transmission": {transmission}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "create_glass_material",
        "material_name": name,
        "properties": {"color": color, "ior": ior, "transmission": transmission},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def create_metal_material(name: str, color: Tuple[float, float, float, float] = (0.7, 0.7, 0.7, 1.0),
                         roughness: float = 0.2) -> Dict[str, Any]:
    """Create a metallic material.
    
    Args:
        name: Name for the material
        color: RGBA color values
        roughness: Surface roughness
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'mat = bpy.data.materials.new(name="{name}")',
        f'mat.use_nodes = True',
        f'bsdf = mat.node_tree.nodes["Principled BSDF"]',
        f'bsdf.inputs["Base Color"].default_value = {color}',
        f'bsdf.inputs["Metallic"].default_value = 1.0',
        f'bsdf.inputs["Roughness"].default_value = {roughness}',
        f'results.append({{"action": "create_metal_material", "material": "{name}", "color": {color}, "roughness": {roughness}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "create_metal_material",
        "material_name": name,
        "properties": {"color": color, "roughness": roughness},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def create_emission_material(name: str, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
                           strength: float = 5.0) -> Dict[str, Any]:
    """Create an emissive/glowing material.
    
    Args:
        name: Name for the material
        color: RGBA emission color
        strength: Emission strength
    
    Returns:
        Dictionary with creation result
    """
    operations = [
        f'mat = bpy.data.materials.new(name="{name}")',
        f'mat.use_nodes = True',
        f'bsdf = mat.node_tree.nodes["Principled BSDF"]',
        f'bsdf.inputs["Base Color"].default_value = {color}',
        f'bsdf.inputs["Emission"].default_value = {color}',
        f'bsdf.inputs["Emission Strength"].default_value = {strength}',
        f'results.append({{"action": "create_emission_material", "material": "{name}", "color": {color}, "strength": {strength}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "create_emission_material",
        "material_name": name,
        "properties": {"color": color, "strength": strength},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_noise_texture(object_name: str, scale: float = 5.0, detail: float = 2.0, 
                     roughness: float = 0.5, distortion: float = 0.0) -> Dict[str, Any]:
    """Add procedural noise texture to an object's material.
    
    Args:
        object_name: Name of the object
        scale: Noise scale
        detail: Level of detail
        roughness: Noise roughness
        distortion: Distortion amount
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'if not obj.data.materials:',
        f'    mat = bpy.data.materials.new(name="{object_name}_Material")',
        f'    mat.use_nodes = True',
        f'    obj.data.materials.append(mat)',
        f'else:',
        f'    mat = obj.data.materials[0]',
        f'    if not mat.use_nodes:',
        f'        mat.use_nodes = True',
        f'nodes = mat.node_tree.nodes',
        f'links = mat.node_tree.links',
        f'bsdf = nodes["Principled BSDF"]',
        f'noise_tex = nodes.new(type="ShaderNodeTexNoise")',
        f'noise_tex.inputs["Scale"].default_value = {scale}',
        f'noise_tex.inputs["Detail"].default_value = {detail}',
        f'noise_tex.inputs["Roughness"].default_value = {roughness}',
        f'noise_tex.inputs["Distortion"].default_value = {distortion}',
        f'links.new(noise_tex.outputs["Fac"], bsdf.inputs["Base Color"])',
        f'results.append({{"action": "add_noise_texture", "object": "{object_name}", "scale": {scale}, "detail": {detail}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_noise_texture",
        "object_name": object_name,
        "parameters": {"scale": scale, "detail": detail, "roughness": roughness, "distortion": distortion},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def add_uv_mapping(object_name: str) -> Dict[str, Any]:
    """Add UV mapping to an object.
    
    Args:
        object_name: Name of the object
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.001)',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "add_uv_mapping", "object": "{object_name}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "add_uv_mapping",
        "object_name": object_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }