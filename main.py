#!/usr/bin/env python3
"""
Main entry point for the Blender MCP Server
"""
import sys
import logging
import asyncio

# Set up logging to go to stderr so it doesn't interfere with MCP stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

def main():
    """Main entry point to run the MCP server."""
    try:
        logger = logging.getLogger(__name__)
        
        # Handle test mode
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            logger.info("Testing Blender MCP Server configuration...")
            from blender_integration import blender_manager
            try:
                # Try to find Blender
                blender_path = blender_manager._find_blender()
                logger.info(f"Blender found at: {blender_path}")
                print("Server configuration test passed")
                return
            except Exception as e:
                logger.error(f"Configuration test failed: {e}")
                print(f"Configuration test failed: {e}")
                sys.exit(1)
        
        # Import and run the MCP server
        from mcp_server import main as server_main
        asyncio.run(server_main())
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()