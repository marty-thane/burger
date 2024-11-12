from neomodel import StructuredNode, StructuredRel, StringProperty, UniqueIdProperty, DateTimeProperty, RelationshipTo, RelationshipFrom
from datetime import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True, required=True, max_length=20)
    password = StringProperty(required=True, max_length=64) # hash with sha256
    posts = RelationshipTo("Post", "POSTED", model=StructuredRel)
    comments = RelationshipTo("Comment", "COMMENTED", model=StructuredRel)
    follows = RelationshipTo("User", "FOLLOWED", model=StructuredRel)
    likes = RelationshipTo("Post", "LIKED", model=StructuredRel)

class Post(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    user = RelationshipFrom("User", "POSTED", model=StructuredRel)
    comments = RelationshipTo("Comment", "HAS", model=StructuredRel)

class Comment(StructuredNode):
    uid = UniqueIdProperty()
    time = DateTimeProperty(default=datetime.now)
    content = StringProperty(required=True)
    user = RelationshipFrom("User", "COMMENTED", model=StructuredRel)
    post = RelationshipFrom("Post", "HAS", model=StructuredRel)
