"""
Blender Python API integration module for MCP server
Handles Blender subprocess management and bpy operations
"""
import subprocess
import sys
import os
import tempfile
import json
from typing import Any, Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class BlenderManager:
    """Manages Blender subprocess and Python API interactions."""
    
    def __init__(self, blender_executable: Optional[str] = None):
        """Initialize Blender manager.
        
        Args:
            blender_executable: Path to Blender executable. If None, tries to find it.
        """
        self.blender_executable = blender_executable or self._find_blender()
        self.temp_dir = tempfile.mkdtemp(prefix="blender_mcp_")
        
    def _find_blender(self) -> str:
        """Try to find Blender executable in common locations."""
        common_paths = [
            "blender",  # In PATH
            r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe", 
            r"C:\Program Files\Blender Foundation\Blender\blender.exe",
            "/usr/bin/blender",
            "/Applications/Blender.app/Contents/MacOS/Blender"
        ]
        
        for path in common_paths:
            if os.path.exists(path) or subprocess.run(["where" if os.name == "nt" else "which", path], 
                                                     capture_output=True).returncode == 0:
                logger.info(f"Found Blender at: {path}")
                return path
                
        raise RuntimeError("Blender executable not found. Please install Blender or provide the path.")
    
    def execute_blender_script(self, script: str, blend_file: Optional[str] = None) -> Dict[str, Any]:
        """Execute a Python script in Blender and return results.
        
        Args:
            script: Python script to execute in Blender
            blend_file: Optional .blend file to load
            
        Returns:
            Dictionary with execution results
        """
        try:
            # Create temporary script file
            script_file = os.path.join(self.temp_dir, "temp_script.py")
            with open(script_file, "w") as f:
                f.write(script)
            
            # Build Blender command
            cmd = [self.blender_executable]
            
            if blend_file:
                cmd.append(blend_file)
            else:
                cmd.append("--background")  # Run without UI
                cmd.append("--factory-startup")  # Start with clean scene
            
            cmd.extend(["--python", script_file])
            
            # Execute Blender
            logger.info(f"Executing Blender command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Clean up temp script
            os.remove(script_file)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Blender script execution timed out",
                "timeout": True
            }
        except Exception as e:
            logger.error(f"Error executing Blender script: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_basic_script(self, operations: List[str]) -> str:
        """Create a basic Blender Python script with error handling.
        
        Args:
            operations: List of Python operations to perform
            
        Returns:
            Complete Python script string
        """
        script_template = '''
import bpy
import bmesh
import json
import sys
import traceback

def main():
    try:
        # Clear existing mesh objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        
        results = []
        
        {operations}
        
        # Success output
        print("BLENDER_MCP_SUCCESS:", json.dumps({{"success": True, "results": results}}))
        
    except Exception as e:
        error_info = {{
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }}
        print("BLENDER_MCP_ERROR:", json.dumps(error_info))
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        operations_code = "\n        ".join(operations)
        return script_template.format(operations=operations_code)
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory: {e}")

# Global Blender manager instance
blender_manager = BlenderManager()