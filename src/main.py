from flask import Flask, render_template, redirect
from forms import LoginForm
from dotenv import load_dotenv
import os
import base64

load_dotenv()

encoded_key = os.getenv('FLASK_SECRET_KEY')

secret_key = base64.urlsafe_b64decode(encoded_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

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
