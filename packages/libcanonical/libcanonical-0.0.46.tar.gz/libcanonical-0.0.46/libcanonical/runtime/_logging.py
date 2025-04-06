# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from libcanonical.environ import defaults


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "libcanonical.utils.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True,
            'datefmt': '%Y-%m-%d %H:%M:%S.%f'
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "canonical": {"handlers": ["default"], "level": defaults.loglevel, "propagate": True},
        "canonical.error": {"level": "INFO"},
    },
}