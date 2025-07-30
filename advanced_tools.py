"""
Advanced 3D modeling tools for complex model generation
"""
from typing import Any, Dict, List, Optional, Tuple
import logging
from blender_integration import blender_manager

logger = logging.getLogger(__name__)

def create_mesh_from_vertices(vertices: List[Tuple[float, float, float]], 
                             faces: List[List[int]], 
                             name: str = "CustomMesh") -> Dict[str, Any]:
    """Create a custom mesh from vertices and faces.
    
    Args:
        vertices: List of (x, y, z) vertex coordinates
        faces: List of face indices (each face is a list of vertex indices)
        name: Name for the mesh object
    
    Returns:
        Dictionary with creation result
    """
    vertices_str = str(vertices).replace("'", "")
    faces_str = str(faces).replace("'", "")
    
    operations = [
        f'import bmesh',
        f'mesh = bpy.data.meshes.new("{name}")',
        f'obj = bpy.data.objects.new("{name}", mesh)',
        f'bpy.context.collection.objects.link(obj)',
        f'bm = bmesh.new()',
        f'vertices = {vertices_str}',
        f'faces = {faces_str}',
        f'for v in vertices:',
        f'    bm.verts.new(v)',
        f'bm.verts.ensure_lookup_table()',
        f'for f in faces:',
        f'    bm.faces.new([bm.verts[i] for i in f])',
        f'bm.to_mesh(mesh)',
        f'bm.free()',
        f'results.append({{"object": "{name}", "type": "custom_mesh", "vertices": len(vertices), "faces": len(faces)}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "object_name": name,
        "object_type": "custom_mesh",
        "vertex_count": len(vertices),
        "face_count": len(faces),
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def extrude_face(object_name: str, face_index: int, distance: float = 1.0) -> Dict[str, Any]:
    """Extrude a face of an object.
    
    Args:
        object_name: Name of the object to modify
        face_index: Index of the face to extrude
        distance: Distance to extrude
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'import bmesh',
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bm = bmesh.from_mesh(obj.data)',
        f'bm.faces.ensure_lookup_table()',
        f'face = bm.faces[{face_index}]',
        f'bmesh.ops.extrude_discrete_faces(bm, faces=[face])',
        f'bmesh.ops.translate(bm, vec=(0, 0, {distance}), verts=face.verts)',
        f'bm.to_mesh(obj.data)',
        f'bm.free()',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "extrude_face", "object": "{object_name}", "face_index": {face_index}, "distance": {distance}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "extrude_face",
        "object_name": object_name,
        "parameters": {"face_index": face_index, "distance": distance},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def inset_faces(object_name: str, thickness: float = 0.1, depth: float = 0.0) -> Dict[str, Any]:
    """Inset faces of an object.
    
    Args:
        object_name: Name of the object to modify
        thickness: Inset thickness
        depth: Inset depth
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'import bmesh',
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'bpy.ops.mesh.inset(thickness={thickness}, depth={depth})',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "inset_faces", "object": "{object_name}", "thickness": {thickness}, "depth": {depth}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "inset_faces",
        "object_name": object_name,
        "parameters": {"thickness": thickness, "depth": depth},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def bevel_edges(object_name: str, offset: float = 0.1, segments: int = 1) -> Dict[str, Any]:
    """Bevel edges of an object.
    
    Args:
        object_name: Name of the object to modify
        offset: Bevel offset distance
        segments: Number of bevel segments
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'bpy.ops.mesh.bevel(offset={offset}, segments={segments})',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "bevel_edges", "object": "{object_name}", "offset": {offset}, "segments": {segments}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "bevel_edges",
        "object_name": object_name,
        "parameters": {"offset": offset, "segments": segments},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def loop_cut(object_name: str, cuts: int = 1, smoothness: float = 0.0) -> Dict[str, Any]:
    """Add loop cuts to an object.
    
    Args:
        object_name: Name of the object to modify
        cuts: Number of cuts to add
        smoothness: Smoothness factor
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={{"number_cuts": {cuts}, "smoothness": {smoothness}}})',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'results.append({{"action": "loop_cut", "object": "{object_name}", "cuts": {cuts}, "smoothness": {smoothness}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "loop_cut",
        "object_name": object_name,
        "parameters": {"cuts": cuts, "smoothness": smoothness},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def scale_object(object_name: str, scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)) -> Dict[str, Any]:
    """Scale an object along different axes.
    
    Args:
        object_name: Name of the object to scale
        scale: Scale factors for (x, y, z) axes
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'obj.scale = {scale}',
        f'results.append({{"action": "scale_object", "object": "{object_name}", "scale": {scale}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "scale_object",
        "object_name": object_name,
        "parameters": {"scale": scale},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def rotate_object(object_name: str, rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Dict[str, Any]:
    """Rotate an object.
    
    Args:
        object_name: Name of the object to rotate
        rotation: Rotation in radians for (x, y, z) axes
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'import mathutils',
        f'obj = bpy.data.objects["{object_name}"]',
        f'obj.rotation_euler = {rotation}',
        f'results.append({{"action": "rotate_object", "object": "{object_name}", "rotation": {rotation}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "rotate_object",
        "object_name": object_name,
        "parameters": {"rotation": rotation},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def move_object(object_name: str, location: Tuple[float, float, float]) -> Dict[str, Any]:
    """Move an object to a new location.
    
    Args:
        object_name: Name of the object to move
        location: New location as (x, y, z)
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'obj.location = {location}',
        f'results.append({{"action": "move_object", "object": "{object_name}", "location": {location}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "move_object",
        "object_name": object_name,
        "parameters": {"location": location},
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }