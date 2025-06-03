import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

class AppSettings:
    def __init__(self):
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_port = os.getenv("QDRANT_PORT")
        self.qdrant_collection = os.getenv("QDRANT_COLLECTION")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")


settings = AppSettings()