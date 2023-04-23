from pymongo import MongoClient
import datetime

mongo = MongoClient('mongodb+srv://lhiur001:0pemDaAuQTiqvR9L@profiles-db.jovxyhy.mongodb.net/?retryWrites=true&w=majority')
db = mongo.WeatherExpress
users = {
    'username':'luquifquif',
    'email': 'lhiur001@gmail.com',
    'image_file' : 'default.jpg',
    'password' : 'password123'
 }
db.users.insert_one(users)

username = 'luquifquif'
user_data = db.users.find_one({'username': username})

if user_data:
    # Extract the user_id from the user document
    user_id = user_data['_id']
    print('User ID:', user_id)
else:
    print('User not found')

posts = {
    'title':'luquifquif',
    'date_posted': datetime.datetime.utcnow(),
    'content' : 'My first post',
    'user_id' : user_id
}

db.posts.insert_one(posts)

# Example code for initiating database for User and Post:'

# users = {
#             'username' : self._username,
#             'email' : self._email,
#             'image_file' : self._image_file,
#             'password' : self._password
#         }

# post_data = {
#             'title': self.title,
#             'date_posted': self.date_posted,
#             'content': self.content,
#             'user_id': self.user_id
#         }