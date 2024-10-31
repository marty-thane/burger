from flask import Flask, render_template

app = Flask(__name__)

navitems = {
        "Home": "/home",
        "Explore": "/explore",
        "Profile": "/profile",
        "New Post": "/newpost",
        }

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", navitems=navitems)

@app.route("/explore")
def explore():
    return render_template("explore.html", navitems=navitems)

@app.route("/profile")
def profile():
    return render_template("profile.html", navitems=navitems)

@app.route("/newpost")
def newpost():
    return render_template("newpost.html", navitems=navitems)

@app.route("/post")
def post():
    return render_template("post.html", navitems=navitems)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
