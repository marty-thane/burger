from flask import redirect, url_for, session
from neomodel import db
import inspect

# Return name of calling function
def get_heading() -> str:
    return inspect.stack()[1].function

def get_feed():
    query = """
    MATCH (u:User)-[:POSTS]->(p:Post)
    RETURN u.username AS author, p.time AS time, p.content AS content
    ORDER BY p.time DESC
    """
    result = db.cypher_query(query)
    return process_result(result)

# Convert cypher query results into a list of dicts
def process_result(result):
    return [dict(zip(result[1], row)) for row in result[0]]
