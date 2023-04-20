from pymongo import MongoClient

# Replace the MongoDB URI with your own URI
MONGO_URI = "mongodb+srv://lhiur001:0pemDaAuQTiqvR9L@profiles-db.jovxyhy.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient instance to connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database
db = client.profiles-db() 

# Access the collection
collection = db['your_collection_name']  # Replace 'your_collection_name' with the name of your collection

# Fetch all the data from the collection
cursor = collection.find()

# Iterate through the cursor to print the data
for document in cursor:
    print(document)

# Close the MongoDB connection
client.close()