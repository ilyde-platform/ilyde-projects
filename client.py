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

import grpc
from google.protobuf import json_format

from protos import project_pb2
from protos import project_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.ProjectServicesStub(channel)

    try:
        payload = {
            'name': 'fashion-mnist',
            'description': 'Introduction to computer vision.',
            'visibility': 'PUBLIC',
            'template': "GENERIC",
            'owner': '1234-2344-1234-2345',
        }
        # response = stub.Create(service_pb2.Project(**payload))
        response = stub.SearchRevision(project_pb2.SearchRevisionRequest())
    except grpc.RpcError as e:
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        print(e.details(), e)
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        print(status_code.name)
        # should print `(3, 'invalid argument')`
        print(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
    else:
        print(json_format.MessageToJson(response, preserving_proto_field_name=True,
                                        including_default_value_fields=True))


if __name__ == '__main__':
    run()
