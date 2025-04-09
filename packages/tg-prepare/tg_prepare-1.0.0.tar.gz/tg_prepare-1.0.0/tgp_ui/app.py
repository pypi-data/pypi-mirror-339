# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de

import logging

import click  # type: ignore
import os
import shutil

from json import loads
from flask import Flask, render_template, request, redirect, session  # type: ignore
from flask import url_for as default_url_for  # type: ignore
from flask_json import json_response, FlaskJSON  # type: ignore

from tgp_backend.directories import generateList
from tgp_backend.project import Project, TGProject

from tgp_backend.auth import SecretKeyManager
from tgp_backend.nextcloud import Nextcloud
from tgp_backend.util import config
from tgp_backend.util import remove_empty_strings_from_dict

from tg_model.tei import TEIParser  # type: ignore

log = logging.getLogger(__name__)

base_params = {
    "title": "TG Prepare",
}

MAIN_PATH = config("main", "path", default="./projects")

app = Flask(__name__)
FlaskJSON(app)


secret_manager = SecretKeyManager(MAIN_PATH)
app.secret_key = secret_manager.secret_key

# Additional security settings, if not in DEBUG mode
app.config.update(SESSION_COOKIE_NAME="tgp_nextcloud_session")
if config("log", "level", default="DEBUG") != "DEBUG":
    app.config.update(
        SESSION_COOKIE_SECURE=True,  # Only allow cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to cookies
        SESSION_COOKIE_SAMESITE="Strict",  # Protect against CSRF attacks
    )

app.jinja_env.globals.update(len=len, round=round)


# Function to retrieve the prefix from headers, used for reverse proxy setups
def get_prefix():
    return request.headers.get(
        "X-Forwarded-Prefix", request.headers.get("X-Script-Name", "")
    )


# Custom implementation of Flask's url_for to include the prefix
def url_for(*args, **kwargs):
    """Overrides Flask's url_for globally to include the prefix"""
    return get_prefix() + default_url_for(*args, **kwargs)


# Context processor to inject the custom url_for into the Jinja2 templates
@app.context_processor
def inject_url_for():
    return dict(url_for=url_for)


def get_projects():
    projects = []
    for sub in os.listdir(MAIN_PATH):
        projectpath = "%s/%s" % (MAIN_PATH, sub)
        if os.path.isdir(projectpath):
            projects.append(Project(sub))
    return projects


app.jinja_env.globals.update(title="TG Prepare", get_projects=get_projects)


def _startup():

    # Create the projects directory if it does not exist
    if not os.path.exists(MAIN_PATH):
        os.makedirs(MAIN_PATH)

    logging.getLogger("zeep").setLevel(logging.INFO)
    app.run(
        host=config("main", "host", default="0.0.0.0"),
        port=config("main", "port", default=8077),
        debug=config("log", "level", default="DEBUG") == "DEBUG",
    )


@click.command()
@click.option("--path", "-p", default=None)
def startup(path):
    base_params["path"] = path if path else os.getcwd()
    _startup()


# *****************
# VIEWS
# *****************
@app.route(
    "/sidebar",
    methods=["GET", "POST"],
)
def sidebar():

    return render_template(
        "layout2.html",
    )


@app.route(
    "/xpath_parser_modal/<string:projectname>/<string:title>",
    methods=["GET", "POST"],
)
def xpath_parser_modal(projectname=None, title=None):
    project = Project(projectname)
    collection = project.get_collection(title)
    # collection_config = collection["config"]
    collection_parser = collection["parser"]

    return render_template(
        "xpath_parser_modal_content.html",
        # collection=collection_config,
        collection_parser=collection_parser,
    )


@app.route("/new_project", methods=["POST"])
def new_project():
    project = Project(request.form.get("projectname"))
    project.create()
    return redirect(url_for("project", projectname=project.name))


@app.route("/upload_files/<string:projectname>", methods=["POST"])
def upload_files(projectname=None):
    Project(projectname).file_upload(request.files.getlist("files"))

    return redirect(url_for("project", projectname=projectname))


@app.route(
    "/collection/<string:projectname>/<string:name>", methods=["GET", "POST"]
)
def collection(projectname, name):
    project = Project(projectname)
    collection = project.get_collection(name)
    return render_template(
        "collection.html",
        project=project,
        collection_title=name,
        collection=collection["config"],
    )


@app.route("/project/<string:projectname>", methods=["GET", "POST"])
def project(projectname=None):
    params = {
        "sub_title": "Project: %s" % projectname,
        "sub_description": "",
    }
    params.update(base_params)

    return render_template(
        "project.html",
        user=session.get("user", "-"),
        current_project=projectname,
        project=Project(projectname),
        tab=request.args.get("tab"),
        **params,
    )


@app.route("/", methods=["GET"])
@app.route("/project", methods=["GET", "POST"])
@app.route("/projects", methods=["GET", "POST"])
def projects():
    params = {
        "sub_title": "Projects",
        "sub_description": "",
    }
    params.update(base_params)

    projectname = request.form.get("projectname")
    fullpath = f"{MAIN_PATH}/{projectname}"

    if request.method == "POST":
        if request.form.get("delete"):
            # Delete the project
            if fullpath.strip("/") == MAIN_PATH.strip("/"):
                log.error(f"Cannot delete main path ({MAIN_PATH})!")
            elif os.path.exists(fullpath):
                shutil.rmtree(fullpath)
            else:
                log.warning("Project does not exist!")

    # Get list of all existing projects/directories
    projects = []
    for sub in os.listdir(MAIN_PATH):
        projectpath = "%s/%s" % (MAIN_PATH, sub)
        if os.path.isdir(projectpath):
            projects.append(Project(sub))
            # projects.append({"name": sub, "fullpath": projectpath})

    return render_template("projects.html", projects=projects, **params)


