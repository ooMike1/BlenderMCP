#!/usr/bin/env python3
"""
Cross-platform installer for Blender MCP Server
"""
import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return the result."""
    try:
        # Use list for command on all platforms
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("Installing Blender MCP Server...")
    print()
    
    # Step 1: Install dependencies
    print("Step 1: Installing Python dependencies...")
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    if success:
        print("[OK] Dependencies installed successfully")
    else:
        print("[ERROR] Failed to install dependencies")
        print(f"Error: {stderr}")
        return 1
    
    print()
    
    # Step 2: Test server
    print("Step 2: Testing server startup...")
    success, stdout, stderr = run_command(f"{sys.executable} main.py --test", check=False)
    if success and "configuration test passed" in stdout.lower():
        print("[OK] Server test passed!")
    else:
        print("[WARNING] Server test had issues. Check Blender installation.")
        print("The server may still work if Blender is properly installed.")
    
    print()
    
    # Step 3: Create configuration
    print("Step 3: Creating MCP configuration...")
    current_dir = Path.cwd()
    config = {
        "mcpServers": {
            "blender": {
                "command": sys.executable,
                "args": [str(current_dir / "main.py")],
                "env": {
                    "PYTHONPATH": str(current_dir)
                }
            }
        }
    }
    
    config_path = current_dir / "mcp_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"[OK] Configuration saved to: {config_path}")
    print()
    print("To use this server, add the configuration to your MCP client.")
    print(f"Server location: {current_dir}")
    
    print()
    print("Step 4: Installation complete!")
    print()
    print("Next steps:")
    print("1. Add the configuration to your MCP client")
    print("2. Restart your MCP client")
    print('3. Test with: "Create a red cube in Blender"')
    print()
    print("See setup_instructions.md for detailed setup guide.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())