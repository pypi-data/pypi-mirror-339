# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import AsyncIterator
from typing import Protocol
from typing import TypeVar


T = TypeVar('T', bound='ITransaction')


class ITransaction(Protocol):
    __module__: str = 'tensorshield.types.protocols'

    async def transaction(
        self: T,
        transaction: T | None = None
    ) -> AsyncIterator[T]:
        ...