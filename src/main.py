from flask import Flask, render_template, redirect
from neomodel import config
from forms import LoginForm
from models import User, Post, Comment
from dotenv import load_dotenv
import os
import base64
import inspect

app = Flask(__name__)

load_dotenv()
encoded_key = os.getenv("FLASK_SECRET_KEY")
secret_key = base64.urlsafe_b64decode(encoded_key)
app.config["SECRET_KEY"] = secret_key

config.DATABASE_URL = "bolt://neo4j:password@neo4j:7687"

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

@app.route("/home")
def home():
    return render_template("home.html", heading=get_heading())

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
