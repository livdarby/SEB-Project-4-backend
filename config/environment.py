import os

db_URI = os.getenv("DATABASE_URL", "postgresql://localhost:5432/predictions_db")
SECRET = os.getenv("SECRET")
API_KEY = os.getenv("API_KEY")

if db_URI.startswith("postgres://"):
    db_URI = db_URI.replace("postgres://", "postgresql://", 1)
