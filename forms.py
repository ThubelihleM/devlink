from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length

class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    github = StringField('GitHub', validators=[Length(max=100)])
    tech_stack = StringField('Tech Stack (comma-separated)', validators=[Length(max=100)])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Save Profile')
