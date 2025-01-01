from neomodel import StructuredNode, StructuredRel, UniqueIdProperty, StringProperty, DateTimeProperty, RelationshipTo, RelationshipFrom
from flask_login import UserMixin
from datetime import datetime

class User(StructuredNode, UserMixin):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True, required=True, max_length=20)
    password = StringProperty(required=True)
    picture = StringProperty(required=True)
    posts = RelationshipTo("Post", "POSTED", model=StructuredRel)
    comments = RelationshipTo("Comment", "COMMENTED", model=StructuredRel)
    follows = RelationshipTo("User", "FOLLOWED", model=StructuredRel)
    followers = RelationshipFrom("User", "FOLLOWED", model=StructuredRel)
    def is_active(self):
        return True
    def get_id(self):
        return str(self.uid)

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
