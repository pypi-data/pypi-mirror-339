from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class WorkspaceSchema(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    workspace_id: Optional[str] = Field(
        description="The id of the workspace", default=None
    )
    title: str = Field(description="The name of the project")
    user_id: str = Field(description="The id of the user")
    chat_session: list[str]
    description: str = Field(description="The description of the project")
    instructions: str = Field(description="The instructions of the project")

    class Config:
        arbitrary_types_allowed = True
        # Cấu hình cho ObjectId vì Pydantic không hỗ trợ ObjectId mặc định
        json_encoders = {ObjectId: str}
