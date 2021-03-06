# -*- coding=UTF-8 -*-
"""Database module selection.  """
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..filter import Filter
from .base import SelectionAttachment


class SelectionHistory(SelectionAttachment):
    """Get history of the selection.  """

    def _combine_filters(self, filters):
        _filters = Filter('#task_id', self.select)
        if filters:
            _filters &= filters
        return _filters

    def get(self, filters=None):
        """Get selection related history.
            filters (Filter or FilterList, optional): Defaults to None.
                Addtional history filters.

        Returns:
            tuple[HistoryInfo]: History records.
        """

        return self.select.module.get_history(
            self._combine_filters(filters))

    def count(self, filters=None):
        """Count selection related history records.

        Args:
            filters (Filter or FilterList):
                Addtional history filters.

        Returns:
            int: Records count.
        """

        return self.select.module.count_history(
            self._combine_filters(filters))

    # TODO: undo_data
