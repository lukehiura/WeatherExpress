import pymongo
import certifi

def test_mongodb_connection(uri):
    try:
        client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        db = client['profiles-db']
        collection = db['users']
        document = collection.find_one()
        print("MongoDB connection test successful!")
        print("First document in 'users' collection:", document)
    except Exception as e:
        print("MongoDB connection test failed:", str(e))

# Replace 'your_mongodb_uri' with your actual MongoDB URI
test_mongodb_connection('mongodb+srv://lhiur001:0pemDaAuQTiqvR9L@profiles-db.jovxyhy.mongodb.net/profiles-db?retryWrites=true&w=majority')
