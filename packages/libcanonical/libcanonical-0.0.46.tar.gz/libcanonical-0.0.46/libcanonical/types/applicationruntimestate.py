# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import enum


class ApplicationRuntimeState(int, enum.Enum):
    BOOTING         = 0
    STARTUP         = 1
    LIVE            = 2
    READY           = 3
    BUSY            = 4
    TEARDOWN        = -1
    BOOTFAILURE     = -2
    RELOADFAILURE   = -3
    FATAL           = -99