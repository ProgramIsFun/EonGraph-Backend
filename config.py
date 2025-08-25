import os

from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")