# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64

from .base64 import Base64

__all__: list[str] = [
    'Base64URLEncoded'
]



class Base64URLEncoded(Base64):
    __module__: str = 'libcanonical.types'

    @classmethod
    def b64decode(cls, value: str):
        return base64.urlsafe_b64decode(value)

    @classmethod
    def b64encode(cls, value: bytes | str) -> str:
        if isinstance(value, str):
            value = str.encode(value, 'utf-8')
        return  bytes.decode(base64.urlsafe_b64encode(value), 'ascii')