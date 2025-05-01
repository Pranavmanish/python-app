import os
from dotenv import load_dotenv

load_dotenv()
print("CONFIG DEBUG: DATABASE_URI =", os.environ.get("DATABASE_URI"))  # Temp debug

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
