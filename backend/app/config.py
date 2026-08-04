from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Read environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
ENV = os.getenv("ENV", "development")
