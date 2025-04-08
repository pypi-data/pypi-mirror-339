from urllib.parse import urlparse

from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)

        # Lấy db_name từ MongoDB URI
        parsed_uri = urlparse(uri)
        db_name = parsed_uri.path.lstrip("/")  # Lấy tên DB từ URI

        self.db = self.client[db_name]

    def close(self):
        self.client.close()


# 👉 Sử dụng không cần truyền db_name
# mongo = MongoDB("mongodb+srv://lochoang611:K8ZvBbaPL8jvyLEa@cluster0.nnwioc9.mongodb.net/example")

# project = Project(title="Test Project", description="This is a test project", instructions="This is a test project")
# print(mongo.insert_project(project))
# mongo.close()
