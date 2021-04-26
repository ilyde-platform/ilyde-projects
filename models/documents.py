# encoding: utf-8
#
# Copyright (c) 2020-2021 Hopenly srl.
#
# This file is part of Ilyde.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
