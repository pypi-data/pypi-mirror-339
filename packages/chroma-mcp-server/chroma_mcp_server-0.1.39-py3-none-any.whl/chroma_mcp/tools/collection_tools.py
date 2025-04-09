"""
Collection management tools for ChromaDB operations.
"""

import json
import logging
import chromadb
from chromadb.api.client import ClientAPI
from chromadb.errors import InvalidDimensionException

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from chromadb.api.types import CollectionMetadata, GetResult, QueryResult
from chromadb.errors import InvalidDimensionException

from mcp import types
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError

from ..utils import (
    get_logger, 
    get_chroma_client, 
    get_embedding_function, 
    validate_input, 
    ValidationError, # Keep this if used
    ClientError, # Keep this if used
    ConfigurationError # Keep this if used
)
from ..utils.config import get_collection_settings, validate_collection_name

def _reconstruct_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Reconstructs the structured metadata (with 'settings') from ChromaDB's internal format."""
    if not metadata:
        return {}
    
    reconstructed = {}
    settings = {}
    for key, value in metadata.items():
        setting_key_to_store = None
        # Check for flattened setting keys
        if key.startswith("chroma:setting:"):
            # Convert 'chroma_setting_hnsw_space' back to 'hnsw:space'
            original_key = key[len("chroma:setting:"):].replace('_', ':')
            setting_key_to_store = original_key
        # Also recognize common raw keys like hnsw:*
        elif key.startswith("hnsw:"):
            setting_key_to_store = key
        
        if setting_key_to_store:
            settings[setting_key_to_store] = value
        # Explicitly check for 'description' as it's handled separately
        elif key == 'description':
            reconstructed[key] = value
        # Store other keys directly (custom user keys)
        elif not key.startswith("chroma:"): # Avoid other potential internal chroma keys
            reconstructed[key] = value
    
    if settings:
        reconstructed["settings"] = settings
        
    return reconstructed

# --- Implementation Functions ---

async def _create_collection_impl(collection_name: str, metadata: Dict[str, Any] = None) -> types.CallToolResult:
    """Implementation logic for creating a collection."""
    logger = get_logger("tools.collection")

    try:
        validate_collection_name(collection_name)
        client = get_chroma_client()
        
        metadata_to_use = None
        log_msg_suffix = ""
        if metadata is not None:
            if not isinstance(metadata, dict):
                # Return MCP-compliant error for validation failure
                logger.warning(f"Invalid metadata type provided for create_collection: {type(metadata)}")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text="Tool Error: metadata parameter, if provided, must be a dictionary.")]
                )
            metadata_to_use = metadata
            log_msg_suffix = "with provided metadata."
        else:
            metadata_to_use = get_collection_settings()
            log_msg_suffix = "with default settings."

        # Explicitly set get_or_create to False to ensure DuplicateCollectionError is raised
        collection = client.create_collection(
            name=collection_name,
            metadata=metadata_to_use,
            embedding_function=get_embedding_function(),
            get_or_create=False
        )
        logger.info(f"Created collection: {collection_name} {log_msg_suffix}")
        count = collection.count()
        # Peek might be expensive, consider removing or making optional if performance is key
        peek_results = collection.peek(limit=5) # Limit peek for efficiency

        result_data = {
            "name": collection.name,
            "id": str(collection.id), # Ensure ID is string if it's UUID
            "metadata": _reconstruct_metadata(collection.metadata),
            "count": count,
            "sample_entries": peek_results # Use limited peek results
        }
        # Serialize success result to JSON
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error creating collection '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:
        # Check if the error message indicates a duplicate collection
        if f"Collection {collection_name} already exists." in str(e):
            logger.warning(f"Collection '{collection_name}' already exists.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' already exists.")]
            )
        else:
            # Handle other ValueErrors as likely invalid parameters
            logger.error(f"Validation error during collection creation '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Invalid parameter during collection creation. Details: {e}")]
            )
    except InvalidDimensionException as e: # Example of another specific Chroma error
        logger.error(f"Dimension error creating collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Error: Invalid dimension configuration. {str(e)}")]
        )
    except Exception as e:
        # Log the full unexpected error server-side
        logger.error(f"Unexpected error creating collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while creating collection '{collection_name}'. Details: {str(e)}")]
        )

