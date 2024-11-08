from neomodel import StructuredNode, UniqueIdProperty, StringProperty, DateTimeProperty, RelationshipTo
from datetime import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True, required=True, max_length=20)
    password = StringProperty(required=True, max_length=64) # hash with sha256
    posts = RelationshipTo("Post", "POSTS")
    comments = RelationshipTo("Comment", "COMMENTS")
    follows = RelationshipTo("User", "FOLLOWS")
    likes = RelationshipTo("Post", "LIKES")

class Post(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)

class Comment(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    commented_on = RelationshipTo("Post", "COMMENTED_ON")
