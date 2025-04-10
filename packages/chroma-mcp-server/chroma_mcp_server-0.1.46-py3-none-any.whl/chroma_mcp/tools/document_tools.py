"""
Document management tools for ChromaDB operations.
"""

import time
import json
import logging

from typing import Dict, List, Optional, Any, Union, cast
from dataclasses import dataclass

from mcp import types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR

# Use relative imports
from ..utils.errors import ValidationError
from ..types import DocumentMetadata

from chromadb.errors import InvalidDimensionException

# --- Imports ---
import chromadb
import chromadb.errors as chroma_errors
from ..app import mcp
from ..utils import (
    get_logger,
    get_chroma_client,
    get_embedding_function
)
# REMOVE invalid validation imports
# from ..utils.validation import validate_collection_name, validate_document_ids, validate_metadata
# REMOVE invalid error imports (commented out or non-existent)
# from ..utils.errors import handle_chroma_error, is_collection_not_found_error, CollectionNotFoundError
# REMOVE invalid helper imports
# from ..utils.helpers import (
#     dict_to_text_content,
#     prepare_metadata_for_chroma,
#     process_chroma_results,
#     format_add_result,
#     format_update_result,
#     format_delete_result,
#     MAX_DOC_LENGTH_FOR_PEEK
# )

# --- Constants ---
# Existing constants...

# Get logger instance for this module
logger = get_logger("tools.document")

# --- Implementation Functions ---

@mcp.tool(name="chroma_add_documents", description="Add documents to a ChromaDB collection.")
async def _add_documents_impl(
    collection_name: str,
    documents: List[str],
    ids: Optional[List[str]] = None,
    metadatas: Optional[List[Dict]] = None,
    increment_index: Optional[bool] = None # Default changed to None
) -> types.CallToolResult:
    """Adds documents to the specified ChromaDB collection.

    Args:
        collection_name: The name of the collection to add documents to.
        documents: A list of strings, where each string is the content of a document.
        ids: An optional list of unique string IDs for each document. If not provided,
             ChromaDB will generate UUIDs. Must be the same length as 'documents'.
        metadatas: An optional list of dictionaries, where each dictionary contains
                   metadata for the corresponding document. Must be the same length
                   as 'documents'.
        increment_index: Whether to immediately index the added documents. Defaults to True.
                         Setting to False can speed up bulk additions but requires manual
                         index building later for querying.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        confirming the addition, typically including the number of items added.
        On error (e.g., collection not found, ID conflict, mismatched list lengths,
        validation error, unexpected issue), isError is True and content contains
        a TextContent object with an error message.
    """

    # Assign effective default if None
    effective_increment_index = True if increment_index is None else increment_index

    try:
        # Handle None defaults for lists
        effective_metadatas = metadatas if metadatas is not None else []
        effective_ids = ids if ids is not None else []
        
        # Input validation
        if not documents:
            raise ValidationError("No documents provided")
        if effective_metadatas and len(effective_metadatas) != len(documents):
            raise ValidationError("Number of metadatas must match number of documents")
        if effective_ids and len(effective_ids) != len(documents):
            raise ValidationError("Number of IDs must match number of documents")
        
        # Get or create collection
        client = get_chroma_client()
        collection = client.get_collection(
            name=collection_name,
            embedding_function=get_embedding_function()
        )
        
        # Generate IDs if not provided
        generated_ids = False
        final_ids = effective_ids
        if not final_ids:
            generated_ids = True
            current_count = collection.count() if effective_increment_index else 0
            timestamp = int(time.time())
            final_ids = [f"doc_{timestamp}_{current_count + i}" for i in range(len(documents))]
        
        # Prepare metadatas
        final_metadatas = effective_metadatas if effective_metadatas else None
        
        # Add documents
        collection.add(
            documents=documents,
            metadatas=final_metadatas,
            ids=final_ids
        )
        
        logger.info(f"Added {len(documents)} documents to collection '{collection_name}'. Indexing: {effective_increment_index}")
        result_data = {
            "status": "success",
            "added_count": len(documents),
            "collection_name": collection_name,
            "document_ids": final_ids,
            "ids_generated": generated_ids
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )
        
    except ValidationError as e:
        logger.warning(f"Validation error adding documents to '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except Exception as e:
        logger.error(f"Unexpected error adding documents to '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while adding documents to '{collection_name}'. Details: {str(e)}")]
        )

