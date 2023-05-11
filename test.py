import os
import pytest
from flask_login import login_user, current_user
from bson import ObjectId
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WeatherExpress import *
from WeatherExpress.forms import (UpdateAccountForm)
from WeatherExpress.models import User, Post
from WeatherExpress import application, mongo, bcrypt, mail
import sys
sys.path.append('./protobuf')
import grpc_client




@pytest.fixture(scope='module')
def test_client():
    return application.test_client()

def test_hello_world(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_get_user_image_file():
    # Insert a test user
    user_id = mongo.db.users.insert_one({'username': 'testuser', 'image_file': 'testimage.jpg'}).inserted_id
    
    # Test that get_user_image_file returns the correct image file for the inserted user
    assert get_user_image_file(str(user_id)) == 'testimage.jpg'
    
    # Remove the test user from the database
    mongo.db.users.delete_one({'_id': user_id})

def test_get_username():
    # Insert a test user
    user_id = mongo.db.users.insert_one({'username': 'testuser', 'image_file': 'testimage.jpg'}).inserted_id
    
    # Test that get_username returns the correct username for the inserted user
    assert get_username(str(user_id)) == 'testuser'
    
    # Remove the test user from the database
    mongo.db.users.delete_one({'_id': user_id})

def test_blog():
    # Call the blog function
    response = routes.blog()

    # Check that the response is a string
    assert isinstance(response, str)

    # Check that the response contains the expected HTML tags
    assert "<html>" in response
    assert "<body>" in response
    assert "<h1>" in response
    assert "<p>" in response
    assert "</html>" in response
    assert "</body>" in response
    assert "</h1>" in response
    assert "</p>" in response


def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200
    
    data = {
        'username': 'testuser',
        'email': 'testuser@test.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been created! You are now able to log in' in response.data
    
    # Test that the user was actually created in the database
    user = User.objects(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@test.com'
    
    # Test that trying to register with the same username or email results in an error
    data['username'] = 'testuser2'
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username already taken. Please choose a different one.' in response.data
    
    data['username'] = 'testuser'
    data['email'] = 'testuser2@test.com'
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already taken. Please choose a different one.' in response.data

def test_login(test_client):
    # Test with invalid credentials
    response = test_client.post('/login', data=dict(
        email='invalid@example.com',
        password='wrongpassword'
    ), follow_redirects=True)
    assert b'Login Unsuccessful' in response.data
    assert current_user.is_anonymous

    # Test with valid credentials
    response = test_client.post('/login', data=dict(
        email='valid@example.com',
        password='correctpassword'
    ), follow_redirects=True)
    assert b'Login Unsuccessful' not in response.data
    assert current_user.is_authenticated


def test_weather_chat(client):
    response = client.post('/weather_chat', json={'message': 'New York'})
    assert response.status_code == 200
    assert 'message' in response.json

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_database"
    mongo.init_app(app)

    with app.app_context():
        # Create a test user
        user = User(username='test_user', email='test@example.com', password='test_password')
        user.save()
        yield app

        # Remove the test user from the database
        mongo.db.users.delete_one({'username': 'test_user'})

def test_save_picture(app):
    """Test that save_picture saves a picture to the correct directory."""
    # Create a test picture
    with app.test_request_context():
        test_picture = app.open_resource('tests/test_picture.jpg')
        picture_fn = save_picture(test_picture)

        # Check that the picture was saved to the correct directory
        assert os.path.exists(os.path.join(app.root_path, 'static/profile_pics', picture_fn))

def test_account_route(client, app):
    """Test that the account route displays the account page for a logged-in user."""
    # Login as the test user
    client.post('/login', data={'email': 'test@example.com', 'password': 'test_password'})

    # Send a GET request to the account route
    response = client.get('/account')

    # Check that the response status code is 200 and that the correct template is used
    assert response.status_code == 200
    assert b'<h1>Account</h1>' in response.data

def test_account_route_requires_login(client, app):
    """Test that the account route requires a logged-in user."""
    # Send a GET request to the account route
    response = client.get('/account')

    # Check that the response status code is 302 (redirect) and that the user is redirected to the login page
    assert response.status_code == 302
    assert b'<h1>Login</h1>' in response.data

def test_update_account_form(app):
    """Test that the UpdateAccountForm correctly updates the User model."""
    with app.test_request_context():
        # Create a test form and populate it with test data
        form_data = {'username': 'new_username', 'email': 'new_email@example.com'}
        form = UpdateAccountForm(data=form_data)

        # Retrieve the test user from the database
        user = mongo.db.users.find_one({'email': 'test@example.com'})

        # Update the user with the form data
        form.update_user(user)

        # Check that the user was updated correctly
        assert user['username'] == 'new_username'
        assert user['email'] == 'new_email@example.com'

def test_user():
    # Insert a test user
    user = User(username='testuser', email='test@example.com', password='testpassword')
    user.save()
    yield user
    # Remove the test user from the database
    user.delete()

@pytest.fixture
def test_post(test_user):
    # Insert a test post by the test user
    post = Post(title='Test Post', content='This is a test post.', user_id=str(test_user.id))
    post_dict = post.to_dict()
    mongo.db.posts.insert_one(post_dict)
    yield post_dict
    # Remove the test post from the database
    mongo.db.posts.delete_one({'_id': ObjectId(post_dict['_id'])})

def test_new_post(client, test_user):
    # Log in as the test user
    client.post('/login', data={'email': test_user.email, 'password': 'testpassword'})
    # Submit a new post
    response = client.post('/post/new', data={'title': 'New Post', 'content': 'This is a new post.'})
    # Check that the post was added to the database
    assert mongo.db.posts.count_documents({'title': 'New Post', 'content': 'This is a new post.'}) == 1
    # Check that the user is redirected to the home page after submitting a new post
    assert response.headers['Location'] == 'http://localhost/'

def test_post(client, test_post):
    # Access the post page for the test post
    response = client.get(f'/post/{str(test_post["_id"])}')
    # Check that the response contains the post content and the user's image file
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data
    assert get_user_image_file(test_post['user_id']) in str(response.data)

def test_update_post(client, test_user, test_post):
    # Log in as the test user
    client.post('/login', data={'email': test_user.email, 'password': 'testpassword'})
    # Access the update post page for the test post
    response = client.get(f'/post/{str(test_post["_id"])}/update')
    # Check that the response contains the current post title and content
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data
    # Submit an updated post
    response = client.post(f'/post/{str(test_post["_id"])}/update', data={'title': 'Updated Post', 'content': 'This post has been updated.'})
    # Check that the post was updated in the database
    assert mongo.db.posts.count_documents({'title': 'Updated Post', 'content': 'This post has been updated.'}) == 1
    # Check that the user is redirected to the post page after updating the post
    assert response.headers['Location'] == f'http://localhost/post/{str(test_post["_id"])}'

@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        with application.app_context():
            yield client

def test_user_posts(client):
    response = client.get('/user/test_user')
    assert response.status_code == 404
    
def test_reset_request(client):
    response = client.get('/reset_password')
    assert response.status_code == 200
    assert b'Reset Password' in response.data

def test_reset_request_post(client):
    response = client.post('/reset_password', data=dict(email='test@test.com'))
    assert response.status_code == 302

def test_reset_request_post_invalid_email(client):
    response = client.post('/reset_password', data=dict(email='invalidemail'))
    assert response.status_code == 200
    assert b'Invalid email address.' in response.data


def test_reset_token(client, init_database):
    # Create a user and generate a reset token
    user = User(username='testuser', email='testuser@test.com', password='password')
    mongo.db.users.insert_one(user.to_dict())
    token = user.get_reset_token()

    # Test GET request to reset_token with valid token
    response = client.get(f'/reset_password/{token}')
    assert response.status_code == 200
    assert b'Reset Password' in response.data

    # Test POST request to reset_token with valid token and new password
    new_password = 'new_password'
    response = client.post(f'/reset_password/{token}', data={'password': new_password, 'confirm_password': new_password})
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/login'

    # Verify that the user's password has been updated
    updated_user = mongo.db.users.find_one({'username': 'testuser'})
    assert bcrypt.check_password_hash(updated_user['password'], new_password)

    # Test GET request to reset_token with invalid token
    response = client.get('/reset_password/invalid_token')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reset_request'

    # Test POST request to reset_token with invalid token and new password
    response = client.post('/reset_password/invalid_token', data={'password': new_password, 'confirm_password': new_password})
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reset_request'


if __name__ == '__main__':
    import pytest
    pytest.main(['-v'])