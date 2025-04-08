from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class DocumentSchema(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    document_id: Optional[int] = Field(
        description="The id of the document", default=None
    )
    workspace_id: str = Field(description="The id of the workspace")
    session_id: Optional[str] = Field(description="The id of the session", default=None)
    doc_url: str = Field(description="document url")
    file_name: str = Field(description="file name")
    file_type: str = Field(description="file type")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