@mcp.tool(name="chroma_query_documents", description="Query documents in a ChromaDB collection using semantic search.")
async def _query_documents_impl(
    collection_name: str,
    query_texts: List[str],
    n_results: Optional[int] = None, # Default changed to None
    where: Optional[Dict] = None,
    where_document: Optional[Dict] = None,
    include: Optional[List[str]] = None
) -> types.CallToolResult:
    """Performs semantic search within a ChromaDB collection.

    Args:
        collection_name: The name of the collection to query.
        query_texts: A list of strings representing the search queries.
        n_results: The number of results to return for each query. Defaults to 10.
        where: An optional dictionary for filtering results based on metadata.
               Example: {"source": "test"}.
        where_document: An optional dictionary for filtering results based on document content.
                        Example: {"$contains": "search term"}.
        include: An optional list of fields to include in the results (e.g.,
                 ["metadatas", "documents", "distances"]). Defaults to ChromaDB's
                 standard return fields.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        representing the QueryResult (containing lists for ids, documents,
        metadatas, distances, etc., corresponding to each query).
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    # Assign effective default if None
    effective_n_results = 10 if n_results is None else n_results

    try:
        # Handle None defaults for dicts/lists
        effective_where = where if where is not None else None # Use None if empty for Chroma query
        effective_where_document = where_document if where_document is not None else None # Use None if empty
        effective_include = include if include is not None else []

        # Input validation (raises ValidationError)
        if not query_texts:
            raise ValidationError("No query texts provided")
        if effective_n_results <= 0:
            raise ValidationError("n_results must be a positive integer")

        # Validate include values if provided
        valid_includes = ["documents", "embeddings", "metadatas", "distances"]
        if effective_include and not all(item in valid_includes for item in effective_include):
            # Use the actual invalid items in the error message if possible
            invalid_items = [item for item in effective_include if item not in valid_includes]
            raise ValidationError(f"Invalid item(s) in include list: {invalid_items}. Valid items are: {valid_includes}")

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot query documents: Collection '{collection_name}' not found.")
                # Return the specific error for collection not found
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                # Re-raise other ValueErrors to be caught later if needed, 
                # or handle them as internal errors immediately.
                # For now, let's assume other ValueErrors here indicate a problem.
                logger.error(f"Value error getting collection '{collection_name}' for query: {e}", exc_info=True)
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}")]
                )
        # Catch potential non-ValueError exceptions during get_collection too
        except Exception as e:
            logger.error(f"Unexpected error getting collection '{collection_name}' for query: {e}", exc_info=True)
            return types.CallToolResult(
                 isError=True,
                 content=[types.TextContent(type="text", text=f"Tool Error: Failed to get collection '{collection_name}'. Details: {str(e)}")]
             )

        # Set default includes if list was empty
        final_include = effective_include if effective_include else ["documents", "metadatas", "distances"]

        # Query documents, handle query-specific errors
        try:
            results = collection.query(
                query_texts=query_texts,
                n_results=effective_n_results,
                where=effective_where, # Pass None if originally None/empty
                where_document=effective_where_document, # Pass None if originally None/empty
                include=final_include
            )
        except ValueError as e: # Catch errors from the query itself (e.g., bad filter)
            logger.error(f"Error executing query on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Query Error: {str(e)}")]
            )

        # Format results - Current logic seems reasonable
        formatted_results_list = []
        if results: # Ensure results is not None or empty
            num_queries = len(results.get("ids", []))
            for i in range(num_queries):
                query_text = query_texts[i] if i < len(query_texts) else "(Query text missing)"
                single_query_result = {
                    "query": query_text,
                    "matches": []
                }

                ids_for_query = results.get("ids", [])[i]
                if ids_for_query:
                    num_matches = len(ids_for_query)
                    for j in range(num_matches):
                        match = {"id": ids_for_query[j]}
                        
                        # Safely get results for each included field
                        distances_list = results.get("distances", [])
                        if "distances" in final_include and i < len(distances_list) and j < len(distances_list[i]):
                            match["distance"] = distances_list[i][j]
                        
                        documents_list = results.get("documents", [])
                        if "documents" in final_include and i < len(documents_list) and documents_list[i] and j < len(documents_list[i]):
                            match["document"] = documents_list[i][j]
                            
                        metadatas_list = results.get("metadatas", [])
                        if "metadatas" in final_include and i < len(metadatas_list) and metadatas_list[i] and j < len(metadatas_list[i]):
                            match["metadata"] = metadatas_list[i][j]
                            
                        embeddings_list = results.get("embeddings", [])
                        if "embeddings" in final_include and i < len(embeddings_list) and embeddings_list[i] and j < len(embeddings_list[i]):
                            match["embedding"] = embeddings_list[i][j]
                            
                        single_query_result["matches"].append(match)
                        
                formatted_results_list.append(single_query_result)
        
        # Success result
        result_data = {
            "results": formatted_results_list, # Use the list directly
            "total_queries": len(query_texts)
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error querying documents in '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except Exception as e:
        # Keep the generic exception handler for other unexpected errors
        logger.error(f"Unexpected error querying documents in '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while querying documents in '{collection_name}'. Details: {str(e)}")]
        )

@mcp.tool(name="chroma_get_documents", description="Get documents from a ChromaDB collection by ID or filter.")
async def _get_documents_impl(
    collection_name: str,
    ids: Optional[List[str]] = None,
    where: Optional[Dict] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    where_document: Optional[Dict] = None,
    include: Optional[List[str]] = None
) -> types.CallToolResult:
    """Retrieves documents from a collection by ID or using filters.

    Args:
        collection_name: The name of the collection to retrieve from.
        ids: An optional list of document IDs to retrieve. If provided, 'where' and
             'where_document' filters are typically ignored by ChromaDB.
        where: An optional dictionary for filtering documents based on metadata.
               Example: {"topic": "specific"}.
        limit: An optional integer limiting the number of documents returned when
               using 'where' or 'where_document' filters.
        offset: An optional integer specifying the starting offset when using filters.
        where_document: An optional dictionary for filtering documents based on content.
                        Example: {"$contains": "test"}.
        include: An optional list of fields to include in the results (e.g.,
                 ["metadatas", "documents"]).

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        representing the GetResult (containing lists for ids, documents,
        metadatas, etc.). If IDs are provided and some are not found, they
        will be omitted from the results without an error.
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    try:
        # Handle None defaults for dicts/lists
        effective_where = where if where is not None else None
        effective_where_document = where_document if where_document is not None else None
        effective_include = include if include is not None else []
        # Assign effective limit/offset for validation, pass original None to ChromaDB
        effective_limit_for_validation = limit
        effective_offset_for_validation = offset

        # Input validation
        if ids is None and where is None and where_document is None:
            raise ValidationError("Must provide either ids, where, or where_document")
        if ids and (where or where_document):
             logger.warning("Both ids and where/where_document provided; ChromaDB typically ignores filters when ids are given.")
             # Reset filters if IDs are present to match expected Chroma behavior
             effective_where = None
             effective_where_document = None

        # Validation for limit and offset using effective values
        if effective_limit_for_validation is not None and effective_limit_for_validation <= 0:
             raise ValidationError("limit must be a positive integer if provided")
        if effective_offset_for_validation is not None and effective_offset_for_validation < 0:
             raise ValidationError("offset must be non-negative if provided")

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot get documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                raise e # Re-raise other ValueErrors

        # Set default includes if empty
        final_include = effective_include if effective_include else ["documents", "metadatas"]

        # Get documents, handle errors
        try:
            results = collection.get(
                ids=ids if ids else None, # Pass None if list is empty/None
                where=effective_where,
                limit=limit, # Pass original limit (can be None)
                offset=offset, # Pass original offset (can be None)
                where_document=effective_where_document,
                include=final_include
            )
        except ValueError as e: # Catch errors from the get itself (e.g., bad filter)
            logger.error(f"Error executing get on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Get Error: {str(e)}")]
            )

        # Format results
        formatted_documents = []
        if results and results.get("ids"):
            ids_list = results["ids"]
            docs_list = results.get("documents") 
            metas_list = results.get("metadatas") 
            embeds_list = results.get("embeddings")
            
            for i, doc_id in enumerate(ids_list):
                doc = {"id": doc_id}
                # Check existence and index bounds before accessing
                if "documents" in final_include and docs_list is not None and i < len(docs_list):
                    doc["content"] = docs_list[i]
                if "metadatas" in final_include and metas_list is not None and i < len(metas_list):
                    doc["metadata"] = metas_list[i]
                if "embeddings" in final_include and embeds_list is not None and i < len(embeds_list):
                    doc["embedding"] = embeds_list[i]
                formatted_documents.append(doc)
        
        # Success result
        result_data = {
            "documents": formatted_documents,
            "retrieved_count": len(formatted_documents),
            "limit_used": limit, # Return original requested limit
            "offset_used": offset # Return original requested offset
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error getting documents from '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e: # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for get: {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while getting documents from '{collection_name}'. Details: {str(e)}")]
        )

