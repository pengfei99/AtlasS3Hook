#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import re

from atlaspyapi.client import Atlas

from atlas_s3_hook.S3Hook import S3Hook
from atlas_s3_hook.S3MetadataClient import S3MetadataClient
from atlas_s3_hook.S3PathClass import S3PathClass


class S3Scanner:
    def __init__(self, s3_client: S3MetadataClient, atlas_client: Atlas, owner="unknown") -> None:
        self.s3_client = s3_client
        self.fs = s3_client.get_fs()
        self.default_owner = owner
        self.s3_atlas_hook = S3Hook(s3_client, atlas_client)

    def scan_path(self, path: str, description: str = "generated by s3 atlas hook") -> None:
        path_queue = []
        # init path_queue with sub content of the current path
        # create the meta data for root path and
        path_class = self.s3_client.get_class_from_path(path)
        # for bucket
        if path_class == S3PathClass.BUCKET:
            # load metadata
            self.add_bucket(path, description)
            path_queue = self.populate_queue(path_queue, path)
        # for directory
        elif path_class == S3PathClass.DIR:
            self.add_dir(path, description)
            path_queue = self.populate_queue(path_queue, path)
        elif path_class == S3PathClass.OBJECT:
            # avoid loading .keep file
            self.add_object(path, description)
        else:
            raise ValueError
        # loop the path_queue
        while len(path_queue) > 0:
            # pop the first element of the queue
            current_path = path_queue.pop(0)
            current_path_class = self.s3_client.get_class_from_path(current_path)
            if current_path_class == S3PathClass.DIR:
                self.add_dir(current_path, description)
                path_queue = self.populate_queue(path_queue, current_path)
            elif current_path_class == S3PathClass.OBJECT:
                self.add_object(current_path, description)

    # helper function to populate the queue path with sub content of the current path
    def populate_queue(self, queue, target_path: str):
        contents = self.fs.ls(target_path)
        logging.info(f"populate_queue: sub content of target path value: {contents}")
        # there is a bug in s3fs, if the directory is empty, the fs.ls does not return an empty list.
        # it returns a list where the first element is the empty directory name
        # walk around for the s3fs bug, remove the parent directory name manually
        if len(contents) == 1 and (target_path in contents):
            return queue
        # if contents is empty, return the origin queue
        # empty list in python is false, bool()
        elif (contents is None) or (bool(contents) == False):
            return queue
        else:
            for item in contents:
                logging.info(f"sub path element:{item}")
                queue.append(item)
            return queue

    # check if the given file_name is in the ignore list or not
    @staticmethod
    def is_ignored(file_name: str, ignored_file_pattern=None) -> bool:
        # Make a regex that matches if any of our regexes match.
        # by default, we ignore all file started by "." (e.g. .keep), we can add other regex in the list
        # ^\. means filename starts with . and followed by any number of any character
        # because . is special character, so we need to use \\ to protect it. without \\, . means any character.
        if ignored_file_pattern is None:
            ignored_file_pattern = ["^\\..*", "^_.*"]
        # file_name may be a abs path, in that case we need to extract the last part of the file and compare it
        file_name = file_name.split("/").pop()
        combined = "(" + ")|(".join(ignored_file_pattern) + ")"
        return True if re.match(combined, file_name) else False

    def add_bucket(self, bucket_name: str, description: str = "generated by s3 atlas hook") -> None:
        bucket_meta = self.s3_client.get_path_meta_data(bucket_name)
        logging.info(f"upload meta data: {bucket_meta}")
        self.s3_atlas_hook.create_atlas_bucket(bucket_meta, description)

    def add_dir(self, dir_name: str, description: str) -> None:
        dir_meta = self.s3_client.get_path_meta_data(dir_name)
        logging.info(f"upload meta data: {dir_meta}")
        self.s3_atlas_hook.create_atlas_ps_dir(dir_meta, description)

    def add_object(self, obj_full_name: str, description: str) -> None:
        if not S3Scanner.is_ignored(obj_full_name):
            obj_meta = self.s3_client.get_path_meta_data(obj_full_name)
            logging.info(f"upload meta data: {obj_meta}")
            self.s3_atlas_hook.create_atlas_object(obj_meta, self.default_owner, description)
