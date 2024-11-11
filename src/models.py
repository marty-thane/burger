from neomodel import StructuredNode, UniqueIdProperty, StringProperty, DateTimeProperty, RelationshipTo
from datetime import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True, required=True, max_length=20)
    password = StringProperty(required=True, max_length=64) # hash with sha256
    posted = RelationshipTo("Post", "POSTED")
    commented = RelationshipTo("Comment", "COMMENTED")
    followed = RelationshipTo("User", "FOLLOWED")
    liked = RelationshipTo("Post", "LIKED")

class Post(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)

class Comment(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    commented_on = RelationshipTo("Post", "COMMENTED_ON")
