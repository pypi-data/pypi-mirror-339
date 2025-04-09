"""
Chroma MCP Server - Main Implementation

This module provides the core server implementation for the Chroma MCP service,
integrating ChromaDB with the Model Context Protocol (MCP).
"""

import os
import argparse
import importlib.metadata
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import logging
import logging.handlers # Add this for FileHandler
import sys # Import sys for stderr output as last resort

from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError

# Import ThoughtMetadata from .types
# Import ChromaClientConfig now also from .types
from .types import ThoughtMetadata, ChromaClientConfig 
# Import config loading and tool registration
from .utils.config import load_config
from .tools.collection_tools import register_collection_tools
from .tools.document_tools import register_document_tools
from .tools.thinking_tools import register_thinking_tools
# Import errors and specific utils (setters/getters for globals)
from .utils import (
    get_logger, 
    set_main_logger, 
    get_server_config, # Keep getter for potential internal use
    set_server_config, 
    BASE_LOGGER_NAME, 
    validate_input, 
    # raise_validation_error # Keep these if used directly in server?
)

# Add this near the top of the file, after imports but before any other code
CHROMA_AVAILABLE = False
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    # Use logger if available later, print is too early here
    # We will log this warning properly within config_server
    pass

FASTMCP_AVAILABLE = False
try:
    import fastmcp
    FASTMCP_AVAILABLE = True
except ImportError:
    # Use logger if available later, print is too early here
    # We will log this warning properly within config_server
    pass

# Initialize logger - will be properly configured in config_server
# logger = None # Removed: Managed via get_logger/set_main_logger in utils

# Add a base logger name
# BASE_LOGGER_NAME = "chromamcp" # Removed: Moved to utils

# Remove handler initializations and related global variables
# _collection_handler = None
# _document_handler = None
# _thinking_handler = None
_mcp_instance = None

# Add this near the top with other globals
# _global_client_config: Optional[ChromaClientConfig] = None # Removed: Moved to utils

# Add the get_logger function here
# _main_logger_instance = None # Removed: Moved to utils

def _initialize_mcp_instance():
    """Helper to initialize MCP and register tools."""
    global _mcp_instance
    # Get the configured logger instance
    logger = get_logger() # Use getter from utils

    if _mcp_instance is not None:
        return _mcp_instance
        
    try:
        mcp = FastMCP("chroma")
        
        # Register main tool categories
        register_collection_tools(mcp)
        register_document_tools(mcp)
        register_thinking_tools(mcp)
        
        # Register server utility tools
        @mcp.tool(name="chroma_get_server_version")
        def get_version_tool() -> Dict[str, str]:
             """Return the installed version of the chroma-mcp-server package."""
             try:
                 version = importlib.metadata.version('chroma-mcp-server')
                 return {"package": "chroma-mcp-server", "version": version}
             except importlib.metadata.PackageNotFoundError:
                 return {"package": "chroma-mcp-server", "version": "unknown (not installed)"}
             except Exception as e:
                 if logger:
                      logger.error(f"Error getting server version: {str(e)}")
                 return {"package": "chroma-mcp-server", "version": f"error ({str(e)})"}

        if logger:
            logger.debug("Successfully initialized and registered MCP tools")
        _mcp_instance = mcp
        return mcp
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to initialize MCP: {str(e)}")
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=f"Failed to initialize MCP: {str(e)}"
        ))

def get_mcp() -> FastMCP:
    """Get the initialized FastMCP instance."""
    if _mcp_instance is None:
        _initialize_mcp_instance()
    if _mcp_instance is None:
        # Should not happen if _initialize_mcp_instance raises correctly
        raise McpError(ErrorData(code=INTERNAL_ERROR, message="MCP instance is None after initialization attempt"))
    return _mcp_instance

