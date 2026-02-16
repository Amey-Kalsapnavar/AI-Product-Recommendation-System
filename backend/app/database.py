from pymongo import MongoClient

MONGO_URL = "mongodb+srv://ameyk_db_user:Ameykalsapnavar2004@cluster0.yyqousx.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["recommendation_db"]
