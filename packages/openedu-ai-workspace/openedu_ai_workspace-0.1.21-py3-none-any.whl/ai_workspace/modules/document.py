from ai_workspace.schemas import DocumentSchema
from ai_workspace.database import MongoDB
from snowflake import SnowflakeGenerator


class Document:
    def __init__(self, mongodb_url: str):
        self.mongodb = MongoDB(mongodb_url)
        self.id_generator = SnowflakeGenerator(42)

    def upload_document(self, document_data: DocumentSchema):
        document_data.document_id = next(self.id_generator)
        documents_dict = document_data.model_dump(exclude_unset=True)
        collection = self.mongodb.db["documents"]
        result = collection.insert_one(documents_dict).inserted_id
        return str(result)


test = Document(
    mongodb_url="mongodb+srv://lochoang611:K8ZvBbaPL8jvyLEa@cluster0.nnwioc9.mongodb.net/example"
)

document = DocumentSchema(
    doc_url="1",
    file_name="example.pdf",
    file_type="pdf",
    session_id="abc123",
    workspace_id="workspace456",
    document_id=1,
)

upload_result = test.upload_document(document_data=document)
print(upload_result)