async def _list_collections_impl(limit: int, offset: int, name_contains: str) -> types.CallToolResult:
    """Implementation logic for listing collections."""
    logger = get_logger("tools.collection")

    try:
        # Input validation
        if limit < 0:
            raise ValidationError("limit cannot be negative")
        if offset < 0:
            raise ValidationError("offset cannot be negative")
            
        client = get_chroma_client()
        # In ChromaDB v0.5+, list_collections returns Collection objects
        # We might need to adjust if upgrading, but for now assume names
        all_collections = client.list_collections()
        collection_names = [col.name for col in all_collections]
        
        # Safety check, though Chroma client should return a list of Collections
        if not isinstance(collection_names, list):
            logger.warning(f"client.list_collections() yielded unexpected structure, processing as empty list.")
            collection_names = []
            
        if name_contains:
            filtered_names = [name for name in collection_names if name_contains.lower() in name.lower()]
        else:
            filtered_names = collection_names
            
        total_count = len(filtered_names)
        start_index = offset
        # Apply limit only if it's positive; 0 means no limit
        end_index = (start_index + limit) if limit > 0 else len(filtered_names)
        paginated_names = filtered_names[start_index:end_index]
        
        result_data = {
            "collection_names": paginated_names,
            "total_count": total_count,
            "limit": limit, # Return the requested limit
            "offset": offset # Return the requested offset
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )
        
    except ValidationError as e:
        logger.warning(f"Validation error listing collections: {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    # Catch other potential ChromaDB or client connection errors if necessary
    # except SomeChromaError as e: ... return CallToolResult(isError=True, ...)
    except Exception as e:
        logger.error(f"Unexpected error listing collections: {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while listing collections. Details: {str(e)}")]
        )

async def _get_collection_impl(collection_name: str) -> types.CallToolResult:
    """Implementation logic for getting collection info."""
    logger = get_logger("tools.collection")

    try:
        client = get_chroma_client()
        # get_collection raises ValueError if not found
        collection = client.get_collection(
            name=collection_name,
            embedding_function=get_embedding_function()
        )
        count = collection.count()
        # Limit peek results
        peek_results = collection.peek(limit=5) 

        result_data = {
            "name": collection.name,
            "id": str(collection.id), # Ensure ID is string
            "metadata": _reconstruct_metadata(collection.metadata),
            "count": count,
            "sample_entries": peek_results
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )
        
    except ValueError as e:
        # ChromaDB often raises ValueError for not found
        logger.warning(f"Error getting collection '{collection_name}': {e}")
        # Check if the error message indicates "not found"
        if f"Collection {collection_name} does not exist." in str(e):
            error_msg = f"ChromaDB Error: Collection '{collection_name}' not found."
        else:
             # Keep the original ValueError message if it's something else
            error_msg = f"ChromaDB Value Error: {str(e)}"
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=error_msg)]
        )
    except Exception as e:
        logger.error(f"Unexpected error getting collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while getting collection '{collection_name}'. Details: {str(e)}")]
        )

async def _set_collection_description_impl(collection_name: str, description: str) -> types.CallToolResult:
    """Implementation logic for setting collection description."""
    logger = get_logger("tools.collection")

    try:
        client = get_chroma_client()

        # Try to get the collection first, handle not found error
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
             # Check if it's the specific "not found" error
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot set description: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors to be caught by the generic handler below
                raise e

        # Check for immutable settings (example: hnsw)
        current_metadata = collection.metadata or {}
        if any(k.startswith("hnsw:") for k in current_metadata):
            logger.warning(f"Attempted to set description on collection '{collection_name}' with immutable settings.")
            # Return MCP-compliant error
            return types.CallToolResult( 
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: Cannot set description on collections with existing immutable settings (e.g., hnsw:*). Modify operation aborted.")]
            )

        # If no immutable settings, proceed with modify
        # Note: modify might raise its own errors, caught by generic Exception handler
        collection.modify(metadata={ "description": description })
        logger.info(f"Set description for collection: {collection_name}")

        # Return the updated collection info by calling the refactored get function
        return await _get_collection_impl(collection_name)

    except ValueError as e: # Catch ValueErrors re-raised from the inner try block
        logger.error(f"Value error during set description for '{collection_name}': {e}", exc_info=False) # No need for full trace here usually
        # It's likely not the "not found" error if it reached here
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error setting description for collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while setting description for '{collection_name}'. Details: {str(e)}")]
        )

