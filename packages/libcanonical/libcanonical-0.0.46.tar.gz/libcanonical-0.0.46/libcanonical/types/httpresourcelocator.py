# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any

from .stringtype import StringType


class HTTPResourceLocator(StringType):
    __module__: str = 'libcanonical.types'
    max_length = 2048
    protocols: set[str] = {'http', 'https'}
    description = (
        "An RFC HTTP resource locator, defined in RFC 3986 and RFC 9110, "
        "is a Uniform Resource Locator (URL) that specifies the location "
        "of a resource on the web, consisting of a scheme (http or https), "
        "an authority (domain or IP), an optional port, a path, an optional "
        "query, and an optional fragment (e.g., `https://example.com:8080/pa"
        "th?query=1#section`)."
    )

    @classmethod
    def validate(cls, v: str, _: Any = None):
        p = urllib.parse.urlparse(v)
        if p.scheme not in cls.protocols:
            raise ValueError(f"Not a valid URL: {v[:128]}")
        return cls(v)

    @property
    def query(self) -> dict[str, str | list[str]]:
        p =urllib.parse.urlparse(self)
        values: dict[str, list[str] | str] = {}
        for name, value in urllib.parse.parse_qs(p.query).items():
            if len(value) == 1:
                value = value[0]
            values[name] = value
        return values

    def with_query(self, **kwargs: Any) -> 'HTTPResourceLocator':
        p: list[str] = list(urllib.parse.urlparse(self))
        q = dict(urllib.parse.parse_qs(p[4]))
        q.update(kwargs)
        p[4] = urllib.parse.urlencode(q, doseq=True)
        return HTTPResourceLocator(urllib.parse.urlunparse(p))
        