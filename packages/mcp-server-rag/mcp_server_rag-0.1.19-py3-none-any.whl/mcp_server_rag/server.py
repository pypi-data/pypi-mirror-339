import asyncio
import os
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.exceptions import McpError
from mcp.server.stdio import stdio_server

# Define strongly typed structures for our responses
@dataclass
class SearchResult:
    document_number: int
    content: str
    metadata: Dict[str, Any]
    relevance: str
    distance_score: float

    def to_text(self) -> str:
        metadata_formatted = "\n".join([f"{key}: {value}" for key, value in self.metadata.items()])
        return f"""
Document Number: {self.document_number}
Relevance: {self.relevance}
Distance Score: {self.distance_score}

Metadata:
{metadata_formatted}

Content:
{self.content}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Search Result: Document #{self.document_number}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]

@dataclass
class SearchResponse:
    status: str
    query: str
    results: List[SearchResult]
    message: Optional[str] = None

    def to_text(self) -> str:
        if self.status != "success":
            return f"Status: {self.status}\nMessage: {self.message or 'No additional information'}"
        
        result_texts = [result.to_text() for result in self.results]
        separator = "\n\n" + "-" * 50 + "\n\n"
        
        return f"""
Search Results for: {self.query}
Status: {self.status}
Number of Results: {len(self.results)}

{separator.join(result_texts)}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Search Results for: {self.query}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]

@dataclass
class ServerConfig:
    """Configuration for the RAG system that can be controlled through environment variables.
    
    Attributes:
        persist_dir: Directory where ChromaDB will store its data
        embedding_model_name: Path or name of the Sentence Transformer model
        n_results: Default number of results to return from searches
    """
    persist_dir: str = os.getenv('RAG_PERSIST_DIR', str(Path.home() / "Documents/chroma_db"))
    embedding_model_name: str = os.getenv(
        'RAG_EMBEDDING_MODEL', 
        str(Path.home() / "LLM/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/fa97f6e7cb1a59073dff9e6b13e2715cf7475ac9")
    )
    n_results: int = int(os.getenv('RAG_N_RESULTS', "5"))

# Global state management
class GlobalState:
    """Container for global state with proper typing"""
    def __init__(self):
        self.embedding_model: Optional[SentenceTransformer] = None
        self.chroma_client: Optional[chromadb.PersistentClient] = None
        self.collections: Dict[str, chromadb.Collection] = {}
        self.config: ServerConfig = ServerConfig()

state = GlobalState()

def initialize_services(collection_name: str) -> None:
    """Asynchronously set up our core services: embedding model and vector database."""
    try:
        # Ensure our data directory exists
        os.makedirs(state.config.persist_dir, exist_ok=True)
        
        # Initialize the embedding model if not already initialized
        if state.embedding_model is None:
            state.embedding_model = SentenceTransformer(state.config.embedding_model_name)
        
        # Set up the vector database connection if not already initialized
        if state.chroma_client is None:
            state.chroma_client = chromadb.PersistentClient(
                path=state.config.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )

        # Get or create collection for the specified name
        if collection_name not in state.collections:
            state.collections[collection_name] = state.chroma_client.get_or_create_collection(
                name=collection_name
            )
        
    except Exception as e:
        raise McpError(f"Initialization error: {str(e)}")

async def retrieve_context(
    query: str,
    collection_name: str
) -> str:
    """Generic search function that works with any collection."""
    try:
        # Ensure system is initialized for this collection
        if not all([state.embedding_model, collection_name in state.collections]):
            initialize_services(collection_name)
        
        # Generate query embedding
        query_embedding = state.embedding_model.encode([query], convert_to_numpy=True)
        
        # Perform vector search with error checking
        try:
            results = state.collections[collection_name].query(
                query_embeddings=query_embedding.tolist(),
                n_results=state.config.n_results,
                include=['documents', 'metadatas', 'distances']
            )
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Search operation failed: {str(e)}"
            }, indent=2)

        # Validate results structure
        if not isinstance(results, dict) or 'documents' not in results:
            return json.dumps({
                "status": "error",
                "message": "Invalid response format from database"
            }, indent=2)

        # Handle empty results
        if not results['documents'] or not results['documents'][0]:
            return json.dumps({
                "status": "no_results",
                "message": "No relevant documents found for the query"
            }, indent=2)

        # Process results safely
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]

        context_entries = []
        for i in range(len(documents)):
            entry = {
                "document_number": i + 1,
                "content": documents[i] if i < len(documents) else "",
                "metadata": metadatas[i] if i < len(metadatas) else {},
                "relevance": "High" if distances[i] < 0.5 else "Medium" if distances[i] < 0.8 else "Low" if i < len(distances) else "Unknown",
                "distance_score": distances[i] if i < len(distances) else 0.0
            }
            context_entries.append(entry)

        return json.dumps({
            "status": "success",
            "query": query,
            "results": context_entries
        }, indent=2)
        
    except Exception as e:
        error_msg = f"Error during context retrieval: {str(e)}"
        return json.dumps({
            "status": "error",
            "message": error_msg
        }, indent=2)

