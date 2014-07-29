#!/usr/bin/env python
# vim: set expandtab sw=4 ts=4:
# Generate a read key for Keen.io trends
# Usage : get_read_key.py project_name
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

from buildtimetrend.keenio import keen_io_generate_read_key
import sys


if __name__ == "__main__":
    # define projectname
    # fe. project_name = "ruleant/buildtime-trend"
    project_name = "projectname"

    # get project name from argument
    if len(sys.argv) > 1:
        project_name = sys.argv[1]

    # generate a read key
    print keen_io_generate_read_key(project_name)
