from datetime import datetime 
from itsdangerous import URLSafeTimedSerializer as Serializer
from weatherVue import mongo, login_manager, application
from flask_login import UserMixin, current_user, AnonymousUserMixin
from bson.objectid import ObjectId
from flask import session


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        if user_id == 'None':  # Check for string 'None' as well
            return AnonymousUser()  # Return custom anonymous user object
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                image_file=user_data['image_file'],
                id=user_data['_id']
            )
    return AnonymousUser()  # Return custom anonymous user object


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.id = None  # Set id to None
        self.username = 'Anonymous'  # Set default username to 'Anonymous'
        self.email = 'Random'

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
    
    def get_username(self):
        return 
    

class User(UserMixin):
    def __init__(self, username, email, password, id=None, image_file=None):
        self._username = username
        self._email = email
        self._id = id
        self._password = password
        if image_file:
            self._image_file = image_file
        else:
            self._image_file = 'default.jpg'
    
    def to_dict(self):
        return {
            'username': self._username,
            'email': self._email,
            'id': self._id,
            'password': self._password,
            'image_file': self._image_file
        }
        

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
    
    def get_username(self):
        return self._username
    
    def get_image_file(self):
        return self._image_file
    
    def get_password(self):
        return self._password
    
    def get_email(self):
        return self._email


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
        return s.dumps({'user_id': str(self._id)}).decode('utf-8')
    
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
    def __init__(self, title, content, user_id, date_posted=None):
        self.title = title
        self.date_posted = date_posted or datetime.utcnow()
        self.content = content
        self.user_id = user_id

    def get_title(self):
        return self.title

    def get_date_posted(self):
        return self.date_posted

    def get_content(self):
        return self.content

    def get_user_id(self):
        return self.user_id


    def to_dict(self):
        """Convert Post object to a dictionary."""
        post_dict = {
            'title': self.title,
            'date_posted': self.date_posted,
            'content': self.content,
            'user_id': self.user_id
        }
        return post_dict
    

    def get_user_image_file(self):
        """Get Image file associated to user_id"""
        user = mongo.db.users.find_one({'_id': self.user_id})
        if user:
            return user['image_file']
        return None
    
    def get_username(self):
        """Retrieve the username associated with the user_id."""
        user = mongo.db.users.find_one({'_id': self.user_id})
        return user['username'] if user else None

    def save(self):
        """Insert the post object into MongoDB"""
        post_data = {
            'title': self.title,
            'date_posted': self.date_posted,
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
    
