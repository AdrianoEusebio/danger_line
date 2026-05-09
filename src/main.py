import sys
import os
from src.modules.mcp.server import start_server
from src.shared.logger import logger

def main():
    """Main entry point for Danger Line."""
    try:
        # Start the MCP Server
        start_server()
    except KeyboardInterrupt:
        logger.info("Danger Line stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
