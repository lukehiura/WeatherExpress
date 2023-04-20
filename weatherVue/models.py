from datetime import datetime 
from itsdangerous import URLSafeTimedSerializer as Serializer
from weatherVue import mongo, login_manager, application
from flask_login import UserMixin
from bson.objectid import ObjectId



@login_manager.user_loader
def load_user(user_id):
    """Callback function to load a user from MongoDB based on user_id."""
    # Assuming you have a MongoDB collection named "users"
    # and the User class has a "_id" attribute as shown in the example above
    user_data = mongo.db.users.find_one({'_id': user_id})
    if user_data:
        return User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            image_file=user_data['image_file']
        )
    return None


class User(UserMixin):
    def __init__(self, username, email, password, image_file=None):
        self._username = username
        self._email = email
        self._image_file = 'default.jpg' or image_file
        self._password = password
        self._id = None
        

    def save(self):
        user_data = {
            'username' : self._username,
            'email' : self._email,
            'image_file' : self._image_file,
            'password' : self._password
        }
        result = mongo.db.users.insert_one(user_data)
        self._id = result.inserted_id
    
    def get_id(self):
        """Return a unique identifier for the user."""
        return str(self._id)

    def get(cls, user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return cls(
                username=user_data['username'],
                email=user_data['email'],
                image_file=user_data['image_file'],
                password=user_data['password']
            )
        return None
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(application.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(application.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.get(user_id)

    def __repr__(self):
        return f"User('{self._username}', '{self._email}', '{self._image_file}')"

    


class Post:
    def __init__(self, title, date_posted, content, user_id):
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.user_id = user_id

    def save(self):
        # Insert the post object into MongoDB
        post_data = {
            'title': self.title,
            'date_posted': datetime.datetime.utcnow(),
            'content': self.content,
            'user_id': self.user_id
        }
        result = mongo.db.posts.insert_one(post_data)
        self.id = result.inserted_id

    @classmethod
    def get(cls, post_id):
        # Retrieve a post object from MongoDB based on post_id
        post_data = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
        if post_data:
            return cls(
                title=post_data['title'],
                date_posted=post_data['date_posted'],
                content=post_data['content'],
                user_id=post_data['user_id']
            )
        return None

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
