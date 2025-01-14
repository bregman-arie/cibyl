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
import logging

LOG = logging.getLogger(__name__)


def safe_request_generic(request, custom_error):
    """Decorator that wraps any errors coming out of a call around a
    custom_error class.

    :param request: The unsafe call to watch errors on.
    :return: The input call decorated to raise the desired error type.
    """

    def request_handler(*args):
        """Calls the unsafe function and wraps any errors coming out of it
        around a custom_error class.

        :param args: Arguments with which the function is called.
        :return: Output of the called function.
        """
        try:
            return request(*args)
        except Exception as ex:
            raise custom_error('Failure on request to target host.') from ex

    return request_handler


class Source:
    """Represents a source of a system on which queries are performed."""

    def __init__(self, name: str, url: str = None):
        self.name = name
        self.url = url

    # pylint: disable=unused-argument
    def query(self, system,  args):
        """Performs query on the source and populates environment instance"""
        LOG.info("performing query on %s", self.name)

    def connect(self):
        """Creates a client and initiates a connection to the source."""
        LOG.info("connection initiated: %s", self.name)
