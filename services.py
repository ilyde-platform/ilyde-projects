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
import functools
import glob
import itertools
import mimetypes
import os
from minio import Minio
import config


def get_minio_client():
    client = Minio(config.MINIO_HOST, access_key=config.AWS_ACCESS_KEY_ID,
                   secret_key=config.AWS_SECRET_ACCESS_KEY, secure=False)
    return client


def create_minio_bucket(bucket_name):
    minio = get_minio_client()
    minio.make_bucket(bucket_name, 'us-west-1')
    minio.enable_bucket_versioning(bucket_name)


def list_minio_bucket_objects(bucket_name):
    minio = get_minio_client()
    objects = minio.list_objects_v2(bucket_name, recursive=True, include_version=True)

    data = []
    for k, g in itertools.groupby(sorted(objects, key=lambda obj: obj.object_name), lambda obj: obj.object_name):
        ob = functools.reduce(
            lambda obj_a, obj_b: obj_a if obj_a.last_modified > obj_b.last_modified else obj_b,
            g)
        data.append({'name': ob.object_name, 'version': ob.version_id})

    return data


def sync_dir_to_minio_bucket(bucket_name, dirpath):
    minio = get_minio_client()
    results = []
    for root, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            pathfile = os.path.join(root, filename)
            key = os.path.relpath(pathfile, dirpath).replace('\\', '/')
            file_type, _ = mimetypes.guess_type(pathfile)
            if file_type is None:
                file_type = 'application/octet-stream'
            etag, version = minio.fput_object(bucket_name, key, pathfile, content_type=file_type)
            results.append({'name': key, 'version': version})

    return results
