# encoding: utf-8
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
