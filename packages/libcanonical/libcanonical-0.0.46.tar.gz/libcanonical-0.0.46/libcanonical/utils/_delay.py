# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import time
from typing import Callable
from typing import TypeVar
from types import TracebackType


R = TypeVar('R')


class DelayContext:

    @property
    def remaining(self):
        elapsed = time.monotonic() - self.started
        remaining = max(self.delay - elapsed, 0.0)
        if remaining > 0.0 and self.timeout:
            timeout = self.timeout - self.latency
            remaining = min(timeout, remaining)
        return remaining

    def __init__(self, delay: float, timeout: float | None = None, latency: float = 1.0):
        self.delay = delay
        self.timeout = timeout or 0.0
        self.latency = latency
        if self.timeout == 0.0:
            self.latency = 0.0

    def sleep(self, func: Callable[[float], R]) -> R:
        return func(self.remaining)

    async def __aenter__(self):
        self.started = time.monotonic()
        return self

    async def __aexit__(
        self,
        cls: type[BaseException],
        exc: BaseException,
        tb: TracebackType
    ):
        if exc:
            raise exc
        await self.sleep(asyncio.sleep)

    def __enter__(self):
        self.started = time.monotonic()
        return self

    def __exit__(
        self,
        cls: type[BaseException],
        exc: BaseException,
        tb: TracebackType
    ):
        if exc:
            raise exc
        self.sleep(time.sleep)


delay = DelayContext