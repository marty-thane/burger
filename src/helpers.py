from flask import redirect, url_for, session
import inspect

# Return name of calling function
def get_heading() -> str:
    return inspect.stack()[1].function

def enforce_login() -> None:
    if not session["user"]:
        return redirect(url_for("login"))

