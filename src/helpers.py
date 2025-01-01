import inspect
import os

# Return name of calling function
def get_heading():
    return inspect.stack()[1].function

# Return JPG files in directory as list
def get_pictures(directory):
    return [p for p in os.listdir(directory) if p.endswith(".jpg")]

# Convert cypher query results into a list of dicts
def process_result(result):
    return [dict(zip(result[1], row)) for row in result[0]]
