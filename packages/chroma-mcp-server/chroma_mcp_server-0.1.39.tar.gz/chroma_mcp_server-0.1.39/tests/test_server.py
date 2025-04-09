"""Tests for the ChromaMCP server implementation."""

# Standard library imports
import argparse
import importlib.metadata
import os
from unittest.mock import AsyncMock, MagicMock, call, patch

# Third-party imports
import pytest
# Import McpError and INTERNAL_ERROR from exceptions
from mcp.shared.exceptions import McpError 

# Local application imports
# Import the module itself to allow monkeypatching its attributes
from chroma_mcp import server
# Only import get_mcp which is still in server.py
from chroma_mcp.server import get_mcp 
# Removed: _initialize_mcp_instance, config_server, create_parser
# from chroma_mcp.server import (
#     _initialize_mcp_instance, config_server, create_parser,
#     get_mcp
# )
# Keep ValidationError import, remove CollectionNotFoundError
from chroma_mcp.utils.errors import ValidationError
# from chroma_mcp.utils.errors import (
#     CollectionNotFoundError, ValidationError
# )

# Mock dependencies globally for simplicity in these tests
@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock external dependencies like ChromaDB and FastMCP availability."""
    with patch("chroma_mcp.server.CHROMA_AVAILABLE", True), \
         patch("chroma_mcp.server.FASTMCP_AVAILABLE", True):
        yield

@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global handlers and MCP instance before each test."""
    server._mcp_instance = None
    server._thinking_handler = None
    yield
    server._mcp_instance = None
    server._thinking_handler = None

@pytest.fixture
def mock_register_collection():
    with patch("chroma_mcp.server.register_collection_tools") as mock:
        yield mock

@pytest.fixture
def mock_register_document():
    with patch("chroma_mcp.server.register_document_tools") as mock:
        yield mock

@pytest.fixture
def mock_register_thinking():
    with patch("chroma_mcp.server.register_thinking_tools") as mock:
        yield mock

@pytest.fixture
def mock_mcp():
    """Mock the FastMCP class."""
    with patch("chroma_mcp.server.FastMCP", autospec=True) as mock:
        yield mock

# Patch logging.getLogger for tests needing to check log calls
@pytest.fixture
def mock_get_logger():
    with patch("chroma_mcp.server.logging.getLogger") as mock_get:
        mock_logger = MagicMock()
        mock_get.return_value = mock_logger
        yield mock_logger # Yield the instance returned by getLogger

# --- Test Functions ---

# Filter the specific RuntimeWarning for this test
@pytest.mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call' was never awaited:RuntimeWarning")
def test_get_mcp_initialization(
    mock_mcp, mock_register_collection, mock_register_document, mock_register_thinking, monkeypatch
):
    """Test successful MCP initialization and tool registration."""
    monkeypatch.setattr(server, "_mcp_instance", None)

    mcp_instance = get_mcp()

    assert mcp_instance is mock_mcp.return_value

    mock_mcp.assert_called_once_with("chroma")

    mock_register_collection.assert_called_once_with(mock_mcp.return_value)
    mock_register_document.assert_called_once_with(mock_mcp.return_value)
    mock_register_thinking.assert_called_once_with(mock_mcp.return_value)

    # Check that the .tool() method was called with the correct name
    # for the get_version_tool
    found_tool_call = False
    for method_call in mock_mcp.return_value.method_calls:
        # method_call looks like call.tool(name=..., ...)
        if method_call[0] == 'tool' and method_call.kwargs.get('name') == 'chroma_get_server_version':
            found_tool_call = True
            break
    assert found_tool_call, "call to .tool(name='chroma_get_server_version') not found on mock MCP"

def test_get_mcp_initialization_error(mock_mcp, monkeypatch):
    """Test MCP initialization error handling."""
    monkeypatch.setattr(server, "_mcp_instance", None)

    mock_mcp.side_effect = Exception("Failed to initialize")

    with pytest.raises(McpError) as exc_info:
        get_mcp()

    assert "Failed to initialize MCP" in str(exc_info.value)
    mock_mcp.assert_called_once_with("chroma")
