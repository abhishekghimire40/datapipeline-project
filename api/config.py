from dotenv import load_dotenv
import os

# loading env file
load_dotenv()

# database credentials
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@localhost/{db_name}"

CHUNK_SIZE = 1024 * 1024  # 1mb to read at once
UPLOAD_DIRECTORY = "./uploads/"
