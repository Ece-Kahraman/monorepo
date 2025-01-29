import os
from dotenv import load_dotenv

from sqlalchemy import create_engine

load_dotenv()

_URL = "postgresql://" + os.environ.get("_DATABASE_URL")
engine = create_engine(_URL)
