from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from neomodel import config
from forms import LoginForm, PostForm, CommentForm
from models import User, Post, Comment
from helpers import get_heading
import os

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
def login() -> None:
    # Logic for registering/logging in
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        create_account = form.create_account.data
        if create_account:
            user = User.nodes.get_or_none(username=username)
            if not user:
                user = User(username=username, password=password).save()
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("This username is already taken.")
                return redirect(url_for("login"))
        else:
            user = User.nodes.get_or_none(username=username, password=password)
            if user:
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong username or password.")
                return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route("/home", methods=["GET", "POST"])
@login_required
def home() -> None:
    # Logic for submitting new posts
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        post = Post(content=content).save()
        current_user.posts.connect(post)
        return redirect(url_for("home"))

    # Get (user, post) tuples to display in feed
    posts = Post.nodes.order_by("-time").all()
    users_posts = [(post.user.single(), post) for post in posts]

    return render_template("home.html", form=form, heading=get_heading(), users_posts=users_posts)

@app.route("/people")
@login_required
def people() -> None:
    ...

@app.route("/post", methods=["GET", "POST"])
@login_required
def post() -> None:
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

    # Get (user, comment) tuples of comments on post
    comments = post.comments.order_by("-time").all()
    users_comments = [(comment.user.single(), comment) for comment in comments]

    return render_template("post.html", form=form, heading=get_heading(), post=post, users_comments=users_comments)

@app.route("/user")
@login_required
def user() -> None:
    # Fetch requested post (404 if not found)
    user_uid = request.args.get("uid")
    user = User.nodes.get_or_none(uid=user_uid)
    if not post:
        return render_template("404.html", heading="Page not found")

    # Get list of posts published by user
    posts = user.posts.order_by("-time").all()

    return render_template("user.html", heading=get_heading(), user=user, posts=posts)

@app.route("/logout")
def logout() -> None:
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
