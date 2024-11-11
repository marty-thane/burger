from neomodel import StructuredNode, StringProperty, UniqueIdProperty, DateTimeProperty, RelationshipTo, RelationshipFrom
from datetime import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True, required=True, max_length=20)
    password = StringProperty(required=True, max_length=64) # hash with sha256
    posts = RelationshipTo("Post", "POSTED")
    comments = RelationshipTo("Comment", "COMMENTED")
    follows = RelationshipTo("User", "FOLLOWED")
    likes = RelationshipTo("Post", "LIKED")

class Post(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    user = RelationshipFrom("User", "POSTED")
    comments = RelationshipTo("Comment", "HAS")

class Comment(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    user = RelationshipFrom("User", "COMMENTED")
    post = RelationshipFrom("Post", "HAS")
