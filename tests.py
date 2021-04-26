# -*- coding: utf-8 -*-
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

import unittest
import logging
import grpc
from protos import project_pb2_grpc, project_pb2
import server

# setup logger
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class ProjectServicerTest(unittest.TestCase):

    def setUp(self):
        self._server, port = server.create_server('[::]:0')
        self._server.start()
        self._channel = grpc.insecure_channel('localhost:%d' % port)

    def tearDown(self):
        self._channel.close()
        self._server.stop(None)

    def test_search(self):
        logger.info("test search project")
        stub = project_pb2_grpc.ProjectServicesStub(self._channel)
        # TODO: create a function that create fake projects for search purpose
        # prepare a payload
        payload = {
            'page': 1,
            'limit': 1,
            'query': {'name': 'Iris Classification Context'}
        }
        response = stub.Search(project_pb2.SearchProjectRequest(**payload))
        self.assertTrue(response.total == 3)
        response = stub.Search(project_pb2.SearchProjectRequest(**payload))
        self.assertEqual(response.total, 3)
        self.assertEqual(len(response.projects), 1)


if __name__ == '__main__':
    logger.info("tests ProjectServicer")
    unittest.main(verbosity=2)
