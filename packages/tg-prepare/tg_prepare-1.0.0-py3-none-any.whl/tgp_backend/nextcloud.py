# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de

import logging

import nextcloud
import os

log = logging.getLogger(__name__)


class Nextcloud:
    def __init__(
        self,
        nextcloud_url=None,
        username=None,
        password=None,
        root_dir=None,
        **kwargs,
    ):
        self._nxc = None
        self._root = None
        self.nextcloud_url = nextcloud_url
        self.username = username
        self.password = password
        self.root_dir = root_dir

    def test_connection(self):
        if all([self.nextcloud_url, self.username, self.password]):
            return str(self.nxc.list_folders().status_code).startswith("2")
        return False

    @property
    def nxc(self):
        if self._nxc is None:
            self._nxc = nextcloud.NextCloud(
                endpoint=self.nextcloud_url,
                user=self.username,
                password=self.password,
            )
        return self._nxc

    @property
    def root(self):
        if self._root is None:
            log.debug("start get_folder")
            self._root = self.nxc.get_folder(self.root_dir)
            if self._root is None:
                raise "Could not find the Root Directory"
        return self._root

    def nxc_list_files_and_folders(self):

        def _list_rec(item):
            items = []
            for d in item.list():
                if d.isdir():
                    children = _list_rec(d)
                    items.append(
                        {
                            "type": "folder",
                            "name": d.basename(),
                            "path": d.get_relative_path(),
                            "children": {
                                "count": len(children),
                                "list": children,
                            },
                        }
                    )
                else:
                    items.append({"type": "file", "name": d.basename()})
            return items

        return _list_rec(self.root)

    def download_nxc_files(self, file_paths, projectname):
        for path in file_paths:
            # Retrieve element (file or folder) from the server
            try:
                element = self.nxc.get_folder(path)
                log.debug(f"Processing {path} in project {projectname}")

                # Determine destination folder
                destination_folder = (
                    f"projects/{projectname}/data/{element.basename()}"
                )
                log.debug(f"Destination folder: {destination_folder}")

                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                # Recursive function to download files and folders
                def download_recursive(
                    current_element, current_path, current_dest
                ):
                    for item in current_element.list():
                        item_path = os.path.join(current_path, item.basename())
                        if item.isdir():
                            # If it's a folder, create subfolder and continue
                            # recursively
                            new_dest = os.path.join(
                                current_dest, item.basename()
                            )
                            if not os.path.exists(new_dest):
                                os.makedirs(new_dest)
                            subfolder = self.nxc.get_folder(item_path)
                            download_recursive(subfolder, item_path, new_dest)
                        else:
                            # If it's a file, download it
                            remote_file = self.nxc.get_file(item_path)
                            target_path = os.path.join(
                                current_dest, item.basename()
                            )
                            remote_file.download(
                                target=target_path, overwrite=True
                            )
                            log.debug(f"Downloaded: {target_path}")

                # Start the recursive download
                download_recursive(element, path, destination_folder)

            except Exception as e:
                log.error(f"Error processing {path}: {str(e)}")