async def _set_collection_settings_impl(collection_name: str, settings: Dict[str, Any]) -> types.CallToolResult:
    """Implementation logic for setting collection settings."""
    logger = get_logger("tools.collection")

    try:
        # Input validation for settings type
        if not isinstance(settings, dict):
            logger.warning(f"Invalid settings type provided for set_collection_settings: {type(settings)}")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: settings parameter must be a dictionary.")]
            )

        client = get_chroma_client()

        # Try to get the collection first, handle not found error
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
             # Check if it's the specific "not found" error
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot set settings: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors
                raise e

        # Check for immutable settings (existing hnsw:* keys in current metadata)
        current_metadata = collection.metadata or {}
        if any(k.startswith("hnsw:") for k in current_metadata):
            logger.warning(f"Attempted to set settings on collection '{collection_name}' with immutable settings.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: Cannot set settings on collections with existing immutable settings (e.g., hnsw:*). Modify operation aborted.")]
            )

        # Prepare metadata, preserving description and other custom keys
        current_metadata_safe = collection.metadata or {}
        preserved_metadata = { 
            k: v for k, v in current_metadata_safe.items() 
            # Keep description and any non-setting, non-hnsw keys
            if k == 'description' or (not k.startswith(("chroma:setting:", "hnsw:")))
        }
        # Format new settings keys correctly for storing
        formatted_settings = {f"chroma:setting:{k.replace(':', '_')}": v for k, v in settings.items()}
        # Combine preserved data with new flattened settings
        updated_metadata = {**preserved_metadata, **formatted_settings}
        
        # Modify the collection
        collection.modify(metadata=updated_metadata)
        logger.info(f"Set settings for collection: {collection_name}")

        # Return updated collection info by calling get_collection_impl
        # which will use _reconstruct_metadata
        return await _get_collection_impl(collection_name)

    except ValueError as e: # Catch ValueErrors re-raised from the inner try block
        logger.error(f"Value error during set settings for '{collection_name}': {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error setting settings for collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while setting settings for '{collection_name}'. Details: {str(e)}")]
        )

async def _update_collection_metadata_impl(collection_name: str, metadata_update: Dict[str, Any]) -> types.CallToolResult:
    """Implementation logic for updating collection metadata."""
    logger = get_logger("tools.collection")

    try:
        # Input validation for metadata_update type
        if not isinstance(metadata_update, dict):
            logger.warning(f"Invalid metadata_update type provided: {type(metadata_update)}")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: metadata_update parameter must be a dictionary.")]
            )
            
        # Input validation for reserved keys
        reserved_keys = ["description", "settings"]
        if any(key in reserved_keys or key.startswith(("chroma:setting:", "hnsw:")) for key in metadata_update):
            logger.warning(f"Attempted to update reserved/immutable keys via update_metadata: {list(metadata_update.keys())}")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: Cannot update reserved keys ('description', 'settings', 'chroma:setting:...', 'hnsw:...') via this tool. Use dedicated tools or recreate the collection.")]
            )
            
        client = get_chroma_client()

        # Try to get the collection first, handle not found error
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
             # Check if it's the specific "not found" error
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot update metadata: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors
                raise e

        # Check for immutable settings (hnsw:*) again
        current_metadata = collection.metadata or {}
        if any(k.startswith("hnsw:") for k in current_metadata):
            logger.warning(f"Attempted to update metadata on collection '{collection_name}' with immutable settings.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Tool Error: Cannot update metadata on collections with existing immutable settings (e.g., hnsw:*). Modify operation aborted.")]
            )

        # Merge metadata: Start with existing, then update with new keys
        current_metadata_safe = collection.metadata or {}
        merged_metadata = current_metadata_safe.copy()
        # Only add/update keys from metadata_update (don't overwrite description/settings)
        for key, value in metadata_update.items():
            # Double-check against reserved keys just in case
            if key != 'description' and not key.startswith(("chroma:setting:", "hnsw:")):
                 merged_metadata[key] = value
            else:
                 logger.warning(f"Skipping attempt to update reserved key '{key}' via update_metadata in collection '{collection_name}'")

        # Modify the collection
        collection.modify(metadata=merged_metadata)
        logger.info(f"Updated custom metadata for collection: {collection_name}")

        # Return updated collection info
        return await _get_collection_impl(collection_name)

    except ValueError as e: # Catch ValueErrors re-raised from the inner try block
        logger.error(f"Value error during update metadata for '{collection_name}': {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error updating metadata for collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while updating metadata for '{collection_name}'. Details: {str(e)}")]
        )

