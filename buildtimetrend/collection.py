# vim: set expandtab sw=4 ts=4:
'''
Dictionary based collection class.

Copyright (C) 2014 Dieter Adriaenssens <ruleant@users.sourceforge.net>

This file is part of buildtime-trend
<https://github.com/ruleant/buildtime-trend/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import copy


class Collection(object):
    '''
    Dictionary based collection object.
    '''

    def __init__(self):
        self.items = {}

    def add_item(self, name, value):
        '''
        Add an item to the collection

        Parameters :
        - name : Item name
        - value : Item value
        '''
        self.items[name] = value

    def get_item(self, name):
        '''
        Get an item from a collection

        Parameters :
        - name : Item name
        '''
        if name in self.items:
            return self.items[name]
        else:
            return None

    def get_items(self):
        '''
        Return items collection as dictionary
        '''
        # copy values of items collection
        return copy.deepcopy(self.items)
