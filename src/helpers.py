from flask import redirect, url_for, session
from neomodel import db
import inspect

# Return name of calling function
def get_heading() -> str:
    return inspect.stack()[1].function

# Convert cypher query results into a list of dicts
def process_result(result):
    return [dict(zip(result[1], row)) for row in result[0]]
