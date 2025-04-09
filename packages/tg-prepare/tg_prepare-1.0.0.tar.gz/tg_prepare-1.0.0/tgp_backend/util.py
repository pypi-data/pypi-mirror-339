# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
import logging

import os
import re

from configparser import ConfigParser

log = logging.getLogger(__name__)


def config(section, parameter, default=None):
    _config = ConfigParser()
    _config.read("config.ini")

    if section not in _config:
        log.warn("Section: %s not in *.ini -> using default" % section)
        return default
    config_val = _config[section].get(parameter)
    if not config_val:
        log.info(
            "Parameter: %s not in section: (%s) of *.ini -> using default: %s"
            % (parameter, section, default)
        )
        return default
    else:
        return config_val


def cli_startup(log_level=logging.INFO, log_file=None):
    log_config = dict(
        level=log_level,
        format="%(asctime)s %(name)-10s %(levelname)-4s %(message)s",
    )
    if log_file:
        log_config["filename"] = log_file

    logging.basicConfig(**log_config)
    logging.getLogger("").setLevel(log_level)


def get_file_extension(fname):
    found_extension = re.search("\.[A-Za-z0-9]*$", fname, re.IGNORECASE)
    if found_extension:
        return found_extension[0][1:].lower()
    return ""


def list_files_and_folders(path):

    def recursive_list(dir_path, depth=0):
        items = []
        for entry in os.scandir(dir_path):
            if entry.name.startswith("."):
                continue

            if entry.is_dir():
                children = recursive_list(entry.path, depth=depth + 1)
                items.append(
                    {
                        "type": "folder",
                        "name": entry.name,
                        "depth": depth,
                        "path": entry.path,
                        "children": {"count": len(children), "list": children},
                    }
                )
            else:
                items.append(
                    {"type": "file", "name": entry.name, "depth": depth}
                )
        return items

    return recursive_list(path)


def remove_empty_strings_from_dict(d):
    for key in d:
        if d[key] == "":
            d[key] = None
    return d
