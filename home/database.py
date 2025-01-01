import os
from dotenv import load_dotenv
from google.cloud import bigquery

# Load environment variables
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Configure BigQuery Client
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE) if SERVICE_ACCOUNT_FILE else None
