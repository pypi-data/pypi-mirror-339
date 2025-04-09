# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de
import logging
import os
import subprocess

from tg_model.collection import CollectionModeler  # type: ignore
from tg_model.tei import TEIParser  # type: ignore

from tg_model.yaml import (  # type: ignore
    CollectionConfig,
    CollectionConfigTemplate,
    ProjectConfigTemplate,
    ProjectConfig,
)

from tgp_backend.tgclient import TGclient
from tgp_backend.util import config, list_files_and_folders

log = logging.getLogger(__name__)

MAIN_PATH = config("main", "path", default="./projects")


class Project(object):
    def __init__(self, projectname):
        self.name = projectname
        self.fullpath = f"{MAIN_PATH}/{projectname}"
        self.datapath = f"{self.fullpath}/data"
        self.metadatapath = f"{self.fullpath}/metadata"
        self._main_config = None
        self._collections = None
        self._nextcloud = None

    def create(self):
        if not os.path.exists(self.fullpath):
            os.makedirs(self.fullpath)
            os.makedirs(self.datapath)
            os.makedirs(self.metadatapath)
        else:
            log.warning("Project already exists!")

    def clone_git_project(self, url):
        repo_name = url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(self.datapath, repo_name)

        if not os.path.exists(repo_path):
            subprocess.run(["git", "clone", url, repo_path])
        else:
            log.warning("Repository already exists!")

    def file_upload(self, files):
        for file in files:
            if file:
                filename = file.filename
                filepath = os.path.join(self.datapath, filename)
                directory = os.path.dirname(filepath)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file.save(filepath)

    def list_files_and_folders(self):
        print(self.datapath)
        return list_files_and_folders(self.datapath)

    @property
    def main_config(self):
        if not self._main_config:
            self._main_config = ProjectConfig(projectpath=self.metadatapath)
        return self._main_config

    @main_config.setter
    def main_config(self, tei_directories):
        self._main_config = ProjectConfigTemplate(self.metadatapath).render(
            tei_directories=tei_directories
        )

    def init_configs(self, tei_directories):
        if not self.main_config.exists():
            self.main_config = tei_directories
        else:
            self.main_config.update(tei_directories=tei_directories)
            # for tei_dir in tei_directories:z
            #     # if not self.main_config.get_subproject(inpath=tei_dir):
            #     break
        self._set_collections()

    def get_subproject_inpath(self, name):
        for subproject in self.main_config.content["subprojects"]:
            if subproject["name"] == name:
                return subproject["inpath"]
        return None

    def _set_collections(self):
        self._collections = {}
        if self.main_config.exists():
            for subproject in self.main_config.content["subprojects"]:
                collection_config = CollectionConfig(subproject["basepath"])
                if not collection_config.exists():
                    collection_config = CollectionConfigTemplate(
                        projectpath=self.metadatapath,
                        subproject=subproject,
                        files=[
                            TEIParser(fullpath=file)
                            for file in subproject["files"]
                        ],
                    ).render(overwrite=False)

                self._collections[subproject["name"]] = {
                    "config": collection_config,
                    "paths": subproject,
                    "parser": CollectionParser(collection_config),
                    "modeler": CollectionModeler(
                        subproject, self.metadatapath
                    ),
                }

    @property
    def collections(self):
        if self._collections is None:
            self._set_collections()
        return self._collections

    def get_collection(self, title):
        return self.collections.get(title)

    def get_collection_parser(self, collection):
        return CollectionParser(collection)

    def get_tgp(self, instance):
        return TGProject(self, instance)


class TGProject(object):

    def __init__(self, project, instance):
        if isinstance(project, Project):
            self.project = project
        else:
            self.project = Project(project)
        self.instance = instance
        self.main_config = self.project.main_config
        self.collections = self.project.collections
        self._tg_client = None
        self._tg_session_id = None
        self._tg_project_id = None

    @property
    def tg_session_id(self):
        if not self._tg_session_id:
            self._tg_session_id = self.main_config.get_tg_session_id(
                self.instance
            )
        return self._tg_session_id

    @tg_session_id.setter
    def tg_session_id(self, session_id):
        self._tg_session_id = session_id
        self.main_config.set_tg_session_id(session_id, self.instance)

    @property
    def tg_project_id(self):
        if not self._tg_project_id:
            self._tg_project_id = self.main_config.get_tg_project_id(
                self.instance
            )
        return self._tg_project_id

    @tg_project_id.setter
    def tg_project_id(self, project_id):
        self._tg_project_id = project_id
        self.main_config.set_tg_project_id(project_id, self.instance)

    @property
    def tg_client(self):
        if not self._tg_client:
            self._tg_client = TGclient(self.tg_session_id, self.instance)
        return self._tg_client

    def create_tg_project(self, name, instance="test", description=""):
        if not self.tg_session_id:
            return []
        tg_project_id = self.tg_client.create_project(name, description)
        if tg_project_id:
            self.tg_project_id = tg_project_id

    def delete_tg_project(self, tg_project_id, instance="test"):
        if not self.tg_session_id:
            return False
        # delete tg-project at textgrid server
        res = self.tg_client.delete_project(tg_project_id)
        # delete tg-project at local config if successful AND
        # is the currently defined project_id
        if res and tg_project_id == self.tg_project_id:
            self.tg_project_id = None
        return True

    def get_tg_projects(self, instance="test"):
        if not self.tg_session_id:
            return []
        return self.tg_client.get_assigned_projects()

    def get_tg_project_hits(self, project_id, instance="test"):
        if self.tg_session_id:
            return self.tg_client.get_project_content(project_id).hits

    def publish_tg_project(self, instance="test"):
        if not self.tg_session_id:
            return False

        # step 1: create required metadata
        for c_name in self.collections:
            collection = self.collections[c_name]
            collection["modeler"].render_collection()

        # step 2: push project to textgrid server
        for collection_name in self.collections:
            collection = self.collections[collection_name]
            self.tg_client.put_aggregation(
                self.tg_project_id,
                collection["modeler"].get_collection_path(),
            )


class CollectionParser(object):

    def __init__(self, collection):
        self.collection = collection
        self._elements = None

    @property
    def elements(self):
        if self._elements is None:
            self._elements = []
            for file in self.collection.elements:
                self._elements.append(
                    {
                        "file": file,
                        "tei_parser": TEIParser(fullpath=file["fullpath"]),
                    }
                )
        return self._elements

    def test_xpath(self, xpath):
        results = []
        for element in self.elements:
            result = element["tei_parser"].find(xpath)
            print(result)
            if result is not None:
                results.append(
                    {
                        "filename": element["file"]["filename"],
                        "result": result,
                    }
                )
        return {
            "results": results,
            "count": {
                "total": len(self.collection.elements),
                "found": len(results),
                "percentage": round(
                    len(results) / len(self.collection.elements) * 100
                ),
            },
        }
