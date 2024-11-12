from flask import Flask, render_template, redirect, url_for, session, flash, request
from neomodel import config
from forms import LoginForm, PostForm, CommentForm
from models import User, Post, Comment
from helpers import get_heading
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

config.DATABASE_URL = f"bolt://neo4j:{os.getenv('NEO4J_PASSWORD')}@neo4j:7687"

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login() -> None:
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        create_account = form.create_account.data
        if create_account:
            user = User.nodes.get_or_none(username=username)
            if not user:
                user = User(username=username, password=password).save()
                session["uid"] = user.uid
                return redirect(url_for("home"))
            else:
                flash("This username is already taken.")
                return redirect(url_for("login"))
        else:
            user = User.nodes.get_or_none(username=username, password=password)
            if user:
                session["uid"] = user.uid
                return redirect(url_for("home"))
            else:
                flash("Wrong username or password.")
                return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route("/home", methods=["GET", "POST"])
def home() -> None:
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        post = Post(content=content).save()
        user = User.nodes.get(uid=session["uid"])
        user.posts.connect(post)
        return redirect(url_for("home"))

    users_posts = [(post.user.single(), post) for post in Post.nodes.order_by("-time").all()]

    return render_template("home.html", form=form, heading=get_heading(), users_posts=users_posts)

@app.route("/people")
def people() -> None:
    return render_template("people.html", heading=get_heading())

@app.route("/post", methods=["GET", "POST"])
def post() -> None:
    post_uid = request.args.get("uid")
    post = Post.nodes.get_or_none(uid=post_uid)
    if not post:
        return render_template("404.html", heading="Page not found")

    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content).save()
        user = User.nodes.get(uid=session["uid"])
        comment.user.connect(user)
        comment.post.connect(post)
        return redirect(url_for("post", uid=post_uid))

    users_comments = [(comment.user.single(), comment) for comment in post.comments.order_by("-time").all()]

    return render_template("post.html", form=form, heading=get_heading(), post=post, users_comments=users_comments)

@app.route("/user")
def user() -> None:
    user_uid = request.args.get("uid")
    user = User.nodes.get_or_none(uid=user_uid)
    if not post:
        return render_template("404.html", heading="Page not found")

    posts = user.posts.order_by("-time").all()

    return render_template("user.html", heading=get_heading(), user=user, posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
