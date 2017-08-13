"""User related forms."""

from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, InputRequired, Email


class UsernamePasswordForm(Form):
    """Abstract form to provide common fields: username and password"""
    username = StringField('Username', [Length(min=1, max=255)])
    password = PasswordField('Password', [Length(min=1, max=255)])


class RegistrationForm(UsernamePasswordForm):
    """User registration form"""
    password2 = PasswordField('Password (repeat)', [Length(min=1, max=255)])

    first_name = StringField('First Name', [Length(min=1, max=255)])
    last_name = StringField('Last Name', [Length(min=1, max=255)])
    email = StringField('Email', [InputRequired(), Email()])


class LoginForm(UsernamePasswordForm):
    """User login form"""
    pass


class UserForm(UsernamePasswordForm):
    """User profile form"""
    username = StringField('Username', [Length(min=1, max=255)])

    password = PasswordField('Password', [Length(min=0, max=255)])
    password2 = PasswordField('Password (repeat)', [Length(min=0, max=255)])

    first_name = StringField('First Name', [Length(min=1, max=255)])
    last_name = StringField('Last Name', [Length(min=1, max=255)])
    email = StringField('Email', [InputRequired(), Email()])