def config_server(args: argparse.Namespace) -> None:
    """
    Configure the server with the provided configuration.
    
    Args:
        args: Parsed command line arguments
        
    Raises:
        McpError: If configuration fails
    """
    # global _main_logger_instance, _global_client_config # Removed globals

    logger = None # Initialize logger to None before try block
    try:
        # Load environment variables if dotenv file exists
        if args.dotenv_path and os.path.exists(args.dotenv_path):
            load_dotenv(dotenv_path=args.dotenv_path)
        
        # --- Start: Logger Configuration --- 
        log_dir = args.log_dir
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        # Get the root logger for our application
        logger = logging.getLogger(BASE_LOGGER_NAME)
        logger.setLevel(log_level)

        # Prevent adding handlers multiple times if config_server is called again (e.g., in tests)
        if not logger.hasHandlers():
            # Create formatter
            formatter = logging.Formatter(
                f'%(asctime)s | %(name)-{len(BASE_LOGGER_NAME)+15}s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # Create file handler if log_dir is specified
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, "chroma_mcp_server.log")
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=10*1024*1024, # 10 MB
                    backupCount=5
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        # Store the configured logger instance globally via setter
        # _main_logger_instance = logger # Removed
        set_main_logger(logger)
        # --- End: Logger Configuration ---

        # Get the logger instance for use within *this* function scope
        # logger = get_logger() # This is redundant now, logger is already assigned above
        
        # Handle CPU provider setting
        use_cpu_provider = None  # Auto-detect
        if args.cpu_execution_provider != 'auto':
            use_cpu_provider = args.cpu_execution_provider == 'true'
        
        # Create client configuration
        client_config = ChromaClientConfig(
            client_type=args.client_type,
            data_dir=args.data_dir,
            host=args.host,
            port=args.port,
            ssl=args.ssl,
            tenant=args.tenant,
            database=args.database,
            api_key=args.api_key,
            use_cpu_provider=use_cpu_provider
        )
        
        # Store the config globally via setter
        # _global_client_config = client_config # Removed
        set_server_config(client_config)

        # This will initialize our configurations for later use
        provider_status = 'auto-detected' if use_cpu_provider is None else ('enabled' if use_cpu_provider else 'disabled')
        logger.info(f"Server configured (CPU provider: {provider_status})")
        
        # Log the configuration details
        if log_dir:
            logger.info(f"Logs will be saved to: {log_dir}")
        if args.data_dir:
            logger.info(f"Data directory: {args.data_dir}")
        
        # Check for required dependencies
        if not CHROMA_AVAILABLE:
            logger.warning("ChromaDB is not installed. Vector database operations will not be available.")
            logger.warning("To enable full functionality, install the optional dependencies:")
            logger.warning("pip install chroma-mcp-server[full]")
        
        if not FASTMCP_AVAILABLE:
            logger.warning("FastMCP is not installed. MCP tools will not be available.")
            logger.warning("To enable full functionality, install the optional dependencies:")
            logger.warning("pip install chroma-mcp-server[full]")
            
    except Exception as e:
        # If logger isn't initialized yet, use print for critical errors
        error_msg = f"Failed to configure server: {str(e)}"
        if logger:
            # Use critical level for configuration failures
            logger.critical(error_msg) 
        else:
            # Last resort if logger setup failed completely
            print(f"CRITICAL CONFIG ERROR: {error_msg}", file=sys.stderr) 
        
        # Wrap the exception in McpError
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=error_msg
        ))

def main() -> None:
    """Entry point for the Chroma MCP server."""
    logger = None # Initialize logger variable for this scope
    try:
        # Configuration should already be done by the caller (cli.py)
        # No need to parse args here again.
        # parser = create_parser()
        # args = parser.parse_args()
        # config_server(args) # This is called by cli.py
        
        # Get the configured logger *after* config_server should have run
        logger = get_logger()
        
        # Ensure MCP instance is initialized (idempotent)
        mcp_instance = get_mcp() # Use get_mcp which calls _initialize_mcp_instance if needed
        
        if logger:
            try:
                 version = importlib.metadata.version('chroma-mcp-server')
            except importlib.metadata.PackageNotFoundError:
                 version = "unknown"
            logger.debug(
                "Starting Chroma MCP server (version: %s) with stdio transport", 
                version
            )
        
        # Start server with stdio transport using the initialized instance
        mcp_instance.run(transport='stdio')
        
    except McpError as e:
        if logger:
            logger.error(f"MCP Error: {str(e)}")
        raise
    except Exception as e:
        error_msg = f"Critical error running MCP server: {str(e)}"
        if logger:
            logger.error(error_msg)
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=error_msg
        ))

if __name__ == "__main__":
    main() 