async def _rename_collection_impl(collection_name: str, new_name: str) -> types.CallToolResult:
    """Implementation logic for renaming a collection."""
    logger = get_logger("tools.collection")

    try:
        # 1. Validate the new name first
        try:
            validate_collection_name(new_name)
        except ValidationError as e:
            logger.warning(f"Invalid new collection name provided for rename: '{new_name}'. Error: {e}")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Validation Error: Invalid new collection name '{new_name}'. {str(e)}")]
            )

        client = get_chroma_client()

        # 2. Get the original collection, handle not found
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot rename: Original collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Original collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors from get_collection
                raise e

        # 3. Attempt the rename via modify, handle potential errors (like new_name exists)
        try:
            collection.modify(name=new_name)
            logger.info(f"Renamed collection '{collection_name}' to '{new_name}'")
        except ValueError as e: # ChromaDB might raise ValueError if new_name exists or is invalid
            logger.warning(f"Failed to rename collection '{collection_name}' to '{new_name}': {e}")
            # Check common error messages if possible, otherwise provide generic
            error_msg = f"ChromaDB Error: Failed to rename to '{new_name}'. It might already exist or be invalid. Details: {str(e)}"
            if "already exists" in str(e).lower():
                 error_msg = f"ChromaDB Error: Cannot rename to '{new_name}' because a collection with that name already exists."
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=error_msg)]
            )

        # 4. On success, return the info for the collection under its NEW name
        return await _get_collection_impl(new_name)

    except ValueError as e: # Catch ValueErrors re-raised from the get_collection block
        logger.error(f"Value error during rename for '{collection_name}' -> '{new_name}': {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting original collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error renaming collection '{collection_name}' to '{new_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while renaming collection '{collection_name}'. Details: {str(e)}")]
        )

async def _delete_collection_impl(collection_name: str) -> types.CallToolResult:
    """Implementation logic for deleting a collection."""
    logger = get_logger("tools.collection")

    try:
        client = get_chroma_client()
        
        # delete_collection raises ValueError if collection doesn't exist
        try:
            client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection: {collection_name}")
            
            # Return success message
            result_data = {"status": "deleted", "collection_name": collection_name}
            result_json = json.dumps(result_data)
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=result_json)]
            )
        except ValueError as e:
            # Check if the error is specifically "not found"
            if f"Collection {collection_name} not found" in str(e):
                logger.warning(f"Attempted to delete non-existent collection: {collection_name}")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found, cannot delete.")]
                )
            else:
                # Handle other potential ValueErrors from delete_collection
                logger.error(f"ValueError deleting collection '{collection_name}': {e}", exc_info=True)
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"ChromaDB Value Error: {str(e)}")]
                )
                
    except Exception as e:
        logger.error(f"Unexpected error deleting collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while deleting collection '{collection_name}'. Details: {str(e)}")]
        )

async def _peek_collection_impl(collection_name: str, limit: int) -> types.CallToolResult:
    """Implementation logic for peeking into a collection."""
    logger = get_logger("tools.collection")

    # Ensure limit is sensible, although schema should enforce >= 1
    limit = max(1, limit) if limit is not None else 10 # Default to 10 if None, ensure at least 1

    try:
        client = get_chroma_client()

        # 1. Get the collection, handle not found
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot peek: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors from get_collection
                raise e

        # 2. Perform the peek operation
        try:
            peek_results = collection.peek(limit=limit)
            logger.info(f"Peeked {len(peek_results.get('ids', []))} items from collection: {collection_name}")
            # Serialize peek results to JSON
            result_json = json.dumps(peek_results, indent=2)
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=result_json)]
            )
        except ValueError as e: # Catch potential errors from peek itself (e.g., invalid limit if not caught by schema)
            logger.warning(f"ValueError during peek for collection '{collection_name}' with limit={limit}: {e}")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Value Error during peek: {str(e)}")]
            )
            
    except ValueError as e: # Catch ValueErrors re-raised from the get_collection block
        logger.error(f"Value error getting collection for peek '{collection_name}': {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error peeking collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while peeking collection '{collection_name}'. Details: {str(e)}")]
        )

# --- Tool Registration ---

class CreateCollectionTool(types.Tool): # Inherit from mcp.types.Tool
    """
        Create a new ChromaDB collection with specific or default settings.
        If `metadata` is provided, it overrides the default settings (e.g., HNSW parameters). 
        If `metadata` is None or omitted, default settings are used. 
        Use other tools like 'set_collection_description' to modify mutable metadata later.

        Args:
            collection_name: Name of the collection to create
            metadata: Optional dictionary of metadata to associate with the collection at creation. 
                      Can include custom key-values and settings like {{"hnsw:space": "cosine"}}. # Escaped curly braces

        Returns:
            Dictionary containing basic collection information
        """
    collection_name: str
    metadata: Optional[Dict[str, Any]] = None

    # Updated _call_impl signature and logic
    async def _call_impl(self) -> types.CallToolResult:
        # The _impl function now handles errors and returns CallToolResult
        return await _create_collection_impl(
            collection_name=self.collection_name,
            metadata=self.metadata
        )

