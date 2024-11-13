from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from neomodel import config
from forms import LoginForm, PostForm, CommentForm
from models import User, Post, Comment
from helpers import get_heading
import os

MAX_FEED_LENGTH = 30

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

config.DATABASE_URL = f"bolt://neo4j:{os.getenv('NEO4J_PASSWORD')}@neo4j:7687"

@login_manager.user_loader
def load_user(user_uid):
    return User.nodes.get_or_none(uid=user_uid)

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

    return render_template("login.html", form=form,
                           heading=get_heading())

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # Logic for submitting new posts
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        post = Post(content=content).save()
        post.user.connect(current_user)
        return redirect(url_for("home"))

    # Get (user, post) tuples to display in feed
    #* Change this once follow logic is implemented (followed users+your own posts)
    posts = Post.nodes.order_by("-time").limit(MAX_FEED_LENGTH).all()
    users_posts = [(post.user.single(), post) for post in posts]

    return render_template("home.html", form=form,
                           users_posts=users_posts,
                           heading=get_heading())

@app.route("/people")
@login_required
def people():
    followed_users = current_user.follows.order_by("username").all()
    recommended_users = None
    return render_template("people.html",
                           followed_users=followed_users,
                           recommended_users=recommended_users,
                           heading=get_heading())
    #* Change this one follow logic is implemented (recommended accounts)

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    # Fetch requested post (404 if not found)
    post_uid = request.args.get("uid")
    post = Post.nodes.get_or_none(uid=post_uid)
    if not post:
        return render_template("404.html", heading="Page not found")
    
    # Logic for submitting comments
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content).save()
        comment.user.connect(current_user)
        comment.post.connect(post)
        return redirect(url_for("post", uid=post_uid))

    # Get author of current post
    author = post.user.single()

    # Get (user, comment) tuples of comments on post
    comments = post.comments.order_by("-time").all()
    users_comments = [(comment.user.single(), comment) for comment in comments]

    return render_template("post.html", form=form,
                           author=author, post=post,
                           users_comments=users_comments,
                           heading=get_heading())

@app.route("/user")
@login_required
def user():
    # Fetch requested post (404 if not found)
    user_uid = request.args.get("uid")
    user = User.nodes.get_or_none(uid=user_uid)
    if not post:
        return render_template("404.html", heading="Page not found")

    # Get list of posts published by user
    posts = user.posts.order_by("-time").all()

    return render_template("user.html",
                           user=user, posts=posts,
                           heading=get_heading())

#* Here, a separate endpoint handling follows/likes will accept POST requests with data about what to do
@app.route("/follow")
@login_required
def follow():
    ...
#* Make up your mind wether to use wtforms or not

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