@mcp.tool(name="chroma_update_documents", description="Update existing documents in a ChromaDB collection.")
async def _update_documents_impl(
    collection_name: str,
    ids: List[str],
    documents: Optional[List[str]] = None,
    metadatas: Optional[List[Dict]] = None
) -> types.CallToolResult:
    """Updates the content and/or metadata of existing documents.

    Args:
        collection_name: The name of the collection containing the documents.
        ids: A list of IDs for the documents to update.
        documents: An optional list of new document content strings. Must be the same
                   length as 'ids' if provided.
        metadatas: An optional list of new metadata dictionaries. Must be the same
                   length as 'ids' if provided.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        confirming the update, potentially indicating the number of documents affected.
        On error (e.g., collection not found, ID not found, mismatched list lengths,
        validation error, unexpected issue), isError is True and content contains
        a TextContent object with an error message.
    """

    try:
        # Handle None defaults for lists
        effective_documents = documents if documents is not None else []
        effective_metadatas = metadatas if metadatas is not None else []

        # Input validation (raises ValidationError)
        if not ids:
            raise ValidationError("List of document IDs (ids) is required for update")
        if not effective_documents and not effective_metadatas:
            raise ValidationError("Either documents or metadatas must be provided for update")
        if effective_documents and len(effective_documents) != len(ids):
            raise ValidationError("Number of documents must match number of IDs")
        if effective_metadatas and len(effective_metadatas) != len(ids):
            raise ValidationError("Number of metadatas must match number of IDs")

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot update documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                raise e # Re-raise other ValueErrors

        # Update documents, handle potential errors
        try:
            # Note: ChromaDB's update might not error if IDs don't exist, it just won't update them.
            # If strict error on non-existent ID is needed, a pre-check `get` would be required.
            collection.update(
                ids=ids,
                documents=effective_documents if effective_documents else None,
                metadatas=effective_metadatas if effective_metadatas else None
            )
        except ValueError as e: # Catch errors from update (e.g., invalid structure)
             # ChromaDB might raise ValueError if ID not found *during* update in some versions/cases
             # Check for common error patterns if they exist
             error_msg = f"ChromaDB Update Error: {str(e)}"
             if "does not exist" in str(e): # Example check
                 error_msg = f"ChromaDB Update Error: One or more specified IDs do not exist in collection '{collection_name}'. Details: {str(e)}"
             
             logger.error(f"Error updating documents in collection '{collection_name}': {e}", exc_info=True)
             return types.CallToolResult(
                 isError=True,
                 content=[types.TextContent(type="text", text=error_msg)]
             )
        except InvalidDimensionException as e:
            logger.error(f"Dimension error updating documents in '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Dimension Error: {str(e)}")]
            )

        logger.info(f"Attempted update for {len(ids)} documents in collection '{collection_name}'")
        
        # Success result (Note: update doesn't return which IDs were *actually* updated)
        result_data = {
            "status": "success",
            "processed_count": len(ids), # Count of IDs submitted for update
            "collection_name": collection_name,
            "document_ids_submitted": ids
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error updating documents in '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e: # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for update: {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error updating documents in '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while updating documents in '{collection_name}'. Details: {str(e)}")]
        )