async def get_collection_info(collection_name: str) -> str:
    """Generic function to get collection information."""
    try:
        if collection_name not in state.collections:
            initialize_services(collection_name)
        
        doc_count = state.collections[collection_name].count()
        return json.dumps({
            "status": "success",
            "collection_name": collection_name,
            "document_count": doc_count,
            "persist_directory": state.config.persist_dir,
            "embedding_model": state.config.embedding_model_name,
            "is_initialized": all([
                state.embedding_model,
                state.chroma_client,
                collection_name in state.collections
            ])
        }, indent=2)
    except Exception as e:
        error_msg = f"Error getting collection info: {str(e)}"
        return json.dumps({
            "status": "error",
            "message": error_msg
        }, indent=2)

async def serve() -> None:
    server = Server("RAG System")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """Return a list of all available tools to the MCP interface."""
        return [
            types.Tool(
                name="retrieve_liv_context",
                description="""Search for documents relevant to a given query in the liv collection.""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query.",
                            "title": "Query"
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="retrieve_ken_context",
                description="""Search for documents relevant to a given query in the ken collection.""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query.",
                            "title": "Query"
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="retrieve_ufa_context",
                description="""Search for documents relevant to a given query in the ufa collection.""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query.",
                            "title": "Query"
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="retrieve_sap_comm_context",
                description="""Search for documents relevant to a given query in the sap commerce collection.""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query.",
                            "title": "Query"
                        }
                    },
                    "required": ["query"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        # Map tool names to collection names for retrieve context tools
        retrieve_collection_mapping = {
            "retrieve_liv_context": "liv-rag",
            "retrieve_ken_context": "ken-rag",
            "retrieve_ufa_context": "ufa-rag",
            "retrieve_sap_comm_context": "sap-comm-rag"
        }

        # Map tool names to collection names for collection info tools
        collection_info_mapping = {
            "get_liv_collection_info": "liv-rag",
            "get_ken_collection_info": "ken-rag",
            "get_ufa_collection_info": "ufa-rag",
            "get_sap_comm_collection_info": "sap-comm-rag"
        }
        # Check if the tool name is in our mapping
        if name in retrieve_collection_mapping:
            if not arguments or "query" not in arguments:
                raise ValueError("Missing query argument")

            query = arguments["query"]
            collection_name = retrieve_collection_mapping[name]

            # Use retrieve_context to get the documents, metadatas, and distances
            raw_result = await retrieve_context(query, collection_name)

            # Parse the JSON result
            result_dict = json.loads(raw_result)

            if result_dict.get("status") != "success":
                # Handle error case
                return [types.TextContent(
                    type="text",
                    text=f"Error: {result_dict.get('message', 'Unknown error')}"
                )]

            # Convert raw results into SearchResult objects
            search_results = []
            for item in result_dict.get("results", []):
                search_result = SearchResult(
                    document_number=item.get("document_number", 0),
                    content=item.get("content", ""),
                    metadata=item.get("metadata", {}),
                    relevance=item.get("relevance", "Unknown"),
                    distance_score=item.get("distance_score", 0.0)
                )
                search_results.append(search_result)

            # Create a SearchResponse object
            search_response = SearchResponse(
                status=result_dict.get("status", "error"),
                query=result_dict.get("query", ""),
                results=search_results,
                message=result_dict.get("message")
            )

            # Return the formatted result
            return search_response.to_tool_result()
        # Check if the tool name is in our collection info mapping
        elif name in collection_info_mapping:
            collection_name = collection_info_mapping[name]
            return await get_collection_info(collection_name)
        else:
            raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)