import os
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("ENVIRONMENT")
base_url = os.getenv("ROOT_PATH")

database_name = os.getenv("DATABASE_NAME")
database_host = os.getenv("DATABASE_HOST")

access_token_secret_key = os.getenv("ACCESS_TOKEN_SECRET_KEY")
access_token_duration_in_minutes = os.getenv("ACCESS_TOKEN_DURATION_IN_MINUTES")
stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe_webhook_key = os.getenv('STRIPE_WEBHOOK_KEY')


algorithm = os.getenv("ALGORITHM")






