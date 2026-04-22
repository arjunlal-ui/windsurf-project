from pymongo import MongoClient
import os

# MongoDB connection details
username = "fitpulse"
password = "fitpulse"
cluster = "cluster0.hcahccp.mongodb.net"

# Connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

try:
    # Connect to MongoDB
    client = MongoClient(connection_string)
    
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
    
    # List databases
    databases = client.list_database_names()
    print(f"\nAvailable databases: {databases}")
    
    # Close connection
    client.close()
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
