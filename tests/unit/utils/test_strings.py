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
from unittest import TestCase

from cibyl.utils.strings import IndentedTextBuilder


class TestIndentedTextBuilder(TestCase):
    def test_add_multiple_levels(self):
        builder = IndentedTextBuilder(2)

        builder \
            .add('Header', 0) \
            .add('Section', 1) \
            .add('Paragraph', 2)

        expected = 'Header\n  Section\n    Paragraph'

        self.assertEqual(expected, builder.build())

    def test_can_modify_line(self):
        builder = IndentedTextBuilder()

        builder.add('Text1,', 0)
        builder[0].append('Text2')

        expected = 'Text1,Text2'

        self.assertEqual(expected, builder.build())

    def test_nested_builders(self):
        builder1 = IndentedTextBuilder()
        builder2 = IndentedTextBuilder()

        builder1.add('Header', 0)
        builder1.add('Section', 1)

        builder2.add('Paragraph 1', 0)
        builder2.add('List 1', 1)

        builder1.add(builder2.build(), 2)

        expected = 'Header\n  Section\n    Paragraph 1\n      List 1'

        self.assertEqual(expected, builder1.build())
