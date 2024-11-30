from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from neomodel import config
from forms import LoginForm, PostForm, CommentForm, FollowForm, PeopleForm
from models import User, Post, Comment
from helpers import get_heading
import random
import os

MAX_FEED_LENGTH = 30
MAX_RECOMMENDED_LENGTH = 5

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

config.DATABASE_URL = f"bolt://neo4j:{os.getenv('NEO4J_PASSWORD')}@neo4j:7687"

@login_manager.user_loader
def load_user(uid):
    return User.nodes.get(uid=uid)

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    # Logic for registering/logging in
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        create_account = form.create_account.data
        if create_account:
            user = User.nodes.get_or_none(username=username) # Check if user exists
            if not user:
                user = User(username=username, password=password).save() # Create new account
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("This username is already taken.")
                return redirect(url_for("login"))
        else:
            user = User.nodes.get_or_none(username=username, password=password) # Check if credentials match
            if user:
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong username or password.")
                return redirect(url_for("login"))

    return render_template("login.html", form=form, heading=get_heading())

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # Logic for submitting new posts
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        post = Post(content=content).save()
        current_user.posts.connect(post)
        return redirect(url_for("home"))

    # Get (user, post) tuples to display in feed
    #* This will get slow for bigger numbers of posts, fix it with cypher
    posts = current_user.posts.all()
    for user in current_user.follows.all():
        posts.extend(user.posts.all())
    posts = sorted(posts, key=lambda post: post.time, reverse=True)[:MAX_FEED_LENGTH] # Sort and limit
    users_posts = [(post.user.single(), post) for post in posts]

    return render_template("home.html", form=form, users_posts=users_posts, heading=get_heading())

@app.route("/people", methods=["GET", "POST"])
@login_required
def people():
    followed_users = current_user.follows.order_by("username").all()
    recommended_users = []
    for user in followed_users: #* maybe use cypher as well (may be faster)
        recommended_users.extend(user.follows.all())
    if recommended_users:
        recommended_users = random.shuffle(recommended_users)[:MAX_RECOMMENDED_LENGTH]
        

    form = PeopleForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.nodes.get_or_none(username=username)
        if user:
            return redirect(url_for("user", uid=user.uid))
        else:
            flash("This user does not exist.")
            return redirect(url_for("people"))

    return render_template("people.html", form=form, followed_users=followed_users, recommended_users=recommended_users, heading=get_heading())

@app.route("/post/<string:uid>", methods=["GET", "POST"])
@login_required
def post(uid):
    # Fetch requested post (404 if not found)
    post = Post.nodes.get_or_none(uid=uid)
    if not post:
        return render_template("404.html")
    
    # Logic for submitting comments
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content).save()
        current_user.comments.connect(comment)
        comment.post.connect(post)
        return redirect(url_for("post", uid=uid))

    # Get author of current post
    author = post.user.single()

    # Get (user, comment) tuples of comments on post
    comments = post.comments.order_by("-time").all()
    users_comments = [(comment.user.single(), comment) for comment in comments]

    return render_template("post.html", form=form, author=author, post=post, users_comments=users_comments, heading=get_heading())

@app.route("/user/<string:uid>", methods=["GET", "POST"])
@login_required
def user(uid):
    # Fetch requested user (404 if not found)
    user = User.nodes.get_or_none(uid=uid)
    if not user:
        return render_template("404.html")

    u = current_user.follows.get_or_none(uid=user.uid)
    if u:
        is_followed = True
    else:
        is_followed = False

    form = FollowForm()
    if form.validate_on_submit():
        if u:
            current_user.follows.disconnect(user)
        else:
            current_user.follows.connect(user)
        is_followed = not is_followed

    # Get list of posts published by user
    posts = user.posts.order_by("-time").all()

    return render_template("user.html", form=form, user=user, is_followed=is_followed, posts=posts, heading=get_heading())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
