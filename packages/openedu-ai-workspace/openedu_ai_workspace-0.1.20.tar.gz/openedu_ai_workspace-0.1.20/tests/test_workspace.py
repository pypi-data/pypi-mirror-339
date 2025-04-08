import os

import pytest
from dotenv import load_dotenv
from pydantic import SecretStr
from ai_workspace.modules.workspace import Workspace
from ai_workspace.schemas.workspace import WorkspaceSchema

load_dotenv()

# Test configuration with default values
TEST_QDRANT_URI = os.getenv("QDRANT_URI", "http://localhost:6333")
TEST_MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
TEST_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
TEST_QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
TEST_AZURE_API_KEY = SecretStr(os.getenv("AZURE_API_KEY", ""))
TEST_AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")
TEST_AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", "")
TEST_AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "")


@pytest.fixture
def workspace_schema() -> WorkspaceSchema:
    """Create a test workspace schema."""
    return WorkspaceSchema(
        workspace_id="test_workspace",
        title="Test Workspace",
        description="A test workspace for testing",
        chat_session=[],
        instructions="Test instructions",
        user_id="fsd23",
    )


@pytest.fixture
def workspace(workspace_schema: WorkspaceSchema) -> Workspace:
    """Create a test workspace instance."""
    return Workspace(
        qdrant_uri=TEST_QDRANT_URI,
        mongodb_url=TEST_MONGODB_URL,
        qdrant_api_key=TEST_QDRANT_API_KEY,
        qdrant_port=TEST_QDRANT_PORT,
        azure_api_key=TEST_AZURE_API_KEY,
        azure_endpoint=TEST_AZURE_ENDPOINT,
        azure_deployment_embedding=TEST_AZURE_DEPLOYMENT,
        azure_api_version=TEST_AZURE_API_VERSION,
    )


@pytest.fixture
def test_workspace_data():
    """Create test workspace data."""
    return WorkspaceSchema(
        description="A test workspace",
        instructions="Test instructions",
        chat_session=["123das", "jnvsjaj3"],
        user_id="12sdgffdgbhd3",
        title="test_title",
        workspace_id="1234567890",
    )


def test_add_workspace(workspace, test_workspace_data):
    """Test adding a new workspace."""
    workspace_id = workspace.add_workspace(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_get_instructions(workspace, test_workspace_data):
    """Test getting workspace instructions."""
    # First add a workspace
    workspace_id = workspace.add_workspace(test_workspace_data)

    # Then get instructions
    instructions = workspace.get_instructions(workspace_id)
    assert instructions == test_workspace_data.instructions

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_update_workspace(workspace, test_workspace_data):
    """Test updating a workspace."""
    # First add a workspace
    workspace_id = workspace.add_workspace(test_workspace_data)

    # Create updated data
    updated_data = WorkspaceSchema(
        description="Updated description",
        instructions="Updated instructions",
        chat_session=["new_chat1", "new_chat2"],
        user_id="new_user_id",
        title="updated_title",
        workspace_id="1234567890",
    )

    # Update workspace
    result = workspace.update_workspace(workspace_id, updated_data)
    assert result == workspace_id

    # Verify update
    updated_instructions = workspace.get_instructions(workspace_id)
    assert updated_instructions == updated_data.instructions

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_update_instructions(workspace, test_workspace_data):
    """Test updating workspace instructions."""
    # First add a workspace
    workspace_id = workspace.add_workspace(test_workspace_data)

    # Update instructions
    new_instructions = "New test instructions"
    result = workspace.update_instructions(workspace_id, new_instructions)
    assert result is True

    # Verify update
    updated_instructions = workspace.get_instructions(workspace_id)
    assert updated_instructions == new_instructions

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_delete_instructions(workspace, test_workspace_data):
    """Test deleting workspace instructions."""
    # First add a workspace
    workspace_id = workspace.add_workspace(test_workspace_data)

    # Delete instructions
    result = workspace.delete_instructions(workspace_id)
    assert result is True

    # Verify deletion
    with pytest.raises(KeyError):
        workspace.get_instructions(workspace_id)

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_delete_workspace(workspace, test_workspace_data):
    """Test deleting a workspace."""
    # First add a workspace
    workspace_id = workspace.add_workspace(test_workspace_data)

    # Delete workspace
    result = workspace.delete_workspace(workspace_id)
    assert result is True

    # Verify deletion
    with pytest.raises(KeyError):
        workspace.get_instructions(workspace_id)


def test_update_workspace_not_found(workspace, test_workspace_data):
    """Test updating non-existent workspace."""
    result = workspace.update_workspace("non_existent_id", test_workspace_data)
    assert result is None


def test_delete_workspace_not_found(workspace):
    """Test deleting non-existent workspace."""
    result = workspace.delete_workspace("non_existent_id")
    assert result is False


def test_update_instructions_not_found(workspace):
    """Test updating instructions for non-existent workspace."""
    result = workspace.update_instructions("non_existent_id", "new instructions")
    assert result is False


def test_delete_instructions_not_found(workspace):
    """Test deleting instructions for non-existent workspace."""
    result = workspace.delete_instructions("non_existent_id")
    assert result is False
