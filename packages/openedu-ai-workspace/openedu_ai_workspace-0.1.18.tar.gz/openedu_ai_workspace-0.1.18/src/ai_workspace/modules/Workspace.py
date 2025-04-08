from typing import List, Optional

from bson.objectid import ObjectId
from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, PointStruct, VectorParams

from ai_workspace.database import MongoDB
from ai_workspace.schemas import WorkspaceSchema
from pydantic import SecretStr


class Workspace:
    """A class to manage vector document storage and retrieval using Qdrant and Azure OpenAI.

    This class provides functionality to store, embed, and retrieve documents using
    Qdrant vector database and Azure OpenAI embeddings.

    Attributes:
        qdrant_uri (str): URI for Qdrant server connection
        qdrant_api_key (str): API key for Qdrant authentication
        qdrant_port (int): Port number for Qdrant server
        mongodb_url (str): URL for MongoDB connection
        azure_api_key (str): API key for Azure OpenAI
        azure_endpoint (str): Endpoint URL for Azure OpenAI
        azure_deployment (str): Deployment name for Azure OpenAI
        azure_api_version (str): API version for Azure OpenAI
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
    ):
        """Initialize a new workspace instance.

        Args:
            qdrant_uri (str): URI for Qdrant server connection
            mongodb_url (str): URL for MongoDB connection
            qdrant_api_key (str, optional): API key for Qdrant authentication
            qdrant_port (int, optional): Port number for Qdrant server
            azure_api_key (str, optional): API key for Azure OpenAI
            azure_endpoint (str, optional): Endpoint URL for Azure OpenAI
            azure_deployment (str, optional): Deployment name for Azure OpenAI
            azure_api_version (str, optional): API version for Azure OpenAI
        """
        self.qdrant_uri = qdrant_uri
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_port = qdrant_port
        self.mongodb = MongoDB(mongodb_url)
        self.azure_api_key = azure_api_key
        self.azure_endpoint = azure_endpoint
        self.azure_deployment_chat = azure_deployment_chat
        self.azure_api_version = azure_api_version
        self.azure_deployment_embedding = azure_deployment_embedding

        # Initialize Qdrant client with proper type handling
        self.client = QdrantClient(
            url=self.qdrant_uri,
            api_key=self.qdrant_api_key,
        )
        self.embedding_model = self.get_embedding_model()
        self.dimensions = self.embedding_model.dimensions

    def get_instructions(self, workspace_id: str) -> str:
        """Get instructions from database schema.

        Args:
            workspace_id (str): The ID of the workspace to get instructions for

        Returns:
            str: The instructions for the workspace

        Raises:
            KeyError: If workspace is not found or has no instructions
        """
        workspace = self.mongodb.db["workspaces"].find_one(
            {"workspace_id": ObjectId(workspace_id)}
        )
        if not workspace or "instructions" not in workspace:
            raise KeyError(f"Workspace {workspace_id} not found or has no instructions")
        return workspace["instructions"]

    def get_embedding_model(self) -> AzureOpenAIEmbeddings:
        """Initialize and return an Azure OpenAI embedding model.

        Returns:
            AzureOpenAIEmbeddings: Configured embedding model instance
        """
        if not all(
            [
                self.azure_api_key,
                self.azure_endpoint,
                self.azure_deployment_embedding,
                self.azure_api_version,
            ]
        ):
            raise ValueError("Azure OpenAI configuration is incomplete")

        model = AzureOpenAIEmbeddings(
            api_key=self.azure_api_key,
            azure_endpoint=self.azure_endpoint,
            azure_deployment=self.azure_deployment_embedding,
            api_version=self.azure_api_version,
        )
        return model

    def save_points(self, collection_name: str, points: List[PointStruct]) -> None:
        """Save vector points to a Qdrant collection.

        Creates a new collection if it doesn't exist and saves the provided points.

        Args:
            collection_name (str): Name of the collection to save points to
            points (List[PointStruct]): List of points to save in the collection
        """
        if not self.client.get_collection(collection_name=collection_name):
            # Ensure dimensions is a valid integer
            if not isinstance(self.dimensions, int):
                raise ValueError(f"Invalid dimensions value: {self.dimensions}")

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.dimensions,
                    distance=Distance.COSINE,
                ),
            )
        self.client.upsert(collection_name=collection_name, points=points)

    def retrieve_document(
        self,
        query: str,
        collection_name: str,
        top_k: int = 5,
        threshold: Optional[float] = None,
        filter: Optional[models.Filter] = None,
    ):
        """Retrieve similar documents based on a query string.

        Args:
            query (str): Query text to search for similar documents
            collection_name (str): Name of the collection to search in
            top_k (int, optional): Number of similar documents to return
            threshold (float, optional): Score threshold for filtering results
            filter (models.Filter, optional): Additional filter criteria

        Returns:
            List[Document] or None: List of similar documents if successful,
            None if an error occurs
        """
        try:
            vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embedding_model,
            )
            found_docs = vector_store.similarity_search(
                query, k=top_k, filter=filter, score_threshold=threshold
            )
            return found_docs
        except Exception as e:
            print(f"ERROR in retrieve document from source: {e}")
            return None

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
                {"workspace_id": ObjectId(workspace_id)},
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
            result = collection.delete_one({"workspace_id": ObjectId(workspace_id)})

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
                {"workspace_id": ObjectId(workspace_id)},
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
                {"workspace_id": ObjectId(workspace_id)},
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
