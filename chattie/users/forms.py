from chattie.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegistrationForm(FlaskForm):
    """
    Form to regiser a user.
    
    Requires passing username, email, password,
    confirm passwrod and submit.
    Username and email have to be unique.
    """
    username = StringField('Username',
                           validators=[DataRequired(), 
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), 
                                    Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if username is unique."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email is unique."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    Form to log in.
    Includes email, password and submit.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    submit = SubmitField('Login')
    

class EditUserProfile(FlaskForm):
    """
    Form to edit elementary user data and profile
    """
    username = StringField('Username',
                           validators=[DataRequired(), 
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    country = StringField('Country')
    city = StringField('City')
    about = TextAreaField('About')
    image_file = FileField('Profile picture')
    submit = SubmitField('Save changes')
