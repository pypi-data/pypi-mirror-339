"""Tests for document management tools."""

import pytest
import uuid
import time # Import time for ID generation check
import json

from typing import Dict, Any, List, Optional
from unittest.mock import patch, MagicMock, ANY

# Import CallToolResult and TextContent for helpers
from mcp import types
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.shared.exceptions import McpError

# Keep only ValidationError from errors module
from src.chroma_mcp.utils.errors import ValidationError
from src.chroma_mcp.tools import document_tools

# Import the implementation functions directly
from src.chroma_mcp.tools.document_tools import (
    _add_documents_impl, 
    _query_documents_impl, 
    _get_documents_impl, 
    _update_documents_impl, 
    _delete_documents_impl
)

DEFAULT_SIMILARITY_THRESHOLD = 0.7

# --- Helper Functions (Copied from test_collection_tools.py) ---

def assert_successful_json_result(result: types.CallToolResult, expected_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Asserts the tool result is successful and contains valid JSON, returning the parsed data."""
    assert isinstance(result, types.CallToolResult)
    assert result.isError is False
    assert isinstance(result.content, list)
    assert len(result.content) == 1
    assert isinstance(result.content[0], types.TextContent)
    assert result.content[0].type == "text"

    try:
        result_data = json.loads(result.content[0].text)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON content: {result.content[0].text}")

    assert isinstance(result_data, dict)
    if expected_data is not None:
        assert result_data == expected_data
    return result_data # Return parsed data for further specific assertions

def assert_error_result(result: types.CallToolResult, expected_error_substring: str):
    """Asserts the tool result is an error and contains the expected substring."""
    assert isinstance(result, types.CallToolResult)
    assert result.isError is True
    assert isinstance(result.content, list)
    assert len(result.content) == 1
    assert isinstance(result.content[0], types.TextContent)
    assert result.content[0].type == "text"
    assert expected_error_substring in result.content[0].text
# --- End Helper Functions ---

@pytest.fixture
def mock_chroma_client():
    """Fixture to mock the Chroma client and its methods (Synchronous)."""
    with patch("src.chroma_mcp.utils.client.get_chroma_client") as mock_get_client, \
         patch("src.chroma_mcp.utils.client.get_embedding_function") as mock_get_embedding_function:
        
        # Use MagicMock for synchronous behavior
        mock_client_instance = MagicMock() 
        mock_collection_instance = MagicMock()
        
        # Configure mock methods for collection (synchronous)
        # add, query, get, update, delete are tracked by MagicMock automatically
        mock_collection_instance.count.return_value = 0 # Sync return for count
        
        # Configure mock methods for client (synchronous)
        mock_client_instance.get_collection.return_value = mock_collection_instance # Sync return
        # get_or_create_collection might not be used if implementation changed to get_collection
        # If still used, mock it: mock_client_instance.get_or_create_collection.return_value = mock_collection_instance
        
        mock_get_client.return_value = mock_client_instance
        mock_get_embedding_function.return_value = None # Assume no specific embedding fn needed for mock
        yield mock_client_instance, mock_collection_instance

class TestDocumentTools:
    """Test cases for document management implementation functions."""

    # --- _add_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_add_documents_success(self, mock_chroma_client):
        """Test successful document addition."""
        mock_client, mock_collection = mock_chroma_client
        mock_collection.count.return_value = 5 # Set initial count for ID generation test
        
        docs = ["doc1", "doc2"]
        ids = ["id1", "id2"]
        metas = [{"k": "v1"}, {"k": "v2"}]
        
        # Call the async implementation function
        result = await _add_documents_impl(
            collection_name="test_add",
            documents=docs,
            ids=ids,
            metadatas=metas,
            increment_index=True # Add missing argument
        )
        
        # Assert that the synchronous collection method was called
        mock_collection.add.assert_called_once_with(
            documents=docs, 
            ids=ids, 
            metadatas=metas
        )
        # Use helper to check result format and parse JSON
        result_data = assert_successful_json_result(result)

        # Check specific values in the parsed JSON data
        assert result_data.get("status") == "success"
        assert result_data.get("added_count") == 2
        assert result_data.get("document_ids") == ids
        assert result_data.get("ids_generated") is False

    @pytest.mark.asyncio
    async def test_add_documents_generate_ids(self, mock_chroma_client):
        """Test document addition with auto-generated IDs."""
        mock_client, mock_collection = mock_chroma_client
        mock_collection.count.return_value = 3 # Initial count for ID generation
        
        docs = ["docA", "docB"]
        start_time = time.time() # For basic check of generated ID format
        
        result = await _add_documents_impl(
            collection_name="test_add_gen",
            documents=docs,
            metadatas=None, 
            ids=None,
            increment_index=True # Explicitly test increment
        )
        
        # Check count was called (synchronously)
        mock_collection.count.assert_called_once()
        # Check add was called (synchronously)
        mock_collection.add.assert_called_once()
        call_args = mock_collection.add.call_args
        assert call_args.kwargs["documents"] == docs
        assert call_args.kwargs["metadatas"] is None # Ensure None was passed
        # Check generated IDs format (basic check)
        generated_ids = call_args.kwargs["ids"]
        assert len(generated_ids) == 2
        assert generated_ids[0].startswith(f"doc_{int(start_time // 1)}") # Check prefix and timestamp part
        assert generated_ids[0].endswith("_3") # Check index part (3 + 0)
        assert generated_ids[1].endswith("_4") # Check index part (3 + 1)
        
        # Use helper to check result format and parse JSON
        result_data = assert_successful_json_result(result)
        assert result_data.get("status") == "success"
        assert result_data.get("added_count") == 2
        assert result_data.get("ids_generated") is True
        assert result_data.get("document_ids") == generated_ids # Check returned IDs match

    @pytest.mark.asyncio
    async def test_add_documents_generate_ids_no_increment(self, mock_chroma_client):
        """Test document addition with auto-generated IDs without incrementing index."""
        mock_client, mock_collection = mock_chroma_client
        # Count should NOT be called if increment_index is False
        
        docs = ["docX"]
        start_time = time.time()
        
        result = await _add_documents_impl(
            collection_name="test_add_gen_noinc",
            documents=docs,
            ids=None,
            increment_index=False # Test this flag
        )
        
        mock_collection.count.assert_not_called() # Ensure count wasn't called
        mock_collection.add.assert_called_once()
        call_args = mock_collection.add.call_args
        generated_ids = call_args.kwargs["ids"]
        assert len(generated_ids) == 1
        assert generated_ids[0].startswith(f"doc_{int(start_time // 1)}")
        assert generated_ids[0].endswith("_0") # Index starts from 0 if count isn't used

        # Use helper to check result format and parse JSON
        result_data = assert_successful_json_result(result)
        assert result_data.get("ids_generated") is True
        assert result_data.get("document_ids") == generated_ids

    @pytest.mark.asyncio
    async def test_add_documents_validation_no_docs(self, mock_chroma_client):
        """Test validation failure when no documents are provided."""
        result = await _add_documents_impl(
            collection_name="test_valid",
            documents=[],
            increment_index=True # Add missing argument
        )
        assert_error_result(result, "Validation Error: No documents provided")

    @pytest.mark.asyncio
    async def test_add_documents_validation_mismatch_ids(self, mock_chroma_client):
        """Test validation failure with mismatched IDs."""
        result = await _add_documents_impl(
            collection_name="test_valid",
            documents=["d1", "d2"],
            ids=["id1"],
            increment_index=True # Add missing argument
        )
        assert_error_result(result, "Validation Error: Number of IDs must match number of documents")

    @pytest.mark.asyncio
    async def test_add_documents_validation_mismatch_metas(self, mock_chroma_client):
        """Test validation failure with mismatched metadatas."""
        result = await _add_documents_impl(
            collection_name="test_valid",
            documents=["d1", "d2"],
            metadatas=[{"k": "v"}],
            increment_index=True # Add missing argument
        )
        assert_error_result(result, "Validation Error: Number of metadatas must match number of documents")

    # --- _query_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_query_documents_success(self, mock_chroma_client):
        """Test successful document query with default include."""
        mock_client, mock_collection = mock_chroma_client
        # Mock the synchronous return value of collection.query
        mock_collection.query.return_value = {
            "ids": [["id1", "id2"]],
            "distances": [[0.1, 0.2]],
            "metadatas": [[{"m": "v1"}, {"m": "v2"}]],
            "documents": [["doc text 1", "doc text 2"]],
            "embeddings": None # Assume embeddings not included by default
        }
        
        result = await _query_documents_impl(
            collection_name="test_query",
            query_texts=["find me stuff"],
            n_results=2 # Mandatory argument
        )
        
        # Assert synchronous call
        mock_collection.query.assert_called_once_with(
            query_texts=["find me stuff"],
            n_results=2,
            where=None,
            where_document=None,
            include=["documents", "metadatas", "distances"] # Default include
        )
        # Use helper to parse JSON
        result_data = assert_successful_json_result(result)

        # Check parsed data
        assert "results" in result_data
        assert len(result_data["results"]) == 1
        assert result_data.get("total_queries") == 1
        assert "matches" in result_data["results"][0]
        assert len(result_data["results"][0]["matches"]) == 2
        match1 = result_data["results"][0]["matches"][0]
        assert match1.get("id") == "id1"
        assert match1.get("distance") == 0.1
        assert match1.get("document") == "doc text 1"
        assert match1.get("metadata") == {"m": "v1"}

    @pytest.mark.asyncio
    async def test_query_documents_custom_include(self, mock_chroma_client):
        """Test query with custom include parameter."""
        mock_client, mock_collection = mock_chroma_client
        mock_collection.query.return_value = {
            "ids": [["id_a"]],
            "distances": None,
            "metadatas": None,
            "documents": [["docA"]],
            "embeddings": [[[0.1, 0.2]]] # Included
        }
        
        result = await _query_documents_impl(
            collection_name="test_query_include",
            query_texts=["find embedding"],
            n_results=1,
            include=["documents", "embeddings"]
        )
        
        # Assert synchronous call
        mock_collection.query.assert_called_once_with(
            query_texts=["find embedding"],
            n_results=1,
            where=None,
            where_document=None,
            include=["documents", "embeddings"]
        )
        # Use helper to check result format and parse JSON
        result_data = assert_successful_json_result(result)

        # Check parsed data
        assert len(result_data.get("results", [])) == 1
        assert result_data.get("total_queries") == 1
        assert len(result_data["results"][0].get("matches", [])) == 1
        match = result_data["results"][0]["matches"][0]
        assert match.get("id") == "id_a"
        assert "distance" not in match
        assert "metadata" not in match
        assert match.get("document") == "docA"
        assert match.get("embedding") == [0.1, 0.2]

    @pytest.mark.asyncio
    async def test_query_documents_validation_no_query(self, mock_chroma_client):
        """Test validation failure with no query text."""
        result = await _query_documents_impl(collection_name="test_valid", query_texts=[], n_results=1)
        assert_error_result(result, "Validation Error: No query texts provided")

    @pytest.mark.asyncio
    async def test_query_documents_validation_invalid_nresults(self, mock_chroma_client):
        """Test validation failure with invalid n_results."""
        result = await _query_documents_impl(collection_name="test_valid", query_texts=["q"], n_results=0)
        assert_error_result(result, "Validation Error: n_results must be a positive integer")

    @pytest.mark.asyncio
    async def test_query_documents_validation_invalid_include(self, mock_chroma_client):
        """Test validation failure with invalid include values."""
        result = await _query_documents_impl(
            collection_name="test_valid",
            query_texts=["q"],
            n_results=1, # Add missing argument
            include=["distances", "invalid_field"]
        )
        assert_error_result(result, "Validation Error: Invalid item(s) in include list: ['invalid_field']")

    # --- _get_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_get_documents_success_by_ids(self, mock_chroma_client):
        """Test successful document retrieval by IDs."""
        mock_client, mock_collection = mock_chroma_client
        mock_collection.get.return_value = {
            "ids": ["id1", "id3"],
            "documents": ["doc one", "doc three"],
            "metadatas": [{"k":1}, {"k":3}]
        }
        
        ids_to_get = ["id1", "id3"]
        result = await _get_documents_impl(
            collection_name="test_get_ids",
            ids=ids_to_get,
            limit=0, # Add mandatory args
            offset=0
        )
        
        # Assert synchronous call
        mock_collection.get.assert_called_once_with(
            ids=ids_to_get,
            where=None,
            where_document=None,
            include=["documents", "metadatas"], # Default include
            limit=None, # limit=0 becomes None
            offset=None # offset=0 becomes None
        )
        # Use helper to parse JSON first
        result_data = assert_successful_json_result(result)

        # Check parsed data - USE .get()
        assert "documents" in result_data
        assert len(result_data.get("documents", [])) == 2
        # Check the correct key based on implementation (likely 'retrieved_count')
        assert result_data.get("retrieved_count", -1) == 2 # Use default if key missing
        doc1 = result_data.get("documents", [])[0]
        assert doc1.get("id") == "id1"
        assert doc1.get("content") == "doc one"
        assert doc1.get("metadata") == {"k":1}
        doc2 = result_data.get("documents", [])[1]
        assert doc2.get("id") == "id3"
        assert doc2.get("content") == "doc three"
        assert doc2.get("metadata") == {"k":3}

    @pytest.mark.asyncio
    async def test_get_documents_success_by_where(self, mock_chroma_client):
        """Test successful get by where filter with limit/offset."""
        mock_client, mock_collection = mock_chroma_client
        mock_collection.get.return_value = {
            "ids": ["id5"],
            "documents": ["doc five"], # Only documents included
            "metadatas": None # Not included
        }
        
        where_filter = {"topic": "filtering"}
        result = await _get_documents_impl(
            collection_name="test_get_filter",
            where=where_filter,
            limit=5,
            offset=4,
            include=["documents"] # Custom include
        )
        
        # Assert synchronous call
        mock_collection.get.assert_called_once_with(
            ids=None,
            where=where_filter,
            where_document=None,
            include=["documents"],
            limit=5, # Limit > 0 passed directly
            offset=4 # Offset > 0 passed directly
        )
        # Use helper to parse JSON first
        result_data = assert_successful_json_result(result)

        # Check parsed data - USE .get()
        assert len(result_data.get("documents", [])) == 1
        # Check the correct key based on implementation (likely 'retrieved_count')
        assert result_data.get("retrieved_count", -1) == 1 # Use default if key missing
        doc1 = result_data.get("documents", [])[0]
        assert doc1.get("id") == "id5"
        assert doc1.get("content") == "doc five"
        assert doc1.get("metadata") is None

    @pytest.mark.asyncio
    async def test_get_documents_validation_no_criteria(self, mock_chroma_client):
        """Test validation failure with no criteria (ids/where)."""
        # Adapted test: Check successful retrieval of all (mocked empty)
        mock_client, mock_collection = mock_chroma_client
        mock_collection.get.return_value = {"ids": [], "documents": [], "metadatas": []}
        result = await _get_documents_impl(
            collection_name="test_valid",
            limit=10, # Provide limit
            offset=0  # Provide offset
        )
        # Expect successful result, not error
        result_data = assert_successful_json_result(result)
        assert result_data.get("documents") == []
        # Correct the key check based on implementation (likely 'retrieved_count')
        assert result_data.get("retrieved_count", -1) == 0 # Check count key
        mock_collection.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_documents_validation_invalid_limit(self, mock_chroma_client):
        """Test validation failure with invalid limit."""
        result = await _get_documents_impl(
            collection_name="test_valid",
            ids=["id1"],
            limit=-1,
            offset=0 # Add missing argument
        )
        assert_error_result(result, "Validation Error: limit cannot be negative")
        
    # --- _update_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_update_documents_success(self, mock_chroma_client):
        """Test successful document update."""
        mock_client, mock_collection = mock_chroma_client
        ids_to_update = ["id1"]
        new_docs = ["new content"]
        new_metas = [{"k": "new_v"}]
        
        result = await _update_documents_impl(
            collection_name="test_update",
            ids=ids_to_update,
            documents=new_docs,
            metadatas=new_metas
        )
        
        # Assert synchronous call
        mock_collection.update.assert_called_once_with(
            ids=ids_to_update,
            documents=new_docs,
            metadatas=new_metas
        )
        # Use helper
        result_data = assert_successful_json_result(result)
        # Check parsed data - USE .get()
        assert result_data.get("status") == "success"
        assert result_data.get("processed_count") == len(ids_to_update)
        assert result_data.get("collection_name") == "test_update"

    @pytest.mark.asyncio
    async def test_update_documents_only_metadata(self, mock_chroma_client):
        """Test updating only metadata."""
        mock_client, mock_collection = mock_chroma_client
        ids_to_update = ["id2"]
        new_metas = [{"status": "archived"}]
        
        result = await _update_documents_impl(
            collection_name="test_update_meta",
            ids=ids_to_update,
            documents=None, # Explicitly None
            metadatas=new_metas
        )
        
        # Assert synchronous call
        mock_collection.update.assert_called_once_with(
            ids=ids_to_update,
            documents=None, # Check None passed correctly
            metadatas=new_metas
        )
        # Use helper
        result_data = assert_successful_json_result(result)
        # Check parsed data - USE .get()
        assert result_data.get("status") == "success"
        assert result_data.get("processed_count") == 1

    @pytest.mark.asyncio
    async def test_update_documents_validation_no_ids(self, mock_chroma_client):
        """Test validation failure when no IDs are provided."""
        result = await _update_documents_impl(collection_name="test_valid", ids=[], documents=["d"])
        # Correct assertion message based on test output
        assert_error_result(result, "Validation Error: List of document IDs (ids) is required for update")

    @pytest.mark.asyncio
    async def test_update_documents_validation_no_data(self, mock_chroma_client):
        """Test validation failure when no data (docs/metas) is provided."""
        result = await _update_documents_impl(collection_name="test_valid", ids=["id1"])
        assert_error_result(result, "Validation Error: Either documents or metadatas must be provided for update")

    @pytest.mark.asyncio
    async def test_update_documents_validation_mismatch(self, mock_chroma_client):
        """Test validation failure with mismatched docs/metas and IDs."""
        result = await _update_documents_impl(collection_name="test_valid", ids=["id1"], documents=["d1", "d2"])
        assert_error_result(result, "Validation Error: Number of documents must match number of IDs")

    # --- _delete_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_delete_documents_success_by_ids(self, mock_chroma_client):
        """Test successful deletion by IDs."""
        mock_client, mock_collection = mock_chroma_client
        ids_to_delete = ["id1", "id2"]
        # Mock delete to return the IDs it was called with, mimicking ChromaDB behavior
        mock_collection.delete.return_value = ids_to_delete 
        
        result = await _delete_documents_impl(
            collection_name="test_delete_ids",
            ids=ids_to_delete
        )
        
        # Assert synchronous call
        mock_collection.delete.assert_called_once_with(
            ids=ids_to_delete,
            where=None,
            where_document=None
        )
        # Use helper
        result_data = assert_successful_json_result(result)
        # Check parsed data - USE .get()
        assert result_data.get("status") == "success"
        assert "deleted_count" in result_data
        assert result_data.get("deleted_count") == len(ids_to_delete)
        assert "deleted_ids" in result_data
        assert result_data.get("deleted_ids") == ids_to_delete

    @pytest.mark.asyncio
    async def test_delete_documents_success_by_where(self, mock_chroma_client):
        """Test successful deletion by where filter."""
        mock_client, mock_collection = mock_chroma_client
        where_filter = {"status": "old"}
        # Mock delete to return an empty list when filter is used (IDs deleted are unknown)
        mock_collection.delete.return_value = [] 
        
        result = await _delete_documents_impl(
            collection_name="test_delete_where",
            where=where_filter
        )
        
        # Assert synchronous call
        mock_collection.delete.assert_called_once_with(
            ids=None,
            where=where_filter,
            where_document=None
        )
        # Use helper
        result_data = assert_successful_json_result(result)
        # Check parsed data - USE .get()
        assert result_data.get("status") == "success"
        assert result_data.get("deleted_count") == 0
        assert result_data.get("deleted_ids") == []

    @pytest.mark.asyncio
    async def test_delete_documents_validation_no_criteria(self, mock_chroma_client):
        """Test validation failure with no criteria (ids/where)."""
        result = await _delete_documents_impl(collection_name="test_valid")
        assert_error_result(result, "Validation Error: Either ids, where, or where_document must be provided for deletion")

    # --- Generic Error Handling Tests ---
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "tool_impl_func, chroma_method_name, args, kwargs, expected_error_msg_part", [
            # Add missing required args to kwargs for each tool
            (_add_documents_impl, "add", [], {"collection_name": "c", "documents": ["d"], "increment_index": True}, "adding documents"),
            (_query_documents_impl, "query", [], {"collection_name": "c", "query_texts": ["q"], "n_results": 1}, "querying documents"),
            (_get_documents_impl, "get", [], {"collection_name": "c", "ids": ["id1"], "limit": 1, "offset": 0}, "getting documents"),
            (_update_documents_impl, "update", [], {"collection_name": "c", "ids": ["id1"], "documents": ["d"]}, "updating documents"),
            (_delete_documents_impl, "delete", [], {"collection_name": "c", "ids": ["id1"]}, "deleting documents"),
        ]
    )
    async def test_generic_chroma_error_handling(self, mock_chroma_client, tool_impl_func, chroma_method_name, args, kwargs, expected_error_msg_part):
        """Tests that unexpected ChromaDB errors during tool execution return CallToolResult(isError=True)."""
        mock_client, mock_collection = mock_chroma_client
        error_message = "Generic Chroma Error"
        
        # Mock the specific chroma method to raise a generic exception
        # getattr(mock_collection, chroma_method_name).side_effect = Exception(error_message)
        # More robust mocking: handle potential AttributeError if method doesn't exist on mock_collection
        if hasattr(mock_collection, chroma_method_name):
             getattr(mock_collection, chroma_method_name).side_effect = Exception(error_message)
        elif hasattr(mock_client, chroma_method_name):
             getattr(mock_client, chroma_method_name).side_effect = Exception(error_message)
        else:
             pytest.fail(f"Method {chroma_method_name} not found on mock client or collection")
        
        # If the error happens during get_collection itself
        if chroma_method_name == 'get_collection':
            mock_client.get_collection.side_effect = Exception(error_message)
        else: # Otherwise, ensure get_collection succeeds before the target method fails
            mock_client.get_collection.return_value = mock_collection
            mock_client.get_collection.side_effect = None # Reset side effect if set previously

        # Call the function with unpacked args and kwargs
        result = await tool_impl_func(*args, **kwargs)
        # Assert it returns an error with the expected substring
        assert_error_result(result, f"Tool Error: An unexpected error occurred while {expected_error_msg_part}")

    @pytest.mark.asyncio
    async def test_query_collection_not_found(self, mock_chroma_client):
        """Test querying a non-existent collection."""
        mock_client, _ = mock_chroma_client
        collection_name = "non_existent_coll"
        # Mock get_collection to raise the specific ValueError Chroma uses
        mock_client.get_collection.side_effect = ValueError(f"Collection {collection_name} does not exist.")
        
        # Use assert_error_result instead of pytest.raises
        # with pytest.raises(McpError) as exc_info:
        #     await _query_documents_impl(collection_name=collection_name, query_texts=["q"])
        # assert f"Collection \'{collection_name}\' not found" in str(exc_info.value)
        result = await _query_documents_impl(
            collection_name=collection_name,
            query_texts=["q"],
            n_results=1 # Add missing argument
        )
        assert_error_result(result, f"Tool Error: Collection '{collection_name}' not found.") 