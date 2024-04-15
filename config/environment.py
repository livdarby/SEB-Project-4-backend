from os import environ

db_URI = "postgresql://localhost:5432/predictions_db"
SECRET = environ.get("SECRET")
API_KEY = environ.get("API_KEY")