class ListCollectionsTool(types.Tool):
    """
        List all collections with optional filtering and pagination.
        
        Args:
            limit: Maximum number of collections to return (0 for no limit)
            offset: Number of collections to skip (0 for no offset)
            name_contains: Filter collections by name substring (empty string for no filter)
            
        Returns:
            Dictionary containing list of collection names and total count
        """
    limit: Optional[int] = 0
    offset: Optional[int] = 0
    name_contains: Optional[str] = ""

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        # Directly await and return the result from the implementation function
        return await _list_collections_impl(
            limit=self.limit,
            offset=self.offset,
            name_contains=self.name_contains
        )

class GetCollectionTool(types.Tool):
    """
        Get information about a specific collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary containing collection information
        """
    collection_name: str

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _get_collection_impl(collection_name=self.collection_name)

class SetCollectionDescriptionTool(types.Tool):
    """
        Sets or updates the description of a collection.

        Args:
            collection_name: Name of the collection to modify
            description: The new description string

        Returns:
            Dictionary containing updated collection information
        """
    collection_name: str
    description: str
    
    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _set_collection_description_impl(
            collection_name=self.collection_name,
            description=self.description
        )

class SetCollectionSettingsTool(types.Tool):
    """
        Sets or updates the settings (e.g., HNSW parameters) of a collection.
        Warning: This replaces the existing 'settings' sub-dictionary in the metadata.
        IMPORTANT: This tool will FAIL if the target collection currently has immutable settings 
        (e.g., 'hnsw:space') defined in its metadata, as ChromaDB prevents modification in such cases.
        Collection settings must be finalized at creation.

        Args:
            collection_name: Name of the collection to modify
            settings: Dictionary containing the new settings (e.g., {{"hnsw:space": "cosine"}}) # Escaped

        Returns:
            Dictionary containing updated collection information
        """
    collection_name: str
    settings: Dict[str, Any]

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _set_collection_settings_impl(
            collection_name=self.collection_name,
            settings=self.settings
        )

class UpdateCollectionMetadataTool(types.Tool):
    """
        Updates or adds custom key-value pairs to a collection's metadata.
        Warning: This REPLACES the entire existing custom metadata block with the provided `metadata_update`.
        It does NOT affect the reserved 'description' or 'settings' keys directly.
        IMPORTANT: This tool will FAIL if the target collection currently has immutable settings 
        (e.g., 'hnsw:space') defined in its metadata, as ChromaDB prevents modification in such cases.
        Set all custom metadata during collection creation if immutable settings are used.

        Args:
            collection_name: Name of the collection to modify
            metadata_update: Dictionary containing key-value pairs to update or add

        Returns:
            Dictionary containing updated collection information
        """
    collection_name: str
    metadata_update: Dict[str, Any]

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _update_collection_metadata_impl(
            collection_name=self.collection_name,
            metadata_update=self.metadata_update
        )

class RenameCollectionTool(types.Tool):
    """
        Renames an existing collection.

        Args:
            collection_name: Current name of the collection
            new_name: New name for the collection

        Returns:
            Dictionary containing updated collection information (under the new name)
        """
    collection_name: str
    new_name: str

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _rename_collection_impl(
            collection_name=self.collection_name,
            new_name=self.new_name
        )

class DeleteCollectionTool(types.Tool):
    """
        Delete a collection.
        
        Args:
            collection_name: Name of the collection to delete
            
        Returns:
            Dictionary containing deletion status
        """
    collection_name: str

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _delete_collection_impl(collection_name=self.collection_name)

class PeekCollectionTool(types.Tool):
    """
        Peek at the first few entries in a collection.

        Args:
            collection_name: Name of the collection
            limit: Maximum number of entries to return (default: 10)

        Returns:
            Dictionary containing the peek results
        """
    collection_name: str
    limit: Optional[int] = 10

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _peek_collection_impl(
            collection_name=self.collection_name,
            limit=self.limit
        )

async def register_collection_tools(mcp: FastMCP) -> None:
    """Register collection management tools with the MCP server."""
    
    # Register using the Tool class types
    mcp.register_tool_type(CreateCollectionTool)
    mcp.register_tool_type(ListCollectionsTool)
    mcp.register_tool_type(GetCollectionTool)
    mcp.register_tool_type(SetCollectionDescriptionTool)
    mcp.register_tool_type(SetCollectionSettingsTool)
    mcp.register_tool_type(UpdateCollectionMetadataTool)
    mcp.register_tool_type(RenameCollectionTool)
    mcp.register_tool_type(DeleteCollectionTool)
    mcp.register_tool_type(PeekCollectionTool)

    logger = logging.getLogger("chroma_mcp.tools.collection")
    logger.info("Registered collection management tools.")