@mcp.tool(name="chroma_delete_documents", description="Delete documents from a ChromaDB collection by ID or filter.")
async def _delete_documents_impl(
    collection_name: str,
    ids: Optional[List[str]] = None,
    where: Optional[Dict] = None,
    where_document: Optional[Dict] = None
) -> types.CallToolResult:
    """Deletes documents from a collection by ID or using filters.

    Note: Provide either 'ids' or filtering criteria ('where'/'where_document'), not both.

    Args:
        collection_name: The name of the collection to delete from.
        ids: An optional list of document IDs to delete.
        where: An optional dictionary for filtering documents to delete based on metadata.
               Example: {"source": "old_data"}.
        where_document: An optional dictionary for filtering documents to delete based on content.
                        Example: {"$contains": "to be deleted"}.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        containing the list of IDs that were actually deleted.
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    try:
        # Handle None defaults
        effective_ids = ids if ids is not None else []
        effective_where = where if where is not None else None # Use None for Chroma
        effective_where_document = where_document if where_document is not None else None # Use None for Chroma

        # Input validation: Must provide at least one condition (raises ValidationError)
        if not effective_ids and not effective_where and not effective_where_document:
            raise ValidationError("Either ids, where, or where_document must be provided for deletion")

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(
                name=collection_name,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot delete documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")]
                )
            else:
                raise e # Re-raise other ValueErrors

        # Delete documents, handle potential errors
        try:
            # `delete` returns a list of the IDs that were actually deleted
            deleted_ids_list = collection.delete(
                ids=effective_ids if effective_ids else None,
                where=effective_where, # Pass None if originally None/empty
                where_document=effective_where_document # Pass None if originally None/empty
            )
        except ValueError as e: # Catch errors from delete (e.g., bad filter)
            logger.error(f"Error executing delete on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Delete Error: {str(e)}")]
            )

        # Log based on input method, report actual deleted count
        deleted_count = len(deleted_ids_list) if deleted_ids_list else 0
        if effective_ids:
            logger.info(f"Attempted deletion by IDs in '{collection_name}'. Actually deleted {deleted_count} documents.")
        else:
             logger.info(f"Attempted deletion by filter in '{collection_name}'. Actually deleted {deleted_count} documents.")

        # Success result
        result_data = {
            "status": "success",
            "deleted_count": deleted_count,
            "collection_name": collection_name,
            "deleted_ids": deleted_ids_list if deleted_ids_list else [] # Return empty list if None
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error deleting documents from '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e: # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for delete: {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error deleting documents from '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while deleting documents from '{collection_name}'. Details: {str(e)}")]
        )
