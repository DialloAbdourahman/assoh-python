import os
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("ENVIRONMENT")
database_name = os.getenv("DATABASE_NAME")
database_host = os.getenv("DATABASE_HOST")
base_url = os.getenv("ROOT_PATH")


