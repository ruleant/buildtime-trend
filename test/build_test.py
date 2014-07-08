# vim: set expandtab sw=4 ts=4:
#
# Unit tests for Trend class
#
# Copyright (C) 2014 Dieter Adriaenssens <ruleant@users.sourceforge.net>
#
# This file is part of buildtime-trend
# <https://github.com/ruleant/buildtime-trend/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from buildtimetrend.build import Build
from buildtimetrend.stages import Stages
from lxml import etree
import unittest

TEST_SAMPLE_FILE = 'test/testsample_timestamps.csv'


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.build = Build()
        # show full diff in case of assert mismatch
        self.maxDiff = None

    def test_novalue(self):
        # number of stages should be zero
        self.assertEquals(0, len(self.build.stages.stages))
        self.assertEquals(0, len(self.build.properties))

        # get properties should return zero duration
        self.assertDictEqual({'duration': 0}, self.build.get_properties())

        # dict should be empty
        self.assertDictEqual({'duration': 0, 'stages' : []}, self.build.to_dict())

        # list should be empty
        self.assertListEqual([], self.build.stages_to_list())

        # xml shouldn't contain items
        self.assertEquals(
            '<build><stages/></build>', etree.tostring(self.build.to_xml()))
        self.assertEquals(
            '<build>\n'
            '  <stages/>\n'
            '</build>\n', self.build.to_xml_string())

    def test_nofile(self):
        # number of stages should be zero when file doesn't exist
        self.build = Build('nofile.csv')
        self.assertEquals(0, len(self.build.stages.stages))

        self.build = Build('')
        self.assertEquals(0, len(self.build.stages.stages))

    def test_add_stages(self):
        self.build.add_stages(None)
        self.assertEquals(0, len(self.build.stages.stages))

        self.build.add_stages("string")
        self.assertEquals(0, len(self.build.stages.stages))

        stages = Stages()
        stages.read_csv(TEST_SAMPLE_FILE)
        self.build.add_stages(stages)
        self.assertEquals(3, len(self.build.stages.stages))

        # stages should not change when submitting an invalid object
        self.build.add_stages(None)
        self.assertEquals(3, len(self.build.stages.stages))

        self.build.add_stages("string")
        self.assertEquals(3, len(self.build.stages.stages))

        self.build.add_stages(Stages())
        self.assertEquals(0, len(self.build.stages.stages))

    def test_add_property(self):
        self.build.add_property('property1', 2)
        self.assertEquals(1, len(self.build.properties))
        self.assertDictEqual({'property1': 2}, self.build.properties)

        self.build.add_property('property2', 3)
        self.assertEquals(2, len(self.build.properties))
        self.assertDictEqual({'property1': 2, 'property2': 3}, self.build.properties)

        self.build.add_property('property2', 4)
        self.assertEquals(2, len(self.build.properties))
        self.assertDictEqual({'property1': 2, 'property2': 4}, self.build.properties)

    def test_get_property(self):
        self.build.add_property('property1', 2)
        self.assertEquals(2, self.build.get_property('property1'))

        self.build.add_property('property1', None)
        self.assertEquals(None, self.build.get_property('property1'))

        self.build.add_property('property2', 3)
        self.assertEquals(3, self.build.get_property('property2'))

        self.build.add_property('property2', 4)
        self.assertEquals(4, self.build.get_property('property2'))

    def test_get_property_does_not_exist(self):
        self.assertEquals(None, self.build.get_property('no_property'))

    def test_get_properties(self):
        self.build.add_property('property1', 2)
        self.assertDictEqual(
            {'duration': 0, 'property1': 2},
            self.build.get_properties())

        self.build.add_property('property2', 3)
        self.assertDictEqual(
            {'duration': 0, 'property1': 2, 'property2': 3},
            self.build.get_properties())

        self.build.add_property('property2', 4)
        self.assertDictEqual(
            {'duration': 0, 'property1': 2, 'property2': 4},
            self.build.get_properties())

    def test_to_dict(self):
        # read and parse sample file
        self.build = Build(TEST_SAMPLE_FILE)

        # test dict
        self.assertDictEqual(
            {'duration': 17, 'started_at': '2014-04-01T18:58:55',
            'stages':
            [{'duration': 2,
              'finished_at': '2014-04-01T18:58:57',
              'name': 'stage1',
              'started_at': '2014-04-01T18:58:55'},
             {'duration': 5,
              'finished_at': '2014-04-01T18:59:02',
              'name': 'stage2',
              'started_at': '2014-04-01T18:58:57'},
             {'duration': 10,
              'finished_at': '2014-04-01T18:59:12',
              'name': 'stage3',
              'started_at': '2014-04-01T18:59:02'}]
            },
            self.build.to_dict())

        # add properties
        self.build.add_property('property1', 2)
        self.build.add_property('property2', 3)
        # started_at property should override default value
        self.build.add_property('started_at', '2014-04-01T18:55:00')
        # test dict
        self.assertDictEqual(
            {'duration': 17, 'started_at': '2014-04-01T18:55:00',
            'property1': 2, 'property2': 3,
            'stages':
            [{'duration': 2,
              'finished_at': '2014-04-01T18:58:57',
              'name': 'stage1',
              'started_at': '2014-04-01T18:58:55'},
             {'duration': 5,
              'finished_at': '2014-04-01T18:59:02',
              'name': 'stage2',
              'started_at': '2014-04-01T18:58:57'},
             {'duration': 10,
              'finished_at': '2014-04-01T18:59:12',
              'name': 'stage3',
              'started_at': '2014-04-01T18:59:02'}]
            },
            self.build.to_dict())

    def test_stages_to_list(self):
        # read and parse sample file
        self.build = Build(TEST_SAMPLE_FILE)

        # test list
        self.assertListEqual(
            [{'stage': {'duration': 2,
              'finished_at': '2014-04-01T18:58:57',
              'name': 'stage1',
              'started_at': '2014-04-01T18:58:55'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:58:55'}},
            {'stage': {'duration': 5,
              'finished_at': '2014-04-01T18:59:02',
              'name': 'stage2',
              'started_at': '2014-04-01T18:58:57'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:58:55'}},
            {'stage': {'duration': 10,
              'finished_at': '2014-04-01T18:59:12',
              'name': 'stage3',
              'started_at': '2014-04-01T18:59:02'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:58:55'}},
            ],
            self.build.stages_to_list())

        # add properties
        self.build.add_property('property1', 2)
        self.build.add_property('property2', 3)
        # started_at property should override default value
        self.build.add_property('started_at', '2014-04-01T18:55:00')
        # test dict
        self.assertListEqual(
            [{'stage': {'duration': 2,
              'finished_at': '2014-04-01T18:58:57',
              'name': 'stage1',
              'started_at': '2014-04-01T18:58:55'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:55:00',
            'property1': 2, 'property2': 3}},
            {'stage': {'duration': 5,
              'finished_at': '2014-04-01T18:59:02',
              'name': 'stage2',
              'started_at': '2014-04-01T18:58:57'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:55:00',
            'property1': 2, 'property2': 3}},
            {'stage': {'duration': 10,
              'finished_at': '2014-04-01T18:59:12',
              'name': 'stage3',
              'started_at': '2014-04-01T18:59:02'},
            'build': {'duration': 17, 'started_at': '2014-04-01T18:55:00',
            'property1': 2, 'property2': 3}},
            ],
            self.build.stages_to_list())

    def test_to_xml(self):
        # read and parse sample file
        self.build = Build(TEST_SAMPLE_FILE)

        # test xml output
        self.assertEquals(
            '<build><stages><stage duration="2" name="stage1"/>'
            '<stage duration="5" name="stage2"/>'
            '<stage duration="10" name="stage3"/></stages></build>',
            etree.tostring(self.build.to_xml()))

        # add properties
        self.build.add_property('property1', 2)
        self.build.add_property('property2', 3)
        # test xml output
        self.assertEquals(
            '<build property1="2" property2="3">'
            '<stages><stage duration="2" name="stage1"/>'
            '<stage duration="5" name="stage2"/>'
            '<stage duration="10" name="stage3"/></stages></build>',
            etree.tostring(self.build.to_xml()))

    def test_to_xml_string(self):
        # read and parse sample file
        self.build = Build(TEST_SAMPLE_FILE)

        # test xml string output
        self.assertEquals(
            '<build>\n'
            '  <stages>\n'
            '    <stage duration="2" name="stage1"/>\n'
            '    <stage duration="5" name="stage2"/>\n'
            '    <stage duration="10" name="stage3"/>\n'
            '  </stages>\n'
            '</build>\n',
            self.build.to_xml_string())

        # add properties
        self.build.add_property('property1', 2)
        self.build.add_property('property2', 3)
        # test xml string output
        self.assertEquals(
            '<build property1="2" property2="3">\n'
            '  <stages>\n'
            '    <stage duration="2" name="stage1"/>\n'
            '    <stage duration="5" name="stage2"/>\n'
            '    <stage duration="10" name="stage3"/>\n'
            '  </stages>\n'
            '</build>\n',
            self.build.to_xml_string())
