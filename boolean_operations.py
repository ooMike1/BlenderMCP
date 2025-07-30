"""
Boolean operations and complex modeling tools
"""
from typing import Any, Dict, List, Optional, Tuple
import logging
from blender_integration import blender_manager

logger = logging.getLogger(__name__)

def boolean_union(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean union operation between two objects.
    
    Args:
        object1_name: Name of the first object
        object2_name: Name of the second object  
        result_name: Name for the resulting object
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj1 = bpy.data.objects["{object1_name}"]',
        f'obj2 = bpy.data.objects["{object2_name}"]',
        f'bpy.context.view_layer.objects.active = obj1',
        f'modifier = obj1.modifiers.new(name="BooleanUnion", type="BOOLEAN")',
        f'modifier.operation = "UNION"',
        f'modifier.object = obj2',
        f'bpy.ops.object.modifier_apply(modifier="BooleanUnion")',
        f'obj1.name = "{result_name}"',
        f'bpy.data.objects.remove(obj2, do_unlink=True)',
        f'results.append({{"action": "boolean_union", "result_object": "{result_name}", "input_objects": ["{object1_name}", "{object2_name}"]}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "boolean_union",
        "result_object": result_name,
        "input_objects": [object1_name, object2_name],
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def boolean_difference(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean difference operation (subtract object2 from object1).
    
    Args:
        object1_name: Name of the base object
        object2_name: Name of the object to subtract
        result_name: Name for the resulting object
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj1 = bpy.data.objects["{object1_name}"]',
        f'obj2 = bpy.data.objects["{object2_name}"]',
        f'bpy.context.view_layer.objects.active = obj1',
        f'modifier = obj1.modifiers.new(name="BooleanDifference", type="BOOLEAN")',
        f'modifier.operation = "DIFFERENCE"',
        f'modifier.object = obj2',
        f'bpy.ops.object.modifier_apply(modifier="BooleanDifference")',
        f'obj1.name = "{result_name}"',
        f'bpy.data.objects.remove(obj2, do_unlink=True)',
        f'results.append({{"action": "boolean_difference", "result_object": "{result_name}", "base_object": "{object1_name}", "subtract_object": "{object2_name}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "boolean_difference", 
        "result_object": result_name,
        "base_object": object1_name,
        "subtract_object": object2_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def boolean_intersection(object1_name: str, object2_name: str, result_name: str = "BooleanResult") -> Dict[str, Any]:
    """Perform boolean intersection operation between two objects.
    
    Args:
        object1_name: Name of the first object
        object2_name: Name of the second object
        result_name: Name for the resulting object
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj1 = bpy.data.objects["{object1_name}"]',
        f'obj2 = bpy.data.objects["{object2_name}"]',
        f'bpy.context.view_layer.objects.active = obj1',
        f'modifier = obj1.modifiers.new(name="BooleanIntersect", type="BOOLEAN")',
        f'modifier.operation = "INTERSECT"',
        f'modifier.object = obj2',
        f'bpy.ops.object.modifier_apply(modifier="BooleanIntersect")',
        f'obj1.name = "{result_name}"',
        f'bpy.data.objects.remove(obj2, do_unlink=True)',
        f'results.append({{"action": "boolean_intersection", "result_object": "{result_name}", "input_objects": ["{object1_name}", "{object2_name}"]}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "boolean_intersection",
        "result_object": result_name,
        "input_objects": [object1_name, object2_name],
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def duplicate_object(object_name: str, new_name: str = None, offset: Tuple[float, float, float] = (0, 0, 0)) -> Dict[str, Any]:
    """Duplicate an object.
    
    Args:
        object_name: Name of the object to duplicate
        new_name: Name for the duplicated object (auto-generated if None)
        offset: Offset position for the duplicate
    
    Returns:
        Dictionary with operation result
    """
    if new_name is None:
        new_name = f"{object_name}_Copy"
    
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'new_obj = obj.copy()',
        f'new_obj.data = obj.data.copy()',
        f'new_obj.name = "{new_name}"',
        f'new_obj.location = (obj.location.x + {offset[0]}, obj.location.y + {offset[1]}, obj.location.z + {offset[2]})',
        f'bpy.context.collection.objects.link(new_obj)',
        f'results.append({{"action": "duplicate_object", "original": "{object_name}", "duplicate": "{new_name}", "offset": {offset}}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "duplicate_object",
        "original_object": object_name,
        "duplicate_object": new_name,
        "offset": offset,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def join_objects(object_names: List[str], result_name: str = "JoinedObject") -> Dict[str, Any]:
    """Join multiple objects into one.
    
    Args:
        object_names: List of object names to join
        result_name: Name for the joined object
    
    Returns:
        Dictionary with operation result
    """
    if len(object_names) < 2:
        return {
            "success": False,
            "error": "At least 2 objects required for joining"
        }
    
    objects_list = ', '.join([f'bpy.data.objects["{name}"]' for name in object_names])
    
    operations = [
        f'objects_to_join = [{objects_list}]',
        f'bpy.ops.object.select_all(action="DESELECT")',
        f'for obj in objects_to_join:',
        f'    obj.select_set(True)',
        f'bpy.context.view_layer.objects.active = objects_to_join[0]',
        f'bpy.ops.object.join()',
        f'bpy.context.active_object.name = "{result_name}"',
        f'results.append({{"action": "join_objects", "input_objects": {object_names}, "result_object": "{result_name}"}})' 
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "join_objects",
        "input_objects": object_names,
        "result_object": result_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }

def separate_object_by_loose_parts(object_name: str) -> Dict[str, Any]:
    """Separate an object into loose parts.
    
    Args:
        object_name: Name of the object to separate
    
    Returns:
        Dictionary with operation result
    """
    operations = [
        f'obj = bpy.data.objects["{object_name}"]',
        f'bpy.context.view_layer.objects.active = obj',
        f'bpy.ops.object.mode_set(mode="EDIT")',
        f'bpy.ops.mesh.select_all(action="SELECT")',
        f'bpy.ops.mesh.separate(type="LOOSE")',
        f'bpy.ops.object.mode_set(mode="OBJECT")',
        f'separated_objects = [obj.name for obj in bpy.context.selected_objects]',
        f'results.append({{"action": "separate_loose_parts", "original_object": "{object_name}", "separated_objects": separated_objects}})'
    ]
    
    script = blender_manager.create_basic_script(operations)
    result = blender_manager.execute_blender_script(script)
    
    return {
        "success": result["success"],
        "action": "separate_loose_parts",
        "original_object": object_name,
        "blender_output": result.get("stdout", ""),
        "errors": result.get("stderr", "") if not result["success"] else None
    }