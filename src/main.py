from flask import Flask, render_template, redirect, url_for
from neomodel import config
from forms import LoginForm, PostForm, CommentForm
from models import User, Post, Comment
import os
import inspect

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

config.DATABASE_URL = f"bolt://neo4j:{os.getenv('NEO4J_PASSWORD')}@neo4j:7687"

def get_heading():
    return inspect.currentframe().f_code.co_name

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ...
        return redirect(url_for("home"))
    else:
        return render_template("login.html", form=form)

@app.route("/home", methods=["GET", "POST"])
def home():
    form = PostForm()
    if form.validate_on_submit():
        ...
        return redirect(url_for("home"))
    return render_template("home.html", form=form, heading=get_heading())

@app.route("/people")
def people():
    return render_template("people.html", heading=get_heading())

@app.route("/post")
def post():
    return render_template("post.html", heading=get_heading())

@app.route("/user")
def user():
    return render_template("user.html", heading=get_heading())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
