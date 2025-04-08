from typing import List, Optional, Union
import logging
from functools import wraps
from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, PointStruct, VectorParams
from pydantic import SecretStr

from ai_workspace.database import MongoDB
from ai_workspace.schemas import WorkspaceSchema

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_exceptions(func):
    """Decorator for consistent error handling."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise WorkspaceError(f"Operation failed: {str(e)}")

    return wrapper


class WorkspaceError(Exception):
    """Custom exception for Workspace-related errors."""

    pass


class Workspace:
    """A class to manage vector document storage and retrieval using Qdrant and Azure OpenAI.

    This class provides functionality to store, embed, and retrieve documents using
    Qdrant vector database and Azure OpenAI embeddings.
    """

    def __init__(
        self,
        qdrant_uri: str,
        mongodb_url: str,
        qdrant_api_key: Optional[str] = None,
        qdrant_port: Optional[int] = None,
        azure_api_key: Optional[SecretStr] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment_chat: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        azure_deployment_embedding: Optional[str] = None,
        embedding_model_name: Optional[str] = None,
    ):
        """Initialize a new workspace instance.

        Args:
            qdrant_uri (str): URI for Qdrant connection
            mongodb_url (str): URL for MongoDB connection
            qdrant_api_key (Optional[str]): API key for Qdrant
            qdrant_port (Optional[int]): Port for Qdrant connection
            azure_api_key (Optional[SecretStr]): Azure OpenAI API key
            azure_endpoint (Optional[str]): Azure OpenAI endpoint
            azure_deployment_chat (Optional[str]): Azure deployment for chat
            azure_api_version (Optional[str]): Azure API version
            azure_deployment_embedding (Optional[str]): Azure deployment for embeddings
            embedding_model_name (Optional[str]): Name of the embedding model
        """
        if not qdrant_uri:
            raise ValueError("Qdrant URI is required")
        if not mongodb_url:
            raise ValueError("MongoDB URL is required")

        self.qdrant_uri = qdrant_uri
        self.mongodb_url = mongodb_url
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_port = qdrant_port
        self.azure_api_key = azure_api_key
        self.azure_endpoint = azure_endpoint
        self.azure_deployment_chat = azure_deployment_chat
        self.azure_api_version = azure_api_version
        self.azure_deployment_embedding = azure_deployment_embedding
        self.embedding_model_name = embedding_model_name or "text-embedding-3-large"

        self._init_clients()
        self._init_embedding_model()

    def _init_clients(self):
        """Initialize database clients."""
        try:
            self.client = QdrantClient(
                url=self.qdrant_uri, api_key=self.qdrant_api_key, port=self.qdrant_port
            )
            self.mongodb = MongoDB(self.mongodb_url)
            logger.info("Database clients initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database clients: {e}")
            raise WorkspaceError("Failed to initialize database connections")

    def _init_embedding_model(self):
        """Initialize the embedding model."""
        try:
            self.embedding_model = self._get_embedding_model()
            self.dimensions = len(self.embedding_model.embed_query("Hi"))
            logger.info(
                f"Embedding model initialized with dimensions: {self.dimensions}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise WorkspaceError("Failed to initialize embedding model")

    @handle_exceptions
    def get_instructions(self, workspace_id: str) -> str:
        """Get instructions from database schema.

        Args:
            workspace_id (str): The ID of the workspace

        Returns:
            str: The instructions for the workspace

        Raises:
            WorkspaceError: If workspace is not found or has no instructions
        """
        workspace = self.mongodb.db["workspaces"].find_one(
            {"workspace_id": workspace_id}
        )
        if not workspace or "instructions" not in workspace:
            raise WorkspaceError(
                f"Workspace {workspace_id} not found or has no instructions"
            )
        return workspace["instructions"]

    @handle_exceptions
    def save_points(self, collection_name: str, points: List[PointStruct]) -> None:
        """Save vector points to a Qdrant collection.

        Args:
            collection_name (str): Name of the collection
            points (List[PointStruct]): List of points to save

        Raises:
            WorkspaceError: If saving points fails
        """
        if not self.client.collection_exists(collection_name=collection_name):
            if not isinstance(self.dimensions, int):
                raise WorkspaceError(f"Invalid dimensions value: {self.dimensions}")

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.dimensions,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Created new collection: {collection_name}")

        self.client.upsert(collection_name=collection_name, points=points)
        logger.info(
            f"Successfully saved {len(points)} points to collection {collection_name}"
        )

    @handle_exceptions
    def retrieve_document(
        self,
        query: str,
        collection_name: str,
        top_k: int = 5,
        threshold: Optional[float] = None,
        filter: Optional[models.Filter] = None,
    ) -> Union[List, None]:
        """Retrieve similar documents based on a query string.

        Args:
            query (str): Query text to search for similar documents
            collection_name (str): Name of the collection to search in
            top_k (int, optional): Number of similar documents to return
            threshold (float, optional): Score threshold for filtering results
            filter (models.Filter, optional): Additional filter criteria

        Returns:
            List[Document] or None: List of similar documents if successful
        """
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding_model,
        )

        found_docs = vector_store.similarity_search(
            query, k=top_k, filter=filter, score_threshold=threshold
        )
        logger.info(
            f"Retrieved {len(found_docs) if found_docs else 0} documents from {collection_name}"
        )
        return found_docs

    def _get_embedding_model(self) -> AzureOpenAIEmbeddings:
        """Initialize and return an Azure OpenAI embedding model.

        Returns:
            AzureOpenAIEmbeddings: Configured embedding model instance

        Raises:
            WorkspaceError: If Azure OpenAI configuration is incomplete
        """
        required_configs = [
            self.azure_api_key,
            self.azure_endpoint,
            self.azure_deployment_embedding,
            self.azure_api_version,
        ]

        if not all(required_configs):
            raise WorkspaceError("Azure OpenAI configuration is incomplete")
        return AzureOpenAIEmbeddings(
            model=self.embedding_model_name,
            api_key=self.azure_api_key,
            azure_endpoint=self.azure_endpoint,
            azure_deployment=self.azure_deployment_embedding,
            api_version=self.azure_api_version,
        )

    def add_workspace(self, workspace_data: WorkspaceSchema) -> Optional[str]:
        """Add a new workspace to MongoDB.

        Args:
            workspace_data (WorkspaceSchema): Data for the workspace to add

        Returns:
            str: ID of the newly added workspace
        """
        try:
            workspace_dict = workspace_data.model_dump(exclude_unset=True)

            # Insert data into MongoDB
            collection = self.mongodb.db["workspaces"]
            result = collection.insert_one(workspace_dict).inserted_id
            print(result)

            return str(result)

        except Exception as e:
            print(f"ERROR in add_workspace: {e}")
            return None

    def update_workspace(
        self, workspace_id: str, workspace_data: WorkspaceSchema
    ) -> Optional[str]:
        """Update an existing workspace in MongoDB.

        Args:
            workspace_id (str): ID of the workspace to update
            workspace_data (WorkspaceSchema): Data for the workspace to update

        Returns:
            str: ID of the updated workspace if successful, None if an error occurs
        """
        try:
            workspace_dict = workspace_data.model_dump(exclude_unset=True)

            # Update data in MongoDB
            collection = self.mongodb.db["workspaces"]
            result = collection.update_one(
                {"workspace_id": workspace_id},
                {"$set": workspace_dict},
            )

            if result.modified_count > 0:
                return workspace_id
            else:
                print(f"No workspace found with ID {workspace_id}")
                return None

        except Exception as e:
            print(f"ERROR in update_workspace: {e}")
            return None

    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete a workspace from MongoDB.

        Args:
            workspace_id (str): ID of the workspace to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            collection = self.mongodb.db["workspaces"]
            result = collection.delete_one({"workspace_id": workspace_id})

            if result.deleted_count > 0:
                return True
            else:
                print(f"No workspace found with ID {workspace_id}")
                return False

        except Exception as e:
            print(f"ERROR in delete_workspace: {e}")
            return False

    def update_instructions(self, workspace_id: str, instructions: str) -> bool:
        """Update instructions for a workspace.

        Args:
            workspace_id (str): ID of the workspace to update
            instructions (str): New instructions for the workspace

        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            collection = self.mongodb.db["workspaces"]
            result = collection.update_one(
                {"workspace_id": workspace_id},
                {"$set": {"instructions": instructions}},
            )

            if result.modified_count > 0:
                return True
            else:
                print(f"No workspace found with ID {workspace_id}")
                return False

        except Exception as e:
            print(f"ERROR in update_instructions: {e}")
            return False

    def delete_instructions(self, workspace_id: str) -> bool:
        """Delete instructions for a workspace.

        Args:
            workspace_id (str): ID of the workspace to delete instructions for

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            collection = self.mongodb.db["workspaces"]
            result = collection.update_one(
                {"workspace_id": workspace_id},
                {"$unset": {"instructions": ""}},
            )

            if result.modified_count > 0:
                return True
            else:
                print(f"No workspace found with ID {workspace_id}")
                return False

        except Exception as e:
            print(f"ERROR in delete_instructions: {e}")
            return False
