# -*- coding=UTF-8 -*-
"""Filter used on cgtw server.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from six import text_type


class Filter(list):
    """CGteamwork style filter.  """

    def __init__(self, key, value, operator=None):
        if operator is None:
            operator = 'in' if isinstance(value, (list, tuple)) else '='
        super(Filter, self).__init__((key, operator, value))

    def __and__(self, other):
        return FilterList(self) & FilterList(other)

    def __or__(self, other):
        return FilterList(self) | FilterList(other)


class FilterList(list):
    """CGteamwork style filter list.  """

    def __init__(self, list_):
        assert isinstance(list_, (Filter, FilterList)), type(list_)
        if isinstance(list_, Filter):
            list_ = [list_]
        super(FilterList, self).__init__(list_)

    def _combine(self, other, operator):
        ret = FilterList(self)
        ret.append(operator)
        ret += FilterList(other)
        return ret

    def __and__(self, other):
        return self._combine(other, 'and')

    def __or__(self, other):
        return self._combine(other, 'or')


class Field(text_type):
    """Data base field name for filter.  """

    def __or__(self, value):
        return self.in_(value)

    def __and__(self, value):
        return self.has(value)

    def __eq__(self, value):
        return Filter(self, value, '=')

    def __gt__(self, value):
        return Filter(self, value, '>')

    def __lt__(self, value):
        return Filter(self, value, '<')

    def in_(self, value):
        """Represents matched data in value list.  """
        if isinstance(value, (str, text_type)):
            value = [value]
        return Filter(self, value, 'in')

    def has(self, value):
        """Represents data has value in it.  """
        return Filter(self, value, 'has')

    def contains(self, value):
        """Represents value in data item list.  """
        return Filter(self, value, 'concat')
