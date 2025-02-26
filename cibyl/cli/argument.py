"""
#    Copyright 2022 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
from dataclasses import dataclass


# pylint: disable=too-many-instance-attributes
@dataclass
class Argument():
    """Represents Parser's argument"""

    name: str
    arg_type: object
    description: str
    nargs: int = 1
    func: str = None
    populated: bool = False
    level: int = 0
    value: object = None
