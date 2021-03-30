# encoding: utf-8
from mongoengine import *
import datetime


class FileVersion(EmbeddedDocument):
    name = StringField(required=True)
    version = StringField(required=True)


class Project(Document):
    """The object Project stored in the Database"""
    name = StringField(required=True)
    description = StringField(required=True, max_length=100)
    visibility = StringField(required=True)
    template = StringField(required=True)
    owner = StringField(required=True)
    members = ListField(StringField(), required=True)
    state = StringField(required=True)
    repo_bucket = StringField(required=True)
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.id)


class Revision(Document):
    """docstring for Revision."""
    commit = StringField(required=True)
    project = ReferenceField(Project, required=True, reverse_delete_rule=2)
    author = StringField(required=True)
    file_tree = ListField(EmbeddedDocumentField(FileVersion), required=True)
    create_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'ordering': ['-create_at']
    }