@app.route(
    "/tei_explorer/<string:projectname>/<string:title>", methods=["GET"]
)
def tei_explorer(projectname, title):
    project = Project(projectname)
    dir_list_dict, file_list_dict = generateList(
        project.get_subproject_inpath(title)
    )

    return render_template(
        "tei_explorer.html",
        dir_list=dir_list_dict,
        file_list=file_list_dict,
        collection_title=title,
        project=project,
    )


# *****************
# JSON-REQUESTS
# *****************
@app.route("/load_tei_content", methods=["GET"])
def load_tei_content():
    path = request.args.get("path")
    log.debug("load_tei_content path: %s" % path)
    _type = request.args.get("type")
    if path is not None:
        tei_parser = TEIParser(fullpath=path)
        if _type == "header":
            return json_response(
                value="OK",
                content=tei_parser.find(
                    "//teiHeader", node_as_text=True
                ).decode("utf-8"),
            )
        elif _type == "text":
            return json_response(
                value="OK",
                content=tei_parser.find(".//text", node_as_text=True).decode(
                    "utf-8"
                ),
            )
        return json_response(value="Unknown type requested!")


@app.route(
    "/set_configs/<string:projectname>/<string:title>", methods=["POST"]
)
def save_collection(projectname, title):
    project = Project(projectname)
    collection = project.get_collection(title)
    collection_config = collection["config"]
    for _attrib in request.form:
        attrib = _attrib.replace("[]", "")
        if attrib in collection_config.multi_attribs:
            value = [
                remove_empty_strings_from_dict(loads(v))
                for v in request.form.getlist(_attrib)
            ]
        elif attrib in collection_config.xpath_or_value_attribs:
            value = remove_empty_strings_from_dict(
                loads(request.form.get(attrib))
            )
        else:
            value = request.form.get(attrib)
        setattr(collection_config, attrib, value)
    collection_config.save()
    return json_response(response="OK")


@app.route("/nextcloud_tab/", methods=["POST"])
def nextcloud_tab():
    nextcloud = Nextcloud(**session)
    return render_template(
        "nxc_tab.html",
        nextcloud=nextcloud if nextcloud.test_connection() else None,
        user=session.get("username", "-"),
    )


@app.route("/nextcloud_login/", methods=["POST"])
def nextcloud_login():

    data = request.get_json()
    login_data = data.get("data", [])

    if Nextcloud(**login_data).test_connection():
        for key in login_data:
            session[key] = login_data[key]

    return json_response(login_succes=True)


@app.route("/nextcloud_logout", methods=["POST"])
def nextcloud_logout():
    session.clear()
    return json_response(response="OK")


@app.route("/nextcloud_download", methods=["POST"])
def nextcloud_download():
    data = request.get_json()
    projectname = data.get("projectname")
    file_paths = data.get("file_paths", [])
    nxt = Nextcloud(**session)
    nxt.download_nxc_files(file_paths, projectname)

    return json_response(response="OK")


@app.route("/clone_git_project/<string:projectname>", methods=["POST"])
def clone_git_project(projectname=None):
    Project(projectname).clone_git_project(request.form.get("github_repo"))

    return json_response(response="OK")


@app.route(
    "/check_xpath/<string:projectname>/<string:collectionname>",
    methods=["GET"],
)
def check_xpath(projectname, collectionname):
    project = Project(projectname)
    collection = project.get_collection(collectionname)
    collection_config = collection["config"]

    xpath = request.args.get("xpath")

    results = []

    for file in collection_config.elements:
        tei_parser = TEIParser(fullpath=file["fullpath"])
        result = tei_parser.find(xpath)
        if result is not None:
            results.append({"filename": file["filename"], "result": result})

    return json_response(value="OK", results=results)


@app.route("/set_configs/<string:projectname>", methods=["POST"])
def set_configs(projectname):
    Project(projectname).init_configs(request.form.getlist("tei_directories"))

    return json_response(response="OK")


@app.route(
    "/publish_project/<string:projectname>/<string:instance>", methods=["POST"]
)
def publish_project(projectname, instance):
    TGProject(projectname, instance).publish_tg_project()
    return json_response(response="OK")


@app.route(
    "/save_session_id/<string:projectname>/<string:instance>", methods=["POST"]
)
def save_session_id(projectname, instance):
    TGProject(projectname, instance).tg_session_id = request.form.get(
        "tg_auth_session_id"
    )

    return json_response(response="OK")


@app.route(
    "/save_tg_project_id/<string:projectname>/<string:instance>",
    methods=["POST"],
)
def save_tg_project_id(projectname, instance):
    TGProject(projectname, instance).tg_project_id = request.form.get(
        "tg_project_id"
    )
    return json_response(response="OK")


@app.route(
    "/delete_tg_project_id/<string:projectname>/<string:instance>/<string:tg_project_id>",
    methods=["POST"],
)
def delete_tg_project_id(projectname, instance, tg_project_id):
    TGProject(projectname, instance).delete_tg_project(tg_project_id)

    return json_response(response="OK")


@app.route(
    "/get_tg_project_hits/<string:projectname>/<string:instance>/<string:tg_project_id>",
    methods=["GET"],
)
def get_tg_project_hits(projectname, instance, tg_project_id):
    hits = TGProject(projectname, instance).get_tg_project_hits(tg_project_id)
    return json_response(response="OK", hits=hits)


@app.route(
    "/create_tg_project/<string:projectname>/<string:instance>",
    methods=["POST"],
)
def create_tg_project(projectname, instance):
    TGProject(projectname, instance).create_tg_project(
        request.form.get("tg_projectname")
    )
    return json_response(response="OK")


if __name__ == "__main__":
    startup()
