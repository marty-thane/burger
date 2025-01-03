from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8)])
    create_account = BooleanField("Create Account")
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=280)])
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=280)])
    submit = SubmitField("Comment")

class FollowForm(FlaskForm):
    follow_submit = SubmitField("Follow")
    unfollow_submit = SubmitField("Unfollow")

class PeopleForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(max=20)])
    submit = SubmitField("Search")
