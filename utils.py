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
import datetime
import json

from bson import ObjectId


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def create_config(project_name, description):
    return {
        'author_name': "Ilyde",
        'project_name': project_name,
        'repo_name': project_name.lower().replace(' ', '_'),
        'description': description,
        'open_source_license': "MIT",
        'python_interpreter': "python3",
    }


def construct_mongo_query(data: dict, mappings: dict, ids: list):
    query = {}
    for key, value in data.items():
        if value and key in mappings.keys():
            query[mappings[key]] = value

    for key in query.keys():
        if key in ids:
            query[key] = ObjectId(query[key])

    return query
