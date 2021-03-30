# encoding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump
from google.protobuf import json_format

from protos.project_pb2 import Project, Status, Revision, ID, SearchProjectRequest, SearchRevisionRequest, \
    SearchProjectResponse, SearchRevisionResponse


class BaseSchema(Schema):
    # Custom options
    __proto_class__ = None
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    def parse_proto_message(self, message):
        return json_format.MessageToDict(message, **self.__decode_options__)

    @staticmethod
    def paginate(data, page: int, limit: int):
        begin = (page - 1) * limit
        end = begin + limit
        return page, limit, data[begin:end]

    @pre_load(pass_many=True)
    def decode(self, data, many, **kwargs):
        if many:
            return [self.parse_proto_message(message) for message in data]
        return self.parse_proto_message(data)

    @post_dump(pass_many=True)
    def encode(self, data, many, **kwargs):
        if many:
            return [self.__proto_class__(**message) for message in data]
        return self.__proto_class__(**data)


class ProjectSerializer(BaseSchema):
    __proto_class__ = Project

    id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    visibility = fields.Str(missing="PRIVATE")
    template = fields.Str(missing="GENERIC")
    owner = fields.Str(required=True)
    members = fields.List(fields.Str, missing=[])
    state = fields.Str(missing="OPEN")
    repo_bucket = fields.Str()
    create_at = fields.Str()
    last_update = fields.Str()


class FileVersionSerializer(Schema):
    name = fields.Str(required=True)
    version = fields.Str(required=True)


class StatusSerializer(BaseSchema):
    __proto_class__ = Status

    status = fields.Integer()
    message = fields.Str()


class RevisionSerializer(BaseSchema):
    __proto_class__ = Revision

    id = fields.Str()
    commit = fields.Str(required=True)
    project = fields.Str(required=True)
    author = fields.Str(required=True)
    file_tree = fields.List(fields.Nested(FileVersionSerializer))
    create_at = fields.Str()


class IDSerializer(BaseSchema):
    __proto_class__ = ID

    id = fields.Str(required=True)


class ProjectFilterSerializer(Schema):
    id = fields.Str()
    name = fields.Str()
    visibility = fields.Str()
    template = fields.Str()
    member = fields.Str()
    state = fields.Str()


class SearchProjectRequestSerializer(BaseSchema):
    __proto_class__ = SearchProjectRequest
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    query = fields.Nested(ProjectFilterSerializer, missing={})
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class RevisionFilterSerializer(Schema):
    id = fields.Str()
    project = fields.Str()
    author = fields.Str()


class SearchRevisionRequestSerializer(BaseSchema):
    __proto_class__ = SearchRevisionRequest
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    query = fields.Nested(RevisionFilterSerializer, missing={})
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class SearchProjectResponseSerializer(BaseSchema):
    __proto_class__ = SearchProjectResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(ProjectSerializer))


class SearchRevisionResponseSerializer(BaseSchema):
    __proto_class__ = SearchRevisionResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(RevisionSerializer))


project_serializer = ProjectSerializer()
id_serializer = IDSerializer()
revision_serializer = RevisionSerializer()
status_serializer = StatusSerializer()
search_revision_request_serializer = SearchRevisionRequestSerializer()
search_revision_response_serializer = SearchRevisionResponseSerializer()
search_project_request_serializer = SearchProjectRequestSerializer()
search_project_response_serializer = SearchProjectResponseSerializer()
