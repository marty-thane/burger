from flask import Flask, render_template, redirect
from neomodel import config
from forms import LoginForm
from models import User, Post, Comment

config.DATABASE_URL = "bolt://neo4j:neo4j@neo4j:7687"

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ...
        return redirect(url_for("/home"))
    else:
        return render_template("login.html", form=form)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
