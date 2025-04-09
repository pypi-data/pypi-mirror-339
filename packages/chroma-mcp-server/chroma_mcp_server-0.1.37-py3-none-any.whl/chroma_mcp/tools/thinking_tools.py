"""
Sequential thinking tools for managing thought chains and context in ChromaDB.
"""

import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR

from ..utils.errors import handle_chroma_error, validate_input, raise_validation_error
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

def _sequential_thinking_impl(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    session_id: str = "",
    branch_from_thought: int = 0,
    branch_id: str = "",
    next_thought_needed: bool = False,
    custom_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Implementation logic for recording a thought."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client, get_embedding_function

    try:
        if custom_data is None:
            custom_data = {}
        if not thought:
            raise_validation_error("Thought content is required")
        if thought_number < 1 or thought_number > total_thoughts:
            raise_validation_error(f"Invalid thought number: {thought_number}")
        
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
        collection = client.get_or_create_collection(
            name=THOUGHTS_COLLECTION,
            embedding_function=get_embedding_function()
        )
        
        thought_id = f"thought_{effective_session_id}_{thought_number}"
        if branch_id:
            thought_id += f"_branch_{branch_id}"
            
        metadata_dict = metadata.__dict__
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        if 'custom_data' in metadata_dict and metadata_dict['custom_data']:
            custom = metadata_dict.pop('custom_data')
            for ck, cv in custom.items():
                metadata_dict[f"custom:{ck}"] = cv 
        
        collection.add(
            documents=[thought],
            metadatas=[metadata_dict],
            ids=[thought_id]
        )
        
        previous_thoughts = []
        if thought_number > 1:
            where_clause = {
                "session_id": effective_session_id,
                "thought_number": {"$lt": thought_number}
            }
            if branch_id:
                where_clause["branch_id"] = branch_id
            
            results = collection.get(
                where=where_clause,
                include=["documents", "metadatas"]
            )
            
            if results and results.get("ids"):
                for i in range(len(results["ids"])):
                    raw_meta = results["metadatas"][i] or {}
                    reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                    base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                    if reconstructed_custom:
                        base_meta['custom_data'] = reconstructed_custom
                        
                    previous_thoughts.append({
                        "content": results["documents"][i],
                        "metadata": base_meta
                    })
        
        logger.info(f"Recorded thought {thought_number}/{total_thoughts} for session {effective_session_id}")
        return {
            "success": True,
            "thought_id": thought_id,
            "session_id": effective_session_id,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "previous_thoughts": previous_thoughts,
            "next_thought_needed": next_thought_needed
        }
    except Exception as e:
        raise handle_chroma_error(e, "sequential_thinking")

def _find_similar_thoughts_impl(
    query: str,
    n_results: int = 5,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    session_id: str = "",
    include_branches: bool = True # Note: include_branches not currently used in filter
) -> Dict[str, Any]:
    """Implementation logic for finding similar thoughts."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client, get_embedding_function

    try:
        client = get_chroma_client()
        collection = client.get_collection(
            name=THOUGHTS_COLLECTION,
            embedding_function=get_embedding_function()
        )
        
        where = None
        if session_id:
            where = {"session_id": session_id}
            # TODO: Add branch filtering logic if needed based on include_branches
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        similar_thoughts = []
        if results and results.get("ids") and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                similarity = 1 - distance
                
                if similarity >= threshold:
                    raw_meta = results["metadatas"][0][i] or {}
                    reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                    base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                    if reconstructed_custom:
                        base_meta['custom_data'] = reconstructed_custom
                    thought = {
                        "content": results["documents"][0][i],
                        "metadata": base_meta,
                        "similarity": similarity
                    }
                    similar_thoughts.append(thought)
        
        return {
            "similar_thoughts": similar_thoughts,
            "total_found": len(similar_thoughts),
            "threshold": threshold
        }
    except Exception as e:
        if "does not exist" in str(e):
             logger.warning(f"Collection '{THOUGHTS_COLLECTION}' not found during similar thought search.")
             return {"similar_thoughts": [], "total_found": 0, "threshold": threshold, "message": f"Collection '{THOUGHTS_COLLECTION}' not found."}
        raise handle_chroma_error(e, "find_similar_thoughts")

def _get_session_summary_impl(
    session_id: str,
    include_branches: bool = True # Note: include_branches not currently used
) -> Dict[str, Any]:
    """Implementation logic for getting session summary."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client, get_embedding_function

    try:
        client = get_chroma_client()
        collection = client.get_collection(
            name=THOUGHTS_COLLECTION,
            embedding_function=get_embedding_function()
        )
        
        where_clause = {"session_id": session_id}
        # TODO: Add branch filtering if needed
        
        results = collection.get(
            where=where_clause,
            include=["documents", "metadatas"]
        )
        
        session_thoughts = []
        if results and results.get("ids"):
            # Sort thoughts by thought_number (requires converting from metadata)
            thought_data = []
            for i in range(len(results["ids"])):
                raw_meta = results["metadatas"][i] or {}
                reconstructed_custom = {k[len('custom:'):]: v for k, v in raw_meta.items() if k.startswith('custom:')}
                base_meta = {k: v for k, v in raw_meta.items() if not k.startswith('custom:')}
                if reconstructed_custom:
                    base_meta['custom_data'] = reconstructed_custom
                    
                thought_data.append({
                    "content": results["documents"][i],
                    "metadata": base_meta,
                    "thought_number": base_meta.get('thought_number', 9999) # Default high for sorting if missing
                })
            
            # Sort based on thought_number
            sorted_thoughts = sorted(thought_data, key=lambda x: x["thought_number"])
            
            # Remove the temporary sorting key
            session_thoughts = [{k: v for k, v in thought.items() if k != 'thought_number'} for thought in sorted_thoughts]

        return {
            "session_id": session_id,
            "session_thoughts": session_thoughts,
            "total_thoughts_in_session": len(session_thoughts)
        }
    except Exception as e:
        if "does not exist" in str(e):
             logger.warning(f"Collection '{THOUGHTS_COLLECTION}' not found during session summary.")
             return {"session_id": session_id, "session_thoughts": [], "total_thoughts_in_session": 0, "message": f"Collection '{THOUGHTS_COLLECTION}' not found or session '{session_id}' has no thoughts."}
        raise handle_chroma_error(e, f"get_session_summary({session_id})")

def _find_similar_sessions_impl(
    query: str,
    n_results: int = 3,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD
) -> Dict[str, Any]:
    """Implementation logic for finding similar sessions."""
    from ..server import get_logger
    logger = get_logger("tools.thinking")
    from ..utils.client import get_chroma_client, get_embedding_function

    try:
        client = get_chroma_client()
        sessions_collection = client.get_or_create_collection(
            name=SESSIONS_COLLECTION,
            embedding_function=get_embedding_function()
        )
        
        thought_collection = client.get_collection(
            name=THOUGHTS_COLLECTION,
            embedding_function=get_embedding_function()
        )
        all_thoughts = thought_collection.get(include=["metadatas"])
        all_session_ids = set(meta['session_id'] for meta in all_thoughts.get('metadatas', []) if meta and 'session_id' in meta)

        summaries = []
        session_ids_processed = []
        for session_id in all_session_ids:
            try:
                summary_data = _get_session_summary_impl(session_id)
                summary_text = " ".join([t['content'] for t in summary_data.get('session_thoughts', [])])
                if summary_text:
                    summaries.append(summary_text)
                    session_ids_processed.append(session_id)
            except Exception as e:
                logger.warning(f"Could not summarize session {session_id}: {e}")

        if not summaries:
            return {"similar_sessions": [], "total_found": 0}

        sessions_collection.upsert(
            ids=session_ids_processed,
            documents=summaries,
            metadatas=[{"last_updated": int(time.time())} for _ in session_ids_processed]
        )

        query_results = sessions_collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        similar_sessions = []
        session_similarities = {}
        if query_results and query_results.get("ids") and query_results["ids"][0]:
            for i in range(len(query_results["ids"][0])):
                distance = query_results["distances"][0][i]
                similarity = 1 - distance
                
                if similarity >= threshold:
                    metadata = query_results["metadatas"][0][i] or {}
                    session_id = metadata.get("session_id")
                    if session_id:
                        if session_id not in session_similarities or similarity > session_similarities[session_id]["max_similarity"]:
                            session_similarities[session_id] = {"max_similarity": similarity}
        
        # Sort sessions by max similarity and take top n_results
        sorted_sessions = sorted(session_similarities.items(), key=lambda item: item[1]["max_similarity"], reverse=True)
        top_sessions = sorted_sessions[:n_results]
        
        # Fetch summaries for top sessions
        similar_session_summaries = []
        for session_id, data in top_sessions:
            summary = _get_session_summary_impl(session_id)
            summary["similarity_score"] = data["max_similarity"] # Add score
            similar_session_summaries.append(summary)
            
        return {
            "similar_sessions": similar_session_summaries,
            "total_found": len(similar_session_summaries),
            "threshold": threshold
        }
    except Exception as e:
        if "does not exist" in str(e):
             logger.warning(f"Collection '{THOUGHTS_COLLECTION}' not found during similar session search.")
             return {"similar_sessions": [], "total_found": 0, "threshold": threshold, "message": f"Collection '{THOUGHTS_COLLECTION}' not found."}
        raise handle_chroma_error(e, "find_similar_sessions")

# --- Tool Registration --- 

def register_thinking_tools(mcp: FastMCP) -> None:
    """Register sequential thinking tools with the MCP server."""
    
    @mcp.tool()
    async def chroma_sequential_thinking(
        thought: str,
        thought_number: int,
        total_thoughts: int,
        session_id: str = "",
        branch_from_thought: int = 0,
        branch_id: str = "",
        next_thought_needed: bool = False,
        custom_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
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
        return await _sequential_thinking_impl(
            thought=thought,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            session_id=session_id,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            next_thought_needed=next_thought_needed,
            custom_data=custom_data
        )
    
    @mcp.tool()
    async def chroma_find_similar_thoughts(
        query: str,
        n_results: int = 5,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
        session_id: str = "",
        include_branches: bool = True
    ) -> Dict[str, Any]:
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
        return await _find_similar_thoughts_impl(
            query=query,
            n_results=n_results,
            threshold=threshold,
            session_id=session_id,
            include_branches=include_branches
        )
    
    @mcp.tool()
    async def chroma_get_session_summary(
        session_id: str,
        include_branches: bool = True
    ) -> Dict[str, Any]:
        """Retrieves all thoughts recorded within a specific thinking session, ordered sequentially.
        
        Allows reconstructing the entire flow of a particular thinking process or problem-solving attempt. 
        Can optionally include thoughts from defined branches.

        Args:
            session_id: The unique identifier of the thinking session to retrieve.
            include_branches: Whether to include thoughts from branched paths (currently not implemented in filter).

        Returns:
            Dictionary containing the session_id and a list of all thoughts belonging to that session.
        """
        return await _get_session_summary_impl(
            session_id=session_id,
            include_branches=include_branches
        )
    
    @mcp.tool()
    async def chroma_find_similar_sessions(
        query: str,
        n_results: int = 3,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD
    ) -> Dict[str, Any]:
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
        return await _find_similar_sessions_impl(
            query=query,
            n_results=n_results,
            threshold=threshold
        )

async def record_thought(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    session_id: Optional[str] = None,
    branch_from_thought: Optional[int] = None,
    branch_id: Optional[str] = None,
    next_thought_needed: bool = False,
    custom_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Record a thought in a sequential thinking process."""
    try:
        from ..utils.client import get_chroma_client

        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Validate inputs
        if thought_number < 1 or thought_number > total_thoughts:
            raise ValueError("Invalid thought number")
        if branch_from_thought and branch_from_thought >= thought_number:
            raise ValueError("Branch must come from an earlier thought")

        # Create thought metadata
        metadata = ThoughtMetadata(
            session_id=session_id,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            timestamp=int(time.time()),
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            next_thought_needed=next_thought_needed,
            custom_data=custom_data
        )

        # Get collections
        client = get_chroma_client()
        thoughts_collection = client.get_collection(THOUGHTS_COLLECTION)
        sessions_collection = client.get_collection(SESSIONS_COLLECTION)

        # Generate thought ID
        thought_id = f"{session_id}_{thought_number}"
        if branch_id:
            thought_id = f"{thought_id}_{branch_id}"

        # Add thought to thoughts collection
        thoughts_collection.add(
            documents=[thought],
            metadatas=[metadata.__dict__],
            ids=[thought_id]
        )

        # Update session metadata if first thought
        if thought_number == 1 and not branch_id:
            sessions_collection.add(
                documents=[f"Session started: {thought}"],
                metadatas=[{
                    "session_id": session_id,
                    "total_thoughts": total_thoughts,
                    "start_time": metadata.timestamp,
                    "status": "in_progress"
                }],
                ids=[session_id]
            )

        # Get previous thoughts in the chain
        where = {"session_id": session_id}
        if branch_id:
            where["branch_id"] = branch_id
        previous_thoughts = thoughts_collection.get(
            where=where,
            include=["documents", "metadatas"]
        )

        return {
            "success": True,
            "thought_id": thought_id,
            "session_id": session_id,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "previous_thoughts": [
                {
                    "id": id,
                    "thought": doc,
                    "metadata": meta
                }
                for id, doc, meta in zip(
                    previous_thoughts["ids"],
                    previous_thoughts["documents"],
                    previous_thoughts["metadatas"]
                )
            ],
            "next_thought_needed": next_thought_needed
        }

    except ValueError as e:
        raise McpError(ErrorData(
            code=INVALID_PARAMS,
            message=f"Invalid parameters: {str(e)}"
        ))
    except Exception as e:
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=f"Failed to record thought: {str(e)}"
        ))
