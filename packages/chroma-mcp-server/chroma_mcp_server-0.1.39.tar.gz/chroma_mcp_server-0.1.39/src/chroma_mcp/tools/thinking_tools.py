"""
Sequential thinking tools for managing thought chains and context in ChromaDB.
"""

import time
import uuid
import json
import logging

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from mcp import types
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR

# Import InvalidDimensionException
from chromadb.errors import InvalidDimensionException 

from ..utils.errors import ValidationError
from ..types import ThoughtMetadata

# Constants
THOUGHTS_COLLECTION = "thoughts"
SESSIONS_COLLECTION = "thinking_sessions"
DEFAULT_SIMILARITY_THRESHOLD = 0.75

@dataclass
class ThoughtMetadata:
    """Metadata structure for thoughts."""
    session_id: str
    thought_number: int
    total_thoughts: int
    timestamp: int
    branch_from_thought: Optional[int] = None
    branch_id: Optional[str] = None
    next_thought_needed: bool = False
    custom_data: Optional[Dict[str, Any]] = None

# --- Implementation Functions ---

async def _sequential_thinking_impl(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    session_id: str = "",
    branch_from_thought: int = 0,
    branch_id: str = "",
    next_thought_needed: bool = False,
    custom_data: Optional[Dict[str, Any]] = None
) -> types.CallToolResult:
    """Implementation logic for recording a thought."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client
    from ..utils.client import get_embedding_function

    try:
        if custom_data is None:
            custom_data = {}
        if not thought:
            raise ValidationError("Thought content is required")
        if thought_number < 1 or (total_thoughts > 0 and thought_number > total_thoughts):
            raise ValidationError(f"Invalid thought number: {thought_number}. Must be between 1 and total_thoughts ({total_thoughts}).")
        
        effective_session_id = session_id if session_id else str(uuid.uuid4())
        timestamp = int(time.time())
        metadata = ThoughtMetadata(
            session_id=effective_session_id,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            timestamp=timestamp,
            branch_from_thought=branch_from_thought if branch_from_thought > 0 else None,
            branch_id=branch_id if branch_id else None,
            next_thought_needed=next_thought_needed,
            custom_data=custom_data if custom_data else None
        )
        
        client = get_chroma_client()
        
        try:
            collection = client.get_or_create_collection(
                name=THOUGHTS_COLLECTION,
                embedding_function=get_embedding_function()
            )
        except Exception as e:
            logger.error(f"Error getting/creating collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Error accessing collection '{THOUGHTS_COLLECTION}': {str(e)}")]
            )
            
        thought_id = f"thought_{effective_session_id}_{thought_number}"
        if branch_id:
            thought_id += f"_branch_{branch_id}"
            
        metadata_dict = asdict(metadata)
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        if 'custom_data' in metadata_dict and metadata_dict['custom_data']:
            custom = metadata_dict.pop('custom_data')
            for ck, cv in custom.items():
                metadata_dict[f"custom:{ck}"] = cv 
        else:
            metadata_dict.pop('custom_data', None)

        try:
            collection.add(
                documents=[thought],
                metadatas=[metadata_dict],
                ids=[thought_id]
            )
        except (ValueError, InvalidDimensionException) as e:
            logger.error(f"Error adding thought to collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Error adding thought: {str(e)}")]
            )
        
        previous_thoughts = []
        if thought_number > 1:
            where_clause = {
                "session_id": effective_session_id,
                "thought_number": {"$lt": thought_number}
            }
            
            try:
                results = collection.get(
                    where=where_clause,
                    include=["documents", "metadatas"],
                )
                
                if results and results.get("ids"):
                    thought_data = []
                    for i in range(len(results["ids"])):
                        raw_meta = results["metadatas"][i] or {}
                        reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                        base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                        if reconstructed_custom:
                            base_meta['custom_data'] = reconstructed_custom
                            
                        thought_data.append({
                            "id": results["ids"][i],
                            "content": results["documents"][i],
                            "metadata": base_meta,
                            "thought_number_sort_key": base_meta.get('thought_number', 999999)
                        })
                    
                    sorted_thoughts = sorted(thought_data, key=lambda x: x["thought_number_sort_key"])
                    
                    previous_thoughts = [{k: v for k, v in thought.items() if k != 'thought_number_sort_key'} for thought in sorted_thoughts]

            except ValueError as e:
                 logger.error(f"Error retrieving previous thoughts for session '{effective_session_id}': {e}", exc_info=True)
                 previous_thoughts = []

        logger.info(f"Recorded thought {thought_number}/{total_thoughts} for session {effective_session_id}")
        
        result_data = {
            "status": "success",
            "thought_id": thought_id,
            "session_id": effective_session_id,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "previous_thoughts": previous_thoughts,
            "next_thought_needed": next_thought_needed
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValidationError as e:
        logger.warning(f"Validation error recording thought for session '{session_id or '(new)'}': {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except Exception as e:
        logger.error(f"Unexpected error recording thought for session '{session_id or '(new)'}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while recording thought. Details: {str(e)}")]
        )

async def _find_similar_thoughts_impl(
    query: str,
    n_results: int = 5,
    threshold: Optional[float] = DEFAULT_SIMILARITY_THRESHOLD,
    session_id: Optional[str] = None,
    include_branches: bool = True
) -> types.CallToolResult:
    """Implementation logic for finding similar thoughts."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client
    from ..utils.client import get_embedding_function

    try:
        # Use default threshold if None is passed
        effective_threshold = threshold if threshold is not None else DEFAULT_SIMILARITY_THRESHOLD
        
        client = get_chroma_client()
        
        # Get collection, handle not found specifically
        try:
            collection = client.get_collection(
                name=THOUGHTS_COLLECTION,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot find similar thoughts: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return success with empty results, indicating collection doesn't exist
                return types.CallToolResult(
                    content=[types.TextContent(type="text", text=json.dumps({
                        "similar_thoughts": [],
                        "total_found": 0,
                        "threshold": effective_threshold,
                        "message": f"Collection '{THOUGHTS_COLLECTION}' not found."
                    }, indent=2))]
                )
            else:
                raise e # Re-raise other ValueErrors
        except Exception as e: # Catch other potential errors during get_collection
             logger.error(f"Error getting collection '{THOUGHTS_COLLECTION}' for query: {e}", exc_info=True)
             return types.CallToolResult(
                 isError=True,
                 content=[types.TextContent(type="text", text=f"ChromaDB Error accessing collection '{THOUGHTS_COLLECTION}': {str(e)}")]
             )
        
        # Prepare where clause if session_id is provided
        where_clause = None
        if session_id:
            where_clause = {"session_id": session_id}
            # TODO: Add branch filtering logic if needed based on include_branches
        
        # Perform query, handle errors
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
        except ValueError as e: # Catch query-specific errors
            logger.error(f"Error querying thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Query Error: {str(e)}")]
            )
        
        # Process results and filter by threshold
        similar_thoughts = []
        if results and results.get("ids") and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                similarity = 1.0 - distance # Ensure float calculation
                
                if similarity >= effective_threshold:
                    raw_meta = results["metadatas"][0][i] or {}
                    # Reconstruct custom data
                    reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                    base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                    if reconstructed_custom:
                        base_meta['custom_data'] = reconstructed_custom
                        
                    thought = {
                        "id": results["ids"][0][i], # Include ID
                        "content": results["documents"][0][i],
                        "metadata": base_meta,
                        "similarity": similarity
                    }
                    similar_thoughts.append(thought)
        
        # Success result
        result_data = {
            "similar_thoughts": similar_thoughts,
            "total_found": len(similar_thoughts),
            "threshold_used": effective_threshold
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )
        
    except ValueError as e: # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error accessing collection '{THOUGHTS_COLLECTION}' for query: {e}", exc_info=False)
        # This path should likely not be hit due to specific handling above, but acts as a fallback
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error accessing collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error finding similar thoughts: {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while finding similar thoughts. Details: {str(e)}")]
        )

