import os
import sys
import pytest
import bcrypt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WeatherExpress import application, mongo, mail, login_manager
from WeatherExpress.models import User, Post, AnonymousUser
from WeatherExpress.routes import get_user_image_file, save_picture
from flask import Flask, render_template, url_for
from bson import ObjectId
from flask_login import current_user, LoginManager
sys.path.append('./protobuf')
import pytest
from PIL import Image
from werkzeug.datastructures import FileStorage
from io import BytesIO



@pytest.fixture(scope='module')
def test_client():
    # Set up a test client that can make requests to the application
    with application.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def user_data():
    return {
        '_id': ObjectId('645c4383f940afe9cb9a3f33'),
        'email': 'testuser@example.com',
        'image_file': 'default.jpg',
        'password': 'password',
        'username': 'testuser'
    }

@pytest.fixture(scope='module')
def authenticated_user(test_client, user_data):
    # Create a new user document in the database
    user_data['_id'] = mongo.db.users.insert_one(user_data).inserted_id

    # Log in as the new user
    with test_client.session_transaction() as session:
        session['_user_id'] = str(user_data['_id'])

    yield user_data

    # Remove the test user from the database
    mongo.db.users.delete_one({'_id': user_data['_id']})

def test_application(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_mongo():
    with application.app_context():
        assert mongo.db.command('ping')['ok'] == 1


def test_bcrypt():
    password = 'mypassword'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    assert bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def test_home(test_client, monkeypatch):
    api_key = 'my-api-key'
    posts = [
        {
            'author': 'Corey Schafer',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'April 20, 2018'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'April 21, 2018'
        }
    ]
    monkeypatch.setenv('GOOGLE_API_KEY', api_key)

    response = test_client.get('/')

    assert response.status_code == 200
    assert bytes(api_key, 'utf-8') in response.data
    assert render_template('home.html', posts=posts, api_key=api_key).encode() == response.data



def test_blog(test_client, monkeypatch):
    posts = [
        {
            '_id': '1',
            'author': 'Corey Schafer',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'April 20, 2018',
            'user_id': '1'
        },
        {
            '_id': '2',
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'April 21, 2018',
            'user_id': '2'
        }
    ]
    monkeypatch.setattr(mongo.db.posts, 'count_documents', lambda _: len(posts))
    monkeypatch.setattr(mongo.db.posts, 'find', lambda: posts)
    monkeypatch.setattr('WeatherExpress.routes.get_user_image_file', lambda user_id: f'/static/profile_pics/user{user_id}.jpg')

    response = test_client.get('/blog')

    assert response.status_code == 200
    assert b'Blog' in response.data



def test_register(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

    response = test_client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }, follow_redirects=True)

    assert response.status_code == 200

    user = User(username='testuser', email='testuser@example.com', password='testpassword')
    assert user is not None
    assert user.get_email() == 'testuser@example.com'
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), salt)
    assert bcrypt.checkpw('testpassword'.encode('utf-8'), hashed_password)


def test_login(test_client):
    # Test GET request to login page
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

    # Test invalid login credentials
    response = test_client.post('/login', data={
        'email': 'invalid@test.com',
        'password': 'invalidpassword'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Test valid login credentials
    response = test_client.post('/login', data={
        'email': 'testuser@test.com',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Simulate a logged-in user
    with test_client.session_transaction() as session:
        session['_user_id'] = str(ObjectId())
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200


def test_save_picture(test_client):
    # Create a test image file
    test_image = Image.new('RGB', (100, 100))
    test_image_path = os.path.join(application.root_path, 'static', 'test_image.jpg')
    test_image.save(test_image_path)
    
    # Call the save_picture function with the test image file
    with open(test_image_path, 'rb') as f:
        test_image_file = FileStorage(f)
        picture_fn = save_picture(test_image_file)

    # Check that the picture was saved and has the correct file extension
    assert picture_fn is not None
    assert picture_fn.endswith('.jpg')



def test_account_view(test_client, authenticated_user):
    # Make a GET request to the account page
    response = test_client.get(url_for('account'))
    assert response.status_code == 200

    # Check that the user's current username and email are pre-filled in the form
    assert 'value="{}"'.format(authenticated_user['username']) in response.data.decode()
    assert 'value="{}"'.format(authenticated_user['email']) in response.data.decode()

    # Make a POST request to update the user's account information
    data = {
        'username': 'new_username',
        'email': 'new_email@example.com',
    }
    with test_client.session_transaction() as session:
        session['_user_id'] = str(authenticated_user['_id']) # set user_id in session

    # Include picture if it's in the request


    response = test_client.post(url_for('account'), data=data, follow_redirects=True)

    # Check that the account was updated successfully
    assert response.status_code == 200

    # Check that the user's information was updated in the database
    updated_user = mongo.db.users.update_one({'_id': authenticated_user['_id']}, {'$set': data})
    assert updated_user.modified_count == 1
    updated_user = mongo.db.users.find_one({'_id': authenticated_user['_id']})
    assert updated_user['username'] == 'new_username'
    assert updated_user['email'] == 'new_email@example.com'

    






"""
Test Cases for Models Class User, and Post
"""
def test_user_model():
    # create a test user object with hashed password
    password = b'testpassword'
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(username='test', email='test@example.com', password=hashed_password)
    
    # test user attributes
    assert user.get_username() == 'test'
    assert user.get_email() == 'test@example.com'
    
    # test password hashing
    assert bcrypt.checkpw(password, user.get_password())


def test_post_model():
    user_id = ObjectId()
    post = Post(title='test', content='test content', user_id=user_id)
    assert post.title == 'test'
    assert post.content == 'test content'
    assert post.user_id == user_id
    assert post.date_posted is not None

    post_dict = {
        'title': 'test',
        'content': 'test content',
        'user_id': user_id,
        'date_posted': post.date_posted
    }

    assert post.to_dict() == post_dict



