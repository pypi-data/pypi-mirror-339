# -*- coding: utf-8 -*-
# Copyright (C) 2023 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.deimport logging

import logging

from .util import config

log = logging.getLogger(__name__)

log_level = config("log", "level", default="INFO")
log_config = dict(
    level=log_level,
    format="%(asctime)s %(name)-10s %(levelname)-4s %(message)s",
)

logging.basicConfig(**log_config)
logging.getLogger("").setLevel(log_level)