async def _get_session_summary_impl(
    session_id: str,
    include_branches: bool = True # Note: include_branches not currently used
) -> types.CallToolResult:
    """Implementation logic for getting session summary."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client
    from ..utils.client import get_embedding_function

    try:
        client = get_chroma_client()
        
        # Get collection, handle not found
        try:
            collection = client.get_collection(
                name=THOUGHTS_COLLECTION,
                embedding_function=get_embedding_function()
            )
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot get session summary: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return success with empty results
                return types.CallToolResult(
                    content=[types.TextContent(type="text", text=json.dumps({
                        "session_id": session_id,
                        "session_thoughts": [],
                        "total_thoughts_in_session": 0,
                        "message": f"Collection '{THOUGHTS_COLLECTION}' not found."
                    }, indent=2))]
                )
            else:
                raise e # Re-raise other ValueErrors
        except Exception as e: # Catch other potential errors during get_collection
             logger.error(f"Error getting collection '{THOUGHTS_COLLECTION}' for session summary: {e}", exc_info=True)
             return types.CallToolResult(
                 isError=True,
                 content=[types.TextContent(type="text", text=f"ChromaDB Error: {str(e)}")]
             )

        where_clause = {"session_id": session_id}
        # TODO: Add branch filtering if needed based on include_branches
        
        # Get thoughts, handle errors
        try:
            results = collection.get(
                where=where_clause,
                include=["ids", "documents", "metadatas"] # Include IDs
            )
        except ValueError as e: # Catch errors from get (e.g., bad filter)
            logger.error(f"Error getting thoughts for session '{session_id}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Get Error: {str(e)}")]
            )
        
        # Process and sort results
        session_thoughts = []
        if results and results.get("ids"):
            thought_data = []
            for i in range(len(results["ids"])):
                raw_meta = results["metadatas"][i] or {}
                # Reconstruct custom data
                reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                if reconstructed_custom:
                    base_meta['custom_data'] = reconstructed_custom
                    
                thought_data.append({
                    "id": results["ids"][i], # Include ID
                    "content": results["documents"][i],
                    "metadata": base_meta,
                    "thought_number_sort_key": base_meta.get('thought_number', 999999) # Temp key for sorting
                })
            
            # Sort based on thought_number
            sorted_thoughts = sorted(thought_data, key=lambda x: x["thought_number_sort_key"])
            
            # Final list without the sort key
            session_thoughts = [{k: v for k, v in thought.items() if k != 'thought_number_sort_key'} for thought in sorted_thoughts]

        # Success result
        result_data = {
            "session_id": session_id,
            "session_thoughts": session_thoughts,
            "total_thoughts_in_session": len(session_thoughts)
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )
        
    except ValueError as e: # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error accessing collection '{THOUGHTS_COLLECTION}' for session summary: {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error accessing collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error getting session summary for '{session_id}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while getting session summary for '{session_id}'. Details: {str(e)}")]
        )

async def _find_similar_sessions_impl(
    query: str,
    n_results: int = 3,
    threshold: Optional[float] = DEFAULT_SIMILARITY_THRESHOLD
) -> types.CallToolResult:
    """Implementation logic for finding similar sessions."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client
    from ..utils.client import get_embedding_function

    try:
        # Use default threshold if None is passed
        effective_threshold = threshold if threshold is not None else DEFAULT_SIMILARITY_THRESHOLD
        
        client = get_chroma_client()
        
        # --- Step 1: Get all unique session IDs from the thoughts collection --- 
        thoughts_collection = None
        all_session_ids = set()
        try:
            thoughts_collection = client.get_collection(
                name=THOUGHTS_COLLECTION,
                embedding_function=get_embedding_function() 
            )
            # Efficiently get all unique session_ids from metadata
            # This might be slow for very large collections, consider optimization if needed
            all_metadata = thoughts_collection.get(include=["metadatas"]) 
            if all_metadata and all_metadata.get("metadatas"):
                for meta in all_metadata["metadatas"]:
                    if meta and "session_id" in meta:
                        all_session_ids.add(meta["session_id"])
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot find similar sessions: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return empty result if thoughts collection is missing
                return types.CallToolResult(content=[types.TextContent(type="text", text=json.dumps({"similar_sessions": [], "total_found": 0, "threshold_used": effective_threshold}, indent=2))])
            else:
                raise e # Re-raise other ValueErrors
        except Exception as e:
            logger.error(f"Error accessing thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Error accessing thoughts collection: {str(e)}")])

        if not all_session_ids:
             logger.info("No sessions found in the thoughts collection.")
             return types.CallToolResult(content=[types.TextContent(type="text", text=json.dumps({"similar_sessions": [], "total_found": 0, "threshold_used": effective_threshold}, indent=2))])

        # --- Step 2: Create/Get Sessions Collection and Embed Session Summaries --- 
        sessions_collection = None
        try:
            sessions_collection = client.get_or_create_collection(
                name=SESSIONS_COLLECTION,
                embedding_function=get_embedding_function() 
            )
            
            # Embed summaries for sessions not already in the sessions collection
            existing_session_ids = set(sessions_collection.get().get("ids", []))
            sessions_to_embed = []
            ids_to_embed = []
            
            for session_id in all_session_ids:
                if session_id not in existing_session_ids:
                    # Get session summary (needs await)
                    summary_result = await _get_session_summary_impl(session_id)
                    # Check if the internal call succeeded
                    if not summary_result.isError:
                        # Safely parse the JSON content
                        try:
                            summary_data = json.loads(summary_result.content[0].text)
                            summary_text = " ".join([t.get('content', '') for t in summary_data.get('session_thoughts', [])])
                            if summary_text: # Only embed if there's content
                                sessions_to_embed.append(summary_text)
                                ids_to_embed.append(session_id)
                        except (json.JSONDecodeError, IndexError, AttributeError) as parse_error:
                             logger.warning(f"Could not parse summary result for session '{session_id}': {parse_error}")
                    else:
                         logger.warning(f"Failed to get summary for session '{session_id}' to embed: {summary_result.content[0].text if summary_result.content else 'Unknown error'}")
            
            if sessions_to_embed:
                logger.info(f"Embedding summaries for {len(sessions_to_embed)} new/updated sessions.")
                sessions_collection.add(
                    documents=sessions_to_embed,
                    ids=ids_to_embed
                )
                
        except Exception as e:
            logger.error(f"Error creating/updating sessions collection '{SESSIONS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Error: {str(e)}")])
            
        # --- Step 3: Query the Sessions Collection --- 
        similar_sessions = []
        if sessions_collection: # Ensure collection was accessed successfully
            try:
                query_results = sessions_collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    include=["metadatas", "distances"] # Only need distance and ID (implicit)
                )
                
                if query_results and query_results.get("ids") and query_results["ids"][0]:
                    for i in range(len(query_results["ids"][0])):
                        session_id = query_results["ids"][0][i]
                        distance = query_results["distances"][0][i]
                        similarity = 1.0 - distance

                        if similarity >= effective_threshold:
                             # Fetch the full summary details again for the result
                             # This is slightly inefficient but ensures fresh data
                             summary_result = await _get_session_summary_impl(session_id)
                             if not summary_result.isError:
                                 try:
                                     summary_data = json.loads(summary_result.content[0].text)
                                     summary_data["similarity_score"] = similarity # Add score
                                     similar_sessions.append(summary_data)
                                 except (json.JSONDecodeError, IndexError, AttributeError) as parse_error:
                                     logger.warning(f"Could not parse final summary result for session '{session_id}': {parse_error}")
                             else:
                                  logger.warning(f"Failed to get final summary for session '{session_id}': {summary_result.content[0].text if summary_result.content else 'Unknown error'}")
            except ValueError as e:
                 logger.error(f"Error querying sessions collection '{SESSIONS_COLLECTION}': {e}", exc_info=True)
                 return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Query Error on sessions: {str(e)}")])

        # Success result
        result_data = {
            "similar_sessions": similar_sessions,
            "total_found": len(similar_sessions),
            "threshold_used": effective_threshold
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result_json)]
        )

    except ValueError as e: # Catch ValueErrors re-raised from get_collection (thoughts)
        logger.error(f"Value error accessing thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=False)
        return types.CallToolResult(
             isError=True,
             content=[types.TextContent(type="text", text=f"ChromaDB Value Error accessing thoughts collection: {str(e)}")]
         )
    except Exception as e:
        logger.error(f"Unexpected error finding similar sessions: {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"Tool Error: An unexpected error occurred while finding similar sessions. Details: {str(e)}")]
        )

# --- Tool Registration ---

class SequentialThinkingTool(types.Tool):
    """Records a single thought as part of a sequential thinking process or workflow.
        
        Use this tool to log steps, observations, decisions, or intermediate results in a structured manner. 
        Each thought is linked to a session (automatically created if none provided) and numbered sequentially. 
        This allows reconstructing the flow of a process or retrieving context from specific points. 
        Optional branching allows capturing alternative paths or explorations within a session.

        Args:
            thought: The content of the current thought, step, or observation.
            thought_number: The sequence number of this thought within the session (1-based).
            total_thoughts: The total expected number of thoughts in this main sequence.
            session_id: Identifier for the thinking session. If empty, a new UUID is generated.
            branch_from_thought: The thought_number this thought branches off from (0 if main sequence).
            branch_id: A unique identifier for this specific branch path (e.g., 'alternative_approach').
            next_thought_needed: Flag indicating if a subsequent thought is expected (default: False).
            custom_data: Optional dictionary for arbitrary metadata related to this thought.

        Returns:
            Dictionary confirming the recording, including thought_id, session_id, and previous thoughts in the sequence.
        """
    thought: str
    thought_number: int
    total_thoughts: int
    session_id: Optional[str] = None # Use None for optional
    branch_from_thought: Optional[int] = None # Use None for optional
    branch_id: Optional[str] = None # Use None for optional
    next_thought_needed: Optional[bool] = False # Default False
    custom_data: Optional[Dict[str, Any]] = None

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _sequential_thinking_impl(
            thought=self.thought,
            thought_number=self.thought_number,
            total_thoughts=self.total_thoughts,
            session_id=self.session_id or "", # Pass empty string if None
            branch_from_thought=self.branch_from_thought or 0, # Pass 0 if None
            branch_id=self.branch_id or "", # Pass empty string if None
            next_thought_needed=self.next_thought_needed or False,
            custom_data=self.custom_data # Pass None if None
        )

class FindSimilarThoughtsTool(types.Tool):
    """Finds thoughts across one or all sessions that are semantically similar to a given query.
        
        Useful for retrieving context from past thinking processes based on conceptual similarity. 
        For example, finding previous attempts at solving a similar problem or recalling related observations.
        The search can be restricted to a specific session_id.

        Args:
            query: The text query representing the concept or thought to search for.
            n_results: Maximum number of similar thoughts to return.
            threshold: Minimum similarity score (1 - distance) for a thought to be included.
            session_id: If provided, restricts the search to only this session.
            include_branches: Whether to include thoughts from branched paths in the search (currently not implemented in filter).

        Returns:
            Dictionary containing a list of similar thoughts, their metadata, and similarity scores.
        """
    query: str
    n_results: Optional[int] = 5
    threshold: Optional[float] = DEFAULT_SIMILARITY_THRESHOLD
    session_id: Optional[str] = None # Optional
    include_branches: Optional[bool] = True # Default True

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _find_similar_thoughts_impl(
            query=self.query,
            n_results=self.n_results,
            threshold=self.threshold,
            session_id=self.session_id, # Pass None if None
            include_branches=self.include_branches
        )

class GetSessionSummaryTool(types.Tool):
    """Retrieves all thoughts recorded within a specific thinking session, ordered sequentially.
        
        Allows reconstructing the entire flow of a particular thinking process or problem-solving attempt. 
        Can optionally include thoughts from defined branches.

        Args:
            session_id: The unique identifier of the thinking session to retrieve.
            include_branches: Whether to include thoughts from branched paths (currently not implemented in filter).

        Returns:
            Dictionary containing the session_id and a list of all thoughts belonging to that session.
        """
    session_id: str
    include_branches: Optional[bool] = True # Default True

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _get_session_summary_impl(
            session_id=self.session_id,
            include_branches=self.include_branches
        )

class FindSimilarSessionsTool(types.Tool):
    """Finds thinking sessions whose overall content is semantically similar to a given query.
        
        This performs a search over *summaries* of entire sessions. Useful for finding past 
        problem-solving sessions related to a general topic or goal, even if specific steps differ.

        Args:
            query: The text query representing the topic or goal to search for in past sessions.
            n_results: Maximum number of similar sessions to return.
            threshold: Minimum similarity score for a session summary to be included.

        Returns:
            Dictionary containing a list of similar sessions, each with its summary and similarity score.
        """
    query: str
    n_results: Optional[int] = 3
    threshold: Optional[float] = DEFAULT_SIMILARITY_THRESHOLD

    async def _call_impl(self) -> types.CallToolResult: # Updated signature
        return await _find_similar_sessions_impl(
            query=self.query,
            n_results=self.n_results,
            threshold=self.threshold
        )

def register_thinking_tools(mcp: FastMCP) -> None:
    """Register sequential thinking tools with the MCP server."""

    # Register using the Tool class types
    mcp.register_tool_type(SequentialThinkingTool)
    mcp.register_tool_type(FindSimilarThoughtsTool)
    mcp.register_tool_type(GetSessionSummaryTool)
    mcp.register_tool_type(FindSimilarSessionsTool)
    
    # Note: The helper async function `record_thought` is not an MCP tool and doesn't need registration.

    logger = logging.getLogger("chroma_mcp.tools.thinking")
    logger.info("Registered sequential thinking tools.")
