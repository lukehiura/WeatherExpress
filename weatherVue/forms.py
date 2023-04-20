from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from weatherVue.models import User
from flask_login import current_user
from weatherVue import mongo
from pymongo.errors import OperationFailure



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        try:
            user = mongo.db.users.find_one({'username': username.data})
        except OperationFailure as e:
            raise ValidationError('Failed to query MongoDB: {}'.format(e))

        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        try:
            user = mongo.db.users.find_one({'email': email.data})
        except OperationFailure as e:
            raise ValidationError('Failed to query MongoDB: {}'.format(e))

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

        

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        try:
            user = mongo.db.users.find_one({'username': username.data})
        except OperationFailure as e:
            raise ValidationError('Failed to query MongoDB: {}'.format(e))

        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        try:
            user = mongo.db.users.find_one({'email': email.data})
        except OperationFailure as e:
            raise ValidationError('Failed to query MongoDB: {}'.format(e))

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        try:
            user = mongo.db.users.find_one({'email': email.data})
        except OperationFailure as e:
            raise ValidationError('Failed to query MongoDB: {}'.format(e))

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


